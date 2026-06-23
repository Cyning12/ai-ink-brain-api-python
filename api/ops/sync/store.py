"""Supabase ops_* 表读写封装。"""

from __future__ import annotations

import os
from datetime import datetime
from typing import Any

from api.rag_env import pick_supabase_service_key, pick_supabase_url, supabase_execute_with_retry
from supabase import create_client

from .github_client import REPO_NAME, REPO_OWNER, GitHubClient


def _client() -> Any:
    url = pick_supabase_url()
    key = pick_supabase_service_key()
    if not url or not key:
        raise RuntimeError(
            "缺少 Supabase 配置：NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"
        )
    return create_client(url, key)


class OpsSyncStore:
    """ops_repos / ops_sync_runs / issues / pulls 持久化。"""

    def ensure_repo(self, owner: str = REPO_OWNER, name: str = REPO_NAME) -> str:
        def _once() -> str:
            sb = _client()
            existing = (
                sb.table("ops_repos")
                .select("id")
                .eq("owner", owner)
                .eq("name", name)
                .limit(1)
                .execute()
            )
            rows = existing.data if isinstance(existing.data, list) else []
            if rows and isinstance(rows[0], dict) and rows[0].get("id"):
                return str(rows[0]["id"])

            inserted = (
                sb.table("ops_repos")
                .insert({"owner": owner, "name": name})
                .execute()
            )
            data = inserted.data if isinstance(inserted.data, list) else []
            if data and isinstance(data[0], dict) and data[0].get("id"):
                return str(data[0]["id"])
            raise RuntimeError("ops_repos insert 未返回 id")

        return supabase_execute_with_retry(_once)

    def get_last_success_cursor(self, repo_id: str) -> datetime | None:
        def _once() -> datetime | None:
            sb = _client()
            res = (
                sb.table("ops_sync_runs")
                .select("cursor")
                .eq("repo_id", repo_id)
                .eq("status", "success")
                .order("started_at", desc=True)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if not rows or not isinstance(rows[0], dict):
                return None
            cursor_raw = rows[0].get("cursor")
            if not cursor_raw:
                return None
            return GitHubClient.parse_github_ts(str(cursor_raw))

        return supabase_execute_with_retry(_once)

    def has_any_sync_run(self, repo_id: str) -> bool:
        def _once() -> bool:
            sb = _client()
            res = (
                sb.table("ops_sync_runs")
                .select("id")
                .eq("repo_id", repo_id)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return bool(rows)

        return supabase_execute_with_retry(_once)

    def get_recent_sync_runs(self, repo_id: str, *, limit: int = 20) -> list[dict[str, Any]]:
        def _once() -> list[dict[str, Any]]:
            sb = _client()
            res = (
                sb.table("ops_sync_runs")
                .select("id, started_at, finished_at, status, trigger, records_issue, records_pr, error_message")
                .eq("repo_id", repo_id)
                .order("started_at", desc=True)
                .limit(limit)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return [r for r in rows if isinstance(r, dict)]

        return supabase_execute_with_retry(_once)

    def get_artifacts_by_run_ids(self, run_ids: list[str]) -> dict[str, dict[str, Any]]:
        def _once() -> dict[str, dict[str, Any]]:
            if not run_ids:
                return {}
            sb = _client()
            res = (
                sb.table("ops_sync_run_artifacts")
                .select("sync_run_id, scan_snapshot_id, graph_snapshot_id")
                .in_("sync_run_id", run_ids)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            result: dict[str, dict[str, Any]] = {}
            for row in rows:
                if not isinstance(row, dict):
                    continue
                rid = str(row.get("sync_run_id"))
                result[rid] = {
                    "scan_snapshot_id": row.get("scan_snapshot_id"),
                    "graph_snapshot_id": row.get("graph_snapshot_id"),
                }
            return result

        return supabase_execute_with_retry(_once)

    def create_sync_run(self, repo_id: str, trigger: str) -> str:
        def _once() -> str:
            sb = _client()
            row = {"repo_id": repo_id, "status": "pending", "trigger": trigger}
            res = sb.table("ops_sync_runs").insert(row).execute()
            data = res.data if isinstance(res.data, list) else []
            if data and isinstance(data[0], dict) and data[0].get("id"):
                return str(data[0]["id"])
            raise RuntimeError("ops_sync_runs insert 未返回 id")

        return supabase_execute_with_retry(_once)

    def update_sync_run(self, run_id: str, **fields: Any) -> None:
        def _once() -> None:
            sb = _client()
            sb.table("ops_sync_runs").update(fields).eq("id", run_id).execute()

        supabase_execute_with_retry(_once)

    def upsert_issue(self, repo_id: str, issue: dict[str, Any]) -> None:
        row = {
            "repo_id": repo_id,
            "number": issue["number"],
            "title": issue.get("title") or "",
            "body": issue.get("body"),
            "state": issue.get("state") or "open",
            "labels": [label.get("name") for label in issue.get("labels", []) if isinstance(label, dict)],
            "assignees": [
                a.get("login") for a in issue.get("assignees", []) if isinstance(a, dict)
            ],
            "milestone": (
                issue.get("milestone", {}).get("title")
                if isinstance(issue.get("milestone"), dict)
                else None
            ),
            "created_at": issue.get("created_at"),
            "updated_at": issue.get("updated_at"),
            "closed_at": issue.get("closed_at"),
            "author": (
                issue.get("user", {}).get("login")
                if isinstance(issue.get("user"), dict)
                else None
            ),
            "html_url": issue.get("html_url"),
        }

        def _once() -> None:
            sb = _client()
            sb.table("ops_issues").upsert(row, on_conflict="repo_id,number").execute()

        supabase_execute_with_retry(_once)

    def upsert_pull_request(self, repo_id: str, pr: dict[str, Any]) -> None:
        merged_at = pr.get("merged_at")
        state = "merged" if merged_at else (pr.get("state") or "open")
        row = {
            "repo_id": repo_id,
            "number": pr["number"],
            "title": pr.get("title") or "",
            "body": pr.get("body"),
            "state": state,
            "draft": bool(pr.get("draft", False)),
            "labels": [label.get("name") for label in pr.get("labels", []) if isinstance(label, dict)],
            "created_at": pr.get("created_at"),
            "updated_at": pr.get("updated_at"),
            "closed_at": pr.get("closed_at"),
            "merged_at": merged_at,
            "author": (
                pr.get("user", {}).get("login") if isinstance(pr.get("user"), dict) else None
            ),
            "html_url": pr.get("html_url"),
            "head_ref": pr.get("head", {}).get("ref") if isinstance(pr.get("head"), dict) else None,
            "base_ref": pr.get("base", {}).get("ref") if isinstance(pr.get("base"), dict) else None,
        }

        def _once() -> None:
            sb = _client()
            sb.table("ops_pull_requests").upsert(row, on_conflict="repo_id,number").execute()

        supabase_execute_with_retry(_once)


def resolve_trigger(explicit: str | None, *, has_prior_run: bool, has_cursor: bool) -> str:
    """解析 sync trigger：cron / manual / initial。"""
    if explicit in ("cron", "manual", "initial"):
        return explicit
    if not has_prior_run and not has_cursor:
        return "initial"
    env_trigger = (os.getenv("OPS_SYNC_TRIGGER") or "").strip()
    if env_trigger in ("cron", "manual", "initial"):
        return env_trigger
    return "cron"
