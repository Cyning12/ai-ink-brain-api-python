"""Agently 学习轨 · Harness 文档审查 lab（与 harness_runtime 生产图隔离）。

规划：Projects/docs/harness/guides/RUNTIME_agently_parallel_learning_track_v0_zh.md
"""

from __future__ import annotations

from api.agently_lab.bootstrap import register_agently_lab_routes
from api.agently_lab.router import router as agently_lab_router

__all__ = ["agently_lab_router", "register_agently_lab_routes"]
