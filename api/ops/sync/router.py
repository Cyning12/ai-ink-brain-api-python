"""Ops Desk sync 手动触发与 runs 列表路由。"""

from __future__ import annotations

import os
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query

from api.ops.deps import require_ops_secret
from api.ops.sync.dispatch import (
    DISPATCH_REPO_NAME,
    DISPATCH_REPO_OWNER,
    DISPATCH_WORKFLOW_FILE,
    GitHubDispatchError,
    dispatch_sync_workflow,
    has_active_sync_workflow_run,
)
from api.ops.sync.github_client import REPO_NAME, REPO_OWNER
from api.ops.sync.store import OpsSyncStore, SyncRunAlreadyActiveError

router = APIRouter(prefix="/ops/sync", tags=["ops-sync"])


def _store() -> OpsSyncStore:
    return OpsSyncStore()


def _dispatch_sync(*, token: str) -> dict[str, Any]:
    """可注入的 dispatch 包装；测试时可通过 dependency_overrides 替换。"""
    return dispatch_sync_workflow(token=token)


@router.post("/trigger")
def trigger_sync(
    store: OpsSyncStore = Depends(_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    """手动触发 GitHub Actions sync workflow。"""
    # 503：token 缺失
    token = (os.getenv("OPS_GITHUB_DISPATCH_TOKEN") or "").strip()
    if not token:
        raise HTTPException(
            status_code=503,
            detail={"code": "DISPATCH_TOKEN_MISSING", "message": "OPS_GITHUB_DISPATCH_TOKEN 未配置"},
        )

    # 409：Supabase 最近 run 仍在 pending/running（sync 脚本阶段）
    repo_id = store.ensure_repo(REPO_OWNER, REPO_NAME)
    recent = store.get_recent_sync_runs(repo_id, limit=1)
    if recent:
        last = recent[0]
        status = last.get("status")
        if status in ("pending", "running"):
            raise HTTPException(
                status_code=409,
                detail={"code": "SYNC_ALREADY_RUNNING", "run_id": str(last.get("id")), "source": "supabase"},
            )

    # 原子 claim：先写入 pending manual（依赖 idx_ops_sync_runs_one_active_per_repo）
    claim_run_id: str | None = None
    try:
        claim_run_id = store.create_sync_run(repo_id, "manual")
    except SyncRunAlreadyActiveError as exc:
        raise HTTPException(
            status_code=409,
            detail={"code": "SYNC_ALREADY_RUNNING", "source": "supabase_claim", "message": str(exc)},
        ) from exc

    # 409：GHA 已有 queued/in_progress（checkout/pip 阶段 · Supabase 尚未写入）
    try:
        if has_active_sync_workflow_run(token=token):
            store.fail_sync_run(claim_run_id, "github_actions already active")
            raise HTTPException(
                status_code=409,
                detail={"code": "SYNC_ALREADY_RUNNING", "source": "github_actions"},
            )
    except GitHubDispatchError as exc:
        store.fail_sync_run(claim_run_id, f"github runs query failed: {exc}")
        raise HTTPException(
            status_code=502,
            detail={
                "code": "GITHUB_DISPATCH_FAILED",
                "message": str(exc),
                "status_code": exc.status_code,
            },
        ) from exc

    # dispatch
    try:
        _dispatch_sync(token=token)
    except GitHubDispatchError as exc:
        store.fail_sync_run(claim_run_id, f"dispatch failed: {exc}")
        raise HTTPException(
            status_code=502,
            detail={
                "code": "GITHUB_DISPATCH_FAILED",
                "message": str(exc),
                "status_code": exc.status_code,
            },
        ) from exc

    return {
        "dispatched": True,
        "workflow": DISPATCH_WORKFLOW_FILE.replace(".yml", ""),
        "repository": f"{DISPATCH_REPO_OWNER}/{DISPATCH_REPO_NAME}",
        "claim_run_id": claim_run_id,
    }


@router.get("/runs")
def list_sync_runs(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    store: OpsSyncStore = Depends(_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    """获取最近 sync runs，含 artifact 布尔字段。"""
    repo_id = store.ensure_repo(REPO_OWNER, REPO_NAME)
    runs = store.get_recent_sync_runs(repo_id, limit=limit)

    # join artifacts 布尔字段
    run_ids = [str(r.get("id")) for r in runs if r.get("id")]
    artifacts_map = store.get_artifacts_by_run_ids(run_ids) if run_ids else {}

    items: list[dict[str, Any]] = []
    for run in runs:
        rid = str(run.get("id"))
        art = artifacts_map.get(rid, {})
        items.append({
            "id": rid,
            "started_at": run.get("started_at"),
            "finished_at": run.get("finished_at"),
            "status": run.get("status"),
            "trigger": run.get("trigger"),
            "records_issue": run.get("records_issue"),
            "records_pr": run.get("records_pr"),
            "error_message": run.get("error_message"),
            "has_graph_snapshot": bool(art.get("graph_snapshot_id")),
            "has_scan_snapshot": bool(art.get("scan_snapshot_id")),
        })

    return {"runs": items}
