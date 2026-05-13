from __future__ import annotations

import importlib
import asyncio
import datetime as dt
from decimal import Decimal
from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient

from api.intent_agent import IntentDecision, StructuredSignals, clear_intent_cache
from api.tools import Tool, ToolResult, ToolName

# --- L5 / FailureTypeHandler：pytest mock 注入点（总规 SPEC-ChatBI-V2-Agent-Overview §7.5.4）---
# 完整说明与示例 A/B 逐步拆解见：docs/diary/L5-ChatBI-V2-FailureTypeHandler-pytest指南.md
# ① error_code：在 dummy 工具 execute 返回的 ToolResult 上设置（勿改 agent.py decide_next）。
# ② 工具表：monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))。
# ③ 意图与 gating：monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_...)，用 IntentDecision(...) +
#    StructuredSignals；字段调整请 dataclasses.replace，禁止 intent.tool = ...。
# ④ 自然「必 RAG」query：CHATBI_V2_INTENT_LLM=false 且不 patch decide_intent_v2；仅 ①+②；query 不含
#    text2sql 启发式关键词，见 test_v2_natural_diary_query_rag_empty_fallback_to_direct。
# canonical（gated SQL）：test_v2_rag_empty_gated_fallback。

# 含「日记」、无统计类关键词：启发式意图首工具恒为 rag_search（不依赖外呼 LLM）。
RAG_FIRST_DIARY_QUERY = "2026-04-28日记的大致内容"


def _reload_api_index(monkeypatch: pytest.MonkeyPatch, *, auth_override: bool = True) -> Any:
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
    if auth_override:
        from tests._chatbi_auth_overrides import install_unified_chat_auth_override

        install_unified_chat_auth_override(index.app)
    else:
        from tests._chatbi_auth_overrides import clear_unified_chat_auth_override

        clear_unified_chat_auth_override(index.app)
    return index


def _make_tool(name: ToolName, execute: Callable[..., Any]) -> Tool:
    async def _exec(
        query: str,
        *,
        history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
        **_: Any,
    ) -> ToolResult:  # noqa: ANN001
        return await execute(query=query, history=history, debug_llm_prompts=debug_llm_prompts)

    return Tool(name=name, description=f"dummy-{name}", parameters={}, execute=_exec)


def test_v2_json_single_tool_fallback_used_true(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _direct_answer_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={"answer": "direct ok"},
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=2,
        )

    async def _rag_search_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
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

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
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

    async def _text2sql_fail_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=False,
            data=None,
            error="sql exec failed",
            error_code="SQL_EXEC_TABLE_NOT_FOUND",
            error_stage="sql.execute",
            latency_ms=7,
        )

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
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

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
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


def test_v2_db_log_text2sql_exec_trace_filters_id_number(monkeypatch: pytest.MonkeyPatch):
    """V2：mode=text2sql 时落库 router_trace_v1.text2sql_exec，且 rows_preview 过滤 id_number。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.rag_env as rag_env_module
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    # mock text2sql tool returns sql + rows with id_number
    async def _sql_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={
                "answer": "sql ok",
                "sql": "select id_number, name from customer_info limit 1",
                "columns": ["id_number", "name"],
                "rows": [{"id_number": "123456", "name": "张三"}],
            },
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=6,
        )

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(success=True, data={"answer": "rag ok", "hits": []}, latency_ms=3)

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("text2sql_query", _sql_exec),
        _make_tool("rag_search", _rag_ok_exec),
        _make_tool("direct_answer", _rag_ok_exec),
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
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

    saved: list[dict[str, Any]] = []

    class _Insert:
        def __init__(self, payload: dict[str, Any]) -> None:
            self._payload = payload

        def execute(self) -> Any:  # noqa: ANN401
            saved.append(self._payload)
            return type("_R", (), {"data": []})()

    class _Table:
        def insert(self, payload: dict[str, Any]) -> _Insert:
            return _Insert(payload)

    class _Sb:
        def table(self, name: str) -> _Table:
            assert name == "rag_conversation_logs"
            return _Table()

    # 落库走 rag_env.supabase_table_insert_with_retry → rag_env.supabase_client（非 unified_chat 命名空间）
    monkeypatch.setattr(rag_env_module, "supabase_client", lambda: _Sb())

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "统计客户数量", "session_id": "s"},
    )
    assert res.status_code == 200
    assert saved, "expected db insert payload"
    meta = saved[-1].get("metadata") if isinstance(saved[-1].get("metadata"), dict) else {}
    router_debug = meta.get("router_debug") if isinstance(meta.get("router_debug"), dict) else {}
    trace = router_debug.get("router_trace_v1") if isinstance(router_debug.get("router_trace_v1"), dict) else {}
    t2 = trace.get("text2sql_exec") if isinstance(trace.get("text2sql_exec"), dict) else {}
    assert t2.get("sql")
    assert t2.get("rows_len") == 1
    rows_preview = t2.get("rows_preview")
    assert isinstance(rows_preview, list) and rows_preview, "expected rows_preview"
    row0 = rows_preview[0] if isinstance(rows_preview[0], dict) else {}
    assert "id_number" not in row0


def test_v2_sse_stream_emits_agent_events(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _text2sql_fail_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=False,
            data=None,
            error="sql exec failed",
            error_code="SQL_EXEC_TABLE_NOT_FOUND",
            error_stage="sql.execute",
            latency_ms=7,
        )

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
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

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
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


def test_v2_sse_stream_sql_result_jsonable_encoder(monkeypatch: pytest.MonkeyPatch):
    """SSE V2：sql.result 中包含 Decimal/date/datetime 也不应导致序列化崩溃。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _sql_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={
                "answer": "sql ok",
                "sql": "select 1",
                "columns": ["amount", "created_at", "birthday"],
                "rows": [
                    {
                        "amount": Decimal("12.34"),
                        "created_at": dt.datetime(2020, 1, 2, 3, 4, 5),
                        "birthday": dt.date(1990, 8, 27),
                    }
                ],
            },
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=6,
        )

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(success=True, data={"answer": "rag ok", "hits": []}, latency_ms=3)

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("text2sql_query", _sql_exec),
        _make_tool("rag_search", _rag_ok_exec),
        _make_tool("direct_answer", _rag_ok_exec),
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
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
        json={"query": "统计客户数量"},
    ) as res:
        assert res.status_code == 200
        text = ""
        for chunk in res.iter_text():
            text += chunk
            if "event: done" in text:
                break
        assert "event: chain" in text
        assert "sql.result" in text
        assert "SSE V2 运行异常" not in text
        assert "event: done" in text


