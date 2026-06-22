"""Ops Desk 只读查询封装。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from api.ops.constants import DEFAULT_DAYS, MAX_LIMIT, REPO_NAME, REPO_OWNER
from api.rag_env import supabase_execute_with_retry


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _bucket_day(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d")


def _hours_between(start: datetime, end: datetime) -> float:
    return round((end - start).total_seconds() / 3600.0, 2)


def _parse_ts(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        value = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None


class OpsQueries:
    """只读查询 ops_* 同步表；默认仓库 MoonshotAI/kimi-code。"""

    def __init__(self, client: Any) -> None:
        self.client = client

    def _repo_id(self) -> str | None:
        def _once() -> Any:
            res = (
                self.client.table("ops_repos")
                .select("id")
                .eq("owner", REPO_OWNER)
                .eq("name", REPO_NAME)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if rows and isinstance(rows[0], dict):
                return rows[0].get("id")
            return None

        return supabase_execute_with_retry(_once)

    def sync_status(self) -> dict[str, Any]:
        repo_id = self._repo_id()
        if not repo_id:
            return {"status": "no_repo", "cursor": None, "as_of": _now_iso()}

        def _once() -> dict[str, Any]:
            res = (
                self.client.table("ops_sync_runs")
                .select("status, cursor, started_at, finished_at, records_issue, records_pr")
                .eq("repo_id", repo_id)
                .order("started_at", desc=True)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if not rows or not isinstance(rows[0], dict):
                return {"status": "never_synced", "cursor": None, "as_of": _now_iso()}
            row = rows[0]
            return {
                "status": row.get("status", "unknown"),
                "cursor": row.get("cursor"),
                "started_at": row.get("started_at"),
                "finished_at": row.get("finished_at"),
                "records_issue": row.get("records_issue", 0),
                "records_pr": row.get("records_pr", 0),
                "as_of": _now_iso(),
            }

        return supabase_execute_with_retry(_once)

    def _cutoff(self, days: int) -> datetime:
        return datetime.now(timezone.utc) - timedelta(days=days)

    def _fetch_rows(
        self,
        table: str,
        days: int,
        extra_filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        cutoff = self._cutoff(days).isoformat()

        def _once() -> list[dict[str, Any]]:
            repo_id = self._repo_id()
            if not repo_id:
                return []
            query = (
                self.client.table(table)
                .select("*")
                .eq("repo_id", repo_id)
                .gte("created_at", cutoff)
            )
            for key, value in (extra_filters or {}).items():
                if value is None:
                    continue
                if isinstance(value, list):
                    query = query.in_(key, value)
                else:
                    query = query.eq(key, value)
            res = query.order("created_at", desc=True).execute()
            return res.data if isinstance(res.data, list) else []

        return supabase_execute_with_retry(_once)

    def count_rows(
        self,
        table: str,
        days: int,
        extra_filters: dict[str, Any] | None = None,
    ) -> int:
        cutoff = self._cutoff(days).isoformat()

        def _once() -> int:
            repo_id = self._repo_id()
            if not repo_id:
                return 0
            query = (
                self.client.table(table)
                .select("*", count="exact")
                .eq("repo_id", repo_id)
                .gte("created_at", cutoff)
            )
            for key, value in (extra_filters or {}).items():
                if value is None:
                    continue
                if isinstance(value, list):
                    query = query.in_(key, value)
                else:
                    query = query.eq(key, value)
            res = query.execute()
            return getattr(res, "count", 0) or 0

        return supabase_execute_with_retry(_once)

    def fetch_issues(
        self,
        days: int = DEFAULT_DAYS,
        state: str | None = None,
        label: str | None = None,
        module: str | None = None,
        age: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        filters: dict[str, Any] = {}
        if state:
            filters["state"] = state
        if label:
            filters["labels"] = [label]
        if module:
            filters["scan_tags"] = [module]
        rows = self._fetch_rows("ops_issues", days, filters)

        if age:
            try:
                max_age_days = int(age)
                cutoff = datetime.now(timezone.utc) - timedelta(days=max_age_days)
                rows = [
                    r
                    for r in rows
                    if (created := _parse_ts(r.get("created_at"))) and created >= cutoff
                ]
            except ValueError:
                pass

        total = len(rows)
        limited = rows[offset : offset + min(limit, MAX_LIMIT)]
        return limited, total

    def fetch_pulls(
        self,
        days: int = DEFAULT_DAYS,
        state: str | None = None,
        ci: str | None = None,
        author: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        filters: dict[str, Any] = {}
        if state:
            filters["state"] = state
        if author:
            filters["author"] = author
        if ci:
            filters["checks_conclusion"] = ci
        rows = self._fetch_rows("ops_pull_requests", days, filters)
        total = len(rows)
        limited = rows[offset : offset + min(limit, MAX_LIMIT)]
        return limited, total

    def cycle_time_metric(self, days: int = DEFAULT_DAYS) -> dict[str, Any]:
        rows = self._fetch_rows("ops_issues", days, {"state": "closed"})
        values: list[float] = []
        buckets: dict[str, list[float]] = {}
        for row in rows:
            created = _parse_ts(row.get("created_at"))
            closed = _parse_ts(row.get("closed_at"))
            if not created or not closed:
                continue
            hours = _hours_between(created, closed)
            values.append(hours)
            bucket = _bucket_day(closed)
            buckets.setdefault(bucket, []).append(hours)

        series = [
            {
                "bucket": bucket,
                "avg_hours": round(sum(vs) / len(vs), 2),
                "count": len(vs),
            }
            for bucket, vs in sorted(buckets.items())
        ]
        if values:
            values.sort()
            summary = {
                "avg_hours": round(sum(values) / len(values), 2),
                "median_hours": values[len(values) // 2],
                "min_hours": values[0],
                "max_hours": values[-1],
                "count": len(values),
            }
        else:
            summary = {"avg_hours": 0, "median_hours": 0, "min_hours": 0, "max_hours": 0, "count": 0}
        return {
            "metric": "cycle-time",
            "days": days,
            "series": series,
            "summary": summary,
            **self.sync_status(),
        }

    def review_time_metric(self, days: int = DEFAULT_DAYS) -> dict[str, Any]:
        rows = self._fetch_rows("ops_pull_requests", days)
        values: list[float] = []
        buckets: dict[str, list[float]] = {}
        for row in rows:
            created = _parse_ts(row.get("created_at"))
            reviewed = _parse_ts(row.get("first_review_at") or row.get("updated_at"))
            if not created or not reviewed or reviewed <= created:
                continue
            hours = _hours_between(created, reviewed)
            values.append(hours)
            bucket = _bucket_day(reviewed)
            buckets.setdefault(bucket, []).append(hours)

        series = [
            {
                "bucket": bucket,
                "avg_hours": round(sum(vs) / len(vs), 2),
                "count": len(vs),
            }
            for bucket, vs in sorted(buckets.items())
        ]
        if values:
            values.sort()
            summary = {
                "avg_hours": round(sum(values) / len(values), 2),
                "median_hours": values[len(values) // 2],
                "min_hours": values[0],
                "max_hours": values[-1],
                "count": len(values),
            }
        else:
            summary = {"avg_hours": 0, "median_hours": 0, "min_hours": 0, "max_hours": 0, "count": 0}
        return {
            "metric": "review-time",
            "days": days,
            "series": series,
            "summary": summary,
            **self.sync_status(),
        }

    def issue_throughput_metric(self, days: int = DEFAULT_DAYS) -> dict[str, Any]:
        rows = self._fetch_rows("ops_issues", days, {"state": "closed"})
        buckets: dict[str, int] = {}
        for row in rows:
            closed = _parse_ts(row.get("closed_at"))
            if not closed:
                continue
            bucket = _bucket_day(closed)
            buckets[bucket] = buckets.get(bucket, 0) + 1

        series = [{"bucket": b, "count": c} for b, c in sorted(buckets.items())]
        total = sum(c for _, c in series)
        return {
            "metric": "issue-throughput",
            "days": days,
            "series": series,
            "summary": {"total": total, "avg_per_day": round(total / max(days, 1), 2)},
            **self.sync_status(),
        }
