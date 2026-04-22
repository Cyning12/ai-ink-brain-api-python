from __future__ import annotations

import importlib
import uuid
from typing import Any

import pytest
from fastapi.testclient import TestClient


def _reload_api_index(monkeypatch: pytest.MonkeyPatch) -> Any:
    monkeypatch.setenv("NEXT_PUBLIC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.setenv("API_KEY", "api-key-123")
    monkeypatch.setenv("SILICONFLOW_API_KEY", "sf-dummy-key")
    monkeypatch.setenv("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    monkeypatch.setenv("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")

    import api.code_retrieval as code_retrieval
    import api.index as index

    importlib.reload(code_retrieval)
    importlib.reload(index)
    return index


class _EmbObj:
    def __init__(self, embedding: list[float]):
        self.embedding = embedding


class _EmbResp:
    def __init__(self, embedding: list[float]):
        self.data = [_EmbObj(embedding)]


class _DummyOpenAI:
    def __init__(self, *, embedding: list[float] | None, fail_embed: bool = False):
        self.embeddings = self
        self._embedding = embedding
        self._fail_embed = fail_embed

    def create(self, **kwargs: Any) -> _EmbResp:  # noqa: ANN401
        if self._fail_embed:
            raise RuntimeError("embed failed")
        assert self._embedding is not None
        return _EmbResp(self._embedding)


def test_code_query_unauthorized(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    client = TestClient(index.app)
    res = client.post("/api/py/code/query", json={"query": "x"})
    assert res.status_code == 401
    assert res.json() == {"ok": False, "error": "Unauthorized"}


def test_code_query_hybrid_ok(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.code_retrieval as code_retrieval

    async def fake_rewrite(*, oai, query, history, chat_model):  # noqa: ANN001
        assert query == "hello"
        return "rewritten"

    monkeypatch.setattr(code_retrieval, "rewrite_query_with_history", fake_rewrite)

    vec = [0.0] * 1024
    shared_id = "00000000-0000-0000-0000-0000000000aa"

    class _Rpc:
        def __init__(self, name: str, params: dict[str, Any]):
            self.name = name
            self.params = params

        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            if self.name == "match_code_chunks":
                r.data = [
                    {
                        "id": shared_id,
                        "content": "[Code Context]\n---\nContent:\nasync def chat():\n    pass\n",
                        "metadata": {
                            "relativePath": "api/index.py",
                            "file_path": "/abs/api/index.py",
                            "filename": "index.py",
                            "slug": "api.index.chat",
                            "chunk_index": 1,
                            "start_line": 10,
                            "end_line": 12,
                            "chunk_type": "function",
                            "name": "chat",
                            "signature": "async def chat() -> None",
                            "module": "api.index",
                        },
                        "similarity": 0.9,
                    }
                ]
            elif self.name == "keyword_code_chunks":
                r.data = [
                    {
                        "id": shared_id,
                        "content": "kw hit",
                        "metadata": {
                            "relativePath": "api/index.py",
                            "file_path": "/abs/api/index.py",
                            "filename": "index.py",
                            "slug": "api.index.chat",
                            "chunk_index": 1,
                            "start_line": 10,
                            "end_line": 12,
                            "chunk_type": "function",
                            "name": "chat",
                            "signature": "async def chat() -> None",
                            "module": "api.index",
                        },
                        "score": 0.2,
                    }
                ]
            else:
                r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):
            return _Rpc(name, params)

    monkeypatch.setattr(code_retrieval, "create_client", lambda url, key: _Sb())
    monkeypatch.setattr(code_retrieval, "OpenAI", lambda **kwargs: _DummyOpenAI(embedding=vec))

    client = TestClient(index.app)
    res = client.post(
        "/api/py/code/query",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "hello", "top_k": 2},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["query"] == "hello"
    assert data["rewritten_query"] == "rewritten"
    assert len(data["chunks"]) >= 1
    assert data["chunks"][0]["name"] == "chat"
    assert data["retrieval_meta"]["vector_hits"] == 1
    assert data["retrieval_meta"]["keyword_hits"] == 1


def test_code_query_filters_file_path(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.code_retrieval as code_retrieval

    async def fake_rewrite(*, oai, query, history, chat_model):  # noqa: ANN001
        return query

    monkeypatch.setattr(code_retrieval, "rewrite_query_with_history", fake_rewrite)

    vec = [0.0] * 1024
    uid = str(uuid.uuid4())

    class _Rpc:
        def __init__(self, name: str, params: dict[str, Any]):
            self.name = name

        def execute(self):
            class _R:
                data = [
                    {
                        "id": uid,
                        "content": "c1",
                        "metadata": {
                            "relativePath": "api/index.py",
                            "file_path": "/Users/x/api/index.py",
                            "filename": "index.py",
                            "slug": "api.index.chat",
                            "chunk_index": 1,
                            "start_line": 1,
                            "end_line": 2,
                            "chunk_type": "function",
                            "name": "chat",
                            "signature": "async def chat()",
                            "module": "api.index",
                        },
                        "similarity": 0.99,
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "content": "c2",
                        "metadata": {
                            "relativePath": "api/other.py",
                            "file_path": "/Users/x/api/other.py",
                            "filename": "other.py",
                            "slug": "api.other.x",
                            "chunk_index": 0,
                            "start_line": 1,
                            "end_line": 2,
                            "chunk_type": "function",
                            "name": "x",
                            "signature": "def x()",
                            "module": "api.other",
                        },
                        "similarity": 0.98,
                    },
                ]

            r = _R()
            if self.name == "keyword_code_chunks":
                # 让 keyword 路也命中 other.py，验证 post-filter 生效
                return r
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):
            return _Rpc(name, params)

    monkeypatch.setattr(code_retrieval, "create_client", lambda url, key: _Sb())
    monkeypatch.setattr(code_retrieval, "OpenAI", lambda **kwargs: _DummyOpenAI(embedding=vec))

    client = TestClient(index.app)
    res = client.post(
        "/api/py/code/query",
        headers={"Authorization": "Bearer api-key-123"},
        json={
            "query": "chat",
            "top_k": 10,
            "filters": {"file_path": "api/index.py"},
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert all(c["file_path"] == "api/index.py" or c["relative_path"] == "api/index.py" for c in data["chunks"])


def test_code_query_embedding_fallback_keyword_only(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.code_retrieval as code_retrieval

    async def fake_rewrite(*, oai, query, history, chat_model):  # noqa: ANN001
        return query

    monkeypatch.setattr(code_retrieval, "rewrite_query_with_history", fake_rewrite)

    class _Rpc:
        def __init__(self, name: str, params: dict[str, Any]):
            self.name = name

        def execute(self):
            class _R:
                data: list[dict[str, Any]]

            r = _R()
            if self.name == "keyword_code_chunks":
                r.data = [
                    {
                        "id": str(uuid.uuid4()),
                        "content": "kw",
                        "metadata": {
                            "relativePath": "api/index.py",
                            "file_path": "/abs/api/index.py",
                            "filename": "index.py",
                            "slug": "api.index.chat",
                            "chunk_index": 0,
                            "start_line": 1,
                            "end_line": 1,
                            "chunk_type": "function",
                            "name": "chat",
                            "signature": "def chat(): ...",
                            "module": "api.index",
                        },
                        "score": 0.5,
                    }
                ]
            else:
                r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):
            return _Rpc(name, params)

    monkeypatch.setattr(code_retrieval, "create_client", lambda url, key: _Sb())
    monkeypatch.setattr(code_retrieval, "OpenAI", lambda **kwargs: _DummyOpenAI(embedding=None, fail_embed=True))

    client = TestClient(index.app)
    res = client.post(
        "/api/py/code/query",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "chat"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["retrieval_meta"]["mode"] == "keyword_only"
    assert "embedding_error" in data["retrieval_meta"]
    assert len(data["chunks"]) >= 1


def test_code_search_empty_without_filters(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    client = TestClient(index.app)
    res = client.post(
        "/api/py/code/search",
        headers={"Authorization": "Bearer api-key-123"},
        json={},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["chunks"] == []


def test_code_search_by_name(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    import api.code_retrieval as code_retrieval

    class _Query:
        def __init__(self):
            self._filters: list[tuple[str, str, str]] = []

        def select(self, *_args: Any, **_kwargs: Any):
            return self

        def eq(self, col: str, val: str):
            self._filters.append(("eq", col, val))
            return self

        def ilike(self, col: str, val: str):
            self._filters.append(("ilike", col, val))
            return self

        def limit(self, n: int):
            self._n = n
            return self

        def execute(self):
            class _R:
                data = [
                    {
                        "id": str(uuid.uuid4()),
                        "content": "c",
                        "metadata": {
                            "relativePath": "api/index.py",
                            "file_path": "/abs/api/index.py",
                            "filename": "index.py",
                            "slug": "api.index.chat",
                            "chunk_index": 0,
                            "start_line": 1,
                            "end_line": 2,
                            "chunk_type": "function",
                            "name": "chat",
                            "signature": "async def chat()",
                            "module": "api.index",
                        },
                    }
                ]

            return _R()

    class _Table:
        def __init__(self, name: str):
            self.name = name

        def select(self, *args: Any, **kwargs: Any):
            assert self.name == "code_chunks"
            return _Query()

    class _Sb:
        def table(self, name: str):
            return _Table(name)

    monkeypatch.setattr(code_retrieval, "create_client", lambda url, key: _Sb())

    client = TestClient(index.app)
    res = client.post(
        "/api/py/code/search",
        headers={"Authorization": "Bearer api-key-123"},
        json={"name": "chat", "top_k": 5},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["ok"] is True
    assert data["retrieval_meta"]["mode"] == "metadata"
    assert any(c["name"] == "chat" for c in data["chunks"])
