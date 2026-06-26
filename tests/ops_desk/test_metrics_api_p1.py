"""P1-1 metrics / list API 路由测试。"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops import lists, metrics
from api.ops.queries import OpsQueries


class FakeOpsQueries:
    def __init__(self, issues: list[dict[str, Any]] | None = None, pulls: list[dict[str, Any]] | None = None) -> None:
        self.issues = issues or []
        self.pulls = pulls or []

    def sync_status(self) -> dict[str, Any]:
        return {"status": "success", "cursor": "2026-06-21T00:00:00Z", "as_of": "2026-06-22T00:00:00Z"}

    def cycle_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {
            "metric": "cycle-time",
            "days": days,
            "series": [{"bucket": "2026-06-01", "avg_hours": 48.0, "count": 1}],
            "summary": {"avg_hours": 48.0, "median_hours": 48.0, "min_hours": 48.0, "max_hours": 48.0, "count": 1},
            **self.sync_status(),
        }

    def review_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {
            "metric": "review-time",
            "days": days,
            "series": [{"bucket": "2026-06-01", "avg_hours": 12.0, "count": 1}],
            "summary": {"avg_hours": 12.0, "median_hours": 12.0, "min_hours": 12.0, "max_hours": 12.0, "count": 1},
            **self.sync_status(),
        }

    def issue_throughput_metric(self, days: int = 30) -> dict[str, Any]:
        return {
            "metric": "issue-throughput",
            "days": days,
            "series": [{"bucket": "2026-06-01", "count": 2}],
            "summary": {"total": 2, "avg_per_day": 0.07},
            **self.sync_status(),
        }

    def fetch_issues(
        self,
        days: int = 30,
        state: str | None = None,
        label: str | None = None,
        module: str | None = None,
        age: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = [r for r in self.issues if state is None or r.get("state") == state]
        if label:
            rows = [r for r in rows if label in (r.get("labels") or [])]
        return rows[offset : offset + limit], len(rows)

    def fetch_pulls(
        self,
        days: int = 30,
        state: str | None = None,
        ci: str | None = None,
        author: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = [r for r in self.pulls if state is None or r.get("state") == state]
        if author:
            rows = [r for r in rows if r.get("author") == author]
        return rows[offset : offset + limit], len(rows)


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    fake = FakeOpsQueries(
        issues=[
            {"number": 545, "title": "Deep demo issue", "state": "open", "labels": ["bug"]},
            {"number": 100, "title": "Other", "state": "closed", "labels": []},
        ],
        pulls=[
            {"number": 83, "title": "PR 83", "state": "merged", "author": "cyning"},
        ],
    )
    app.dependency_overrides[lists.ops_queries] = lambda: fake
    app.dependency_overrides[metrics.ops_queries] = lambda: fake
    yield TestClient(app)
    app.dependency_overrides.clear()


def test_metrics_cycle_time(client: TestClient) -> None:
    resp = client.get("/api/py/ops/metrics/cycle-time?days=7", headers={"x-ops-secret": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["metric"] == "cycle-time"
    assert data["days"] == 7
    assert "summary" in data


def test_metrics_review_time(client: TestClient) -> None:
    resp = client.get("/api/py/ops/metrics/review-time", headers={"x-ops-secret": "test"})
    assert resp.status_code == 200
    assert resp.json()["metric"] == "review-time"


def test_metrics_issue_throughput(client: TestClient) -> None:
    resp = client.get("/api/py/ops/metrics/issue-throughput", headers={"x-ops-secret": "test"})
    assert resp.status_code == 200
    assert resp.json()["metric"] == "issue-throughput"


def test_list_issues(client: TestClient) -> None:
    resp = client.get("/api/py/ops/issues?state=open&label=bug", headers={"x-ops-secret": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["number"] == 545


def test_list_pulls(client: TestClient) -> None:
    resp = client.get("/api/py/ops/pulls?state=merged", headers={"x-ops-secret": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 1
    assert data["items"][0]["number"] == 83


def test_ops_secret_missing(client: TestClient, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPS_DESK_SECRET_TEST", "test")
    monkeypatch.delenv("OPS_DESK_SECRET", raising=False)
    resp = client.get("/api/py/ops/metrics/cycle-time")
    assert resp.status_code == 401


def test_ops_queries_class_has_methods() -> None:
    assert callable(OpsQueries.cycle_time_metric)
    assert callable(OpsQueries.fetch_issues)
    assert callable(OpsQueries.fetch_pulls)
