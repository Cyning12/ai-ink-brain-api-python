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


def _rag_rule_hits(query: str) -> list[str]:
    """偏「读仓库内文档 / 日记 / 任务说明」的轻量规则，用于在 auto 下优先走 RAG 候选。"""
    hits: list[str] = []
    q = (query or "").strip()
    if not q:
        return hits

    rag_kw = [
        "日记",
        "diary",
        "markdown",
        ".md",
        "任务单",
        "规范",
        "架构说明",
        "_tech_graph",
        "文档",
        "文章",
        "博客",
        "写了什么",
        "内容是什么",
        "讲了什么",
        "说了什么",
        "摘录",
        "这篇",
        "那篇",
        "哪篇",
        "readme",
    ]
    if _contains_any(q, rag_kw):
        hits.append("rule:rag_keywords")

    # 任务编号 / 章节式引用（偏文档检索）
    if re.search(r"\btask\s*\d+", q, re.IGNORECASE):
        hits.append("rule:task_ref_hint")

    # 日期 + 文档形态（如 2026-04-28.md、某天的日记）
    if re.search(r"\d{4}-\d{2}-\d{2}", q) and (".md" in q.lower() or "日记" in q or "diary" in q.lower()):
        hits.append("rule:date_doc_hint")

    if "content/" in q.lower() or "task_" in q.lower():
        hits.append("rule:repo_path_hint")

    return hits


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


def _is_safe_count_query(query: str) -> bool:
    """是否属于“安全 COUNT 查询”。

    目标：避免在 DDL evidence=0 时把明确的计数类查询误降级到 no_data。
    约束：仅放行“计数/总数”这一类不依赖列信息的查询意图。
    """
    q = (query or "").strip().lower()
    if not q:
        return False

    # 必须出现“表”与一个可疑标识符（表名倾向）
    has_table_word = "表" in q
    has_identifier_hint = re.search(r"\b[a-z][a-z0-9_]{2,}\b", q) is not None
    if not (has_table_word and has_identifier_hint):
        return False

    # 必须是计数语义（不要求精确关键词匹配，但至少要有明显的 count/总数/多少条）
    count_needles = (
        "count",
        "总数",
        "多少条",
        "多少行",
        "有多少",
        "多少条数据",
        "条数据",
        "记录数",
        "条记录",
    )
    if any(n in q for n in count_needles):
        return True

    # “统计 + 表 + 多少/条”也视为计数类（中文口语常见）
    if "统计" in q and ("多少" in q or "条" in q):
        return True

    return False


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
    rag_hits = _rag_rule_hits(query)
    sql_hits = _sql_rule_hits(query)
    nodata_hits = _no_data_rule_hits(query)
    rule_hits.extend(tool_hits)
    rule_hits.extend(rag_hits)
    rule_hits.extend(sql_hits)
    rule_hits.extend(nodata_hits)

    # candidate selection（rag 信号优先于纯 SQL 关键词 / no_data 创作词，减少「查日记」误成 text2sql）
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
        # 特判：明确的“统计某表有多少条”属于安全 COUNT 查询，不依赖列信息，允许直接走 text2sql。
        if _is_safe_count_query(query):
            final_mode = "text2sql"
            fallback = "text2sql_without_ddl_allowed_safe_count"
        # fall back: prefer rag if fts has evidence else no_data
        elif fts_hits > 0:
            final_mode = "rag"
            fallback = "text2sql_without_ddl→rag"
        else:
            final_mode = "no_data"
            fallback = "text2sql_without_ddl→no_data"

    # protect: rag 在 FTS 无命中时，仅当 DDL 与 FTS 两侧都无有效信号且无 rag 规则命中时再降为 no_data
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

