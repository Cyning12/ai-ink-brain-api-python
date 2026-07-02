"""S3 Session subagent dispatch 测试。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.harness_runtime.graph.session_orchestrator_v1 import reset_checkpointer_for_tests
from api.index import app
from api.ops import sessions
from tests.harness_runtime.test_session_orchestrator_s2 import S2FakeStore, _create_session
from tests.ops_desk.test_orchestrator_p1 import FakeDemoCache, FakeQueries


@pytest.fixture
def sessions_root(tmp_path: Path) -> Path:
    root = tmp_path / "sessions"
    root.mkdir()
    return root


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch, sessions_root: Path) -> TestClient:
    reset_checkpointer_for_tests()
    fake_store = S2FakeStore()
    fake_queries = FakeQueries()

    app.dependency_overrides[sessions._queries] = lambda: fake_queries
    app.dependency_overrides[sessions._store] = lambda: fake_store
    app.dependency_overrides[sessions._demo_cache] = lambda: FakeDemoCache()
    app.dependency_overrides[sessions._sessions_root] = lambda: sessions_root

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        return LlmCompletionResult(
            content='{"reasoning": "ok", "suggestion": "参与", "confidence": 0.8, "citations": []}',
            usage=LlmUsage(
                provider="siliconflow",
                model="test",
                prompt_tokens=1,
                completion_tokens=1,
                total_tokens=2,
                latency_ms=1,
                step="analyze",
            ),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        return LlmCompletionResult(
            content="S3 综合答复",
            usage=LlmUsage(
                provider="siliconflow",
                model="test",
                prompt_tokens=1,
                completion_tokens=1,
                total_tokens=2,
                latency_ms=1,
                step="synthesize",
            ),
        )

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    yield TestClient(app)
    app.dependency_overrides.clear()
    reset_checkpointer_for_tests()


def _approve_session(client: TestClient, slug: str) -> str:
    session_id = _create_session(client, slug)
    client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "实现 subagent 派工"},
        headers={"x-ops-secret": "test"},
    )
    client.post(
        f"/api/py/ops/sessions/{session_id}/auth",
        json={"action": "approve"},
        headers={"x-ops-secret": "test"},
    )
    return session_id


def test_s3_dispatched_runs_subagent(client: TestClient) -> None:
    session_id = _approve_session(client, "s3-disp")
    msg = client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "最近指标趋势"},
        headers={"x-ops-secret": "test"},
    )
    assert msg.status_code == 200
    data = msg.json()
    assert data["route"] == "fast"
    assert data.get("answer")


def test_s3_deliverables_written(client: TestClient, sessions_root: Path) -> None:
    session_id = _approve_session(client, "s3-deliv")
    msg = client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "最近指标趋势"},
        headers={"x-ops-secret": "test"},
    )
    run_id = msg.json()["run_id"]
    result_path = sessions_root / session_id / "deliverables" / run_id / "result.json"
    assert result_path.is_file()

    # auth 路径 dispatch 落在 planning run_id 目录
    planning_runs = list((sessions_root / session_id / "deliverables").iterdir())
    assert len(planning_runs) >= 1


def test_s3_list_deliverables_endpoint(client: TestClient) -> None:
    session_id = _approve_session(client, "s3-list-deliv")
    client.post(
        f"/api/py/ops/sessions/{session_id}/messages",
        json={"message": "最近指标趋势"},
        headers={"x-ops-secret": "test"},
    )
    detail = client.get(
        f"/api/py/ops/sessions/{session_id}",
        headers={"x-ops-secret": "test"},
    ).json()
    assert detail["deliverables"]
    assert detail["deliverables"][0]["run_id"]

    listed = client.get(
        f"/api/py/ops/sessions/{session_id}/deliverables",
        headers={"x-ops-secret": "test"},
    ).json()
    assert listed["session_id"] == session_id
    assert len(listed["items"]) >= 1


def test_s3_auth_approve_dispatch_events(client: TestClient) -> None:
    session_id = _approve_session(client, "s3-auth-dispatch")
    events = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    ).json()["events"]
    types = [e["event_type"] for e in events]
    assert "session.dispatch" in types
    assert "session.subagent.ack" in types
    assert "session.review.pass" in types
