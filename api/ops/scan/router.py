"""Ops Desk Scan summary 路由。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.ops.deps import get_supabase_client, require_ops_secret

from .store import OpsScanStore

router = APIRouter(prefix="/ops/scan", tags=["ops-scan"])


def get_scan_store(client: Any = Depends(get_supabase_client)) -> OpsScanStore:
    """解析默认 repo 并返回 ScanStore；测试时可通过 dependency_overrides 替换。"""
    from api.ops.sync.store import OpsSyncStore

    repo_id = OpsSyncStore().ensure_repo()
    return OpsScanStore(repo_id=repo_id, client=client)


@router.get("/summary")
def scan_summary(
    store: OpsScanStore = Depends(get_scan_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    snapshot = store.get_latest_snapshot()
    if not snapshot:
        raise HTTPException(
            status_code=404,
            detail={"code": "SCAN_SNAPSHOT_NOT_FOUND"},
        )

    def _count(field: str) -> int:
        value = snapshot.get(field)
        return len(value) if isinstance(value, list) else 0

    return {
        "snapshot_id": snapshot["id"],
        "scan_version": snapshot["scan_version"],
        "total_open": snapshot.get("total_open"),
        "p0_count": _count("p0_items"),
        "p1_count": _count("p1_items"),
        "p2_count": _count("p2_items"),
        "deferred_count": _count("deferred_items"),
        "raw_markdown_url": snapshot.get("raw_markdown_url"),
        "parsed_summary": snapshot.get("parsed_summary"),
        "created_at": snapshot.get("created_at"),
    }
