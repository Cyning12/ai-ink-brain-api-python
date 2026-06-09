from __future__ import annotations

import asyncio
import os
import time
from collections.abc import Awaitable, Callable
from typing import Any

from openai import OpenAI

from .chatbi_policies import load_chatbi_table_policies_sync
from .chatbi_request_ctx import get_chatbi_log_ctx, get_chatbi_principal
from .chatbi_sql_gate import (
    ChatBiSqlGateDenied,
    apply_chatbi_sql_gate,
    filter_text2sql_retrieved,
)
from .query_rewrite import history_to_rewrite_block
from .rag_env import siliconflow_base
from .text2sql_core import (
    build_sql_prompt,
    build_summary_prompt,
    execute_mutating_sql,
    execute_select_sql,
    llm_generate_sql,
    llm_summarize,
    try_summarize_aggregate,
    validate_sql_readonly,
)
from .text2sql_schema_prefetch import run_text2sql_schema_prefetch_sync
from .text2sql_store import get_text2sql_store
from .text2sql_value_hints import build_value_hints_block_for_text2sql
from .tool_models import ToolResult
from .tools_shared import (
    _elapsed_ms,
    _pick_chat_model,
    _sql_error_code_from_message,
    _sql_exec_user_facing_error,
)


def _text2sql_retrieve_query(query: str, history: list[dict[str, Any]] | None) -> str:
    """多轮追问常省略表名；把历史 Q/A 拼进检索串，便于向量/哈希检索命中上轮相关 DDL。"""
    block = history_to_rewrite_block(history or [])
    if not block:
        return query
    merged = f"{block}\n\n【当前问题】\n{query}".strip()
    max_len = int(os.getenv("TEXT2SQL_RETRIEVE_QUERY_MAX_LEN", "1200"))
    if max_len > 0 and len(merged) > max_len:
        merged = merged[-max_len:]
    return merged


_T2SQL_GEN_SYSTEM = "You are a helpful assistant."


