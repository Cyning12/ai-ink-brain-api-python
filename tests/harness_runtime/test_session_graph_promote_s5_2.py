"""S5.2 Session graph_delta promote API 测试。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.harness_runtime import promote as promote_mod
from api.harness_runtime.gate_sync.human_gate import patch_gate_and_sync
from api.harness_runtime.graph.session_orchestrator_v1 import reset_checkpointer_for_tests
from api.harness_runtime.promote import HG_PROMOTE_GRAPH
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
    (root / "docs/_tech_graph").mkdir(parents=True)
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
            content="S5.2 综合答复",
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


def _seed_graph_delta(
    client: TestClient,
    sessions_root: Path,
    slug: str,
    files: dict[str, str] | None = None,
    approve_graph_gate: bool = True,
) -> tuple[str, Path]:
    """创建 session 并写入 graph_delta 文件；返回 session_id 与 graph_delta 目录。"""
    session_id = _approve_session(client, slug)
    session_dir = sessions_root / session_id
    graph_dir = session_dir / "deliverables" / "graph_delta"
    graph_dir.mkdir(parents=True)

    default_files = {"00_main.md": "# Graph 00\n\nNew content.\n"}
    for name, body in (files or default_files).items():
        path = graph_dir / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(body, encoding="utf-8")

    if approve_graph_gate:
        patch_gate_and_sync(session_dir, HG_PROMOTE_GRAPH, "approved")

    return session_id, graph_dir


def test_s5_2_preview_returns_file_list_and_diff(client: TestClient, sessions_root: Path) -> None:
    session_id, _graph_dir = _seed_graph_delta(
        client, sessions_root, "s52-preview", approve_graph_gate=False
    )
    resp = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/graph/preview"
        "?target_repo=ai-ink-brain-api-python&target_branch=main",
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["session_id"] == session_id
    assert data["target_repo"] == "ai-ink-brain-api-python"
    assert data["source_graph_dir"] == "deliverables/graph_delta"
    assert len(data["files"]) == 1
    file_entry = data["files"][0]
    assert file_entry["source_path"] == "deliverables/graph_delta/00_main.md"
    assert file_entry["target_exists"] is False
    assert file_entry["diff_summary"]["has_conflict"] is False
    assert file_entry["diff_summary"]["line_stats"]["source_lines"] > 0


def test_s5_2_preview_invalid_target_repo(client: TestClient, sessions_root: Path) -> None:
    session_id, _graph_dir = _seed_graph_delta(
        client, sessions_root, "s52-invalid-repo", approve_graph_gate=False
    )
    resp = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/graph/preview"
        "?target_repo=unknown-repo&target_branch=main",
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 400
    detail = resp.json()["detail"]
    assert detail["code"] == "INVALID_TARGET_REPO"


def test_s5_2_preview_empty_graph_delta(client: TestClient, sessions_root: Path) -> None:
    session_id = _approve_session(client, "s52-empty")
    graph_dir = sessions_root / session_id / "deliverables" / "graph_delta"
    graph_dir.mkdir(parents=True)

    resp = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/graph/preview"
        "?target_repo=ai-ink-brain-api-python&target_branch=main",
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "GRAPH_DELTA_EMPTY"


def test_s5_2_preview_missing_graph_delta_dir(client: TestClient, sessions_root: Path) -> None:
    session_id = _approve_session(client, "s52-missing-dir")
    resp = client.get(
        f"/api/py/ops/sessions/{session_id}/promote/graph/preview"
        "?target_repo=ai-ink-brain-api-python&target_branch=main",
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "GRAPH_DELTA_EMPTY"


def test_s5_2_promote_gate_pending(client: TestClient, sessions_root: Path) -> None:
    session_id, _graph_dir = _seed_graph_delta(
        client, sessions_root, "s52-gate-pending", approve_graph_gate=False
    )
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    detail = resp.json()["detail"]
    assert detail["code"] == "GRAPH_PROMOTE_GATE_PENDING"


def test_s5_2_promote_requires_confirm(client: TestClient, sessions_root: Path) -> None:
    session_id, _graph_dir = _seed_graph_delta(client, sessions_root, "s52-noconfirm")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": False,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "PROMOTE_NOT_CONFIRMED"


def test_s5_2_promote_conflict_block(client: TestClient, sessions_root: Path, target_repo_root: Path) -> None:
    session_id, graph_dir = _seed_graph_delta(
        client, sessions_root, "s52-conflict-block", approve_graph_gate=True
    )
    target = target_repo_root / "docs/_tech_graph" / "00_main.md"
    target.write_text("# existing graph\n", encoding="utf-8")

    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "block",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 409
    detail = resp.json()["detail"]
    assert detail["code"] == "GRAPH_PROMOTE_CONFLICT"
    assert "diff_summary" in detail


def test_s5_2_promote_overwrite_success(
    client: TestClient, sessions_root: Path, target_repo_root: Path
) -> None:
    session_id, graph_dir = _seed_graph_delta(client, sessions_root, "s52-overwrite")
    target = target_repo_root / "docs/_tech_graph" / "00_main.md"
    target.write_text("# existing graph\n", encoding="utf-8")

    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
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
    assert data["conflict_action"] == "overwrite"
    assert len(data["copied_files"]) == 1
    assert target.is_file()
    assert "New content" in target.read_text(encoding="utf-8")

    events = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    ).json()["events"]
    assert "session.graph_promoted" in [e["event_type"] for e in events]


def test_s5_2_promote_merge_success(
    client: TestClient, sessions_root: Path, target_repo_root: Path
) -> None:
    session_id, graph_dir = _seed_graph_delta(
        client,
        sessions_root,
        "s52-merge",
        files={"00_main.md": "# Graph 00\n\nSession delta line.\n"},
    )
    target = target_repo_root / "docs/_tech_graph" / "00_main.md"
    target.write_text("# Graph 00\n\nTarget existing line.\n", encoding="utf-8")

    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
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
    assert data["conflict_action"] == "merge"
    merged_text = target.read_text(encoding="utf-8")
    assert "# Merge Draft" in merged_text or "Session delta line" in merged_text

    events = client.get(
        f"/api/py/ops/sessions/{session_id}/events?after_seq=0",
        headers={"x-ops-secret": "test"},
    ).json()["events"]
    assert "session.graph_promoted" in [e["event_type"] for e in events]


def test_s5_2_promote_no_conflict_copies_files(
    client: TestClient, sessions_root: Path, target_repo_root: Path
) -> None:
    session_id, graph_dir = _seed_graph_delta(
        client,
        sessions_root,
        "s52-copy",
        files={
            "00_main.md": "# Graph 00\n",
            "nested/01_struct.md": "# Struct\n",
        },
    )
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
            "conflict_action": "block",
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert len(data["copied_files"]) == 2
    assert (target_repo_root / "docs/_tech_graph" / "00_main.md").is_file()
    assert (target_repo_root / "docs/_tech_graph" / "nested" / "01_struct.md").is_file()


def test_s5_2_promote_copy_failed(
    monkeypatch: pytest.MonkeyPatch,
    client: TestClient,
    sessions_root: Path,
) -> None:
    session_id, _graph_dir = _seed_graph_delta(client, sessions_root, "s52-copy-fail")

    def fake_write_text(*args: Any, **kwargs: Any) -> None:
        raise OSError("mock write failure")

    monkeypatch.setattr("pathlib.Path.write_text", fake_write_text)

    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 500
    assert resp.json()["detail"]["code"] == "GRAPH_PROMOTE_COPY_FAILED"


def test_s5_2_promote_graph_gate_approved_after_success(
    client: TestClient, sessions_root: Path, target_repo_root: Path
) -> None:
    session_id, _graph_dir = _seed_graph_delta(client, sessions_root, "s52-gate-approved")
    resp = client.post(
        f"/api/py/ops/sessions/{session_id}/promote/graph",
        json={
            "target_repo": "ai-ink-brain-api-python",
            "target_branch": "main",
            "confirm": True,
        },
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200

    detail = client.get(
        f"/api/py/ops/sessions/{session_id}", headers={"x-ops-secret": "test"}
    ).json()
    assert HG_PROMOTE_GRAPH in detail["gate_summary"]["approved"]
