#!/usr/bin/env python3
"""Ops Desk P0-2 · MoonshotAI/kimi-code GHA sync 入口。"""

from __future__ import annotations

import sys
from pathlib import Path

# 允许从仓库根目录直接运行
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from api.ops.sync.runner import main

if __name__ == "__main__":
    raise SystemExit(main())
