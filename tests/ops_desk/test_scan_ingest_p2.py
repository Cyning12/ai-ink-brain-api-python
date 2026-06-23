"""Ops Desk P2-2 Scan Ingest 验收（markdown fixture · mock Supabase）。"""

from __future__ import annotations

from datetime import datetime
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops.graph.store import GraphIngestResult
from api.ops.scan.parser import parse_issue_scan
from api.ops.scan.router import get_scan_store
from api.ops.scan.store import (
    OpsScanStore,
    ScanIngestResult,
    ingest_scan_after_github_sync,
)
from api.ops.sync.runner import run_sync

SAMPLE_ISSUE_SCAN = """\
# Issue 扫描 · MoonshotAI/kimi-code（C2/C3 · 主索引 · v1）

| 项        | 内容                                                                                                             |
| -------- | -------------------------------------------------------------------------------------------------------------- |
| **状态**   | `active`                                                                                                       |
| **版本**   | v1.5.4                                                                                                         |
| **日期**   | 2026-06-21（复扫 · open **184** · +14 vs v1.5.3）                                                                  |
| **扫描源**  | [MoonshotAI/kimi-code Issues](https://github.com/MoonshotAI/kimi-code/issues)（`is:issue state:open` · **184**） |

---

## 1. 总览（2026-06-21）

| 轨            | 项                                                               | 状态                                                                          |
| ------------ | --------------------------------------------------------------- | --------------------------------------------------------------------------- |
| **C1**       | #565 → [#622](https://github.com/MoonshotAI/kimi-code/pull/622) | **MERGED**                                                                  |
| **C2**       | #583 → [#630](https://github.com/MoonshotAI/kimi-code/pull/630) | OPEN · Codex P2                                                             |
| **C3 P0**    | #94 → [#708](https://github.com/MoonshotAI/kimi-code/pull/708)  | **本 fork OPEN** · CI 绿 · 无 maintainer review                                |
| **C3 P0′**   | #437 → [#901](https://github.com/MoonshotAI/kimi-code/pull/901) | **本 fork OPEN** · CI 绿 · `Fixes #437` · meta **done**                       |
| **C3 P1 暂缓** | #705/#701/#660 · #704 · #751 · #792                             | 他人 PR 占坑                                                                  |
| **C3 P2 次优** | **#545**（下一张无 PR **首选**）· #476 · #659                           | 候选                                                                          |
| **C3 P3 观察** | #794 · #796 · **6/18–6/20 新 open**（#870–#872）                   | 观察                                                                          |

## 2. 扫描方法（可复跑）

```bash
gh api 'search/issues?q=repo:MoonshotAI/kimi-code+is:issue+is:open&per_page=1' --jq '.total_count'
```

## 3. C2 · #583（PR OPEN）

占位。

## 4. C3 P0 · #94 → [#708](https://github.com/MoonshotAI/kimi-code/pull/708)

占位。
"""


def test_parser_extracts_version_and_total_open() -> None:
    parsed = parse_issue_scan(SAMPLE_ISSUE_SCAN, raw_url="https://example.com/scan.md")
    assert parsed["scan_version"] == "v1.5.4"
    assert parsed["total_open"] == 184


def test_parser_extracts_tier_items() -> None:
    parsed = parse_issue_scan(SAMPLE_ISSUE_SCAN)
    p0_numbers = [item["number"] for item in parsed["p0_items"]]
    p1_numbers = [item["number"] for item in parsed["p1_items"]]
    p2_numbers = [item["number"] for item in parsed["p2_items"]]
    deferred_numbers = [item["number"] for item in parsed["deferred_items"]]

    assert p0_numbers == [94, 437]
    assert p1_numbers == [705, 701, 660, 704, 751, 792]
    assert p2_numbers == [545, 476, 659]
    assert deferred_numbers == [794, 796, 870, 871, 872]


def test_parser_maps_scan_tags_by_number() -> None:
    parsed = parse_issue_scan(SAMPLE_ISSUE_SCAN)
    tags = parsed["tags_by_number"]
    assert tags[583] == ["C2"]
    assert tags[94] == ["C3-P0"]
    assert tags[437] == ["C3-P0"]
    assert tags[545] == ["C3-P2"]
    assert tags[870] == ["OBSERVE"]
    assert tags[872] == ["OBSERVE"]


