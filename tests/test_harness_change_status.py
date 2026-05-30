# harness_change_status CLI 单元测试
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "tools" / "harness_change_status.py"
MOTHER_TASK = REPO_ROOT / "docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_status_json_mother_task() -> None:
    rel = str(MOTHER_TASK.relative_to(REPO_ROOT))
    proc = _run("--task", rel, "--json")
    assert proc.returncode == 0, proc.stderr
    data = json.loads(proc.stdout)
    assert data["task_slug"] == "p0-openspec-tdd"
    assert data["freeze_id"] == "HARNESS-P0-OPENSPEC-TDD-LOOP@2026-05-30"
    assert isinstance(data["human_gates"], list)
    assert data["pending_gates"] == []
    assert data["suggested_next_hat"] in {"22", "30", "40", "50", "CLOSE", None}
    assert "validate" in data
    assert data["validate"]["ok"] is True


def test_status_json_scenario_status_json(tmp_path: Path) -> None:
    task = tmp_path / "task_status.md"
    task.write_text(
        """
## Harness 元信息

| 字段 | 值 |
| **test_strategy** | `recommended` |
| **semi_auto** | `true` |
| **git_branch** | `task/foo` |
| **task_slug** | `status-demo` |
| **freeze_id** | `DEMO@2026-05-30` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
| HG-DEMO | pending | 30 | demo |

## 行为变更（Delta）

无

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| F1 | `fp-status-json` | x | error | 否 | msg |

## 验收标准

- [ ] pytest tests/foo.py
""",
        encoding="utf-8",
    )
    proc = _run("--task", str(task), "--json")
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert len(data["pending_gates"]) == 1
    assert data["pending_gates"][0]["gate_id"] == "HG-DEMO"
    assert data["suggested_next_hat"] == "22"
