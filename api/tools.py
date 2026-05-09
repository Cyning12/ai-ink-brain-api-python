from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Literal

from openai import OpenAI

from .hybrid_fusion import RRF_K, fuse_hits_rrf
from .rag_env import (
    embedding_kwargs_for_inputs,
    openai_siliconflow_client,
    siliconflow_base,
    supabase_client,
)
from .rag_recall_tools import (
    keyword_query_text_with_i18n_meta,
    rpc_execute_with_retry,
    structured_recall_by_date,
)
from .rag_shared import parse_match_threshold, strip_doc_context_prefix
from .text2sql_core import (
    build_sql_prompt,
    build_summary_prompt,
    execute_select_sql,
    llm_generate_sql,
    llm_summarize,
    validate_sql_readonly,
)
from .query_rewrite import build_rewrite_llm_messages, history_to_rewrite_block
from .text2sql_store import get_text2sql_store


@dataclass(frozen=True)
class ToolResult:
    """Tool 执行结果（Agent 仅依赖 error_code/error_stage 做失败类型判定）。"""

    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None
    error_code: str | None = None
    error_stage: str | None = None
    latency_ms: int = 0


ToolName = Literal["rag_search", "text2sql_query", "direct_answer"]


@dataclass(frozen=True)
class Tool:
    name: ToolName
    description: str
    parameters: dict[str, Any]
    execute: Callable[..., Awaitable[ToolResult]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())


def _elapsed_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _pick_chat_model() -> str:
    return os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")


def _pick_embed_model_kwargs() -> dict[str, Any]:
    # 统一由 embedding_kwargs_for_inputs 处理维度参数等
    return {}


def _sql_error_code_from_message(msg: str) -> str:
    m = (msg or "").lower()
    # 粗粒度映射：足够满足 gating/fallback 行为（CI 不应强依赖文案精确命中）
    if "syntax" in m or "parse" in m or "token" in m:
        return "SQL_GEN_SYNTAX"
    if "does not exist" in m or "relation" in m or "undefined table" in m or "表" in msg:
        return "SQL_EXEC_TABLE_NOT_FOUND"
    if "permission" in m or "denied" in m or "权限" in msg:
        return "SQL_EXEC_PERMISSION_DENIED"
    if "no data" in m or "empty" in m:
        return "SQL_EXEC_NO_DATA"
    return "UNKNOWN"


def _rag_should_treat_as_uncertain(answer: str) -> bool:
    a = (answer or "").strip()
    if not a:
        return True
    # 与 V1 行为一致：当模型明确表达“不确定/无法回答”，可按不确定失败处理
    lowered = a.lower()
    return "不确定" in lowered or "无法" in lowered or "暂时无法" in lowered


def _safe_snippet(text: str, *, max_len: int) -> str:
    t = (text or "").replace("\r\n", "\n").replace("\r", "\n").strip()
    return t[:max_len] if len(t) > max_len else t


async def _rag_retrieve(query: str, *, rewritten: str, history: list[dict[str, Any]]) -> dict[str, Any]:
    oai = openai_siliconflow_client()
    chat_model = _pick_chat_model()
    # embed
    vec: list[float] | None = None
    emb_err: str | None = None
    try:
        emb_res = await asyncio.to_thread(
            lambda: oai.embeddings.create(**embedding_kwargs_for_inputs([rewritten]))
        )
        vec = list(emb_res.data[0].embedding)
    except Exception as exc:  # noqa: BLE001
        emb_err = str(exc)
        vec = None

    match_threshold = parse_match_threshold()
    match_count = int(os.getenv("RAG_MATCH_COUNT", "10"))
    retry_count = 0

    structured_hits = structured_recall_by_date(
        supabase_client(), query=query, rewritten=rewritten, limit_rows=6
    ).hits

    vector_hits: list[dict[str, Any]] = []
    if vec is not None:
        vector_hits, rc_vec, err_vec = rpc_execute_with_retry(
            supabase_client(),
            "match_documents",
            {"query_embedding": vec, "match_count": match_count, "match_threshold": match_threshold},
            retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
        )
        retry_count += rc_vec
        _ = err_vec  # 仅记录，不阻断

    kw_qt_raw, _kw_meta_raw = keyword_query_text_with_i18n_meta(query)
    kw_qt_rw, _kw_meta_rw = keyword_query_text_with_i18n_meta(rewritten)

    keyword_hits_raw, rc_raw, _err_raw = rpc_execute_with_retry(
        supabase_client(),
        "keyword_documents",
        {"query_text": kw_qt_raw, "match_count": 12},
        retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
    )
    retry_count += rc_raw

    keyword_hits_rewrite, rc_rw, _err_rw = rpc_execute_with_retry(
        supabase_client(),
        "keyword_documents",
        {"query_text": kw_qt_rw, "match_count": 12},
        retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
    )
    retry_count += rc_rw

    merged_keyword = fuse_hits_rrf(keyword_hits_raw, keyword_hits_rewrite, max_total=22)
    merged_kw2 = fuse_hits_rrf(structured_hits, merged_keyword, max_total=22)
    hits = fuse_hits_rrf(vector_hits, merged_kw2, max_total=22)

    return {
        "hits": hits,
        "latency": {"retry_count": retry_count, "embedding_error": emb_err, "rrf_k": RRF_K},
        "top_k": 10,
        "history": history,
    }


