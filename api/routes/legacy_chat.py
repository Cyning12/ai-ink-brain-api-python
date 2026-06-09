"""Legacy chat 路由 handlers（从 api/index.py 下沉）。"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from typing import Any
from urllib.parse import quote

from fastapi import BackgroundTasks, Header, HTTPException, Query, Request
from fastapi.responses import JSONResponse, StreamingResponse
from openai import OpenAI

from supabase import create_client

from ..chatbi_circuit_breaker import CircuitBreakerOpenError
from ..chatbi_principal import (
    resolve_chatbi_from_plain_token,
)
from ..database_manager import SupabaseManager
from ..hybrid_fusion import RRF_K, fuse_hits_rrf
from ..keyword_fallback import (
    KeywordFallbackConfig,
    compare_anchor_tokens,
    run_keyword_fallback,
)
from ..query_rewrite import rewrite_query_with_history
from ..rag_embedding_guard import ensure_embedding_alignment
from ..rag_env import (
    content_default_year,
    llm_execute_with_circuit_breaker,
    max_x_sources_header_chars,
    pick_supabase_service_key,
    pick_supabase_url,
    rag_debug_enabled,
    siliconflow_api_key_optional,
    siliconflow_base,
    siliconflow_chat_model,
    siliconflow_embedding_dimensions,
    siliconflow_embedding_model,
)
from ..rag_logging import (
    build_rag_match_meta,
    build_retrieved_context_for_log,
    summarize_hits_brief,
)
from ..rag_recall_tools import keyword_query_text_with_i18n_meta
from ..rag_shared import (
    _extract_title_from_context,
    _fetch_keyword_hits_for_fallback,
    _short,
    build_sources_payload,
    fetch_keyword_hits,
    parse_match_threshold,
)

MATCH_COUNT = 10
CONTEXT_MAX_CHARS = 6000

SOURCES_JSON_SEPARATOR = "---RAG_SOURCES_JSON---"


def _rag_log(msg: str) -> None:
    if rag_debug_enabled():
        print(f"[rag-debug] {msg}", flush=True)


def _filename_title_hints(year: int, month: int, day: int) -> list[str]:
    return list(
        {
            f"{year}-{month}-{day}.md",
            f"{year}-{month:02d}-{day:02d}.md",
            f"{year}-{month}-{day:02d}.md",
            f"{year}-{month:02d}-{day}.md",
        }
    )


def _collect_date_hints(text: str) -> list[str]:
    hints: set[str] = set()

    for m in re.finditer(r"\b(20\d{2})[-/.](\d{1,2})[-/.](\d{1,2})\b", text):
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        for h in _filename_title_hints(y, mo, d):
            hints.add(h)

    for m in re.finditer(r"(?<![\d])(\d{2})[-/](\d{1,2})[-/](\d{1,2})(?![\d])", text):
        yy, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        y = 2000 + yy
        for h in _filename_title_hints(y, mo, d):
            hints.add(h)

    for m in re.finditer(r"(?<![\d])(\d{1,2})[-/](\d{1,2})(?![\d])", text):
        mo, d = int(m.group(1)), int(m.group(2))
        for h in _filename_title_hints(content_default_year(), mo, d):
            hints.add(h)

    return sorted(hints)


def augment_query_for_embedding(user_query: str) -> str:
    hints = _collect_date_hints(user_query)
    if not hints:
        return user_query
    anchor_block = "\n".join(f"TitleAnchor: {h}" for h in hints)
    return f"{user_query}\n\n{anchor_block}"


def _hint_to_slug(hint: str) -> str:
    h = hint.strip()
    lower = h.lower()
    if lower.endswith(".md"):
        return h[:-3]
    if lower.endswith(".mdx"):
        return h[:-4]
    return h


def _row_chunk_index(row: dict[str, Any]) -> int:
    m = row.get("metadata")
    if isinstance(m, dict):
        ci = m.get("chunk_index")
        if isinstance(ci, int):
            return ci
        try:
            return int(ci)  # type: ignore[arg-type]
        except (TypeError, ValueError):
            pass
    return 0


def fetch_date_anchor_hits(sb: Any, date_hints: list[str]) -> list[dict[str, Any]]:
    if not date_hints:
        return []
    seen_ids: set[Any] = set()
    collected: list[dict[str, Any]] = []

    for hint in sorted(set(date_hints))[:8]:
        slug = _hint_to_slug(hint)
        rows: list[dict[str, Any]] = []
        if slug:
            try:
                res = (
                    sb.table("documents")
                    .select("id, content, metadata")
                    .eq("metadata->>slug", slug)
                    .limit(48)
                    .execute()
                )
                data = res.data if isinstance(res.data, list) else []
                rows.extend([r for r in data if isinstance(r, dict)])
            except Exception as exc:  # noqa: BLE001
                _rag_log(f"anchor eq slug={slug!r}: {exc!s}")

        if not rows and hint:
            try:
                res = (
                    sb.table("documents")
                    .select("id, content, metadata")
                    .ilike("content", f"%Title: {hint}%")
                    .limit(24)
                    .execute()
                )
                data = res.data if isinstance(res.data, list) else []
                rows.extend([r for r in data if isinstance(r, dict)])
            except Exception as exc:  # noqa: BLE001
                _rag_log(f"anchor ilike Title hint={hint!r}: {exc!s}")

        rows.sort(key=_row_chunk_index)
        for r in rows:
            rid = r.get("id")
            if rid is None or rid in seen_ids:
                continue
            seen_ids.add(rid)
            collected.append(
                {
                    "id": rid,
                    "content": r.get("content") if isinstance(r.get("content"), str) else "",
                    "metadata": r.get("metadata") if isinstance(r.get("metadata"), dict) else {},
                    "similarity": 1.0,
                }
            )

    return collected


def merge_hits_anchors_first(
    anchor_hits: list[dict[str, Any]],
    vector_hits: list[dict[str, Any]],
    max_total: int = 22,
) -> list[dict[str, Any]]:
    seen: set[Any] = set()
    out: list[dict[str, Any]] = []
    for h in anchor_hits:
        hid = h.get("id")
        if hid is not None:
            if hid in seen:
                continue
            seen.add(hid)
        out.append(h)
        if len(out) >= max_total:
            return out
    for h in vector_hits:
        hid = h.get("id")
        if hid is not None:
            if hid in seen:
                continue
            seen.add(hid)
        out.append(h)
        if len(out) >= max_total:
            break
    return out


def message_to_text(message: dict[str, Any]) -> str:
    if not isinstance(message, dict):
        return ""
    c = message.get("content")
    if isinstance(c, str):
        return c
    parts = message.get("parts")
    if isinstance(parts, list):
        chunks: list[str] = []
        for p in parts:
            if not isinstance(p, dict):
                continue
            if p.get("type") == "text" and isinstance(p.get("text"), str):
                chunks.append(p["text"])
        return "".join(chunks)
    return ""


def last_user_text(messages: list[dict[str, Any]]) -> str | None:
    for m in reversed(messages):
        if not isinstance(m, dict) or m.get("role") != "user":
            continue
        t = message_to_text(m).strip()
        if t:
            return t
    return None


def build_system_prompt(context: str) -> str:
    rules = (
        "你必须优先查找并依据以「[Document Context]」标记的片段作答。\n"
        "若某段以「Title: 某文件名.md」形式出现，例如「Title: 2026-4-09.md」，"
        "即表示这是该日期的笔记正文摘要（文件名中年-月-日对应公历日期）。\n"
        "当上下文中存在与用户提到日期相符的 Title 时，你必须在回答开头明确说明“已找到该日记/文档”，并优先引用其内容；\n"
        "不要被后续语义检索到的其他日期内容干扰。\n"
        "请综合多个片段回答；若上下文仍不足，请明确说明。\n"
    )
    body = context.strip() or "（无检索命中）"
    return f"{rules}\n【检索到的文档片段】\n{body}"


def _try_chatbi_bearer_plain_sync(plain: str) -> bool:
    """同步版本：尝试将明文当作 ChatBI DB token 校验。成功返回 True；`bad_hash` 返回 False（回退 Ink）；其它 401 原样抛出。"""
    t = plain.strip()
    if not t:
        return False
    try:
        resolve_chatbi_from_plain_token(t)
        return True
    except HTTPException as e:
        if e.status_code != 401:
            raise
        det = e.detail if isinstance(e.detail, dict) else {}
        if det.get("reason") == "bad_hash":
            return False
        raise


async def _require_rag_history_auth(
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
    x_chatbi_access_token: str | None,
) -> None:
    """ChatBI：`X-ChatBI-Access-Token` 或 `Authorization: Bearer <明文>`；否则 Ink admin / API_KEY。"""
    if (x_chatbi_access_token or "").strip():
        await asyncio.to_thread(resolve_chatbi_from_plain_token, (x_chatbi_access_token or "").strip())
        return
    auth = (authorization or "").strip()
    bearer_plain = ""
    if auth.lower().startswith("bearer "):
        bearer_plain = auth[7:].strip()
    if bearer_plain:
        ok = await asyncio.to_thread(_try_chatbi_bearer_plain_sync, bearer_plain)
        if ok:
            return
    # Fallback to require_auth logic from index.py
    from ..index import _require_auth

    _require_auth(authorization, x_blog_admin_token, x_admin_token)


async def chat(
    request: Request,
    background_tasks: BackgroundTasks,
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
) -> StreamingResponse:
    from ..index import _require_auth

    _require_auth(authorization, x_blog_admin_token, x_admin_token)

    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc

    messages_raw = body.get("messages")
    if not isinstance(messages_raw, list):
        raise HTTPException(status_code=400, detail="Missing messages array")
    messages: list[dict[str, Any]] = [m for m in messages_raw if isinstance(m, dict)]

    query = last_user_text(messages)
    if not query:
        raise HTTPException(status_code=400, detail="Missing user message")

    session_id_raw = body.get("session_id")
    if not isinstance(session_id_raw, str) or not session_id_raw.strip():
        raise HTTPException(status_code=400, detail="Missing session_id")
    session_id = session_id_raw.strip()

    api_key = siliconflow_api_key_optional()
    if not api_key:
        raise HTTPException(status_code=500, detail="Missing SILICONFLOW_API_KEY")

    supabase_url = pick_supabase_url()
    supabase_key = pick_supabase_service_key()
    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=500,
            detail=(
                "缺少 Supabase 配置：请设置 NEXT_PUBLIC_SUPABASE_URL 或 SUPABASE_URL，以及 "
                "SUPABASE_SERVICE_ROLE_KEY 或 SUPABASE_SERVICE_KEY。"
            ),
        )

    sbm = SupabaseManager(url=supabase_url, service_key=supabase_key)

    t0 = time.perf_counter()
    try:
        history = await sbm.get_chat_history(session_id=session_id, limit=5)
    except Exception as exc:  # noqa: BLE001
        _rag_log(f"get_chat_history failed: {exc!s}")
        history = []
    t_history_ms = int((time.perf_counter() - t0) * 1000)

    date_hints = _collect_date_hints(query)
    oai = OpenAI(api_key=api_key, base_url=siliconflow_base())

    t1 = time.perf_counter()
    try:
        rewritten_query = await rewrite_query_with_history(
            oai=oai,
            query=query,
            history=history,
            chat_model=siliconflow_chat_model(),
        )
    except Exception as exc:  # noqa: BLE001
        _rag_log(f"rewrite_query failed: {exc!s}")
        rewritten_query = query
    t_rewrite_ms = int((time.perf_counter() - t1) * 1000)

    embed_input = augment_query_for_embedding(rewritten_query)
    match_threshold = parse_match_threshold()

    _rag_log(
        f"last_user_query(len={len(query)})={_short(query, 500)!r} "
        f"| date_hints={date_hints} | DEFAULT_YEAR={content_default_year()}"
    )

    vec: list[float] | None = None
    embedding_error: str | None = None
    t2 = time.perf_counter()
    try:
        emb_model = siliconflow_embedding_model()
        emb_kw: dict[str, Any] = {
            "model": emb_model,
            "input": [embed_input],
        }
        if "Qwen3-Embedding" in emb_model:
            emb_kw["dimensions"] = siliconflow_embedding_dimensions()
        emb_res = llm_execute_with_circuit_breaker(lambda: oai.embeddings.create(**emb_kw))
        vec = list(emb_res.data[0].embedding)
    except CircuitBreakerOpenError as exc:
        raise HTTPException(status_code=503, detail=exc.to_error_body()) from exc
    except Exception as exc:  # noqa: BLE001
        embedding_error = str(exc)
        _rag_log(f"embedding failed, fallback to keyword-only: {embedding_error}")
        vec = None
    t_embedding_ms = int((time.perf_counter() - t2) * 1000)

    hits: list[dict[str, Any]] = []
    vector_hits: list[dict[str, Any]] = []
    keyword_hits: list[dict[str, Any]] = []
    keyword_hits_raw_for_metrics: list[dict[str, Any]] = []
    keyword_hits_rw_for_metrics: list[dict[str, Any]] = []
    query_compare_meta: dict[str, Any] | None = None
    keyword_fallback: Any = None
    date_anchor_count = 0
    i18n_expand_raw: dict[str, Any] | None = None
    i18n_expand_rw: dict[str, Any] | None = None

    t3 = time.perf_counter()
    try:
        sb = create_client(supabase_url, supabase_key)

        alignment = ensure_embedding_alignment(sb)
        if not alignment.ok:
            raise HTTPException(
                status_code=503,
                detail={
                    "code": "RAG_EMBEDDING_MODEL_MISMATCH",
                    "message": alignment.message,
                    "runtime_model": alignment.runtime_model,
                    "stored_models": list(alignment.stored_models),
                },
            )

        if vec is not None:
            rpc = sb.rpc(
                "match_documents",
                {
                    "query_embedding": vec,
                    "match_count": MATCH_COUNT,
                    "match_threshold": match_threshold,
                },
            )
            raw = rpc.execute().data
            if isinstance(raw, list):
                vector_hits = [h for h in raw if isinstance(h, dict)]
        else:
            vector_hits = []

        kw_qt_raw, i18n_expand_raw = keyword_query_text_with_i18n_meta(query)
        kw_qt_rw, i18n_expand_rw = keyword_query_text_with_i18n_meta(rewritten_query)
        keyword_hits_raw_for_metrics = fetch_keyword_hits(sb, kw_qt_raw, match_count=12)
        keyword_hits_rw_for_metrics = fetch_keyword_hits(sb, kw_qt_rw, match_count=12)

        def _top1_keyword_score(rows: list[dict[str, Any]]) -> float | None:
            if not rows:
                return None
            v = rows[0].get("score")
            try:
                return float(v) if v is not None else None
            except Exception:  # noqa: BLE001
                return None

        entity_cmp = compare_anchor_tokens(query, rewritten_query)
        query_compare_meta = {
            "query_raw": query,
            "query_rewrite": rewritten_query,
            "keyword_query_text_raw": kw_qt_raw,
            "keyword_query_text_rewrite": kw_qt_rw,
            "recall_raw_count": len(keyword_hits_raw_for_metrics),
            "recall_rw_count": len(keyword_hits_rw_for_metrics),
            "recall_raw_top1_score": _top1_keyword_score(keyword_hits_raw_for_metrics),
            "recall_rw_top1_score": _top1_keyword_score(keyword_hits_rw_for_metrics),
            "is_key_entity_lost": bool(entity_cmp.get("is_key_entity_lost")),
            "key_entities": entity_cmp,
            "score_type": "fts_score",
        }

        keyword_hits = keyword_hits_rw_for_metrics
        cfg_kw_fb = KeywordFallbackConfig.from_env()
        keyword_hits, keyword_fallback = run_keyword_fallback(
            sb=sb,
            raw_query=query,
            cfg=cfg_kw_fb,
            fetch_keyword_hits=_fetch_keyword_hits_for_fallback,
            initial_hits=keyword_hits,
        )

        fused_hits = fuse_hits_rrf(vector_hits, keyword_hits, max_total=22)
        hits = fused_hits

        if rag_debug_enabled():
            fb = keyword_fallback
            _rag_log(
                "retrieve_summary "
                f"raw_query={_short(query, 200)!r} "
                f"rewritten_query={_short(rewritten_query, 260)!r} "
                f"vec={'ok' if vec is not None else 'none'} "
                f"vector_hits={len(vector_hits)} "
                f"keyword_hits={len(keyword_hits)} "
                f"fallback={'none' if not fb else (fb.query_used or 'unknown')}"
            )
            if query_compare_meta:
                _rag_log(
                    "query_compare "
                    f"raw_count={query_compare_meta.get('recall_raw_count')} "
                    f"rw_count={query_compare_meta.get('recall_rw_count')} "
                    f"raw_top1={query_compare_meta.get('recall_raw_top1_score')!r} "
                    f"rw_top1={query_compare_meta.get('recall_rw_top1_score')!r} "
                    f"is_key_entity_lost={query_compare_meta.get('is_key_entity_lost')} "
                    f"missing={(query_compare_meta.get('key_entities') or {}).get('missing')!r}"
                )
            if fb and fb.triggered:
                _rag_log(
                    "keyword_fallback_detail "
                    f"reason={fb.reason!r} query_used={fb.query_used!r} "
                    f"query_text={_short(fb.query_text or '', 220)!r} "
                    f"anchor_tokens={fb.anchor_tokens!r} "
                    f"{fb.initial_hits}->{fb.final_hits} latency_ms={fb.latency_ms}"
                )
            _rag_log(f"top_hits={summarize_hits_brief(hits, top_n=5)!r}")

        if date_hints:
            ah = fetch_date_anchor_hits(sb, date_hints)
            if ah:
                date_anchor_count = len(ah)
                print(
                    f"[rag] date_anchor_injected={date_anchor_count} "
                    f"vector_only={len(vector_hits)} keyword_only={len(keyword_hits)} → merged",
                    flush=True,
                )
                hits = merge_hits_anchors_first(ah, hits, max_total=22)

        scores = [round(float(h.get("fused_score", 0)), 6) for h in hits]
        print(
            f"[rag] hybrid vector_count={len(vector_hits)} keyword_count={len(keyword_hits)} "
            f"match_count={MATCH_COUNT} threshold={match_threshold!s} fused_scores={scores}",
            flush=True,
        )

        if rag_debug_enabled():
            titles = []
            for h in hits:
                c = h.get("content") if isinstance(h.get("content"), str) else ""
                t = _extract_title_from_context(c)
                if t:
                    titles.append(t)
            if titles:
                _rag_log(f"hits Title 列表（去重前，最多24）：{titles[:24]!r}")

    except HTTPException:
        raise
    except Exception as exc:  # noqa: BLE001
        print(f"[rag] match_documents error: {exc!s}", flush=True)
        hits = []
        vector_hits = []
        keyword_hits = []
    t_retrieve_ms = int((time.perf_counter() - t3) * 1000)

    context_parts: list[str] = []
    for i, h in enumerate(hits):
        content = h.get("content")
        if not isinstance(content, str):
            continue
        meta = h.get("metadata") if isinstance(h.get("metadata"), dict) else {}
        slug = meta.get("slug") if isinstance(meta.get("slug"), str) else ""
        category = meta.get("category") if isinstance(meta.get("category"), str) else ""
        head_bits = [f"slug={slug}" if slug else "", f"category={category}" if category else ""]
        head = " ".join(b for b in head_bits if b)
        prefix = f"[#{i + 1}"
        if head:
            prefix += f" {head}"
        prefix += "]\n"
        context_parts.append(prefix + content)

    context_body = "\n\n---\n\n".join(context_parts)
    if date_anchor_count:
        context_body = (
            "【以下前列片段已按用户问题中的日期与库中 slug/Title 对齐，请优先据此回答；"
            "其后为语义检索补充，可能含主题相近但日期不同的内容。】\n\n---\n\n"
            + context_body
        )
    context = context_body[:CONTEXT_MAX_CHARS]

    system_content = build_system_prompt(context)

    chat_messages: list[dict[str, str]] = [{"role": "system", "content": system_content}]
    for m in messages:
        role = m.get("role")
        if role not in ("user", "assistant", "system"):
            continue
        text = message_to_text(m).strip()
        if not text:
            continue
        chat_messages.append({"role": str(role), "content": text})

    response_chunks: list[str] = []
    gen_started_at = time.perf_counter()
    gen_finished_ms: int | None = None
    sources_payload = build_sources_payload(hits, top_k=5)
    sources_header: str | None = None
    try:
        sources_header = quote(
            json.dumps(sources_payload, ensure_ascii=False, separators=(",", ":")),
            safe="",
        )
        max_sources_chars = max_x_sources_header_chars()
        if sources_header and len(sources_header) > max_sources_chars:
            _rag_log(
                "x-sources header too large: "
                f"{len(sources_header)}>{max_sources_chars}; "
                "will omit header and rely on stream tail JSON"
            )
            sources_header = None
    except Exception as exc:  # noqa: BLE001
        _rag_log(f"build x-sources header failed: {exc!s}")
        sources_header = None

    def token_stream():
        nonlocal gen_finished_ms
        try:
            stream = oai.chat.completions.create(
                model=siliconflow_chat_model(),
                messages=chat_messages,
                temperature=0.2,
                stream=True,
            )
            for chunk in stream:
                choice = chunk.choices[0] if chunk.choices else None
                if not choice or not choice.delta or not choice.delta.content:
                    continue
                piece = choice.delta.content
                response_chunks.append(piece)
                yield piece.encode("utf-8")
        except Exception as exc:  # noqa: BLE001
            yield f"\n[错误] 对话生成失败: {exc!s}".encode()
        finally:
            if sys.exc_info()[0] is GeneratorExit:
                return  # noqa: B012
            gen_finished_ms = int((time.perf_counter() - gen_started_at) * 1000)
            try:
                blob = json.dumps(sources_payload, ensure_ascii=False, separators=(",", ":"))
                tail = f"\n\n{SOURCES_JSON_SEPARATOR}\n{blob}\n"
                yield tail.encode("utf-8")
            except Exception as exc:  # noqa: BLE001
                _rag_log(f"build sources json failed: {exc!s}")

    async def save_log_after_stream() -> None:
        response_text = "".join(response_chunks).strip()
        kw_qt_used, _i18n_meta_used = keyword_query_text_with_i18n_meta(rewritten_query)
        meta: dict[str, Any] = {
            "latency_ms": {
                "history": t_history_ms,
                "rewrite": t_rewrite_ms,
                "embedding": t_embedding_ms,
                "retrieve": t_retrieve_ms,
                "generate": gen_finished_ms,
            },
            "models": {
                "embedding": siliconflow_embedding_model(),
                "chat": siliconflow_chat_model(),
            },
            "match": build_rag_match_meta(
                match_count=MATCH_COUNT,
                match_threshold=match_threshold,
                date_anchor_count=date_anchor_count,
                rrf_k=RRF_K,
                vector_hits_count=len(vector_hits),
                keyword_hits_count=len(keyword_hits),
                embedding_error=embedding_error,
                keyword_fallback=keyword_fallback,
                vec_available=vec is not None,
                query_compare=query_compare_meta,
            ),
        }
        if isinstance(meta.get("match"), dict):
            meta["match"]["i18n_expand"] = {
                "raw": i18n_expand_raw,
                "rewrite": i18n_expand_rw,
                "used": "rewrite",
                "used_query_text": kw_qt_used,
            }
        payload: dict[str, Any] = {
            "session_id": session_id,
            "query": query,
            "rewritten_query": rewritten_query,
            "retrieved_context": build_retrieved_context_for_log(hits, limit=22),
            "response": response_text,
            "metadata": meta,
        }
        try:
            await sbm.save_debug_log(payload)
        except Exception as exc:  # noqa: BLE001
            _rag_log(f"save_debug_log failed: {exc!s}")

    background_tasks.add_task(save_log_after_stream)
    headers: dict[str, str] = {}
    if sources_header:
        headers["x-sources"] = sources_header
    return StreamingResponse(
        token_stream(),
        media_type="text/plain; charset=utf-8",
        background=background_tasks,
        headers=headers,
    )


async def chat_history(
    session_id: str = Query(..., description="与 POST /api/py/chat 相同的 session_id"),
    limit: int = Query(100, ge=1, le=200, description="最多返回最近多少轮完整问答"),
    authorization: str | None = Header(default=None),
    x_blog_admin_token: str | None = Header(default=None, alias="x-blog-admin-token"),
    x_admin_token: str | None = Header(default=None, alias="x-admin-token"),
    x_chatbi_access_token: str | None = Header(default=None, alias="x-chatbi-access-token"),
) -> dict[str, Any]:
    await _require_rag_history_auth(
        authorization=authorization,
        x_blog_admin_token=x_blog_admin_token,
        x_admin_token=x_admin_token,
        x_chatbi_access_token=x_chatbi_access_token,
    )

    sid = session_id.strip()
    if not sid:
        raise HTTPException(status_code=400, detail="Missing session_id")

    supabase_url = pick_supabase_url()
    supabase_key = pick_supabase_service_key()
    if not supabase_url or not supabase_key:
        raise HTTPException(
            status_code=500,
            detail=(
                "缺少 Supabase 配置：请设置 NEXT_PUBLIC_SUPABASE_URL 或 SUPABASE_URL，以及 "
                "SUPABASE_SERVICE_ROLE_KEY 或 SUPABASE_SERVICE_KEY。"
            ),
        )

    sbm = SupabaseManager(url=supabase_url, service_key=supabase_key)
    try:
        turns = await sbm.list_session_turns(sid, limit=limit)
    except asyncio.CancelledError:
        raise HTTPException(status_code=499, detail="Client Closed Request") from None
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(
            status_code=500,
            detail={"error_type": "DATABASE_DISCONNECT", "message": str(exc)},
        ) from exc

    messages: list[dict[str, Any]] = []
    for row in turns:
        q = row.get("query") if isinstance(row.get("query"), str) else ""
        a = row.get("response") if isinstance(row.get("response"), str) else ""
        created_at = row.get("created_at")
        if q.strip():
            m: dict[str, Any] = {"role": "user", "content": q.strip()}
            if created_at is not None:
                m["created_at"] = created_at
            messages.append(m)
        if a.strip():
            m2: dict[str, Any] = {"role": "assistant", "content": a.strip()}
            if created_at is not None:
                m2["created_at"] = created_at
            messages.append(m2)

    return {
        "ok": True,
        "session_id": sid,
        "messages": messages,
    }


def chat_suggested_questions() -> JSONResponse:
    """返回推荐问法列表，供前端展示（不再本地写死）。"""
    return JSONResponse(
        {
            "ok": True,
            "questions": [
                "《AI 编程可闭环协作》卷三讲什么？Harness 和签收是什么？",
                "Tech Graph 是什么",
                "冷/温/热 和 架构三层 区别？",
                "简单介绍下刘新宁",
                "AI Ink Brain 的架构是怎样的",
                "统计 agent_info 表里有多少条数据",
                "按日期统计最近 7 天的订单数量",
            ],
        }
    )
