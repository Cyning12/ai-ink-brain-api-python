from __future__ import annotations

import hmac
import os
import re
import time
import uuid
from typing import Any, Literal

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

from .hybrid_fusion import RRF_K, fuse_hits_rrf
from .query_rewrite import rewrite_query_with_history
from .rag_env import (
    admin_secret,
    embedding_kwargs_for_inputs,
    openai_siliconflow_client,
    siliconflow_base,
    supabase_client,
)
from .text2sql_core import (
    build_sql_prompt,
    build_summary_prompt,
    execute_select_sql,
    is_text2sql_intent,
    llm_generate_sql,
    llm_summarize,
    validate_sql_readonly,
)
from .text2sql_store import get_text2sql_store


PreferMode = Literal["auto", "rag", "text2sql"]


def _require_unified_auth(authorization: str | None, x_blog_admin_token: str | None, x_admin_token: str | None) -> None:
    expected_admin = (admin_secret() or "").strip() or None
    expected_api = (os.getenv("API_KEY") or "").strip() or None
    if not expected_admin and not expected_api:
        raise HTTPException(status_code=500, detail="未配置 NEXT_PUBLIC_ADMIN_SECRET / CHAT_API_SECRET 或 API_KEY")

    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif x_blog_admin_token:
        token = x_blog_admin_token.strip()
    elif x_admin_token:
        token = x_admin_token.strip()

    def _match(expected: str | None) -> bool:
        if not expected:
            return False
        if len(token) != len(expected):
            return False
        return hmac.compare_digest(token.encode("utf-8"), expected.encode("utf-8"))

    if not (_match(expected_admin) or _match(expected_api)):
        raise HTTPException(status_code=401, detail="Unauthorized")


def _now_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _event(*, typ: str, started_at: float, step_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"type": typ, "ts": _now_ms(started_at), "step_id": step_id, "payload": payload}


def _parse_prefer(raw: object) -> PreferMode:
    if not isinstance(raw, str):
        return "auto"
    v = raw.strip().lower()
    if v in ("rag", "text2sql", "auto"):
        return v  # type: ignore[return-value]
    return "auto"


def _parse_match_threshold() -> float | None:
    raw = os.getenv("RAG_MATCH_THRESHOLD", "").strip()
    if not raw:
        return 0.3
    if raw.lower() in ("none", "null", "off"):
        return None
    try:
        v = float(raw)
    except ValueError:
        return 0.3
    if v > 1.0:
        return None
    if v < 0:
        return 0.3
    return v


def _strip_doc_context_prefix(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return ""
    m = re.search(r"(?m)^Content:\s*", t)
    if m:
        return t[m.end() :].strip()
    t = re.sub(r"(?m)^\[Document Context\]\s*$", "", t).strip()
    t = re.sub(r"(?m)^Title:\s*.*$", "", t).strip()
    t = re.sub(r"(?m)^Date:\s*.*$", "", t).strip()
    t = re.sub(r"(?m)^Category:\s*.*$", "", t).strip()
    t = re.sub(r"(?m)^---\s*$", "", t).strip()
    return t


def _build_rag_sources_event(hits: list[dict[str, Any]], *, top_k: int = 10) -> dict[str, Any]:
    packed: list[dict[str, Any]] = []
    for h in hits[: max(1, int(top_k))]:
        meta = h.get("metadata") if isinstance(h.get("metadata"), dict) else {}
        content = h.get("content") if isinstance(h.get("content"), str) else ""
        snippet = _strip_doc_context_prefix(content).replace("\r\n", "\n").strip()
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
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> JSONResponse:
    _require_unified_auth(authorization, x_blog_admin_token, x_admin_token)

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

    started_at = time.perf_counter()
    run_id = str(uuid.uuid4())
    events: list[dict[str, Any]] = []

    def finish(*, ok: bool, mode: str) -> JSONResponse:
        return JSONResponse(
            content={"ok": ok, "run_id": run_id, "session_id": session_id, "mode": mode, "events": events}
        )

    # mode decide
    mode: Literal["rag", "text2sql"]
    if prefer == "rag":
        mode = "rag"
    elif prefer == "text2sql":
        mode = "text2sql"
    else:
        mode = "text2sql" if is_text2sql_intent(query) else "rag"

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
                _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at)})
            )
            return finish(ok=False, mode=mode)

        oai = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY", "").strip(), base_url=siliconflow_base())
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

        # generate sql
        sql_prompt = build_sql_prompt(query, retrieved)
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
        gen_err: str | None = None
        try:
            sql_raw = llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
            sql = validate_sql_readonly(sql_raw)
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
                _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at)})
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
            columns, rows = execute_select_sql(sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200")))
        except Exception as exc:  # noqa: BLE001
            exec_err = str(exc)
        t_exec_ms = int((time.perf_counter() - t2) * 1000)
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
    keyword_hits: list[dict[str, Any]] = []
    hits: list[dict[str, Any]] = []
    ret_err: str | None = None
    try:
        sb = supabase_client()
        match_threshold = _parse_match_threshold()
        match_count = int(os.getenv("RAG_MATCH_COUNT", "10"))
        if vec is not None:
            raw = (
                sb.rpc(
                    "match_documents",
                    {"query_embedding": vec, "match_count": match_count, "match_threshold": match_threshold},
                )
                .execute()
                .data
            )
            if isinstance(raw, list):
                vector_hits = [h for h in raw if isinstance(h, dict)]

        raw_kw = (
            sb.rpc("keyword_documents", {"query_text": rewritten, "match_count": 12}).execute().data
        )
        if isinstance(raw_kw, list):
            keyword_hits = [h for h in raw_kw if isinstance(h, dict)]

        hits = fuse_hits_rrf(vector_hits, keyword_hits, max_total=22)
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
                "output": {"vector_hits": len(vector_hits), "keyword_hits": len(keyword_hits), "hits": len(hits)},
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
    return finish(ok=gen_err is None, mode=mode)

