"""S4.2 Session promote conflict action（block · overwrite · merge / diff 预览）测试。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.harness_runtime import promote as promote_mod
from api.harness_runtime.gate_sync.human_gate import HG_PROMOTE_OVERWRITE, patch_gate_and_sync
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
            content="S4.2 综合答复",
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


def _seed_conflict(client: TestClient, sessions_root: Path, slug: str) -> tuple[str, Path]:
    session_id = _approve_session(client, slug)
    session_dir = sessions_root / session_id
    preview = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/preview"
        "?target_repo=ai-ink-brain-api-python&target_branch=main",
        headers={"x-ops-secret": "test"},
    ).json()
    target = Path(preview["target_task_path"])
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("# existing target task\n\n> existing note\n", encoding="utf-8")
    return session_id, target


def test_s4_2_preview_diff_summary(client: TestClient) -> None:
    session_id = _approve_session(client, "s42-preview-diff")
    resp = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/preview"
        "?target_repo=ai-ink-brain-api-python&target_branch=main",
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "diff_summary" in data
    assert data["diff_summary"]["target_exists"] is False
    assert data["diff_summary"]["has_conflict"] is False
    assert "line_stats" in data["diff_summary"]


def test_s4_2_block_default_returns_conflict_and_diff(
    client: TestClient, sessions_root: Path
) -> None:
    session_id, target = _seed_conflict(client, sessions_root, "s42-block")
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
    detail = resp.json()["detail"]
    assert detail["code"] == "PROMOTE_CONFLICT"
    assert "diff_summary" in detail
    assert detail["diff_summary"]["has_conflict"] is True
    assert detail["diff_summary"]["line_stats"]["added"] > 0


def test_s4_2_block_explicit(client: TestClient, sessions_root: Path) -> None:
    session_id, _target = _seed_conflict(client, sessions_root, "s42-block-explicit")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "block",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "PROMOTE_CONFLICT"


def test_s4_2_overwrite_unconfirmed_without_gate(
    client: TestClient, sessions_root: Path
) -> None:
    session_id, _target = _seed_conflict(client, sessions_root, "s42-overwrite-unconfirmed")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "overwrite",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "PROMOTE_OVERWRITE_UNCONFIRMED"


def test_s4_2_overwrite_success_with_gate(
    client: TestClient, sessions_root: Path, target_repo_root: Path
) -> None:
    session_id, target = _seed_conflict(client, sessions_root, "s42-overwrite-success")
    session_dir = sessions_root / session_id
    patch_gate_and_sync(session_dir, HG_PROMOTE_OVERWRITE, "approved")

    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "overwrite",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["verify_passed"] is True
    assert target.is_file()
    target_text = target.read_text(encoding="utf-8")
    assert "promoted_from_session" in target_text
    assert "overwrite_of" in target_text
    assert "# existing target task" not in target_text

    events = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    ).json()["events"]
    assert "session.promoted" in [e["event_type"] for e in events]


def test_s4_2_merge_blocked_creates_draft(
    client: TestClient, sessions_root: Path
) -> None:
    session_id, _target = _seed_conflict(client, sessions_root, "s42-merge-blocked")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "merge",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    detail = resp.json()["detail"]
    assert detail["code"] == "PROMOTE_MERGE_BLOCKED"
    assert "merge_draft_path" in detail

    session_dir = sessions_root / session_id
    meta_path = session_dir / "session.meta.yaml"
    meta_text = meta_path.read_text(encoding="utf-8")
    import yaml

    latest_run_id = yaml.safe_load(meta_text).get("latest_run_id")
    assert latest_run_id
    draft_path = session_dir / "deliverables" / latest_run_id / "task_s42_merge_blocked_merged_v1.md"
    assert draft_path.is_file()
    draft_text = draft_path.read_text(encoding="utf-8")
    assert "<<<<<<< session draft" in draft_text or "# Merge Draft" in draft_text


def test_s4_2_merge_success_with_gate(
    client: TestClient, sessions_root: Path, target_repo_root: Path
) -> None:
    session_id, target = _seed_conflict(client, sessions_root, "s42-merge-success")
    session_dir = sessions_root / session_id
    patch_gate_and_sync(session_dir, HG_PROMOTE_OVERWRITE, "approved")

    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "merge",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["verify_passed"] is True
    assert target.is_file()
    target_text = target.read_text(encoding="utf-8")
    assert "promoted_from_session" in target_text
    assert "# Merge Draft" in target_text

    events = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    ).json()["events"]
    assert "session.promoted" in [e["event_type"] for e in events]


def test_s4_2_merge_base_missing(client: TestClient, sessions_root: Path) -> None:
    session_id = _approve_session(client, "s42-merge-missing")
    # 不创建目标文件，直接 merge
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "merge",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "PROMOTE_MERGE_BASE_MISSING"