def test_parser_includes_raw_url_in_summary() -> None:
    parsed = parse_issue_scan(SAMPLE_ISSUE_SCAN, raw_url="https://example.com/scan.md")
    assert parsed["raw_markdown_url"] == "https://example.com/scan.md"
    assert parsed["parsed_summary"]["version"] == "v1.5.4"
    assert any(section["tier"] == "C3-P0" for section in parsed["parsed_summary"]["sections"])


def _parsed_sample() -> dict[str, Any]:
    return parse_issue_scan(SAMPLE_ISSUE_SCAN, raw_url="https://example.com/scan.md")


class FakeSupabase:
    """链式 mock，覆盖 store 使用的 insert/update/select 路径。"""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.inserted: list[dict[str, Any]] = []
        self.updated: list[dict[str, Any]] = []
        self.selected: list[dict[str, Any]] | None = None

    def table(self, name: str) -> FakeTable:
        return FakeTable(self, name)


class FakeTable:
    def __init__(self, sb: FakeSupabase, name: str) -> None:
        self._sb = sb
        self._name = name
        self._row: dict[str, Any] | None = None
        self._filters: list[tuple[str, Any]] = []
        self._ordering: tuple[str, bool] | None = None
        self._limit: int | None = None

    def insert(self, row: dict[str, Any]) -> FakeTable:
        self._row = row
        return self

    def update(self, row: dict[str, Any]) -> FakeTable:
        self._row = row
        return self

    def select(self, *_cols: str) -> FakeTable:
        return self

    def eq(self, _col: str, _value: Any) -> FakeTable:
        self._filters.append((_col, _value))
        return self

    def order(self, col: str, *, desc: bool = False) -> FakeTable:
        self._ordering = (col, desc)
        return self

    def limit(self, n: int) -> FakeTable:
        self._limit = n
        return self

    def execute(self) -> MagicMock:
        call: dict[str, Any] = {"table": self._name, "filters": self._filters}
        if self._row is not None:
            call["row"] = self._row
        if self._ordering is not None:
            call["order"] = self._ordering
        if self._limit is not None:
            call["limit"] = self._limit
        self._sb.calls.append(call)

        resp = MagicMock()
        if self._name == "ops_scan_snapshots" and self._row is not None:
            resp.data = [{"id": "snapshot-1", **self._row}]
            self._sb.inserted.append(self._row)
        elif self._name == "ops_issues" and self._row is not None:
            number = next((v for c, v in self._filters if c == "number"), None)
            if number == 999:
                resp.data = []
            else:
                resp.data = [{"number": number, "scan_tags": self._row.get("scan_tags")}]
            self._sb.updated.append(self._row)
        elif self._name == "ops_sync_run_artifacts" and self._row is not None:
            resp.data = [{"id": "artifact-1", **self._row}]
            self._sb.inserted.append(self._row)
        elif self._name == "ops_scan_snapshots" and self._row is None:
            resp.data = self._sb.selected or []
        else:
            resp.data = []
        return resp


@pytest.fixture
def fake_supabase() -> FakeSupabase:
    return FakeSupabase()


def test_store_write_snapshot(fake_supabase: FakeSupabase) -> None:
    store = OpsScanStore(repo_id="repo-1", client=fake_supabase)
    parsed = _parsed_sample()
    snapshot_id = store.write_snapshot(parsed)

    assert snapshot_id == "snapshot-1"
    assert fake_supabase.calls[0]["table"] == "ops_scan_snapshots"
    row = fake_supabase.calls[0]["row"]
    assert row["repo_id"] == "repo-1"
    assert row["scan_version"] == "v1.5.4"
    assert row["total_open"] == 184
    assert len(row["p0_items"]) == 2
    assert len(row["deferred_items"]) == 5
    assert row["raw_markdown_url"] == "https://example.com/scan.md"


def test_store_backfill_scan_tags(fake_supabase: FakeSupabase) -> None:
    store = OpsScanStore(repo_id="repo-1", client=fake_supabase)
    tags = {94: ["C3-P0"], 437: ["C3-P0"], 999: ["C3-P2"]}
    updated = store.backfill_scan_tags(tags)

    assert updated == 2
    assert all(call["table"] == "ops_issues" for call in fake_supabase.calls)
    issue_numbers = [call["filters"][1][1] for call in fake_supabase.calls]
    assert issue_numbers == [94, 437, 999]


def test_store_link_artifact(fake_supabase: FakeSupabase) -> None:
    store = OpsScanStore(repo_id="repo-1", client=fake_supabase)
    store.link_artifact("run-1", "snapshot-1", None)

    assert fake_supabase.calls[0]["table"] == "ops_sync_run_artifacts"
    row = fake_supabase.calls[0]["row"]
    assert row["sync_run_id"] == "run-1"
    assert row["scan_snapshot_id"] == "snapshot-1"
    assert row["graph_snapshot_id"] is None


