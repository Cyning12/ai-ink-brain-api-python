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


def test_chat_unauthorized(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.index as index

    importlib.reload(index)
    client = TestClient(index.app)
    res = client.post("/api/py/chat", json={"session_id": "s1", "messages": [{"role": "user", "content": "hi"}]})
    assert res.status_code == 401


def test_chat_missing_messages(monkeypatch: pytest.MonkeyPatch, _reload_index: Any) -> None:
    client = TestClient(_reload_index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}
    res = client.post("/api/py/chat", headers=headers, json={"session_id": "s1"})
    assert res.status_code == 400


def test_chat_missing_session_id(monkeypatch: pytest.MonkeyPatch, _reload_index: Any) -> None:
    client = TestClient(_reload_index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}
    res = client.post("/api/py/chat", headers=headers, json={"messages": [{"role": "user", "content": "hi"}]})
    assert res.status_code == 400


def test_chat_missing_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.index as index

    importlib.reload(index)
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}
    res = client.post(
        "/api/py/chat",
        headers=headers,
        json={"session_id": "s1", "messages": [{"role": "user", "content": "hi"}]},
    )
    assert res.status_code == 500


def test_chat_mock_streaming(monkeypatch: pytest.MonkeyPatch, _reload_index: Any) -> None:
    index = _reload_index
    client = TestClient(index.app)
    headers = {"Authorization": "Bearer secret-token-1234567890"}

    # Mock OpenAI streaming
    mock_chunk = MagicMock()
    mock_chunk.choices = [MagicMock()]
    mock_chunk.choices[0].delta = MagicMock()
    mock_chunk.choices[0].delta.content = "hello"

    mock_oai = MagicMock()
    mock_oai.chat.completions.create.return_value = iter([mock_chunk])
    mock_oai.embeddings.create.return_value = MagicMock(data=[MagicMock(embedding=[0.1] * 1024)])

    # Mock Supabase client
    mock_sb = MagicMock()
    mock_sb.rpc.return_value.execute.return_value = MagicMock(data=[])
    mock_sb.table.return_value.select.return_value.eq.return_value.limit.return_value.execute.return_value = MagicMock(
        data=[]
    )

    mock_sbm = MagicMock()
    mock_sbm.get_chat_history.return_value = []

    with (
        patch("api.routes.legacy_chat.OpenAI", return_value=mock_oai),
        patch("api.routes.legacy_chat.create_client", return_value=mock_sb),
        patch("api.routes.legacy_chat.SupabaseManager", return_value=mock_sbm),
        patch("api.routes.legacy_chat.ensure_embedding_alignment", return_value=MagicMock(ok=True)),
        patch("api.routes.legacy_chat.rewrite_query_with_history", return_value="rewritten hi"),
        patch("api.routes.legacy_chat.keyword_query_text_with_i18n_meta", return_value=("kw", {})),
        patch("api.routes.legacy_chat.fetch_keyword_hits", return_value=[]),
        patch("api.routes.legacy_chat.run_keyword_fallback", return_value=([], None)),
        patch("api.routes.legacy_chat.fuse_hits_rrf", return_value=[]),
    ):
        res = client.post(
            "/api/py/chat",
            headers=headers,
            json={"session_id": "s1", "messages": [{"role": "user", "content": "hi"}]},
        )
        assert res.status_code == 200
        assert res.headers.get("content-type", "").startswith("text/plain")
        body = b"".join(res.iter_bytes()).decode("utf-8")
        assert "hello" in body
