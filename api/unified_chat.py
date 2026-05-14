from __future__ import annotations

import asyncio
import math
import os
import re
import time
import uuid
import json
from typing import Any, Literal

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from openai import OpenAI

from .chatbi_principal import ChatBiPrincipal
from .chatbi_policies import load_chatbi_table_policies_sync
from .chatbi_request_ctx import set_chatbi_log_ctx, set_chatbi_principal
from .chatbi_json_log import log_chatbi_record
from .chatbi_prompt_guard import chatbi_prompt_guard_mode, scan as prompt_guard_scan
from .chatbi_sql_gate import ChatBiSqlGateDenied, apply_chatbi_sql_gate, filter_text2sql_retrieved
from .hybrid_fusion import RRF_K, fuse_hits_rrf
from .query_rewrite import rewrite_query_with_history
from .rag_recall_tools import keyword_query_text_with_i18n_meta, rpc_execute_with_retry, structured_recall_by_date
from .rag_env import (
    embedding_kwargs_for_inputs,
    openai_siliconflow_client,
    siliconflow_base,
    supabase_client,
    supabase_table_insert_with_retry,
)
from .text2sql_core import (
    build_sql_prompt,
    build_summary_prompt,
    execute_mutating_sql,
    execute_select_sql,
    llm_generate_sql,
    llm_summarize,
)
from .text2sql_value_hints import build_value_hints_block_for_text2sql
from .text2sql_grounding import build_text2sql_grounding_dict
from .text2sql_schema_prefetch import run_text2sql_schema_prefetch_sync
from .text2sql_store import get_text2sql_store
from .intent_agent import IntentDecision
from .intent_router import decide_intent
from .rag_shared import parse_match_threshold, strip_doc_context_prefix
from .agent import AgentRunView, ChatBIAgent
from .agent_memory import get_memory_store
from .tools import get_tool_registry


PreferMode = Literal["auto", "rag", "text2sql", "no_data"]


def _chatbi_log_ctx(request: Request) -> dict[str, Any]:
    return {"request_id": (request.headers.get("x-request-id") or "").strip() or None}
def _now_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _event(*, typ: str, started_at: float, step_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"type": typ, "ts": _now_ms(started_at), "step_id": step_id, "payload": payload}


def _agent_intent_obs_payload(intent_decision: IntentDecision, *, debug_router: bool) -> dict[str, Any]:
    """agent.intent 的 payload：契约要求键齐全；cache 可观测字段仅在 debug_router 时取自 raw_response。"""
    rr: dict[str, Any] = intent_decision.raw_response if debug_router else {}
    cache_raw = rr.get("cache")
    cache_out = cache_raw if isinstance(cache_raw, str) and cache_raw in ("hit", "miss") else None
    h_raw = rr.get("cache_key_hash")
    hash_out = h_raw.strip() if isinstance(h_raw, str) and h_raw.strip() else None
    lat_raw = rr.get("latency_ms")
    lat_out: int | None = None
    if isinstance(lat_raw, (int, float)) and math.isfinite(float(lat_raw)):
        lat_out = int(round(float(lat_raw)))
    return {
        "tool": intent_decision.tool,
        "mode": intent_decision.mode,
        "reasoning": intent_decision.reasoning,
        "confidence": intent_decision.confidence,
        "fallback": intent_decision.fallback,
        "cache": cache_out,
        "cache_key_hash": hash_out,
        "latency_ms": lat_out,
    }


