"""S2 Session LangGraph 00 编排测试。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.harness_runtime.graph.session_orchestrator_v1 import reset_checkpointer_for_tests
from api.index import app
from api.ops import sessions
from tests.ops_desk.test_orchestrator_p1 import FakeDemoCache, FakeStore


class S2FakeStore(FakeStore):
    def __init__(self) -> None:
        super().__init__()
        self.checkpoints: dict[str, dict[str, Any]] = {}

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

    def save_checkpoint(
        self, run_id: str, checkpoint_id: str, state_json: dict[str, Any]
    ) -> dict[str, Any]:
        key = f"{run_id}:{checkpoint_id}"
        row = {"run_id": run_id, "checkpoint_id": checkpoint_id, "state_json": state_json}
        self.checkpoints[key] = row
        return row


@pytest.fixture
def sessions_root(tmp_path: Path) -> Path:
    root = tmp_path / "sessions"
    root.mkdir()
    return root


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, sessions_root: Path) -> TestClient:
    reset_checkpointer_for_tests()
    fake_store = S2FakeStore()

    app.dependency_overrides[sessions._store] = lambda: fake_store
    app.dependency_overrides[sessions._demo_cache] = lambda: FakeDemoCache()
    app.dependency_overrides[sessions._sessions_root] = lambda: sessions_root

    yield TestClient(app)
    app.dependency_overrides.clear()
    reset_checkpointer_for_tests()


def _create_session(client: TestClient, slug: str = "s2-demo") -> str:
    resp = client.post(
        "/api/py/ops/sessions",
        json={"slug": slug, "title": "S2 Demo"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    return resp.json()["session_id"]


def test_s2_messages_00_graph_interrupt(client: TestClient) -> None:
    session_id = _create_session(client)
    msg_resp = client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "实现 LangGraph 00 授权流"},
        headers={"x-ops-secret": "test"},
    )
    assert msg_resp.status_code == 200
    data = msg_resp.json()
    assert data["route"] == "session_00"
    assert data.get("awaiting_auth") is True
    assert "计划摘要" in data["answer"]

    detail = client.get(f"/api/py/ops/sessions/{session_id}", headers={"x-ops-secret": "test"}).json()
    assert detail["meta"]["status"] == "awaiting_auth"


def test_s2_auth_approve_dual_write(client: TestClient, sessions_root: Path) -> None:
    session_id = _create_session(client, "s2-auth")
    client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "授权测试计划"},
        headers={"x-ops-secret": "test"},
    )

    auth_resp = client.post(
        f"/api/py/ops/sessions/{session_id}/auth",
        json={"action": "approve"},
        headers={"x-ops-secret": "test"},
    )
    assert auth_resp.status_code == 200
    body = auth_resp.json()
    assert body["status"] == "dispatched"
    assert "HG-SESSION-PLAN" in body["gate_summary"]["approved"]

    detail = client.get(f"/api/py/ops/sessions/{session_id}", headers={"x-ops-secret": "test"}).json()
    assert detail["meta"]["status"] == "dispatched"

    task_path = sessions_root / session_id / detail["meta"]["primary_task_path"]
    task_text = task_path.read_text(encoding="utf-8")
    assert "HG-SESSION-PLAN | approved" in task_text.replace("`", "")

    events = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    ).json()["events"]
    event_types = [e["event_type"] for e in events]
    assert "gate.approved" in event_types
    assert "session.dispatch" in event_types


def test_s2_auth_wrong_status(client: TestClient) -> None:
    session_id = _create_session(client, "s2-wrong")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/auth",
        json={"action": "approve"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "SESSION_STATUS_INVALID"


def test_s2_auth_idempotent(client: TestClient) -> None:
    session_id = _create_session(client, "s2-idem")
    client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "幂等测试"},
        headers={"x-ops-secret": "test"},
    )
    client.post(
        f"/api/py/ops/sessions/{session_id}/auth",
        json={"action": "approve"},
        headers={"x-ops-secret": "test"},
    )
    again = client.post(
        f"/api/py/ops/sessions/{session_id}/auth",
        json={"action": "approve"},
        headers={"x-ops-secret": "test"},
    )
    assert again.status_code == 200
    assert again.json().get("idempotent") is True
