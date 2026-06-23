"""Ops Desk P2-3 Manual Sync 验收（mock httpx + Supabase）。"""

from __future__ import annotations

# 直接获取 router 模块对象（绕过 __init__ 的 re-export）
import importlib
from typing import Any

import httpx
import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops.sync.dispatch import GitHubDispatchError, dispatch_sync_workflow
from api.ops.sync.router import _store

_sync_router_mod = importlib.import_module("api.ops.sync.router")


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """隔离环境变量，避免泄漏真实 token。"""
    monkeypatch.delenv("OPS_GITHUB_DISPATCH_TOKEN", raising=False)
    monkeypatch.delenv("OPS_DESK_SECRET", raising=False)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_store(
    runs: list[dict[str, Any]] | None = None,
    artifacts: dict[str, dict[str, Any]] | None = None,
) -> Any:
    class FakeStore:
        def __init__(self) -> None:
            self.repo_id = "repo-uuid-1"
            self._runs = runs or []
            self._artifacts = artifacts or {}

        def ensure_repo(self, owner: str, name: str) -> str:
            return self.repo_id

        def get_recent_sync_runs(self, repo_id: str, *, limit: int = 20) -> list[dict[str, Any]]:
            return list(self._runs[:limit])

        def get_artifacts_by_run_ids(self, run_ids: list[str]) -> dict[str, dict[str, Any]]:
            return {rid: self._artifacts.get(rid, {}) for rid in run_ids}

    return FakeStore()


# ---------------------------------------------------------------------------
# dispatch_sync_workflow 单元测试
# ---------------------------------------------------------------------------


def test_dispatch_missing_token() -> None:
    with pytest.raises(GitHubDispatchError) as exc:
        dispatch_sync_workflow()
    assert "OPS_GITHUB_DISPATCH_TOKEN" in str(exc.value)
    assert exc.value.status_code is None


def test_dispatch_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")

    class FakeResponse:
        status_code = 204
        text = ""

    class FakeClient:
        def __init__(self, **_: Any) -> None:
            pass

        def __enter__(self) -> FakeClient:
            return self

        def __exit__(self, *args: Any) -> None:
            pass

        def post(self, url: str, headers: dict[str, Any], json: dict[str, Any]) -> FakeResponse:
            assert "workflows/ops_sync_kimi_code.yml/dispatches" in url
            assert json == {"ref": "main"}
            assert headers["Authorization"] == "Bearer ghp_test"
            return FakeResponse()

    monkeypatch.setattr("api.ops.sync.dispatch.httpx.Client", FakeClient)
    result = dispatch_sync_workflow()
    assert result["dispatched"] is True


