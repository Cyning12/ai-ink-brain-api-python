from __future__ import annotations

import importlib
import asyncio
from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient

from api.intent_agent import IntentDecision, StructuredSignals
from api.tools import Tool, ToolResult, ToolName


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


def _make_tool(name: ToolName, execute: Callable[..., Any]) -> Tool:
    async def _exec(query: str, *, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        return await execute(query=query, history=history)

    return Tool(name=name, description=f"dummy-{name}", parameters={}, execute=_exec)


def test_v2_json_single_tool_fallback_used_true(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _direct_answer_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={"answer": "direct ok"},
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=2,
        )

    async def _rag_search_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={"answer": "rag ok", "hits": []},
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=3,
        )

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("direct_answer", _direct_answer_exec),
        _make_tool("rag_search", _rag_search_exec),
        _make_tool("text2sql_query", _rag_search_exec),  # 不会走到
    ]

    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout)
        return IntentDecision(
            tool="rag_search",
            mode="rag",
            reasoning="置信度过低，使用 fallback。",
            reasoning_full="置信度过低，使用 fallback。",
            confidence=0.2,
            fallback="direct_answer",
            structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=False),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "hi"},
    )
    assert res.status_code == 200
    data = res.json()
    assert data["mode"] in ("no_data", "rag", "text2sql")

    types = [e.get("type") for e in data["events"]]
    assert "agent.final" in types

    final_evt = next(e for e in data["events"] if e.get("type") == "agent.final")
    assert final_evt["payload"]["fallback_used"] is True


def test_v2_json_multi_tool_sql_fail_then_rag(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _text2sql_fail_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=False,
            data=None,
            error="sql exec failed",
            error_code="SQL_EXEC_TABLE_NOT_FOUND",
            error_stage="sql.execute",
            latency_ms=7,
        )

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={
                "answer": "rag ok",
                "hits": [
                    {
                        "id": "1",
                        "content": "Content: hello",
                        "metadata": {
                            "filename": "a.md",
                            "relativePath": "diary/a.md",
                            "original_link": "http://example",
                            "slug": "slug-a",
                            "category": "diary",
                            "chunk_index": 0,
                        },
                        "fused_score": 1.0,
                    }
                ],
            },
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=4,
        )

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("text2sql_query", _text2sql_fail_exec),
        _make_tool("rag_search", _rag_ok_exec),
        _make_tool("direct_answer", _rag_ok_exec),  # 不会走到
    ]

    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout)
        return IntentDecision(
            tool="text2sql_query",
            mode="text2sql",
            reasoning="该问题需要统计数据。",
            reasoning_full="该问题需要统计数据。",
            confidence=0.9,
            fallback=None,
            structured_signals=StructuredSignals(llm_prefers_sql=True, has_aggregation_signals=True),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "销售额下降原因"},
    )
    assert res.status_code == 200
    data = res.json()

    final_evt = next(e for e in data["events"] if e.get("type") == "agent.final")
    assert final_evt["payload"]["total_steps"] == 2
    assert "text2sql_query" in final_evt["payload"]["tools_used"]
    assert "rag_search" in final_evt["payload"]["tools_used"]


def test_v2_sse_stream_emits_agent_events(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _text2sql_fail_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=False,
            data=None,
            error="sql exec failed",
            error_code="SQL_EXEC_TABLE_NOT_FOUND",
            error_stage="sql.execute",
            latency_ms=7,
        )

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={
                "answer": "rag ok",
                "hits": [
                    {
                        "id": "1",
                        "content": "Content: hello",
                        "metadata": {
                            "filename": "a.md",
                            "relativePath": "diary/a.md",
                            "original_link": "http://example",
                            "slug": "slug-a",
                            "category": "diary",
                            "chunk_index": 0,
                        },
                        "fused_score": 1.0,
                    }
                ],
            },
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=4,
        )

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("text2sql_query", _text2sql_fail_exec),
        _make_tool("rag_search", _rag_ok_exec),
        _make_tool("direct_answer", _rag_ok_exec),  # 不会走到
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout)
        return IntentDecision(
            tool="text2sql_query",
            mode="text2sql",
            reasoning="该问题需要统计数据。",
            reasoning_full="该问题需要统计数据。",
            confidence=0.9,
            fallback=None,
            structured_signals=StructuredSignals(llm_prefers_sql=True, has_aggregation_signals=True),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    with client.stream(
        "POST",
        "/api/py/unified/chat/stream",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "销售额下降原因"},
    ) as res:
        assert res.status_code == 200
        text = ""
        for chunk in res.iter_text():
            text += chunk
            if "event: done" in text:
                break
        assert "event: chain" in text
        assert "agent.step.start" in text
        assert "agent.final" in text
        assert "event: done" in text


