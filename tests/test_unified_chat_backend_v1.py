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
    monkeypatch.setenv("TEXT2SQL_DATABASE_URL", "postgresql://u:p@localhost:5432/postgres")

    import api.unified_chat as unified_chat
    import api.index as index

    importlib.reload(unified_chat)
    importlib.reload(index)
    return index


def test_unified_unauthorized(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    client = TestClient(index.app)
    res = client.post("/api/py/unified/chat", json={"session_id": "s", "query": "hi"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Unauthorized"}


def test_unified_prefer_text2sql(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DEBUG_ROUTER_EVIDENCE", "1")
    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat

    class _DummyOAI:
        pass

    monkeypatch.setattr(unified_chat, "OpenAI", lambda api_key, base_url: _DummyOAI())

    def fake_get_store():  # noqa: ANN001
        class _S:
            def search(self, query: str, *, top_k: int = 6):  # noqa: ANN001
                return [{"doc_type": "ddl", "title": "DDL: agent_info", "content": "create table ...", "score": 1.0}]

        return _S()

    monkeypatch.setattr(unified_chat, "get_text2sql_store", fake_get_store)
    monkeypatch.setattr(unified_chat, "llm_generate_sql", lambda *, oai, model, prompt: "select 1 as count")  # noqa: ARG005
    monkeypatch.setattr(unified_chat, "validate_sql_readonly", lambda s: s)
    monkeypatch.setattr(unified_chat, "execute_select_sql", lambda sql, limit_rows=200: (["count"], [{"count": 0}]))  # noqa: ARG005
    monkeypatch.setattr(unified_chat, "llm_summarize", lambda *, oai, model, prompt: "共有 0 条。")  # noqa: ARG005

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "text2sql", "query": "随便问"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "text2sql"
    types = [e.get("type") for e in data["events"]]
    assert "router.evidence" in types
    assert "router.evidence.details" in types
    assert "sql.result" in types
    assert "assistant.message" in types


def test_unified_router_trace_db_toggle(monkeypatch: pytest.MonkeyPatch):
    # 覆盖 3 个关键行为：
    # 1) DEBUG_ROUTER_TRACE_DB=1 默认写入 router_trace_v1
    # 2) DEBUG_ROUTER_TRACE_DB=0 且 debug_router=false 不写入 router_trace_v1
    # 3) DEBUG_ROUTER_TRACE_DB=0 但 debug_router=true 强制写入 router_trace_v1
    import api.unified_chat as unified_chat

    class _DummyChatMsg:
        def __init__(self, content: str):
            self.content = content

    class _DummyChoice:
        def __init__(self, content: str):
            self.message = _DummyChatMsg(content)

    class _DummyChatResp:
        def __init__(self, content: str):
            self.choices = [_DummyChoice(content)]

    class _DummyOpenAI:
        def __init__(self):
            self.chat = self
            self.completions = self

        def create(self, **_kwargs: Any):  # noqa: ANN401
            return _DummyChatResp("ok")

    def _install_common_mocks() -> list[dict[str, Any]]:
        saved: list[dict[str, Any]] = []

        monkeypatch.setattr(unified_chat, "openai_siliconflow_client", lambda: _DummyOpenAI())

        def fake_get_store():  # noqa: ANN001
            class _S:
                def search(self, query: str, *, top_k: int = 6):  # noqa: ANN001
                    return [{"doc_type": "ddl", "title": "DDL: customer_info", "content": "create table ...", "score": 0.9}][:top_k]

            return _S()

        class _Rpc:
            def execute(self):
                class _R:
                    data: list[dict[str, Any]]

                r = _R()
                r.data = [{"id": "d1", "score": 0.12, "metadata": {"relativePath": "docs/a.md"}}]
                return r

        class _Sb:
            def rpc(self, _name: str, _params: dict[str, Any]):  # noqa: ANN001
                return _Rpc()

        monkeypatch.setattr(unified_chat, "get_text2sql_store", fake_get_store)
        monkeypatch.setattr(unified_chat, "supabase_client", lambda: _Sb())

        def fake_async_save(payload: dict[str, Any]) -> None:
            saved.append(payload)

        monkeypatch.setattr(unified_chat, "_async_save_rag_log", fake_async_save)
        return saved

    # case 1: env=1 -> 写入
    monkeypatch.setenv("DEBUG_ROUTER_TRACE_DB", "1")
    monkeypatch.setenv("DEBUG_ROUTER_EVIDENCE_DB", "0")
    index = _reload_api_index(monkeypatch)
    importlib.reload(unified_chat)
    saved = _install_common_mocks()
    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "no_data", "query": "hi"},
    )
    assert res.status_code == 200
    assert saved, "expected best-effort DB log payload"
    meta = (saved[-1].get("metadata") or {}).get("router_debug") or {}
    trace = meta.get("router_trace_v1") if isinstance(meta, dict) else None
    assert isinstance(trace, dict)
    assert trace.get("v") == "router_trace_v1"
    assert isinstance(trace.get("decision"), dict)
    assert isinstance((trace.get("timing_ms") or {}), dict)

    # case 2: env=0 + debug_router=false -> 不写入
    monkeypatch.setenv("DEBUG_ROUTER_TRACE_DB", "0")
    monkeypatch.setenv("DEBUG_ROUTER_EVIDENCE_DB", "0")
    index2 = _reload_api_index(monkeypatch)
    importlib.reload(unified_chat)
    saved2 = _install_common_mocks()
    client2 = TestClient(index2.app)
    res2 = client2.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "no_data", "query": "hi"},
    )
    assert res2.status_code == 200
    assert not saved2, "expected no DB log when both DEBUG_ROUTER_TRACE_DB and DEBUG_ROUTER_EVIDENCE_DB are disabled"

    # case 3: env=0 + debug_router=true -> 强制写入
    monkeypatch.setenv("DEBUG_ROUTER_TRACE_DB", "0")
    monkeypatch.setenv("DEBUG_ROUTER_EVIDENCE_DB", "0")
    index3 = _reload_api_index(monkeypatch)
    importlib.reload(unified_chat)
    saved3 = _install_common_mocks()
    client3 = TestClient(index3.app)
    res3 = client3.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "no_data", "query": "hi", "debug_router": True},
    )
    assert res3.status_code == 200
    meta3 = (saved3[-1].get("metadata") or {}).get("router_debug") or {}
    trace3 = meta3.get("router_trace_v1") if isinstance(meta3, dict) else None
    assert isinstance(trace3, dict)
    assert trace3.get("v") == "router_trace_v1"


