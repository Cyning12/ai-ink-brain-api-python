"""text2sql_schema_prefetch：意图、DDL 锚点、策略与只读 SQL 形态。"""

from __future__ import annotations

import pytest

from api import text2sql_schema_prefetch as sp


def test_mutate_intent_positive() -> None:
    q = "生成sql并执行，将数据插入到agent_info表，若存在则更新"
    assert sp.is_text2sql_mutate_intent_query(q) is True


def test_mutate_intent_negative_select_only() -> None:
    q = "统计 public.agent_info 表中 active 用户数量"
    assert sp.is_text2sql_mutate_intent_query(q) is False


def test_extract_tables() -> None:
    q = "把数据写入 agent_info 表，并更新 public.orders 状态"
    assert set(sp.extract_candidate_tables_from_query(q)) == {"agent_info", "orders"}


def test_ddl_column_anchor_positive() -> None:
    retrieved = [
        {
            "doc_type": "ddl",
            "title": "DDL: agent_info",
            "content": (
                "create table public.agent_info (\n"
                "  user_id uuid not null,\n"
                "  display_name text,\n"
                "  primary key (user_id)\n"
                ");"
            ),
        }
    ]
    assert sp.ddl_fragment_has_column_anchor(retrieved, "agent_info") is True


def test_ddl_column_anchor_negative_short() -> None:
    retrieved = [
        {
            "doc_type": "ddl",
            "title": "DDL: agent_info",
            "content": "create table public.agent_info ();",
        }
    ]
    assert sp.ddl_fragment_has_column_anchor(retrieved, "agent_info") is False


def test_prefetch_sql_template_uses_information_schema_select_only() -> None:
    import inspect

    src = inspect.getsource(sp.fetch_public_table_columns_sync)
    assert "FROM information_schema.columns" in src
    assert "SELECT table_name, column_name" in src
    low = src.lower()
    assert "insert " not in low and "update " not in low and "delete " not in low


def test_run_prefetch_skips_when_not_mutate(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEXT2SQL_SCHEMA_PREFETCH", "1")
    monkeypatch.delenv("TEXT2SQL_DATABASE_URL", raising=False)
    blk, err, meta = sp.run_text2sql_schema_prefetch_sync(
        user_query="仅查询 agent_info 行数",
        retrieved=[],
        principal=None,
        policies=None,
    )
    assert blk is None and err is None
    assert meta.get("schema_prefetch_source") == "skipped_not_mutate"


def test_run_prefetch_error_when_mutate_but_no_table(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TEXT2SQL_SCHEMA_PREFETCH", "1")
    monkeypatch.delenv("TEXT2SQL_DATABASE_URL", raising=False)
    blk, err, meta = sp.run_text2sql_schema_prefetch_sync(
        user_query="请插入一行数据",
        retrieved=[],
        principal=None,
        policies=None,
    )
    assert blk is None and err is not None
    assert meta.get("schema_prefetch_source") == "error_no_table"


def test_build_sql_prompt_includes_prefetched_block() -> None:
    from api.text2sql_core import build_sql_prompt

    p = build_sql_prompt(
        "插入",
        [],
        prefetched_schema_block="### public.t\n- `a` : int (nullable: NO)",
    )
    assert "系统预取表结构" in p
    assert "information_schema" in p
    assert "public.t" in p
