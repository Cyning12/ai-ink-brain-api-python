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
    assert "sql.result" in types
    assert "assistant.message" in types


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

