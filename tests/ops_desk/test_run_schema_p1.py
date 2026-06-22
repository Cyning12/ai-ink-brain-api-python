"""Ops Desk P1 Run Schema DDL 与存储层测试。"""

from __future__ import annotations

import os
import uuid
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

REPO_ROOT = Path(__file__).resolve().parents[2]
if load_dotenv is not None:
    load_dotenv(REPO_ROOT / ".env.local", override=False)
    load_dotenv(REPO_ROOT / ".env", override=False)

SCHEMA_PATH = REPO_ROOT / "supabase" / "sql" / "ops_desk_p1_run_schema.sql"
ROLLBACK_PATH = REPO_ROOT / "supabase" / "sql" / "ops_desk_p1_run_schema_rollback.sql"
P0_SCHEMA_PATH = REPO_ROOT / "supabase" / "sql" / "ops_desk_p0_schema.sql"
P0_ROLLBACK_PATH = REPO_ROOT / "supabase" / "sql" / "ops_desk_p0_schema_rollback.sql"


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
            for t in ("ops_runs", "ops_run_events", "ops_run_checkpoints")
            if _table_exists(conn, schema_name, t)
        ]
        if not existing:
            # P1 run schema 依赖 P0 repos 表
            if not _table_exists(conn, schema_name, "ops_repos"):
                try:
                    with conn.cursor() as cur:
                        cur.execute(_read_sql(P0_ROLLBACK_PATH))
                        cur.execute(_read_sql(P0_SCHEMA_PATH))
                except psycopg.errors.InsufficientPrivilege as exc:
                    pytest.skip(f"当前数据库用户无 DDL 权限: {exc}")
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
                if not _table_exists(conn, schema_name, "ops_issues"):
                    cur.execute(_read_sql(P0_ROLLBACK_PATH))
        conn.close()


def _require_writable(info: SchemaInfo) -> None:
    if not info.created_by_us:
        pytest.skip("public 中表已存在，跳过写测试以避免破坏数据")


def test_three_tables_exist(db_schema: SchemaInfo) -> None:
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        for table in ("ops_runs", "ops_run_events", "ops_run_checkpoints"):
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


def test_runs_columns_and_constraints(db_schema: SchemaInfo) -> None:
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (db_schema.name, "ops_runs"),
            )
            columns = {row[0] for row in cur.fetchall()}
            for col in (
                "id", "repo_id", "session_id", "query", "route", "status",
                "final_answer", "retry_token", "created_at", "updated_at",
            ):
                assert col in columns, f"ops_runs 缺少列 {col}"

        defs = _get_constraint_defs(conn, db_schema.name, "ops_runs")
        joined = "\n".join(defs)
        assert "FOREIGN KEY (repo_id) REFERENCES ops_repos(id) ON DELETE CASCADE" in joined
        for status in ("queued", "running", "done", "failed", "partial"):
            assert status in joined, f"ops_runs status CHECK 缺少 {status}"
        for route in ("fast", "deep"):
            assert route in joined, f"ops_runs route CHECK 缺少 {route}"
    finally:
        conn.close()


def test_events_columns_and_unique_seq(db_schema: SchemaInfo) -> None:
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (db_schema.name, "ops_run_events"),
            )
            columns = {row[0] for row in cur.fetchall()}
            for col in ("id", "run_id", "seq", "ts_ms", "node_id", "agent_role", "event_type", "payload", "created_at"):
                assert col in columns, f"ops_run_events 缺少列 {col}"

        defs = _get_constraint_defs(conn, db_schema.name, "ops_run_events")
        joined = "\n".join(defs)
        assert "UNIQUE (run_id, seq)" in joined
        assert "FOREIGN KEY (run_id) REFERENCES ops_runs(id) ON DELETE CASCADE" in joined
    finally:
        conn.close()


def test_checkpoints_columns_and_constraints(db_schema: SchemaInfo) -> None:
    dsn = _dsn()
    assert dsn
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                "select column_name from information_schema.columns "
                "where table_schema = %s and table_name = %s",
                (db_schema.name, "ops_run_checkpoints"),
            )
            columns = {row[0] for row in cur.fetchall()}
            for col in ("id", "run_id", "checkpoint_id", "state_json", "created_at"):
                assert col in columns, f"ops_run_checkpoints 缺少列 {col}"

        defs = _get_constraint_defs(conn, db_schema.name, "ops_run_checkpoints")
        joined = "\n".join(defs)
        assert "UNIQUE (run_id, checkpoint_id)" in joined
    finally:
        conn.close()


def test_run_events_seq_monotonic_and_unique(db_schema: SchemaInfo) -> None:
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
                f"insert into {db_schema.name}.ops_runs (repo_id, query, route, status) values (%s, %s, %s, %s) returning id",
                (repo_id, "test query", "deep", "running"),
            )
            run_id = cur.fetchone()[0]
            cur.execute(
                f"insert into {db_schema.name}.ops_run_events (run_id, seq, ts_ms, agent_role, event_type) values (%s, %s, %s, %s, %s)",
                (run_id, 1, 1, "orchestrator", "run.start"),
            )
            cur.execute(
                f"insert into {db_schema.name}.ops_run_events (run_id, seq, ts_ms, agent_role, event_type) values (%s, %s, %s, %s, %s)",
                (run_id, 2, 2, "issue_analyst", "agent.tool.result"),
            )
            with pytest.raises(psycopg.errors.UniqueViolation):
                cur.execute(
                    f"insert into {db_schema.name}.ops_run_events (run_id, seq, ts_ms, agent_role, event_type) values (%s, %s, %s, %s, %s)",
                    (run_id, 2, 3, "review", "review.pass"),
                )
    finally:
        conn.close()


