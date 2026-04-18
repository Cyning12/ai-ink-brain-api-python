from __future__ import annotations

from dataclasses import asdict
from typing import Any

from .keyword_fallback import KeywordFallbackResult


def build_retrieved_context_for_log(rows: list[dict[str, Any]], *, limit: int = 22) -> list[dict[str, Any]]:
    packed: list[dict[str, Any]] = []
    for r in rows[: max(1, int(limit))]:
        meta = r.get("metadata") if isinstance(r.get("metadata"), dict) else {}
        content = r.get("content") if isinstance(r.get("content"), str) else ""
        packed.append(
            {
                "id": r.get("id"),
                "similarity": r.get("similarity"),
                "keyword_score": r.get("score"),
                "fused_score": r.get("fused_score"),
                "rrf": r.get("rrf"),
                "metadata": meta,
                "content": content[:2000],
            }
        )
    return packed


def build_keyword_fallback_meta(keyword_fallback: KeywordFallbackResult | None) -> dict[str, Any] | None:
    if not keyword_fallback:
        return None
    # dataclass -> dict，确保字段稳定
    return asdict(keyword_fallback)


def build_rag_match_meta(
    *,
    match_count: int,
    match_threshold: float | None,
    date_anchor_count: int,
    rrf_k: int,
    vector_hits_count: int,
    keyword_hits_count: int,
    embedding_error: str | None,
    keyword_fallback: KeywordFallbackResult | None,
    vec_available: bool,
    query_compare: dict[str, Any] | None = None,
) -> dict[str, Any]:
    out: dict[str, Any] = {
        "count": match_count,
        "threshold": match_threshold,
        "date_anchor_count": date_anchor_count,
        "hybrid": {
            "rrf_k": rrf_k,
            "vector_hits": int(vector_hits_count),
            "keyword_hits": int(keyword_hits_count),
            "mode": "hybrid" if vec_available else "keyword_only",
            "embedding_error": embedding_error,
            "keyword_fallback": build_keyword_fallback_meta(keyword_fallback),
        },
    }
    if query_compare is not None:
        out["query_compare"] = query_compare
    return out


def summarize_hits_brief(hits: list[dict[str, Any]], *, top_n: int = 5) -> list[dict[str, Any]]:
    """给 console debug 用的精简命中摘要（避免打印大段 content）。"""
    out: list[dict[str, Any]] = []
    for h in hits[: max(1, int(top_n))]:
        meta = h.get("metadata") if isinstance(h.get("metadata"), dict) else {}
        out.append(
            {
                "id": h.get("id"),
                "path": meta.get("relativePath"),
                "filename": meta.get("filename"),
                "slug": meta.get("slug"),
                "category": meta.get("category"),
                "similarity": h.get("similarity"),
                "keyword_score": h.get("score"),
                "fused_score": h.get("fused_score"),
                "rrf": h.get("rrf"),
            }
        )
    return out

