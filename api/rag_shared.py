"""RAG 侧无状态共享工具（Legacy chat 与 Unified 共用，行为以 Unified 实现为基准）。"""

from __future__ import annotations

import os
import re
from typing import Any

from .chatbi_circuit_breaker import CircuitBreakerOpenError
from .rag_env import rag_debug_enabled, supabase_execute_with_retry


def _rag_log(msg: str) -> None:
    if rag_debug_enabled():
        print(f"[rag-debug] {msg}", flush=True)


def _short(text: str, max_len: int) -> str:
    t = text.replace("\n", "\\n")
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


def _extract_title_from_context(content: str) -> str | None:
    m = re.search(r"Title:\s*(\S+)", content)
    return m.group(1).strip() if m else None


def fetch_keyword_hits(sb: Any, query_text: str, *, match_count: int = 12) -> list[dict[str, Any]]:
    """Keyword 路：调用 Supabase RPC keyword_documents（FTS）。"""
    qt = (query_text or "").strip()
    if not qt:
        return []
    try:
        res = supabase_execute_with_retry(
            lambda: sb.rpc(
                "keyword_documents",
                {
                    "query_text": qt,
                    "match_count": int(match_count),
                },
            )
            .execute()
            .data
        )
        if isinstance(res, list):
            return [r for r in res if isinstance(r, dict)]
    except CircuitBreakerOpenError:
        raise
    except Exception as exc:  # noqa: BLE001
        _rag_log(f"keyword_documents error: {exc!s}")
    return []


def _fetch_keyword_hits_for_fallback(sb: Any, query_text: str, match_count: int) -> list[dict[str, Any]]:
    # 适配 keyword_fallback 模块的 Callable 签名，避免在模块间传递关键字参数。
    return fetch_keyword_hits(sb, query_text, match_count=match_count)


def build_sources_payload(hits: list[dict[str, Any]], *, top_k: int = 10) -> dict[str, Any]:
    """从融合后的命中结果里提取 sources（供前端引用卡片展示）。"""
    from .hybrid_fusion import RRF_K

    packed: list[dict[str, Any]] = []
    for h in hits[: max(1, int(top_k))]:
        meta = h.get("metadata") if isinstance(h.get("metadata"), dict) else {}
        content = h.get("content") if isinstance(h.get("content"), str) else ""
        snippet = strip_doc_context_prefix(content).replace("\r\n", "\n").strip()
        snippet = snippet[:400] if len(snippet) > 400 else snippet

        filename = meta.get("filename")
        relative_path = meta.get("relativePath")
        original_link = meta.get("original_link")
        fused_score = h.get("fused_score")

        packed.append(
            {
                "id": h.get("id"),
                # --- Task04 规范字段（前端用于"证据链"展示）---
                "content": snippet,
                "filename": filename,
                "score": fused_score,
                "path": relative_path,
                "url": original_link,
                # --- 兼容历史字段（不破坏已有 SourceCitation 组件）---
                "relativePath": relative_path,
                "slug": meta.get("slug"),
                "original_link": original_link,
                "category": meta.get("category"),
                "chunk_index": meta.get("chunk_index"),
                "snippet": snippet,
                "fused_score": fused_score,
            }
        )
    return {
        "sources": packed,
        "retrieval": {"top_k": int(top_k), "rrf_k": RRF_K},
    }


def parse_match_threshold() -> float | None:
    """解析 RAG_MATCH_THRESHOLD：默认 0.3；none/null/off 关闭过滤；非法或 <0 回退 0.3；>1 视为关闭过滤（None）。"""
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


def strip_doc_context_prefix(text: str) -> str:
    """去掉 ingest 写入的文档前缀信息，避免 snippet 噪声。"""
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
