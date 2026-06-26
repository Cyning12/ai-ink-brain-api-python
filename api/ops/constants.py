"""Ops Desk 共享常量。"""

from __future__ import annotations

import os

REPO_OWNER = "MoonshotAI"
REPO_NAME = "kimi-code"
DEFAULT_DAYS = 30
MAX_LIMIT = 100

OPS_SECRET_ENV = "OPS_DESK_SECRET"
OPS_SECRET_TEST_ENV = "OPS_DESK_SECRET_TEST"
OPS_SECRET_TEST_DEFAULT = "test"


def legacy_secret_candidates() -> frozenset[str]:
    """生产秘钥 + 门禁测试秘钥（pytest / CI 用 OPS_DESK_SECRET_TEST，与本地 .env 生产值隔离）。"""
    out: set[str] = set()
    for name in (OPS_SECRET_ENV, OPS_SECRET_TEST_ENV):
        val = (os.getenv(name) or "").strip()
        if val:
            out.add(val)
    return frozenset(out)