def test_store_get_latest_snapshot(fake_supabase: FakeSupabase) -> None:
    fake_supabase.selected = [
        {
            "id": "snapshot-2",
            "repo_id": "repo-1",
            "scan_version": "v1.5.4",
            "p0_items": [{"number": 94}],
            "created_at": "2026-06-21T00:00:00Z",
        }
    ]
    store = OpsScanStore(repo_id="repo-1", client=fake_supabase)
    snapshot = store.get_latest_snapshot()

    assert snapshot is not None
    assert snapshot["id"] == "snapshot-2"
    assert snapshot["scan_version"] == "v1.5.4"
    call = fake_supabase.calls[0]
    assert call["table"] == "ops_scan_snapshots"
    assert call["order"] == ("created_at", True)
    assert call["limit"] == 1


class FakeRunStore:
    def __init__(self) -> None:
        self.repo_id = "repo-uuid-1"
        self.runs: list[dict[str, Any]] = []
        self.run_updates: list[dict[str, Any]] = []

    def ensure_repo(self, owner: str = "MoonshotAI", name: str = "kimi-code") -> str:
        assert owner == "MoonshotAI"
        assert name == "kimi-code"
        return self.repo_id

    def get_last_success_cursor(self, repo_id: str) -> datetime | None:
        return None

    def has_any_sync_run(self, repo_id: str) -> bool:
        return False

    def create_sync_run(self, repo_id: str, trigger: str) -> str:
        run_id = f"run-{len(self.runs) + 1}"
        self.runs.append({"id": run_id, "status": "pending", "trigger": trigger})
        return run_id

    def update_sync_run(self, run_id: str, **fields: Any) -> None:
        self.run_updates.append({"run_id": run_id, **fields})
        for run in self.runs:
            if run["id"] == run_id:
                run.update(fields)

    def upsert_issue(self, repo_id: str, issue: dict[str, Any]) -> None:
        pass

    def upsert_pull_request(self, repo_id: str, pr: dict[str, Any]) -> None:
        pass


class FakeGitHubEmpty:
    def fetch_issues(self, since: datetime | None) -> list[dict[str, Any]]:
        return []

    def fetch_pull_requests(self, since: datetime | None) -> list[dict[str, Any]]:
        return []


def test_runner_ingests_scan_on_success(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, Any] = {}

    def fake_scan_ingest(repo_id: str, run_id: str, **kwargs: Any) -> ScanIngestResult:
        captured.update({"repo_id": repo_id, "run_id": run_id, **kwargs})
        return ScanIngestResult(
            snapshot_id="scan-1",
            status="success",
            total_open=184,
            counts={"C3-P0": 2, "C3-P1": 6, "C3-P2": 3, "OBSERVE": 5},
        )

    def fake_graph_ingest(_repo_id: str, _run_id: str, **_: Any) -> GraphIngestResult:
        return GraphIngestResult(
            snapshot_id="graph-1",
            status="success",
            meta={"node_count": 3},
        )

    monkeypatch.setattr("api.ops.sync.runner.ingest_scan_after_github_sync", fake_scan_ingest)
    monkeypatch.setattr("api.ops.sync.runner.ingest_graph_after_github_sync", fake_graph_ingest)

    store = FakeRunStore()
    result = run_sync(trigger="manual", github=FakeGitHubEmpty(), store=store)  # type: ignore[arg-type]

    assert result.status == "success"
    assert result.scan_snapshot_id == "scan-1"
    assert captured["repo_id"] == store.repo_id
    assert captured["run_id"].startswith("run-")


def test_runner_partial_when_scan_fails(monkeypatch: pytest.MonkeyPatch) -> None:
    def fake_scan_ingest(_repo_id: str, _run_id: str, **kwargs: Any) -> ScanIngestResult:
        return ScanIngestResult(
            snapshot_id=None,
            status="skipped",
            total_open=None,
            counts={},
            error_message="scan index not found",
        )

    def fake_graph_ingest(_repo_id: str, _run_id: str, **_: Any) -> GraphIngestResult:
        return GraphIngestResult(
            snapshot_id="graph-1",
            status="success",
            meta={"node_count": 3},
        )

    monkeypatch.setattr("api.ops.sync.runner.ingest_scan_after_github_sync", fake_scan_ingest)
    monkeypatch.setattr("api.ops.sync.runner.ingest_graph_after_github_sync", fake_graph_ingest)

    store = FakeRunStore()
    result = run_sync(trigger="manual", github=FakeGitHubEmpty(), store=store)  # type: ignore[arg-type]

    assert result.status == "partial"
    assert result.scan_snapshot_id is None
    assert "scan index not found" in (result.error_message or "")
    assert store.runs[-1]["status"] == "partial"