def test_v2_rag_empty_gated_fallback(monkeypatch: pytest.MonkeyPatch):
    """RAG_RETRIEVE_EMPTY + has_aggregation_signals=true -> fallback SQL（gated 生效）。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    # [mock ①a] 首步 rag_search：ToolResult.error_code=RAG_RETRIEVE_EMPTY（模拟检索无命中）。
    async def _rag_empty_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=False,
            data=None,
            error="RAG empty",
            error_code="RAG_RETRIEVE_EMPTY",
            error_stage="rag.retrieve",
            latency_ms=4,
        )

    # [mock ①b] 第二步 text2sql_query：成功桩，验证 gated fallback 后下一工具可执行。
    async def _sql_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
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
    # [mock ②] 见文件头说明：替换 get_tool_registry，本轮仅使用 dummy_tools。
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    # [mock ③] 见文件头说明：替换 decide_intent_v2；首工具 rag_search + has_aggregation_signals 驱动 gating。
    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
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
    # 请求体仅作语义占位；首步工具与失败码完全由 [mock ②][mock ③] 决定。
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "按月统计销售额"},
    )
    assert res.status_code == 200
    data = res.json()
    # [验收] agent.final：先 rag_search，再因 RAG_RETRIEVE_EMPTY + gating 出现 text2sql_query。
    final_evt = next(e for e in data["events"] if e.get("type") == "agent.final")
    assert final_evt["payload"]["total_steps"] == 2
    assert final_evt["payload"]["tools_used"][0] == "rag_search"
    assert "text2sql_query" in final_evt["payload"]["tools_used"]


def test_v2_text2sql_write_denied_stops_without_rag(monkeypatch: pytest.MonkeyPatch):
    """CHATBI_SQL_WRITE_DENIED：直接终态回答，不调用 rag_search。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    t2s_calls = {"n": 0}

    async def _t2s_fail(
        *,
        query: str,
        history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
        **kwargs: Any,
    ) -> ToolResult:
        _ = (query, history, debug_llm_prompts, kwargs)
        t2s_calls["n"] += 1
        return ToolResult(
            success=False,
            data={"text2sql_phases_ms": {"retrieve": 1}},
            error="当前账号无权对该表执行写入或更新（表级安全策略限制）。",
            error_code="CHATBI_SQL_WRITE_DENIED",
            error_stage="text2sql.schema_prefetch",
            latency_ms=3,
        )

    async def _rag_must_not_run(
        *,
        query: str,
        history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:
        raise AssertionError("无权限 Text2SQL 后不应再尝试 RAG")

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("text2sql_query", _t2s_fail),
        _make_tool("rag_search", _rag_must_not_run),
        _make_tool("direct_answer", _rag_must_not_run),
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_intent(
        *,
        query: str,
        history: list[dict[str, Any]],
        tools: list[Tool],
        min_confidence: float,
        timeout: float,
        **kwargs: Any,
    ) -> IntentDecision:
        _ = (query, history, tools, min_confidence, timeout, kwargs)
        return IntentDecision(
            tool="text2sql_query",
            mode="text2sql",
            reasoning="写库",
            reasoning_full="写库",
            confidence=0.95,
            fallback=None,
            structured_signals=StructuredSignals(llm_prefers_sql=True, has_aggregation_signals=True),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_intent)

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "插入 agent_info 一行数据"},
    )
    assert res.status_code == 200
    data = res.json()
    final_evt = next(e for e in data["events"] if e.get("type") == "agent.final")
    assert t2s_calls["n"] == 1
    assert final_evt["payload"]["tools_used"] == ["text2sql_query"]
    ans_evt = next(e for e in data["events"] if e.get("type") == "assistant.message")
    assert "无权" in ans_evt["payload"]["content"]
    assert "问题太复杂" not in ans_evt["payload"]["content"]


