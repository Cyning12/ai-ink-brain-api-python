from __future__ import annotations

import asyncio
import os
import time
from typing import Any

from .hybrid_fusion import RRF_K, fuse_hits_rrf
from .query_rewrite import build_rewrite_llm_messages
from .rag_embedding_guard import (
    EMBEDDING_MISMATCH_ERROR_CODE,
    EmbeddingAlignment,
    ensure_embedding_alignment,
)
from .rag_env import (
    embedding_kwargs_for_inputs,
    openai_siliconflow_client,
    supabase_client,
)
from .rag_recall_tools import (
    keyword_query_text_with_i18n_meta,
    rpc_execute_with_retry,
    structured_recall_by_date,
)
from .rag_shared import parse_match_threshold
from .tool_models import ToolResult
from .tools_shared import (
    _elapsed_ms,
    _pick_chat_model,
    _rag_should_treat_as_uncertain,
    _safe_snippet,
    _sql_error_code_from_message,
)


async def _rag_retrieve(query: str, *, rewritten: str, history: list[dict[str, Any]]) -> dict[str, Any]:
    sb = supabase_client()
    alignment = ensure_embedding_alignment(sb)
    if not alignment.ok:
        return {
            "hits": [],
            "embedding_guard": alignment,
            "latency": {"retry_count": 0, "embedding_error": None, "rrf_k": RRF_K},
            "top_k": 10,
            "history": history,
        }

    oai = openai_siliconflow_client()
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
        sb, query=query, rewritten=rewritten, limit_rows=6
    ).hits

    vector_hits: list[dict[str, Any]] = []
    if vec is not None:
        vector_hits, rc_vec, err_vec = rpc_execute_with_retry(
            sb,
            "match_documents",
            {"query_embedding": vec, "match_count": match_count, "match_threshold": match_threshold},
            retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
        )
        retry_count += rc_vec
        _ = err_vec  # 仅记录，不阻断

    kw_qt_raw, _kw_meta_raw = keyword_query_text_with_i18n_meta(query)
    kw_qt_rw, _kw_meta_rw = keyword_query_text_with_i18n_meta(rewritten)

    keyword_hits_raw, rc_raw, _err_raw = rpc_execute_with_retry(
        sb,
        "keyword_documents",
        {"query_text": kw_qt_raw, "match_count": 12},
        retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
    )
    retry_count += rc_raw

    keyword_hits_rewrite, rc_rw, _err_rw = rpc_execute_with_retry(
        sb,
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
    preview_only: bool = False,
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
        guard = retrieved.get("embedding_guard")
        if isinstance(guard, EmbeddingAlignment) and not guard.ok:
            return ToolResult(
                success=False,
                data={"runtime_model": guard.runtime_model, "stored_models": list(guard.stored_models)},
                error=guard.message or "Embedding 模型与向量库不一致",
                error_code=guard.error_code or EMBEDDING_MISMATCH_ERROR_CODE,
                error_stage="rag.embedding_guard",
                latency_ms=_elapsed_ms(started_at),
            )

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

        if preview_only:
            planned_top_k = int(retrieved.get("top_k") or 10)
            headlines: list[str] = []
            for h in hits[:6]:
                if not isinstance(h, dict):
                    continue
                label = (
                    h.get("filename")
                    or h.get("title")
                    or h.get("path")
                    or h.get("url")
                    or h.get("id")
                )
                if isinstance(label, str) and label.strip():
                    headlines.append(label.strip()[:120])
            out_preview: dict[str, Any] = {
                "rewritten": rewritten,
                "planned_top_k": planned_top_k,
                "preview_headlines": headlines,
            }
            if debug_llm_prompts and llm_prompts:
                out_preview["llm_prompts"] = llm_prompts
            return ToolResult(success=True, data=out_preview, latency_ms=_elapsed_ms(started_at))

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