class FakeScanStore:
    def __init__(self, snapshot: dict[str, Any] | None) -> None:
        self._snapshot = snapshot

    def get_latest_snapshot(self) -> dict[str, Any] | None:
        return self._snapshot

    def write_snapshot(self, parsed: dict[str, Any]) -> str:
        return "snapshot-1"


@pytest.fixture
def summary_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("OPS_DESK_SECRET", "test")
    snapshot = {
        "id": "snapshot-1",
        "scan_version": "v1.5.4",
        "total_open": 184,
        "p0_items": [{"number": 94}, {"number": 437}],
        "p1_items": [{"number": 705}],
        "p2_items": [{"number": 545}],
        "deferred_items": [{"number": 794}, {"number": 870}, {"number": 871}],
        "raw_markdown_url": "https://example.com/scan.md",
        "parsed_summary": {"version": "v1.5.4"},
        "created_at": "2026-06-21T00:00:00Z",
    }
    app.dependency_overrides[get_scan_store] = lambda: FakeScanStore(snapshot)
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_scan_summary_ok(summary_client: TestClient) -> None:
    resp = summary_client.get("/api/py/ops/scan/summary", headers={"x-ops-secret": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["scan_version"] == "v1.5.4"
    assert data["total_open"] == 184
    assert data["p0_count"] == 2
    assert data["p1_count"] == 1
    assert data["p2_count"] == 1
    assert data["deferred_count"] == 3


def test_scan_summary_not_found(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "")
    app.dependency_overrides[get_scan_store] = lambda: FakeScanStore(None)
    client = TestClient(app)
    try:
        resp = client.get("/api/py/ops/scan/summary", headers={"x-ops-secret": "test"})
        assert resp.status_code == 404
        assert resp.json()["detail"]["code"] == "SCAN_SNAPSHOT_NOT_FOUND"
    finally:
        app.dependency_overrides.clear()


def test_scan_summary_secret_missing(summary_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET", "required")
    resp = summary_client.get("/api/py/ops/scan/summary")
    assert resp.status_code == 401


def test_ingest_function_skips_when_index_missing(tmp_path: pytest.TempPathFactory) -> None:
    missing = tmp_path / "no-such-scan.md"
    result = ingest_scan_after_github_sync(
        repo_id="repo-1",
        sync_run_id="run-1",
        index_path=missing,
    )
    assert result.status == "skipped"
    assert result.error_message is not None
    assert "not found" in result.error_message


def test_ddl_and_rollback_files_exist() -> None:
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    ddl = root / "supabase" / "sql" / "ops_desk_p2_scan_schema.sql"
    rollback = root / "supabase" / "sql" / "ops_desk_p2_scan_schema_rollback.sql"
    assert ddl.exists()
    assert rollback.exists()
    rollback_sql = rollback.read_text(encoding="utf-8")
    for table in ("ops_sync_run_artifacts", "ops_graph_snapshots", "ops_scan_snapshots"):
        assert f"drop table if exists public.{table}" in rollback_sql


def test_ddl_parses_with_pglast() -> None:
    from pathlib import Path

    pytest.importorskip("pglast")
    import pglast

    root = Path(__file__).resolve().parents[2]
    ddl = (root / "supabase" / "sql" / "ops_desk_p2_scan_schema.sql").read_text(encoding="utf-8")
    rollback = (root / "supabase" / "sql" / "ops_desk_p2_scan_schema_rollback.sql").read_text(encoding="utf-8")
    ddl_stmts = pglast.parse_sql(ddl)
    rollback_stmts = pglast.parse_sql(rollback)
    assert len(ddl_stmts) == 7  # extension + 3 tables + 3 indexes
    assert len(rollback_stmts) == 3


def test_ops_scan_store_has_required_methods() -> None:
    assert callable(OpsScanStore.write_snapshot)
    assert callable(OpsScanStore.backfill_scan_tags)
    assert callable(OpsScanStore.link_artifact)
    assert callable(OpsScanStore.get_latest_snapshot)