def test_v2_natural_diary_query_rag_empty_fallback_to_direct(monkeypatch: pytest.MonkeyPatch):
    """自然 query 首步必 rag：不 patch decide_intent_v2；rag 空命中且无 SQL gating 时走 direct_answer。

    与 test_v2_rag_empty_gated_fallback 区别：本用例验证「无聚合/SQL 信号」时不得盲启 text2sql_query。
    """
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
    # 与启发式 rag 置信度（约 0.68）对齐，避免开发者 .env 提高 INTENT_MIN_CONFIDENCE 后首步误切 fallback
    monkeypatch.setenv("INTENT_MIN_CONFIDENCE", "0.6")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat

    clear_intent_cache()

    async def _rag_empty_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=False,
            data=None,
            error="RAG empty",
            error_code="RAG_RETRIEVE_EMPTY",
            error_stage="rag.retrieve",
            latency_ms=2,
        )

    async def _direct_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={"answer": "stub：库中未检索到该日日记正文。"},
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=3,
        )

    async def _sql_must_not_run(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
        raise AssertionError("无 gating 时不应调用 text2sql_query")

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("rag_search", _rag_empty_exec),
        _make_tool("direct_answer", _direct_ok_exec),
        _make_tool("text2sql_query", _sql_must_not_run),
    ]
    # [mock ②] 仅替换工具表；[mock ③] 不使用——走真实 decide_intent_v2（启发式）。
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": RAG_FIRST_DIARY_QUERY},
    )
    assert res.status_code == 200
    data = res.json()
    final_evt = next(e for e in data["events"] if e.get("type") == "agent.final")
    used = final_evt["payload"]["tools_used"]
    assert used[0] == "rag_search"
    assert used[1] == "direct_answer"
    assert "text2sql_query" not in used
    assert final_evt["payload"]["total_steps"] == 2


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

    async def _rag_ok_exec(*, query: str, history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
    ) -> ToolResult:  # noqa: ANN001
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


def test_v3_low_confidence_clarify_json_skips_text2sql(monkeypatch: pytest.MonkeyPatch):
    """P1-4 §4.3：CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1 时须下发 agent.clarify 且不执行 text2sql_query。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
    monkeypatch.setenv("CHATBI_V3_LOW_CONFIDENCE_CLARIFY", "1")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    t2s_calls = {"n": 0}

    async def _text2sql_forbidden(
        *,
        query: str,
        history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
        **_: Any,
    ) -> ToolResult:  # noqa: ANN401
        _ = (query, history, debug_llm_prompts)
        t2s_calls["n"] += 1
        raise AssertionError("text2sql must not run under clarify short-circuit")

    async def _rag_ok_exec(
        *, query: str, history: list[dict[str, Any]] | None = None, debug_llm_prompts: bool = False
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={"answer": "rag ok", "hits": []},
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=2,
        )

    async def _direct_ok_exec(
        *, query: str, history: list[dict[str, Any]] | None = None, debug_llm_prompts: bool = False
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history)
        return ToolResult(
            success=True,
            data={"answer": "direct"},
            error=None,
            error_code=None,
            error_stage=None,
            latency_ms=1,
        )

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    dummy_tools = [
        _make_tool("direct_answer", _direct_ok_exec),
        _make_tool("rag_search", _rag_ok_exec),
        _make_tool("text2sql_query", _text2sql_forbidden),
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(
        *,
        query: str,
        history: list[dict[str, Any]],
        tools: list[Tool],
        min_confidence: float,
        timeout: float,
        **kwargs: Any,
    ):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
        return IntentDecision(
            tool="text2sql_query",
            mode="text2sql",
            reasoning="stub reasoning for test",
            reasoning_full="stub reasoning for test",
            confidence=0.35,
            fallback="rag_search",
            structured_signals=StructuredSignals(llm_prefers_sql=True, has_aggregation_signals=False),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    res = client.post(
        "/api/py/unified/chat",
        headers={"Authorization": "Bearer api-key-123"},
        json={"query": "低置信查数探针", "prefer": "auto"},
    )
    assert res.status_code == 200
    data = res.json()
    types = [e.get("type") for e in data["events"]]
    assert "agent.clarify" in types
    assert t2s_calls["n"] == 0
    clarify_evt = next(e for e in data["events"] if e.get("type") == "agent.clarify")
    assert clarify_evt["payload"]["message"] == "待您澄清（低置信度）"
    assert "请补充您关心" in clarify_evt["payload"]["prompt_for_user"]

    rd = next(e for e in data["events"] if e.get("type") == "router.decision")
    assert rd["payload"]["candidate_mode"] == "text2sql"
    assert rd["payload"]["final_mode"] == "text2sql"

