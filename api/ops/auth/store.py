"""Ops Desk invite / session 存储。"""

from __future__ import annotations

import hashlib
import uuid
from datetime import datetime, timezone
from typing import Any, Literal

from api.ops.auth.duration import perpetual_session_expires_at
from api.rag_env import supabase_execute_with_retry

InviteError = Literal["invalid", "expired", "revoked"]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.strip().encode("utf-8")).hexdigest()


def _parse_iso(ts: str) -> datetime:
    return datetime.fromisoformat(str(ts).replace("Z", "+00:00"))


def is_auth_schema_error(exc: BaseException) -> bool:
    """PostgREST / Postgres：auth 表未 migration。"""
    text = str(exc).lower()
    needles = (
        "ops_desk_invites",
        "ops_desk_sessions",
        "pgrst205",
        "42p01",
        "does not exist",
        "could not find the table",
    )
    return any(n in text for n in needles)


class OpsAuthStore:
    """invite 兑换 + session 生命周期（仅 DB · 对齐 ChatBI access token 模式）。"""

    def __init__(self, client: Any) -> None:
        self.client = client

    def upsert_invite(
        self,
        label: str,
        raw_token: str,
        role: str,
        *,
        expires_at: datetime | None = None,
    ) -> None:
        """插入 invite 行（hash 存储）；同 hash 已存在则跳过。"""
        if role not in ("viewer", "maintainer"):
            raise ValueError("role must be viewer or maintainer")
        token_hash = _hash_token(raw_token)
        row: dict[str, Any] = {
            "label": label,
            "token_hash": token_hash,
            "role": role,
        }
        if expires_at is not None:
            row["expires_at"] = expires_at.isoformat().replace("+00:00", "Z")

        def _once() -> None:
            existing = (
                self.client.table("ops_desk_invites")
                .select("id")
                .eq("token_hash", token_hash)
                .limit(1)
                .execute()
            )
            rows = existing.data if isinstance(existing.data, list) else []
            if rows:
                return
            self.client.table("ops_desk_invites").insert(row).execute()

        supabase_execute_with_retry(_once)

    def _lookup_invite_row(
        self, token: str
    ) -> tuple[str | None, InviteError | None, datetime | None]:
        token_hash = _hash_token(token)

        def _once() -> tuple[str | None, InviteError | None, datetime | None]:
            res = (
                self.client.table("ops_desk_invites")
                .select("role, expires_at, revoked_at")
                .eq("token_hash", token_hash)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if not rows or not isinstance(rows[0], dict):
                return None, "invalid", None
            row = rows[0]
            if row.get("revoked_at"):
                return None, "revoked", None
            invite_expires: datetime | None = None
            raw_expires = row.get("expires_at")
            if raw_expires:
                invite_expires = _parse_iso(str(raw_expires))
                if invite_expires <= _now():
                    return None, "expired", None
            role = row.get("role")
            if role not in ("viewer", "maintainer"):
                return None, "invalid", None
            return role, None, invite_expires

        return supabase_execute_with_retry(_once)

    def redeem_invite_detail(
        self, token: str
    ) -> tuple[str | None, InviteError | None, datetime | None]:
        """校验 invite；返回 (role, error_code, invite_expires_at)。"""
        if not token.strip():
            return None, "invalid", None
        try:
            return self._lookup_invite_row(token)
        except Exception:
            return None, "invalid", None

    def redeem_invite(self, token: str) -> str | None:
        role, _err, _exp = self.redeem_invite_detail(token)
        return role

    def create_session(
        self,
        role: str,
        *,
        expires_at: datetime | None = None,
    ) -> dict[str, Any]:
        """Session 过期时刻与 invite 对齐；invite 永不过期则用固定远未来（不读 env）。"""
        session_expires = (
            expires_at if expires_at is not None else perpetual_session_expires_at(now=_now())
        )
        session_id = str(uuid.uuid4())
        payload = {
            "id": session_id,
            "role": role,
            "expires_at": session_expires.isoformat().replace("+00:00", "Z"),
        }

        def _once() -> dict[str, Any]:
            self.client.table("ops_desk_sessions").insert(payload).execute()
            return payload

        return supabase_execute_with_retry(_once)

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        if not session_id.strip():
            return None

        def _once() -> dict[str, Any] | None:
            res = (
                self.client.table("ops_desk_sessions")
                .select("id, role, expires_at, revoked_at")
                .eq("id", session_id.strip())
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if not rows or not isinstance(rows[0], dict):
                return None
            row = rows[0]
            if row.get("revoked_at"):
                return None
            expires_at = row.get("expires_at")
            if expires_at and _parse_iso(str(expires_at)) <= _now():
                return None
            return row

        return supabase_execute_with_retry(_once)

    def revoke_session(self, session_id: str) -> bool:
        if not session_id.strip():
            return False
        revoked_at = _now().isoformat().replace("+00:00", "Z")

        def _once() -> bool:
            self.client.table("ops_desk_sessions").update({"revoked_at": revoked_at}).eq(
                "id", session_id.strip()
            ).execute()
            return True

        return supabase_execute_with_retry(_once)
