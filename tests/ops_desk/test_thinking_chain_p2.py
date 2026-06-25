"""Ops Desk P2-4 Thinking Chain v2 测试。

覆盖：
- A1: citation url 归一化（Review V2 前用 DB html_url 替换）
- A2: analyze_issue 支持 review_feedback 注入
- A3: run_deep 重试环携带 feedback
- A4: agent.tool.result expanded payload（reasoning/suggestion/confidence/citations）
- A5: FALLBACK → fast 澄清（非 silent deep #545）
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops import chat
from api.ops.agents.issue_analyst import _normalize_citations, analyze_issue
from api.ops.demo_cache import DemoClassifier
from api.ops.orchestrator import Intent, classify_intent, is_fast_intent
from api.ops.orchestrator.core import run_deep
from api.ops.store.runs import OpsRunStore


class FakeDemoCache:
    """让现有 orchestrator 测试不访问 ops_demo_answers 表；始终 miss。"""

    def __init__(self) -> None:
        self.classifier = DemoClassifier()

    def get(self, demo_id: str) -> dict[str, Any] | None:
        return None

    def set(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {"demo_id": args[0] if args else None}

    def delete(self, demo_id: str) -> None:
        return None


class FakeQueries:
    def __init__(self) -> None:
        self.issues = {
            545: {
                "number": 545,
                "title": "Deep demo issue",
                "state": "open",
                "labels": ["bug"],
                "html_url": "https://github.com/MoonshotAI/kimi-code/issues/545",
            }
        }
        self.pulls: dict[int, dict[str, Any]] = {}

    def fetch_issue_by_number(self, number: int) -> dict[str, Any] | None:
        return self.issues.get(number)

    def fetch_pull_by_number(self, number: int) -> dict[str, Any] | None:
        return self.pulls.get(number)

    def cycle_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "cycle-time", "summary": {"avg_hours": 48.0}}

    def review_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "review-time", "summary": {"avg_hours": 12.0}}

    def issue_throughput_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "issue-throughput", "summary": {"total": 2}}

    def fetch_issues(
        self,
        days: int = 30,
        state: str | None = None,
        label: str | None = None,
        module: str | None = None,
        age: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = list(self.issues.values())
        if state:
            rows = [r for r in rows if r.get("state") == state]
        return rows, len(rows)

    def fetch_pulls(
        self,
        days: int = 30,
        state: str | None = None,
        ci: str | None = None,
        author: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = list(self.pulls.values())
        return rows, len(rows)


class FakeStore(OpsRunStore):
    def __init__(self) -> None:  # type: ignore[override]
        self.runs: dict[str, dict[str, Any]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {}
        self._counter = 0

    def create_run(
        self, query: str, route: str, repo_owner: str = "MoonshotAI", repo_name: str = "kimi-code", session_id: str | None = None
    ) -> dict[str, Any]:
        self._counter += 1
        run_id = f"run-{self._counter}"
        run = {
            "id": run_id,
            "repo_id": "repo-1",
            "query": query,
            "route": route,
            "status": "running" if route == "deep" else "done",
            "session_id": session_id,
            "retry_token": f"token-{self._counter}",
        }
        self.runs[run_id] = run
        self.events[run_id] = []
        return run

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        return self.runs.get(run_id)

    def update_run(self, run_id: str, **fields: Any) -> None:
        if run_id in self.runs:
            self.runs[run_id].update(fields)

    def append_event(
        self,
        run_id: str,
        agent_role: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
        seq: int | None = None,
    ) -> dict[str, Any]:
        if seq is None:
            seq = len(self.events.get(run_id, [])) + 1
        evt = {
            "run_id": run_id,
            "seq": seq,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
        }
        self.events.setdefault(run_id, []).append(evt)
        return evt

    def get_events(self, run_id: str, after_seq: int = 0, limit: int = 200) -> list[dict[str, Any]]:
        return [e for e in self.events.get(run_id, []) if e["seq"] > after_seq][:limit]

    def next_seq(self, run_id: str) -> int:
        return len(self.events.get(run_id, [])) + 1

    def validate_retry_token(self, run_id: str, retry_token: str) -> bool:
        run = self.get_run(run_id)
        return bool(run) and run.get("retry_token") == retry_token


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    fake_queries = FakeQueries()
    fake_store = FakeStore()

    app.dependency_overrides[chat._queries] = lambda: fake_queries
    app.dependency_overrides[chat._store] = lambda: fake_store
    app.dependency_overrides[chat._demo_cache] = lambda: FakeDemoCache()
    # Override auth to bypass secret check
    from api.ops import deps, runs
    app.dependency_overrides[deps.require_ops_secret] = lambda: None
    app.dependency_overrides[runs._store] = lambda: fake_store

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content='{"reasoning": "分析完成", "suggestion": "建议参与", "confidence": 0.85, "citations": [{"number": 545, "url": "https://wrong-url.com/545"}]}',
            usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=10, completion_tokens=5, total_tokens=15, latency_ms=100, step="analyze"),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content="综合建议：#545 值得参与。",
            usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=8, completion_tokens=4, total_tokens=12, latency_ms=80, step="synthesize"),
        )

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    yield TestClient(app)
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# A1: citation url 归一化
# ---------------------------------------------------------------------------


def test_normalize_citations_replaces_url_with_db_html_url() -> None:
    queries = FakeQueries()
    citations = [{"number": 545, "url": "https://wrong-url.com/545"}]
    normalized = _normalize_citations(citations, queries)
    assert len(normalized) == 1
    assert normalized[0]["number"] == 545
    assert normalized[0]["url"] == "https://github.com/MoonshotAI/kimi-code/issues/545"


def test_normalize_citations_keeps_url_for_missing_issue() -> None:
    queries = FakeQueries()
    citations = [{"number": 999, "url": "https://example.com/999"}]
    normalized = _normalize_citations(citations, queries)
    assert len(normalized) == 1
    assert normalized[0]["number"] == 999
    assert normalized[0]["url"] == "https://example.com/999"


# ---------------------------------------------------------------------------
# A2: analyze_issue 支持 review_feedback
# ---------------------------------------------------------------------------


def test_analyze_issue_includes_feedback_in_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    queries = FakeQueries()
    captured_messages: list[list[dict[str, str]]] = []

    def capture_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        captured_messages.append(messages)
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content='{"reasoning": "修正后分析", "suggestion": "建议", "confidence": 0.9, "citations": [{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}]}',
            usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=10, completion_tokens=5, total_tokens=15, latency_ms=100, step="analyze"),
        )

    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", capture_chat_completion)

    feedback = {"rule": "V2", "message": "url 不匹配"}
    result = analyze_issue("#545 适合我吗", 545, queries, review_feedback=feedback)

    assert result["found"] is True
    assert result["confidence"] == 0.9
    assert len(captured_messages) == 1
    prompt = captured_messages[0][0]["content"]
    assert "上一轮 Review 未通过" in prompt
    assert "V2" in prompt
    assert "url 不匹配" in prompt


# ---------------------------------------------------------------------------
# A3: run_deep 重试环携带 feedback
# ---------------------------------------------------------------------------


def test_run_deep_retry_carries_feedback(monkeypatch: pytest.MonkeyPatch) -> None:
    """Mock Review V3 fail on first attempt, then pass on retry."""
    fake_queries = FakeQueries()
    fake_store = FakeStore()

    analyze_call_count = 0

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        nonlocal analyze_call_count
        analyze_call_count += 1
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        # First attempt: V3 fail (contains merge)
        if analyze_call_count == 1:
            return LlmCompletionResult(
                content='{"reasoning": "建议 merge 这个 PR", "suggestion": "open PR", "confidence": 0.85, "citations": [{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}]}',
                usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=10, completion_tokens=5, total_tokens=15, latency_ms=100, step="analyze"),
            )
        # Retry: pass
        return LlmCompletionResult(
            content='{"reasoning": "分析完成", "suggestion": "建议参与", "confidence": 0.82, "citations": [{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}]}',
            usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=10, completion_tokens=5, total_tokens=15, latency_ms=100, step="analyze"),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content="综合建议：#545 值得参与。",
            usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=8, completion_tokens=4, total_tokens=12, latency_ms=80, step="synthesize"),
        )

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    result = run_deep("run-1", "#545 适合我吗", {"issue_number": 545}, fake_store, fake_queries, max_retries=2)

    assert result["status"] == "done"
    events = fake_store.events["run-1"]
    event_types = [e["event_type"] for e in events]

    # Should have review.fail then review.pass
    assert event_types.count("review.fail") == 1
    assert event_types.count("review.pass") == 1

    # Check first review.fail payload
    fail_events = [e for e in events if e["event_type"] == "review.fail"]
    assert len(fail_events) == 1
    assert fail_events[0]["payload"]["rule"] == "V3"

    # Check that analyze_issue was called twice (attempt 0 and retry)
    assert analyze_call_count == 2


# ---------------------------------------------------------------------------
# A4: agent.tool.result expanded payload
# ---------------------------------------------------------------------------


def test_agent_tool_result_expanded_payload(client: TestClient) -> None:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我吗"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    run_id = data["run_id"]

    events_resp = client.get(f"/api/py/ops/runs/{run_id}/events?after_seq=0", headers={"x-ops-secret": "test"})
    assert events_resp.status_code == 200
    events = events_resp.json()["events"]

    tool_result_events = [e for e in events if e["event_type"] == "agent.tool.result"]
    assert len(tool_result_events) >= 1
    payload = tool_result_events[0]["payload"]
    assert "reasoning" in payload
    assert "suggestion" in payload
    assert "confidence" in payload
    assert "citations" in payload
    assert isinstance(payload["citations"], list)


# ---------------------------------------------------------------------------
# A5: FALLBACK → fast 澄清
# ---------------------------------------------------------------------------


def test_fallback_fast_clarification_no_deep_run(client: TestClient) -> None:
    """P3-1: FALLBACK 现在走 ReAct 而非 fast 澄清；验证不进 deep。"""
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "你好"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    # P3-1: fallback now goes to react, not fast
    assert data["route"] in ("fast", "react")
    assert data["status"] in ("done", "partial")
    assert "answer" in data
    # Should NOT be a deep analysis result
    assert "综合建议" not in data["answer"]

    run_id = data["run_id"]
    events_resp = client.get(f"/api/py/ops/runs/{run_id}/events?after_seq=0", headers={"x-ops-secret": "test"})
    assert events_resp.status_code == 200
    events = events_resp.json()["events"]
    event_types = [e["event_type"] for e in events]
    assert "run.start" in event_types
    assert "final.answer" in event_types
    assert "run.end" in event_types
    # Should NOT have deep path events
    assert "agent.delegate.start" not in event_types
    assert "agent.tool.result" not in event_types


def test_fallback_no_issue_number_does_not_trigger_deep() -> None:
    intent, slots = classify_intent("随便问问")
    assert intent == Intent.FALLBACK
    assert slots == {}
    assert not is_fast_intent(intent)


# ---------------------------------------------------------------------------
# Regression: D4 Demo still works
# ---------------------------------------------------------------------------


def test_demo_d4_still_deep(client: TestClient) -> None:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我吗"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "deep"
    assert data["status"] in ("done", "partial")
