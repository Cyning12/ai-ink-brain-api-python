"""harness_runtime import 边界动态测试（隔离进程 + sys.modules）。

在干净 Python 进程中 import `api.harness_runtime` 及关键子模块，验证无黑名单模块
被加载（fp-import-chat-dynamic / fp-import-rag-dynamic / fp-import-probe）。
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

FORBIDDEN_MODULE_ROOTS = (
    "api.ingest",
    "api.rag",
    "api.index",
    "public.documents",
    "harness_probe",
)

# 关键子模块：覆盖 graph / nodes / store / adapters / promote 等 S0–S4 落点
_IMPORT_STATEMENT = """
import sys
import json

import api.harness_runtime
import api.harness_runtime.adapters.probe_runner
import api.harness_runtime.gate_sync.human_gate
import api.harness_runtime.session_store.io
import api.harness_runtime.session_store.schema
import api.harness_runtime.graph.session_orchestrator_v1
import api.harness_runtime.nodes.session_00
import api.harness_runtime.nodes.session_subagent
import api.harness_runtime.session_orchestrator
import api.harness_runtime.promote
import api.harness_runtime.deliverables
import api.harness_runtime.errors
import api.harness_runtime.state

print(json.dumps(sorted(sys.modules.keys())))
"""


def _is_forbidden(name: str) -> str | None:
    for forbidden in FORBIDDEN_MODULE_ROOTS:
        if name == forbidden or name.startswith(forbidden + "."):
            return forbidden
    return None


def _venv_python() -> str:
    """优先使用项目 .venv，避免 subprocess 继承不到当前 Python 环境。"""
    venv = REPO_ROOT / ".venv" / "bin" / "python"
    if venv.exists():
        return str(venv)
    return sys.executable


def test_import_boundary_dynamic_no_blacklist_loaded() -> None:
    """fp-import-chat-dynamic：动态 import 后不加载黑名单模块。"""
    env = {"PYTHONPATH": str(REPO_ROOT), **{k: v for k, v in __import__("os").environ.items() if k != "PYTHONPATH"}}
    proc = subprocess.run(
        [_venv_python(), "-c", _IMPORT_STATEMENT],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
        env=env,
        timeout=60,
        check=False,
    )
    assert proc.returncode == 0, (
        f"Dynamic import failed with rc={proc.returncode}\n"
        f"stdout: {proc.stdout}\nstderr: {proc.stderr}"
    )

    loaded = json.loads(proc.stdout.splitlines()[-1])
    violations = [(name, forbidden) for name in loaded if (forbidden := _is_forbidden(name))]

    assert not violations, (
        f"Scenario fp-import-chat-dynamic: "
        f"unexpected blacklisted modules loaded: {violations}"
    )
