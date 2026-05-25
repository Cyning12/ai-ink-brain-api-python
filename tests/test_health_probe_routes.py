from __future__ import annotations

import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _reload_api_index(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setenv("NEXT_PUBLIC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    index = importlib.import_module("api.index")
    importlib.reload(index)
    return index


def test_live_returns_200_and_ok_true(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    client = TestClient(index.app)

    res = client.get("/api/py/live")

    assert res.status_code == 200
    body = res.json()
    assert body["ok"] is True


def test_ready_returns_503_with_components_when_supabase_missing(
    monkeypatch: pytest.MonkeyPatch,
):
    index = _reload_api_index(monkeypatch)
    monkeypatch.delenv("NEXT_PUBLIC_SUPABASE_URL", raising=False)
    monkeypatch.delenv("SUPABASE_URL", raising=False)

    client = TestClient(index.app)
    res = client.get("/api/py/ready")

    assert res.status_code == 503
    body = res.json()
    assert body["ok"] is False
    assert isinstance(body.get("components"), list)
    assert any(c.get("name") == "supabase" and c.get("status") == "failed" for c in body["components"])
