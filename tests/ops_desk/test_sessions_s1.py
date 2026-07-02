"""S1 Session REST API 测试。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops import sessions
from tests.ops_desk.test_orchestrator_p1 import FakeDemoCache, FakeQueries, FakeStore


class SessionFakeStore(FakeStore):
    def list_runs_by_session_id(self, session_id: str, *, limit: int = 50) -> list[dict[str, Any]]:
        rows = [r for r in self.runs.values() if r.get("session_id") == session_id]
        rows.sort(key=lambda r: str(r.get("id", "")), reverse=True)
        return rows[:limit]

    def list_events_for_session(
        self,
        session_id: str,
        *,
        after_seq: int = 0,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        run_ids = {str(r["id"]) for r in self.list_runs_by_session_id(session_id)}
        events: list[dict[str, Any]] = []
        for run_id, evts in self.events.items():
            if run_id not in run_ids:
                continue
            events.extend(e for e in evts if e["seq"] > after_seq)
        events.sort(key=lambda e: e.get("seq", 0))
        return events[:limit]


@pytest.fixture
def sessions_root(tmp_path: Path) -> Path:
    root = tmp_path / "sessions"
    root.mkdir()
    return root


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, sessions_root: Path) -> TestClient:
    fake_queries = FakeQueries()
    fake_store = SessionFakeStore()

    app.dependency_overrides[sessions._queries] = lambda: fake_queries
    app.dependency_overrides[sessions._store] = lambda: fake_store
    app.dependency_overrides[sessions._demo_cache] = lambda: FakeDemoCache()
    app.dependency_overrides[sessions._sessions_root] = lambda: sessions_root

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        return LlmCompletionResult(
            content='{"reasoning": "分析完成", "suggestion": "建议参与", "confidence": 0.85, "citations": [{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}]}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step="analyze",
            ),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        return LlmCompletionResult(
            content="综合建议：#545 值得参与。",
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

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    yield TestClient(app)
    app.dependency_overrides.clear()


def test_create_and_list_sessions(client: TestClient) -> None:
    create_resp = client.post(
        "/api/py/ops/sessions",
        json={"slug": "s1-demo", "title": "S1 Demo"},
        headers={"x-ops-secret": "test"},
    )
    assert create_resp.status_code == 200
    data = create_resp.json()
    session_id = data["session_id"]
    assert session_id.startswith("sess_")
    assert data["meta"]["slug"] == "s1-demo"
    assert data["meta"]["status"] == "planning"

    list_resp = client.get("/api/py/ops/sessions", headers={"x-ops-secret": "test"})
    assert list_resp.status_code == 200
    items = list_resp.json()["items"]
    assert any(i["session_id"] == session_id for i in items)


def test_get_session_and_messages(client: TestClient) -> None:
    create_resp = client.post(
        "/api/py/ops/sessions",
        json={"slug": "msg-demo", "title": "Message Demo"},
        headers={"x-ops-secret": "test"},
    )
    session_id = create_resp.json()["session_id"]

    msg_resp = client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "最近指标趋势"},
        headers={"x-ops-secret": "test"},
    )
    assert msg_resp.status_code == 200
    msg_data = msg_resp.json()
    assert msg_data["session_id"] == session_id
    assert msg_data["route"] == "fast"
    run_id = msg_data["run_id"]

    detail_resp = client.get(f"/api/py/ops/sessions/{session_id}", headers={"x-ops-secret": "test"})
    assert detail_resp.status_code == 200
    detail = detail_resp.json()
    assert detail["meta"]["latest_run_id"] == run_id
    assert len(detail["recent_messages"]) >= 1

    events_resp = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    )
    assert events_resp.status_code == 200
    event_types = [e["event_type"] for e in events_resp.json()["events"]]
    assert "session.created" in event_types
    assert "session.status_changed" in event_types


def test_session_not_found(client: TestClient) -> None:
    resp = client.get("/api/py/ops/sessions/sess_missing_00000000", headers={"x-ops-secret": "test"})
    assert resp.status_code == 404
    assert resp.json()["detail"]["code"] == "SESSION_NOT_FOUND"
