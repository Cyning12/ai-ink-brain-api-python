"""闸口 C jsonPKmermaid fixtures：pytest 默认只读，避免日常跑测污染 Git 工作区。"""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1"
MATERIALIZE_SCRIPT = FIXTURE_ROOT / "scripts/materialize_gate_c_payloads.py"
MATERIALIZE_REPORT = FIXTURE_ROOT / "payloads/materialize_report.json"

# 显式设为 1 时才重写 fixtures（CI 更新快照或闸口 C 实验复现时用）
UPDATE_ENV = "GATE_CTX_C_UPDATE_FIXTURES"


def materialize_gate_c_payloads_if_requested() -> None:
    """默认不物化；仅校验已提交的 payload/report 存在。"""
    if os.environ.get(UPDATE_ENV, "").strip() == "1":
        proc = subprocess.run(
            [sys.executable, str(MATERIALIZE_SCRIPT)],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        assert proc.returncode == 0, proc.stderr or proc.stdout
        return

    d_dir = FIXTURE_ROOT / "payloads/CTX_V2_QUERY"
    e_dir = FIXTURE_ROOT / "payloads/CTX_DUAL_MD"
    assert MATERIALIZE_REPORT.is_file(), (
        f"missing {MATERIALIZE_REPORT.relative_to(REPO_ROOT)}; "
        f"run with {UPDATE_ENV}=1 pytest … to regenerate"
    )
    assert d_dir.is_dir() and any(d_dir.glob("*.json")), "missing CTX_V2_QUERY payloads"
    assert e_dir.is_dir() and any(e_dir.glob("*.md")), "missing CTX_DUAL_MD payloads"
