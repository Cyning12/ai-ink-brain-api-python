"""Ops Desk P0 schema DDL 验收测试。

本测试需要可写 PostgreSQL 连接（TEXT2SQL_DATABASE_URL）。
未配置、无法连接或无 DDL 权限时跳过；在 public schema 中建表并清理。
"""

from __future__ import annotations

import os
from pathlib import Path

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


def _dsn() -> str | None:
    return (os.getenv("TEXT2SQL_DATABASE_URL") or "").strip() or None


def _read_sql(path: Path) -> str:
    return path.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def db_schema():
    """在 public schema 中应用 P0 DDL，测试模块结束后 rollback 清理。

    若 public 中已存在四表（可能已被其他流程创建或正在使用），
    直接跳过避免破坏现有数据。
    """
    dsn = _dsn()
    if not dsn or psycopg is None:
        pytest.skip("TEXT2SQL_DATABASE_URL 未配置或 psycopg 未安装")

    schema_name = "public"
    try:
        conn = psycopg.connect(dsn, autocommit=True)
    except Exception as exc:  # noqa: BLE001
        pytest.skip(f"无法连接数据库: {exc}")

    try:
        existing = [
            t
            for t in ("ops_repos", "ops_issues", "ops_pull_requests", "ops_sync_runs")
            if _table_exists(conn, schema_name, t)
        ]
        if existing:
            pytest.skip(f"public schema 已存在 {existing}，跳过避免破坏数据")

        rollback = _read_sql(ROLLBACK_PATH)
        ddl = _read_sql(SCHEMA_PATH)
        try:
            with conn.cursor() as cur:
                cur.execute(rollback)
                cur.execute(ddl)
        except psycopg.errors.InsufficientPrivilege as exc:
            pytest.skip(f"当前数据库用户无 DDL 权限: {exc}")
        yield schema_name
    finally:
        with conn.cursor() as cur:
            cur.execute(_read_sql(ROLLBACK_PATH))
        conn.close()


def _table_exists(conn, schema: str, table: str) -> bool:
    with conn.cursor() as cur:
        cur.execute(
            "select 1 from information_schema.tables "
            "where table_schema = %s and table_name = %s",
            (schema, table),
        )
        return cur.fetchone() is not None


def test_four_tables_exist(db_schema: str) -> None:
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        for table in ("ops_repos", "ops_issues", "ops_pull_requests", "ops_sync_runs"):
            assert _table_exists(conn, db_schema, table), f"{table} 未创建"
    finally:
        conn.close()


def test_repo_full_name_generated(db_schema: str) -> None:
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema}.ops_repos (owner, name) values (%s, %s) returning full_name",
                ("MoonshotAI", "kimi-code"),
            )
            row = cur.fetchone()
            assert row is not None
            assert row[0] == "MoonshotAI/kimi-code"
    finally:
        conn.close()


def test_issue_repo_number_unique(db_schema: str) -> None:
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            cur.execute(
                f"insert into {db_schema}.ops_issues "
                "(repo_id, number, title, state, created_at, updated_at) "
                "values (%s, %s, %s, %s, now(), now())",
                (repo_id, 1, "first", "open"),
            )
            with pytest.raises(psycopg.errors.UniqueViolation):
                cur.execute(
                    f"insert into {db_schema}.ops_issues "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 1, "second", "open"),
                )
    finally:
        conn.close()


def test_pull_request_repo_number_unique(db_schema: str) -> None:
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            cur.execute(
                f"insert into {db_schema}.ops_pull_requests "
                "(repo_id, number, title, state, created_at, updated_at) "
                "values (%s, %s, %s, %s, now(), now())",
                (repo_id, 1, "first", "open"),
            )
            with pytest.raises(psycopg.errors.UniqueViolation):
                cur.execute(
                    f"insert into {db_schema}.ops_pull_requests "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 1, "second", "open"),
                )
    finally:
        conn.close()


def test_sync_runs_status_check(db_schema: str) -> None:
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            for status in ("pending", "running", "success", "failed", "partial"):
                cur.execute(
                    f"insert into {db_schema}.ops_sync_runs "
                    "(repo_id, status, trigger) values (%s, %s, %s)",
                    (repo_id, status, "cron"),
                )
            with pytest.raises(psycopg.errors.CheckViolation):
                cur.execute(
                    f"insert into {db_schema}.ops_sync_runs "
                    "(repo_id, status, trigger) values (%s, %s, %s)",
                    (repo_id, "invalid", "cron"),
                )
    finally:
        conn.close()


def test_issue_state_check(db_schema: str) -> None:
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            with pytest.raises(psycopg.errors.CheckViolation):
                cur.execute(
                    f"insert into {db_schema}.ops_issues "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 2, "bad", "unknown"),
                )
    finally:
        conn.close()


def test_pull_request_state_check(db_schema: str) -> None:
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            with pytest.raises(psycopg.errors.CheckViolation):
                cur.execute(
                    f"insert into {db_schema}.ops_pull_requests "
                    "(repo_id, number, title, state, created_at, updated_at) "
                    "values (%s, %s, %s, %s, now(), now())",
                    (repo_id, 2, "bad", "unknown"),
                )
    finally:
        conn.close()


def test_repo_cascade_delete(db_schema: str) -> None:
    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]
            cur.execute(
                f"insert into {db_schema}.ops_issues "
                "(repo_id, number, title, state, created_at, updated_at) "
                "values (%s, %s, %s, %s, now(), now())",
                (repo_id, 3, "cascade test", "open"),
            )
            cur.execute(f"delete from {db_schema}.ops_repos where id = %s", (repo_id,))
            cur.execute(
                f"select 1 from {db_schema}.ops_issues where repo_id = %s", (repo_id,)
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
