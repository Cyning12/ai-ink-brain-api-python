"""vNext：Unified Agent SSE 增量路径（协商头 + CHATBI_SSE_INCREMENTAL）。"""
from __future__ import annotations

import importlib
import json
from typing import Any, Callable

import pytest
from fastapi.testclient import TestClient

from api.agent import AgentFinalView, AgentRunView
from api.intent_agent import IntentDecision, StructuredSignals
from api.tools import Tool, ToolName, ToolResult


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


def _parse_chain_objects(sse_text: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for block in sse_text.split("\n\n"):
        for line in block.split("\n"):
            if not line.startswith("data: "):
                continue
            raw = line[6:].strip()
            if not raw or raw.startswith(":"):
                continue
            try:
                j = json.loads(raw)
            except json.JSONDecodeError:
                continue
            if isinstance(j, dict) and j.get("type"):
                out.append(j)
    return out


def test_sse_incremental_meta_then_whitelisted_chain(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
    monkeypatch.setenv("CHATBI_SSE_INCREMENTAL", "true")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _rag_ok(
        *, query: str, history: list[dict[str, Any]] | None = None, debug_llm_prompts: bool = False
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history, debug_llm_prompts)
        return ToolResult(
            success=True,
            data={"answer": "stub-rag", "hits": []},
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
        _make_tool("rag_search", _rag_ok),
        _make_tool("direct_answer", _rag_ok),
        _make_tool("text2sql_query", _rag_ok),
    ]
    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry(dummy_tools))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
        return IntentDecision(
            tool="rag_search",
            mode="rag",
            reasoning="走 RAG。",
            reasoning_full="走 RAG。",
            confidence=0.9,
            fallback=None,
            structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=False),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    text = ""
    with client.stream(
        "POST",
        "/api/py/unified/chat/stream",
        headers={
            "Authorization": "Bearer api-key-123",
            "X-ChatBI-Sse-Contract": "2",
        },
        json={"session_id": "s1", "query": "hello"},
    ) as res:
        assert res.status_code == 200
        for chunk in res.iter_text():
            text += chunk
            if "event: done" in text:
                break

    chains = _parse_chain_objects(text)
    types = [c.get("type") for c in chains]
    assert types[0] == "meta"
    first_meaningful = types[1]
    assert first_meaningful in (
        "router.decision",
        "agent.step.start",
        "agent.intent",
        "agent.llm.start",
        "tool.call.start",
    )
    assert "agent.llm.delta" in types
    assert "assistant.message" in types
    assert "latency" in types


def test_sse_batch_without_contract_header_starts_with_router(monkeypatch: pytest.MonkeyPatch) -> None:
    """缺省协商头：保持 await run 后批量 replay，meta 后首条有意义 chain 为 router.decision。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
    monkeypatch.setenv("CHATBI_SSE_INCREMENTAL", "true")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _rag_ok(
        *, query: str, history: list[dict[str, Any]] | None = None, debug_llm_prompts: bool = False
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history, debug_llm_prompts)
        return ToolResult(success=True, data={"answer": "x", "hits": []}, error=None, error_code=None, error_stage=None, latency_ms=1)

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry([_make_tool("rag_search", _rag_ok), _make_tool("direct_answer", _rag_ok), _make_tool("text2sql_query", _rag_ok)]))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
        return IntentDecision(
            tool="rag_search",
            mode="rag",
            reasoning="r",
            reasoning_full="r",
            confidence=0.9,
            fallback=None,
            structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=False),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    text = ""
    with client.stream(
        "POST",
        "/api/py/unified/chat/stream",
        headers={"Authorization": "Bearer api-key-123"},
        json={"session_id": "s1", "query": "hello"},
    ) as res:
        for chunk in res.iter_text():
            text += chunk
            if "event: done" in text:
                break

    chains = _parse_chain_objects(text)
    assert chains[0]["type"] == "meta"
    assert chains[1]["type"] == "router.decision"
    assert "agent.llm.start" not in [c.get("type") for c in chains[:5]]


def test_sse_incremental_disabled_env_forces_batch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
    monkeypatch.setenv("CHATBI_SSE_INCREMENTAL", "false")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _rag_ok(
        *, query: str, history: list[dict[str, Any]] | None = None, debug_llm_prompts: bool = False
    ) -> ToolResult:  # noqa: ANN001
        _ = (query, history, debug_llm_prompts)
        return ToolResult(success=True, data={"answer": "x", "hits": []}, error=None, error_code=None, error_stage=None, latency_ms=1)

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    monkeypatch.setattr(unified_chat, "get_tool_registry", lambda: _DummyRegistry([_make_tool("rag_search", _rag_ok), _make_tool("direct_answer", _rag_ok), _make_tool("text2sql_query", _rag_ok)]))

    async def _fake_decide_intent_v2(*, query: str, history: list[dict[str, Any]], tools: list[Tool], min_confidence: float, timeout: float, **kwargs: Any):  # noqa: ANN001
        _ = (query, history, tools, min_confidence, timeout, kwargs)
        return IntentDecision(
            tool="rag_search",
            mode="rag",
            reasoning="r",
            reasoning_full="r",
            confidence=0.9,
            fallback=None,
            structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=False),
            raw_response={"used": "stub"},
        )

    monkeypatch.setattr(agent_module, "decide_intent_v2", _fake_decide_intent_v2)

    client = TestClient(index.app)
    text = ""
    with client.stream(
        "POST",
        "/api/py/unified/chat/stream",
        headers={
            "Authorization": "Bearer api-key-123",
            "X-ChatBI-Sse-Contract": "2",
        },
        json={"session_id": "s1", "query": "hello"},
    ) as res:
        for chunk in res.iter_text():
            text += chunk
            if "event: done" in text:
                break

    chains = _parse_chain_objects(text)
    assert chains[0]["type"] == "meta"
    assert chains[1]["type"] == "router.decision"


def test_sse_incremental_agent_run_raises_error_without_assistant_message(monkeypatch: pytest.MonkeyPatch) -> None:
    """vNext §8.3：异常路径无 assistant.message，仍到达 done（本仓固定为「空」策略 + error chain）。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_SSE_INCREMENTAL", "true")

    index = _reload_api_index(monkeypatch)
    import api.agent as agent_module

    async def _boom(self: Any, **kwargs: Any) -> AgentRunView:
        _ = self
        _ = kwargs
        raise RuntimeError("forced agent failure for pytest")

    monkeypatch.setattr(agent_module.ChatBIAgent, "run", _boom)

    client = TestClient(index.app)
    text = ""
    with client.stream(
        "POST",
        "/api/py/unified/chat/stream",
        headers={
            "Authorization": "Bearer api-key-123",
            "X-ChatBI-Sse-Contract": "2",
        },
        json={"session_id": "s1", "query": "hello"},
    ) as res:
        assert res.status_code == 200
        for chunk in res.iter_text():
            text += chunk
            if "event: done" in text:
                break

    chains = _parse_chain_objects(text)
    types = [c.get("type") for c in chains]
    assert types[0] == "meta"
    assert "error" in types
    assert "assistant.message" not in types
    assert "event: done" in text
    done_ok: bool | None = None
    for block in text.split("\n\n"):
        if "event: done" not in block:
            continue
        for line in block.split("\n"):
            if line.startswith("data: "):
                try:
                    done_ok = bool(json.loads(line[6:].strip()).get("ok"))
                except json.JSONDecodeError:
                    continue
    assert done_ok is False


def test_sse_incremental_queue_backpressure_emits_truncated(monkeypatch: pytest.MonkeyPatch) -> None:
    """vNext §4.3：emit 队列触顶时须出现 reason=backpressure 的 agent.llm.truncated。"""
    monkeypatch.setenv("CHATBI_USE_AGENT", "true")
    monkeypatch.setenv("CHATBI_SSE_INCREMENTAL", "true")
    monkeypatch.setenv("CHATBI_SSE_EMIT_QUEUE_MAX", "6")

    index = _reload_api_index(monkeypatch)
    import api.unified_chat as unified_chat
    import api.agent as agent_module

    async def _persist_ok(**kwargs: Any) -> dict[str, Any]:
        _ = kwargs
        return {"ok": True}

    monkeypatch.setattr(unified_chat, "_await_persist_chatbi_v2_agent_log", _persist_ok)

    async def _spam_emit_run(
        self: Any,
        *,
        query: str,
        session_id: str | None,
        prefer: str,
        sse_started_at: float | None = None,
        run_id: str | None = None,
        emit: Any = None,
        debug_router: bool = False,
        debug_llm_prompts: bool = False,
        intent_obs_payload_fn: Any = None,
        plan_execution_token: str | None = None,
    ) -> AgentRunView:
        _ = (
            self,
            query,
            session_id,
            prefer,
            sse_started_at,
            run_id,
            debug_router,
            debug_llm_prompts,
            intent_obs_payload_fn,
            plan_execution_token,
        )
        if emit is None:
            raise AssertionError("emit required")
        for i in range(40):
            await emit(
                {
                    "type": "agent.llm.delta",
                    "ts": i,
                    "step_id": "spam_bp",
                    "payload": {"text": str(i), "part_index": i},
                }
            )
        return AgentRunView(
            intent_decision=None,
            steps=[],
            final=AgentFinalView(
                answer="spam-done",
                mode="rag",
                total_steps=1,
                tools_used=["rag_search"],
                modes=["rag"],
                fallback_used=False,
            ),
        )

    monkeypatch.setattr(agent_module.ChatBIAgent, "run", _spam_emit_run)

    client = TestClient(index.app)
    # 读完全部 SSE 再解析：勿在出现子串 `event: done` 时提前 break，否则可能截断在
    # `event: chain` 块中间，漏掉后续 `agent.llm.truncated`（与 iter_text 分块边界有关）。
    raw = b""
    with client.stream(
        "POST",
        "/api/py/unified/chat/stream",
        headers={
            "Authorization": "Bearer api-key-123",
            "X-ChatBI-Sse-Contract": "2",
        },
        json={"session_id": "s1", "query": "hello"},
    ) as res:
        assert res.status_code == 200
        for chunk in res.iter_bytes():
            raw += chunk
    text = raw.decode("utf-8")

    chains = _parse_chain_objects(text)
    truncated = [c for c in chains if c.get("type") == "agent.llm.truncated"]
    assert truncated, "expected at least one agent.llm.truncated under small queue + spam emit"
    assert any((t.get("payload") or {}).get("reason") == "backpressure" for t in truncated)
