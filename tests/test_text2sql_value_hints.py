"""Text2SQL 值域字典：加载、表裁剪、prompt 顺序。"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("yaml", reason="值域 YAML 测试依赖 PyYAML（requirements.txt 含 pyyaml）")

from api.text2sql_core import build_sql_prompt
from api.text2sql_value_hints import (
    build_value_hints_block_for_text2sql,
    ddl_table_names_from_retrieved,
    format_hints_for_prompt,
    load_hints,
    merge_hints_with_distinct_probes,
    parse_distinct_allowlist,
    tables_for_value_hints,
)


def _sample_hints() -> dict:
    return {
        "version": 1,
        "tables": {
            "agent_info": {
                "gender": {
                    "column": "gender",
                    "values": ["男", "女"],
                    "synonyms": {"男性": "男", "男的": "男", "female": "女"},
                },
                "commission_structure": {
                    "column": "commission_structure",
                    "values": ["底薪加提成", "固定佣金", "提成结构"],
                    "synonyms": {"提成结构": "底薪加提成"},
                },
            }
        },
    }


def test_ddl_table_names_from_retrieved() -> None:
    retrieved = [
        {
            "doc_type": "ddl",
            "title": "DDL: agent_info",
            "content": "create table public.agent_info (\n  gender text\n);",
        }
    ]
    assert ddl_table_names_from_retrieved(retrieved) == {"agent_info"}


def test_tables_for_value_hints_primary_narrows() -> None:
    ddl = {"agent_info", "customer_info"}
    assert tables_for_value_hints(ddl, "agent_info") == {"agent_info"}
    assert tables_for_value_hints(ddl, None) == ddl


def test_format_hints_contains_synonyms_and_values() -> None:
    body = format_hints_for_prompt(_sample_hints(), {"agent_info"})
    assert "库内取值：男、女" in body
    assert "男性→男" in body
    assert "commission_structure" in body
    assert "底薪加提成" in body


def test_build_sql_prompt_inserts_hints_before_dialogue() -> None:
    body = format_hints_for_prompt(_sample_hints(), {"agent_info"})
    vh = "【业务术语与库内取值】\n" + body
    prompt = build_sql_prompt(
        "多少男性",
        [{"doc_type": "ddl", "title": "DDL: agent_info", "content": "create table public.agent_info (gender text);"}],
        dialogue_context="上一轮问过 agent_info",
        value_hints_block=vh,
    )
    i_hints = prompt.find("【业务术语与库内取值】")
    i_ctx = prompt.find("【近期对话（指代消解）】")
    assert i_hints != -1 and i_ctx != -1
    assert i_hints < i_ctx


def test_load_hints_from_file_roundtrip(tmp_path: Path) -> None:
    import api.text2sql_value_hints as vh_mod

    vh_mod._loaded.clear()
    p = tmp_path / "h.yaml"
    p.write_text(
        """
version: 1
tables:
  agent_info:
    gender:
      column: gender
      values: ["男", "女"]
      synonyms:
        男性: 男
""",
        encoding="utf-8",
    )
    data = load_hints(p)
    if data is None:
        pytest.fail(f"load_hints 返回 None，请检查 PyYAML 与文件内容: {p}（exists={p.is_file()}）")
    assert isinstance(data, dict)
    assert data.get("version") == 1
    body = format_hints_for_prompt(data, {"agent_info"})
    assert "男性→男" in body


def test_build_value_hints_block_respects_env_path(tmp_path: Path, monkeypatch) -> None:
    import api.text2sql_value_hints as vh_mod

    vh_mod._loaded.clear()
    repo_root = Path(__file__).resolve().parents[1]
    bundled = repo_root / "docs/text2sql/v1/value_hints.yaml"
    fallback = """
version: 1
tables:
  agent_info:
    gender:
      column: gender
      values: ["男", "女"]
      synonyms:
        男性: 男
