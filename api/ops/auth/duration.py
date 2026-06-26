"""Ops Desk 有效期解析（小时 / 天 · 支持小数 · 最小 0.01h）。"""

from __future__ import annotations

import math
from datetime import datetime, timedelta, timezone

MIN_DURATION_HOURS = 0.01
DEFAULT_SESSION_TTL_HOURS = 24.0


def resolve_duration_hours(
    *,
    hours: float | None = None,
    days: float | None = None,
) -> float | None:
    """解析有效期为小时；均未指定时返回 None（永不过期，仅 invite）。"""
    if hours is not None and days is not None:
        raise ValueError("仅指定 hours 或 days 之一")
    if hours is not None:
        h = float(hours)
    elif days is not None:
        h = float(days) * 24.0
    else:
        return None
    if not math.isfinite(h) or h < MIN_DURATION_HOURS:
        raise ValueError(f"有效期须 >= {MIN_DURATION_HOURS} 小时")
    return h


def parse_session_ttl_hours(raw: str | None) -> float:
    """从 env OPS_DESK_SESSION_TTL_HOURS 解析 session TTL（默认 24h）。"""
    if not (raw or "").strip():
        return DEFAULT_SESSION_TTL_HOURS
    try:
        h = float(raw.strip())
    except ValueError:
        return DEFAULT_SESSION_TTL_HOURS
    if not math.isfinite(h) or h < MIN_DURATION_HOURS:
        return DEFAULT_SESSION_TTL_HOURS
    return h


def expires_at_from_hours(hours: float, *, now: datetime | None = None) -> datetime:
    """自 now 起 hours 小时后的 UTC 时刻。"""
    base = now or datetime.now(timezone.utc)
    ttl = max(MIN_DURATION_HOURS, float(hours))
    return base + timedelta(seconds=ttl * 3600.0)


def perpetual_session_expires_at(*, now: datetime | None = None) -> datetime:
    """invite 无 expires_at 时 session 的绝对过期时刻（固定远未来 · 不读 env）。"""
    return datetime(2099, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
