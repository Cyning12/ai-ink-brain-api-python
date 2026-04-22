from __future__ import annotations

import fnmatch
import re
import time
import uuid
from typing import Any

import os

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI
from supabase import create_client

from .database_manager import SupabaseManager
from .hybrid_fusion import fuse_hits_rrf
from .query_rewrite import rewrite_query_with_history
from .rag_env import admin_secret, pick_supabase_service_key, pick_supabase_url

# 这些符号在 api.index 中定义；本模块通过运行时注入避免循环 import。
build_sources_payload: Any
_parse_match_threshold: Any
SILICONFLOW_BASE: str
SILICONFLOW_EMBEDDING_MODEL: str
SILICONFLOW_EMBEDDING_DIMENSIONS: int
SILICONFLOW_CHAT_MODEL: str
MATCH_COUNT: int
_rag_log: Any


def _require_code_api_auth(
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> None:
    """Code Query/Search 的鉴权：优先使用 API_KEY；兼容 admin_secret。"""
    expected = (os.getenv("API_KEY") or "").strip() or (admin_secret() or "").strip()
    if not expected:
        raise HTTPException(status_code=500, detail="未配置 API_KEY 或 NEXT_PUBLIC_ADMIN_SECRET / CHAT_API_SECRET")

    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif x_blog_admin_token:
        token = x_blog_admin_token.strip()
    elif x_admin_token:
        token = x_admin_token.strip()

    # constant time compare
    if len(token) != len(expected) or not __import__("hmac").compare_digest(
        token.encode("utf-8"), expected.encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Unauthorized")


def _clamp_int(v: Any, *, default: int, lo: int, hi: int) -> int:
    try:
        n = int(v) if v is not None else int(default)
    except (TypeError, ValueError):
        n = int(default)
    return max(lo, min(hi, n))


def _meta_dict(row: dict[str, Any]) -> dict[str, Any]:
    m = row.get("metadata")
    return m if isinstance(m, dict) else {}


def _chunk_from_hit(row: dict[str, Any]) -> dict[str, Any]:
    m = _meta_dict(row)
    rel = (m.get("relativePath") or m.get("relative_path") or "").strip()
    # 对外输出优先使用 relative_path（避免暴露本机绝对路径，且便于前端定位）
    fp = rel or (str(m.get("file_path") or "").strip())
    score = row.get("similarity")
    if score is None:
        score = row.get("score")
    try:
        score_f = float(score) if score is not None else 0.0
    except (TypeError, ValueError):
        score_f = 0.0
    fused = row.get("fused_score")
    try:
        fused_f = float(fused) if fused is not None else 0.0
    except (TypeError, ValueError):
        fused_f = 0.0

    cid = row.get("id")
    cid_str = str(cid) if cid is not None else str(uuid.uuid4())

    return {
        "id": cid_str,
        "content": (row.get("content") or "") if isinstance(row.get("content"), str) else str(row.get("content") or ""),
        "file_path": fp,
        "relative_path": rel or fp,
        "start_line": int(m.get("start_line") or 0),
        "end_line": int(m.get("end_line") or 0),
        "chunk_type": str(m.get("chunk_type") or ""),
        "name": str(m.get("name") or ""),
        "signature": str(m.get("signature") or ""),
        "module": str(m.get("module") or ""),
        "score": score_f,
        "fused_score": fused_f,
    }


def _passes_code_filters(row: dict[str, Any], filters: dict[str, Any] | None) -> bool:
    if not filters:
        return True
    m = _meta_dict(row)

    fp_filter = filters.get("file_path")
    if isinstance(fp_filter, str) and fp_filter.strip():
        pat = fp_filter.strip().replace("\\", "/")
        rel = str(m.get("relativePath") or m.get("relative_path") or "").replace("\\", "/")
        file_path = str(m.get("file_path") or "").replace("\\", "/")
        candidates = {rel, file_path}
        # 兼容绝对路径入库：basename / 后缀匹配
        for c in list(candidates):
            if c:
                candidates.add(c.split("/")[-1])
        if not any(fnmatch.fnmatch(c, pat) or c == pat for c in candidates if c):
            return False

    ct = filters.get("chunk_type")
    if isinstance(ct, str) and ct.strip():
        if str(m.get("chunk_type") or "") != ct.strip():
            return False

    mod = filters.get("module")
    if isinstance(mod, str) and mod.strip():
        if str(m.get("module") or "") != mod.strip():
            return False

    return True


def _boost_by_query_name(hits: list[dict[str, Any]], query_text: str) -> list[dict[str, Any]]:
    """轻量 rerank：当 query 明确包含符号名时，优先返回同名 chunk。"""
    qt = (query_text or "").strip().lower()
    if not qt:
        return hits

    boosted: list[dict[str, Any]] = []
    for h in hits:
        m = _meta_dict(h)
        name = str(m.get("name") or "").strip()
        if not name:
            boosted.append(h)
            continue

        if name.lower() in qt:
            row = dict(h)
            try:
                row["fused_score"] = float(row.get("fused_score") or 0.0) + 100.0
            except (TypeError, ValueError):
                row["fused_score"] = 100.0
            boosted.append(row)
        else:
            boosted.append(h)

    boosted.sort(key=lambda r: float(r.get("fused_score") or 0.0), reverse=True)
    return boosted


def _identifier_only_query(text: str) -> str:
    """从混合语言 query 中提取代码标识符，提升 FTS 命中率。"""
    t = (text or "").strip()
    if not t:
        return ""
    ids = re.findall(r"[A-Za-z_][A-Za-z0-9_\\.]*", t)
    # 去重但保序
    seen: set[str] = set()
    out: list[str] = []
    for x in ids:
        if x in seen:
            continue
        seen.add(x)
        out.append(x)
    return " ".join(out).strip()


def _keyword_light_query(text: str) -> str:
    """当英文自然语言包含大量停用词时，抽取关键 token 以避免 FTS AND 过严导致 0 命中。"""
    t = (text or "").strip()
    if not t:
        return ""
    toks = re.findall(r"[A-Za-z_][A-Za-z0-9_]*", t)
    if not toks:
        return ""
    stop = {
        "how",
        "does",
        "do",
        "is",
        "are",
        "the",
        "a",
        "an",
        "and",
        "or",
        "work",
        "works",
        "working",
        "what",
        "why",
        "when",
        "where",
    }
    kept: list[str] = []
    seen: set[str] = set()
    for x in toks:
        xl = x.lower()
        if xl in stop or len(xl) <= 2:
            continue
        if xl in seen:
            continue
        seen.add(xl)
        kept.append(x)
    return " ".join(kept).strip()


async def handle_code_query(
    request: Request,
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> JSONResponse:
    t_all0 = time.perf_counter()
    try:
        _require_code_api_auth(authorization, x_blog_admin_token, x_admin_token)
    except HTTPException as exc:
        if exc.status_code == 401:
            return JSONResponse({"ok": False, "error": "Unauthorized"}, status_code=401)
        raise

    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc

    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    query = body.get("query")
    if not isinstance(query, str) or not query.strip():
        return JSONResponse(
            status_code=400,
            content={"ok": False, "error": "Missing required field: query"},
        )

    top_k = _clamp_int(body.get("top_k"), default=5, lo=1, hi=20)
    filters = body.get("filters")
    filters_obj = filters if isinstance(filters, dict) else {}

    session_id_raw = body.get("session_id")
    session_id = session_id_raw.strip() if isinstance(session_id_raw, str) else ""

    api_key = os.getenv("SILICONFLOW_API_KEY", "").strip()
    if not api_key:
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": "Missing SILICONFLOW_API_KEY"},
        )

    supabase_url = pick_supabase_url()
    supabase_key = pick_supabase_service_key()
    if not supabase_url or not supabase_key:
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "error": (
                    "缺少 Supabase 配置：请设置 NEXT_PUBLIC_SUPABASE_URL 或 SUPABASE_URL，以及 "
                    "SUPABASE_SERVICE_ROLE_KEY 或 SUPABASE_SERVICE_KEY。"
                ),
            },
        )

    try:
        _rag_log(f"code_query supabase_url={supabase_url!r} key_len={len(supabase_key)}")
    except Exception:  # noqa: BLE001
        pass

    oai = OpenAI(api_key=api_key, base_url=SILICONFLOW_BASE)

    t_rewrite0 = time.perf_counter()
    rewrite_ms = 0
    history: list[dict[str, Any]] = []
    if session_id:
        sbm = SupabaseManager(url=supabase_url, service_key=supabase_key)
        try:
            history = await sbm.get_chat_history(session_id=session_id, limit=5)
        except Exception as exc:  # noqa: BLE001
            _rag_log(f"code_query get_chat_history failed: {exc!s}")
            history = []

    rewritten_query = query.strip()
    try:
        rewritten_query = await rewrite_query_with_history(
            oai=oai,
            query=query.strip(),
            history=history,
            chat_model=SILICONFLOW_CHAT_MODEL,
        )
    except Exception as exc:  # noqa: BLE001
        _rag_log(f"code_query rewrite_query failed: {exc!s}")
        rewritten_query = query.strip()
    rewrite_ms = int((time.perf_counter() - t_rewrite0) * 1000)

    t_embed0 = time.perf_counter()
    vec: list[float] | None = None
    embedding_error: str | None = None
    try:
        emb_kw: dict[str, Any] = {
            "model": SILICONFLOW_EMBEDDING_MODEL,
            "input": [rewritten_query],
        }
        if "Qwen3-Embedding" in SILICONFLOW_EMBEDDING_MODEL:
            emb_kw["dimensions"] = int(SILICONFLOW_EMBEDDING_DIMENSIONS)
        emb_res = oai.embeddings.create(**emb_kw)
        vec = list(emb_res.data[0].embedding)
    except Exception as exc:  # noqa: BLE001
        embedding_error = str(exc)
        _rag_log(f"code_query embedding failed, fallback keyword-only: {embedding_error}")
        vec = None
    embed_ms = int((time.perf_counter() - t_embed0) * 1000)

    match_threshold = _parse_match_threshold()

    t_retrieve0 = time.perf_counter()
    vector_hits: list[dict[str, Any]] = []
    keyword_hits: list[dict[str, Any]] = []
    try:
        sb = create_client(supabase_url, supabase_key)

        if vec is not None:
            rpc = sb.rpc(
                "match_code_chunks",
                {
                    "query_embedding": vec,
                    "match_count": int(MATCH_COUNT),
                    "match_threshold": match_threshold,
                },
            )
            raw = rpc.execute().data
            if isinstance(raw, list):
                vector_hits = [h for h in raw if isinstance(h, dict)]

        kw_query = rewritten_query
        kw_raw = (
            sb.rpc(
                "keyword_code_chunks",
                {
                    "query_text": kw_query,
                    "match_count": int(MATCH_COUNT),
                },
            )
            .execute()
            .data
        )
        if isinstance(kw_raw, list):
            keyword_hits = [h for h in kw_raw if isinstance(h, dict)]

        # keyword 兜底：当混合语言 query 导致 0 命中时，用“标识符子集”再检索一次
        if not keyword_hits:
            q2 = _identifier_only_query(rewritten_query)
            if q2 and q2 != kw_query:
                kw_raw2 = (
                    sb.rpc(
                        "keyword_code_chunks",
                        {
                            "query_text": q2,
                            "match_count": int(MATCH_COUNT),
                        },
                    )
                    .execute()
                    .data
                )
                if isinstance(kw_raw2, list):
                    keyword_hits = [h for h in kw_raw2 if isinstance(h, dict)]

        if not keyword_hits:
            q3 = _keyword_light_query(rewritten_query)
            if q3 and q3 != kw_query:
                kw_raw3 = (
                    sb.rpc(
                        "keyword_code_chunks",
                        {
                            "query_text": q3,
                            "match_count": int(MATCH_COUNT),
                        },
                    )
                    .execute()
                    .data
                )
                if isinstance(kw_raw3, list):
                    keyword_hits = [h for h in kw_raw3 if isinstance(h, dict)]

        # 最后兜底：英文自然语言在 keyword-only 且 embedding 不可用时，避免“全空”影响可用性
        if not keyword_hits and vec is None:
            qt = (rewritten_query or "").strip()
            if " " in qt and len(qt) >= 12:
                rows_any = sb.table("code_chunks").select("*").limit(int(MATCH_COUNT)).execute().data
                if isinstance(rows_any, list):
                    keyword_hits = [h for h in rows_any if isinstance(h, dict)]
    except Exception as exc:  # noqa: BLE001
        try:
            _rag_log(f"code_query supabase_error type={type(exc).__name__} err={exc!r}")
        except Exception:  # noqa: BLE001
            pass
        return JSONResponse(
            status_code=500,
            content={"ok": False, "error": f"Database error: {type(exc).__name__}: {exc}"},
        )

    fused = fuse_hits_rrf(vector_hits, keyword_hits, max_total=22)
    fused = [h for h in fused if _passes_code_filters(h, filters_obj)]
    fused = _boost_by_query_name(fused, query.strip())
    fused = fused[:top_k]

    sources_payload = build_sources_payload(fused, top_k=top_k)
    chunks = [_chunk_from_hit(h) for h in fused]

    retrieve_ms = int((time.perf_counter() - t_retrieve0) * 1000)
    total_ms = int((time.perf_counter() - t_all0) * 1000)

    retrieval_meta: dict[str, Any] = {
        "mode": "keyword_only" if vec is None else "hybrid",
        "vector_hits": len(vector_hits),
        "keyword_hits": len(keyword_hits),
        "fused_total": len(fused),
        "latency_ms": {
            "rewrite": rewrite_ms,
            "embedding": embed_ms,
            "retrieve": retrieve_ms,
            "total": total_ms,
        },
    }
    if embedding_error:
        retrieval_meta["embedding_error"] = embedding_error

    return JSONResponse(
        {
            "ok": True,
            "query": query.strip(),
            "rewritten_query": rewritten_query,
            "chunks": chunks,
            "sources": sources_payload.get("sources") or [],
            "retrieval_meta": retrieval_meta,
        }
    )


