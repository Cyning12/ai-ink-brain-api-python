from __future__ import annotations

import asyncio
import os
import time
import uuid
from typing import Any, Literal

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

from ..agent import ChatBIAgent
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
from ..intent_agent import IntentDecision, build_intent_path_obs
from ..intent_router import decide_intent
from ..query_rewrite import rewrite_query_with_history
from ..rag_embedding_guard import (
    ensure_embedding_alignment,
)
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

# Import shared helpers from unified_chat to avoid duplication and keep SSE untouched.
from ..unified_chat import (
    _agent_intent_obs_payload,
    _async_save_rag_log,
    _await_persist_chatbi_v2_agent_log,
    _build_query_expand_event_payload,
    _build_rag_sources_event,
    _build_text2sql_exec_trace,
    _chatbi_log_ctx,
    _clarify_short_circuit_events,
    _compact_errors,
    _compact_event_digest,
    _debug_llm_prompts_enabled,
    _debug_router_evidence_enabled,
    _event,
    _now_ms,
    _parse_prefer,
    _rag_generate_answer,
    _router_evidence_db_log_enabled,
    _router_trace_db_log_enabled,
    _safe_text_for_event,
    _shrink_router_trace_v1,
    _unified_prompt_guard_short_circuit_events,
)

PreferMode = Literal["auto", "rag", "text2sql", "no_data"]


