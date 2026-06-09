from __future__ import annotations

import asyncio
import json
import os
import time
import uuid
from typing import Any, Literal

from fastapi import HTTPException, Request
from fastapi.responses import StreamingResponse
from openai import OpenAI

from ..agent import AgentRunView, ChatBIAgent
from ..agent_memory import get_memory_store
from ..chatbi_policies import load_chatbi_table_policies_sync
from ..chatbi_principal import ChatBiPrincipal
from ..chatbi_request_ctx import set_chatbi_log_ctx, set_chatbi_principal
from ..chatbi_sql_gate import (
    ChatBiSqlGateDenied,
    apply_chatbi_sql_gate,
    filter_text2sql_retrieved,
)
from ..hybrid_fusion import fuse_hits_rrf
from ..intent_router import decide_intent
from ..query_rewrite import rewrite_query_with_history
from ..rag_embedding_guard import ensure_embedding_alignment
from ..rag_env import (
    embedding_kwargs_for_inputs,
    openai_siliconflow_client,
    siliconflow_base,
    supabase_client,
)
from ..rag_recall_tools import (
    keyword_query_text_with_i18n_meta,
    rpc_execute_with_retry,
    structured_recall_by_date,
)
from ..rag_shared import parse_match_threshold
from ..text2sql_core import (
    build_sql_prompt,
    build_summary_prompt,
    execute_mutating_sql,
    execute_select_sql,
    llm_generate_sql,
    llm_summarize,
)
from ..text2sql_schema_prefetch import run_text2sql_schema_prefetch_sync
from ..text2sql_store import get_text2sql_store
from ..text2sql_value_hints import build_value_hints_block_for_text2sql
from ..tools import get_tool_registry

# Import shared helpers from unified_chat to avoid duplication.
from ..unified_chat import (
    _agent_intent_obs_payload,
    _async_save_rag_log,
    _await_persist_chatbi_v2_agent_log,
    _build_query_expand_event_payload,
    _build_rag_sources_event,
    _build_text2sql_exec_trace,
    _chatbi_log_ctx,
    _clarify_short_circuit_events,
    _debug_llm_prompts_enabled,
    _debug_router_evidence_enabled,
    _event,
    _now_ms,
    _parse_prefer,
    _rag_generate_answer,
    _router_agent_evidence,
    _router_evidence_db_log_enabled,
    _router_trace_db_log_enabled,
    _safe_text_for_event,
    _shrink_router_trace_v1,
    _sse_emit_queue_event_estimate_chars,
    _sse_emit_queue_maxsize,
    _unified_agent_sse_incremental,
    _unified_prompt_guard_short_circuit_events,
)

PreferMode = Literal["auto", "rag", "text2sql", "no_data"]


def _sse(event: str, data: dict[str, Any]) -> str:
    # SSE 要求每条消息以空行结束
    # 注意：SSE 分支使用 json.dumps，无法像 JSONResponse 一样自动处理 Decimal/date/datetime 等类型。
    # 这里统一做 jsonable_encoder，避免在后续事件（如 sql.result rows）序列化时报错，导致 SSE 中断。
    try:
        from fastapi.encoders import jsonable_encoder

        safe = jsonable_encoder(data)
    except Exception:  # noqa: BLE001
        safe = data
    payload = json.dumps(safe, ensure_ascii=False, separators=(",", ":"), default=str)
    return f"event: {event}\ndata: {payload}\n\n"


