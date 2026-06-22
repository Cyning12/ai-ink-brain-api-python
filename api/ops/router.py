"""Ops Desk 路由聚合。"""

from __future__ import annotations

from fastapi import APIRouter

from api.ops import chat, lists, metrics, runs
from api.ops.scan import router as scan_router

ops_router = APIRouter()
ops_router.include_router(metrics.router)
ops_router.include_router(lists.router)
ops_router.include_router(chat.router)
ops_router.include_router(runs.router)
ops_router.include_router(scan_router)
