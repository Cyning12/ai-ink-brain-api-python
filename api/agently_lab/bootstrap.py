"""将 agently_lab 路由挂到 FastAPI app。"""

from __future__ import annotations

from fastapi import FastAPI

from api.agently_lab.router import router as agently_lab_router


def register_agently_lab_routes(app: FastAPI, *, prefix: str = "/api/py") -> None:
    """注册 lab 路由；单路由内用 AGENTLY_LAB_ENABLED 控制 404。"""
    app.include_router(agently_lab_router, prefix=prefix)
