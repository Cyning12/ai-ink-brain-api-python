"""Scan snapshot 持久化与 sync_run 关联。"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from api.rag_env import pick_supabase_service_key, pick_supabase_url, supabase_execute_with_retry
from supabase import create_client

from .parser import load_issue_scan, parse_issue_scan


def _client() -> Any:
    url = pick_supabase_url()
    key = pick_supabase_service_key()
    if not url or not key:
        raise RuntimeError(
            "缺少 Supabase 配置：NEXT_PUBLIC_SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY"
        )
    return create_client(url, key)


def _default_index_path() -> Path:
    raw = (os.getenv("OPS_SCAN_INDEX_PATH") or "").strip()
    if raw:
        return Path(raw)
    return Path("workspace/docs/harness/guides/ISSUE_SCAN_kimi_code_open_c2_v1_zh.md")


def _default_raw_url() -> str | None:
    raw = (os.getenv("OPS_SCAN_RAW_URL") or "").strip()
    return raw or None


@dataclass(frozen=True)
class ScanIngestResult:
    snapshot_id: str | None
    status: str
    total_open: int | None
    counts: dict[str, int]
    error_message: str | None = None


class OpsScanStore:
    """ops_scan_snapshots / ops_sync_run_artifacts / ops_issues.scan_tags 读写。"""

    def __init__(self, repo_id: str, client: Any | None = None) -> None:
        self.repo_id = repo_id
        self._client = client

    def _sb(self) -> Any:
        return self._client or _client()

    def write_snapshot(self, parsed: dict[str, Any]) -> str:
        row = {
            "repo_id": self.repo_id,
            "scan_version": parsed["scan_version"],
            "total_open": parsed.get("total_open"),
            "p0_items": parsed.get("p0_items") or [],
            "p1_items": parsed.get("p1_items") or [],
            "p2_items": parsed.get("p2_items") or [],
            "deferred_items": parsed.get("deferred_items") or [],
            "raw_markdown_url": parsed.get("raw_markdown_url"),
            "parsed_summary": parsed.get("parsed_summary"),
        }

        def _once() -> str:
            sb = self._sb()
            res = sb.table("ops_scan_snapshots").insert(row).execute()
            data = res.data if isinstance(res.data, list) else []
            if data and isinstance(data[0], dict) and data[0].get("id"):
                return str(data[0]["id"])
            raise RuntimeError("ops_scan_snapshots insert 未返回 id")

        return supabase_execute_with_retry(_once)

    def backfill_scan_tags(self, tags_by_number: dict[int, list[str]]) -> int:
        """按 issue# 回填 ops_issues.scan_tags；不存在的行静默跳过。"""
        updated = 0
        for number, tags in tags_by_number.items():
            if not tags:
                continue

            def _once(n: int = number, t: list[str] = tags) -> Any:
                sb = self._sb()
                return (
                    sb.table("ops_issues")
                    .update({"scan_tags": t})
                    .eq("repo_id", self.repo_id)
                    .eq("number", n)
                    .execute()
                )

            try:
                res = supabase_execute_with_retry(_once)
                rows = res.data if isinstance(res.data, list) else []
                if rows:
                    updated += 1
            except Exception:
                # 行不存在或并发更新失败时跳过
                pass
        return updated

    def link_artifact(
        self,
        sync_run_id: str,
        scan_snapshot_id: str | None,
        graph_snapshot_id: str | None = None,
    ) -> None:
        row = {
            "sync_run_id": sync_run_id,
            "scan_snapshot_id": scan_snapshot_id,
            "graph_snapshot_id": graph_snapshot_id,
        }

        def _once() -> None:
            sb = self._sb()
            sb.table("ops_sync_run_artifacts").insert(row).execute()

        supabase_execute_with_retry(_once)

    def get_latest_snapshot(self) -> dict[str, Any] | None:
        def _once() -> dict[str, Any] | None:
            sb = self._sb()
            res = (
                sb.table("ops_scan_snapshots")
                .select("*")
                .eq("repo_id", self.repo_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return rows[0] if rows and isinstance(rows[0], dict) else None

        return supabase_execute_with_retry(_once)


def ingest_scan_after_github_sync(
    repo_id: str,
    sync_run_id: str,
    *,
    index_path: Path | None = None,
    raw_url: str | None = None,
    client: Any | None = None,
) -> ScanIngestResult:
    """sync_run 成功后调用：解析 ISSUE_SCAN 并写入 snapshot + artifact。"""
    path = index_path or _default_index_path()
    if not path.exists():
        return ScanIngestResult(
            snapshot_id=None,
            status="skipped",
            total_open=None,
            counts={},
            error_message=f"scan index not found: {path}",
        )

    markdown = load_issue_scan(path)
    parsed = parse_issue_scan(markdown, raw_url=raw_url or _default_raw_url())

    store = OpsScanStore(repo_id=repo_id, client=client)
    snapshot_id = store.write_snapshot(parsed)
    store.backfill_scan_tags(parsed["tags_by_number"])
    store.link_artifact(sync_run_id, snapshot_id, graph_snapshot_id=None)

    counts = {
        "C3-P0": len(parsed["p0_items"]),
        "C3-P1": len(parsed["p1_items"]),
        "C3-P2": len(parsed["p2_items"]),
        "OBSERVE": len(parsed["deferred_items"]),
    }
    return ScanIngestResult(
        snapshot_id=snapshot_id,
        status="success",
        total_open=parsed["total_open"],
        counts=counts,
        error_message=None,
    )
