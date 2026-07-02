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


def _supports_repo_root_flag() -> bool:
    """探测 CLI 是否支持 --repo-root（v0.10.1+ 未发布前勿传）。"""
    try:
        proc = subprocess.run(
            [probe_bin(), "verify", "--help"],
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return "--repo-root" in (proc.stdout + proc.stderr)


def _is_session_draft_task(task_path: Path) -> bool:
    parts = task_path.resolve().parts
    return "harness" in parts and "sessions" in parts


def _filter_session_promote_gate_errors(errors: list[str]) -> list[str]:
    """Session 草稿 promote：HG-AUDIT-R1 为业务仓开工闸，不阻塞复制。"""
    return [e for e in errors if "HG-AUDIT-R1" not in e]


def verify_for_session_promote(
    task_path: Path,
    *,
    timeout: int = 60,
) -> tuple[bool, dict[str, Any]]:
    """Session 草稿 promote 专用：task validate · 豁免 HG-AUDIT-R1 阻塞。"""
    ok, items = task_validate(task_path, timeout=timeout)
    errors: list[str] = []
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("errors"), list):
            errors.extend(str(e) for e in item["errors"])
    blocking = _filter_session_promote_gate_errors(errors)
    passed = len(blocking) == 0
    report: dict[str, Any] = {
        "passed": passed,
        "mode": "session_promote_validate",
        "items": items,
        "waived_gate_errors": [e for e in errors if "HG-AUDIT-R1" in e],
        "blocking_errors": blocking,
    }
    return passed, report


def verify_task(
    task_path: Path,
    *,
    repo_root: Path | None = None,
    ci: bool = True,
    timeout: int = 300,
) -> tuple[bool, dict[str, Any]]:
    """promote 前 verify · 返回 (passed, report)。"""
    if _is_session_draft_task(task_path):
        return verify_for_session_promote(task_path, timeout=min(timeout, 60))

    cmd = [probe_bin(), "verify", "--task", str(task_path.resolve()), "--format", "json"]
    if ci:
        cmd.append("--ci")
    run_cwd = repo_root.resolve() if repo_root is not None else None
    if repo_root is not None and _supports_repo_root_flag():
        cmd.extend(["--repo-root", str(repo_root.resolve())])
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
        cwd=str(run_cwd) if run_cwd is not None else None,
    )
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
