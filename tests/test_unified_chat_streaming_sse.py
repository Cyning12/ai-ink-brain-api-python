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


def test_unified_stream_unauthorized(monkeypatch: pytest.MonkeyPatch):
    index = _reload_api_index(monkeypatch)
    client = TestClient(index.app)
    res = client.post("/api/py/unified/chat/stream", json={"session_id": "s", "query": "hi"})
    assert res.status_code == 401
    assert res.json() == {"detail": "Unauthorized"}


def test_unified_stream_emits_sse(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DEBUG_ROUTER_EVIDENCE", "1")
    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat

    # stub RAG branch dependencies to avoid external calls
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
            r.data = []
            return r

    class _Sb:
        def rpc(self, name: str, params: dict[str, Any]):  # noqa: ANN001
            return _Rpc(name)

        def table(self, _name: str):  # noqa: ANN001
            return _TableQuery()

    monkeypatch.setattr(unified_chat, "supabase_client", lambda: _Sb())

    client = TestClient(index.app)
    with client.stream(
        "POST",
        "/api/py/unified/chat/stream",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s", "prefer": "rag", "query": "hello"},
    ) as res:
        assert res.status_code == 200
        ct = res.headers.get("content-type") or ""
        assert "text/event-stream" in ct
        text = ""
        for chunk in res.iter_text():
            text += chunk
            if "event: done" in text:
                break
        assert "event: chain" in text
        assert "event: done" in text
        assert '"type":"router.evidence"' in text
        assert '"type":"router.evidence.details"' in text

