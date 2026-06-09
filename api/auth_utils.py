"""Admin / API_KEY 认证工具（供 admin 路由与 legacy_chat 共用）。"""

from __future__ import annotations

import hmac

from fastapi import HTTPException

from .rag_env import admin_secret, api_key_optional


def _require_auth(
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None = None,
) -> None:
    expected_admin = admin_secret()
    expected_api = api_key_optional()
    if not expected_admin and not expected_api:
        raise HTTPException(status_code=500, detail="未配置 SYNC_ADMIN_SECRET 或 API_KEY")
    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif x_blog_admin_token:
        token = x_blog_admin_token.strip()
    elif x_admin_token:
        token = x_admin_token.strip()

    def _match(expected: str | None) -> bool:
        if not expected:
            return False
        if len(token) != len(expected):
            return False
        return hmac.compare_digest(token.encode("utf-8"), expected.encode("utf-8"))

    if not (_match(expected_admin) or _match(expected_api)):
        raise HTTPException(status_code=401, detail="Unauthorized")
