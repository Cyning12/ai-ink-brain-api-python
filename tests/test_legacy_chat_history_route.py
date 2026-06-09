from __future__ import annotations

import importlib
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
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


def test_history_unauthorized(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.index as index

    importlib.reload(index)
    client = TestClient(index.app)
    res = client.get("/api/py/chat/history?session_id=s1")
    assert res.status_code == 401


def test_history_missing_session_id(monkeypatch: pytest.MonkeyPatch, _reload_index: Any) -> None:
    client = TestClient(_reload_index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}
    res = client.get("/api/py/chat/history", headers=headers)
    # FastAPI Query(...) without value produces 422 (validation error), not 400
    assert res.status_code == 422


def test_history_mock(monkeypatch: pytest.MonkeyPatch, _reload_index: Any) -> None:
    client = TestClient(_reload_index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}

    async def _mock_list_turns(sid: str, *, limit: int = 100) -> list[dict[str, Any]]:
        return [
            {"query": "q1", "response": "a1", "created_at": "2026-01-01T00:00:00Z"},
            {"query": "q2", "response": "a2", "created_at": "2026-01-01T00:01:00Z"},
        ]

    mock_sbm = MagicMock()
    mock_sbm.list_session_turns = _mock_list_turns

    async def _mock_auth(**kw: Any) -> None:
        pass

    with (
        patch("api.routes.legacy_chat.SupabaseManager", return_value=mock_sbm),
        patch("api.routes.legacy_chat._require_rag_history_auth", _mock_auth),
    ):
        res = client.get("/api/py/chat/history?session_id=s1", headers=headers)
        assert res.status_code == 200
        data = res.json()
        assert data["ok"] is True
        assert data["session_id"] == "s1"
        msgs = data["messages"]
        assert isinstance(msgs, list)
        assert len(msgs) == 4  # q1, a1, q2, a2
        assert msgs[0]["role"] == "user"
        assert msgs[0]["content"] == "q1"
        assert msgs[1]["role"] == "assistant"
        assert msgs[1]["content"] == "a1"
