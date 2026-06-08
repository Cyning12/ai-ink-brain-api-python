"""BE-1 隐藏测：评测机专用（解题 Agent 不应读取本文件）。"""

from __future__ import annotations

import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.text2sql_core import validate_sql_readonly


class TestValidateSqlReadonlyHidden:
    """validate_sql_readonly 边界：变体与 DDL。"""

    @pytest.mark.parametrize(
        "sql",
        [
            "select 1 ; select 2",
            "SELECT 1;\nSELECT 2",
            "SELECT 1;SELECT 2",
        ],
    )
    def test_hidden_multi_statement_variants(self, sql: str) -> None:
        with pytest.raises(ValueError, match="Multiple statements"):
            validate_sql_readonly(sql)

    def test_hidden_reject_drop_table(self) -> None:
        with pytest.raises(ValueError, match="(?i)select|forbidden"):
            validate_sql_readonly("DROP TABLE public.agent_info")

    def test_hidden_reject_select_then_delete(self) -> None:
        with pytest.raises(ValueError):
            validate_sql_readonly("SELECT 1; DELETE FROM public.agent_info")

    def test_hidden_reject_empty_sql(self) -> None:
        with pytest.raises(ValueError, match="Empty SQL"):
            validate_sql_readonly("   ")


def _reload_chain_index(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("TEXT2SQL_DATABASE_URL", "postgresql://u:p@localhost:5432/postgres")
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.chain_chat as chain_chat
    import api.index as index

    importlib.reload(chain_chat)
    importlib.reload(index)
    return index


class TestChainChatHiddenIntegration:
    """chain_chat 端到端：不 mock validate_sql_readonly。"""

    def test_hidden_chain_chat_rejects_multi_statement_sql(self, monkeypatch: pytest.MonkeyPatch) -> None:
        index = _reload_chain_index(monkeypatch)
        import api.chain_chat as chain_chat

        class _DummyOAI:
            pass

        monkeypatch.setattr(chain_chat, "OpenAI", lambda api_key, base_url: _DummyOAI())

        def fake_get_store():  # noqa: ANN001
            class _S:
                def search(self, query: str, *, top_k: int = 6):  # noqa: ANN001
                    return [{"doc_type": "ddl", "title": "DDL: agent_info", "content": "create table ...", "score": 1.0}]

            return _S()

        monkeypatch.setattr(chain_chat, "get_text2sql_store", fake_get_store)
        monkeypatch.setattr(
            chain_chat,
            "llm_generate_sql",
            lambda *, oai, model, prompt: "SELECT 1; SELECT 2",  # noqa: ARG005
        )
        # 故意不 mock validate_sql_readonly / execute_select_sql

        client = TestClient(index.app)
        res = client.post(
            "/api/py/chain/chat",
            headers={"Authorization": "Bearer api-key-123"},
            json={"session_id": "s-hidden", "query": "统计 agent_info 表里有多少条数据"},
        )
        assert res.status_code == 200
        data = res.json()
        assert data["ok"] is False
        events = data["events"]
        types = [e.get("type") for e in events]
        assert "error" in types
        gen_ends = [e for e in events if e.get("type") == "tool.call.end" and e.get("step_id") == "t_generate_sql"]
        assert gen_ends and gen_ends[0].get("payload", {}).get("error")