async def rag_search_execute(
    query: str,
    *,
    history: list[dict[str, Any]] | None = None,
    debug_llm_prompts: bool = False,
) -> ToolResult:
    started_at = time.perf_counter()
    hist = history or []
    llm_prompts: list[dict[str, Any]] = []
    try:
        oai = openai_siliconflow_client()
        chat_model = _pick_chat_model()
        rw_msgs = build_rewrite_llm_messages(history=hist[-6:], query=query)
        rewrite_ms = 0
        if rw_msgs is None:
            rewritten = query
        else:
            if debug_llm_prompts:
                llm_prompts.append({"phase": "rag.rewrite", "model": chat_model, "messages": list(rw_msgs)})
            t_rw0 = time.perf_counter()

            def _sync_rw() -> str:
                res = oai.chat.completions.create(
                    model=chat_model,
                    messages=rw_msgs,
                    temperature=0.0,
                    stream=False,
                )
                try:
                    return (res.choices[0].message.content or "").strip()
                except Exception:  # noqa: BLE001
                    return ""

            rw_out = await asyncio.to_thread(_sync_rw)
            rewrite_ms = int((time.perf_counter() - t_rw0) * 1000)
            rewritten = rw_out if rw_out else query

        retrieved = await _rag_retrieve(query, rewritten=rewritten, history=hist)
        hits = retrieved.get("hits")
        if not isinstance(hits, list) or not hits:
            data_err: dict[str, Any] | None = None
            if debug_llm_prompts and llm_prompts:
                data_err = {"llm_prompts": llm_prompts, "rewritten": rewritten, "rewrite_latency_ms": rewrite_ms}
            return ToolResult(
                success=False,
                data=data_err,
                error="RAG 命中为空",
                error_code="RAG_RETRIEVE_EMPTY",
                error_stage="rag.retrieve",
                latency_ms=_elapsed_ms(started_at),
            )

        parts: list[str] = []
        for i, h in enumerate(hits[:12]):
            content = h.get("content") if isinstance(h, dict) else None
            if not isinstance(content, str) or not content.strip():
                continue
            parts.append(f"[#{i + 1}]\n{_safe_snippet(content, max_len=1500)}")
        context = "\n\n---\n\n".join(parts)

        system = (
            "你是一个检索增强问答助手。请仅基于提供的上下文回答；若上下文不足以回答，请明确说明不确定。\n"
            "回答要求：中文、简洁、给出关键结论；必要时引用上下文要点。"
        )
        user = f"【上下文】\n{context}\n\n【问题】\n{query}\n"
        gen_messages = [{"role": "system", "content": system}, {"role": "user", "content": user}]
        if debug_llm_prompts:
            llm_prompts.append({"phase": "rag.generate", "model": chat_model, "messages": gen_messages})

        def _sync_generate() -> str:
            res = oai.chat.completions.create(
                model=chat_model,
                messages=gen_messages,
                temperature=0.2,
                stream=False,
            )
            return (res.choices[0].message.content or "").strip()

        answer = await asyncio.to_thread(_sync_generate)
        if not answer or _rag_should_treat_as_uncertain(answer):
            data_err2: dict[str, Any] | None = None
            if debug_llm_prompts and llm_prompts:
                data_err2 = {
                    "llm_prompts": llm_prompts,
                    "rewritten": rewritten,
                    "rewrite_latency_ms": rewrite_ms,
                }
            return ToolResult(
                success=False,
                data=data_err2,
                error="RAG 生成不确定/为空",
                error_code="RAG_GENERATE_UNCERTAIN",
                error_stage="rag.generate",
                latency_ms=_elapsed_ms(started_at),
            )

        out: dict[str, Any] = {
            "answer": answer,
            "hits": hits,
            "rewritten": rewritten,
            "rewrite_latency_ms": rewrite_ms,
        }
        if debug_llm_prompts and llm_prompts:
            out["llm_prompts"] = llm_prompts
        return ToolResult(success=True, data=out, latency_ms=_elapsed_ms(started_at))
    except asyncio.TimeoutError:
        return ToolResult(
            success=False,
            data=None,
            error="RAG 超时",
            error_code="LLM_API_TIMEOUT",
            error_stage="llm.call",
            latency_ms=_elapsed_ms(started_at),
        )
    except Exception as exc:  # noqa: BLE001
        return ToolResult(
            success=False,
            data=None,
            error=str(exc),
            error_code=_sql_error_code_from_message(str(exc))
            if "sql" in str(exc).lower()
            else "UNKNOWN",
            error_stage="rag.tool",
            latency_ms=_elapsed_ms(started_at),
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


async def text2sql_execute(
    query: str,
    *,
    history: list[dict[str, Any]] | None = None,
    debug_llm_prompts: bool = False,
) -> ToolResult:
    started_at = time.perf_counter()
    hist = history or []
    dialogue_ctx = history_to_rewrite_block(hist)
    llm_prompts: list[dict[str, Any]] = []
    try:
        store = get_text2sql_store()
        topk = int(os.getenv("TEXT2SQL_RETRIEVE_TOPK", "6"))
        retrieve_q = _text2sql_retrieve_query(query, hist)
        retrieved = store.search(retrieve_q, top_k=topk)

        api_key = os.getenv("SILICONFLOW_API_KEY", "").strip()
        oai = OpenAI(api_key=api_key, base_url=siliconflow_base())
        chat_model = _pick_chat_model()

        sql_prompt = build_sql_prompt(query, retrieved, dialogue_context=dialogue_ctx or None)
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
        try:
            sql_raw = await asyncio.to_thread(
                lambda: llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
            )
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            return ToolResult(
                success=False,
                data=None,
                error=msg,
                error_code=_sql_error_code_from_message(msg),
                error_stage="text2sql.generate",
                latency_ms=_elapsed_ms(started_at),
            )

        sql_raw = (sql_raw or "").strip()
        if not sql_raw:
            return ToolResult(
                success=False,
                data=None,
                error="SQL 生成为空",
                error_code="SQL_GEN_EMPTY",
                error_stage="text2sql.generate",
                latency_ms=_elapsed_ms(started_at),
            )

        try:
            sql = validate_sql_readonly(sql_raw)
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            return ToolResult(
                success=False,
                data=None,
                error=msg,
                error_code=_sql_error_code_from_message(msg) if "SQL_GEN" in msg else "SQL_GEN_SYNTAX",
                error_stage="text2sql.validate",
                latency_ms=_elapsed_ms(started_at),
            )

        try:
            columns, rows = await asyncio.to_thread(
                lambda: execute_select_sql(
                    sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200"))
                )
            )
        except Exception as exc:  # noqa: BLE001
            msg = str(exc)
            return ToolResult(
                success=False,
                data=None,
                error=msg,
                error_code=_sql_error_code_from_message(msg),
                error_stage="text2sql.execute",
                latency_ms=_elapsed_ms(started_at),
            )

        if not rows:
            return ToolResult(
                success=False,
                data=None,
                error="SQL 无数据",
                error_code="SQL_EXEC_NO_DATA",
                error_stage="text2sql.execute",
                latency_ms=_elapsed_ms(started_at),
            )

        # summarize
        api_key2 = os.getenv("SILICONFLOW_API_KEY", "").strip()
        oai2 = OpenAI(api_key=api_key2, base_url=siliconflow_base())
        sum_prompt = build_summary_prompt(query, sql, columns, rows)
        if debug_llm_prompts:
            llm_prompts.append(
                {
                    "phase": "text2sql_summary",
                    "model": chat_model,
                    "messages": [
                        {"role": "system", "content": _T2SQL_GEN_SYSTEM},
                        {"role": "user", "content": sum_prompt},
                    ],
                }
            )
        try:
            answer = await asyncio.to_thread(
                lambda: llm_summarize(oai=oai2, model=chat_model, prompt=sum_prompt)
            )
        except Exception as exc:  # noqa: BLE001
            # summarize 失败但仍可降级为“查到数据行数”
            _ = exc
            answer = f"查询返回 {len(rows)} 行结果。"

        out: dict[str, Any] = {"answer": answer, "sql": sql, "columns": columns, "rows": rows}
        if debug_llm_prompts and llm_prompts:
            out["llm_prompts"] = llm_prompts
        return ToolResult(success=True, data=out, latency_ms=_elapsed_ms(started_at))
    except asyncio.TimeoutError:
        return ToolResult(
            success=False,
            data=None,
            error="Text2SQL 超时",
            error_code="LLM_API_TIMEOUT",
            error_stage="llm.call",
            latency_ms=_elapsed_ms(started_at),
        )
    except Exception as exc:  # noqa: BLE001
        msg = str(exc)
        return ToolResult(
            success=False,
            data=None,
            error=msg,
            error_code=_sql_error_code_from_message(msg),
            error_stage="text2sql.tool",
            latency_ms=_elapsed_ms(started_at),
        )


async def direct_answer_execute(
    query: str,
    *,
    history: list[dict[str, Any]] | None = None,
    debug_llm_prompts: bool = False,
) -> ToolResult:
    started_at = time.perf_counter()
    _ = history
    try:
        oai = openai_siliconflow_client()
        chat_model = _pick_chat_model()

        system = "你是一个中文助手。请直接回答用户问题。"
        user = query
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]

        def _sync_generate() -> str:
            res = oai.chat.completions.create(
                model=chat_model,
                messages=msgs,
                temperature=0.7,
                stream=False,
            )
            return (res.choices[0].message.content or "").strip()

        answer = await asyncio.to_thread(_sync_generate)
        if not answer:
            return ToolResult(
                success=False,
                data=None,
                error="direct answer 为空",
                error_code="UNKNOWN",
                error_stage="direct_answer.generate",
                latency_ms=_elapsed_ms(started_at),
            )
        out: dict[str, Any] = {"answer": answer}
        if debug_llm_prompts:
            out["llm_prompts"] = [{"phase": "direct_answer", "model": chat_model, "messages": msgs}]
        return ToolResult(success=True, data=out, latency_ms=_elapsed_ms(started_at))
    except asyncio.TimeoutError:
        return ToolResult(
            success=False,
            data=None,
            error="DirectAnswer 超时",
            error_code="LLM_API_TIMEOUT",
            error_stage="llm.call",
            latency_ms=_elapsed_ms(started_at),
        )
    except Exception as exc:  # noqa: BLE001
        return ToolResult(
            success=False,
            data=None,
            error=str(exc),
            error_code="UNKNOWN",
            error_stage="direct_answer.tool",
            latency_ms=_elapsed_ms(started_at),
        )


