"""Ops Desk P0 schema DDL 验收测试。

本测试需要 PostgreSQL 连接（TEXT2SQL_DATABASE_URL）。
- 若 public 中四表不存在：自动创建 DDL，运行写测试，最后 rollback 清理。
- 若 public 中四表已存在：跳过写测试，仅执行只读结构验证，不破坏数据。
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import NamedTuple

import pytest

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None  # type: ignore[assignment]

try:
    import psycopg
except ImportError:  # pragma: no cover
    psycopg = None  # type: ignore[assignment]

try:
    import pglast
except ImportError:  # pragma: no cover
    pglast = None  # type: ignore[assignment]


REPO_ROOT = Path(__file__).resolve().parents[2]
if load_dotenv is not None:
    # 优先从本地 .env 读取数据库连接，便于开发机直接运行
    load_dotenv(REPO_ROOT / ".env.local", override=False)
    load_dotenv(REPO_ROOT / ".env", override=False)
SCHEMA_PATH = REPO_ROOT / "supabase" / "sql" / "ops_desk_p0_schema.sql"
ROLLBACK_PATH = REPO_ROOT / "supabase" / "sql" / "ops_desk_p0_schema_rollback.sql"


class SchemaInfo(NamedTuple):
    name: str
    created_by_us: bool


def _dsn() -> str | None:
    return (os.getenv("TEXT2SQL_DATABASE_URL") or "").strip() or None


def _read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _table_exists(conn, schema: str, table: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "select 1 from information_schema.tables "
            "where table_schema = %s and table_name = %s",
            (schema, table),
        )
        return cur.fetchone() is not None


@pytest.fixture(scope="module")
def db_schema():
    """返回 public schema 信息；若表不存在则创建并在模块结束时清理。"""
    dsn = _dsn()
    if not dsn or psycopg is None:
        pytest.skip("TEXT2SQL_DATABASE_URL 未配置或 psycopg 未安装")

    schema_name = "public"
    try:
        conn = psycopg.connect(dsn, autocommit=True)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"无法连接数据库: {exc}")

    created_by_us = False
    try:
        existing = [
            t
            for t in ("ops_repos", "ops_issues", "ops_pull_requests", "ops_sync_runs")
            if _table_exists(conn, schema_name, t)
        ]
        if not existing:
            try:
                with conn.cursor() as cur:
                    cur.execute(_read_sql(ROLLBACK_PATH))
                    cur.execute(_read_sql(SCHEMA_PATH))
                created_by_us = True
            except psycopg.errors.InsufficientPrivilege as exc:
                pytest.skip(f"当前数据库用户无 DDL 权限: {exc}")
        yield SchemaInfo(name=schema_name, created_by_us=created_by_us)
    finally:
        if created_by_us:
            with conn.cursor() as cur:
                cur.execute(_read_sql(ROLLBACK_PATH))
        conn.close()


def _require_writable(info: SchemaInfo) -> None:
    if not info.created_by_us:
        pytest.skip("public 中表已存在，跳过写测试以避免破坏数据")


def test_four_tables_exist(db_schema: SchemaInfo) -> None:
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        for table in ("ops_repos", "ops_issues", "ops_pull_requests", "ops_sync_runs"):
            assert _table_exists(conn, db_schema.name, table), f"{table} 未创建"
    finally:
        conn.close()


def _get_constraint_defs(conn, schema: str, table: str) -> list[str]:
    with conn.cursor() as cur:
        cur.execute(
            "select pg_get_constraintdef(oid) from pg_constraint "
            "where conrelid = (%s || '.' || %s)::regclass",
            (schema, table),
        )
        return [row[0] for row in cur.fetchall() if row[0]]


def test_issue_columns_and_constraints(db_schema: SchemaInfo) -> None:
    """只读验证 ops_issues 列与 (repo_id, number) 唯一约束。"""
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (db_schema.name, "ops_issues"),
            )
            columns = {row[0] for row in cur.fetchall()}
            for col in (
                "id", "repo_id", "number", "title", "body", "state",
                "labels", "assignees", "milestone", "created_at", "updated_at",
                "closed_at", "author", "html_url", "scan_tags",
            ):
                assert col in columns, f"ops_issues 缺少列 {col}"

        defs = _get_constraint_defs(conn, db_schema.name, "ops_issues")
        joined = "\n".join(defs)
        assert "UNIQUE (repo_id, number)" in joined
        assert "state = ANY (ARRAY['open'::text, 'closed'::text])" in joined
        assert "FOREIGN KEY (repo_id) REFERENCES ops_repos(id) ON DELETE CASCADE" in joined
    finally:
        conn.close()


def test_pull_request_columns_and_constraints(db_schema: SchemaInfo) -> None:
    """只读验证 ops_pull_requests 列与 (repo_id, number) 唯一约束。"""
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (db_schema.name, "ops_pull_requests"),
            )
            columns = {row[0] for row in cur.fetchall()}
            for col in (
                "id", "repo_id", "number", "title", "body", "state", "draft",
                "labels", "created_at", "updated_at", "closed_at", "merged_at",
                "author", "html_url", "head_ref", "base_ref", "checks_conclusion",
                "review_decision", "first_review_at", "additions", "deletions", "changed_files",
            ):
                assert col in columns, f"ops_pull_requests 缺少列 {col}"

        defs = _get_constraint_defs(conn, db_schema.name, "ops_pull_requests")
        joined = "\n".join(defs)
        assert "UNIQUE (repo_id, number)" in joined
        assert "state = ANY (ARRAY['open'::text, 'closed'::text, 'merged'::text])" in joined
        assert "FOREIGN KEY (repo_id) REFERENCES ops_repos(id) ON DELETE CASCADE" in joined
    finally:
        conn.close()


def test_sync_runs_columns_and_status_check(db_schema: SchemaInfo) -> None:
    """只读验证 ops_sync_runs 列与 status CHECK 约束。"""
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (db_schema.name, "ops_sync_runs"),
            )
            columns = {row[0] for row in cur.fetchall()}
            for col in (
                "id", "repo_id", "started_at", "finished_at", "status",
                "cursor", "records_issue", "records_pr", "error_message", "trigger",
            ):
                assert col in columns, f"ops_sync_runs 缺少列 {col}"

        defs = _get_constraint_defs(conn, db_schema.name, "ops_sync_runs")
        joined = "\n".join(defs)
        for status in ("pending", "running", "success", "failed", "partial"):
            assert status in joined, f"status CHECK 缺少 {status}"
        for trigger in ("cron", "manual", "initial"):
            assert trigger in joined, f"trigger CHECK 缺少 {trigger}"
        assert "FOREIGN KEY (repo_id) REFERENCES ops_repos(id) ON DELETE CASCADE" in joined
    finally:
        conn.close()


def test_repo_columns_and_constraints(db_schema: SchemaInfo) -> None:
    """只读验证 ops_repos 列与 (owner, name) 唯一约束。"""
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (db_schema.name, "ops_repos"),
            )
            columns = {row[0] for row in cur.fetchall()}
            for col in ("id", "owner", "name", "full_name", "default_branch", "created_at", "updated_at"):
                assert col in columns, f"ops_repos 缺少列 {col}"

        defs = _get_constraint_defs(conn, db_schema.name, "ops_repos")
        joined = "\n".join(defs)
        assert "UNIQUE (owner, name)" in joined
    finally:
        conn.close()


def test_repo_full_name_generated(db_schema: SchemaInfo) -> None:
    _require_writable(db_schema)
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning full_name",
                ("MoonshotAI", "kimi-code"),
            )
            row = cur.fetchone()
            assert row is not None
            assert row[0] == "MoonshotAI/kimi-code"
    finally:
        conn.close()


def test_issue_repo_number_unique(db_schema: SchemaInfo) -> None:
    _require_writable(db_schema)
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            cur.execute(
                f"insert into {db_schema.name}.ops_issues "
                "(repo_id, number, title, state, created_at, updated_at) "
                "values (%s, %s, %s, %s, now(), now())",
                (repo_id, 1, "first", "open"),
            )
            with pytest.raises(psycopg.errors.UniqueViolation):
                cur.execute(
                    f"insert into {db_schema.name}.ops_issues "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 1, "second", "open"),
                )
    finally:
        conn.close()


def test_pull_request_repo_number_unique(db_schema: SchemaInfo) -> None:
    _require_writable(db_schema)
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            cur.execute(
                f"insert into {db_schema.name}.ops_pull_requests "
                "(repo_id, number, title, state, created_at, updated_at) "
                "values (%s, %s, %s, %s, now(), now())",
                (repo_id, 1, "first", "open"),
            )
            with pytest.raises(psycopg.errors.UniqueViolation):
                cur.execute(
                    f"insert into {db_schema.name}.ops_pull_requests "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 1, "second", "open"),
                )
    finally:
        conn.close()


def test_sync_runs_status_check(db_schema: SchemaInfo) -> None:
    _require_writable(db_schema)
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            for status in ("pending", "running", "success", "failed", "partial"):
                cur.execute(
                    f"insert into {db_schema.name}.ops_sync_runs "
                    "(repo_id, status, trigger) values (%s, %s, %s)",
                    (repo_id, status, "cron"),
                )
            with pytest.raises(psycopg.errors.CheckViolation):
                cur.execute(
                    f"insert into {db_schema.name}.ops_sync_runs "
                    "(repo_id, status, trigger) values (%s, %s, %s)",
                    (repo_id, "invalid", "cron"),
                )
    finally:
        conn.close()


def test_issue_state_check(db_schema: SchemaInfo) -> None:
    _require_writable(db_schema)
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            with pytest.raises(psycopg.errors.CheckViolation):
                cur.execute(
                    f"insert into {db_schema.name}.ops_issues "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 2, "bad", "unknown"),
                )
    finally:
        conn.close()


def test_pull_request_state_check(db_schema: SchemaInfo) -> None:
    _require_writable(db_schema)
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            with pytest.raises(psycopg.errors.CheckViolation):
                cur.execute(
                    f"insert into {db_schema.name}.ops_pull_requests "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 2, "bad", "unknown"),
                )
    finally:
        conn.close()


def test_repo_cascade_delete(db_schema: SchemaInfo) -> None:
    _require_writable(db_schema)
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            cur.execute(
                f"insert into {db_schema.name}.ops_issues "
                "(repo_id, number, title, state, created_at, updated_at) "
                "values (%s, %s, %s, %s, now(), now())",
                (repo_id, 3, "cascade test", "open"),
            )
            cur.execute(f"delete from {db_schema.name}.ops_repos where id = %s", (repo_id,))
            cur.execute(
                f"select 1 from {db_schema.name}.ops_issues where repo_id = %s", (repo_id,)
            )
            assert cur.fetchone() is None
    finally:
        conn.close()


def test_rollback_file_loads() -> None:
    """回滚脚本存在且包含四表删除语句。"""
    sql = _read_sql(ROLLBACK_PATH)
    for table in ("ops_sync_runs", "ops_pull_requests", "ops_issues", "ops_repos"):
        assert f"drop table if exists public.{table}" in sql


def test_ddl_parses_with_pglast() -> None:
    """不依赖数据库：用 pglast 验证 DDL 与 rollback 可被 PostgreSQL 解析。"""
    if pglast is None:
        pytest.skip("pglast 未安装")
    ddl = _read_sql(SCHEMA_PATH)
    rollback = _read_sql(ROLLBACK_PATH)
    ddl_stmts = pglast.parse_sql(ddl)
    rollback_stmts = pglast.parse_sql(rollback)
    assert len(ddl_stmts) == 11  # extension + 4 tables + 6 indexes
    assert len(rollback_stmts) == 4  # 4 drop table
