"""Agently lab 功能开关（默认关闭 · 本地/线上分别控制）。"""

from __future__ import annotations

import os


def _truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes", "on")


def is_agently_lab_enabled() -> bool:
    """挂载路由与 doc-review API；默认 false。"""
    return _truthy("AGENTLY_LAB_ENABLED")


def is_agently_lab_online() -> bool:
    """线上 maintainer 模式（GitHub 读 path 等）；须同时开启 ENABLED。"""
    return is_agently_lab_enabled() and _truthy("AGENTLY_LAB_ONLINE")
