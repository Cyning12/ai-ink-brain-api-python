from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any, Literal

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


def _contains_any(text: str, needles: list[str]) -> bool:
    t = (text or "").lower()
    return any(n.lower() in t for n in needles)


def _no_data_rule_hits(query: str) -> list[str]:
    hits: list[str] = []
    q = (query or "").strip()
    if not q:
        return hits
    no_data_kw = [
        "润色",
        "改写",
        "翻译",
        "写作",
        "起标题",
        "总结",
        "概括",
        "生成",
        "提纲",
        "头脑风暴",
        "邮件",
        "周报",
        "改成更正式",
        "rewrite",
        "polish",
        "translate",
        "brainstorm",
    ]
    if _contains_any(q, no_data_kw):
        hits.append("rule:no_data_keywords")
    return hits


def _sql_rule_hits(query: str) -> list[str]:
    hits: list[str] = []
    q = (query or "").strip()
    if not q:
        return hits
    sql_kw = [
        "查询",
        "统计",
        "多少",
        "金额",
        "人数",
        "数量",
        "总数",
        "平均",
        "最大",
        "最小",
        "top",
        "排行",
        "分组",
        "汇总",
        "group by",
        "count",
        "sum",
        "avg",
    ]
    if _contains_any(q, sql_kw):
        hits.append("rule:sql_keywords")
    # 明确提表名/字段名的倾向（snake_case）
    if re.search(r"\b[a-z][a-z0-9_]{2,}\b", q):
        hits.append("rule:identifier_hint")
    return hits


def _tool_rule_hits(query: str) -> list[str]:
    # v1 仅预留，返回空
    _ = query
    return []


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
    tool_hits = _tool_rule_hits(query)
    sql_hits = _sql_rule_hits(query)
    nodata_hits = _no_data_rule_hits(query)
    rule_hits.extend(tool_hits)
    rule_hits.extend(sql_hits)
    rule_hits.extend(nodata_hits)

    # candidate selection
    candidate: str
    if tool_hits:
        candidate = "tool:unknown"
    elif nodata_hits and not sql_hits:
        candidate = "no_data"
    elif sql_hits:
        candidate = "text2sql"
    else:
        candidate = "rag"

    evidence: dict[str, Any] = {}
    fallback: str | None = None

    # evidence check
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

    # protect: sql needs ddl evidence
    if candidate == "text2sql" and ddl_hits <= 0:
        # fall back: prefer rag if fts has evidence else no_data
        if fts_hits > 0:
            final_mode = "rag"
            fallback = "text2sql_without_ddl→rag"
        else:
            final_mode = "no_data"
            fallback = "text2sql_without_ddl→no_data"

    # protect: rag without evidence becomes no_data unless sql evidence exists
    if final_mode == "rag" and fts_hits <= 0:
        if ddl_hits > 0 and sql_hits:
            final_mode = "text2sql"
            fallback = fallback or "rag_without_fts→text2sql"
        else:
            final_mode = "no_data"
            fallback = fallback or "rag_without_fts→no_data"

    return RouterDecision(
        prefer="auto",
        candidate_mode=candidate,
        final_mode=final_mode,
        rule_hits=rule_hits,
        evidence=evidence,
        fallback=fallback,
    )

