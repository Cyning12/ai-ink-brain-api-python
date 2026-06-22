"""Ops Desk Run 管理路由。"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Path, Query

from api.ops.deps import get_supabase_client, require_ops_secret
from api.ops.store import OpsRunStore

router = APIRouter(prefix="/ops/runs", tags=["ops-runs"])


def _store() -> OpsRunStore:
    return OpsRunStore(get_supabase_client())


@router.get("/{run_id}")
def get_run(
    run_id: str = Path(...),
    store: OpsRunStore = Depends(_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    run = store.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail={"code": "RUN_NOT_FOUND"})
    return dict(run)


@router.get("/{run_id}/events")
def get_events(
    run_id: str = Path(...),
    after_seq: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
    store: OpsRunStore = Depends(_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    events = store.get_events(run_id, after_seq=after_seq, limit=limit)
    return {"run_id": run_id, "after_seq": after_seq, "events": events}


@router.post("/{run_id}/retry")
def retry_run(
    run_id: str = Path(...),
    retry_token: str = Query(...),
    store: OpsRunStore = Depends(_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    run = store.retry_run(run_id, retry_token)
    if not run:
        raise HTTPException(status_code=409, detail={"code": "RETRY_TOKEN_INVALID"})
    return {"run_id": run_id, "status": run.get("status"), "retry_accepted": True}


@router.get("/{run_id}/stream")
def stream_run(
    run_id: str = Path(...),
    store: OpsRunStore = Depends(_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    """SSE stream stub：P1-5 前返回 404 说明。"""
    raise HTTPException(status_code=404, detail={"code": "SSE_NOT_IMPLEMENTED", "message": "P1-5 前端接入前不强制 SSE"})
