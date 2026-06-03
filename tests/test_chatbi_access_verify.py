from __future__ import annotations

import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _reload_index(monkeypatch: pytest.MonkeyPatch, *, auth_override: bool) -> Any:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("TEXT2SQL_DATABASE_URL", "postgresql://u:p@localhost:5432/postgres")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.index as index

    importlib.reload(index)
    if auth_override:
        from tests._chatbi_auth_overrides import install_unified_chat_auth_override

        install_unified_chat_auth_override(index.app)
    else:
        from tests._chatbi_auth_overrides import clear_unified_chat_auth_override

        clear_unified_chat_auth_override(index.app)
    return index


def test_chatbi_access_verify_ok(monkeypatch: pytest.MonkeyPatch):
    index = _reload_index(monkeypatch, auth_override=True)
    client = TestClient(index.app)
    res = client.get("/api/py/chatbi/access/verify", headers={"Authorization": "Bearer dummy-plain"})
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["principal_kind"] == "super"
    assert data["access_level"] == 0
    assert data["token_id"] == "00000000-0000-0000-0000-000000000001"


def test_chatbi_access_verify_unauthorized(monkeypatch: pytest.MonkeyPatch):
    index = _reload_index(monkeypatch, auth_override=False)
    client = TestClient(index.app)
    res = client.get("/api/py/chatbi/access/verify")
    assert res.status_code == 401
    assert res.json()["detail"]["code"] == "CHATBI_UNAUTHORIZED"
