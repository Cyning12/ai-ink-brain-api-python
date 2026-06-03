from __future__ import annotations

import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _reload_api_index(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("TEXT2SQL_DATABASE_URL", "postgresql://u:p@localhost:5432/postgres")
    # 避免仓库 .env 默认开启 agent 影响其他路由初始化副作用。
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.chain_chat as chain_chat
    import api.index as index

    importlib.reload(chain_chat)
    importlib.reload(index)
    return index


def test_chain_chat_unauthorized(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    client = TestClient(index.app)
    res = client.post("/api/py/chain/chat", json={"session_id": "s", "query": "hi"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Unauthorized"}


def test_chain_chat_events_ok(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.chain_chat as chain_chat

    class _DummyOAI:
        pass

    monkeypatch.setattr(chain_chat, "OpenAI", lambda api_key, base_url: _DummyOAI())

    def fake_get_store():  # noqa: ANN001
        class _S:
            def search(self, query: str, *, top_k: int = 6):  # noqa: ANN001
                assert top_k == 6
                return [{"doc_type": "ddl", "title": "DDL: agent_info", "content": "create table ...", "score": 1.0}]

        return _S()

    monkeypatch.setattr(chain_chat, "get_text2sql_store", fake_get_store)

    monkeypatch.setattr(chain_chat, "llm_generate_sql", lambda *, oai, model, prompt: "select 1 as count")  # noqa: ARG005
    monkeypatch.setattr(chain_chat, "validate_sql_readonly", lambda s: s)
    monkeypatch.setattr(chain_chat, "execute_select_sql", lambda sql, limit_rows=200: (["count"], [{"count": 0}]))  # noqa: ARG005
    monkeypatch.setattr(chain_chat, "llm_summarize", lambda *, oai, model, prompt: "共有 0 条。")  # noqa: ARG005

    client = TestClient(index.app)
    res = client.post(
        "/api/py/chain/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "query": "统计 agent_info 表里有多少条数据"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert isinstance(data["run_id"], str) and data["run_id"]
    assert data["session_id"] == "s"
    events = data["events"]
    assert isinstance(events, list) and len(events) >= 6
    # must include sql.result and assistant.message
    types = [e.get("type") for e in events]
    assert "sql.result" in types
    assert "assistant.message" in types

