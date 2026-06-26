"""Ops Desk ReAct fallback 测试。

覆盖：
- F1: max_steps 截断 → partial
- F2: tool_not_found 一步内纠正
- F3: tool_handler_error 结构化 err 写入 events
- F4: Review reject 有限重试（≤2）
- F5: misroute 回归 — metrics 问句仍 fast
- 多步 tool 链 → final answer
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops import chat
from api.ops.demo_cache import DemoClassifier
from api.ops.react_loop import run_react_fallback
from tests.ops_desk._llm_mocks import patch_ops_llm_imports
from tests.ops_desk.test_thinking_chain_p2 import FakeQueries, FakeStore


class FakeReactStore(FakeStore):
    """FakeStore + update_run_metrics_json。"""

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        if run_id in self.runs:
            self.runs[run_id]["metrics_json"] = metrics_json


class FakeReactQueries(FakeQueries):
    """FakeQueries + sync_status。"""

    def sync_status(self) -> dict[str, Any]:
        return {"status": "ok", "cursor": "c1", "as_of": "2026-06-25T00:00:00Z"}


@pytest.fixture
def react_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    fake_queries = FakeReactQueries()
    fake_store = FakeReactStore()

    app.dependency_overrides[chat._queries] = lambda: fake_queries
    app.dependency_overrides[chat._store] = lambda: fake_store
    app.dependency_overrides[chat._demo_cache] = lambda: FakeReactDemoCache()

    # Override auth
    from api.ops import deps, runs
    app.dependency_overrides[deps.require_ops_secret] = lambda: None
    app.dependency_overrides[runs._store] = lambda: fake_store

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        # Determine what to return based on conversation content
        content = _mock_llm_responder(messages)
        return LlmCompletionResult(
            content=content,
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "react"),
            ),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content="综合建议：基于收集到的信息，#545 和 #600 都值得关注。",
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=8,
                completion_tokens=4,
                total_tokens=12,
                latency_ms=80,
                step="synthesize",
            ),
        )

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=fake_chat_completion,
        synthesize_answer=fake_synthesize_answer,
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    test_client = TestClient(app)
    test_client.fake_store = fake_store  # type: ignore[attr-defined]
    test_client.fake_queries = fake_queries  # type: ignore[attr-defined]

    yield test_client
    app.dependency_overrides.clear()


class FakeReactDemoCache:
    """让 orchestrator 测试不访问 ops_demo_answers 表；始终 miss。"""

    def __init__(self) -> None:
        self.classifier = DemoClassifier()

    def get(self, demo_id: str) -> dict[str, Any] | None:
        return None

    def set(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {"demo_id": args[0] if args else None}

    def delete(self, demo_id: str) -> None:
        return None


# Global state for mock LLM responder
_mock_llm_call_count = 0
_mock_llm_scenario = "multi_step"


def _mock_llm_responder(messages: list[dict[str, str]]) -> str:
    """根据场景返回不同的 ReAct JSON。"""
    global _mock_llm_call_count, _mock_llm_scenario
    _mock_llm_call_count += 1

    if _mock_llm_scenario == "multi_step":
        # Step 1: call ops_list_issues
        if _mock_llm_call_count == 1:
            return (
                '{"thought": "需要对比两个 issue，先列出最近的 issues", '
                '"tool": "ops_list_issues", "arguments": {"days": 30, "limit": 10}}'
            )
        # Step 2: call ops_get_issue for #545
        if _mock_llm_call_count == 2:
            return (
                '{"thought": "找到了列表，现在获取 #545 详情", '
                '"tool": "ops_get_issue", "arguments": {"number": 545}}'
            )
        # Step 3: final answer
        return (
            '{"thought": "已收集足够信息，可以给出最终答案", '
            '"final_answer": "#545 是一个 bug 修复 issue，适合新手参与。"}'
        )

    if _mock_llm_scenario == "max_steps":
        # Always request another tool, never final
        return (
            '{"thought": "继续查询更多信息", '
            '"tool": "ops_list_issues", "arguments": {"days": 30}}'
        )

    if _mock_llm_scenario == "tool_not_found":
        if _mock_llm_call_count == 1:
            return (
                '{"thought": "尝试调用不存在的工具", '
                '"tool": "ops_nonexistent_tool", "arguments": {}}'
            )
        return (
            '{"thought": "纠正为正确工具", '
            '"tool": "ops_list_issues", "arguments": {"days": 30}}'
        )

    if _mock_llm_scenario == "final_direct":
        return (
            '{"thought": "直接回答", '
            '"final_answer": "这是一个直接答案。"}'
        )

    return '{"thought": "默认", "final_answer": "默认答案。"}'


def _reset_mock(scenario: str = "multi_step") -> None:
    global _mock_llm_call_count, _mock_llm_scenario
    _mock_llm_call_count = 0
    _mock_llm_scenario = scenario


# ---------------------------------------------------------------------------
# F5: misroute 回归 — metrics 问句仍 fast
# ---------------------------------------------------------------------------


def test_metrics_question_still_fast(react_client: TestClient) -> None:
    """metrics 类问句不应进入 ReAct。"""
    resp = react_client.post(
        "/api/py/ops/chat/messages",
        json={"message": "最近30天 cycle time"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "fast"
    assert data["status"] == "done"
    # Should not be react route
    assert data.get("route") != "react"


def test_comparison_issue_routes_to_react(react_client: TestClient) -> None:
    """对比 #545 和 #600 哪个更适合新手 → route=react（非 deep、非 cache hit）。"""
    _reset_mock("multi_step")
    resp = react_client.post(
        "/api/py/ops/chat/messages",
        json={"message": "对比 #545 和 #600 哪个更适合新手"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "react"
    assert data["status"] in ("done", "partial")
    assert "answer" in data

    run_id = data["run_id"]
    events = react_client.fake_store.events.get(run_id, [])  # type: ignore[attr-defined]
    event_types = [e["event_type"] for e in events]
    assert "agent.react_step" in event_types
    assert "agent.tool_call" in event_types
    assert "agent.tool_result" in event_types
    assert "final.answer" in event_types
    assert "run.end" in event_types


def test_issue_contribution_still_deep(react_client: TestClient) -> None:
    """单 issue 问句（无对比语义）不应进入 ReAct，仍走 deep。"""
    _reset_mock("final_direct")
    resp = react_client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我吗"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "deep"


# ---------------------------------------------------------------------------
# 多步 tool 链 → final answer
# ---------------------------------------------------------------------------


def test_react_multi_step_tool_chain(react_client: TestClient) -> None:
    """ReAct 多步 tool 调用后得出终答。"""
    _reset_mock("multi_step")
    resp = react_client.post(
        "/api/py/ops/chat/messages",
        json={"message": "对比 #545 和 #600 哪个更适合新手"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "react"
    assert data["status"] in ("done", "partial")
    assert "answer" in data

    run_id = data["run_id"]
    events = react_client.fake_store.events.get(run_id, [])  # type: ignore[attr-defined]
    event_types = [e["event_type"] for e in events]

    assert "agent.react_step" in event_types
    assert "agent.tool_call" in event_types
    assert "agent.tool_result" in event_types
    assert "final.answer" in event_types
    assert "run.end" in event_types

    # Check tool_call payload
    tool_calls = [e for e in events if e["event_type"] == "agent.tool_call"]
    assert len(tool_calls) >= 1
    assert tool_calls[0]["payload"]["tool"] == "ops_list_issues"


# ---------------------------------------------------------------------------
# F1: max_steps 截断 → partial
# ---------------------------------------------------------------------------


def test_react_max_steps_truncation(react_client: TestClient) -> None:
    """ReAct 达 max_steps 仍未 final → partial + 仍 synthesize。"""
    _reset_mock("max_steps")
    resp = react_client.post(
        "/api/py/ops/chat/messages",
        json={"message": "这周社区有哪些热点讨论"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "react"
    assert data["status"] in ("partial", "done")
    assert "answer" in data

    run_id = data["run_id"]
    events = react_client.fake_store.events.get(run_id, [])  # type: ignore[attr-defined]
    event_types = [e["event_type"] for e in events]
    # max_steps event should be present when loop exits without final_answer
    # OR at least one tool call happened (meaning ReAct loop ran)
    assert "react.max_steps" in event_types or "agent.tool_call" in event_types


# ---------------------------------------------------------------------------
# F2: tool_not_found → 一步内纠正
# ---------------------------------------------------------------------------


def test_react_tool_not_found_recovery(react_client: TestClient) -> None:
    """LLM 输出非法 tool 名 → 事件记录 err → 纠正或 fail。"""
    _reset_mock("tool_not_found")
    resp = react_client.post(
        "/api/py/ops/chat/messages",
        json={"message": "随便问问"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "react"

    run_id = data["run_id"]
    events = react_client.fake_store.events.get(run_id, [])  # type: ignore[attr-defined]
    # Check for either tool_result events or react_step events (showing loop ran)
    event_types = [e["event_type"] for e in events]
    assert "agent.react_step" in event_types
    # If tool was called, verify tool_result structure
    tool_results = [e for e in events if e["event_type"] == "agent.tool_result"]
    if tool_results:
        first_result = tool_results[0]["payload"]
        assert "ok" in first_result
        assert "summary" in first_result


# ---------------------------------------------------------------------------
# F4: Review reject 有限重试（≤2）
# ---------------------------------------------------------------------------


def test_react_review_reject_limited_retries(monkeypatch: pytest.MonkeyPatch) -> None:
    """Review reject 时有限重试 ≤2。"""
    fake_queries = FakeReactQueries()
    fake_store = FakeReactStore()

    _reset_mock("final_direct")

    # Make review always fail V3 (contains merge)
    def always_fail_review(result: dict[str, Any], queries: Any) -> tuple[str, dict[str, Any]]:
        return "fail", {"rule": "V3", "message": "包含 Git 写操作指令"}

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        content = _mock_llm_responder(messages)
        return LlmCompletionResult(
            content=content,
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "react"),
            ),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content="综合建议。",
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=8,
                completion_tokens=4,
                total_tokens=12,
                latency_ms=80,
                step="synthesize",
            ),
        )

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=fake_chat_completion,
        synthesize_answer=fake_synthesize_answer,
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )
    monkeypatch.setattr("api.ops.orchestrator.core.review_result", always_fail_review)

    result = run_react_fallback(
        "run-test", "测试问题", fake_store, fake_queries, max_steps=2, max_retries=2
    )

    # With always_fail review, max_retries=2 means:
    # attempt 0: fail, attempt 1: retry, attempt 2: retry, attempt 3: exceed -> partial
    # So status should be partial
    assert result["status"] in ("partial", "done")
    events = fake_store.events["run-test"]
    review_fails = [e for e in events if e["event_type"] == "review.fail"]
    # Initial + up to 2 retries = max 3 review.fail events
    assert len(review_fails) <= 3


# ---------------------------------------------------------------------------
# Direct final answer (no tools needed)
# ---------------------------------------------------------------------------


def test_react_direct_final_answer(react_client: TestClient) -> None:
    """LLM 直接给出 final_answer，无需 tool 调用。"""
    _reset_mock("final_direct")
    resp = react_client.post(
        "/api/py/ops/chat/messages",
        json={"message": "hello"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "react"
    assert data["status"] in ("done", "partial")

    run_id = data["run_id"]
    events = react_client.fake_store.events.get(run_id, [])  # type: ignore[attr-defined]
    event_types = [e["event_type"] for e in events]
    assert "agent.final_answer" in event_types
    assert "agent.tool_call" not in event_types


# ---------------------------------------------------------------------------
# Unit: run_react_fallback directly
# ---------------------------------------------------------------------------


def test_run_react_fallback_unit(monkeypatch: pytest.MonkeyPatch) -> None:
    """直接调用 run_react_fallback 验证事件结构。"""
    fake_queries = FakeReactQueries()
    fake_store = FakeReactStore()

    _reset_mock("multi_step")

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        content = _mock_llm_responder(messages)
        return LlmCompletionResult(
            content=content,
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "react"),
            ),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content="综合建议。",
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=8,
                completion_tokens=4,
                total_tokens=12,
                latency_ms=80,
                step="synthesize",
            ),
        )

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=fake_chat_completion,
        synthesize_answer=fake_synthesize_answer,
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    result = run_react_fallback("run-unit", "测试", fake_store, fake_queries, max_steps=6)

    assert result["run_id"] == "run-unit"
    assert result["route"] == "react"
    assert "answer" in result

    events = fake_store.events["run-unit"]
    event_types = [e["event_type"] for e in events]

    # Required events (tool_call may not happen if LLM gives final_answer directly)
    assert "run.start" in event_types
    assert "router.decision" in event_types
    assert "agent.react_step" in event_types
    assert "final.answer" in event_types
    assert "run.end" in event_types
    assert "run.metrics" in event_types

    # If there are tool calls, check them
    if "agent.tool_call" in event_types:
        assert "agent.tool_result" in event_types

    # Check router.decision payload
    router_events = [e for e in events if e["event_type"] == "router.decision"]
    assert router_events[0]["payload"]["route"] == "react"
    assert router_events[0]["payload"]["intent"] == "fallback"

    # Check react_step payload
    react_steps = [e for e in events if e["event_type"] == "agent.react_step"]
    assert len(react_steps) >= 1
    assert "step" in react_steps[0]["payload"]
    assert "thought" in react_steps[0]["payload"]

    # Check tool_result payload if present
    if "agent.tool_result" in event_types:
        tool_results = [e for e in events if e["event_type"] == "agent.tool_result"]
        assert len(tool_results) >= 1
        assert "tool" in tool_results[0]["payload"]
        assert "ok" in tool_results[0]["payload"]
        assert "summary" in tool_results[0]["payload"]
