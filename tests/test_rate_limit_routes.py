from __future__ import annotations

import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.chatbi_rate_limit import reset_rate_limit_state_for_tests


def _reload_index(monkeypatch: pytest.MonkeyPatch, *, auth_override: bool = True) -> Any:
    monkeypatch.setenv("NEXT_PUBLIC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")
    monkeypatch.setenv("CHATBI_RATE_LIMIT_ENABLED", "true")
    monkeypatch.setenv("CHATBI_RATE_LIMIT_MAX_REQUESTS", "2")
    monkeypatch.setenv("CHATBI_RATE_LIMIT_WINDOW_SEC", "60")

    import api.chatbi_rate_limit as rate_limit_mod
    import api.index as index

    importlib.reload(rate_limit_mod)
    importlib.reload(index)
    reset_rate_limit_state_for_tests()

    if auth_override:
        from tests._chatbi_auth_overrides import install_unified_chat_auth_override

        install_unified_chat_auth_override(index.app)
    else:
        from tests._chatbi_auth_overrides import clear_unified_chat_auth_override

        clear_unified_chat_auth_override(index.app)
    return index


def _assert_rate_limit_body(res) -> None:  # noqa: ANN001
    assert res.status_code == 429
    body = res.json()
    assert body.get("ok") is False
    assert body.get("error_code") == "RATE_LIMIT_EXCEEDED"
    assert isinstance(body.get("message"), str) and body["message"]
    assert isinstance(body.get("retry_after"), int) and body["retry_after"] >= 1


def test_chat_route_returns_429_after_threshold(monkeypatch: pytest.MonkeyPatch):
    index = _reload_index(monkeypatch, auth_override=False)
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}
    payload = {
        "session_id": "sess-rate-limit",
        "messages": [{"role": "user", "content": "hi"}],
    }

    for _ in range(2):
        res = client.post("/api/py/chat", headers=headers, json=payload)
        assert res.status_code != 429

    res3 = client.post("/api/py/chat", headers=headers, json=payload)
    _assert_rate_limit_body(res3)


def test_unified_stream_returns_429_after_threshold(monkeypatch: pytest.MonkeyPatch):
    index = _reload_index(monkeypatch, auth_override=True)
    client = TestClient(index.app)
    payload = {"session_id": "sess-unified-rl", "query": "hi"}

    for _ in range(2):
        res = client.post("/api/py/unified/chat/stream", json=payload)
        assert res.status_code != 429

    res3 = client.post("/api/py/unified/chat/stream", json=payload)
    _assert_rate_limit_body(res3)


def test_live_probe_not_rate_limited(monkeypatch: pytest.MonkeyPatch):
    index = _reload_index(monkeypatch, auth_override=False)
    client = TestClient(index.app)

    for _ in range(5):
        res = client.get("/api/py/live")
        assert res.status_code == 200
        assert res.json().get("ok") is True


def test_rate_limit_disabled_when_max_requests_zero(monkeypatch: pytest.MonkeyPatch):
    index = _reload_index(monkeypatch, auth_override=False)
    monkeypatch.setenv("CHATBI_RATE_LIMIT_MAX_REQUESTS", "0")
    reset_rate_limit_state_for_tests()
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}
    payload = {
        "session_id": "sess-no-limit",
        "messages": [{"role": "user", "content": "hi"}],
    }

    for _ in range(4):
        res = client.post("/api/py/chat", headers=headers, json=payload)
        assert res.status_code != 429
