from __future__ import annotations

import importlib
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

