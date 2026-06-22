"""Ops Desk P0-2 GitHub sync 验收（mock · 无外呼）。"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from unittest.mock import MagicMock

import pytest

from api.ops.scan.store import ScanIngestResult
from api.ops.sync.github_client import (
    FAIL_FAST_STATUS,
    MAX_RETRIES,
    RETRYABLE_STATUS,
    GitHubClient,
    GitHubSyncError,
)
from api.ops.sync.runner import run_sync
from api.ops.sync.store import OpsSyncStore, resolve_trigger


@pytest.fixture(autouse=True)
def _stub_scan_ingest(monkeypatch: pytest.MonkeyPatch) -> None:
    """P0 sync 测试不依赖真实 ISSUE_SCAN 文件；扫描步骤默认返回成功。"""

    def fake_ingest(_repo_id: str, _run_id: str, **_: Any) -> ScanIngestResult:
        return ScanIngestResult(
            snapshot_id="scan-1",
            status="success",
            total_open=0,
            counts={},
        )

    monkeypatch.setattr("api.ops.sync.runner.ingest_scan_after_github_sync", fake_ingest)


def _issue(number: int, updated_at: str = "2026-06-01T10:00:00Z") -> dict[str, Any]:
    return {
        "number": number,
        "title": f"Issue {number}",
        "body": "body",
        "state": "open",
        "labels": [{"name": "bug"}],
        "assignees": [{"login": "dev1"}],
        "milestone": None,
        "created_at": "2026-06-01T09:00:00Z",
        "updated_at": updated_at,
        "closed_at": None,
        "user": {"login": "author1"},
        "html_url": f"https://github.com/MoonshotAI/kimi-code/issues/{number}",
    }


def _pr(number: int, updated_at: str = "2026-06-01T11:00:00Z") -> dict[str, Any]:
    return {
        "number": number,
        "title": f"PR {number}",
        "body": "pr body",
        "state": "open",
        "draft": False,
        "labels": [],
        "created_at": "2026-06-01T09:30:00Z",
        "updated_at": updated_at,
        "closed_at": None,
        "merged_at": None,
        "user": {"login": "dev2"},
        "html_url": f"https://github.com/MoonshotAI/kimi-code/pull/{number}",
        "head": {"ref": "feature"},
        "base": {"ref": "main"},
    }


class FakeStore:
    def __init__(self) -> None:
        self.repo_id = "repo-uuid-1"
        self.cursor: datetime | None = None
        self.has_prior = False
        self.runs: list[dict[str, Any]] = []
        self.issues: list[dict[str, Any]] = []
        self.prs: list[dict[str, Any]] = []
        self.run_updates: list[dict[str, Any]] = []

    def ensure_repo(self, owner: str = "MoonshotAI", name: str = "kimi-code") -> str:
        assert owner == "MoonshotAI"
        assert name == "kimi-code"
        return self.repo_id

    def get_last_success_cursor(self, repo_id: str) -> datetime | None:
        assert repo_id == self.repo_id
        return self.cursor

    def has_any_sync_run(self, repo_id: str) -> bool:
        return self.has_prior

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
        self.issues.append(issue)

    def upsert_pull_request(self, repo_id: str, pr: dict[str, Any]) -> None:
        self.prs.append(pr)


class FakeGitHub:
    def __init__(
        self,
        issues: list[dict[str, Any]] | None = None,
        pulls: list[dict[str, Any]] | None = None,
        error: GitHubSyncError | None = None,
    ) -> None:
        self.issues = issues or []
        self.pulls = pulls or []
        self.error = error
        self.issue_since: datetime | None = None
        self.pull_since: datetime | None = None

    def fetch_issues(self, since: datetime | None) -> list[dict[str, Any]]:
        self.issue_since = since
        if self.error:
            raise self.error
        return list(self.issues)

    def fetch_pull_requests(self, since: datetime | None) -> list[dict[str, Any]]:
        self.pull_since = since
        if self.error:
            raise self.error
        return list(self.pulls)


def test_resolve_trigger_initial() -> None:
    assert resolve_trigger(None, has_prior_run=False, has_cursor=False) == "initial"


def test_resolve_trigger_manual_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_SYNC_TRIGGER", "manual")
    assert resolve_trigger(None, has_prior_run=True, has_cursor=True) == "manual"


def test_sync_success_state_machine() -> None:
    store = FakeStore()
    gh = FakeGitHub(issues=[_issue(1)], pulls=[_pr(2)])
    result = run_sync(trigger="manual", github=gh, store=store)  # type: ignore[arg-type]

    assert result.status == "success"
    assert result.records_issue == 1
    assert result.records_pr == 1
    assert result.cursor == datetime(2026, 6, 1, 11, 0, tzinfo=timezone.utc)
    assert any(u.get("status") == "running" for u in store.run_updates)
    assert store.runs[-1]["status"] == "success"
    assert store.runs[-1]["trigger"] == "manual"
    assert len(store.issues) == 1
    assert len(store.prs) == 1


def test_sync_incremental_passes_cursor() -> None:
    store = FakeStore()
    store.cursor = datetime(2026, 6, 1, 8, 0, tzinfo=timezone.utc)
    store.has_prior = True
    gh = FakeGitHub()
    run_sync(trigger="cron", github=gh, store=store)  # type: ignore[arg-type]
    assert gh.issue_since == store.cursor
    assert gh.pull_since == store.cursor


def test_f1_401_fails_fast_no_partial() -> None:
    store = FakeStore()
    gh = FakeGitHub(error=GitHubSyncError("401", status_code=401, fail_fast=True))
    result = run_sync(github=gh, store=store)  # type: ignore[arg-type]

    assert result.status == "failed"
    assert result.records_issue == 0
    assert result.error_message is not None
    assert store.runs[-1]["status"] == "failed"


def test_f1_422_fails_fast() -> None:
    store = FakeStore()
    gh = FakeGitHub(error=GitHubSyncError("422", status_code=422, fail_fast=True))
    result = run_sync(github=gh, store=store)  # type: ignore[arg-type]
    assert result.status == "failed"
    assert "422" in (result.error_message or "")


def test_f2_partial_after_some_upserts() -> None:
    store = FakeStore()

    class PartialFailGitHub(FakeGitHub):
        def fetch_pull_requests(self, since: datetime | None) -> list[dict[str, Any]]:
            raise GitHubSyncError("403 rate limit", status_code=403, fail_fast=False)

    gh = PartialFailGitHub(issues=[_issue(5)])
    result = run_sync(github=gh, store=store)  # type: ignore[arg-type]

    assert result.status == "partial"
    assert result.records_issue == 1
    assert result.records_pr == 0


def test_github_client_fail_fast_constants() -> None:
    assert 401 in FAIL_FAST_STATUS
    assert 422 in FAIL_FAST_STATUS
    assert 403 in RETRYABLE_STATUS
    assert MAX_RETRIES == 5


def test_github_client_retry_then_success(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("api.ops.sync.github_client.time.sleep", lambda s: sleeps.append(s))

    responses = [
        MagicMock(status_code=403, text="rate limit"),
        MagicMock(status_code=200, text='[{"number":1}]'),
    ]
    responses[1].json.return_value = [{"number": 1, "title": "x", "state": "open"}]

    session = MagicMock()
    session.request.side_effect = responses
    client = GitHubClient(token="tok", session=session)
    data = client._request_json("GET", "/repos/MoonshotAI/kimi-code/issues", params={"state": "all"})
    assert isinstance(data, list)
    assert len(sleeps) == 1
    assert sleeps[0] == 2.0


def test_github_client_fail_fast_no_retry(monkeypatch: pytest.MonkeyPatch) -> None:
    sleeps: list[float] = []
    monkeypatch.setattr("api.ops.sync.github_client.time.sleep", lambda s: sleeps.append(s))

    session = MagicMock()
    session.request.return_value = MagicMock(status_code=401, text="bad creds")
    client = GitHubClient(token="tok", session=session)

    with pytest.raises(GitHubSyncError) as exc:
        client._request_json("GET", "/repos/MoonshotAI/kimi-code/issues")
    assert exc.value.fail_fast is True
    assert sleeps == []


def test_github_fetch_pulls_filters_by_since(monkeypatch: pytest.MonkeyPatch) -> None:
    client = GitHubClient(token="tok")
    since = datetime(2026, 6, 1, 10, 0, tzinfo=timezone.utc)

    def fake_paginate(path: str, *, params: dict[str, Any]) -> list[dict[str, Any]]:
        return [
            _pr(1, "2026-06-01T09:00:00Z"),
            _pr(2, "2026-06-01T11:00:00Z"),
        ]

    monkeypatch.setattr(client, "_paginate", fake_paginate)
    rows = client.fetch_pull_requests(since)
    assert len(rows) == 1
    assert rows[0]["number"] == 2


def test_store_maps_issue_fields() -> None:
    store = OpsSyncStore()
    captured: dict[str, Any] = {}

    def fake_retry(fn: Any) -> Any:
        return fn()

    monkey = pytest.MonkeyPatch()
    monkey.setattr("api.ops.sync.store.supabase_execute_with_retry", fake_retry)

    class FakeTable:
        def upsert(self, row: dict[str, Any], on_conflict: str) -> FakeTable:
            captured.update(row)
            return self

        def execute(self) -> MagicMock:
            return MagicMock()

    class FakeSb:
        def table(self, name: str) -> FakeTable:
            return FakeTable()

    monkey.setattr("api.ops.sync.store._client", lambda: FakeSb())
    try:
        store.upsert_issue("repo-1", _issue(9))
    finally:
        monkey.undo()

    assert captured["number"] == 9
    assert captured["repo_id"] == "repo-1"
    assert captured["labels"] == ["bug"]
    assert captured["assignees"] == ["dev1"]
    assert captured["author"] == "author1"