async def handle_unified_chat(
    request: Request,
    *,
    principal: ChatBiPrincipal,
) -> JSONResponse:
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
    events: list[dict[str, Any]] = []
    debug_router = _debug_router_evidence_enabled() or bool(body.get("debug_router") is True)
    debug_llm_prompts = _debug_llm_prompts_enabled(body)
    db_log_router = _router_evidence_db_log_enabled() or bool(body.get("debug_router") is True)
    db_log_router_trace = _router_trace_db_log_enabled() or bool(body.get("debug_router") is True)
    router_trace_v1: dict[str, Any] | None = None
    t_router_decide_ms: int | None = None
    t_ddl_search_ms: int | None = None
    t_fts_search_ms: int | None = None

    def finish(*, ok: bool, mode: str, persist: dict[str, Any] | None = None) -> JSONResponse:
        body: dict[str, Any] = {"ok": ok, "run_id": run_id, "session_id": session_id, "mode": mode, "events": events}
        if persist is not None:
            body["persist"] = persist
        return JSONResponse(content=body)

    # P1-2：Prompt guard 扫描用户 query，早于任何上游 LLM（Intent / Text2SQL / no_data / Agent）。
    # P1-1 SQL AST gate 仍在 text2sql SQL 生成之后；同请求内顺序：本守卫 → … → SQL gate。
    _pg_abort, _pg_events = _unified_prompt_guard_short_circuit_events(
        query, ctx_log=ctx_log, run_id=run_id, session_id=session_id, started_at=started_at, route="unified_chat"
    )
    if _pg_abort:
        events.extend(_pg_events)
        return finish(ok=False, mode=str(prefer))

    # CHATBI v2（Agent）主路径：开关开启时，输出 agent.* 事件
    use_agent = (os.getenv("CHATBI_USE_AGENT", "false") or "").strip().lower() in ("1", "true", "yes", "on")
    if use_agent:
        # prefer=tool:* 仍按 v1 路由返回 error（保持行为一致）
        if str(prefer).startswith("tool:"):
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_agent",
                    payload={"stage": "agent", "message": f"未实现的工具路由：{prefer}"},
                )
            )
            events.append(
                _event(
                    typ="latency",
                    started_at=started_at,
                    step_id="l1",
                    payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                )
            )
            return finish(ok=False, mode=str(prefer))

        tool_registry = get_tool_registry()
        agent = ChatBIAgent(tools=tool_registry.list_tools(), memory=get_memory_store())
        agent_result = await agent.run(
            query=query,
            session_id=session_id,
            prefer=prefer,
            sse_started_at=started_at,
            run_id=run_id,
            debug_llm_prompts=debug_llm_prompts,
            plan_execution_token=plan_execution_token,
        )

        mode = agent_result.final.mode
        max_steps = max(1, int(os.getenv("AGENT_MAX_STEPS", "5")))

        # router.decision：Agent 初始决策（V1 payload 结构保持一致）
        intent_decision = agent_result.intent_decision
        step1 = agent_result.steps[0] if agent_result.steps else None
        step1_mode = step1.mode if step1 else mode
        candidate_mode = intent_decision.mode if intent_decision else step1_mode
        final_mode = step1_mode

        events.append(
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
            )
        )

        events.extend(
            _clarify_short_circuit_events(
                agent_result=agent_result,
                started_at=started_at,
                max_steps=max_steps,
                debug_router=debug_router,
                debug_llm_prompts=debug_llm_prompts,
            )
        )

        # 事件流：agent.step.start → (step1) agent.intent → agent.think → tool.call.start/end → agent.step.end
        for step in agent_result.steps:
            step_id = f"a{step.step_number}"
            events.append(
                _event(
                    typ="agent.step.start",
                    started_at=started_at,
                    step_id=step_id,
                    payload={"step_number": step.step_number, "max_steps": max_steps},
                )
            )

            if step.step_number == 1 and intent_decision is not None:
                events.append(
                    _event(
                        typ="agent.intent",
                        started_at=started_at,
                        step_id="intent_1",
                        payload=_agent_intent_obs_payload(intent_decision, debug_router=debug_router),
                    )
                )
                if debug_llm_prompts and isinstance(intent_decision.raw_response, dict):
                    _ilp = intent_decision.raw_response.get("llm_prompts")
                    if isinstance(_ilp, list) and _ilp:
                        events.append(
                            _event(
                                typ="agent.debug.llm_prompts",
                                started_at=started_at,
                                step_id="intent_llm_json",
                                payload={"scope": "intent", "items": _ilp},
                            )
                        )

            events.append(
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
                )
            )

            td = step.tool_result.data if isinstance(step.tool_result.data, dict) else {}
            if step.tool_used == "rag_search":
                _rw = td.get("rewritten") if isinstance(td.get("rewritten"), str) else ""
                _rw_ms = int(td.get("rewrite_latency_ms") or 0)
                events.append(
                    _event(
                        typ="tool.call.start",
                        started_at=started_at,
                        step_id=f"t_step{step.step_number}_rewrite",
                        payload={"tool": "rag.rewrite", "input": {"query": query}},
                    )
                )
                events.append(
                    _event(
                        typ="tool.call.end",
                        started_at=started_at,
                        step_id=f"t_step{step.step_number}_rewrite",
                        payload={
                            "output": {"rewritten_query": _rw or query},
                            "error": None,
                            "latency_ms": _rw_ms,
                        },
                    )
                )
                events.append(
                    _event(
                        typ="tool.call.start",
                        started_at=started_at,
                        step_id=f"t_step{step.step_number}",
                        payload={"tool": "rag_search", "input": {"query": query, "rewritten_query": _rw or query}},
                    )
                )
            else:
                events.append(
                    _event(
                        typ="tool.call.start",
                        started_at=started_at,
                        step_id=f"t_step{step.step_number}",
                        payload={"tool": step.tool_used, "input": {"query": query}},
                    )
                )

            err = step.tool_result.error
            out_answer: str | None = None
            if step.tool_result.data and isinstance(step.tool_result.data.get("answer"), str):
                out_answer = step.tool_result.data.get("answer")

            _out_payload_json: dict[str, Any] = {}
            if out_answer is not None:
                _out_payload_json["answer"] = out_answer
            if step.tool_used == "rag_search" and isinstance(td.get("rewritten"), str):
                _out_payload_json["rewritten_query"] = td["rewritten"]

            events.append(
                _event(
                    typ="tool.call.end",
                    started_at=started_at,
                    step_id=f"t_step{step.step_number}",
                    payload={
                        "output": _out_payload_json,
                        "error": err,
                        "latency_ms": step.tool_result.latency_ms,
                    },
                )
            )
            if debug_llm_prompts and isinstance(td.get("llm_prompts"), list) and td.get("llm_prompts"):
                events.append(
                    _event(
                        typ="agent.debug.llm_prompts",
                        started_at=started_at,
                        step_id=f"tool_llm_json_{step.step_number}",
                        payload={
                            "scope": "tool",
                            "tool": step.tool_used,
                            "step_number": step.step_number,
                            "items": td["llm_prompts"],
                        },
                    )
                )

            # 可视化来源：按工具类型补齐 v1 事件
            if step.tool_used == "text2sql_query" and step.tool_result.success and step.tool_result.data:
                data = step.tool_result.data
                columns = data.get("columns") if isinstance(data.get("columns"), list) else []
                rows_any = data.get("rows") if isinstance(data.get("rows"), list) else []
                rows: list[dict[str, Any]] = [r for r in rows_any if isinstance(r, dict)]
                truncated = len(rows) > 20
                events.append(
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
                    )
                )
            elif step.tool_used == "rag_search" and step.tool_result.success and step.tool_result.data:
                data = step.tool_result.data
                hits_any = data.get("hits")
                hits: list[dict[str, Any]] = hits_any if isinstance(hits_any, list) else []
                rag_sources_payload = _build_rag_sources_event(hits, top_k=10)
                events.append(
                    _event(
                        typ="rag.sources",
                        started_at=started_at,
                        step_id=f"s_step{step.step_number}",
                        payload=rag_sources_payload,
                    )
                )

            events.append(
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
                )
            )

        events.append(
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
            )
        )

        events.append(
            _event(
                typ="assistant.message",
                started_at=started_at,
                step_id="s_answer",
                payload={"role": "assistant", "content": agent_result.final.answer},
            )
        )

        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
            )
        )

        persist_json = await _await_persist_chatbi_v2_agent_log(
            session_id=session_id,
            query=query,
            run_id=run_id,
            prefer=prefer,
            started_at=started_at,
            agent_result=agent_result,
        )
        if not persist_json.get("ok"):
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_agent_db",
                    payload={
                        "stage": "agent_db",
                        "message": (str(persist_json.get("error") or "persist_failed"))[:500],
                        "persist": persist_json,
                    },
                )
            )

        return finish(ok=True, mode=mode, persist=persist_json)

    # mode decide (v1 router)
    t_router0 = time.perf_counter()
    decision = decide_intent(query=query, prefer=prefer)
    t_router_decide_ms = int((time.perf_counter() - t_router0) * 1000)
    mode = decision.final_mode

    events.append(
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
        )
    )
    events.append(
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
        )
    )
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
            events.append(
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
                )
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
                    "events_digest": _compact_event_digest(events, max_events=64),
                    "errors": _compact_errors(events, max_items=16),
                    "v": "router_trace_v1",
                }
            )

    if mode.startswith("tool:"):
        events.append(
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_tool",
                payload={"stage": "router", "message": f"未实现的工具路由：{mode}"},
            )
        )
        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
            )
        )
        return finish(ok=False, mode=mode)

    if mode == "no_data":
        oai = openai_siliconflow_client()
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_generate",
                payload={"tool": "no_data.generate", "input": {"query": query}},
            )
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
        t_gen_ms = int((time.perf_counter() - t0) * 1000)
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_generate",
                payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms},
            )
        )
        if gen_err:
            events.append(_event(typ="error", started_at=started_at, step_id="e_generate", payload={"stage": "no_data.generate", "message": gen_err}))
        events.append(_event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": ans}))
        events.append(_event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"generate": t_gen_ms}}))
        if (db_log_router or db_log_router_trace) and session_id:
            if router_trace_v1:
                router_trace_v1 = dict(router_trace_v1)
                timing = router_trace_v1.get("timing_ms") if isinstance(router_trace_v1.get("timing_ms"), dict) else {}
                timing2 = dict(timing)
                timing2["total"] = _now_ms(started_at)
                router_trace_v1["timing_ms"] = timing2
            _async_save_rag_log(
                {
                    "session_id": session_id,
                    "query": query,
                    "rewritten_query": query,
                    "retrieved_context": {},
                    "response": ans,
                    "metadata": {
                        "mode": mode,
                        "v": "router_evidence_observability_v1",
                        "router_debug": {
                            "router_evidence_details": locals().get("details_payload"),
                            **({"router_trace_v1": router_trace_v1} if router_trace_v1 else {}),
                        },
                    },
                }
            )
        return finish(ok=gen_err is None, mode=mode)

    if mode == "text2sql":
        # ---- Text2SQL branch: reuse chain-like events ----
        # retrieve
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_retrieve",
                payload={"tool": "text2sql.retrieve", "input": {"query": query}},
            )
        )
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
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_retrieve",
                payload={
                    "output": {"retrieved_count": len(retrieved), "retrieved": retrieved[:6]},
                    "error": retrieve_err,
                    "latency_ms": t_retrieve_ms,
                },
            )
        )
        if retrieve_err:
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_retrieve",
                    payload={"stage": "text2sql.retrieve", "message": retrieve_err},
                )
            )
            events.append(
                _event(
                    typ="latency",
                    started_at=started_at,
                    step_id="l1",
                    payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                )
            )
            return finish(ok=False, mode=mode)

        pols = await asyncio.to_thread(load_chatbi_table_policies_sync)
        retrieved = filter_text2sql_retrieved(retrieved, principal=principal, policies=pols)

        oai = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY", "").strip(), base_url=siliconflow_base())
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")

        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_schema_prefetch",
                payload={"tool": "text2sql.schema_prefetch", "input": {"query": query}},
            )
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
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_schema_prefetch",
                payload={
                    "output": pf_meta,
                    "error": pf_err,
                    "latency_ms": t_pf_ms,
                    "tool": "text2sql.schema_prefetch",
                },
            )
        )
        if pf_err:
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_schema_prefetch",
                    payload={"stage": "text2sql.schema_prefetch", "message": pf_err},
                )
            )
            events.append(
                _event(
                    typ="latency",
                    started_at=started_at,
                    step_id="l1",
                    payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                )
            )
            return finish(ok=False, mode=mode)

        # generate sql
        sql_prompt = build_sql_prompt(
            query,
            retrieved,
            value_hints_block=build_value_hints_block_for_text2sql(retrieved, history=None),
            prefetched_schema_block=pf_block,
            chatbi_access_level=principal.access_level,
            chatbi_subject_user_id=principal.subject_user_id,
        )
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_generate_sql",
                payload={"tool": "text2sql.generate_sql", "input": {"query": query}},
            )
        )
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
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_generate_sql",
                payload={"output": {"sql": sql or sql_raw}, "error": gen_err, "latency_ms": t_gen_ms},
            )
        )
        if gen_err or not (sql or sql_raw):
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_generate_sql",
                    payload={"stage": "text2sql.generate_sql", "message": gen_err or "empty sql"},
                )
            )
            events.append(
                _event(
                    typ="latency",
                    started_at=started_at,
                    step_id="l1",
                    payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                )
            )
            return finish(ok=False, mode=mode)

        # execute sql
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_execute_sql",
                payload={"tool": "text2sql.execute_sql", "input": {"sql": sql}},
            )
        )
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
        text2sql_exec_trace: dict[str, Any] | None = _build_text2sql_exec_trace(sql=sql, sql_raw=sql_raw, columns=columns, rows=rows, error=exec_err, latency_ms=t_exec_ms)
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_execute_sql",
                payload={"output": {"columns": columns, "rows_len": len(rows)}, "error": exec_err, "latency_ms": t_exec_ms},
            )
        )
        if exec_err:
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_execute_sql",
                    payload={"stage": "text2sql.execute_sql", "message": exec_err},
                )
            )
        events.append(
            _event(
                typ="sql.result",
                started_at=started_at,
                step_id="q1",
                payload={"sql": sql, "columns": columns, "rows": rows[:20], "truncated": len(rows) > 20},
            )
        )

        # summarize
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_summarize",
                payload={"tool": "text2sql.summarize", "input": {"query": query}},
            )
        )
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
        t_sum_ms = int((time.perf_counter() - t3) * 1000)
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_summarize",
                payload={"output": {"answer": answer}, "error": sum_err, "latency_ms": t_sum_ms},
            )
        )
        events.append(
            _event(
                typ="assistant.message",
                started_at=started_at,
                step_id="s_answer",
                payload={"role": "assistant", "content": answer},
            )
        )
        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={
                    "total_ms": _now_ms(started_at),
                    "stages_ms": {"retrieve": t_retrieve_ms, "generate_sql": t_gen_ms, "execute_sql": t_exec_ms, "summarize": t_sum_ms},
                },
            )
        )
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
                    "rewritten_query": query,
                    "retrieved_context": {},
                    "response": answer,
                    "metadata": {
                        "mode": mode,
                        "v": "router_evidence_observability_v1",
                        "router_debug": {
                            "router_evidence_details": locals().get("details_payload"),
                            **({"router_trace_v1": router_trace_v1} if router_trace_v1 else {}),
                        },
                    },
                }
            )
        return finish(ok=exec_err is None and gen_err is None, mode=mode)

    # ---- RAG branch (non-streaming v1) ----
    oai = openai_siliconflow_client()
    chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V4-Pro")

    # rewrite
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_rewrite",
            payload={"tool": "rag.rewrite", "input": {"query": query}},
        )
    )
    t_rw0 = time.perf_counter()
    rewritten = query
    rw_err: str | None = None
    try:
        rewritten = await rewrite_query_with_history(oai=oai, query=query, history=[], chat_model=chat_model)
    except Exception as exc:  # noqa: BLE001
        rw_err = str(exc)
        rewritten = query
    t_rw_ms = int((time.perf_counter() - t_rw0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_rewrite",
            payload={"output": {"rewritten_query": rewritten}, "error": rw_err, "latency_ms": t_rw_ms},
        )
    )

    # embed
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_embed",
            payload={"tool": "rag.embed", "input": {"query": rewritten}},
        )
    )
    t_emb0 = time.perf_counter()
    vec: list[float] | None = None
    emb_err: str | None = None
    try:
        emb_res = oai.embeddings.create(**embedding_kwargs_for_inputs([rewritten]))
        vec = list(emb_res.data[0].embedding)
    except Exception as exc:  # noqa: BLE001
        emb_err = str(exc)
        vec = None
    t_emb_ms = int((time.perf_counter() - t_emb0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_embed",
            payload={"output": {"vec_available": vec is not None}, "error": emb_err, "latency_ms": t_emb_ms},
        )
    )

    # retrieve
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_retrieve",
            payload={"tool": "rag.retrieve", "input": {"query": rewritten}},
        )
    )
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
            # structured recall（日期类确定性召回）
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
            events.append(
                _event(
                    typ="rag.query_expand",
                    started_at=started_at,
                    step_id="q_expand",
                    payload={
                        "raw": _build_query_expand_event_payload(kw_meta_raw, max_raw=160, max_expanded=220),
                        "rewrite": _build_query_expand_event_payload(kw_meta_rw, max_raw=160, max_expanded=220),
                    },
                )
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
    t_ret_ms = int((time.perf_counter() - t_ret0) * 1000)
    events.append(
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
        )
    )

    sources_payload = _build_rag_sources_event(hits, top_k=10)
    events.append(
        _event(
            typ="rag.sources",
            started_at=started_at,
            step_id="s_sources",
            payload=sources_payload,
        )
    )

    # generate
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_generate",
            payload={"tool": "rag.generate", "input": {"query": query}},
        )
    )
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
    t_gen_ms = int((time.perf_counter() - t_gen0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_generate",
            payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms},
        )
    )
    if gen_err:
        events.append(
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_generate",
                payload={"stage": "rag.generate", "message": gen_err},
            )
        )

    events.append(
        _event(
            typ="assistant.message",
            started_at=started_at,
            step_id="s_answer",
            payload={"role": "assistant", "content": ans},
        )
    )
    events.append(
        _event(
            typ="latency",
            started_at=started_at,
            step_id="l1",
            payload={"total_ms": _now_ms(started_at), "stages_ms": {"rewrite": t_rw_ms, "embed": t_emb_ms, "retrieve": t_ret_ms, "generate": t_gen_ms}},
        )
    )
    if (db_log_router or db_log_router_trace) and session_id:
        if router_trace_v1:
            router_trace_v1 = dict(router_trace_v1)
            timing = router_trace_v1.get("timing_ms") if isinstance(router_trace_v1.get("timing_ms"), dict) else {}
            timing2 = dict(timing)
            timing2["total"] = _now_ms(started_at)
            router_trace_v1["timing_ms"] = timing2
        _async_save_rag_log(
            {
                "session_id": session_id,
                "query": query,
                "rewritten_query": rewritten,
                "retrieved_context": {},
                "response": ans,
                "metadata": {
                    "mode": mode,
                    "v": "router_evidence_observability_v1",
                    "router_debug": {
                        "router_evidence_details": locals().get("details_payload"),
                        **({"router_trace_v1": router_trace_v1} if router_trace_v1 else {}),
                    },
                },
            }
        )
    return finish(ok=gen_err is None, mode=mode)


def _router_agent_evidence(intent_decision: IntentDecision | None) -> dict[str, Any]:
    """router.decision.evidence：Intent reasoning + 路径可观测（U1.5 重试 / Step2 仲裁）。"""
    out: dict[str, Any] = {
        "agent_reasoning": intent_decision.reasoning_full if intent_decision else "",
    }
    raw = intent_decision.raw_response if intent_decision is not None else None
    out.update(build_intent_path_obs(raw if isinstance(raw, dict) else None))
    return out
