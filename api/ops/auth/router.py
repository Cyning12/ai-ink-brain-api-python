"""Ops Desk auth 路由：login / logout / session。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from api.ops.auth.store import OpsAuthStore, is_auth_schema_error
from api.ops.deps import get_supabase_client

router = APIRouter(prefix="/ops/auth", tags=["ops-auth"])

# 用户可见文案：简短 · 无项目内部信息
_INVITE_ERROR_MESSAGES = {
    "expired": "秘钥已过期",
    "revoked": "秘钥无效",
    "invalid": "秘钥无效",
}


class LoginRequest(BaseModel):
    token: str


def _auth_store(client: Any = Depends(get_supabase_client)) -> OpsAuthStore:
    return OpsAuthStore(client)


@router.post("/login")
def auth_login(body: LoginRequest, store: OpsAuthStore = Depends(_auth_store)) -> dict[str, Any]:
    try:
        role, invite_err, invite_expires_at = store.redeem_invite_detail(body.token)
    except Exception as exc:
        if is_auth_schema_error(exc):
            raise HTTPException(
                status_code=503,
                detail={
                    "code": "AUTH_SCHEMA_MISSING",
                    "message": "服务暂不可用",
                },
            ) from exc
        raise

    if not role:
        code = "INVITE_EXPIRED" if invite_err == "expired" else "INVITE_INVALID"
        raise HTTPException(
            status_code=401,
            detail={
                "code": code,
                "message": _INVITE_ERROR_MESSAGES.get(invite_err or "invalid", "秘钥无效"),
            },
        )

    try:
        session = store.create_session(role, expires_at=invite_expires_at)
    except Exception as exc:
        if is_auth_schema_error(exc):
            raise HTTPException(
                status_code=503,
                detail={
                    "code": "AUTH_SCHEMA_MISSING",
                    "message": "服务暂不可用",
                },
            ) from exc
        raise

    return {
        "ok": True,
        "session_id": session["id"],
        "role": role,
        "expires_at": session["expires_at"],
    }


@router.get("/session")
def auth_session(
    x_ops_session: str | None = Header(default=None, alias="x-ops-session"),
    store: OpsAuthStore = Depends(_auth_store),
) -> dict[str, Any]:
    if not x_ops_session:
        raise HTTPException(
            status_code=401,
            detail={"code": "SESSION_MISSING", "message": "未登录"},
        )
    row = store.get_session(x_ops_session)
    if not row:
        raise HTTPException(
            status_code=401,
            detail={"code": "SESSION_EXPIRED", "message": "登录已过期"},
        )
    return {
        "ok": True,
        "role": row.get("role"),
        "expires_at": row.get("expires_at"),
    }


@router.post("/logout")
def auth_logout(
    x_ops_session: str | None = Header(default=None, alias="x-ops-session"),
    store: OpsAuthStore = Depends(_auth_store),
) -> dict[str, Any]:
    if x_ops_session:
        store.revoke_session(x_ops_session)
    return {"ok": True}
