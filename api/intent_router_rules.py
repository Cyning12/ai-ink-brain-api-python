"""V1 意图路由：表驱动规则命中（keyword / regex / hints）。"""

from __future__ import annotations

import re

from .intent_hints import load_resolved_hints, rag_rule_hits_from_hints


def _contains_any(text: str, needles: list[str]) -> bool:
    t = (text or "").lower()
    return any(n.lower() in t for n in needles)


def rag_rule_hits(query: str) -> list[str]:
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

    if re.search(r"\btask\s*\d+", q, re.IGNORECASE):
        hits.append("rule:task_ref_hint")

    if re.search(r"\d{4}-\d{2}-\d{2}", q) and (".md" in q.lower() or "日记" in q or "diary" in q.lower()):
        hits.append("rule:date_doc_hint")

    if "content/" in q.lower() or "task_" in q.lower():
        hits.append("rule:repo_path_hint")

    try:
        hints = load_resolved_hints()
        if hints:
            for h in rag_rule_hits_from_hints(q, hints):
                if h not in hits:
                    hits.append(h)
    except Exception:  # noqa: BLE001
        pass

    return hits


def no_data_rule_hits(query: str) -> list[str]:
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


def sql_rule_hits(query: str) -> list[str]:
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
    if re.search(r"\b[a-z][a-z0-9_]{2,}\b", q):
        hits.append("rule:identifier_hint")
    return hits


def is_safe_count_query(query: str) -> bool:
    """是否属于“安全 COUNT 查询”。

    目标：避免在 DDL evidence=0 时把明确的计数类查询误降级到 no_data。
    约束：仅放行“计数/总数”这一类不依赖列信息的查询意图。
    """
    q = (query or "").strip().lower()
    if not q:
        return False

    has_table_word = "表" in q
    has_identifier_hint = re.search(r"\b[a-z][a-z0-9_]{2,}\b", q) is not None
    if not (has_table_word and has_identifier_hint):
        return False

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

    if "统计" in q and ("多少" in q or "条" in q):
        return True

    return False


def tool_rule_hits(query: str) -> list[str]:
    _ = query
    return []
