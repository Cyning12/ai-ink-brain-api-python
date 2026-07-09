"""P1-3: Ops Chat 服务 FALLBACK 澄清路由单测。

覆盖：
- FALLBACK 进入 clarify 而不是直接 ReAct。
- clarify 返回需要澄清时，响应含 needs_clarification=true 且不含默认 #545。
- clarify 解析为具体 intent 时路由到 deep / fast。
- clarify 仍返回 fallback 时降级到 ReAct。
- 无 session_id 时 clarify 仍能工作。
"""

from __future__ import annotations

from typing import Any

import pytest

from api.ops.chat_service import ChatMessageRequest, handle_ops_chat_message
from api.ops.demo_cache import DemoClassifier


class FakeServiceStore:
    """内存版 OpsRunStore，支持 chat_service 所需方法。"""

    def __init__(self) -> None:
        self.runs: dict[str, dict[str, Any]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {}
        self._counter = 0

    def create_run(
        self,
        query: str,
        route: str,
        repo_owner: str = "MoonshotAI",
        repo_name: str = "kimi-code",
        session_id: str | None = None,
    ) -> dict[str, Any]:
        self._counter += 1
        run_id = f"run-{self._counter}"
        self.runs[run_id] = {
            "id": run_id,
            "query": query,
            "route": route,
            "session_id": session_id,
        }
        self.events[run_id] = []
        return self.runs[run_id]

    def append_event(
        self,
        run_id: str,
        agent_role: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
        seq: int | None = None,
    ) -> dict[str, Any]:
        evt: dict[str, Any] = {
            "run_id": run_id,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
            "seq": seq or len(self.events.get(run_id, [])) + 1,
        }
        self.events.setdefault(run_id, []).append(evt)
        return evt

    def update_run(self, run_id: str, **fields: Any) -> None:
        if run_id in self.runs:
            self.runs[run_id].update(fields)

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        self.update_run(run_id, metrics_json=metrics_json)

    def list_runs_by_session_id(self, session_id: str, *, limit: int = 50) -> list[dict[str, Any]]:
        return [r for r in self.runs.values() if r.get("session_id") == session_id][:limit]

    def get_events(self, run_id: str, after_seq: int = 0, limit: int = 200) -> list[dict[str, Any]]:
        return [e for e in self.events.get(run_id, []) if e.get("seq", 0) > after_seq][:limit]


class FakeServiceQueries:
    def fetch_issue_by_number(self, number: int) -> dict[str, Any] | None:
        return None

    def fetch_pull_by_number(self, number: int) -> dict[str, Any] | None:
        return None


class FakeDemoCache:
    def __init__(self) -> None:
        self.classifier = DemoClassifier()

    def get(self, demo_id: str) -> dict[str, Any] | None:
        return None

    def set(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        return {"demo_id": args[0] if args else None}


@pytest.fixture
def fake_service_store() -> FakeServiceStore:
    return FakeServiceStore()


@pytest.fixture
def fake_service_queries() -> FakeServiceQueries:
    return FakeServiceQueries()


@pytest.fixture
def fake_demo_cache() -> FakeDemoCache:
    return FakeDemoCache()


def test_fallback_enters_clarify_not_direct_react(
    monkeypatch: pytest.MonkeyPatch,
    fake_service_store: FakeServiceStore,
    fake_service_queries: FakeServiceQueries,
    fake_demo_cache: FakeDemoCache,
) -> None:
    """FALLBACK 应先进入 clarify，而不是直接 ReAct。"""
    from api.ops.orchestrator import clarify

    monkeypatch.setattr("api.ops.chat_service.classify_intent", lambda msg: ("fallback", {}))

    clarify_called = {"count": 0}

    def fake_clarify_if_fallback(*args: Any, **kwargs: Any) -> clarify.ClarifyResult:
        clarify_called["count"] += 1
        return clarify.ClarifyResult(
            needs_clarification=True,
            clarify_question="你想查询什么？",
        )

    react_called = {"count": 0}

    def fake_run_react_fallback(*args: Any, **kwargs: Any) -> dict[str, Any]:
        react_called["count"] += 1
        return {"status": "done", "answer": "react answer"}

    monkeypatch.setattr("api.ops.chat_service.clarify_if_fallback", fake_clarify_if_fallback)
    monkeypatch.setattr("api.ops.chat_service.run_react_fallback", fake_run_react_fallback)

    body = ChatMessageRequest(message="模糊问题", session_id="sess-1")
    result = handle_ops_chat_message(body, fake_service_queries, fake_service_store, fake_demo_cache)

    assert clarify_called["count"] == 1
    assert react_called["count"] == 0
    assert result["route"] == "clarify"
    assert result["status"] == "clarify"
    assert result["needs_clarification"] is True
    assert result["clarify_question"] == "你想查询什么？"
    assert "answer" not in result
    assert "issue_number" not in result

    # 验证 clarify run 记录了 clarify.asked 事件
    run_id = result["run_id"]
    clarify_events = [e for e in fake_service_store.events.get(run_id, []) if e["event_type"] == "clarify.asked"]
    assert len(clarify_events) == 1
    assert clarify_events[0]["payload"]["clarify_question"] == "你想查询什么？"


def test_fallback_clarify_resolved_routes_to_deep(
    monkeypatch: pytest.MonkeyPatch,
    fake_service_store: FakeServiceStore,
    fake_service_queries: FakeServiceQueries,
    fake_demo_cache: FakeDemoCache,
) -> None:
    """clarify 解析为 issue_contribution 时应路由到 deep。"""
    from api.ops.orchestrator import clarify

    monkeypatch.setattr("api.ops.chat_service.classify_intent", lambda msg: ("fallback", {}))

    def fake_clarify_if_fallback(*args: Any, **kwargs: Any) -> clarify.ClarifyResult:
        return clarify.ClarifyResult(
            needs_clarification=False,
            intent="issue_contribution",
            slots={"issue_number": 123},
        )

    deep_called: dict[str, Any] = {"args": None, "kwargs": None}

    def fake_run_deep(*args: Any, **kwargs: Any) -> dict[str, Any]:
        deep_called["args"] = args
        deep_called["kwargs"] = kwargs
        return {"status": "done", "answer": "deep answer", "issue_number": 123}

    monkeypatch.setattr("api.ops.chat_service.clarify_if_fallback", fake_clarify_if_fallback)
    monkeypatch.setattr("api.ops.chat_service.run_deep", fake_run_deep)

    body = ChatMessageRequest(message="那个 issue 适合吗", session_id="sess-1")
    result = handle_ops_chat_message(body, fake_service_queries, fake_service_store, fake_demo_cache)

    assert result["route"] == "deep"
    assert result["status"] == "done"
    assert deep_called["args"] is not None
    _, _, slots, *_ = deep_called["args"]
    assert slots == {"issue_number": 123}
    assert deep_called["kwargs"]["intent"] == "issue_contribution"
    assert deep_called["kwargs"]["session_id"] == "sess-1"


def test_fallback_clarify_resolved_routes_to_fast(
    monkeypatch: pytest.MonkeyPatch,
    fake_service_store: FakeServiceStore,
    fake_service_queries: FakeServiceQueries,
    fake_demo_cache: FakeDemoCache,
) -> None:
    """clarify 解析为 metrics_trend 时应路由到 fast。"""
    from api.ops.orchestrator import clarify

    monkeypatch.setattr("api.ops.chat_service.classify_intent", lambda msg: ("fallback", {}))

    def fake_clarify_if_fallback(*args: Any, **kwargs: Any) -> clarify.ClarifyResult:
        return clarify.ClarifyResult(
            needs_clarification=False,
            intent="metrics_trend",
            slots={"metric": "cycle-time", "days": 30},
        )

    fast_called: dict[str, Any] = {"args": None, "kwargs": None}

    def fake_run_fast(*args: Any, **kwargs: Any) -> dict[str, Any]:
        fast_called["args"] = args
        fast_called["kwargs"] = kwargs
        return {"status": "done", "answer": "fast answer"}

    monkeypatch.setattr("api.ops.chat_service.clarify_if_fallback", fake_clarify_if_fallback)
    monkeypatch.setattr("api.ops.chat_service.run_fast", fake_run_fast)

    body = ChatMessageRequest(message="最近情况怎样", session_id="sess-1")
    result = handle_ops_chat_message(body, fake_service_queries, fake_service_store, fake_demo_cache)

    assert result["route"] == "fast"
    assert result["answer"] == "fast answer"
    assert fast_called["args"] is not None
    _, _, intent, slots, *_ = fast_called["args"]
    assert intent == "metrics_trend"
    assert slots == {"metric": "cycle-time", "days": 30}


def test_fallback_clarify_resolved_fallback_routes_to_react(
    monkeypatch: pytest.MonkeyPatch,
    fake_service_store: FakeServiceStore,
    fake_service_queries: FakeServiceQueries,
    fake_demo_cache: FakeDemoCache,
) -> None:
    """clarify 仍返回 fallback 时应路由到 ReAct。"""
    from api.ops.orchestrator import clarify

    monkeypatch.setattr("api.ops.chat_service.classify_intent", lambda msg: ("fallback", {}))

    def fake_clarify_if_fallback(*args: Any, **kwargs: Any) -> clarify.ClarifyResult:
        return clarify.ClarifyResult(
            needs_clarification=False,
            intent="fallback",
            slots={},
        )

    react_called: dict[str, Any] = {"args": None, "kwargs": None}

    def fake_run_react_fallback(*args: Any, **kwargs: Any) -> dict[str, Any]:
        react_called["args"] = args
        react_called["kwargs"] = kwargs
        return {"status": "done", "answer": "react answer"}

    monkeypatch.setattr("api.ops.chat_service.clarify_if_fallback", fake_clarify_if_fallback)
    monkeypatch.setattr("api.ops.chat_service.run_react_fallback", fake_run_react_fallback)

    body = ChatMessageRequest(message="复杂对比问题", session_id="sess-1")
    result = handle_ops_chat_message(body, fake_service_queries, fake_service_store, fake_demo_cache)

    assert result["route"] == "react"
    assert result["answer"] == "react answer"
    assert react_called["args"] is not None
    assert react_called["args"][0] == result["run_id"]
    assert react_called["kwargs"]["session_id"] == "sess-1"


def test_fallback_clarify_without_session_id(
    monkeypatch: pytest.MonkeyPatch,
    fake_service_store: FakeServiceStore,
    fake_service_queries: FakeServiceQueries,
    fake_demo_cache: FakeDemoCache,
) -> None:
    """无 session_id 时 clarify 仍能工作。"""
    from api.ops.orchestrator import clarify

    monkeypatch.setattr("api.ops.chat_service.classify_intent", lambda msg: ("fallback", {}))

    def fake_clarify_if_fallback(*args: Any, **kwargs: Any) -> clarify.ClarifyResult:
        query, session_id, transcript, slots = args
        assert session_id is None
        assert transcript == []
        return clarify.ClarifyResult(
            needs_clarification=True,
            clarify_question="请补充信息。",
        )

    monkeypatch.setattr("api.ops.chat_service.clarify_if_fallback", fake_clarify_if_fallback)

    body = ChatMessageRequest(message="模糊问题", session_id=None)
    result = handle_ops_chat_message(body, fake_service_queries, fake_service_store, fake_demo_cache)

    assert result["route"] == "clarify"
    assert result["needs_clarification"] is True
    assert result["clarify_question"] == "请补充信息。"
