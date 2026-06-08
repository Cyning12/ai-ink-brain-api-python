"""BE-1 公开测：validate_sql_readonly 行为（解题 Agent 可见）。"""

from __future__ import annotations

import pytest

from api.text2sql_core import validate_sql_readonly


class TestValidateSqlReadonlyPublic:
    """正例：加固后仍须通过。"""

    def test_public_with_cte_select(self) -> None:
        sql = validate_sql_readonly("WITH c AS (SELECT 1 AS n) SELECT n FROM c")
        assert "with" in sql.lower()
        assert "select" in sql.lower()

    def test_public_simple_select(self) -> None:
        sql = validate_sql_readonly("SELECT 42 AS answer")
        assert "42" in sql

    def test_public_trailing_semicolon_single_statement(self) -> None:
        sql = validate_sql_readonly("SELECT 1 AS n;")
        assert sql.endswith("SELECT 1 AS n") or "select 1" in sql.lower()


class TestValidateSqlReadonlyPublicNegative:
    """负例：公开暴露主缺口，引导 Agent 对齐 AST 多语句规则。"""

    def test_public_reject_multi_statement_single_semicolon(self) -> None:
        with pytest.raises(ValueError, match="Multiple statements"):
            validate_sql_readonly("SELECT 1; SELECT 2")