def _clarify_short_circuit_events(
    *,
    agent_result: AgentRunView,
    started_at: float,
    max_steps: int,
    debug_router: bool,
    debug_llm_prompts: bool,
) -> list[dict[str, Any]]:
    """P1-4：emit 关闭时由本模块补发与 SSE 增量路径一致的 agent.* 前缀帧。"""
    if not agent_result.clarify_short_circuit or agent_result.clarify_user_payload is None:
        return []
    intent_decision = agent_result.intent_decision
    out: list[dict[str, Any]] = [
        _event(
            typ="agent.step.start",
            started_at=started_at,
            step_id="a1",
            payload={"step_number": 1, "max_steps": max_steps},
        )
    ]
    if intent_decision is not None:
        out.append(
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
                out.append(
                    _event(
                        typ="agent.debug.llm_prompts",
                        started_at=started_at,
                        step_id="intent_llm_json",
                        payload={"scope": "intent", "items": _ilp},
                    )
                )
    _pp = agent_result.clarify_plan_preview_payload
    if isinstance(_pp, dict) and _pp:
        out.append(
            _event(
                typ="agent.plan.preview",
                started_at=started_at,
                step_id="a1_plan_prev",
                payload=_pp,
            )
        )
    out.append(
        _event(
            typ="agent.clarify",
            started_at=started_at,
            step_id="a1_clarify",
            payload=agent_result.clarify_user_payload,
        )
    )
    return out


# 契约静态扫描锚点：与 _agent_intent_obs_payload 键集合一致（勿删改键名）
_CONTRACT_ANCHOR_AGENT_INTENT_KEYS = _event(
    typ="agent.intent",
    started_at=0.0,
    step_id="__contract_anchor__",
    payload={
        "tool": "",
        "mode": "",
        "reasoning": "",
        "confidence": 0.0,
        "fallback": None,
        "cache": "hit",
        "cache_key_hash": "",
        "latency_ms": 0,
    },
)

_MASK_SECRET_RE = re.compile(r"(?i)\b(sk-[A-Za-z0-9]{10,}|sf-[A-Za-z0-9]{10,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b")


def _safe_text_for_event(text: str, *, max_len: int) -> str:
    t = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    t = _MASK_SECRET_RE.sub("***", t)
    t = t.replace("\n", "\\n")
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


# Text2SQL 结果摘要的敏感字段过滤：当前最小化仅过滤 id_number（未来可按权限扩展）。
_TEXT2SQL_SENSITIVE_COL_RE = re.compile(r"(?i)(^|_)id_number($|_)")


def _build_text2sql_exec_trace(
    *,
    sql: str,
    sql_raw: str,
    columns: list[str],
    rows: list[dict[str, Any]],
    error: str | None,
    latency_ms: int,
) -> dict[str, Any]:
    """构造可落库的 Text2SQL 执行摘要（严格限量/截断/脱敏）。"""
    truncated = False

    sql_safe = _safe_text_for_event(sql or "", max_len=2000)
    if (sql or "") != sql_safe:
        truncated = True

    sql_raw_safe = _safe_text_for_event(sql_raw or "", max_len=2000) if (sql_raw or "").strip() else ""
    if (sql_raw or "").strip() and sql_raw_safe != (sql_raw or ""):
        truncated = True

    err_safe: str | None = None
    if error:
        err_safe = _safe_text_for_event(str(error), max_len=300)
        if err_safe != str(error):
            truncated = True

    cols_in = [c for c in columns if isinstance(c, str) and c.strip()]
    if len(cols_in) > 30:
        truncated = True
    cols_raw = [c.strip() for c in cols_in[:30]]
    cols_safe = [_safe_text_for_event(c, max_len=64) for c in cols_raw]
    col_pairs = list(zip(cols_raw, cols_safe, strict=True))

    # rows_preview：允许落预览，但需过滤敏感列（当前仅 id_number）。
    def _is_sensitive_col(col: str) -> bool:
        return bool(_TEXT2SQL_SENSITIVE_COL_RE.search(col))

    has_sensitive_col = any(_is_sensitive_col(raw) or _is_sensitive_col(safe) for (raw, safe) in col_pairs)
    rows_preview: list[dict[str, str]] | None = None
    rows_preview = []
    if len(rows) > 10:
        truncated = True

    preview_pairs_all = col_pairs[:20]
    if len(col_pairs) > 20:
        truncated = True

    preview_pairs = [(raw, safe) for (raw, safe) in preview_pairs_all if not (_is_sensitive_col(raw) or _is_sensitive_col(safe))]
    if has_sensitive_col:
        truncated = True

    # 若只剩敏感列，则不落 rows_preview（只保留 rows_len/columns）。
    if not preview_pairs:
        rows_preview = None
    else:
        for r in rows[:10]:
            if not isinstance(r, dict):
                continue
            packed: dict[str, str] = {}
            for raw_col, safe_col in preview_pairs:
                v = r.get(raw_col)
                raw = "" if v is None else str(v)
                safe = _safe_text_for_event(raw, max_len=80)
                if safe != raw:
                    truncated = True
                packed[safe_col] = safe
            rows_preview.append(packed)

    out: dict[str, Any] = {
        "sql": sql_safe,
        "ok": bool(error is None),
        "error": err_safe,
        "latency_ms": int(latency_ms),
        "rows_len": int(len(rows)),
        "columns": cols_safe,
        "truncated": bool(truncated),
    }
    if sql_raw_safe:
        out["sql_raw"] = sql_raw_safe
    if rows_preview is not None and error is None:
        out["rows_preview"] = rows_preview
    return out


def _agent_text2sql_exec_trace(agent_result: Any) -> dict[str, Any] | None:  # noqa: ANN401
    """从 V2 Agent 的 steps 里提取 Text2SQL 的 sql/结果摘要（若可得）。"""
    steps = getattr(agent_result, "steps", None)
    if not isinstance(steps, list):
        return None

    for s in steps:
        tool_used = getattr(s, "tool_used", None)
        if tool_used != "text2sql_query":
            continue
        tool_result = getattr(s, "tool_result", None)
        data = getattr(tool_result, "data", None) if tool_result is not None else None
        if not isinstance(data, dict):
            return None
        sql = data.get("sql") if isinstance(data.get("sql"), str) else ""
        sql_raw = data.get("sql_raw") if isinstance(data.get("sql_raw"), str) else ""
        columns_any = data.get("columns")
        columns = [c for c in columns_any if isinstance(c, str)] if isinstance(columns_any, list) else []
        rows_any = data.get("rows")
        rows = [r for r in rows_any if isinstance(r, dict)] if isinstance(rows_any, list) else []
        err = getattr(tool_result, "error", None) if tool_result is not None else None
        err_s = err if isinstance(err, str) and err.strip() else None
        lat = getattr(tool_result, "latency_ms", 0) if tool_result is not None else 0
        try:
            latency_ms = int(lat)
        except Exception:  # noqa: BLE001
            latency_ms = 0
        if not sql and not sql_raw and not columns and not rows and err_s is None:
            return None
        return _build_text2sql_exec_trace(
            sql=sql,
            sql_raw=sql_raw,
            columns=columns,
            rows=rows,
            error=err_s,
            latency_ms=latency_ms,
        )
    return None


def _text2sql_grounding_from_agent_result(agent_result: Any) -> dict[str, Any] | None:  # noqa: ANN401
    """成功执行的 Text2SQL 步上抽取主表/SQL 摘要，写入 tool_results.text2sql_grounding。"""
    steps = getattr(agent_result, "steps", None)
    if not isinstance(steps, list):
        return None
    for s in steps:
        if getattr(s, "tool_used", None) != "text2sql_query":
            continue
        tr = getattr(s, "tool_result", None)
        if tr is None or not bool(getattr(tr, "success", False)):
            continue
        data = getattr(tr, "data", None)
        if not isinstance(data, dict):
            continue
        sql = data.get("sql")
        if not isinstance(sql, str) or not sql.strip():
            continue
        return build_text2sql_grounding_dict(sql=sql)
    return None


def _debug_router_evidence_enabled() -> bool:
    return (os.getenv("DEBUG_ROUTER_EVIDENCE", "0") or "").strip().lower() in ("1", "true", "yes", "on")


def _router_evidence_db_log_enabled() -> bool:
    # 默认开启：便于事后追溯；如需关闭可设置为 0/false/off。
    return (os.getenv("DEBUG_ROUTER_EVIDENCE_DB", "1") or "").strip().lower() in ("1", "true", "yes", "on")


def _router_trace_db_log_enabled() -> bool:
    # 默认开启：便于事后追溯；如需关闭可设置为 0/false/off。
    return (os.getenv("DEBUG_ROUTER_TRACE_DB", "1") or "").strip().lower() in ("1", "true", "yes", "on")


def _debug_agent_db_log_enabled() -> bool:
    return (os.getenv("DEBUG_AGENT_DB_LOG", "0") or "").strip().lower() in ("1", "true", "yes", "on")


def _debug_llm_prompts_enabled(body: dict[str, Any]) -> bool:
    """SSE/JSON：透传完整 LLM messages（Intent + 各工具内多段 LLM）。可用 env 或请求体开启。"""
    raw = (os.getenv("CHATBI_V2_DEBUG_LLM_PROMPTS", "") or "").strip().lower()
    if raw in ("1", "true", "yes", "on"):
        return True
    return bool(body.get("debug_llm_prompts") is True)


def _compact_event_digest(events: list[dict[str, Any]], *, max_events: int = 64) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for e in events[: max(1, int(max_events))]:
        if not isinstance(e, dict):
            continue
        typ = e.get("type")
        step_id = e.get("step_id")
        ts = e.get("ts")
        if not isinstance(typ, str) or not isinstance(step_id, str):
            continue
        try:
            ts_i = int(ts)
        except Exception:  # noqa: BLE001
            ts_i = 0
        out.append({"type": typ, "step_id": step_id, "ts": ts_i})
    return out


def _compact_errors(events: list[dict[str, Any]], *, max_items: int = 16) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for e in events:
        if not isinstance(e, dict) or e.get("type") != "error":
            continue
        payload = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        stage = payload.get("stage") if isinstance(payload.get("stage"), str) else ""
        msg = payload.get("message") if isinstance(payload.get("message"), str) else ""
        if stage or msg:
            out.append({"stage": _safe_text_for_event(stage, max_len=64), "message": _safe_text_for_event(msg, max_len=300)})
        if len(out) >= max(1, int(max_items)):
            break
    return out


def _shrink_router_trace_v1(trace: dict[str, Any], *, max_bytes: int = 8192) -> dict[str, Any]:
    """限制落库体积（best-effort）。超限时按“先丢非关键、后截断”策略缩小。"""
    try:
        raw = json.dumps(trace, ensure_ascii=False, separators=(",", ":"))
        if len(raw.encode("utf-8")) <= max_bytes:
            return trace
    except Exception:  # noqa: BLE001
        return trace

    t = dict(trace)
    # 1) 丢弃 events_digest
    t.pop("events_digest", None)
    try:
        if len(json.dumps(t, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) <= max_bytes:
            return t
    except Exception:  # noqa: BLE001
        return t

    # 2) 丢弃 candidates（仍保留 returned 计数与阈值）
    for k in ("ddl_search", "fts_search"):
        part = t.get(k)
        if isinstance(part, dict):
            part2 = dict(part)
            part2.pop("candidates", None)
            t[k] = part2
    try:
        if len(json.dumps(t, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) <= max_bytes:
            return t
    except Exception:  # noqa: BLE001
        return t

    # 3) 丢弃 text2sql_exec.rows_preview（保留 sql/ok/error/rows_len/columns）
    part = t.get("text2sql_exec")
    if isinstance(part, dict):
        part2 = dict(part)
        part2.pop("rows_preview", None)
        t["text2sql_exec"] = part2
    try:
        if len(json.dumps(t, ensure_ascii=False, separators=(",", ":")).encode("utf-8")) <= max_bytes:
            return t
    except Exception:  # noqa: BLE001
        return t

    # 4) 最后兜底：强制缩短 query_text
    for k in ("ddl_search", "fts_search"):
        part = t.get(k)
        if isinstance(part, dict) and isinstance(part.get("query_text"), str):
            part2 = dict(part)
            part2["query_text"] = _safe_text_for_event(part2["query_text"], max_len=80)
            t[k] = part2
    return t


def _async_save_rag_log(payload: dict[str, Any]) -> None:
    """异步写入 rag_conversation_logs（best-effort，不阻塞主流程）。"""
    try:
        def _sync_insert() -> None:
            supabase_table_insert_with_retry("rag_conversation_logs", payload)

        asyncio.create_task(asyncio.to_thread(_sync_insert))
    except Exception:
        # best-effort：任何异常都不影响主流程
        return


def _sync_persist_chatbi_v2_agent_log(
    *,
    session_id: str | None,
    query: str,
    run_id: str,
    prefer: PreferMode | str,
    started_at: float,
    agent_result: AgentRunView,
) -> dict[str, Any]:
    """V2 Agent 一轮结束落库（同步，在线程池中执行）。返回结构化结果供 SSE done / JSON 与 error 事件使用。"""
    if not session_id:
        return {"ok": True, "skipped": True, "reason": "no_session_id"}
    try:
        agent_steps_json: dict[str, Any] = {
            "total_steps": agent_result.final.total_steps,
            "tools_used": agent_result.final.tools_used,
            "fallback_used": agent_result.final.fallback_used,
            "steps": [
                {
                    "step_number": s.step_number,
                    "tool_used": s.tool_used,
                    "mode": s.mode,
                    "success": s.success,
                    "next_action": s.next_action,
                    "thought": s.think_payload.get("thought"),
                }
                for s in agent_result.steps
            ],
        }
        tool_results_json: dict[str, Any] = {
            "results": [
                {
                    "tool": s.tool_used,
                    "success": s.tool_result.success,
                    "error_code": s.tool_result.error_code,
                    "error_stage": s.tool_result.error_stage,
                    "latency_ms": s.tool_result.latency_ms,
                    "answer": (s.tool_result.data or {}).get("answer") if s.tool_result.data else None,
                }
                for s in agent_result.steps
            ]
        }
        t2s_ground = _text2sql_grounding_from_agent_result(agent_result)
        if t2s_ground:
            tool_results_json["text2sql_grounding"] = t2s_ground
        text2sql_exec_trace = _agent_text2sql_exec_trace(agent_result)
        router_trace_v1: dict[str, Any] | None = None
        mode_local = agent_result.final.mode
        if mode_local == "text2sql" and text2sql_exec_trace:
            router_trace_v1 = _shrink_router_trace_v1(
                {
                    "v": "router_trace_v1",
                    "ts_ms": int(time.time() * 1000),
                    "run_id": run_id,
                    "mode": mode_local,
                    "prefer": "auto" if prefer == "auto" else str(prefer),
                    "decision": {
                        "candidate_mode": "text2sql",
                        "final_mode": "text2sql",
                        "fallback": None,
                    },
                    "timing_ms": {"total": _now_ms(started_at)},
                    "text2sql_exec": text2sql_exec_trace,
                }
            )

        payload_full = {
            "session_id": session_id,
            "query": query,
            "rewritten_query": query,
            "retrieved_context": {},
            "response": agent_result.final.answer,
            "metadata": {
                "mode": agent_result.final.mode,
                "v": "chatbi_v2_agent",
                "router_debug": {"router_trace_v1": router_trace_v1},
            },
            "agent_steps": agent_steps_json,
            "tool_results": tool_results_json,
        }
        try:
            supabase_table_insert_with_retry("rag_conversation_logs", payload_full)
            return {"ok": True, "path": "full"}
        except Exception as exc:  # noqa: BLE001
            if _debug_agent_db_log_enabled():
                print(f"[agent-db] insert full failed: {exc!s}", flush=True)
            payload_fallback = {
                "session_id": session_id,
                "query": query,
                "rewritten_query": query,
                "retrieved_context": {},
                "response": agent_result.final.answer,
                "metadata": {
                    "mode": agent_result.final.mode,
                    "v": "chatbi_v2_agent",
                    "router_debug": {"router_trace_v1": router_trace_v1},
                    "agent": {"agent_steps": agent_steps_json, "tool_results": tool_results_json},
                    "agent_db_fallback": True,
                },
            }
            try:
                supabase_table_insert_with_retry("rag_conversation_logs", payload_fallback)
                return {
                    "ok": True,
                    "path": "fallback",
                    "full_insert_error": str(exc)[:500],
                }
            except Exception as exc2:  # noqa: BLE001
                if _debug_agent_db_log_enabled():
                    print(f"[agent-db] insert failed: {exc2!s}", flush=True)
                return {
                    "ok": False,
                    "path": "fallback",
                    "error": str(exc2)[:500],
                    "full_insert_error": str(exc)[:500],
                }
    except Exception as exc:  # noqa: BLE001
        if _debug_agent_db_log_enabled():
            print(f"[agent-db] insert failed: {exc!s}", flush=True)
        return {"ok": False, "path": "none", "error": str(exc)[:500]}


async def _await_persist_chatbi_v2_agent_log(
    *,
    session_id: str | None,
    query: str,
    run_id: str,
    prefer: PreferMode | str,
    started_at: float,
    agent_result: AgentRunView,
) -> dict[str, Any]:
    """在线程池执行落库，带总超时，避免无限挂死 SSE。"""
    raw = (os.getenv("CHATBI_AGENT_DB_PERSIST_TIMEOUT_S", "12") or "").strip()
    try:
        timeout_s = float(raw)
    except Exception:  # noqa: BLE001
        timeout_s = 12.0
    timeout_s = max(1.0, min(timeout_s, 120.0))
    try:
        return await asyncio.wait_for(
            asyncio.to_thread(
                _sync_persist_chatbi_v2_agent_log,
                session_id=session_id,
                query=query,
                run_id=run_id,
                prefer=prefer,
                started_at=started_at,
                agent_result=agent_result,
            ),
            timeout=timeout_s,
        )
    except asyncio.TimeoutError:
        return {
            "ok": False,
            "error": "persist_wait_timeout",
            "timeout_s": timeout_s,
            "hint": "Supabase 写入在超时内未完成，可能仍会在后台重试失败；会话摘要或次轮历史可能缺失",
        }


def _build_query_expand_event_payload(meta: dict[str, Any] | None, *, max_raw: int, max_expanded: int) -> dict[str, Any]:
    if not meta:
        return {"raw": "", "expanded": "", "candidates": [], "source": "none", "truncated": False, "enabled": False, "mode": "off"}
    raw = meta.get("raw") if isinstance(meta.get("raw"), str) else ""
    expanded = meta.get("expanded") if isinstance(meta.get("expanded"), str) else ""
    cands = meta.get("candidates") if isinstance(meta.get("candidates"), list) else []
    safe_cands: list[str] = []
    for c in cands[:8]:
        if isinstance(c, str) and c.strip():
            safe_cands.append(_safe_text_for_event(c.strip(), max_len=48))
    return {
        "raw": _safe_text_for_event(raw, max_len=max_raw),
        "expanded": _safe_text_for_event(expanded, max_len=max_expanded),
        "candidates": safe_cands,
        "source": meta.get("source"),
        "truncated": bool(meta.get("truncated")),
        "enabled": bool(meta.get("enabled")),
        "mode": meta.get("mode"),
    }


def _env_chatbi_sse_incremental_enabled() -> bool:
    """vNext：默认 true；false 时强制 await run 后批量 replay。"""
    raw = (os.getenv("CHATBI_SSE_INCREMENTAL", "true") or "").strip().lower()
    return raw not in ("0", "false", "no", "off")


def _request_sse_contract_v2(request: Request) -> bool:
    v = (request.headers.get("x-chatbi-sse-contract") or "").strip()
    return v == "2"


def _unified_agent_sse_incremental(request: Request) -> bool:
    return _env_chatbi_sse_incremental_enabled() and _request_sse_contract_v2(request)


def _sse_emit_queue_maxsize() -> int:
    """G2 增量 emit 队列上限（有界缓冲）；触顶时先发 `agent.llm.truncated`（vNext §4.3）。可调低便于单测。"""
    raw = (os.getenv("CHATBI_SSE_EMIT_QUEUE_MAX", "512") or "").strip()
    try:
        n = int(raw)
    except ValueError:
        n = 512
    # 下限取 1：允许单测用极小队列触发 backpressure（勿强制 ≥8，否则 CHATBI_SSE_EMIT_QUEUE_MAX=6 无效）
    return max(1, min(n, 8192))


def _sse_emit_queue_event_estimate_chars(ev: dict[str, Any]) -> int:
    try:
        return len(json.dumps(ev, ensure_ascii=False))
    except (TypeError, ValueError):
        return len(str(ev))


def _parse_prefer(raw: object) -> PreferMode:
    if not isinstance(raw, str):
        return "auto"
    v = raw.strip().lower()
    # 允许 no_data：跳过检索/查库，直接生成（用于 i18n/无证据场景兜底）。
    if v in ("rag", "text2sql", "no_data", "auto"):
        return v  # type: ignore[return-value]
    # 允许 tool:* 透传给 intent_router（v1 预留，未实现时会返回 error 事件）。
    if v.startswith("tool:"):
        return v  # type: ignore[return-value]
    return "auto"


def _build_rag_sources_event(hits: list[dict[str, Any]], *, top_k: int = 10) -> dict[str, Any]:
    packed: list[dict[str, Any]] = []
    for h in hits[: max(1, int(top_k))]:
        meta = h.get("metadata") if isinstance(h.get("metadata"), dict) else {}
        content = h.get("content") if isinstance(h.get("content"), str) else ""
        snippet = strip_doc_context_prefix(content).replace("\r\n", "\n").strip()
        snippet = snippet[:400] if len(snippet) > 400 else snippet
        packed.append(
            {
                "id": h.get("id"),
                "content": snippet,
                "filename": meta.get("filename"),
                "score": h.get("fused_score"),
                "path": meta.get("relativePath"),
                "url": meta.get("original_link"),
                "relativePath": meta.get("relativePath"),
                "slug": meta.get("slug"),
                "original_link": meta.get("original_link"),
                "category": meta.get("category"),
                "chunk_index": meta.get("chunk_index"),
                "snippet": snippet,
                "fused_score": h.get("fused_score"),
            }
        )
    return {"sources": packed, "retrieval": {"top_k": int(top_k), "rrf_k": RRF_K}}


def _router_evidence_payload(*, candidate_mode: str, final_mode: str, fallback: str | None, evidence: dict[str, Any] | None) -> dict[str, Any]:
    """构造 router.evidence 的 payload（用于 Timeline 直观展示降级前证据）。"""
    ev = evidence if isinstance(evidence, dict) else {}
    ddl_topk = int(os.getenv("INTENT_DDL_EVIDENCE_TOPK", "3"))
    ddl_min_score = float(os.getenv("INTENT_DDL_EVIDENCE_MIN_SCORE", "0.05"))
    fts_topk = int(os.getenv("INTENT_FTS_EVIDENCE_TOPK", "3"))
    return {
        "candidate_mode": candidate_mode,
        "final_mode": final_mode,
        "fallback": fallback,
        "ddl": {
            "hits": int(ev.get("ddl_hits") or 0),
            "top_score": ev.get("ddl_top_score"),
            "topk": ddl_topk,
            "min_score": ddl_min_score,
        },
        "fts": {
            "hits": int(ev.get("fts_hits") or 0),
            "top1_score": ev.get("fts_top1_score"),
            "topk": fts_topk,
        },
    }


def _rag_generate_answer(*, oai: OpenAI, chat_model: str, query: str, hits: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for i, h in enumerate(hits[:12]):
        content = h.get("content")
        if not isinstance(content, str) or not content.strip():
            continue
        parts.append(f"[#{i + 1}]\n{content.strip()}")
    context = "\n\n---\n\n".join(parts)
    system = (
        "你是一个检索增强问答助手。请仅基于提供的上下文回答；若上下文不足以回答，请明确说明不确定。\n"
        "回答要求：中文、简洁、给出关键结论；必要时引用上下文要点。"
    )
    user = f"【上下文】\n{context}\n\n【问题】\n{query}\n"
    res = oai.chat.completions.create(
        model=chat_model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.2,
        stream=False,
    )
    return (res.choices[0].message.content or "").strip()


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
    # P1-1 SQL AST gate 仍在 text2sql SQL 生成之后（apply_chatbi_sql_gate）；同请求内顺序：本守卫 → … → SQL gate。
    _pg_mode = chatbi_prompt_guard_mode()
    if _pg_mode != "off":
        _pg_res = prompt_guard_scan(query)
        if _pg_res.blocked:
            if _pg_mode == "warn" and not _pg_res.internal_error:
                log_chatbi_record(
                    message="prompt_guard_warn",
                    request_id=ctx_log.get("request_id"),
                    run_id=run_id,
                    session_id=session_id,
                    matched_rule_id=_pg_res.matched_rule_id,
                    reason_code=_pg_res.reason_code,
                    route="unified_chat",
                )
            else:
                log_chatbi_record(
                    message="prompt_guard_deny",
                    request_id=ctx_log.get("request_id"),
                    run_id=run_id,
                    session_id=session_id,
                    matched_rule_id=_pg_res.matched_rule_id,
                    reason_code=_pg_res.reason_code,
                    route="unified_chat",
                )
                events.append(
                    _event(
                        typ="error",
                        started_at=started_at,
                        step_id="e_prompt_guard",
                        payload={"stage": "prompt_guard", "message": "请求无法处理。"},
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
                    "evidence": {"agent_reasoning": intent_decision.reasoning_full if intent_decision else ""},
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
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")
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
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

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
    chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

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
                                "evidence": {"agent_reasoning": intent_decision.reasoning_full if intent_decision else ""},
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
                chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")
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
                chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

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
            chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

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

