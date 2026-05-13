"""低置信 Text2SQL 澄清：一次性放行令牌（HMAC，无服务端会话表）。"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import time
from typing import Any

_PURPOSE = "clarify_text2sql_once"


def _token_secret() -> bytes:
    raw = (os.getenv("CHATBI_PLAN_EXEC_TOKEN_SECRET") or "").strip()
    if raw:
        return hashlib.sha256(raw.encode("utf-8")).digest()
    # 开发/单测回退：与 admin secret 派生，避免仓库内硬编码明文
    from .rag_env import admin_secret

    adm = (admin_secret() or "").strip()
    if adm:
        return hashlib.sha256(f"chatbi_plan_token|{adm}".encode("utf-8")).digest()
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


def mint_clarify_text2sql_bypass_token(*, session_id: str | None, query: str) -> str:
    """签发「跳过一轮 clarify」令牌：绑定 session + 问句指纹 + TTL。"""
    ttl = plan_token_ttl_s()
    payload: dict[str, Any] = {
        "v": 1,
        "p": _PURPOSE,
        "sid": (session_id or "")[:256],
        "qh": _query_fingerprint(query),
        "exp": int(time.time()) + ttl,
    }
    body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    sig = hmac.new(_token_secret(), body, hashlib.sha256).digest()
    raw = body + b"\n" + sig
    return base64.urlsafe_b64encode(raw).decode("ascii").rstrip("=")


def verify_clarify_text2sql_bypass_token(token: str | None, *, session_id: str | None, query: str) -> bool:
    if not isinstance(token, str) or not token.strip():
        return False
    try:
        raw = base64.urlsafe_b64decode(token.strip() + "==")
    except Exception:  # noqa: BLE001
        return False
    if b"\n" not in raw:
        return False
    body_b, sig_b = raw.rsplit(b"\n", 1)
    expect = hmac.new(_token_secret(), body_b, hashlib.sha256).digest()
    if not hmac.compare_digest(expect, sig_b):
        return False
    try:
        payload = json.loads(body_b.decode("utf-8"))
    except Exception:  # noqa: BLE001
        return False
    if payload.get("p") != _PURPOSE or int(payload.get("exp") or 0) < int(time.time()):
        return False
    if (payload.get("sid") or "") != (session_id or ""):
        return False
    if (payload.get("qh") or "") != _query_fingerprint(query):
        return False
    return True


def plan_preview_confirm_enabled() -> bool:
    """低置信澄清时是否走 SQL 预览 + plan_execution_token。

    默认 **开启**（未设置或空字符串视为开）；显式 ``0``/``false``/``no``/``off`` 关闭。
    仍须 ``CHATBI_V3_LOW_CONFIDENCE_CLARIFY`` 开启且命中澄清分支才会实际预览。
    """
    raw = (os.getenv("CHATBI_V3_PLAN_PREVIEW_CONFIRM") or "").strip().lower()
    if raw in ("0", "false", "no", "off"):
        return False
    return True