def test_dispatch_github_403(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")

    class FakeResponse:
        status_code = 403
        text = "Forbidden"

    class FakeClient:
        def __init__(self, **_: Any) -> None:
            pass

        def __enter__(self) -> FakeClient:
            return self

        def __exit__(self, *args: Any) -> None:
            pass

        def post(self, url: str, headers: dict[str, Any], json: dict[str, Any]) -> FakeResponse:
            return FakeResponse()

    monkeypatch.setattr("api.ops.sync.dispatch.httpx.Client", FakeClient)
    with pytest.raises(GitHubDispatchError) as exc:
        dispatch_sync_workflow()
    assert exc.value.status_code == 403
    assert "403" in str(exc.value)


def test_dispatch_network_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")

    class FakeClient:
        def __init__(self, **_: Any) -> None:
            pass

        def __enter__(self) -> FakeClient:
            return self

        def __exit__(self, *args: Any) -> None:
            pass

        def post(self, url: str, headers: dict[str, Any], json: dict[str, Any]) -> None:
            raise httpx.ConnectError("connection refused")

    monkeypatch.setattr("api.ops.sync.dispatch.httpx.Client", FakeClient)
    with pytest.raises(GitHubDispatchError) as exc:
        dispatch_sync_workflow()
    assert exc.value.status_code is None
    assert "网络错误" in str(exc.value)


# ---------------------------------------------------------------------------
# trigger_sync 路由测试（使用 dependency_overrides + 直接模块属性 patch）
# ---------------------------------------------------------------------------


def test_trigger_503_token_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    store = _make_store(runs=[])
    app.dependency_overrides[_store] = lambda: store

    tc = TestClient(app)
    resp = tc.post("/api/py/ops/sync/trigger", headers={"x-ops-secret": ""})
    assert resp.status_code == 503
    assert resp.json()["detail"]["code"] == "DISPATCH_TOKEN_MISSING"
    app.dependency_overrides.clear()


def test_trigger_409_already_running(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")

    runs = [{"id": "run-1", "status": "running", "started_at": "2026-06-23T08:00:00Z"}]
    store = _make_store(runs=runs)
    app.dependency_overrides[_store] = lambda: store
    monkeypatch.setattr(_sync_router_mod, "has_active_sync_workflow_run", lambda *, token: False)

    tc = TestClient(app)
    resp = tc.post("/api/py/ops/sync/trigger", headers={"x-ops-secret": ""})
    assert resp.status_code == 409
    assert resp.json()["detail"]["code"] == "SYNC_ALREADY_RUNNING"
    app.dependency_overrides.clear()


def test_trigger_409_github_actions_active(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")

    store = _make_store(runs=[{"id": "run-1", "status": "success", "started_at": "2026-06-23T08:00:00Z"}])
    app.dependency_overrides[_store] = lambda: store
    monkeypatch.setattr(_sync_router_mod, "has_active_sync_workflow_run", lambda *, token: True)

    tc = TestClient(app)
    resp = tc.post("/api/py/ops/sync/trigger", headers={"x-ops-secret": ""})
    assert resp.status_code == 409
    assert resp.json()["detail"]["source"] == "github_actions"
    app.dependency_overrides.clear()


def test_trigger_502_github_fail(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")

    store = _make_store(runs=[])
    app.dependency_overrides[_store] = lambda: store
    monkeypatch.setattr(_sync_router_mod, "has_active_sync_workflow_run", lambda *, token: False)

    def fake_dispatch(*, token: str | None = None) -> dict[str, Any]:
        raise GitHubDispatchError("GitHub 403", status_code=403)

    monkeypatch.setattr(_sync_router_mod, "dispatch_sync_workflow", fake_dispatch)

    tc = TestClient(app)
    resp = tc.post("/api/py/ops/sync/trigger", headers={"x-ops-secret": ""})
    assert resp.status_code == 502
    assert resp.json()["detail"]["code"] == "GITHUB_DISPATCH_FAILED"
    app.dependency_overrides.clear()


def test_trigger_200_success(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")

    store = _make_store(runs=[{"id": "run-1", "status": "success", "started_at": "2026-06-23T07:00:00Z"}])
    app.dependency_overrides[_store] = lambda: store
    monkeypatch.setattr(_sync_router_mod, "has_active_sync_workflow_run", lambda *, token: False)

    dispatched = {"dispatched": True}
    monkeypatch.setattr(_sync_router_mod, "dispatch_sync_workflow", lambda *, token: dispatched)

    tc = TestClient(app)
    resp = tc.post("/api/py/ops/sync/trigger", headers={"x-ops-secret": ""})
    assert resp.status_code == 200
    body = resp.json()
    assert body["dispatched"] is True
    assert body["workflow"] == "ops_sync_kimi_code"
    assert body["repository"] == "Cyning12/ai-ink-brain-api-python"
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# list_sync_runs 路由测试
# ---------------------------------------------------------------------------


def test_list_runs_empty(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    store = _make_store(runs=[])
    app.dependency_overrides[_store] = lambda: store

    tc = TestClient(app)
    resp = tc.get("/api/py/ops/sync/runs", headers={"x-ops-secret": ""})
    assert resp.status_code == 200
    assert resp.json()["runs"] == []
    app.dependency_overrides.clear()


def test_list_runs_with_artifacts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    runs = [
        {
            "id": "run-1",
            "started_at": "2026-06-23T08:00:00Z",
            "finished_at": "2026-06-23T08:05:00Z",
            "status": "success",
            "trigger": "cron",
            "records_issue": 5,
            "records_pr": 3,
            "error_message": None,
        },
        {
            "id": "run-2",
            "started_at": "2026-06-23T07:00:00Z",
            "finished_at": None,
            "status": "running",
            "trigger": "manual",
            "records_issue": 0,
            "records_pr": 0,
            "error_message": None,
        },
    ]
    artifacts = {
        "run-1": {"scan_snapshot_id": "scan-1", "graph_snapshot_id": "graph-1"},
        "run-2": {"scan_snapshot_id": None, "graph_snapshot_id": None},
    }
    store = _make_store(runs=runs, artifacts=artifacts)
    app.dependency_overrides[_store] = lambda: store

    tc = TestClient(app)
    resp = tc.get("/api/py/ops/sync/runs?limit=10", headers={"x-ops-secret": ""})
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["runs"]) == 2

    r1 = body["runs"][0]
    assert r1["id"] == "run-1"
    assert r1["has_scan_snapshot"] is True
    assert r1["has_graph_snapshot"] is True

    r2 = body["runs"][1]
    assert r2["id"] == "run-2"
    assert r2["has_scan_snapshot"] is False
    assert r2["has_graph_snapshot"] is False
    assert r2["status"] == "running"
    assert r2["trigger"] == "manual"
    app.dependency_overrides.clear()


def test_list_runs_limit_bound(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    runs = [{"id": f"run-{i}", "status": "success", "started_at": f"2026-06-{23-i:02d}T08:00:00Z"} for i in range(25)]
    store = _make_store(runs=runs)
    app.dependency_overrides[_store] = lambda: store

    tc = TestClient(app)
    resp = tc.get("/api/py/ops/sync/runs?limit=5", headers={"x-ops-secret": ""})
    assert resp.status_code == 200
    assert len(resp.json()["runs"]) == 5
    app.dependency_overrides.clear()


def test_list_runs_limit_too_high(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    store = _make_store(runs=[])
    app.dependency_overrides[_store] = lambda: store

    tc = TestClient(app)
    resp = tc.get("/api/py/ops/sync/runs?limit=200", headers={"x-ops-secret": ""})
    assert resp.status_code == 422
    app.dependency_overrides.clear()


# ---------------------------------------------------------------------------
# 鉴权测试
# ---------------------------------------------------------------------------


def test_trigger_secret_required(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "secret-123")
    monkeypatch.setenv("OPS_GITHUB_DISPATCH_TOKEN", "ghp_test")
    store = _make_store(runs=[])
    app.dependency_overrides[_store] = lambda: store
    monkeypatch.setattr(_sync_router_mod, "has_active_sync_workflow_run", lambda *, token: False)
    monkeypatch.setattr(_sync_router_mod, "dispatch_sync_workflow", lambda *, token: {"dispatched": True})

    tc = TestClient(app)
    # 无 header
    resp = tc.post("/api/py/ops/sync/trigger")
    assert resp.status_code == 401

    # 错误 header
    resp = tc.post("/api/py/ops/sync/trigger", headers={"x-ops-secret": "wrong"})
    assert resp.status_code == 403

    # 正确 header
    resp = tc.post("/api/py/ops/sync/trigger", headers={"x-ops-secret": "secret-123"})
    assert resp.status_code == 200
    app.dependency_overrides.clear()