def test_v2_rag_empty_gated_fallback(monkeypatch: pytest.MonkeyPatch):
    """RAG_RETRIEVE_EMPTY + has_aggregation_signals=true -> fallback SQL（gated 生效）。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _rag_empty_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=False,
            data=None,
            error="RAG empty",
            error_code="RAG_RETRIEVE_EMPTY",
            error_stage="rag.retrieve",
            latency_ms=4,
        )

    async def _sql_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={"answer": "sql ok", "sql": "select 1", "columns": ["a"], "rows": [{"a": 1}]},
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=6,
        )

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("rag_search", _rag_empty_exec),
        _make_tool("text2sql_query", _sql_ok_exec),
        _make_tool("direct_answer", _sql_ok_exec),
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout)
        return IntentDecision(
            tool="rag_search",
            mode="rag",
            reasoning="先检索资料。",
            reasoning_full="先检索资料。",
            confidence=0.9,
            fallback=None,
            structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=True),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "按月统计销售额"},
    )
    assert res.status_code == 200
    data = res.json()
    final_evt = next(e for e in data["events"] if e.get("type") == "agent.final")
    assert final_evt["payload"]["total_steps"] == 2
    assert final_evt["payload"]["tools_used"][0] == "rag_search"
    assert "text2sql_query" in final_evt["payload"]["tools_used"]


def test_v2_intent_timeout_fallback_v1(monkeypatch: pytest.MonkeyPatch):
    """Intent LLM 超时 -> decide_intent_v2 内部降级到 V1 规则路由。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.intent_agent as intent_agent

    # 让 LLM 意图调用直接超时
    async def _timeout_llm(*_args: Any, **_kwargs: Any):  # noqa: ANN401
        raise asyncio.TimeoutError()

    monkeypatch.setattr(intent_agent, "_llm_decide_v2", _timeout_llm)

    # V1 规则路由稳定返回 rag
    class _V1:
        final_mode = "rag"

    monkeypatch.setattr(intent_agent, "decide_intent_v1", lambda *, query, prefer: _V1())  # noqa: ARG005

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(success=True, data={"answer": "rag ok", "hits": []}, latency_ms=2)

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("rag_search", _rag_ok_exec),
        _make_tool("text2sql_query", _rag_ok_exec),
        _make_tool("direct_answer", _rag_ok_exec),
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "hello"},
    )
    assert res.status_code == 200
    data = res.json()
    # 确认 agent.intent 仍存在，且 tool/mode 来自 v1 fallback（rag）
    intent_evt = next(e for e in data["events"] if e.get("type") == "agent.intent")
    assert intent_evt["payload"]["mode"] == "rag"


def test_v2_agent_disabled_regression(monkeypatch: pytest.MonkeyPatch):
    """CHATBI_USE_AGENT=false：必须走 V1，且 events 中不出现 agent.*。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat

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
            self.chat = self
            self.completions = self

        def create(self, **_kwargs: Any):  # noqa: ANN401
            return _ChatResp("direct answer")

    monkeypatch.setattr(unified_chat, "openai_siliconflow_client", lambda: _DummyOpenAI())

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "hello", "prefer": "no_data", "session_id": "s"},
    )
    assert res.status_code == 200
    data = res.json()
    types = [e.get("type") for e in data["events"]]
    assert all(not str(t).startswith("agent.") for t in types)