def _t2sql_chain_dict(typ: str, chain_started_at: float, step_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """与 agent._agent_chain 同形，供 Text2SQL 子阶段 SSE 复用。"""
    return {"type": typ, "ts": int((time.perf_counter() - chain_started_at) * 1000), "step_id": step_id, "payload": payload}


def _text2sql_llm_fallback_timeout_s() -> float:
    raw = (os.getenv("CHATBI_TEXT2SQL_LLM_TIMEOUT_S") or "").strip()
    if raw:
        try:
            v = float(raw)
            return max(1.0, min(v, 600.0))
        except ValueError:
            pass
    return 120.0


def _text2sql_llm_sql_timeout_s() -> float:
    raw = (os.getenv("CHATBI_TEXT2SQL_LLM_SQL_TIMEOUT_S") or "").strip()
    if raw:
        try:
            v = float(raw)
            return max(1.0, min(v, 600.0))
        except ValueError:
            pass
    return _text2sql_llm_fallback_timeout_s()


def _text2sql_llm_summary_timeout_s() -> float:
    raw = (os.getenv("CHATBI_TEXT2SQL_LLM_SUMMARY_TIMEOUT_S") or "").strip()
    if raw:
        try:
            v = float(raw)
            return max(1.0, min(v, 600.0))
        except ValueError:
            pass
    return _text2sql_llm_fallback_timeout_s()


def _text2sql_summary_chat_model() -> str:
    """未设置 CHATBI_TEXT2SQL_SUMMARY_LLM_MODEL 时与 Intent 默认模型对齐。"""
    raw = (os.getenv("CHATBI_TEXT2SQL_SUMMARY_LLM_MODEL") or "").strip()
    if raw:
        return raw
    return os.getenv("INTENT_LLM_MODEL", "deepseek-ai/DeepSeek-V4-Pro")


def _clip_dialogue_context_block(ctx: str) -> str:
    max_len = int(os.getenv("TEXT2SQL_DIALOGUE_CONTEXT_MAX_LEN", "8000"))
    if max_len <= 0 or len(ctx) <= max_len:
        return ctx
    return ctx[-max_len:]


def _t2sql_phase_kind(phase_id: str) -> str:
    if phase_id in ("llm_sql", "llm_summary"):
        return "llm"
    if phase_id == "db":
        return "db"
    return "io"


def _msg_looks_like_timeout(msg: str) -> bool:
    m = (msg or "").lower()
    return "timeout" in m or "timed out" in m


async def text2sql_execute(
    query: str,
    *,
    history: list[dict[str, Any]] | None = None,
    debug_llm_prompts: bool = False,
    chain_emit: Callable[[dict[str, Any]], Awaitable[None]] | None = None,
    chain_started_at: float | None = None,
    json_log_ctx: dict[str, Any] | None = None,
    preview_only: bool = False,
) -> ToolResult:
    started_at = time.perf_counter()
    phases_ms: dict[str, int] = {}
    hist = history or []
    raw_ctx = history_to_rewrite_block(hist)
    dialogue_ctx = _clip_dialogue_context_block(raw_ctx)
    llm_prompts: list[dict[str, Any]] = []

    def _data_with_phases(extra: dict[str, Any] | None) -> dict[str, Any] | None:
        if not phases_ms and not extra:
            return None
        out = dict(extra or {})
        if phases_ms:
            out["text2sql_phases_ms"] = dict(phases_ms)
        return out or None

    async def _emit_phase_start(phase_id: str) -> None:
        if chain_emit is None or chain_started_at is None:
            return
        sid = f"text2sql.phase.{phase_id}"
        await chain_emit(
            _t2sql_chain_dict(
                "text2sql.phase.start",
                chain_started_at,
                sid,
                {
                    "subphase_id": sid,
                    "phase_id": phase_id,
                    "phase_kind": _t2sql_phase_kind(phase_id),
                },
            )
        )

    async def _emit_phase_end(phase_id: str, t0: float, *, chain_extra: dict[str, Any] | None = None) -> None:
        ms = max(0, int((time.perf_counter() - t0) * 1000))
        phases_ms[phase_id] = ms
        sid = f"text2sql.phase.{phase_id}"
        if json_log_ctx:
            from .chatbi_json_log import chatbi_json_log_enabled, log_chatbi_record

            if chatbi_json_log_enabled():
                log_chatbi_record(
                    message="text2sql_phase_end",
                    request_id=json_log_ctx.get("request_id"),
                    run_id=json_log_ctx.get("run_id"),
                    session_id=json_log_ctx.get("session_id"),
                    route="agent",
                    mode="text2sql",
                    tool="text2sql_query",
                    subphase_id=sid,
                    phase_id=phase_id,
                    text2sql_phases_ms=dict(phases_ms),
                    schema_prefetch_source=(chain_extra or {}).get("schema_prefetch_source"),
                    schema_prefetch_tables=(chain_extra or {}).get("schema_prefetch_tables"),
                )
        if chain_emit is None or chain_started_at is None:
            return
        # 第四参数须为字面量 `{...}`：`tech_graph_contract_check` 用「type 串后首个 `{`」扫 payload 键；
        # 若传变量名，会误扫到下方 `chain_pf = {` 的 schema_* 键并漏掉 latency/phase 键。
        await chain_emit(
            _t2sql_chain_dict(
                "text2sql.phase.end",
                chain_started_at,
                sid,
                {
                    "subphase_id": sid,
                    "phase_id": phase_id,
                    "latency_ms": ms,
                    **(chain_extra or {}),
                },
            )
        )

    try:
        await _emit_phase_start("retrieve")
        t_retrieve = time.perf_counter()
        store = get_text2sql_store()
        topk = int(os.getenv("TEXT2SQL_RETRIEVE_TOPK", "6"))
        retrieve_q = _text2sql_retrieve_query(query, hist)
        retrieved = store.search(retrieve_q, top_k=topk)
        principal = get_chatbi_principal()
        pols_loaded = None
        if principal is not None:
            pols_loaded = await asyncio.to_thread(load_chatbi_table_policies_sync)
            retrieved = filter_text2sql_retrieved(retrieved, principal=principal, policies=pols_loaded)

        api_key = os.getenv("SILICONFLOW_API_KEY", "").strip()
        oai = OpenAI(api_key=api_key, base_url=siliconflow_base())
        chat_model = _pick_chat_model()

        vh_block = await asyncio.to_thread(
            build_value_hints_block_for_text2sql, retrieved, history=hist
        )
        await _emit_phase_end("retrieve", t_retrieve)

        await _emit_phase_start("schema_prefetch")
        t_pf = time.perf_counter()
        prefetch_block, pf_err, pf_meta = await asyncio.to_thread(
            run_text2sql_schema_prefetch_sync,
            user_query=query,
            retrieved=retrieved,
            principal=principal,
            policies=pols_loaded,
        )
        chain_pf: dict[str, Any] = {
            "schema_prefetch_source": pf_meta.get("schema_prefetch_source"),
            "schema_prefetch_tables": pf_meta.get("schema_prefetch_tables") or [],
        }
        if pf_meta.get("schema_prefetch_candidates") is not None:
            chain_pf["schema_prefetch_candidates"] = pf_meta.get("schema_prefetch_candidates")
        await _emit_phase_end("schema_prefetch", t_pf, chain_extra=chain_pf)
        if pf_err:
            policy = pf_meta.get("schema_prefetch_source") == "error_policy"
            if policy:
                user_msg = (
                    "当前账号无权对该表执行写入或更新（表级安全策略限制）。"
                    "如需开通，请联系管理员在 chatbi_sql_table_policy 中配置权限或提升访问等级。"
                )
                return ToolResult(
                    success=False,
                    data=_data_with_phases({"schema_prefetch": pf_meta, "technical_message": pf_err}),
                    error=user_msg,
                    error_code="CHATBI_SQL_WRITE_DENIED",
                    error_stage="text2sql.schema_prefetch",
                    latency_ms=_elapsed_ms(started_at),
                )
            return ToolResult(
                success=False,
                data=_data_with_phases({"schema_prefetch": pf_meta}),
                error=pf_err,
                error_code="TEXT2SQL_SCHEMA_PREFETCH_FAILED",
                error_stage="text2sql.schema_prefetch",
                latency_ms=_elapsed_ms(started_at),
            )

        sql_prompt = build_sql_prompt(
            query,
            retrieved,
            dialogue_context=dialogue_ctx or None,
            value_hints_block=vh_block,
            prefetched_schema_block=prefetch_block,
            chatbi_access_level=principal.access_level if principal else None,
            chatbi_subject_user_id=principal.subject_user_id if principal else None,
        )

        if debug_llm_prompts:
            llm_prompts.append(
                {
                    "phase": "text2sql_sql",
                    "model": chat_model,
                    "messages": [
                        {"role": "system", "content": _T2SQL_GEN_SYSTEM},
                        {"role": "user", "content": sql_prompt},
                    ],
                }
            )
        await _emit_phase_start("llm_sql")
        t_llm_sql = time.perf_counter()
        try:
            sql_raw = await asyncio.wait_for(
                asyncio.to_thread(
                    lambda: llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
                ),
                timeout=_text2sql_llm_sql_timeout_s(),
            )
        except asyncio.TimeoutError:
            await _emit_phase_end("llm_sql", t_llm_sql)
            return ToolResult(
                success=False,
                data=_data_with_phases({"detail": {"phase": "llm_sql"}}),
                error="Text2SQL SQL 生成 LLM 超时",
                error_code="LLM_API_TIMEOUT",
                error_stage="text2sql.generate",
                latency_ms=_elapsed_ms(started_at),
            )
        except Exception as exc:  # noqa: BLE001
            await _emit_phase_end("llm_sql", t_llm_sql)
            msg = str(exc)
            if _msg_looks_like_timeout(msg):
                return ToolResult(
                    success=False,
                    data=_data_with_phases({"detail": {"phase": "llm_sql"}}),
                    error=msg,
                    error_code="LLM_API_TIMEOUT",
                    error_stage="text2sql.generate",
                    latency_ms=_elapsed_ms(started_at),
                )
            return ToolResult(
                success=False,
                data=_data_with_phases(None),
                error=msg,
                error_code=_sql_error_code_from_message(msg),
                error_stage="text2sql.generate",
                latency_ms=_elapsed_ms(started_at),
            )
        await _emit_phase_end("llm_sql", t_llm_sql)

        sql_raw = (sql_raw or "").strip()
        if not sql_raw:
            return ToolResult(
                success=False,
                data=_data_with_phases(None),
                error="SQL 生成为空",
                error_code="SQL_GEN_EMPTY",
                error_stage="text2sql.generate",
                latency_ms=_elapsed_ms(started_at),
            )

        await _emit_phase_start("validate")
        t_validate = time.perf_counter()
        sql = ""
        sql_kind = "select"
        try:
            principal2 = get_chatbi_principal()
            merged = {**(get_chatbi_log_ctx() or {}), **(json_log_ctx or {})}
            if principal2 is None:
                sql = validate_sql_readonly(sql_raw)
                sql_kind = "select"
            else:
                pols = pols_loaded
                if pols is None:
                    pols = await asyncio.to_thread(load_chatbi_table_policies_sync)
                sql, sk = apply_chatbi_sql_gate(
                    sql_raw,
                    principal=principal2,
                    policies=pols,
                    run_id=merged.get("run_id"),
                    request_id=merged.get("request_id"),
                )
                sql_kind = sk
        except ChatBiSqlGateDenied as exc:
            await _emit_phase_end("validate", t_validate)
            return ToolResult(
                success=False,
                data=_data_with_phases(None),
                error=exc.message_zh,
                error_code=exc.deny_code,
                error_stage="text2sql.validate",
                latency_ms=_elapsed_ms(started_at),
            )
        except Exception as exc:  # noqa: BLE001
            await _emit_phase_end("validate", t_validate)
            msg = str(exc)
            return ToolResult(
                success=False,
                data=_data_with_phases(None),
                error=msg,
                error_code=_sql_error_code_from_message(msg) if "SQL_GEN" in msg else "SQL_GEN_SYNTAX",
                error_stage="text2sql.validate",
                latency_ms=_elapsed_ms(started_at),
            )
        await _emit_phase_end("validate", t_validate)

        if preview_only:
            return ToolResult(
                success=True,
                data=_data_with_phases(
                    {
                        "sql": sql,
                        "sql_kind": sql_kind,
                        "preview_only": True,
                        "answer": "（预览）已通过只读校验的 SQL 草案，尚未连接数据库执行。",
                    }
                ),
                error=None,
                error_code=None,
                error_stage=None,
                latency_ms=_elapsed_ms(started_at),
            )

        await _emit_phase_start("db")
        t_db = time.perf_counter()
        try:
            if sql_kind == "select":
                columns, rows = await asyncio.to_thread(
                    lambda: execute_select_sql(
                        sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200"))
                    )
                )
            else:
                rowcount = await asyncio.to_thread(lambda: execute_mutating_sql(sql))
                columns = ["affected_rows"]
                rows = [{"affected_rows": rowcount}]
        except Exception as exc:  # noqa: BLE001
            await _emit_phase_end("db", t_db)
            msg = str(exc)
            ec = _sql_error_code_from_message(msg)
            return ToolResult(
                success=False,
                data=_data_with_phases(None),
                error=_sql_exec_user_facing_error(msg, code=ec),
                error_code=ec,
                error_stage="text2sql.execute",
                latency_ms=_elapsed_ms(started_at),
            )
        await _emit_phase_end("db", t_db)

        if sql_kind == "select" and not rows:
            return ToolResult(
                success=False,
                data=_data_with_phases(None),
                error="SQL 无数据",
                error_code="SQL_EXEC_NO_DATA",
                error_stage="text2sql.execute",
                latency_ms=_elapsed_ms(started_at),
            )

        summary_model = _text2sql_summary_chat_model()
        agg = try_summarize_aggregate(query, columns, rows)
        if agg is not None:
            answer = agg
        else:
            sum_prompt = build_summary_prompt(query, sql, columns, rows)
            if debug_llm_prompts:
                llm_prompts.append(
                    {
                        "phase": "text2sql_summary",
                        "model": summary_model,
                        "messages": [
                            {"role": "system", "content": _T2SQL_GEN_SYSTEM},
                            {"role": "user", "content": sum_prompt},
                        ],
                    }
                )
            await _emit_phase_start("llm_summary")
            t_sum = time.perf_counter()
            try:
                answer = await asyncio.wait_for(
                    asyncio.to_thread(
                        lambda: llm_summarize(oai=oai, model=summary_model, prompt=sum_prompt)
                    ),
                    timeout=_text2sql_llm_summary_timeout_s(),
                )
                await _emit_phase_end("llm_summary", t_sum)
            except asyncio.TimeoutError:
                await _emit_phase_end("llm_summary", t_sum)
                return ToolResult(
                    success=False,
                    data=_data_with_phases({"detail": {"phase": "llm_summary"}}),
                    error="Text2SQL 总结 LLM 超时",
                    error_code="LLM_API_TIMEOUT",
                    error_stage="text2sql.summarize",
                    latency_ms=_elapsed_ms(started_at),
                )
            except Exception as exc:  # noqa: BLE001
                await _emit_phase_end("llm_summary", t_sum)
                msg = str(exc)
                if _msg_looks_like_timeout(msg):
                    return ToolResult(
                        success=False,
                        data=_data_with_phases({"detail": {"phase": "llm_summary"}}),
                        error=msg,
                        error_code="LLM_API_TIMEOUT",
                        error_stage="text2sql.summarize",
                        latency_ms=_elapsed_ms(started_at),
                    )
                # 非超时：降级为行数摘要（保持与旧版兼容）
                answer = f"查询返回 {len(rows)} 行结果。"

        out: dict[str, Any] = {"answer": answer, "sql": sql, "columns": columns, "rows": rows}
        out["schema_prefetch"] = pf_meta
        out["text2sql_phases_ms"] = dict(phases_ms)
        if debug_llm_prompts and llm_prompts:
            out["llm_prompts"] = llm_prompts
        return ToolResult(success=True, data=out, latency_ms=_elapsed_ms(started_at))
    except asyncio.TimeoutError:
        return ToolResult(
            success=False,
            data=_data_with_phases(None),
            error="Text2SQL 超时",
            error_code="LLM_API_TIMEOUT",
            error_stage="llm.call",
            latency_ms=_elapsed_ms(started_at),
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        return ToolResult(
            success=False,
            data=_data_with_phases(None),
            error=msg,
            error_code=_sql_error_code_from_message(msg),
            error_stage="text2sql.tool",
            latency_ms=_elapsed_ms(started_at),
        )