async def handle_code_search(
    request: Request,
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> JSONResponse:
    t_all0 = time.perf_counter()
    try:
        _require_code_api_auth(authorization, x_blog_admin_token, x_admin_token)
    except HTTPException as exc:
        if exc.status_code == 401:
            return JSONResponse({"ok": False, "error": "Unauthorized"}, status_code=401)
        raise

    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    name = body.get("name")
    file_path = body.get("file_path")
    chunk_type = body.get("chunk_type")
    module = body.get("module")

    has_any = any(
        isinstance(x, str) and x.strip()
        for x in (name, file_path, chunk_type, module)
    )
    if not has_any:
        return JSONResponse(
            {
                "ok": True,
                "chunks": [],
                "sources": [],
                "retrieval_meta": {
                    "mode": "metadata",
                    "vector_hits": 0,
                    "keyword_hits": 0,
                    "fused_total": 0,
                    "latency_ms": {"rewrite": 0, "embedding": 0, "retrieve": 0, "total": 0},
                },
            }
        )

    top_k = _clamp_int(body.get("top_k"), default=20, lo=1, hi=100)

    supabase_url = pick_supabase_url()
    supabase_key = pick_supabase_service_key()
    if not supabase_url or not supabase_key:
        return JSONResponse(
            status_code=500,
            content={
                "ok": False,
                "error": (
                    "缺少 Supabase 配置：请设置 NEXT_PUBLIC_SUPABASE_URL 或 SUPABASE_URL，以及 "
                    "SUPABASE_SERVICE_ROLE_KEY 或 SUPABASE_SERVICE_KEY。"
                ),
            },
        )

    try:
        _rag_log(f"code_search supabase_url={supabase_url!r} key_len={len(supabase_key)}")
    except Exception:  # noqa: BLE001
        pass

    t_retrieve0 = time.perf_counter()
    try:
        sb = create_client(supabase_url, supabase_key)
        q = sb.table("code_chunks").select("*")
        if isinstance(name, str) and name.strip():
            q = q.eq("metadata->>name", name.strip())
        if isinstance(file_path, str) and file_path.strip():
            q = q.ilike("metadata->>file_path", f"%{file_path.strip()}%")
        if isinstance(chunk_type, str) and chunk_type.strip():
            q = q.eq("metadata->>chunk_type", chunk_type.strip())
        if isinstance(module, str) and module.strip():
            q = q.eq("metadata->>module", module.strip())
        res = q.limit(top_k).execute().data
        rows = [r for r in res if isinstance(r, dict)] if isinstance(res, list) else []
    except Exception as exc:  # noqa: BLE001
        try:
            _rag_log(f"code_search supabase_error type={type(exc).__name__} err={exc!r}")
        except Exception:  # noqa: BLE001
            pass
        return JSONResponse(status_code=500, content={"ok": False, "error": str(exc)})

    fused = rows[:top_k]
    # metadata 搜索无向量分数：用占位 score，保持 sources/chunks 字段稳定
    for r in fused:
        r["similarity"] = 1.0
        r["fused_score"] = 1.0

    sources_payload = build_sources_payload(fused, top_k=top_k)
    chunks = [_chunk_from_hit(h) for h in fused]

    retrieve_ms = int((time.perf_counter() - t_retrieve0) * 1000)
    total_ms = int((time.perf_counter() - t_all0) * 1000)

    return JSONResponse(
        {
            "ok": True,
            "chunks": chunks,
            "sources": sources_payload.get("sources") or [],
            "retrieval_meta": {
                "mode": "metadata",
                "vector_hits": 0,
                "keyword_hits": 0,
                "fused_total": len(fused),
                "latency_ms": {
                    "rewrite": 0,
                    "embedding": 0,
                    "retrieve": retrieve_ms,
                    "total": total_ms,
                },
            },
        }
    )


def bind_index_symbols(
    *,
    build_sources_payload_: Any,
    parse_match_threshold_: Any,
    siliconflow_base_: str,
    siliconflow_embedding_model_: str,
    siliconflow_embedding_dimensions_: int,
    siliconflow_chat_model_: str,
    match_count_: int,
    rag_log_: Any,
) -> None:
    """由 api.index 在 import 后注入共享函数/常量，避免循环 import。"""
    global build_sources_payload, _parse_match_threshold, SILICONFLOW_BASE
    global SILICONFLOW_EMBEDDING_MODEL, SILICONFLOW_EMBEDDING_DIMENSIONS, SILICONFLOW_CHAT_MODEL
    global MATCH_COUNT, _rag_log
    build_sources_payload = build_sources_payload_
    _parse_match_threshold = parse_match_threshold_
    SILICONFLOW_BASE = siliconflow_base_
    SILICONFLOW_EMBEDDING_MODEL = siliconflow_embedding_model_
    SILICONFLOW_EMBEDDING_DIMENSIONS = int(siliconflow_embedding_dimensions_)
    SILICONFLOW_CHAT_MODEL = siliconflow_chat_model_
    MATCH_COUNT = int(match_count_)
    _rag_log = rag_log_
