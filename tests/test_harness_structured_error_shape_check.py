"""Harness P1-3：结构化错误响应 shape 门禁测试。"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_harness_structured_error_shape_check_passes():
    proc = subprocess.run(
        [sys.executable, "tools/harness_structured_error_shape_check.py", "--check"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