def get_tool_registry() -> ToolRegistry:
    # 懒加载注册：避免导入即执行重载（对单测更友好）
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="rag_search",
            description="从文档库中检索信息，适合概念解释与非结构化内容问题。",
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "用户问题"}},
                "required": ["query"],
            },
            execute=rag_search_execute,
        )
    )
    registry.register(
        Tool(
            name="text2sql_query",
            description=(
                "执行数据库查询，获取结构化数据结果。适合以下场景：\n"
                "- 用户要求查数据、统计数据、计算金额（如'有多少条'、'总和多少'、'排名第几'）\n"
                "- 用户问具体数值（如'昨天销售额是多少'）\n"
                "- 需要时间趋势、分组汇总、排序排名\n"
                "不适合：解释 SQL 语法、教用户怎么写 SQL、概念解释"
            ),
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "自然语言查询"}},
                "required": ["query"],
            },
            execute=text2sql_execute,
        )
    )
    registry.register(
        Tool(
            name="direct_answer",
            description="无需检索或查库，直接用 LLM 生成回答。",
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "用户问题"}},
                "required": ["query"],
            },
            execute=direct_answer_execute,
        )
    )
    return registry


def tool_mode_map() -> dict[ToolName, str]:
    return {"rag_search": "rag", "text2sql_query": "text2sql", "direct_answer": "no_data"}

