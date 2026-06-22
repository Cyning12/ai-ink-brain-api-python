"""Ops Desk 路由共享依赖。"""

from __future__ import annotations

import os
from typing import Any

from fastapi import Header, HTTPException

from api.ops.constants import OPS_SECRET_ENV, REPO_NAME, REPO_OWNER
from api.rag_env import pick_supabase_service_key, pick_supabase_url
from supabase import create_client


def require_ops_secret(x_ops_secret: str | None = Header(default=None, alias="x-ops-secret")) -> None:
    """轻量 M0 鉴权：前端 /ops 路由共享 OPS_DESK_SECRET。"""
    expected = (os.getenv(OPS_SECRET_ENV) or "").strip()
    if not expected:
        return
    if not x_ops_secret:
        raise HTTPException(status_code=401, detail={"code": "OPS_SECRET_MISSING"})
    if x_ops_secret != expected:
        raise HTTPException(status_code=403, detail={"code": "OPS_SECRET_INVALID"})


def get_supabase_client() -> Any:
    url = pick_supabase_url()
    key = pick_supabase_service_key()
    if not url or not key:
        raise HTTPException(
            status_code=500,
            detail={"code": "DATABASE_DISCONNECT", "message": "Supabase 配置缺失"},
        )
    return create_client(url, key)


def get_default_repo() -> dict[str, str]:
    return {"owner": REPO_OWNER, "name": REPO_NAME, "full_name": f"{REPO_OWNER}/{REPO_NAME}"}
