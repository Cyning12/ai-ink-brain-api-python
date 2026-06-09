"""低置信澄清：一次性放行令牌（HMAC，无服务端会话表）。"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any

_PURPOSE_LEGACY = "clarify_text2sql_once"
_PURPOSE = "clarify_plan_once"
_SIG_LEN = 32  # HMAC-SHA256 digest size；签名字节中可出现 ``0x0a``，不得用 ``rsplit(b"\\n")`` 定界


def _token_secret() -> bytes:
    raw = (os.getenv("CHATBI_PLAN_EXEC_TOKEN_SECRET") or "").strip()
    if raw:
        return hashlib.sha256(raw.encode("utf-8")).digest()
    # 开发/单测回退：与 admin secret 派生，避免仓库内硬编码明文
    from .rag_env import admin_secret

    adm = (admin_secret() or "").strip()
    if adm:
        return hashlib.sha256(f"chatbi_plan_token|{adm}".encode()).digest()
    return b"chatbi_plan_token_dev_fallback"


def _query_fingerprint(query: str) -> str:
    q = (query or "").strip()
    return hashlib.sha256(q.encode("utf-8")).hexdigest()[:32]


def plan_token_ttl_s() -> int:
    try:
        v = int((os.getenv("CHATBI_PLAN_TOKEN_TTL_S") or "120").strip())
    except Exception:  # noqa: BLE001
        v = 120
    return max(30, min(600, v))


def mint_clarify_plan_bypass_token(*, session_id: str | None, query: str, tool: str) -> str:
    """签发「跳过一轮 clarify」令牌：绑定 session + 问句指纹 + 工具 + TTL。"""
    ttl = plan_token_ttl_s()
    payload: dict[str, Any] = {
        "v": 1,
        "p": _PURPOSE,
        "t": (tool or "").strip()[:64],
        "sid": (session_id or "")[:256],
        "qh": _query_fingerprint(query),
        "exp": int(time.time()) + ttl,
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    sig = hmac.new(_token_secret(), body, hashlib.sha256).digest()
    raw = body + b"\n" + sig
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def mint_clarify_text2sql_bypass_token(*, session_id: str | None, query: str) -> str:
    """兼容 5-2：等价于 ``mint_clarify_plan_bypass_token(..., tool=text2sql_query)``。"""
    return mint_clarify_plan_bypass_token(session_id=session_id, query=query, tool="text2sql_query")


def _b64url_decode_padded(token: str) -> bytes:
    """urlsafe base64 无填充串的可靠解码（禁止固定追加 ``==``，否则部分长度会误解码/验签偶发失败）。"""
    t = token.strip()
    pad = (-len(t)) % 4
    return base64.urlsafe_b64decode(t + ("=" * pad))


def _payload_tool(payload: dict[str, Any]) -> str:
    if payload.get("p") == _PURPOSE_LEGACY:
        return "text2sql_query"
    t = payload.get("t")
    return t if isinstance(t, str) else ""


def verify_clarify_plan_bypass_token(
    token: str | None, *, session_id: str | None, query: str, expected_tool: str
) -> bool:
    if not isinstance(token, str) or not token.strip():
        return False
    try:
        raw = _b64url_decode_padded(token)
    except Exception:  # noqa: BLE001
        return False
    if len(raw) < _SIG_LEN + 1:
        return False
    sig_b = raw[-_SIG_LEN:]
    rest = raw[:-_SIG_LEN]
    if not rest.endswith(b"\n"):
        return False
    body_b = rest[:-1]
    expect = hmac.new(_token_secret(), body_b, hashlib.sha256).digest()
    if not hmac.compare_digest(expect, sig_b):
        return False
    try:
        payload = json.loads(body_b.decode("utf-8"))
    except Exception:  # noqa: BLE001
        return False
    purpose = payload.get("p")
    if purpose not in (_PURPOSE, _PURPOSE_LEGACY):
        return False
    if int(payload.get("exp") or 0) < int(time.time()):
        return False
    if (payload.get("sid") or "") != (session_id or ""):
        return False
    if (payload.get("qh") or "") != _query_fingerprint(query):
        return False
    tool = _payload_tool(payload)
    return tool == (expected_tool or "").strip()


def verify_clarify_text2sql_bypass_token(token: str | None, *, session_id: str | None, query: str) -> bool:
    return verify_clarify_plan_bypass_token(
        token, session_id=session_id, query=query, expected_tool="text2sql_query"
    )


def plan_preview_confirm_enabled() -> bool:
    """低置信澄清时是否走方案预览 + plan_execution_token。

    默认 **开启**（未设置或空字符串视为开）；显式 ``0``/``false``/``no``/``off`` 关闭。
    仍须 ``CHATBI_V3_LOW_CONFIDENCE_CLARIFY`` 开启且命中澄清分支才会实际预览。
    """
    raw = (os.getenv("CHATBI_V3_PLAN_PREVIEW_CONFIRM") or "").strip().lower()
    if raw in ("0", "false", "no", "off"):
        return False
    return True
