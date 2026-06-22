"""Ops Desk metrics 路由。"""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from api.ops.constants import DEFAULT_DAYS
from api.ops.deps import get_supabase_client, require_ops_secret
from api.ops.queries import OpsQueries

router = APIRouter(prefix="/ops/metrics", tags=["ops-metrics"])


def ops_queries() -> OpsQueries:
    return OpsQueries(get_supabase_client())


@router.get("/cycle-time")
def cycle_time(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    return queries.cycle_time_metric(days)


@router.get("/review-time")
def review_time(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    return queries.review_time_metric(days)


@router.get("/issue-throughput")
def issue_throughput(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    return queries.issue_throughput_metric(days)
