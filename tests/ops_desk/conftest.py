"""Ops Desk 测试公共 fixture · 门禁秘钥真值。"""

from __future__ import annotations

import os

# 门禁：fixture 发送 x-ops-secret: test 时对齐 OPS_DESK_SECRET_TEST，不依赖生产 OPS_DESK_SECRET
os.environ.setdefault("OPS_DESK_SECRET_TEST", os.getenv("OPS_DESK_SECRET_TEST") or "test")
