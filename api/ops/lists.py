"""Ops Desk issues / pulls 列表路由。"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from api.ops.constants import DEFAULT_DAYS, MAX_LIMIT
from api.ops.deps import get_supabase_client, require_ops_secret
from api.ops.queries import OpsQueries

router = APIRouter(prefix="/ops", tags=["ops-lists"])


def ops_queries() -> OpsQueries:
    return OpsQueries(get_supabase_client())


@router.get("/issues")
def list_issues(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    state: Annotated[str | None, Query()] = None,
    label: Annotated[str | None, Query()] = None,
    module: Annotated[str | None, Query()] = None,
    age: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_LIMIT)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    items, total = queries.fetch_issues(
        days=days,
        state=state,
        label=label,
        module=module,
        age=age,
        limit=limit,
        offset=offset,
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}


@router.get("/pulls")
def list_pulls(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    state: Annotated[str | None, Query()] = None,
    ci: Annotated[str | None, Query()] = None,
    author: Annotated[str | None, Query()] = None,
    limit: Annotated[int, Query(ge=1, le=MAX_LIMIT)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    items, total = queries.fetch_pulls(
        days=days, state=state, ci=ci, author=author, limit=limit, offset=offset
    )
    return {"items": items, "total": total, "limit": limit, "offset": offset}
