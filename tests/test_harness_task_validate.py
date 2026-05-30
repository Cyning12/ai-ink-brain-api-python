# harness_task_validate CLI 与规则单元测试
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
TOOL = REPO_ROOT / "tools" / "harness_task_validate.py"
R1_TASK = REPO_ROOT / "docs/tasks/active/task_harness_p0_task_validate_v1.md"


def _run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOL), *args],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )


def test_validate_r1_task_exit_zero() -> None:
    proc = _run(str(R1_TASK.relative_to(REPO_ROOT)))
    assert proc.returncode == 0, proc.stdout + proc.stderr


def test_validate_active_scenario(tmp_path: Path) -> None:
    task = tmp_path / "task_ok.md"
    task.write_text(
        """
## Harness 元信息

| 字段 | 值 |
| **test_strategy** | `required` |
| **semi_auto** | `true` |
| **git_branch** | `task/foo` |

## 范围

- [ ] 新增 `tools/harness_task_validate.py`

## 行为变更（Delta）

### ADDED

- **Requirement**：CLI 校验 task
  - **Scenario**：`validate-active` — GIVEN active task WHEN run validate THEN 报告清单

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| F1 | `fp-validate-active` | 缺字段 | error | 改 task | 规则 ID |

## 验收标准

- [ ] `pytest tests/test_harness_task_validate.py` 绿
""",
        encoding="utf-8",
    )
    proc = _run(str(task))
    assert proc.returncode == 0, proc.stdout + proc.stderr
    assert "OK" in proc.stdout


def test_fp_validate_api_na(tmp_path: Path) -> None:
    task = tmp_path / "task_api_na.md"
    task.write_text(
        """
## Harness 元信息

| 字段 | 值 |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | docs only |
| **semi_auto** | `true` |
| **git_branch** | `task/foo` |

## 范围

- [ ] 改 `api/index.py`

## 行为变更（Delta）

无

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| F1 | `fp-x` | x | error | 否 | msg |

## 验收标准

- [ ] 文档更新
""",
        encoding="utf-8",
    )
    proc = _run(str(task))
    assert proc.returncode == 1
    assert "API-NOT-APPLICABLE" in proc.stdout


def test_fp_validate_missing_fp(tmp_path: Path) -> None:
    task = tmp_path / "task_no_fp.md"
    task.write_text(
        """
## Harness 元信息

| 字段 | 值 |
| **test_strategy** | `required` |
| **semi_auto** | `true` |
| **git_branch** | `task/foo` |

## 范围

- [ ] tools only

## 行为变更（Delta）

无

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |

## 验收标准

- [ ] pytest tests/foo.py 绿
""",
        encoding="utf-8",
    )
    proc = _run(str(task))
    assert proc.returncode == 1
    assert "FAILURE-PATHS-EMPTY" in proc.stdout


def test_json_output(tmp_path: Path) -> None:
    task = tmp_path / "task_json.md"
    task.write_text(
        """
## Harness 元信息

| 字段 | 值 |
| **test_strategy** | `required` |
| **semi_auto** | `true` |
| **git_branch** | `task/foo` |

## 行为变更（Delta）

无

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| F1 | `fp-json` | x | error | 否 | msg |

## 验收标准

- [ ] pytest tests/x.py 绿
""",
        encoding="utf-8",
    )
    proc = _run("--json", str(task))
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data[0]["ok"] is True
    assert data[0]["errors"] == []


def test_all_active_runs() -> None:
    proc = _run("--all-active")
    assert proc.returncode in (0, 1)
    assert proc.stdout.strip()
