from __future__ import annotations

import asyncio
import os
import time
from typing import Any

from .chatbi_agent_models import AgentRunView
from .rag_env import supabase_table_insert_with_retry


def _debug_agent_db_log_enabled() -> bool:
    return (os.getenv("DEBUG_AGENT_DB_LOG", "0") or "").strip().lower() in ("1", "true", "yes", "on")


def _now_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def shrink_router_trace_v1(trace: dict[str, Any], *, max_bytes: int = 8192) -> dict[str, Any]:
    """限制落库体积（best-effort）。超限时按"先丢非关键、后截断"策略缩小。"""
    import json

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


_MASK_SECRET_RE = __import__("re").compile(
    r"(?i)\b(sk-[A-Za-z0-9]{10,}|sf-[A-Za-z0-9]{10,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b"
)


def _safe_text_for_event(text: str, *, max_len: int) -> str:
    t = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    t = _MASK_SECRET_RE.sub("***", t)
    t = t.replace("\n", "\\n")
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


_TEXT2SQL_SENSITIVE_COL_RE = __import__("re").compile(r"(?i)(^|_)id_number($|_)")


def build_text2sql_exec_trace(
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
        return build_text2sql_exec_trace(
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
    from .text2sql_grounding import build_text2sql_grounding_dict

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


def sync_persist_chatbi_v2_agent_log(
    *,
    session_id: str | None,
    query: str,
    run_id: str,
    prefer: str,
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
            router_trace_v1 = shrink_router_trace_v1(
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


async def await_persist_chatbi_v2_agent_log(
    *,
    session_id: str | None,
    query: str,
    run_id: str,
    prefer: str,
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
                sync_persist_chatbi_v2_agent_log,
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
