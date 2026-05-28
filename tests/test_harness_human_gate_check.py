# Harness human_gate 门禁脚本单元测试
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "tools" / "harness_human_gate_check.py"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_pending_gate_fails_on_mother_task() -> None:
    proc = _run("--task", "docs/tasks/active/task_harness_wiki_loop_unit_a_v1.md")
    assert proc.returncode == 1
    assert "HG-LOOP-BATCH" in proc.stderr
    assert "pending" in proc.stderr.lower() or "HARNESS_HUMAN_GATE_FAIL" in proc.stderr


def test_parse_approved_tmp_task(tmp_path: Path) -> None:
    task = tmp_path / "task_ok.md"
    task.write_text(
        """
### 人工闸 `human_gate`
| human_gate_id | status | blocks_hats | 说明 |
| HG-TEST | approved | 30 | ok |
""",
        encoding="utf-8",
    )
    proc = _run("--task", str(task))
    assert proc.returncode == 0, proc.stderr
