"""Ops Desk 路由共享依赖。"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from fastapi import Header, HTTPException

from api.ops.constants import REPO_NAME, REPO_OWNER, legacy_secret_candidates
from api.rag_env import pick_supabase_service_key, pick_supabase_url
from supabase import create_client


@dataclass(frozen=True)
class OpsPrincipal:
    role: str  # viewer | maintainer
    source: str  # session | legacy_secret


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


def _resolve_session_principal(x_ops_session: str | None) -> OpsPrincipal | None:
    if not x_ops_session:
        return None
    from api.ops.auth.store import OpsAuthStore

    client = get_supabase_client()
    row = OpsAuthStore(client).get_session(x_ops_session)
    if not row:
        return None
    role = row.get("role")
    if role not in ("viewer", "maintainer"):
        return None
    return OpsPrincipal(role=role, source="session")


def _resolve_legacy_secret(x_ops_secret: str | None) -> OpsPrincipal | None:
    allowed = legacy_secret_candidates()
    if not allowed:
        return None
    if not x_ops_secret or x_ops_secret not in allowed:
        return None
    # M0 Python 不区分 viewer/maintainer；legacy 视为 maintainer 能力
    return OpsPrincipal(role="maintainer", source="legacy_secret")


def require_ops_access(
    x_ops_session: str | None = Header(default=None, alias="x-ops-session"),
    x_ops_secret: str | None = Header(default=None, alias="x-ops-secret"),
) -> OpsPrincipal:
    """P3-2a：优先 DB session，回退 M0 x-ops-secret。"""
    principal = _resolve_session_principal(x_ops_session)
    if principal:
        return principal
    principal = _resolve_legacy_secret(x_ops_secret)
    if principal:
        return principal
    if not legacy_secret_candidates() and not x_ops_session:
        # 本地/dev 未配置任何 legacy 秘钥且无 session 时放行（与 M0 一致）
        return OpsPrincipal(role="maintainer", source="legacy_secret")
    if not x_ops_session and not x_ops_secret:
        raise HTTPException(status_code=401, detail={"code": "OPS_AUTH_MISSING"})
    raise HTTPException(status_code=403, detail={"code": "OPS_AUTH_INVALID"})


def require_ops_secret(
    x_ops_session: str | None = Header(default=None, alias="x-ops-session"),
    x_ops_secret: str | None = Header(default=None, alias="x-ops-secret"),
) -> None:
    """兼容旧 Depends 签名；内部走 require_ops_access。"""
    require_ops_access(x_ops_session=x_ops_session, x_ops_secret=x_ops_secret)


def require_ops_maintainer(
    x_ops_session: str | None = Header(default=None, alias="x-ops-session"),
    x_ops_secret: str | None = Header(default=None, alias="x-ops-secret"),
) -> OpsPrincipal:
    principal = require_ops_access(x_ops_session=x_ops_session, x_ops_secret=x_ops_secret)
    if principal.role != "maintainer":
        raise HTTPException(status_code=403, detail={"code": "MAINTAINER_REQUIRED"})
    return principal
