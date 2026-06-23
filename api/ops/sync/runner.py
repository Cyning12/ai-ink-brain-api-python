"""Ops Desk GitHub sync 编排与 sync_runs 状态机。"""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

from api.ops.graph.store import ingest_graph_after_github_sync
from api.ops.scan.store import ingest_scan_after_github_sync

from .github_client import GitHubClient, GitHubSyncError
from .store import OpsSyncStore, resolve_trigger


@dataclass(frozen=True)
class SyncRunResult:
    run_id: str
    status: str
    records_issue: int
    records_pr: int
    cursor: datetime | None
    error_message: str | None = None
    scan_snapshot_id: str | None = None
    graph_snapshot_id: str | None = None


def _max_updated(items: list[dict[str, Any]], fallback: datetime | None) -> datetime | None:
    best = fallback
    for item in items:
        ts = GitHubClient.parse_github_ts(item.get("updated_at"))
        if ts is None:
            continue
        if best is None or ts > best:
            best = ts
    return best


def run_sync(
    *,
    trigger: str | None = None,
    github: GitHubClient | None = None,
    store: OpsSyncStore | None = None,
) -> SyncRunResult:
    """pending → running → success|failed|partial。"""
    gh = github or GitHubClient.from_env()
    db = store or OpsSyncStore()

    repo_id = db.ensure_repo()
    cursor = db.get_last_success_cursor(repo_id)
    has_prior = db.has_any_sync_run(repo_id)
    resolved_trigger = resolve_trigger(trigger, has_prior_run=has_prior, has_cursor=cursor is not None)

    run_id = db.create_sync_run(repo_id, resolved_trigger)
    db.update_sync_run(run_id, status="running")

    records_issue = 0
    records_pr = 0
    synced_items: list[dict[str, Any]] = []

    try:
        issues = gh.fetch_issues(cursor)
        for issue in issues:
            db.upsert_issue(repo_id, issue)
            records_issue += 1
            synced_items.append(issue)

        pulls = gh.fetch_pull_requests(cursor)
        for pr in pulls:
            db.upsert_pull_request(repo_id, pr)
            records_pr += 1
            synced_items.append(pr)

        new_cursor = _max_updated(synced_items, cursor) or cursor
        finished = datetime.now(timezone.utc).isoformat()
        db.update_sync_run(
            run_id,
            status="success",
            finished_at=finished,
            cursor=new_cursor.isoformat() if new_cursor else None,
            records_issue=records_issue,
            records_pr=records_pr,
            error_message=None,
        )

        scan_snapshot_id: str | None = None
        scan_status = "success"
        scan_error: str | None = None
        try:
            scan_result = ingest_scan_after_github_sync(repo_id, run_id)
            scan_snapshot_id = scan_result.snapshot_id
            if scan_result.status != "success":
                scan_status = "partial"
                scan_error = scan_result.error_message or "scan ingest failed"
        except Exception as exc:  # noqa: BLE001
            scan_status = "partial"
            scan_error = f"scan ingest exception: {exc}"

        graph_snapshot_id: str | None = None
        graph_status = "success"
        graph_error: str | None = None
        try:
            graph_result = ingest_graph_after_github_sync(repo_id, run_id)
            graph_snapshot_id = graph_result.snapshot_id
            if graph_result.status != "success":
                graph_status = "partial"
                graph_error = graph_result.error_message or "graph ingest failed"
        except Exception as exc:  # noqa: BLE001
            graph_status = "partial"
            graph_error = f"graph ingest exception: {exc}"

        # 合并 scan + graph 状态
        if scan_status == "partial" or graph_status == "partial":
            combined_error = "; ".join(
                e for e in [scan_error, graph_error] if e
            ) or "partial ingest"
            db.update_sync_run(run_id, status="partial", error_message=combined_error)
            return SyncRunResult(
                run_id=run_id,
                status="partial",
                records_issue=records_issue,
                records_pr=records_pr,
                cursor=new_cursor,
                error_message=combined_error,
                scan_snapshot_id=scan_snapshot_id,
                graph_snapshot_id=graph_snapshot_id,
            )

        return SyncRunResult(
            run_id=run_id,
            status="success",
            records_issue=records_issue,
            records_pr=records_pr,
            cursor=new_cursor,
            error_message=None,
            scan_snapshot_id=scan_snapshot_id,
            graph_snapshot_id=graph_snapshot_id,
        )

    except GitHubSyncError as exc:
        status = "failed"
        if records_issue + records_pr > 0 and not exc.fail_fast:
            status = "partial"
        finished = datetime.now(timezone.utc).isoformat()
        db.update_sync_run(
            run_id,
            status=status,
            finished_at=finished,
            records_issue=records_issue,
            records_pr=records_pr,
            error_message=str(exc),
        )
        return SyncRunResult(
            run_id=run_id,
            status=status,
            records_issue=records_issue,
            records_pr=records_pr,
            cursor=cursor,
            error_message=str(exc),
        )

    except Exception as exc:  # noqa: BLE001
        status = "partial" if records_issue + records_pr > 0 else "failed"
        finished = datetime.now(timezone.utc).isoformat()
        db.update_sync_run(
            run_id,
            status=status,
            finished_at=finished,
            records_issue=records_issue,
            records_pr=records_pr,
            error_message=str(exc),
        )
        return SyncRunResult(
            run_id=run_id,
            status=status,
            records_issue=records_issue,
            records_pr=records_pr,
            cursor=cursor,
            error_message=str(exc),
        )


def main() -> int:
    result = run_sync()
    print(
        f"sync_run={result.run_id} status={result.status} "
        f"issues={result.records_issue} prs={result.records_pr} "
        f"cursor={result.cursor} error={result.error_message or ''} "
        f"scan_snapshot_id={result.scan_snapshot_id or ''} "
        f"graph_snapshot_id={result.graph_snapshot_id or ''}"
    )
    # cron 兼容：issue/PR 同步成功但 scan/graph 被跳过或部分失败时不阻断 GHA
    return 0 if result.status in ("success", "partial") else 1


if __name__ == "__main__":
    sys.exit(main())
