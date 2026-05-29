"""ChatBI V3 P2-1b：高消耗端点按客户端 IP 的滑动窗口限流。"""

from __future__ import annotations

import logging
import os
import time
from collections import defaultdict
from dataclasses import dataclass
from threading import Lock
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)

# 与 task / SPEC-ChatBI-V3-Resilience-Ops §2 对齐的高消耗路径（仅 POST）
_PROTECTED_POST_PATHS = frozenset(
    {
        "/api/py/chat",
        "/api/py/unified/chat/stream",
    }
)

_DEFAULT_MAX_REQUESTS = 60
_DEFAULT_WINDOW_SEC = 60.0


@dataclass(frozen=True)
class RateLimitConfig:
    enabled: bool
    max_requests: int
    window_sec: float


def _parse_bool(raw: str | None, *, default: bool) -> bool:
    if raw is None or not str(raw).strip():
        return default
    val = str(raw).strip().lower()
    if val in {"1", "true", "yes", "on"}:
        return True
    if val in {"0", "false", "no", "off"}:
        return False
    return default


def _parse_positive_int(raw: str | None, *, default: int, field: str) -> int:
    if raw is None or not str(raw).strip():
        return default
    try:
        val = int(str(raw).strip())
    except ValueError:
        logger.warning(
            "chatbi_rate_limit: invalid %s=%r, fallback to %s",
            field,
            raw,
            default,
        )
        return default
    if val < 0:
        logger.warning(
            "chatbi_rate_limit: invalid %s=%s, fallback to %s",
            field,
            val,
            default,
        )
        return default
    return val


def _parse_positive_float(raw: str | None, *, default: float, field: str) -> float:
    if raw is None or not str(raw).strip():
        return default
    try:
        val = float(str(raw).strip())
    except ValueError:
        logger.warning(
            "chatbi_rate_limit: invalid %s=%r, fallback to %s",
            field,
            raw,
            default,
        )
        return default
    if val <= 0:
        logger.warning(
            "chatbi_rate_limit: invalid %s=%s, fallback to %s",
            field,
            val,
            default,
        )
        return default
    return val


def load_rate_limit_config() -> RateLimitConfig:
    """从 env 加载限流配置；非法值回退默认并打告警（F2）。"""
    enabled = _parse_bool(os.getenv("CHATBI_RATE_LIMIT_ENABLED"), default=True)
    max_requests = _parse_positive_int(
        os.getenv("CHATBI_RATE_LIMIT_MAX_REQUESTS"),
        default=_DEFAULT_MAX_REQUESTS,
        field="CHATBI_RATE_LIMIT_MAX_REQUESTS",
    )
    window_sec = _parse_positive_float(
        os.getenv("CHATBI_RATE_LIMIT_WINDOW_SEC"),
        default=_DEFAULT_WINDOW_SEC,
        field="CHATBI_RATE_LIMIT_WINDOW_SEC",
    )
    if max_requests == 0:
        enabled = False
    return RateLimitConfig(enabled=enabled, max_requests=max_requests, window_sec=window_sec)


class _InMemorySlidingWindowLimiter:
    def __init__(self) -> None:
        self._timestamps: dict[str, list[float]] = defaultdict(list)
        self._lock = Lock()

    def reset_for_tests(self) -> None:
        with self._lock:
            self._timestamps.clear()

    def check(self, key: str, config: RateLimitConfig) -> tuple[bool, int | None]:
        if not config.enabled or config.max_requests <= 0:
            return True, None
        now = time.monotonic()
        window = config.window_sec
        with self._lock:
            bucket = self._timestamps[key]
            cutoff = now - window
            bucket[:] = [t for t in bucket if t > cutoff]
            if len(bucket) >= config.max_requests:
                oldest = bucket[0]
                retry_after = max(1, int(window - (now - oldest)) + 1)
                return False, retry_after
            bucket.append(now)
        return True, None


_limiter = _InMemorySlidingWindowLimiter()


def reset_rate_limit_state_for_tests() -> None:
    """单测隔离：清空内存桶。"""
    _limiter.reset_for_tests()


def client_ip_from_request(request: Request) -> str:
    forwarded = (request.headers.get("x-forwarded-for") or "").strip()
    if forwarded:
        return forwarded.split(",")[0].strip() or "unknown"
    if request.client and request.client.host:
        return request.client.host
    return "unknown"


def rate_limit_response_body(retry_after: int | None) -> dict[str, Any]:
    body: dict[str, Any] = {
        "ok": False,
        "error_code": "RATE_LIMIT_EXCEEDED",
        "message": "请求过于频繁，请稍后重试",
    }
    if retry_after is not None:
        body["retry_after"] = retry_after
    return body


def register_rate_limit_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def chatbi_rate_limit_middleware(request: Request, call_next):  # type: ignore[no-untyped-def]
        path = request.url.path
        if request.method.upper() != "POST" or path not in _PROTECTED_POST_PATHS:
            return await call_next(request)

        config = load_rate_limit_config()
        client_key = f"ip:{client_ip_from_request(request)}"
        allowed, retry_after = _limiter.check(client_key, config)
        if not allowed:
            return JSONResponse(
                status_code=429,
                content=rate_limit_response_body(retry_after),
                headers={"Retry-After": str(retry_after)} if retry_after is not None else None,
            )
        return await call_next(request)
