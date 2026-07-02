"""harness-probe subprocess 适配（S4 · B7 · 禁止 Runtime import probe）。"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Any


def probe_bin() -> str:
    return os.environ.get("HARNESS_PROBE_BIN", "harness-probe")


def probe_available() -> bool:
    return shutil.which(probe_bin()) is not None


def task_validate(task_path: Path, *, timeout: int = 30) -> tuple[bool, list[Any]]:
    """轻量 task validate · 返回 (ok, items)。"""
    proc = subprocess.run(
        [probe_bin(), "task", "validate", "--task", str(task_path.resolve()), "--format", "json"],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    raw = proc.stdout.strip() or "[]"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = []
    items = data if isinstance(data, list) else [data]
    ok = proc.returncode == 0 and all(
        isinstance(x, dict) and x.get("ok", True) for x in items if isinstance(x, dict)
    )
    if proc.returncode != 0 and not items:
        items = [{"ok": False, "stderr": proc.stderr}]
    return ok, items


def verify_task(
    task_path: Path,
    *,
    repo_root: Path | None = None,
    ci: bool = True,
    timeout: int = 300,
) -> tuple[bool, dict[str, Any]]:
    """promote 前 verify · 返回 (passed, report)。"""
    cmd = [probe_bin(), "verify", "--task", str(task_path.resolve()), "--format", "json"]
    if ci:
        cmd.append("--ci")
    if repo_root is not None:
        cmd.extend(["--repo-root", str(repo_root.resolve())])
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False)
    raw = proc.stdout.strip() or "{}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"passed": False, "raw_stdout": raw, "stderr": proc.stderr}
    if not isinstance(data, dict):
        data = {"passed": proc.returncode == 0, "items": data}
    passed = proc.returncode == 0 and bool(data.get("passed", proc.returncode == 0))
    data.setdefault("exit_code", proc.returncode)
    if proc.stderr:
        data.setdefault("stderr", proc.stderr)
    return passed, data
