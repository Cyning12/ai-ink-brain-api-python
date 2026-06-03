from __future__ import annotations

import importlib
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _reload_api_index(monkeypatch: pytest.MonkeyPatch, *, auth_override: bool = True) -> Any:
    monkeypatch.setenv("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    monkeypatch.setenv("TEXT2SQL_DATABASE_URL", "postgresql://u:p@localhost:5432/postgres")
    monkeypatch.setenv("INTENT_DDL_EVIDENCE_MIN_SCORE", "0.0")
    # 仓库 .env 可能默认开启 v2 agent；v1 测试必须显式关闭，避免分支被短路。
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    import api.intent_router as intent_router
    import api.unified_chat as unified_chat
    import api.index as index

    importlib.reload(intent_router)
    importlib.reload(unified_chat)
    importlib.reload(index)
    if auth_override:
        from tests._chatbi_auth_overrides import install_unified_chat_auth_override

        install_unified_chat_auth_override(index.app)
    else:
        from tests._chatbi_auth_overrides import clear_unified_chat_auth_override

        clear_unified_chat_auth_override(index.app)
    return index


def test_router_auto_to_no_data(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.intent_router as intent_router
    import api.unified_chat as unified_chat

    # ddl evidence: none
    def fake_store():  # noqa: ANN001
        class _S:
            def search(self, query: str, *, top_k: int = 3):  # noqa: ANN001
                return []

        return _S()

    monkeypatch.setattr(intent_router, "get_text2sql_store", fake_store)

    class _Rpc:
        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc()

    monkeypatch.setattr(intent_router, "supabase_client", lambda: _Sb())

    # no_data will call openai client: stub
    class _ChatMsg:
        def __init__(self, content: str):
            self.content = content

    class _Choice:
        def __init__(self, content: str):
            self.message = _ChatMsg(content)

    class _ChatResp:
        def __init__(self, content: str):
            self.choices = [_Choice(content)]

    class _DummyOAI:
        def __init__(self):
            self.chat = self
            self.completions = self

        def create(self, **kwargs: Any):  # noqa: ANN401
            return _ChatResp("ok")

    monkeypatch.setattr(unified_chat, "openai_siliconflow_client", lambda: _DummyOAI())

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "auto", "query": "帮我润色这段话"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "no_data"
    types = [e.get("type") for e in data["events"]]
    assert "router.decision" in types


def test_router_auto_to_rag(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.intent_router as intent_router
    import api.unified_chat as unified_chat

    def fake_store():  # noqa: ANN001
        class _S:
            def search(self, query: str, *, top_k: int = 3):  # noqa: ANN001
                return []

        return _S()

    monkeypatch.setattr(intent_router, "get_text2sql_store", fake_store)

    class _Rpc:
        def __init__(self, name: str):
            self.name = name

        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            r.data = [{"id": "1", "content": "Content: x", "metadata": {"relativePath": "a.md"}, "score": 0.1}] if self.name == "keyword_documents" else []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc(name)

    monkeypatch.setattr(intent_router, "supabase_client", lambda: _Sb())
    monkeypatch.setattr(unified_chat, "supabase_client", lambda: _Sb())

    # stub openai for rag
    class _EmbObj:
        def __init__(self, embedding: list[float]):
            self.embedding = embedding

    class _EmbResp:
        def __init__(self, embedding: list[float]):
            self.data = [_EmbObj(embedding)]

    class _ChatMsg:
        def __init__(self, content: str):
            self.content = content

    class _Choice:
        def __init__(self, content: str):
            self.message = _ChatMsg(content)

    class _ChatResp:
        def __init__(self, content: str):
            self.choices = [_Choice(content)]

    class _DummyOpenAI:
        def __init__(self):
            self.embeddings = self
            self.chat = self
            self.completions = self

        def create(self, **kwargs: Any):  # noqa: ANN401
            if "input" in kwargs and isinstance(kwargs["input"], list):
                return _EmbResp([0.0] * 8)
            return _ChatResp("rag answer")

    async def fake_rewrite(*, oai, query, history, chat_model):  # noqa: ANN001
        return "rewritten"

    monkeypatch.setattr(unified_chat, "openai_siliconflow_client", lambda: _DummyOpenAI())
    monkeypatch.setattr(unified_chat, "rewrite_query_with_history", fake_rewrite)

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "auto", "query": "Task 04 来源引用怎么做？"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "rag"
    types = [e.get("type") for e in data["events"]]
    assert "router.decision" in types
    assert "rag.sources" in types


def test_router_allows_safe_count_without_ddl(monkeypatch: pytest.MonkeyPatch):
    _reload_api_index(monkeypatch)
    import api.intent_router as intent_router

    # ddl evidence: none
    def fake_store():  # noqa: ANN001
        class _S:
            def search(self, query: str, *, top_k: int = 3):  # noqa: ANN001
                return []

        return _S()

    monkeypatch.setattr(intent_router, "get_text2sql_store", fake_store)

    # fts evidence: none
    class _Rpc:
        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc()

    monkeypatch.setattr(intent_router, "supabase_client", lambda: _Sb())

    d = intent_router.decide_intent(query="统计 heros 表里有多少条数据", prefer="auto")
    assert d.candidate_mode == "text2sql"
    assert d.final_mode == "text2sql"


def test_router_rag_signals_priority_over_sql_keywords(monkeypatch: pytest.MonkeyPatch):
    """日记 / 文档类表述优先 RAG 候选，避免「查询」单独把整句划进 text2sql。"""
    _reload_api_index(monkeypatch)
    import api.intent_router as intent_router

    def fake_store():  # noqa: ANN001
        class _S:
            def search(self, query: str, *, top_k: int = 3):  # noqa: ANN001
                return []

        return _S()

    monkeypatch.setattr(intent_router, "get_text2sql_store", fake_store)

    class _Rpc:
        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc()

    monkeypatch.setattr(intent_router, "supabase_client", lambda: _Sb())

    d = intent_router.decide_intent(query="查询下我的2026-04-28的日记", prefer="auto")
    assert d.candidate_mode == "rag"
    assert "rule:rag_keywords" in d.rule_hits
    assert d.final_mode == "rag"
    assert d.fallback == "rag_without_evidence_but_rag_signals"


def test_router_rag_keeps_when_ddl_positive_but_fts_empty(monkeypatch: pytest.MonkeyPatch):
    """FTS 无命中但 DDL 有证据且非 sql 升级：保持 RAG，不降为 no_data。"""
    _reload_api_index(monkeypatch)
    import api.intent_router as intent_router

    def fake_store():  # noqa: ANN001
        class _S:
            def search(self, query: str, *, top_k: int = 3):  # noqa: ANN001
                return [
                    {"doc_type": "ddl", "score": 0.2, "content": "create table t (id int);"},
                ]

        return _S()

    monkeypatch.setattr(intent_router, "get_text2sql_store", fake_store)

    class _Rpc:
        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc()

    monkeypatch.setattr(intent_router, "supabase_client", lambda: _Sb())

    d = intent_router.decide_intent(query="这个项目怎么部署？", prefer="auto")
    assert d.candidate_mode == "rag"
    assert d.final_mode == "rag"
    assert d.fallback == "rag_without_fts_keep_rag_ddl_evidence"

