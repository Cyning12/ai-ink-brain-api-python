"""text2sql_grounding：表抽取、落库块、history 拼接。"""

from __future__ import annotations

from api.query_rewrite import history_to_rewrite_block
from api.text2sql_grounding import (
    build_text2sql_grounding_dict,
    extract_resolved_tables_from_sql,
    grounding_line_for_history_block,
    grounding_prefix_for_intent,
)


def test_extract_tables_from_simple_select() -> None:
    sql = "SELECT COUNT(*) FROM public.agent_info WHERE gender = '男'"
    assert extract_resolved_tables_from_sql(sql) == ["agent_info"]


def test_extract_tables_join_order() -> None:
    sql = "select * from customer_info c join public.agent_info a on true"
    t = extract_resolved_tables_from_sql(sql)
    assert t[0] == "customer_info"
    assert "agent_info" in t


def test_build_grounding_dict() -> None:
    g = build_text2sql_grounding_dict(sql="select count(*) from public.agent_info")
    assert g is not None
    assert g["primary_table"] == "agent_info"
    assert g["resolved_tables"] == ["agent_info"]
    assert "count" in g["sql_excerpt"].lower()


def test_history_block_includes_grounding() -> None:
    hist = [
        {
            "query": "统计 agent_info",
            "response": "共 10 条",
            "text2sql_grounding": {
                "v": 1,
                "primary_table": "agent_info",
                "resolved_tables": ["agent_info"],
                "sql_excerpt": "select count(*) from public.agent_info",
            },
        }
    ]
    block = history_to_rewrite_block(hist)
    assert "agent_info" in block
    assert "[Text2SQL 锚点]" in block


def test_grounding_line_for_intent_prefix() -> None:
    line = grounding_line_for_history_block(
        {"primary_table": "agent_info", "sql_excerpt": "select 1 from public.agent_info", "v": 1}
    )
    assert "public.agent_info" in line
    pre = grounding_prefix_for_intent(
        {
            "query": "q",
            "response": "r",
            "text2sql_grounding": {"primary_table": "agent_info", "sql_excerpt": "select 1", "v": 1},
        }
    )
    assert pre.startswith("[Text2SQL 锚点]")
