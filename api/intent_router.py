from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Literal

from .intent_router_rules import (
    is_safe_count_query,
    no_data_rule_hits,
    rag_rule_hits,
    sql_rule_hits,
    tool_rule_hits,
)
from .rag_env import supabase_client
from .text2sql_store import get_text2sql_store

PreferMode = Literal["auto", "rag", "text2sql", "no_data"]


@dataclass(frozen=True)
class RouterDecision:
    prefer: str
    candidate_mode: str
    final_mode: str
    rule_hits: list[str]
    evidence: dict[str, Any]
    fallback: str | None


def _ddl_evidence(query: str) -> tuple[int, float | None]:
    """Text2SQL evidence：DDL 命中数与 top1 分数（若可得）。"""
    topk = int(os.getenv("INTENT_DDL_EVIDENCE_TOPK", "3"))
    min_score = float(os.getenv("INTENT_DDL_EVIDENCE_MIN_SCORE", "0.05"))
    store = get_text2sql_store()
    rows = store.search(query, top_k=topk)
    ddls = [r for r in rows if isinstance(r, dict) and r.get("doc_type") == "ddl"]
    top_score: float | None = None
    if ddls:
        s0 = ddls[0].get("score")
        try:
            top_score = float(s0) if s0 is not None else None
        except Exception:  # noqa: BLE001
            top_score = None
    hits = 0
    for r in ddls:
        try:
            s = float(r.get("score") or 0.0)
        except Exception:  # noqa: BLE001
            s = 0.0
        if s >= min_score:
            hits += 1
    return hits, top_score


def _fts_evidence(query: str) -> tuple[int, float | None]:
    """RAG evidence：keyword_documents 命中数与 top1 score（若可得）。"""
    topk = int(os.getenv("INTENT_FTS_EVIDENCE_TOPK", "3"))
    sb = supabase_client()
    raw = sb.rpc("keyword_documents", {"query_text": (query or "").strip(), "match_count": topk}).execute().data
    rows = raw if isinstance(raw, list) else []
    top1: float | None = None
    if rows:
        v = rows[0].get("score") if isinstance(rows[0], dict) else None
        try:
            top1 = float(v) if v is not None else None
        except Exception:  # noqa: BLE001
            top1 = None
    return len([r for r in rows if isinstance(r, dict)]), top1


def decide_intent(*, query: str, prefer: str) -> RouterDecision:
    """v1 路由：规则候选 + 证据校验 → final_mode。"""
    pref = (prefer or "auto").strip().lower()
    if pref.startswith("tool:"):
        return RouterDecision(
            prefer=pref,
            candidate_mode=pref,
            final_mode=pref,
            rule_hits=["prefer:tool"],
            evidence={},
            fallback=None,
        )
    if pref in ("rag", "text2sql", "no_data"):
        return RouterDecision(
            prefer=pref,
            candidate_mode=pref,
            final_mode=pref,
            rule_hits=[f"prefer:{pref}"],
            evidence={},
            fallback=None,
        )

    rule_hits: list[str] = []
    tool_hits = tool_rule_hits(query)
    rag_hits = rag_rule_hits(query)
    sql_hits = sql_rule_hits(query)
    nodata_hits = no_data_rule_hits(query)
    rule_hits.extend(tool_hits)
    rule_hits.extend(rag_hits)
    rule_hits.extend(sql_hits)
    rule_hits.extend(nodata_hits)

    candidate: str
    if tool_hits:
        candidate = "tool:unknown"
    elif rag_hits:
        candidate = "rag"
    elif nodata_hits and not sql_hits:
        candidate = "no_data"
    elif sql_hits:
        candidate = "text2sql"
    else:
        candidate = "rag"

    evidence: dict[str, Any] = {}
    fallback: str | None = None

    ddl_hits = 0
    ddl_top: float | None = None
    fts_hits = 0
    fts_top: float | None = None

    try:
        ddl_hits, ddl_top = _ddl_evidence(query)
    except Exception as exc:  # noqa: BLE001
        evidence["ddl_error"] = str(exc)

    try:
        fts_hits, fts_top = _fts_evidence(query)
    except Exception as exc:  # noqa: BLE001
        evidence["fts_error"] = str(exc)

    evidence.update(
        {
            "ddl_hits": ddl_hits,
            "ddl_top_score": ddl_top,
            "fts_hits": fts_hits,
            "fts_top1_score": fts_top,
        }
    )

    final_mode = candidate

    if candidate == "text2sql" and ddl_hits <= 0:
        if is_safe_count_query(query):
            final_mode = "text2sql"
            fallback = "text2sql_without_ddl_allowed_safe_count"
        elif fts_hits > 0:
            final_mode = "rag"
            fallback = "text2sql_without_ddl→rag"
        else:
            final_mode = "no_data"
            fallback = "text2sql_without_ddl→no_data"

    if final_mode == "rag" and fts_hits <= 0:
        if ddl_hits > 0 and sql_hits:
            final_mode = "text2sql"
            fallback = fallback or "rag_without_fts→text2sql"
        elif ddl_hits <= 0 and fts_hits <= 0 and not rag_hits:
            final_mode = "no_data"
            fallback = fallback or "rag_without_fts→no_data"
        else:
            final_mode = "rag"
            if not fallback:
                if rag_hits and ddl_hits <= 0 and fts_hits <= 0:
                    fallback = "rag_without_evidence_but_rag_signals"
                else:
                    fallback = "rag_without_fts_keep_rag_ddl_evidence"

    return RouterDecision(
        prefer="auto",
        candidate_mode=candidate,
        final_mode=final_mode,
        rule_hits=rule_hits,
        evidence=evidence,
        fallback=fallback,
    )
