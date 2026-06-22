"""Ops Desk 路由聚合。"""

from __future__ import annotations

from fastapi import APIRouter

from api.ops import lists, metrics

ops_router = APIRouter()
ops_router.include_router(metrics.router)
ops_router.include_router(lists.router)
