from __future__ import annotations

import asyncio
import json
import math
import os
import re
import time
from typing import Any, Literal

from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from openai import OpenAI

from .agent import AgentRunView
from .chatbi_json_log import log_chatbi_record
from .chatbi_principal import ChatBiPrincipal
from .chatbi_prompt_guard import chatbi_prompt_guard_mode
from .chatbi_prompt_guard import scan as prompt_guard_scan

# Re-exports for test backward compatibility (tests monkeypatch unified_chat.xxx).
# These are used by JSON/SSE handlers via their own imports; kept here for test patches.
from .chatbi_sql_gate import apply_chatbi_sql_gate  # noqa: F401
from .hybrid_fusion import RRF_K
from .intent_agent import IntentDecision, build_intent_path_obs
from .query_rewrite import rewrite_query_with_history  # noqa: F401
from .rag_env import (  # noqa: F401
    openai_siliconflow_client,
    supabase_client,
    supabase_table_insert_with_retry,
)
from .rag_shared import strip_doc_context_prefix
from .text2sql_core import execute_select_sql, llm_generate_sql, llm_summarize  # noqa: F401
from .text2sql_grounding import build_text2sql_grounding_dict
from .text2sql_store import get_text2sql_store  # noqa: F401
from .tools import get_tool_registry  # noqa: F401

PreferMode = Literal["auto", "rag", "text2sql", "no_data"]


def _chatbi_log_ctx(request: Request) -> dict[str, Any]:
    return {"request_id": (request.headers.get("x-request-id") or "").strip() or None}


def _now_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _event(*, typ: str, started_at: float, step_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"type": typ, "ts": _now_ms(started_at), "step_id": step_id, "payload": payload}


def _unified_prompt_guard_short_circuit_events(
    query: str,
    *,
    ctx_log: dict[str, Any],
    run_id: str,
    session_id: str | None,
    started_at: float,
    route: str = "unified_chat",
) -> tuple[bool, list[dict[str, Any]]]:
    """P1-2：早于任何上游 LLM；与 JSON / SSE 共用。返回 (应短路, [error, latency] 或 [])。"""
    mode = chatbi_prompt_guard_mode()
    if mode == "off":
        return (False, [])
    res = prompt_guard_scan(query)
    if not res.blocked:
        return (False, [])
    if mode == "warn" and not res.internal_error:
        log_chatbi_record(
            message="prompt_guard_warn",
            request_id=ctx_log.get("request_id"),
            run_id=run_id,
            session_id=session_id,
            matched_rule_id=res.matched_rule_id,
            reason_code=res.reason_code,
            route=route,
        )
        return (False, [])
    log_chatbi_record(
        message="prompt_guard_deny",
        request_id=ctx_log.get("request_id"),
        run_id=run_id,
        session_id=session_id,
        matched_rule_id=res.matched_rule_id,
        reason_code=res.reason_code,
        route=route,
    )
    return (
        True,
        [
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_prompt_guard",
                payload={"stage": "prompt_guard", "message": "请求无法处理。"},
            ),
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
            ),
        ],
    )


def _router_agent_evidence(intent_decision: IntentDecision | None) -> dict[str, Any]:
    """router.decision.evidence：Intent reasoning + 路径可观测（U1.5 重试 / Step2 仲裁）。"""
    out: dict[str, Any] = {
        "agent_reasoning": intent_decision.reasoning_full if intent_decision else "",
    }
    raw = intent_decision.raw_response if intent_decision is not None else None
    out.update(build_intent_path_obs(raw if isinstance(raw, dict) else None))
    return out


def _agent_intent_obs_payload(intent_decision: IntentDecision, *, debug_router: bool) -> dict[str, Any]:
    """agent.intent 的 payload：路径/仲裁字段始终透出；cache 哈希等仅在 debug_router。"""
    rr: dict[str, Any] = (
        dict(intent_decision.raw_response) if isinstance(intent_decision.raw_response, dict) else {}
    )
    cache_raw = rr.get("cache")
    cache_out = cache_raw if isinstance(cache_raw, str) and cache_raw in ("hit", "miss") else None
    h_raw = rr.get("cache_key_hash")
    hash_out = h_raw.strip() if isinstance(h_raw, str) and h_raw.strip() else None
    lat_raw = rr.get("latency_ms")
    lat_out: int | None = None
    if isinstance(lat_raw, (int, float)) and math.isfinite(float(lat_raw)):
        lat_out = int(round(float(lat_raw)))
    if not debug_router:
        hash_out = None

    return {
        "tool": intent_decision.tool,
        "mode": intent_decision.mode,
        "reasoning": intent_decision.reasoning,
        "confidence": intent_decision.confidence,
        "fallback": intent_decision.fallback,
        "cache": cache_out,
        "cache_key_hash": hash_out,
        "latency_ms": lat_out,
        **build_intent_path_obs(rr),
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
        "intent_path": "llm",
        "intent_attempt": 1,
        "hints_arbitration": None,
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
    from .unified.json_handler import handle_unified_chat as _json_handler
    return await _json_handler(request, principal=principal)



def _sse(event: str, data: dict[str, Any]) -> str:
    from .unified.sse_handler import _sse as _sse_impl
    return _sse_impl(event, data)


async def handle_unified_chat_stream(
    request: Request,
    *,
    principal: ChatBiPrincipal,
) -> StreamingResponse:
    from .unified.sse_handler import handle_unified_chat_stream as _sse_handler
    return await _sse_handler(request, principal=principal)

