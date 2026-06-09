from __future__ import annotations

import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _reload_index(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.index as index

    importlib.reload(index)
    return index


def test_admin_sync_post_unauthorized(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.index as index

    importlib.reload(index)
    client = TestClient(index.app)
    res = client.post("/api/py/admin/sync")
    assert res.status_code == 401


def test_admin_sync_post_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _reload_index(monkeypatch)
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}

    import api.routes.admin_ingest as admin_ingest_mod

    importlib.reload(admin_ingest_mod)

    called: dict[str, Any] = {}

    def fake_create_sync_job():
        called["create"] = True
        return {"id": "job-abc-123"}

    def fake_get_job(jid: str):
        return {"id": jid, "status": "queued"}

    monkeypatch.setattr(admin_ingest_mod, "create_sync_job", fake_create_sync_job)
    monkeypatch.setattr(admin_ingest_mod, "get_job", fake_get_job)

    res = client.post("/api/py/admin/sync", headers=headers)
    assert res.status_code == 202
    data = res.json()
    assert data["ok"] is True
    assert data["statusUrl"] == "/api/py/admin/sync?jobId=job-abc-123"
    assert data["job"]["id"] == "job-abc-123"


def test_admin_sync_get_missing_job_id(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _reload_index(monkeypatch)
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}

    res = client.get("/api/py/admin/sync?jobId=", headers=headers)
    # FastAPI Query(...) with empty string still passes validation;
    # handler strips and checks empty -> 400
    assert res.status_code == 400


def test_admin_sync_get_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _reload_index(monkeypatch)
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}

    import api.routes.admin_ingest as admin_ingest_mod

    importlib.reload(admin_ingest_mod)

    monkeypatch.setattr(admin_ingest_mod, "get_job", lambda jid: None)

    res = client.get("/api/py/admin/sync?jobId=no-such-job", headers=headers)
    assert res.status_code == 404


def test_admin_sync_get_mock(monkeypatch: pytest.MonkeyPatch) -> None:
    index = _reload_index(monkeypatch)
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}

    import api.routes.admin_ingest as admin_ingest_mod

    importlib.reload(admin_ingest_mod)

    def fake_get_job(jid: str):
        return {"id": jid, "status": "succeeded"}

    monkeypatch.setattr(admin_ingest_mod, "get_job", fake_get_job)

    res = client.get("/api/py/admin/sync?jobId=job-xyz", headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["job"]["id"] == "job-xyz"
    assert data["job"]["status"] == "succeeded"
