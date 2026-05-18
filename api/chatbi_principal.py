"""ChatBI V3：Bearer → chatbi_access_tokens → ChatBiPrincipal（仅 DB 校验链）。"""

from __future__ import annotations

import asyncio
import uuid
from dataclasses import dataclass
from typing import Any, Literal

from fastapi import Header, HTTPException

from .chatbi_access_hash import hash_chatbi_access_token
from .chatbi_json_log import chatbi_json_log_enabled, log_chatbi_record
from .rag_env import supabase_client, supabase_execute_with_retry, transient_supabase_network_error

PrincipalKind = Literal["super", "admin", "end_user"]


@dataclass(frozen=True)
class ChatBiPrincipal:
    """Unified Chat / Text2SQL / RAG 闸门的统一主体。"""

    principal_kind: PrincipalKind
    access_level: int
    subject_user_id: str | None
    token_id: uuid.UUID


def _kind_for_level(level: int) -> PrincipalKind:
    if level <= 0:
        return "super"
    if level == 1:
        return "admin"
    return "end_user"


def _fetch_token_row_by_hash(key_hash: str) -> dict[str, Any] | None:
    def _once() -> dict[str, Any] | None:
        sb = supabase_client()
        res = (
            sb.table("chatbi_access_tokens")
            .select("id,access_level,subject_user_id,expires_at,revoked_at")
            .eq("key_hash", key_hash)
            .is_("revoked_at", "null")
            .limit(1)
            .execute()
        )
        rows = getattr(res, "data", None) or []
        if not rows:
            return None
        r0 = rows[0]
        return r0 if isinstance(r0, dict) else None

    return supabase_execute_with_retry(_once)


def _supabase_unavailable_http(exc: BaseException) -> HTTPException:
    return HTTPException(
        status_code=500,
        detail={
            "code": "DATABASE_DISCONNECT",
            "error_type": "DATABASE_DISCONNECT",
            "message_zh": "数据库连接不可用，请稍后重试",
            "message": str(exc),
        },
    )


def _parse_uuid(val: Any) -> uuid.UUID | None:
    if val is None:
        return None
    try:
        return uuid.UUID(str(val))
    except Exception:  # noqa: BLE001
        return None


def _resolve_principal_sync(authorization: str | None, *, request_id: str | None) -> ChatBiPrincipal:
    bearer = ""
    if authorization and authorization.lower().startswith("bearer "):
        bearer = authorization[7:].strip()
    if not bearer:
        if chatbi_json_log_enabled():
            log_chatbi_record(
                message="auth_fail",
                event="auth_fail",
                request_id=request_id,
                reason="missing_bearer",
            )
        raise HTTPException(
            status_code=401,
            detail={
                "code": "CHATBI_UNAUTHORIZED",
                "reason": "missing_bearer",
                "message_zh": "未授权",
            },
        )

    key_hash = hash_chatbi_access_token(bearer)
    try:
        row = _fetch_token_row_by_hash(key_hash)
    except Exception as exc:  # noqa: BLE001
        if transient_supabase_network_error(exc):
            if chatbi_json_log_enabled():
                log_chatbi_record(
                    message="auth_fail",
                    event="auth_fail",
                    request_id=request_id,
                    reason="supabase_unreachable",
                )
            raise _supabase_unavailable_http(exc) from exc
        raise
    if row is None:
        if chatbi_json_log_enabled():
            log_chatbi_record(
                message="auth_fail",
                event="auth_fail",
                request_id=request_id,
                reason="bad_hash",
            )
        raise HTTPException(
            status_code=401,
            detail={
                "code": "CHATBI_UNAUTHORIZED",
                "reason": "bad_hash",
                "message_zh": "未授权",
            },
        )

    if row.get("revoked_at") is not None:
        if chatbi_json_log_enabled():
            log_chatbi_record(
                message="auth_fail",
                event="auth_fail",
                request_id=request_id,
                reason="revoked",
                token_id=str(row.get("id") or ""),
            )
        raise HTTPException(
            status_code=401,
            detail={"code": "CHATBI_UNAUTHORIZED", "reason": "revoked", "message_zh": "未授权"},
        )

    exp = row.get("expires_at")
    if exp is not None and str(exp).strip():
        # 由 DB 比较更准；此处仅防御性解析 ISO 字符串
        from datetime import datetime, timezone

        try:
            exp_s = str(exp).replace("Z", "+00:00")
            exp_dt = datetime.fromisoformat(exp_s)
            if exp_dt.tzinfo is None:
                exp_dt = exp_dt.replace(tzinfo=timezone.utc)
            if exp_dt < datetime.now(timezone.utc):
                if chatbi_json_log_enabled():
                    log_chatbi_record(
                        message="auth_fail",
                        event="auth_fail",
                        request_id=request_id,
                        reason="expired",
                        token_id=str(row.get("id") or ""),
                    )
                raise HTTPException(
                    status_code=401,
                    detail={"code": "CHATBI_UNAUTHORIZED", "reason": "expired", "message_zh": "未授权"},
                )
        except HTTPException:
            raise
        except Exception:  # noqa: BLE001
            pass

    level_raw = row.get("access_level")
    try:
        access_level = int(level_raw)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=500, detail="Invalid access_level in token row") from exc
    if access_level not in (0, 1, 2):
        raise HTTPException(status_code=500, detail="Invalid access_level in token row")

    subj = row.get("subject_user_id")
    subject_user_id = str(subj).strip() if subj is not None and str(subj).strip() else None
    if access_level == 2 and not subject_user_id:
        if chatbi_json_log_enabled():
            log_chatbi_record(
                message="auth_fail",
                event="auth_fail",
                request_id=request_id,
                reason="l2_missing_subject",
                token_id=str(row.get("id") or ""),
            )
        raise HTTPException(
            status_code=401,
            detail={
                "code": "CHATBI_UNAUTHORIZED",
                "reason": "l2_missing_subject",
                "message_zh": "未授权",
            },
        )

    tid = _parse_uuid(row.get("id"))
    if tid is None:
        raise HTTPException(status_code=500, detail="Invalid token id")

    principal = ChatBiPrincipal(
        principal_kind=_kind_for_level(access_level),
        access_level=access_level,
        subject_user_id=subject_user_id,
        token_id=tid,
    )
    if chatbi_json_log_enabled():
        log_chatbi_record(
            message="auth_ok",
            event="auth_ok",
            request_id=request_id,
            principal_kind=principal.principal_kind,
            token_id=str(principal.token_id),
        )
    return principal


def resolve_chatbi_from_plain_token(plain: str, *, request_id: str | None = None) -> ChatBiPrincipal:
    """非 Depends 场景（如 RAG history 双轨鉴权）：明文 token → 与 Unified 相同的 DB 校验链。"""
    t = plain.strip()
    if t.lower().startswith("bearer "):
        t = t[7:].strip()
    return _resolve_principal_sync(f"Bearer {t}" if t else None, request_id=request_id)


async def require_chatbi_principal(
    authorization: str | None = Header(default=None),
    x_request_id: str | None = Header(default=None, alias="x-request-id"),
) -> ChatBiPrincipal:
    """FastAPI Depends：仅接受 `Authorization: Bearer`，校验 `chatbi_access_tokens.key_hash`。"""
    rid = (x_request_id or "").strip() or None
    return await asyncio.to_thread(_resolve_principal_sync, authorization, request_id=rid)