def test_store_layer_upsert_and_events(db_schema: SchemaInfo, monkeypatch: pytest.MonkeyPatch) -> None:
    """通过 OpsRunStore 验证 append_event seq++ 与查询。"""
    _require_writable(db_schema)
    from api.ops.store import OpsRunStore

    dsn = _dsn()
    conn = psycopg.connect(dsn)
    try:
        with conn.cursor() as cur:
            cur.execute(
                f"insert into {db_schema.name}.ops_repos (owner, name) values (%s, %s) returning id",
                ("MoonshotAI", "kimi-code"),
            )
            repo_id = cur.fetchone()[0]

        # 使用真实 supabase client 需要 URL/key；这里直接通过 psycopg 构造一个 mock client
        class FakeClient:
            def __init__(self, connection) -> None:
                self._conn = connection

            class _Table:
                def __init__(self, conn, name: str) -> None:
                    self._conn = conn
                    self._name = name
                    self._select = "*"
                    self._filters = []
                    self._order = None
                    self._limit = None
                    self._count = None
                    self._data = None

                def select(self, *cols, count=None):
                    self._select = ",".join(cols) if cols else "*"
                    self._count = count
                    return self

                def eq(self, column, value):
                    self._filters.append(("eq", column, value))
                    return self

                def gt(self, column, value):
                    self._filters.append(("gt", column, value))
                    return self

                def order(self, column, desc=False):
                    self._order = (column, "desc" if desc else "asc")
                    return self

                def limit(self, n):
                    self._limit = n
                    return self

                def insert(self, row):
                    self._data = row
                    return self

                def update(self, row):
                    self._data = row
                    return self

                def execute(self):
                    with self._conn.cursor() as cur:
                        if self._data:
                            if self._name == "ops_runs":
                                cur.execute(
                                    f"insert into {db_schema.name}.ops_runs (repo_id, query, route, status, session_id) values (%s, %s, %s, %s, %s) returning *",
                                    (
                                        self._data.get("repo_id"),
                                        self._data.get("query"),
                                        self._data.get("route"),
                                        self._data.get("status"),
                                        self._data.get("session_id"),
                                    ),
                                )
                            elif self._name == "ops_run_events":
                                cur.execute(
                                    f"insert into {db_schema.name}.ops_run_events (run_id, seq, ts_ms, node_id, agent_role, event_type, payload) values (%s, %s, %s, %s, %s, %s, %s) returning *",
                                    (
                                        self._data.get("run_id"),
                                        self._data.get("seq"),
                                        self._data.get("ts_ms"),
                                        self._data.get("node_id"),
                                        self._data.get("agent_role"),
                                        self._data.get("event_type"),
                                        self._data.get("payload"),
                                    ),
                                )
                            elif self._name == "ops_run_checkpoints":
                                cur.execute(
                                    f"insert into {db_schema.name}.ops_run_checkpoints (run_id, checkpoint_id, state_json) values (%s, %s, %s) on conflict (run_id, checkpoint_id) do update set state_json=excluded.state_json returning *",
                                    (
                                        self._data.get("run_id"),
                                        self._data.get("checkpoint_id"),
                                        self._data.get("state_json"),
                                    ),
                                )
                            row = cur.fetchone()
                            cols = [desc[0] for desc in cur.description]
                            return type("Res", (), {"data": [dict(zip(cols, row))]})

                        where = " and ".join(
                            f"{c} = %s" if op == "eq" else f"{c} > %s"
                            for op, c, _ in self._filters
                        )
                        params = [v for _, _, v in self._filters]
                        q = f"select {self._select} from {db_schema.name}.{self._name}"
                        if where:
                            q += f" where {where}"
                        if self._order:
                            q += f" order by {self._order[0]} {self._order[1]}"
                        if self._limit:
                            q += f" limit {self._limit}"
                        cur.execute(q, params)
                        rows = [dict(zip([desc[0] for desc in cur.description], row)) for row in cur.fetchall()]
                        res = type("Res", (), {"data": rows})
                        if self._count:
                            cur.execute(f"select count(*) from {db_schema.name}.{self._name} where {where}" if where else f"select count(*) from {db_schema.name}.{self._name}", params)
                            res.count = cur.fetchone()[0]
                        return res

            def table(self, name: str):
                return self._Table(self._conn, name)

        store = OpsRunStore(FakeClient(conn))
        run = store.create_run("#545 适合我吗", "deep")
        assert run["query"] == "#545 适合我吗"
        assert run["route"] == "deep"

        evt1 = store.append_event(run["id"], "orchestrator", "run.start")
        assert evt1["seq"] == 1
        evt2 = store.append_event(run["id"], "issue_analyst", "agent.tool.result", payload={"issue": 545})
        assert evt2["seq"] == 2

        events = store.get_events(run["id"], after_seq=0)
        assert len(events) == 2
        assert events[0]["seq"] == 1
        assert events[1]["seq"] == 2

        cp = store.save_checkpoint(run["id"], "cp-1", {"foo": "bar"})
        assert cp["checkpoint_id"] == "cp-1"
    finally:
        conn.close()
