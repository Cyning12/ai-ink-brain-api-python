"""Text2SQL 多轮结构化锚点：从 SQL 抽取主表/表集合，供落库与次轮 prompt 注入。"""

from __future__ import annotations

import re
from typing import Any

_GROUNDING_V = 1
# 与 intent_agent 单条 history 截断 200 对齐，控制单行长度
_MAX_SQL_EXCERPT = 220
_MAX_TABLES = 8


def extract_resolved_tables_from_sql(sql: str) -> list[str]:
    """从只读 SELECT 中抽取 FROM/JOIN 后的表名（public.xxx 或 xxx），去重保序。"""
    s = (sql or "").strip()
    if not s:
        return []
    s = re.sub(r"/\*[\s\S]*?\*/", " ", s)
    s = re.sub(r"--[^\n]*", " ", s)
    seen: set[str] = set()
    out: list[str] = []
    for m in re.finditer(r"\b(?:from|join)\s+(?:public\.)?([a-z_][a-z0-9_]*)", s, flags=re.IGNORECASE):
        name = (m.group(1) or "").strip().lower()
        if not name or name in ("select", "where", "on", "and", "or", "as", "left", "right", "inner", "outer", "cross"):
            continue
        if name not in seen:
            seen.add(name)
            out.append(name)
        if len(out) >= _MAX_TABLES:
            break
    return out


def sql_excerpt_for_grounding(sql: str, *, max_len: int = _MAX_SQL_EXCERPT) -> str:
    """单行、截断的 SQL 摘要（不含换行，便于 JSON 与 prompt）。"""
    one = re.sub(r"\s+", " ", (sql or "").strip())
    if len(one) <= max_len:
        return one
    return one[: max(0, max_len - 1)].rstrip() + "…"


def build_text2sql_grounding_dict(*, sql: str) -> dict[str, Any] | None:
    """构造写入 rag_conversation_logs.tool_results 的锚点块；无法解析时返回 None。"""
    sql_s = (sql or "").strip()
    if not sql_s:
        return None
    tables = extract_resolved_tables_from_sql(sql_s)
    if not tables:
        return None
    excerpt = sql_excerpt_for_grounding(sql_s)
    return {
        "v": _GROUNDING_V,
        "primary_table": tables[0],
        "resolved_tables": tables,
        "sql_excerpt": excerpt,
    }


def grounding_line_for_history_block(g: dict[str, Any] | None) -> str:
    """拼入 history_to_rewrite_block 的一行说明（中文）。"""
    if not isinstance(g, dict) or not g:
        return ""
    pt = g.get("primary_table")
    pt_s = pt.strip().lower() if isinstance(pt, str) and pt.strip() else ""
    if not pt_s:
        return ""
    excerpt = g.get("sql_excerpt")
    ex = excerpt.strip() if isinstance(excerpt, str) else ""
    if ex and len(ex) > 160:
        ex = ex[:159] + "…"
    if ex:
        return f"[Text2SQL 锚点] 主表 public.{pt_s}；上轮 SQL 摘要：{ex}"
    return f"[Text2SQL 锚点] 主表 public.{pt_s}"


def grounding_prefix_for_intent(history_item: dict[str, Any]) -> str:
    """供 Intent 历史：锚点行置于 assistant 正文之前，避免 intent_agent 对 content[:200] 截断时丢掉表名。"""
    g = history_item.get("text2sql_grounding") if isinstance(history_item, dict) else None
    line = grounding_line_for_history_block(g if isinstance(g, dict) else None)
    if not line:
        return ""
    if len(line) > 180:
        return line[:179] + "…"
    return line