async def handle_unified_chat_stream(
    request: Request,
    *,
    principal: ChatBiPrincipal,
) -> StreamingResponse:
    """SSE：实时输出 chain 事件，最终输出 done。v1 不强制 token 级文本流。"""
    ctx_log = _chatbi_log_ctx(request)
    set_chatbi_principal(principal)
    set_chatbi_log_ctx(ctx_log)

    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    query = body.get("query")
    if not isinstance(query, str) or not query.strip():
        raise HTTPException(status_code=400, detail="Missing required field: query")
    session_id = body.get("session_id") if isinstance(body.get("session_id"), str) else None
    prefer = _parse_prefer(body.get("prefer"))
    _pet_raw = body.get("plan_execution_token")
    plan_execution_token: str | None = None
    if isinstance(_pet_raw, str) and _pet_raw.strip():
        plan_execution_token = _pet_raw.strip()

    started_at = time.perf_counter()
    run_id = str(uuid.uuid4())
    ctx_log["run_id"] = run_id
    debug_router = _debug_router_evidence_enabled() or bool(body.get("debug_router") is True)
    debug_llm_prompts = _debug_llm_prompts_enabled(body)
    db_log_router = _router_evidence_db_log_enabled() or bool(body.get("debug_router") is True)
    db_log_router_trace = _router_trace_db_log_enabled() or bool(body.get("debug_router") is True)

    # CHATBI v2（Agent）SSE 主路径
    use_agent = (os.getenv("CHATBI_USE_AGENT", "false") or "").strip().lower() in ("1", "true", "yes", "on")
    if use_agent:
        if str(prefer).startswith("tool:"):
            mode = str(prefer)

            async def event_stream():
                ok_local = False
                try:
                    yield _sse(
                        "chain",
                        {"type": "meta", "ts": _now_ms(started_at), "step_id": "m1", "payload": {"run_id": run_id, "mode": mode, "session_id": session_id}},
                    )
                    _pg_tool_ab, _pg_tool_evs = _unified_prompt_guard_short_circuit_events(
                        query,
                        ctx_log=ctx_log,
                        run_id=run_id,
                        session_id=session_id,
                        started_at=started_at,
                        route="unified_chat_sse",
                    )
                    if _pg_tool_ab:
                        for _gev in _pg_tool_evs:
                            yield _sse("chain", _gev)
                    else:
                        yield _sse(
                            "chain",
                            _event(
                                typ="error",
                                started_at=started_at,
                                step_id="e_agent",
                                payload={"stage": "agent", "message": f"未实现的工具路由：{prefer}"},
                            ),
                        )
                except GeneratorExit:
                    return
                except Exception as exc:  # noqa: BLE001
                    _ = exc
                    ok_local = False
                finally:
                    yield _sse(
                        "done",
                        {
                            "ok": ok_local,
                            "mode": mode,
                            "run_id": run_id,
                            "request_id": run_id,
                            "session_id": session_id,
                        },
                    )

            headers = {"Cache-Control": "no-cache"}
            return StreamingResponse(event_stream(), media_type="text/event-stream; charset=utf-8", headers=headers)

        tool_registry = get_tool_registry()
        agent = ChatBIAgent(tools=tool_registry.list_tools(), memory=get_memory_store())
        max_steps = max(1, int(os.getenv("AGENT_MAX_STEPS", "5")))
        sse_incremental = _unified_agent_sse_incremental(request)

        async def event_stream():
            agent_result: AgentRunView | None = None
            mode_local: str = "auto" if prefer == "auto" else str(prefer)
            ok_local = False
            persist_result: dict[str, Any] | None = None
            try:
                yield _sse(
                    "chain",
                    {
                        "type": "meta",
                        "ts": _now_ms(started_at),
                        "step_id": "m1",
                        "payload": {"run_id": run_id, "mode": mode_local, "session_id": session_id},
                    },
                )

                _pg_ab, _pg_evs = _unified_prompt_guard_short_circuit_events(
                    query,
                    ctx_log=ctx_log,
                    run_id=run_id,
                    session_id=session_id,
                    started_at=started_at,
                    route="unified_chat_sse",
                )
                if _pg_ab:
                    for _gev in _pg_evs:
                        yield _sse("chain", _gev)
                    ok_local = False
                if not _pg_ab:
                    if sse_incremental:
                        # G2：Agent 内 emit → 队列 → 本生成器边收边 yield（vNext 协商头 + CHATBI_SSE_INCREMENTAL）
                        q: asyncio.Queue[dict[str, Any] | None] = asyncio.Queue(maxsize=_sse_emit_queue_maxsize())
                        holder: dict[str, Any] = {}
                        overflow_pending: list[dict[str, Any]] = []

                        async def forward(ev: dict[str, Any]) -> None:
                            try:
                                q.put_nowait(ev)
                                return
                            except asyncio.QueueFull:
                                sid = ev.get("step_id") if isinstance(ev.get("step_id"), str) else "bp1"
                                overflow_pending.append(
                                    _event(
                                        typ="agent.llm.truncated",
                                        started_at=started_at,
                                        step_id=sid,
                                        payload={
                                            "dropped_chars": _sse_emit_queue_event_estimate_chars(ev),
                                            "reason": "backpressure",
                                        },
                                    )
                                )
                            await q.put(ev)

                        async def runner() -> None:
                            try:
                                holder["agent_result"] = await agent.run(
                                    query=query,
                                    session_id=session_id,
                                    prefer=prefer,
                                    sse_started_at=started_at,
                                    run_id=run_id,
                                    emit=forward,
                                    debug_router=debug_router,
                                    debug_llm_prompts=debug_llm_prompts,
                                    intent_obs_payload_fn=lambda d: _agent_intent_obs_payload(d, debug_router=debug_router),
                                    plan_execution_token=plan_execution_token,
                                )
                            except Exception as exc:  # noqa: BLE001
                                holder["exc"] = exc
                            finally:
                                await q.put(None)

                        run_task = asyncio.create_task(runner())
                        try:
                            _iv = float((os.getenv("SSE_KEEPALIVE_INTERVAL_S") or "15").strip() or "15")
                        except Exception:  # noqa: BLE001
                            _iv = 15.0
                        _iv = max(5.0, min(_iv, 60.0))
                        while True:
                            while overflow_pending:
                                yield _sse("chain", overflow_pending.pop(0))
                            try:
                                item = await asyncio.wait_for(q.get(), timeout=_iv)
                            except asyncio.TimeoutError:
                                if run_task.done():
                                    break
                                yield ": sse-keepalive\n\n"
                                continue
                            if item is None:
                                break
                            yield _sse("chain", item)
                        await run_task
                        while overflow_pending:
                            yield _sse("chain", overflow_pending.pop(0))
                        while True:
                            try:
                                tail = q.get_nowait()
                            except asyncio.QueueEmpty:
                                break
                            if tail is not None:
                                yield _sse("chain", tail)
                        exc_run = holder.get("exc")
                        if exc_run is not None:
                            ok_local = False
                            yield _sse(
                                "chain",
                                _event(
                                    typ="error",
                                    started_at=started_at,
                                    step_id="e_agent_run",
                                    payload={"stage": "agent", "message": str(exc_run)[:500]},
                                ),
                            )
                        else:
                            agent_result = holder.get("agent_result")
                            if agent_result is not None:
                                ok_local = True
                                mode_local = agent_result.final.mode
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="latency",
                                        started_at=started_at,
                                        step_id="l1",
                                        payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                                    ),
                                )
                                persist_result = await _await_persist_chatbi_v2_agent_log(
                                    session_id=session_id,
                                    query=query,
                                    run_id=run_id,
                                    prefer=prefer,
                                    started_at=started_at,
                                    agent_result=agent_result,
                                )
                                if not persist_result.get("ok"):
                                    yield _sse(
                                        "chain",
                                        _event(
                                            typ="error",
                                            started_at=started_at,
                                            step_id="e_agent_db",
                                            payload={
                                                "stage": "agent_db",
                                                "message": (str(persist_result.get("error") or "persist_failed"))[:500],
                                                "persist": persist_result,
                                            },
                                        ),
                                    )
                    else:
                        # 批量 replay：await run 结束后再按旧顺序 yield（兼容缺省协商头）
                        _run_task = asyncio.create_task(
                            agent.run(
                                query=query,
                                session_id=session_id,
                                prefer=prefer,
                                sse_started_at=started_at,
                                run_id=run_id,
                                debug_llm_prompts=debug_llm_prompts,
                                plan_execution_token=plan_execution_token,
                            )
                        )
                        try:
                            _iv = float((os.getenv("SSE_KEEPALIVE_INTERVAL_S") or "15").strip() or "15")
                        except Exception:  # noqa: BLE001
                            _iv = 15.0
                        _iv = max(5.0, min(_iv, 60.0))
                        while not _run_task.done():
                            await asyncio.wait({_run_task}, timeout=_iv)
                            if _run_task.done():
                                break
                            yield ": sse-keepalive\n\n"
                        agent_result = await _run_task
                        mode_local = agent_result.final.mode
                        ok_local = True

                    if not sse_incremental:
                        intent_decision = agent_result.intent_decision
                        step1 = agent_result.steps[0] if agent_result.steps else None
                        step1_mode = step1.mode if step1 else mode_local
                        candidate_mode = intent_decision.mode if intent_decision else step1_mode
                        final_mode = step1_mode

                        yield _sse(
                            "chain",
                            _event(
                                typ="router.decision",
                                started_at=started_at,
                                step_id="r1",
                                payload={
                                    "prefer": "auto" if prefer == "auto" else prefer,
                                    "candidate_mode": candidate_mode,
                                    "final_mode": final_mode,
                                    "rule_hits": [],
                                    "evidence": _router_agent_evidence(intent_decision),
                                    "fallback": intent_decision.fallback if intent_decision else None,
                                },
                            ),
                        )

                        for ev in _clarify_short_circuit_events(
                            agent_result=agent_result,
                            started_at=started_at,
                            max_steps=max_steps,
                            debug_router=debug_router,
                            debug_llm_prompts=debug_llm_prompts,
                        ):
                            yield _sse("chain", ev)

                        for step in agent_result.steps:
                            step_id = f"a{step.step_number}"
                            yield _sse(
                                "chain",
                                _event(
                                    typ="agent.step.start",
                                    started_at=started_at,
                                    step_id=step_id,
                                    payload={"step_number": step.step_number, "max_steps": max_steps},
                                ),
                            )

                            if step.step_number == 1 and intent_decision is not None:
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="agent.intent",
                                        started_at=started_at,
                                        step_id="intent_1",
                                        payload=_agent_intent_obs_payload(intent_decision, debug_router=debug_router),
                                    ),
                                )
                                if debug_llm_prompts and isinstance(intent_decision.raw_response, dict):
                                    _ilp2 = intent_decision.raw_response.get("llm_prompts")
                                    if isinstance(_ilp2, list) and _ilp2:
                                        yield _sse(
                                            "chain",
                                            _event(
                                                typ="agent.debug.llm_prompts",
                                                started_at=started_at,
                                                step_id="intent_llm_replay",
                                                payload={"scope": "intent", "items": _ilp2},
                                            ),
                                        )

                            yield _sse(
                                "chain",
                                _event(
                                    typ="agent.think",
                                    started_at=started_at,
                                    step_id=f"{step_id}_think",
                                    payload={
                                        "step_number": step.step_number,
                                        "thought": step.think_payload["thought"],
                                        "selected_tool": step.think_payload["selected_tool"],
                                        "mode": step.think_payload["mode"],
                                        "confidence": step.think_payload["confidence"],
                                    },
                                ),
                            )

                            td2 = step.tool_result.data if isinstance(step.tool_result.data, dict) else {}
                            if step.tool_used == "rag_search":
                                _rw2 = td2.get("rewritten") if isinstance(td2.get("rewritten"), str) else ""
                                _rw_ms2 = int(td2.get("rewrite_latency_ms") or 0)
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="tool.call.start",
                                        started_at=started_at,
                                        step_id=f"t_step{step.step_number}_rewrite",
                                        payload={"tool": "rag.rewrite", "input": {"query": query}},
                                    ),
                                )
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="tool.call.end",
                                        started_at=started_at,
                                        step_id=f"t_step{step.step_number}_rewrite",
                                        payload={
                                            "output": {"rewritten_query": _rw2 or query},
                                            "error": None,
                                            "latency_ms": _rw_ms2,
                                        },
                                    ),
                                )
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="tool.call.start",
                                        started_at=started_at,
                                        step_id=f"t_step{step.step_number}",
                                        payload={"tool": "rag_search", "input": {"query": query, "rewritten_query": _rw2 or query}},
                                    ),
                                )
                            else:
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="tool.call.start",
                                        started_at=started_at,
                                        step_id=f"t_step{step.step_number}",
                                        payload={"tool": step.tool_used, "input": {"query": query}},
                                    ),
                                )

                            err = step.tool_result.error
                            out_answer: str | None = None
                            if step.tool_result.data and isinstance(step.tool_result.data.get("answer"), str):
                                out_answer = step.tool_result.data.get("answer")

                            _out_payload_replay: dict[str, Any] = {}
                            if out_answer is not None:
                                _out_payload_replay["answer"] = out_answer
                            if step.tool_used == "rag_search" and isinstance(td2.get("rewritten"), str):
                                _out_payload_replay["rewritten_query"] = td2["rewritten"]

                            yield _sse(
                                "chain",
                                _event(
                                    typ="tool.call.end",
                                    started_at=started_at,
                                    step_id=f"t_step{step.step_number}",
                                    payload={
                                        "output": _out_payload_replay,
                                        "error": err,
                                        "latency_ms": step.tool_result.latency_ms,
                                    },
                                ),
                            )
                            if debug_llm_prompts and isinstance(td2.get("llm_prompts"), list) and td2.get("llm_prompts"):
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="agent.debug.llm_prompts",
                                        started_at=started_at,
                                        step_id=f"tool_llm_replay_{step.step_number}",
                                        payload={
                                            "scope": "tool",
                                            "tool": step.tool_used,
                                            "step_number": step.step_number,
                                            "items": td2["llm_prompts"],
                                        },
                                    ),
                                )

                            if step.tool_used == "text2sql_query" and step.tool_result.success and step.tool_result.data:
                                data = step.tool_result.data
                                columns_any = data.get("columns")
                                columns = columns_any if isinstance(columns_any, list) else []
                                rows_any = data.get("rows")
                                rows_any2 = rows_any if isinstance(rows_any, list) else []
                                rows: list[dict[str, Any]] = [r for r in rows_any2 if isinstance(r, dict)]
                                truncated = len(rows) > 20
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="sql.result",
                                        started_at=started_at,
                                        step_id=f"q_step{step.step_number}",
                                        payload={
                                            "sql": data.get("sql") if isinstance(data.get("sql"), str) else "",
                                            "columns": [c for c in columns if isinstance(c, str)],
                                            "rows": rows[:20],
                                            "truncated": truncated,
                                        },
                                    ),
                                )
                            elif step.tool_used == "rag_search" and step.tool_result.success and step.tool_result.data:
                                data = step.tool_result.data
                                hits_any = data.get("hits")
                                hits: list[dict[str, Any]] = hits_any if isinstance(hits_any, list) else []
                                yield _sse(
                                    "chain",
                                    _event(
                                        typ="rag.sources",
                                        started_at=started_at,
                                        step_id=f"s_step{step.step_number}",
                                        payload=_build_rag_sources_event(hits, top_k=10),
                                    ),
                                )

                            yield _sse(
                                "chain",
                                _event(
                                    typ="agent.step.end",
                                    started_at=started_at,
                                    step_id=f"{step_id}_end",
                                    payload={
                                        "step_number": step.step_number,
                                        "tool_used": step.tool_used,
                                        "mode": step.mode,
                                        "success": step.success,
                                        "next_action": step.next_action,
                                    },
                                ),
                            )

                        yield _sse(
                            "chain",
                            _event(
                                typ="agent.final",
                                started_at=started_at,
                                step_id="a_final",
                                payload={
                                    "total_steps": agent_result.final.total_steps,
                                    "tools_used": agent_result.final.tools_used,
                                    "modes": agent_result.final.modes,
                                    "fallback_used": agent_result.final.fallback_used,
                                },
                            ),
                        )

                        yield _sse(
                            "chain",
                            _event(
                                typ="assistant.message",
                                started_at=started_at,
                                step_id="s_answer",
                                payload={"role": "assistant", "content": agent_result.final.answer},
                            ),
                        )

                        yield _sse(
                            "chain",
                            _event(
                                typ="latency",
                                started_at=started_at,
                                step_id="l1",
                                payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                            ),
                        )
                        persist_result = await _await_persist_chatbi_v2_agent_log(
                            session_id=session_id,
                            query=query,
                            run_id=run_id,
                            prefer=prefer,
                            started_at=started_at,
                            agent_result=agent_result,
                        )
                        if not persist_result.get("ok"):
                            yield _sse(
                                "chain",
                                _event(
                                    typ="error",
                                    started_at=started_at,
                                    step_id="e_agent_db",
                                    payload={
                                        "stage": "agent_db",
                                        "message": (str(persist_result.get("error") or "persist_failed"))[:500],
                                        "persist": persist_result,
                                    },
                                ),
                            )
            except GeneratorExit:
                return
            except Exception:  # noqa: BLE001
                ok_local = False
                yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_unhandled", payload={"stage": "agent", "message": "SSE V2 运行异常"}))
            finally:
                done_body: dict[str, Any] = {
                    "ok": ok_local,
                    "mode": mode_local if isinstance(mode_local, str) else ("auto" if prefer == "auto" else str(prefer)),
                    "run_id": run_id,
                    "request_id": run_id,
                    "session_id": session_id,
                }
                if persist_result is not None:
                    done_body["persist"] = persist_result
                yield _sse("done", done_body)

        headers = {"Cache-Control": "no-cache"}
        return StreamingResponse(event_stream(), media_type="text/event-stream; charset=utf-8", headers=headers)

    _pg_sse_v1_abort, _pg_sse_v1_events = _unified_prompt_guard_short_circuit_events(
        query,
        ctx_log=ctx_log,
        run_id=run_id,
        session_id=session_id,
        started_at=started_at,
        route="unified_chat_sse",
    )
    if _pg_sse_v1_abort:
        _sse_short_mode = str(prefer) if prefer != "auto" else "auto"

        async def event_stream_prompt_guard_only() -> None:
            yield _sse(
                "chain",
                {
                    "type": "meta",
                    "ts": _now_ms(started_at),
                    "step_id": "m1",
                    "payload": {"run_id": run_id, "mode": _sse_short_mode, "session_id": session_id},
                },
            )
            for _gev in _pg_sse_v1_events:
                yield _sse("chain", _gev)
            yield _sse(
                "done",
                {
                    "ok": False,
                    "mode": _sse_short_mode,
                    "run_id": run_id,
                    "request_id": run_id,
                    "session_id": session_id,
                },
            )

        return StreamingResponse(
            event_stream_prompt_guard_only(),
            media_type="text/event-stream; charset=utf-8",
            headers={"Cache-Control": "no-cache"},
        )

    t_router0 = time.perf_counter()
    decision = decide_intent(query=query, prefer=prefer)
    t_router_decide_ms = int((time.perf_counter() - t_router0) * 1000)
    mode = decision.final_mode

    async def event_stream():
        ok = True
        try:
            # 首包：让前端先拿到 run_id/mode
            yield _sse("chain", {"type": "meta", "ts": _now_ms(started_at), "step_id": "m1", "payload": {"run_id": run_id, "mode": mode, "session_id": session_id}})
            yield _sse(
                "chain",
                _event(
                    typ="router.decision",
                    started_at=started_at,
                    step_id="r1",
                    payload={
                        "prefer": decision.prefer,
                        "candidate_mode": decision.candidate_mode,
                        "final_mode": decision.final_mode,
                        "rule_hits": decision.rule_hits,
                        "evidence": decision.evidence,
                        "fallback": decision.fallback,
                    },
                ),
            )
            yield _sse(
                "chain",
                _event(
                    typ="router.evidence",
                    started_at=started_at,
                    step_id="re1",
                    payload={
                        "candidate_mode": decision.candidate_mode,
                        "final_mode": decision.final_mode,
                        "fallback": decision.fallback,
                        "ddl": {
                            "hits": int((decision.evidence or {}).get("ddl_hits") or 0),
                            "top_score": (decision.evidence or {}).get("ddl_top_score"),
                            "topk": int(os.getenv("INTENT_DDL_EVIDENCE_TOPK", "3")),
                            "min_score": float(os.getenv("INTENT_DDL_EVIDENCE_MIN_SCORE", "0.05")),
                        },
                        "fts": {
                            "hits": int((decision.evidence or {}).get("fts_hits") or 0),
                            "top1_score": (decision.evidence or {}).get("fts_top1_score"),
                            "topk": int(os.getenv("INTENT_FTS_EVIDENCE_TOPK", "3")),
                        },
                    },
                ),
            )
            details_payload: dict[str, Any] | None = None
            log_rewritten_query: str = query
            log_retrieved_context: dict[str, Any] = {}
            log_response: str = ""
            text2sql_exec_trace: dict[str, Any] | None = None

            if debug_router or db_log_router or db_log_router_trace:
                ddl_topk = int(os.getenv("INTENT_DDL_EVIDENCE_TOPK", "3"))
                ddl_min_score = float(os.getenv("INTENT_DDL_EVIDENCE_MIN_SCORE", "0.05"))
                fts_topk = int(os.getenv("INTENT_FTS_EVIDENCE_TOPK", "3"))

                ddl_rows_any: list[dict[str, Any]] = []
                try:
                    t0 = time.perf_counter()
                    store = get_text2sql_store()
                    raw_any = store.search(query, top_k=ddl_topk)
                    ddl_rows_any = raw_any if isinstance(raw_any, list) else []
                    t_ddl_search_ms = int((time.perf_counter() - t0) * 1000)
                except Exception:
                    ddl_rows_any = []
                    t_ddl_search_ms = None

                ddl_candidates: list[dict[str, Any]] = []
                for r in ddl_rows_any[: max(1, ddl_topk)]:
                    if not isinstance(r, dict) or r.get("doc_type") != "ddl":
                        continue
                    title = r.get("title") if isinstance(r.get("title"), str) else ""
                    score = r.get("score")
                    try:
                        score_f = float(score) if score is not None else None
                    except Exception:  # noqa: BLE001
                        score_f = None
                    ddl_candidates.append({"title": _safe_text_for_event(title, max_len=120), "score": score_f})

                fts_candidates: list[dict[str, Any]] = []
                try:
                    t1 = time.perf_counter()
                    sb = supabase_client()
                    raw = sb.rpc("keyword_documents", {"query_text": (query or "").strip(), "match_count": fts_topk}).execute().data
                    rows = raw if isinstance(raw, list) else []
                    for rr in rows[: max(1, fts_topk)]:
                        if not isinstance(rr, dict):
                            continue
                        meta = rr.get("metadata") if isinstance(rr.get("metadata"), dict) else {}
                        path = meta.get("relativePath") if isinstance(meta.get("relativePath"), str) else None
                        score = rr.get("score")
                        try:
                            score_f = float(score) if score is not None else None
                        except Exception:  # noqa: BLE001
                            score_f = None
                        fts_candidates.append(
                            {
                                "id": rr.get("id"),
                                "path": _safe_text_for_event(path or "", max_len=180),
                                "score": score_f,
                            }
                        )
                except Exception:
                    fts_candidates = []
                    t_fts_search_ms = None
                else:
                    t_fts_search_ms = int((time.perf_counter() - t1) * 1000)

                details_payload = {
                    "candidate_mode": decision.candidate_mode,
                    "final_mode": decision.final_mode,
                    "fallback": decision.fallback,
                    "thresholds": {"ddl_topk": ddl_topk, "ddl_min_score": ddl_min_score, "fts_topk": fts_topk},
                    "ddl_candidates": ddl_candidates,
                    "fts_candidates": fts_candidates,
                }
                if debug_router:
                    yield _sse(
                        "chain",
                        _event(
                            typ="router.evidence.details",
                            started_at=started_at,
                            step_id="red1",
                            payload={
                                "candidate_mode": decision.candidate_mode,
                                "final_mode": decision.final_mode,
                                "fallback": decision.fallback,
                                "thresholds": {"ddl_topk": ddl_topk, "ddl_min_score": ddl_min_score, "fts_topk": fts_topk},
                                "ddl_candidates": ddl_candidates,
                                "fts_candidates": fts_candidates,
                            },
                        ),
                    )

                if db_log_router_trace:
                    router_trace_v1 = _shrink_router_trace_v1(
                        {
                            "ts_ms": int(time.time() * 1000),
                            "run_id": run_id,
                            "mode": mode,
                            "prefer": decision.prefer,
                            "debug_router": bool(body.get("debug_router") is True),
                            "timing_ms": {
                                "router_decide": int(t_router_decide_ms or 0),
                                "ddl_search": int(t_ddl_search_ms or 0),
                                "fts_search": int(t_fts_search_ms or 0),
                                "total": 0,
                            },
                            "ddl_search": {
                                "query_text": _safe_text_for_event(query, max_len=200),
                                "topk": int(ddl_topk),
                                "min_score": float(ddl_min_score),
                                "returned": int(len(ddl_candidates)),
                                "candidates": ddl_candidates[: max(1, ddl_topk)],
                            },
                            "fts_search": {
                                "query_text": _safe_text_for_event(query, max_len=200),
                                "match_count": int(fts_topk),
                                "returned": int(len(fts_candidates)),
                                "candidates": fts_candidates[: max(1, fts_topk)],
                            },
                            "decision": {
                                "candidate_mode": decision.candidate_mode,
                                "final_mode": decision.final_mode,
                                "fallback": decision.fallback,
                            },
                            "events_digest": [
                                {"type": "router.decision", "step_id": "r1", "ts": _now_ms(started_at)},
                                {"type": "router.evidence", "step_id": "re1", "ts": _now_ms(started_at)},
                            ],
                            "errors": [],
                            "v": "router_trace_v1",
                        }
                    )

            if mode.startswith("tool:"):
                ok = False
                yield _sse(
                    "chain",
                    _event(
                        typ="error",
                        started_at=started_at,
                        step_id="e_tool",
                        payload={"stage": "router", "message": f"未实现的工具路由：{mode}"},
                    ),
                )
                yield _sse(
                    "chain",
                    _event(
                        typ="latency",
                        started_at=started_at,
                        step_id="l1",
                        payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                    ),
                )
                return

            if mode == "no_data":
                oai = openai_siliconflow_client()
                chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")
                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.start",
                        started_at=started_at,
                        step_id="t_generate",
                        payload={"tool": "no_data.generate", "input": {"query": query}},
                    ),
                )
                t0 = time.perf_counter()
                ans = ""
                gen_err: str | None = None
                try:
                    res = oai.chat.completions.create(
                        model=chat_model,
                        messages=[
                            {"role": "system", "content": "你是一个中文助手。用户的问题不需要检索或查库，请直接回答。"},
                            {"role": "user", "content": query},
                        ],
                        temperature=0.7,
                        stream=False,
                    )
                    ans = (res.choices[0].message.content or "").strip()
                except Exception as exc:  # noqa: BLE001
                    gen_err = str(exc)
                    ans = "对话生成失败。"
                    ok = False
                t_gen_ms = int((time.perf_counter() - t0) * 1000)
                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.end",
                        started_at=started_at,
                        step_id="t_generate",
                        payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms},
                    ),
                )
                if gen_err:
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_generate", payload={"stage": "no_data.generate", "message": gen_err}))
                yield _sse("chain", _event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": ans}))
                yield _sse("chain", _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"generate": t_gen_ms}}))
                log_response = ans
                return

            if mode == "text2sql":
                # retrieve
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_retrieve", payload={"tool": "text2sql.retrieve", "input": {"query": query}}))
                t0 = time.perf_counter()
                retrieve_err: str | None = None
                retrieved: list[dict[str, Any]] = []
                try:
                    store = get_text2sql_store()
                    topk = int(os.getenv("TEXT2SQL_RETRIEVE_TOPK", "6"))
                    retrieved = store.search(query, top_k=topk)
                except Exception as exc:  # noqa: BLE001
                    retrieve_err = str(exc)
                t_retrieve_ms = int((time.perf_counter() - t0) * 1000)
                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.end",
                        started_at=started_at,
                        step_id="t_retrieve",
                        payload={"output": {"retrieved_count": len(retrieved), "retrieved": retrieved[:6]}, "error": retrieve_err, "latency_ms": t_retrieve_ms},
                    ),
                )
                if retrieve_err:
                    ok = False
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_retrieve", payload={"stage": "text2sql.retrieve", "message": retrieve_err}))
                    return

                pols = await asyncio.to_thread(load_chatbi_table_policies_sync)
                retrieved = filter_text2sql_retrieved(retrieved, principal=principal, policies=pols)

                oai = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY", "").strip(), base_url=siliconflow_base())
                chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")

                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.start",
                        started_at=started_at,
                        step_id="t_schema_prefetch",
                        payload={"tool": "text2sql.schema_prefetch", "input": {"query": query}},
                    ),
                )
                t_pf0 = time.perf_counter()
                pf_block, pf_err, pf_meta = await asyncio.to_thread(
                    run_text2sql_schema_prefetch_sync,
                    user_query=query,
                    retrieved=retrieved,
                    principal=principal,
                    policies=pols,
                )
                t_pf_ms = int((time.perf_counter() - t_pf0) * 1000)
                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.end",
                        started_at=started_at,
                        step_id="t_schema_prefetch",
                        payload={"output": pf_meta, "error": pf_err, "latency_ms": t_pf_ms},
                    ),
                )
                if pf_err:
                    ok = False
                    yield _sse(
                        "chain",
                        _event(
                            typ="error",
                            started_at=started_at,
                            step_id="e_schema_prefetch",
                            payload={"stage": "text2sql.schema_prefetch", "message": pf_err},
                        ),
                    )
                    return

                # generate sql
                sql_prompt = build_sql_prompt(
                    query,
                    retrieved,
                    value_hints_block=build_value_hints_block_for_text2sql(retrieved, history=None),
                    prefetched_schema_block=pf_block,
                    chatbi_access_level=principal.access_level,
                    chatbi_subject_user_id=principal.subject_user_id,
                )
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_generate_sql", payload={"tool": "text2sql.generate_sql", "input": {"query": query}}))
                t1 = time.perf_counter()
                sql_raw = ""
                sql = ""
                sql_kind = "select"
                gen_err: str | None = None
                try:
                    sql_raw = llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
                    sql, sql_kind = apply_chatbi_sql_gate(
                        sql_raw,
                        principal=principal,
                        policies=pols,
                        run_id=ctx_log.get("run_id"),
                        request_id=ctx_log.get("request_id"),
                    )
                except ChatBiSqlGateDenied as exc:
                    gen_err = exc.message_zh
                except Exception as exc:  # noqa: BLE001
                    gen_err = str(exc)
                t_gen_ms = int((time.perf_counter() - t1) * 1000)
                yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_generate_sql", payload={"output": {"sql": sql or sql_raw}, "error": gen_err, "latency_ms": t_gen_ms}))
                if gen_err or not (sql or sql_raw):
                    ok = False
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_generate_sql", payload={"stage": "text2sql.generate_sql", "message": gen_err or "empty sql"}))
                    return

                # execute sql
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_execute_sql", payload={"tool": "text2sql.execute_sql", "input": {"sql": sql}}))
                t2 = time.perf_counter()
                columns: list[str] = []
                rows: list[dict[str, Any]] = []
                exec_err: str | None = None
                try:
                    if sql_kind == "select":
                        columns, rows = execute_select_sql(sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200")))
                    else:
                        rowcount = execute_mutating_sql(sql)
                        columns = ["affected_rows"]
                        rows = [{"affected_rows": rowcount}]
                except Exception as exc:  # noqa: BLE001
                    exec_err = str(exc)
                t_exec_ms = int((time.perf_counter() - t2) * 1000)
                text2sql_exec_trace = _build_text2sql_exec_trace(sql=sql, sql_raw=sql_raw, columns=columns, rows=rows, error=exec_err, latency_ms=t_exec_ms)
                yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_execute_sql", payload={"output": {"columns": columns, "rows_len": len(rows)}, "error": exec_err, "latency_ms": t_exec_ms}))
                if exec_err:
                    ok = False
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_execute_sql", payload={"stage": "text2sql.execute_sql", "message": exec_err}))
                yield _sse("chain", _event(typ="sql.result", started_at=started_at, step_id="q1", payload={"sql": sql, "columns": columns, "rows": rows[:20], "truncated": len(rows) > 20}))

                # summarize
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_summarize", payload={"tool": "text2sql.summarize", "input": {"query": query}}))
                t3 = time.perf_counter()
                answer = ""
                sum_err: str | None = None
                try:
                    if rows:
                        sum_prompt = build_summary_prompt(query, sql, columns, rows)
                        answer = llm_summarize(oai=oai, model=chat_model, prompt=sum_prompt)
                    else:
                        answer = "未查到数据。"
                except Exception as exc:  # noqa: BLE001
                    sum_err = str(exc)
                    answer = "未查到数据。" if not rows else f"查询返回 {len(rows)} 行结果。"
                    ok = False
                t_sum_ms = int((time.perf_counter() - t3) * 1000)
                yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_summarize", payload={"output": {"answer": answer}, "error": sum_err, "latency_ms": t_sum_ms}))
                yield _sse("chain", _event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": answer}))
                yield _sse("chain", _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"retrieve": t_retrieve_ms, "generate_sql": t_gen_ms, "execute_sql": t_exec_ms, "summarize": t_sum_ms}}))
                log_response = answer
                return

            # ---- RAG branch (non-streaming answer v1) ----
            oai = openai_siliconflow_client()
            chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")

            # rewrite
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_rewrite", payload={"tool": "rag.rewrite", "input": {"query": query}}))
            t_rw0 = time.perf_counter()
            rewritten = query
            rw_err: str | None = None
            try:
                rewritten = await rewrite_query_with_history(oai=oai, query=query, history=[], chat_model=chat_model)
            except Exception as exc:  # noqa: BLE001
                rw_err = str(exc)
                rewritten = query
                ok = False
            t_rw_ms = int((time.perf_counter() - t_rw0) * 1000)
            yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_rewrite", payload={"output": {"rewritten_query": rewritten}, "error": rw_err, "latency_ms": t_rw_ms}))

            # embed
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_embed", payload={"tool": "rag.embed", "input": {"query": rewritten}}))
            t_emb0 = time.perf_counter()
            vec: list[float] | None = None
            emb_err: str | None = None
            try:
                emb_res = oai.embeddings.create(**embedding_kwargs_for_inputs([rewritten]))
                vec = list(emb_res.data[0].embedding)
            except Exception as exc:  # noqa: BLE001
                emb_err = str(exc)
                vec = None
                ok = False
            t_emb_ms = int((time.perf_counter() - t_emb0) * 1000)
            yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_embed", payload={"output": {"vec_available": vec is not None}, "error": emb_err, "latency_ms": t_emb_ms}))

            # retrieve
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_retrieve", payload={"tool": "rag.retrieve", "input": {"query": rewritten}}))
            t_ret0 = time.perf_counter()
            vector_hits: list[dict[str, Any]] = []
            structured_hits: list[dict[str, Any]] = []
            keyword_hits_raw: list[dict[str, Any]] = []
            keyword_hits_rewrite: list[dict[str, Any]] = []
            hits: list[dict[str, Any]] = []
            ret_err: str | None = None
            retry_count = 0
            try:
                sb = supabase_client()
                alignment = ensure_embedding_alignment(sb)
                if not alignment.ok:
                    ret_err = alignment.message
                else:
                    structured_hits = structured_recall_by_date(
                        sb,
                        query=query,
                        rewritten=rewritten,
                        limit_rows=6,
                        principal_kind=principal.principal_kind,
                        access_level=principal.access_level,
                        subject_user_id=principal.subject_user_id,
                    ).hits
                    match_threshold = parse_match_threshold()
                    match_count = int(os.getenv("RAG_MATCH_COUNT", "10"))
                    if vec is not None:
                        vector_hits, rc_vec, err_vec = rpc_execute_with_retry(
                            sb,
                            "match_documents",
                            {"query_embedding": vec, "match_count": match_count, "match_threshold": match_threshold},
                            retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
                        )
                        retry_count += rc_vec
                        if err_vec:
                            ret_err = err_vec

                    kw_qt_raw, kw_meta_raw = keyword_query_text_with_i18n_meta(query)
                    kw_qt_rw, kw_meta_rw = keyword_query_text_with_i18n_meta(rewritten)
                    yield _sse(
                        "chain",
                        _event(
                            typ="rag.query_expand",
                            started_at=started_at,
                            step_id="q_expand",
                            payload={
                                "raw": _build_query_expand_event_payload(kw_meta_raw, max_raw=160, max_expanded=220),
                                "rewrite": _build_query_expand_event_payload(kw_meta_rw, max_raw=160, max_expanded=220),
                            },
                        ),
                    )

                    keyword_hits_raw, rc_raw, err_raw = rpc_execute_with_retry(
                        sb,
                        "keyword_documents",
                        {"query_text": kw_qt_raw, "match_count": 12},
                        retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
                    )
                    retry_count += rc_raw
                    if err_raw:
                        ret_err = err_raw

                    keyword_hits_rewrite, rc_rw, err_rw = rpc_execute_with_retry(
                        sb,
                        "keyword_documents",
                        {"query_text": kw_qt_rw, "match_count": 12},
                        retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
                    )
                    retry_count += rc_rw
                    if err_rw:
                        ret_err = err_rw

                    merged_keyword = fuse_hits_rrf(keyword_hits_raw, keyword_hits_rewrite, max_total=22)
                    merged_kw2 = fuse_hits_rrf(structured_hits, merged_keyword, max_total=22)
                    hits = fuse_hits_rrf(vector_hits, merged_kw2, max_total=22)
            except Exception as exc:  # noqa: BLE001
                ret_err = str(exc)
                hits = []
                ok = False
            t_ret_ms = int((time.perf_counter() - t_ret0) * 1000)
            yield _sse(
                "chain",
                _event(
                    typ="tool.call.end",
                    started_at=started_at,
                    step_id="t_retrieve",
                    payload={
                        "output": {
                            "vector_hits": len(vector_hits),
                            "structured_hits": len(structured_hits),
                            "keyword_hits_raw": len(keyword_hits_raw),
                            "keyword_hits_rewrite": len(keyword_hits_rewrite),
                            "hits": len(hits),
                            "retry_count": retry_count,
                            "embedding_error": emb_err,
                        },
                        "error": ret_err,
                        "latency_ms": t_ret_ms,
                    },
                ),
            )

            # sources
            yield _sse("chain", _event(typ="rag.sources", started_at=started_at, step_id="s_sources", payload=_build_rag_sources_event(hits, top_k=10)))

            # generate
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_generate", payload={"tool": "rag.generate", "input": {"query": query}}))
            t_gen0 = time.perf_counter()
            ans = ""
            gen_err: str | None = None
            try:
                ans = _rag_generate_answer(oai=oai, chat_model=chat_model, query=query, hits=hits)
                if not ans:
                    ans = "我暂时无法根据现有资料给出确定回答。"
            except Exception as exc:  # noqa: BLE001
                gen_err = str(exc)
                ans = "对话生成失败。"
                ok = False
            t_gen_ms = int((time.perf_counter() - t_gen0) * 1000)
            yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_generate", payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms}))
            if gen_err:
                yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_generate", payload={"stage": "rag.generate", "message": gen_err}))
            yield _sse("chain", _event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": ans}))
            yield _sse("chain", _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"rewrite": t_rw_ms, "embed": t_emb_ms, "retrieve": t_ret_ms, "generate": t_gen_ms}}))
            log_rewritten_query = rewritten
            log_response = ans
        except GeneratorExit:
            return
        except Exception as exc:  # noqa: BLE001
            ok = False
            yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_unhandled", payload={"stage": "unhandled", "message": str(exc)}))
        finally:
            if (db_log_router or db_log_router_trace) and session_id:
                if router_trace_v1:
                    router_trace_v1 = dict(router_trace_v1)
                    if mode == "text2sql" and text2sql_exec_trace:
                        router_trace_v1["text2sql_exec"] = text2sql_exec_trace
                    timing = router_trace_v1.get("timing_ms") if isinstance(router_trace_v1.get("timing_ms"), dict) else {}
                    timing2 = dict(timing)
                    timing2["total"] = _now_ms(started_at)
                    router_trace_v1["timing_ms"] = timing2
                    router_trace_v1 = _shrink_router_trace_v1(router_trace_v1)
                _async_save_rag_log(
                    {
                        "session_id": session_id,
                        "query": query,
                        "rewritten_query": log_rewritten_query,
                        "retrieved_context": log_retrieved_context,
                        "response": log_response,
                        "metadata": {
                            "mode": mode,
                            "v": "router_evidence_observability_v1",
                            "router_debug": {
                                "router_evidence_details": details_payload,
                                **({"router_trace_v1": router_trace_v1} if router_trace_v1 else {}),
                            },
                        },
                    }
                )
            # done must be the last message if client still connected
            try:
                # request_id：端到端链路标识（当前与 run_id 等价，便于逐步在前后端统一命名）
                yield _sse(
                    "done",
                    {
                        "ok": ok,
                        "mode": mode,
                        "run_id": run_id,
                        "request_id": run_id,
                        "session_id": session_id,
                    },
                )
            except Exception:
                return

    headers = {"Cache-Control": "no-cache"}
    return StreamingResponse(event_stream(), media_type="text/event-stream; charset=utf-8", headers=headers)
