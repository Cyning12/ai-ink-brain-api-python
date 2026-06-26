"""Ops Desk eval_cases_v0 Tier A 回归：JSON 驱动 batch runner（P2-5b）。"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops import chat
from api.ops.orchestrator.core import review_result
from tests.ops_desk.test_demo_cache_p1 import FakeDemoCacheStore, FakeQueries, FakeStore
from tests.ops_desk._llm_mocks import patch_ops_llm_imports

FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "ops_desk_eval_cases_v0.json"
CHAT_HEADERS = {"x-ops-secret": "test"}


class EvalFakeStore(FakeStore):
    """FakeStore + metrics_json 写入（run_deep / cache hit 需要）。"""

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        if run_id in self.runs:
            self.runs[run_id]["metrics_json"] = metrics_json


def _load_eval_cases() -> dict[str, Any]:
    return json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))


def _tier_a_cases() -> list[dict[str, Any]]:
    data = _load_eval_cases()
    return [
        c
        for c in data["cases"]
        if c.get("tier") == "A" and c.get("enabled", True) is not False
    ]


def _case_by_id(case_id: str) -> dict[str, Any]:
    for case in _tier_a_cases():
        if case["id"] == case_id:
            return case
    raise KeyError(f"eval case not found: {case_id}")


def _clear_demo_cache(demo_cache: FakeDemoCacheStore, demo_ids: list[str]) -> None:
    for demo_id in demo_ids:
        demo_cache.delete(demo_id)


def _post_chat(client: TestClient, message: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": message},
        headers=CHAT_HEADERS,
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    run_id = data["run_id"]
    events = client.fake_store.events.get(run_id, [])  # type: ignore[attr-defined]
    return data, events


def _assert_expect(
    data: dict[str, Any],
    events: list[dict[str, Any]],
    expect: dict[str, Any],
    *,
    queries: FakeQueries | None = None,
) -> None:
    if "route" in expect:
        assert data["route"] == expect["route"]
    if "status" in expect:
        assert data["status"] == expect["status"]
    if "status_in" in expect:
        assert data["status"] in expect["status_in"]
    if "demo_hit" in expect:
        assert data["demo_hit"] is expect["demo_hit"]

    answer = str(data.get("answer") or "")
    must_any = expect.get("answer_must_contain_any") or []
    if must_any:
        assert any(token.lower() in answer.lower() for token in must_any), (
            f"answer missing any of {must_any!r}: {answer!r}"
        )
    for token in expect.get("answer_must_not_contain") or []:
        assert token.lower() not in answer.lower(), f"answer must not contain {token!r}: {answer!r}"

    llm_count = sum(1 for e in events if e["event_type"] == "llm.usage")
    if "llm_usage_events" in expect:
        assert llm_count == expect["llm_usage_events"]
    if "llm_usage_events_min" in expect:
        assert llm_count >= expect["llm_usage_events_min"]

    for evt_type in expect.get("events_must_include") or []:
        event_types = {e["event_type"] for e in events}
        assert evt_type in event_types, f"missing event {evt_type!r} in {event_types}"

    if "intent" in expect:
        router = [e for e in events if e["event_type"] == "router.decision"]
        assert router, "missing router.decision event"
        assert router[0]["payload"]["intent"] == expect["intent"]

    if "review_rules" in expect and queries is not None:
        fail_events = [e for e in events if e["event_type"] == "review.fail"]
        assert not fail_events, f"review.fail: {fail_events}"
        tool_results = [e for e in events if e["event_type"] == "agent.tool.result"]
        assert tool_results, "missing agent.tool.result for review"
        payload = tool_results[0]["payload"]
        analyst = {
            "reasoning": payload.get("reasoning", ""),
            "suggestion": payload.get("suggestion", ""),
            "confidence": payload.get("confidence", 0),
            "citations": payload.get("citations", []),
        }
        verdict, detail = review_result(analyst, queries)
        assert verdict != "fail", f"review_result fail: {detail}"
        for rule in expect["review_rules"]:
            if rule == "V4":
                continue
            if verdict == "pass":
                break


def _run_case(
    client: TestClient,
    case: dict[str, Any],
    *,
    queries: FakeQueries,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    setup = case.get("setup") or {}
    clear_ids = setup.get("clear_demo_cache")
    if clear_ids is not None:
        _clear_demo_cache(client.fake_demo_cache, clear_ids)  # type: ignore[attr-defined]

    data, events = _post_chat(client, case["message"])
    _assert_expect(data, events, case["expect"], queries=queries)
    return data, events


@pytest.fixture
def eval_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("OPS_DESK_SECRET_TEST", "test")

    fake_queries = FakeQueries()
    fake_store = EvalFakeStore()
    fake_demo_cache = FakeDemoCacheStore()

    app.dependency_overrides[chat._queries] = lambda: fake_queries
    app.dependency_overrides[chat._store] = lambda: fake_store
    app.dependency_overrides[chat._demo_cache] = lambda: fake_demo_cache

    def _append_llm_usage(run_id: str | None, store: Any, usage: Any) -> None:
        if not run_id or store is None:
            return
        store.append_event(
            run_id,
            "llm",
            "llm.usage",
            payload={
                "provider": usage.provider,
                "model": usage.model,
                "prompt_tokens": usage.prompt_tokens,
                "completion_tokens": usage.completion_tokens,
                "total_tokens": usage.total_tokens,
                "latency_ms": usage.latency_ms,
                "step": usage.step,
            },
            node_id=f"llm.{usage.step}",
        )

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        step = kwargs.get("step", "analyze")
        usage = LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            latency_ms=100,
            step=step,
        )
        _append_llm_usage(kwargs.get("run_id"), kwargs.get("store"), usage)
        return LlmCompletionResult(
            content=(
                '{"reasoning": "分析完成", "suggestion": "建议参与", '
                '"confidence": 0.85, "citations": [{"number": 545, '
                '"url": "https://github.com/MoonshotAI/kimi-code/issues/545"}]}'
            ),
            usage=usage,
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        usage = LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=8,
            completion_tokens=4,
            total_tokens=12,
            latency_ms=80,
            step="synthesize",
        )
        _append_llm_usage(kwargs.get("run_id"), kwargs.get("store"), usage)
        return LlmCompletionResult(
            content="综合建议：#545 值得参与。",
            usage=usage,
        )

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=fake_chat_completion,
        synthesize_answer=fake_synthesize_answer,
    )

    # A8 (react fallback) 使用专用 responder（多步 tool → final）
    _mock_react_call_count = 0

    def fake_react_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        nonlocal _mock_react_call_count
        _mock_react_call_count += 1

        step = kwargs.get("step", "react")
        usage = LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            latency_ms=100,
            step=step,
        )
        _append_llm_usage(kwargs.get("run_id"), kwargs.get("store"), usage)

        # First call: tool call; second call: final answer
        if _mock_react_call_count == 1:
            content = (
                '{"thought": "需要获取 issue 信息", '
                '"tool": "ops_list_issues", "arguments": {"days": 30, "limit": 10}}'
            )
        else:
            content = (
                '{"thought": "已收集信息", '
                '"final_answer": "项目整体架构分析：#545 是一个值得关注的 issue，'
                '涉及核心指标问题。建议查看相关指标数据。"}'
            )

        return LlmCompletionResult(content=content, usage=usage)

    monkeypatch.setattr("api.ops.react_loop.chat_completion", fake_react_chat_completion)

    test_client = TestClient(app)
    test_client.fake_demo_cache = fake_demo_cache  # type: ignore[attr-defined]
    test_client.fake_store = fake_store  # type: ignore[attr-defined]
    test_client.fake_queries = fake_queries  # type: ignore[attr-defined]

    yield test_client
    app.dependency_overrides.clear()


def test_eval_fixture_schema() -> None:
    data = _load_eval_cases()
    assert data["schema_version"] == "ops_desk_eval_cases_v0"
    assert data["freeze_id"] == "OPS-DESK-EVAL-CASES-V0"
    tier_a = _tier_a_cases()
    assert len(tier_a) == 8
    assert {c["id"] for c in tier_a} == {"A1", "A2", "A3", "A4", "A5", "A6", "A7", "A8"}


class TestEvalCasesV0TierA:
    """A1→A6 顺序跑：A5/A6 依赖前序写 cache。"""

    def test_eval_sequence_a1_through_a6(self, eval_client: TestClient) -> None:
        queries: FakeQueries = eval_client.fake_queries  # type: ignore[attr-defined]
        for case_id in ("A1", "A2", "A3", "A4", "A5", "A6"):
            _run_case(eval_client, _case_by_id(case_id), queries=queries)

    def test_a7_generic_metrics_baseline(self, eval_client: TestClient) -> None:
        case = _case_by_id("A7")
        _run_case(eval_client, case, queries=eval_client.fake_queries)  # type: ignore[attr-defined]

    def test_a8_fallback_clarification(self, eval_client: TestClient) -> None:
        case = _case_by_id("A8")
        _run_case(eval_client, case, queries=eval_client.fake_queries)  # type: ignore[attr-defined]