"""
    p = tmp_path / "hints.yaml"
    p.write_text(
        bundled.read_text(encoding="utf-8") if bundled.is_file() else fallback,
        encoding="utf-8",
    )
    monkeypatch.setenv("TEXT2SQL_VALUE_HINTS_PATH", str(p))
    monkeypatch.setenv("TEXT2SQL_VALUE_HINTS_ENABLED", "true")
    retrieved = [
        {
            "doc_type": "ddl",
            "title": "DDL: agent_info",
            "content": "create table public.agent_info (\n  gender text\n);",
        }
    ]
    block = build_value_hints_block_for_text2sql(retrieved, history=None)
    if block is None:
        import os

        rp = vh_mod._resolve_hints_path()
        pytest.fail(
            "build_value_hints_block_for_text2sql 返回 None；"
            f"_resolve_hints_path()={rp!s}, TEXT2SQL_VALUE_HINTS_ENABLED={os.environ.get('TEXT2SQL_VALUE_HINTS_ENABLED')!r}"
        )
    assert block
    assert "【值域与口语映射】" in block
    assert "男性→男" in block


def test_build_value_hints_disabled(monkeypatch) -> None:
    monkeypatch.setenv("TEXT2SQL_VALUE_HINTS_ENABLED", "false")
    retrieved = [
        {
            "doc_type": "ddl",
            "title": "DDL: agent_info",
            "content": "create table public.agent_info (gender text);",
        }
    ]
    assert build_value_hints_block_for_text2sql(retrieved, history=None) is None


def test_parse_distinct_allowlist_filters_invalid(monkeypatch) -> None:
    monkeypatch.setenv("TEXT2SQL_DISTINCT_COLUMNS", "public.agent_info.gender,bad,public.x.y")
    got = parse_distinct_allowlist()
    assert got == [("public", "agent_info", "gender"), ("public", "x", "y")]


def test_merge_hints_distinct_off_returns_same_ref(monkeypatch) -> None:
    monkeypatch.delenv("TEXT2SQL_DISTINCT_PROBE", raising=False)
    h = _sample_hints()
    out = merge_hints_with_distinct_probes(h, {"agent_info"})
    assert out is h


def test_merge_hints_distinct_unions_yaml_and_db(monkeypatch) -> None:
    calls: list[str] = []

    def fake_execute(
        sql: str,
        *,
        limit_rows: int = 200,
        statement_timeout_ms: int | None = None,
    ) -> tuple[list[str], list[dict]]:
        calls.append(sql)
        assert "DISTINCT" in sql.upper()
        assert "LIMIT" in sql.upper()
        return (["gender"], [{"gender": "库内新枚举"}])

    monkeypatch.setenv("TEXT2SQL_DISTINCT_PROBE", "true")
    monkeypatch.setenv("TEXT2SQL_DISTINCT_COLUMNS", "public.agent_info.gender")
    monkeypatch.setattr("api.text2sql_value_hints.execute_select_sql", fake_execute)
    h = _sample_hints()
    out = merge_hints_with_distinct_probes(h, {"agent_info"})
    assert out is not h
    body = format_hints_for_prompt(out, {"agent_info"})
    assert "男" in body and "女" in body and "库内新枚举" in body
    assert len(calls) == 1


def test_merge_hints_distinct_failure_keeps_yaml_only(monkeypatch) -> None:
    def boom(
        sql: str,
        *,
        limit_rows: int = 200,
        statement_timeout_ms: int | None = None,
    ) -> tuple[list[str], list[dict]]:
        raise RuntimeError("db down")

    monkeypatch.setenv("TEXT2SQL_DISTINCT_PROBE", "true")
    monkeypatch.setenv("TEXT2SQL_DISTINCT_COLUMNS", "public.agent_info.gender")
    monkeypatch.setattr("api.text2sql_value_hints.execute_select_sql", boom)
    h = _sample_hints()
    out = merge_hints_with_distinct_probes(h, {"agent_info"})
    body_yaml = format_hints_for_prompt(h, {"agent_info"})
    body_out = format_hints_for_prompt(out, {"agent_info"})
    assert body_out == body_yaml


def test_build_value_hints_includes_merge_disclaimer_when_probe_on(monkeypatch, tmp_path: Path) -> None:
    import api.text2sql_value_hints as vh_mod

    vh_mod._loaded.clear()
    p = tmp_path / "hints.yaml"
    p.write_text(
        """
version: 1
tables:
  agent_info:
    gender:
      column: gender
      values: ["男", "女"]
      synonyms:
        男性: 男
""",
        encoding="utf-8",
    )
    monkeypatch.setenv("TEXT2SQL_VALUE_HINTS_PATH", str(p))
    monkeypatch.setenv("TEXT2SQL_VALUE_HINTS_ENABLED", "true")
    monkeypatch.setenv("TEXT2SQL_DISTINCT_PROBE", "true")
    monkeypatch.setenv("TEXT2SQL_DISTINCT_COLUMNS", "public.agent_info.gender")

    def fake_execute(
        sql: str,
        *,
        limit_rows: int = 200,
        statement_timeout_ms: int | None = None,
    ) -> tuple[list[str], list[dict]]:
        return (["gender"], [{"gender": "男"}])

    monkeypatch.setattr("api.text2sql_value_hints.execute_select_sql", fake_execute)
    retrieved = [
        {
            "doc_type": "ddl",
            "title": "DDL: agent_info",
            "content": "create table public.agent_info (\n  gender text\n);",
        }
    ]
    block = build_value_hints_block_for_text2sql(retrieved, history=None)
    assert block
    assert "DISTINCT 采样" in block
    assert "非全量闭集" in block
