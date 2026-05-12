"""ChatBI V3 P0-2：单行 JSON 结构化日志（与 SPEC-ChatBI-V3-Logging-Trace 对齐）。"""

from __future__ import annotations

import json
import logging
import os
from datetime import datetime, timezone
from typing import Any

_LOGGER = logging.getLogger("chatbi.obs")


def _ensure_json_only_handler() -> None:
    """独立 logger，避免默认格式污染 JSON 行。"""
    if _LOGGER.handlers:
        return
    _LOGGER.setLevel(logging.INFO)
    _LOGGER.propagate = False
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("%(message)s"))
    _LOGGER.addHandler(h)


def chatbi_json_log_enabled() -> bool:
    raw = (os.getenv("CHATBI_JSON_LOG", "") or "").strip().lower()
    return raw in ("1", "true", "yes", "on")


def log_chatbi_record(*, message: str, level: int = logging.INFO, **extra: Any) -> None:
    """输出一行 JSON；未开启 CHATBI_JSON_LOG 时 no-op。"""
    if not chatbi_json_log_enabled():
        return
    rec: dict[str, Any] = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": logging.getLevelName(level),
        "message": message,
        "service": "chatbi-api",
    }
    for k, v in extra.items():
        if v is not None:
            rec[k] = v
    try:
        line = json.dumps(rec, ensure_ascii=False, default=str)
    except Exception:  # noqa: BLE001
        line = json.dumps(
            {
                "timestamp": rec.get("timestamp", ""),
                "message": message,
                "service": "chatbi-api",
                "error": "log_json_serialize_failed",
            },
            ensure_ascii=False,
        )
    _ensure_json_only_handler()
    _LOGGER.log(level, line)
