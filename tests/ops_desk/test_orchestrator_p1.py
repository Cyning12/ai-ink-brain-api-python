"""P1-3 Orchestrator Core 路由与 FSM 测试。"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops import chat, runs
from api.ops.orchestrator import Intent, classify_intent, is_fast_intent, review_result
from api.ops.store import OpsRunStore


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
    app.dependency_overrides[runs._store] = lambda: fake_store

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3) -> str:
        return '{"reasoning": "分析完成", "suggestion": "建议参与", "confidence": 0.85, "citations": [{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}]}'

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]]) -> str:
        return "综合建议：#545 值得参与。"

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    # issue_analyst / core import these names directly, so also patch their module bindings.
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    yield TestClient(app)
    app.dependency_overrides.clear()


def test_classify_fast_intents() -> None:
    assert classify_intent("指标趋势")[0] == Intent.METRICS_TREND
    assert classify_intent("issue list")[0] == Intent.ISSUE_LIST
    assert classify_intent("pulls")[0] == Intent.PR_LIST
    assert is_fast_intent(Intent.METRICS_TREND)


def test_classify_deep_intent() -> None:
    intent, slots = classify_intent("#545 适合我吗")
    assert intent == Intent.ISSUE_CONTRIBUTION
    assert slots.get("issue_number") == 545
    assert not is_fast_intent(intent)


def test_review_pass() -> None:
    queries = FakeQueries()
    result = {
        "confidence": 0.85,
        "evidence": [{"number": 545}],
        "citations": [{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}],
        "reasoning": "适合参与",
        "suggestion": "建议",
    }
    verdict, _ = review_result(result, queries)
    assert verdict == "pass"


def test_review_fail_missing_issue() -> None:
    queries = FakeQueries()
    result = {
        "confidence": 0.85,
        "evidence": [],
        "citations": [{"number": 999, "url": "https://github.com/MoonshotAI/kimi-code/issues/999"}],
        "reasoning": "适合参与",
        "suggestion": "建议",
    }
    verdict, detail = review_result(result, queries)
    assert verdict == "fail"
    assert detail["rule"] == "V1"


def test_chat_fast_metrics(client: TestClient) -> None:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "最近指标趋势"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "fast"
    assert data["status"] == "done"
    assert "answer" in data


def test_chat_deep_issue(client: TestClient) -> None:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我吗"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "deep"
    assert data["status"] in ("done", "partial")
    run_id = data["run_id"]

    events_resp = client.get(f"/api/py/ops/runs/{run_id}/events?after_seq=0", headers={"x-ops-secret": "test"})
    assert events_resp.status_code == 200
    events = events_resp.json()["events"]
    event_types = [e["event_type"] for e in events]
    assert "router.decision" in event_types
    assert "final.answer" in event_types


def test_get_run_and_retry(client: TestClient) -> None:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我吗"},
        headers={"x-ops-secret": "test"},
    )
    run_id = resp.json()["run_id"]

    get_resp = client.get(f"/api/py/ops/runs/{run_id}", headers={"x-ops-secret": "test"})
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == run_id

    retry_resp = client.post(
        f"/api/py/ops/runs/{run_id}/retry?retry_token=wrong", headers={"x-ops-secret": "test"}
    )
    assert retry_resp.status_code == 409


def test_stream_not_implemented(client: TestClient) -> None:
    resp = client.get("/api/py/ops/runs/run-1/stream", headers={"x-ops-secret": "test"})
    assert resp.status_code == 404
    assert resp.json()["detail"]["code"] == "SSE_NOT_IMPLEMENTED"
