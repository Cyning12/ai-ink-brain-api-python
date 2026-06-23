"""Ops Desk P2-1 Graph Ingest 验收（graph.json fixture · mock Supabase）。"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops.graph.router import get_graph_store
from api.ops.graph.store import (
    GraphIngestResult,
    OpsGraphStore,
    ingest_graph_after_github_sync,
)
from api.ops.graph.validator import GraphValidationError, validate_graph_json
from api.ops.sync.runner import run_sync

# ── Fixtures ──────────────────────────────────────────────────────────────

@pytest.fixture
def sample_graph_json() -> dict[str, Any]:
    """基于真实 graph.json 结构的匿名子集。"""
    return {
        "schema_version": "graph_v2",
        "freeze_id": "KIMI-META-GRAPH-V2-BATCH@0fa2d54f",
        "generated_at": "2026-06-18T14:26:55Z",
        "graphs": [
            {
                "id": "00_main",
                "source_yaml_path": "docs/_tech_graph/00_main.graph.yaml",
                "title": "顶层流程总图"
            }
        ],
        "nodes": [
            {"graph_id": "00_main", "id": "AC", "label": "agent-core"},
            {"graph_id": "00_main", "id": "CLI", "label": "kimi CLI / TUI"},
            {"graph_id": "00_main", "id": "SDK", "label": "node-sdk"},
        ],
        "edges": [
            {
                "anchors": [],
                "from": "CLI",
                "graph_id": "00_main",
                "label": "",
                "mark": "->",
                "sync": True,
                "to": "SDK",
                "type": "depends_on",
            }
        ],
    }


@pytest.fixture
def sample_manifest_json() -> dict[str, Any]:
    return {"version": "2.0.3", "preset": "harness-only"}


# ── Fake Supabase（复用 scan 测试模式）───────────────────────────────────────

class FakeSupabase:
    """链式 mock，覆盖 store 使用的 insert/update/select 路径。"""

    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []
        self.inserted: list[dict[str, Any]] = []
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

    def contains(self, _col: str, _value: Any) -> FakeTable:
        self._filters.append(("contains", _col, _value))
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
        if self._name == "ops_graph_snapshots" and self._row is not None:
            resp.data = [{"id": "graph-snapshot-1", **self._row}]
            self._sb.inserted.append(self._row)
        elif self._name == "ops_sync_run_artifacts" and self._row is not None:
            resp.data = [{"id": "artifact-1", **self._row}]
            self._sb.inserted.append(self._row)
        elif self._name == "ops_graph_snapshots" and self._row is None:
            resp.data = self._sb.selected or []
        elif self._name == "ops_issues":
            resp.data = self._sb.selected or []
        else:
            resp.data = []
        return resp


@pytest.fixture
def fake_supabase() -> FakeSupabase:
    return FakeSupabase()


# ── Validator Tests ─────────────────────────────────────────────────────────

class TestValidateGraphJson:
    def test_valid_graph(self, sample_graph_json: dict[str, Any]) -> None:
        meta = validate_graph_json(sample_graph_json)
        assert meta["schema_version"] == "graph_v2"
        assert meta["freeze_id"] == "KIMI-META-GRAPH-V2-BATCH@0fa2d54f"
        assert meta["node_count"] == 3
        assert meta["edge_count"] == 1
        assert meta["graph_count"] == 1

    def test_missing_schema_version(self, sample_graph_json: dict[str, Any]) -> None:
        payload = {k: v for k, v in sample_graph_json.items() if k != "schema_version"}
        with pytest.raises(GraphValidationError, match="schema_version"):
            validate_graph_json(payload)

    def test_missing_freeze_id(self, sample_graph_json: dict[str, Any]) -> None:
        payload = {k: v for k, v in sample_graph_json.items() if k != "freeze_id"}
        with pytest.raises(GraphValidationError, match="freeze_id"):
            validate_graph_json(payload)

    def test_missing_nodes(self, sample_graph_json: dict[str, Any]) -> None:
        payload = {k: v for k, v in sample_graph_json.items() if k != "nodes"}
        with pytest.raises(GraphValidationError, match="nodes"):
            validate_graph_json(payload)

    def test_node_missing_id(self, sample_graph_json: dict[str, Any]) -> None:
        payload = {**sample_graph_json, "nodes": [{"label": "x", "graph_id": "g"}]}
        with pytest.raises(GraphValidationError, match="missing 'id'"):
            validate_graph_json(payload)

    def test_edge_missing_from(self, sample_graph_json: dict[str, Any]) -> None:
        payload = {
            **sample_graph_json,
            "edges": [{"to": "SDK", "type": "depends_on", "graph_id": "g"}],
        }
        with pytest.raises(GraphValidationError, match="missing 'from'"):
            validate_graph_json(payload)

    def test_non_dict_root(self) -> None:
        with pytest.raises(GraphValidationError, match="expected dict"):
            validate_graph_json([])  # type: ignore[arg-type]


# ── Store Tests ─────────────────────────────────────────────────────────────

class TestOpsGraphStore:
    def test_write_snapshot(self, fake_supabase: FakeSupabase) -> None:
        store = OpsGraphStore(repo_id="repo-1", client=fake_supabase)
        payload = {"schema_version": "graph_v2", "nodes": [], "edges": [], "graphs": []}
        snapshot_id = store.write_snapshot(
            payload,
            source_branch="cyning/meta",
            source_commit="abc123",
            manifest_version="2.0.3",
        )
        assert snapshot_id == "graph-snapshot-1"
        assert fake_supabase.calls[0]["table"] == "ops_graph_snapshots"
        row = fake_supabase.calls[0]["row"]
        assert row["repo_id"] == "repo-1"
        assert row["source_branch"] == "cyning/meta"
        assert row["source_commit"] == "abc123"
        assert row["manifest_version"] == "2.0.3"
        assert row["payload"] == payload

    def test_link_artifact(self, fake_supabase: FakeSupabase) -> None:
        store = OpsGraphStore(repo_id="repo-1", client=fake_supabase)
        store.link_artifact("run-1", "graph-snapshot-1", None)

        assert fake_supabase.calls[0]["table"] == "ops_sync_run_artifacts"
        row = fake_supabase.calls[0]["row"]
        assert row["sync_run_id"] == "run-1"
        assert row["graph_snapshot_id"] == "graph-snapshot-1"
        assert row["scan_snapshot_id"] is None

    def test_get_latest_snapshot(self, fake_supabase: FakeSupabase) -> None:
        fake_supabase.selected = [
            {
                "id": "graph-snapshot-2",
                "repo_id": "repo-1",
                "source_branch": "cyning/meta",
                "payload": {"schema_version": "graph_v2"},
                "created_at": "2026-06-21T00:00:00Z",
            }
        ]
        store = OpsGraphStore(repo_id="repo-1", client=fake_supabase)
        snapshot = store.get_latest_snapshot()

        assert snapshot is not None
        assert snapshot["id"] == "graph-snapshot-2"
        call = fake_supabase.calls[0]
        assert call["table"] == "ops_graph_snapshots"
        assert call["order"] == ("created_at", True)
        assert call["limit"] == 1

    def test_get_open_issues_for_module(self, fake_supabase: FakeSupabase) -> None:
        fake_supabase.selected = [
            {
                "number": 123,
                "title": "Fix AC bug",
                "state": "open",
                "labels": ["module:AC"],
                "created_at": "2026-06-01T00:00:00Z",
                "updated_at": "2026-06-21T00:00:00Z",
            }
        ]
        store = OpsGraphStore(repo_id="repo-1", client=fake_supabase)
        issues = store.get_open_issues_for_module("AC")

        assert len(issues) == 1
        assert issues[0]["number"] == 123
        call = fake_supabase.calls[0]
        assert call["table"] == "ops_issues"
        assert any(f == ("state", "open") for f in call["filters"])


# ── Ingest Function Tests ───────────────────────────────────────────────────

class TestIngestGraphAfterGithubSync:
    def test_skips_when_graph_json_missing(self, tmp_path: Path) -> None:
        missing = tmp_path / "no-such-graph.json"
        result = ingest_graph_after_github_sync(
            repo_id="repo-1",
            sync_run_id="run-1",
            graph_json_path=missing,
        )
        assert result.status == "skipped"
        assert "not found" in (result.error_message or "")

    def test_fails_on_invalid_json(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text("not json", encoding="utf-8")
        result = ingest_graph_after_github_sync(
            repo_id="repo-1",
            sync_run_id="run-1",
            graph_json_path=bad,
        )
        assert result.status == "failed"
        assert "JSON decode" in (result.error_message or "")

    def test_fails_on_validation_error(self, tmp_path: Path) -> None:
        bad = tmp_path / "bad.json"
        bad.write_text('{"schema_version": "v1"}', encoding="utf-8")
        result = ingest_graph_after_github_sync(
            repo_id="repo-1",
            sync_run_id="run-1",
            graph_json_path=bad,
        )
        assert result.status == "failed"
        assert "validation" in (result.error_message or "")

    def test_success_with_manifest(self, tmp_path: Path, sample_graph_json: dict[str, Any], sample_manifest_json: dict[str, Any]) -> None:
        graph_path = tmp_path / "graph.json"
        graph_path.write_text(json.dumps(sample_graph_json), encoding="utf-8")
        manifest_path = tmp_path / "manifest.json"
        manifest_path.write_text(json.dumps(sample_manifest_json), encoding="utf-8")

        # 使用 mock client 避免真实 Supabase 调用
        fake = FakeSupabase()
        result = ingest_graph_after_github_sync(
            repo_id="repo-1",
            sync_run_id="run-1",
            graph_json_path=graph_path,
            manifest_json_path=manifest_path,
            source_branch="cyning/meta",
            source_commit="abc123",
            client=fake,
        )
        assert result.status == "success"
        assert result.snapshot_id == "graph-snapshot-1"
        assert result.meta is not None
        assert result.meta["schema_version"] == "graph_v2"

    def test_success_without_manifest(self, tmp_path: Path, sample_graph_json: dict[str, Any]) -> None:
        graph_path = tmp_path / "graph.json"
        graph_path.write_text(json.dumps(sample_graph_json), encoding="utf-8")

        fake = FakeSupabase()
        result = ingest_graph_after_github_sync(
            repo_id="repo-1",
            sync_run_id="run-1",
            graph_json_path=graph_path,
            client=fake,
        )
        assert result.status == "success"
        assert result.snapshot_id == "graph-snapshot-1"


# ── Runner Integration Tests ────────────────────────────────────────────────

class FakeRunStore:
    def __init__(self) -> None:
        self.repo_id = "repo-uuid-1"
        self.runs: list[dict[str, Any]] = []
        self.run_updates: list[dict[str, Any]] = []

    def ensure_repo(self, owner: str = "MoonshotAI", name: str = "kimi-code") -> str:
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


def test_runner_ingests_graph_on_success(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, sample_graph_json: dict[str, Any]
) -> None:
    """runner 成功时调用 graph ingest。"""
    graph_path = tmp_path / "graph.json"
    graph_path.write_text(json.dumps(sample_graph_json), encoding="utf-8")

    captured_graph: dict[str, Any] = {}
    captured_scan: dict[str, Any] = {}

    def fake_scan_ingest(repo_id: str, run_id: str, **kwargs: Any) -> Any:
        captured_scan.update({"repo_id": repo_id, "run_id": run_id, **kwargs})
        from api.ops.scan.store import ScanIngestResult
        return ScanIngestResult(
            snapshot_id="scan-1",
            status="success",
            total_open=100,
            counts={},
        )

    def fake_graph_ingest(repo_id: str, run_id: str, **kwargs: Any) -> GraphIngestResult:
        captured_graph.update({"repo_id": repo_id, "run_id": run_id, **kwargs})
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
    assert result.graph_snapshot_id == "graph-1"
    assert captured_graph["repo_id"] == store.repo_id


def test_runner_partial_when_graph_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """graph ingest 失败时 runner 返回 partial。"""
    def fake_scan_ingest(_repo_id: str, _run_id: str, **kwargs: Any) -> Any:
        from api.ops.scan.store import ScanIngestResult
        return ScanIngestResult(
            snapshot_id="scan-1",
            status="success",
            total_open=100,
            counts={},
        )

    def fake_graph_ingest(_repo_id: str, _run_id: str, **kwargs: Any) -> GraphIngestResult:
        return GraphIngestResult(
            snapshot_id=None,
            status="skipped",
            meta=None,
            error_message="graph.json not found",
        )

    monkeypatch.setattr("api.ops.sync.runner.ingest_scan_after_github_sync", fake_scan_ingest)
    monkeypatch.setattr("api.ops.sync.runner.ingest_graph_after_github_sync", fake_graph_ingest)

    store = FakeRunStore()
    result = run_sync(trigger="manual", github=FakeGitHubEmpty(), store=store)  # type: ignore[arg-type]

    assert result.status == "partial"
    assert result.graph_snapshot_id is None
    assert "graph.json not found" in (result.error_message or "")
    assert store.runs[-1]["status"] == "partial"


def test_runner_partial_when_scan_and_graph_both_fail(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """scan 和 graph 都失败时返回 partial，错误信息合并。"""
    def fake_scan_ingest(_repo_id: str, _run_id: str, **kwargs: Any) -> Any:
        from api.ops.scan.store import ScanIngestResult
        return ScanIngestResult(
            snapshot_id=None,
            status="skipped",
            total_open=None,
            counts={},
            error_message="scan index missing",
        )

    def fake_graph_ingest(_repo_id: str, _run_id: str, **kwargs: Any) -> GraphIngestResult:
        return GraphIngestResult(
            snapshot_id=None,
            status="failed",
            meta=None,
            error_message="graph.json invalid",
        )

    monkeypatch.setattr("api.ops.sync.runner.ingest_scan_after_github_sync", fake_scan_ingest)
    monkeypatch.setattr("api.ops.sync.runner.ingest_graph_after_github_sync", fake_graph_ingest)

    store = FakeRunStore()
    result = run_sync(trigger="manual", github=FakeGitHubEmpty(), store=store)  # type: ignore[arg-type]

    assert result.status == "partial"
    assert "scan index missing" in (result.error_message or "")
    assert "graph.json invalid" in (result.error_message or "")


# ── API Router Tests ────────────────────────────────────────────────────────

class FakeGraphStore:
    def __init__(self, snapshot: dict[str, Any] | None) -> None:
        self._snapshot = snapshot

    def get_latest_snapshot(self) -> dict[str, Any] | None:
        return self._snapshot

    def get_open_issues_for_module(self, module_id: str) -> list[dict[str, Any]]:
        return [
            {
                "number": 123,
                "title": f"Issue for {module_id}",
                "state": "open",
                "labels": [f"module:{module_id}"],
            }
        ]


@pytest.fixture
def graph_client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("OPS_DESK_SECRET", "test")
    snapshot = {
        "id": "graph-snapshot-1",
        "source_branch": "cyning/meta",
        "source_commit": "abc123",
        "manifest_version": "2.0.3",
        "payload": {
            "schema_version": "graph_v2",
            "freeze_id": "KIMI-META-GRAPH-V2-BATCH@0fa2d54f",
            "graphs": [
                {"id": "00_main", "title": "顶层流程总图"}
            ],
            "nodes": [
                {"graph_id": "00_main", "id": "AC", "label": "agent-core"},
                {"graph_id": "00_main", "id": "CLI", "label": "kimi CLI"},
            ],
            "edges": [
                {"from": "CLI", "to": "SDK", "type": "depends_on", "graph_id": "00_main"}
            ],
        },
        "created_at": "2026-06-21T00:00:00Z",
    }
    app.dependency_overrides[get_graph_store] = lambda: FakeGraphStore(snapshot)
    yield TestClient(app)
    app.dependency_overrides.clear()


class TestGraphSummaryAPI:
    def test_graph_summary_ok(self, graph_client: TestClient) -> None:
        resp = graph_client.get("/api/py/ops/graph/summary", headers={"x-ops-secret": "test"})
        assert resp.status_code == 200
        data = resp.json()
        assert data["snapshot_id"] == "graph-snapshot-1"
        assert data["source_branch"] == "cyning/meta"
        assert data["source_commit"] == "abc123"
        assert data["manifest_version"] == "2.0.3"
        assert data["schema_version"] == "graph_v2"
        assert data["freeze_id"] == "KIMI-META-GRAPH-V2-BATCH@0fa2d54f"
        assert data["node_count"] == 2
        assert data["edge_count"] == 1
        assert data["graph_count"] == 1
        assert len(data["graphs"]) == 1
        assert data["graphs"][0]["id"] == "00_main"

    def test_graph_summary_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("OPS_DESK_SECRET", "")
        app.dependency_overrides[get_graph_store] = lambda: FakeGraphStore(None)
        client = TestClient(app)
        try:
            resp = client.get("/api/py/ops/graph/summary", headers={"x-ops-secret": "test"})
            assert resp.status_code == 404
            assert resp.json()["detail"]["code"] == "GRAPH_SNAPSHOT_NOT_FOUND"
        finally:
            app.dependency_overrides.clear()

    def test_graph_summary_secret_missing(self, graph_client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("OPS_DESK_SECRET", "required")
        resp = graph_client.get("/api/py/ops/graph/summary")
        assert resp.status_code == 401


class TestModuleIssuesAPI:
    def test_module_issues_ok(self, graph_client: TestClient) -> None:
        resp = graph_client.get("/api/py/ops/graph/module-issues?state=open", headers={"x-ops-secret": "test"})
        assert resp.status_code == 200
        data = resp.json()
        assert "modules" in data
        assert len(data["modules"]) == 2
        # AC module
        ac = next(m for m in data["modules"] if m["module_id"] == "AC")
        assert ac["label"] == "agent-core"
        assert ac["open_issue_count"] == 1
        assert len(ac["sample_issues"]) == 1
        assert ac["sample_issues"][0]["number"] == 123

    def test_module_issues_not_found(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("OPS_DESK_SECRET", "")
        app.dependency_overrides[get_graph_store] = lambda: FakeGraphStore(None)
        client = TestClient(app)
        try:
            resp = client.get("/api/py/ops/graph/module-issues", headers={"x-ops-secret": "test"})
            assert resp.status_code == 404
            assert resp.json()["detail"]["code"] == "GRAPH_SNAPSHOT_NOT_FOUND"
        finally:
            app.dependency_overrides.clear()


# ── Fixture File Tests ──────────────────────────────────────────────────────

def test_fixture_graph_snapshot_sample_exists() -> None:
    root = Path(__file__).resolve().parents[2]
    fixture = root / "tests" / "fixtures" / "graph_snapshot_sample_v1.json"
    assert fixture.exists()
    data = json.loads(fixture.read_text(encoding="utf-8"))
    assert data["schema_version"] == "graph_v2"
    assert "nodes" in data
    assert "edges" in data
    assert "graphs" in data


def test_fixture_parses_with_validator() -> None:
    root = Path(__file__).resolve().parents[2]
    fixture = root / "tests" / "fixtures" / "graph_snapshot_sample_v1.json"
    data = json.loads(fixture.read_text(encoding="utf-8"))
    meta = validate_graph_json(data)
    assert meta["node_count"] == 3
    assert meta["edge_count"] == 1


# ── DDL Tests ─────────────────────────────────────────────────────────────────

def test_ddl_and_rollback_files_exist() -> None:
    root = Path(__file__).resolve().parents[2]
    ddl = root / "supabase" / "sql" / "ops_desk_p2_scan_schema.sql"
    rollback = root / "supabase" / "sql" / "ops_desk_p2_scan_schema_rollback.sql"
    assert ddl.exists()
    assert rollback.exists()
    rollback_sql = rollback.read_text(encoding="utf-8")
    for table in ("ops_sync_run_artifacts", "ops_graph_snapshots", "ops_scan_snapshots"):
        assert f"drop table if exists public.{table}" in rollback_sql


def test_ops_graph_store_has_required_methods() -> None:
    assert callable(OpsGraphStore.write_snapshot)
    assert callable(OpsGraphStore.link_artifact)
    assert callable(OpsGraphStore.get_latest_snapshot)
    assert callable(OpsGraphStore.get_open_issues_for_module)
