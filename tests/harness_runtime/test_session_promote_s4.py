"""S4 Session promote · probe verify 测试。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.harness_runtime import promote as promote_mod
from api.harness_runtime.graph.session_orchestrator_v1 import reset_checkpointer_for_tests
from api.index import app
from api.ops import sessions
from tests.harness_runtime.test_session_orchestrator_s2 import S2FakeStore
from tests.harness_runtime.test_session_orchestrator_s3 import _approve_session
from tests.ops_desk.test_orchestrator_p1 import FakeDemoCache, FakeQueries


@pytest.fixture
def sessions_root(tmp_path: Path) -> Path:
    root = tmp_path / "sessions"
    root.mkdir()
    return root


@pytest.fixture
def target_repo_root(tmp_path: Path) -> Path:
    root = tmp_path / "api-python"
    (root / "docs/tasks/active").mkdir(parents=True)
    return root


@pytest.fixture
def client(
    monkeypatch: pytest.MonkeyPatch,
    sessions_root: Path,
    target_repo_root: Path,
) -> TestClient:
    reset_checkpointer_for_tests()
    promote_mod.clear_repo_root_overrides()
    promote_mod.set_repo_root_override("ai-ink-brain-api-python", target_repo_root)

    fake_store = S2FakeStore()
    app.dependency_overrides[sessions._queries] = lambda: FakeQueries()
    app.dependency_overrides[sessions._store] = lambda: fake_store
    app.dependency_overrides[sessions._demo_cache] = lambda: FakeDemoCache()
    app.dependency_overrides[sessions._sessions_root] = lambda: sessions_root

    monkeypatch.setattr("api.harness_runtime.promote.probe_runner.probe_available", lambda: True)
    monkeypatch.setattr(
        "api.harness_runtime.promote.probe_runner.verify_task",
        lambda task_path, repo_root=None, ci=True, timeout=300: (
            True,
            {"passed": True, "task": str(task_path)},
        ),
    )

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
            content="S4 综合答复",
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
    promote_mod.clear_repo_root_overrides()
    reset_checkpointer_for_tests()


def test_s4_promote_preview(client: TestClient) -> None:
    session_id = _approve_session(client, "s4-preview")
    resp = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/preview"
        "?target_repo=ai-ink-brain-api-python&target_branch=main",
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["session_id"] == session_id
    assert data["target_repo"] == "ai-ink-brain-api-python"
    assert data["conflict"] is False


def test_s4_promote_success(client: TestClient, target_repo_root: Path, sessions_root: Path) -> None:
    session_id = _approve_session(client, "s4-promote")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["verify_passed"] is True
    target = Path(data["target_task_path"])
    assert target.is_file()
    assert "promoted_from_session" in target.read_text(encoding="utf-8")

    events = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    ).json()["events"]
    assert "session.promoted" in [e["event_type"] for e in events]


def test_s4_promote_verify_failed(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
    target_repo_root: Path,
) -> None:
    monkeypatch.setattr(
        "api.harness_runtime.promote.probe_runner.verify_task",
        lambda *args, **kwargs: (False, {"passed": False, "reason": "mock fail"}),
    )
    session_id = _approve_session(client, "s4-verify-fail")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "VERIFY_FAILED"
    assert not list((target_repo_root / "docs/tasks/active").glob("task_*.md"))


def test_s4_promote_conflict(client: TestClient, target_repo_root: Path) -> None:
    session_id = _approve_session(client, "s4-conflict")
    preview = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/preview"
        "?target_repo=ai-ink-brain-api-python",
        headers={"x-ops-secret": "test"},
    ).json()
    target = Path(preview["target_task_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# existing\n", encoding="utf-8")

    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "PROMOTE_CONFLICT"


def test_s4_promote_requires_confirm(client: TestClient) -> None:
    session_id = _approve_session(client, "s4-noconfirm")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": False,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "PROMOTE_NOT_CONFIRMED"