def test_unified_prefer_rag(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat

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
            # embeddings.create
            if "input" in kwargs and "model" in kwargs and isinstance(kwargs["input"], list):
                return _EmbResp([0.0] * 8)
            # chat.completions.create
            return _ChatResp("rag answer")

    monkeypatch.setattr(unified_chat, "openai_siliconflow_client", lambda: _DummyOpenAI())

    async def fake_rewrite(*, oai, query, history, chat_model):  # noqa: ANN001
        return "rewritten"

    monkeypatch.setattr(unified_chat, "rewrite_query_with_history", fake_rewrite)

    class _Rpc:
        def __init__(self, name: str):
            self.name = name

        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            if self.name == "keyword_documents":
                r.data = [{"id": "1", "content": "Content: hello", "metadata": {"relativePath": "a.md"}}]
            else:
                r.data = []
            return r

    class _TableQuery:
        def __init__(self):
            self._k = ""
            self._v = ""

        def select(self, *_args: Any, **_kwargs: Any):  # noqa: ANN401
            return self

        def eq(self, k: str, v: str):  # noqa: ANN001
            self._k = k
            self._v = v
            return self

        def limit(self, _n: int):  # noqa: ANN001
            return self

        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            # 结构化召回：当命中 diary/2026-4-14.md 时返回一条
            if self._k == "metadata->>relativePath" and self._v == "diary/2026-4-14.md":
                r.data = [{"id": 4414, "content": "Content: diary", "metadata": {"relativePath": "diary/2026-4-14.md"}}]
            else:
                r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc(name)

        def table(self, _name: str):  # noqa: ANN001
            return _TableQuery()

    monkeypatch.setattr(unified_chat, "supabase_client", lambda: _Sb())

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "rag", "query": "hello"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "rag"
    types = [e.get("type") for e in data["events"]]
    assert "rag.sources" in types
    assert "assistant.message" in types


def test_unified_rag_structured_recall_cn_date(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat

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

    monkeypatch.setattr(unified_chat, "openai_siliconflow_client", lambda: _DummyOpenAI())

    async def fake_rewrite(*, oai, query, history, chat_model):  # noqa: ANN001
        return query

    monkeypatch.setattr(unified_chat, "rewrite_query_with_history", fake_rewrite)

    class _Rpc:
        def __init__(self, name: str):
            self.name = name

        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            r.data = []
            return r

    class _TableQuery:
        def __init__(self):
            self._k = ""
            self._v = ""

        def select(self, *_args: Any, **_kwargs: Any):  # noqa: ANN401
            return self

        def eq(self, k: str, v: str):  # noqa: ANN001
            self._k = k
            self._v = v
            return self

        def limit(self, _n: int):  # noqa: ANN001
            return self

        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            if self._k == "metadata->>date_norm" and self._v == "2026-04-14":
                r.data = [{"id": 4414, "content": "Content: diary", "metadata": {"date_norm": "2026-04-14", "relativePath": "diary/2026-4-14.md"}}]
            elif self._k == "metadata->>relativePath" and self._v in ("diary/2026-4-14.md", "diary/2026-04-14.md"):
                r.data = [{"id": 4414, "content": "Content: diary", "metadata": {"relativePath": self._v}}]
            else:
                r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc(name)

        def table(self, _name: str):  # noqa: ANN001
            return _TableQuery()

    monkeypatch.setattr(unified_chat, "supabase_client", lambda: _Sb())

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "rag", "query": "二零二六年四月十四号那天写了什么"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] == "rag"
    # 找到 rag.retrieve end 事件，确保 structured_hits 计数生效
    retrieve_end = [e for e in data["events"] if e.get("type") == "tool.call.end" and e.get("step_id") == "t_retrieve"]
    assert retrieve_end
    out = retrieve_end[-1]["payload"]["output"]
    assert out.get("structured_hits", 0) >= 1


def test_date_norm_candidates_cn_numerals():
    from api.rag_recall_tools import date_norm_candidates_for_structured

    cands = date_norm_candidates_for_structured("二零二六年四月十四号那天写了什么")
    assert "2026-04-14" in cands


def test_date_norm_candidates_cn_uppercase_numerals():
    from api.rag_recall_tools import date_norm_candidates_for_structured

    cands = date_norm_candidates_for_structured("贰零贰陆年肆月拾肆号那天写了什么")
    assert "2026-04-14" in cands


def test_keyword_query_text_expands_version_hyphen():
    from api.rag_recall_tools import keyword_query_text

    qt = keyword_query_text("langchain 0-1-0 正式版什么时候发布")
    # 保留原 query + 版本候选 OR 扩展
    assert "\"langchain 0-1-0 正式版什么时候发布\"" in qt
    assert "\"0-1-0\"" in qt
    assert "\"0_1_0\"" in qt
    assert "\"0.1.0\"" in qt
    assert "\"v0.1.0\"" in qt


def test_i18n_expand_glossary_or_compose():
    from api.rag_recall_tools import keyword_query_text_with_i18n_meta

    qt, meta = keyword_query_text_with_i18n_meta("如何实现消息历史的可运行链？")
    assert "\"如何实现消息历史的可运行链？\"" in qt
    # glossary 命中：消息历史 -> message history
    assert "\"message history\"" in qt
    assert isinstance(meta, dict)
    assert meta.get("source") in ("glossary", "none")


def test_i18n_expand_limits_and_truncation(monkeypatch: pytest.MonkeyPatch):
    from api.rag_recall_tools import keyword_query_text_with_i18n_meta

    monkeypatch.setenv("I18N_EXPAND_ENABLED", "1")
    monkeypatch.setenv("I18N_EXPAND_MODE", "glossary")
    monkeypatch.setenv("I18N_EXPAND_MAX_CANDIDATES", "1")
    monkeypatch.setenv("I18N_EXPAND_MAX_CANDIDATE_CHARS", "8")
    monkeypatch.setenv("I18N_EXPAND_MAX_QUERY_TEXT_CHARS", "64")

    qt, meta = keyword_query_text_with_i18n_meta("对话历史和向量数据库怎么选？")
    assert isinstance(meta, dict)
    cands = meta.get("candidates")
    assert isinstance(cands, list)
    assert len(cands) <= 1
    assert len(qt) <= 64
    assert meta.get("truncated") in (True, False)


def test_i18n_expand_graceful_fallback_on_error(monkeypatch: pytest.MonkeyPatch):
    import api.rag_recall_tools as tools

    monkeypatch.setenv("I18N_EXPAND_ENABLED", "1")
    monkeypatch.setenv("I18N_EXPAND_MODE", "glossary")

    def _boom():  # noqa: ANN001
        raise RuntimeError("boom")

    monkeypatch.setattr(tools, "_load_i18n_glossary", _boom)
    qt, meta = tools.keyword_query_text_with_i18n_meta("向量库怎么做")
    # 任何异常必须优雅降级：至少保留原 query（不抛错）
    assert "\"向量库怎么做\"" in qt
    assert isinstance(meta, dict)

