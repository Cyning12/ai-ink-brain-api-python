"""agently_lab 不得依赖 harness_runtime 生产图（ADR / 并行学习轨边界）。"""

from __future__ import annotations

import ast
from pathlib import Path

PKG_ROOT = Path(__file__).resolve().parents[2] / "api" / "agently_lab"
FORBIDDEN_PREFIXES = ("api.harness_runtime", "harness_runtime")


def _imports_in_file(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    found: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module)
    return found


def test_agently_lab_does_not_import_harness_runtime() -> None:
    violations: list[str] = []
    for py in sorted(PKG_ROOT.glob("*.py")):
        for mod in _imports_in_file(py):
            if any(mod == p or mod.startswith(f"{p}.") for p in FORBIDDEN_PREFIXES):
                violations.append(f"{py.name}: import {mod}")
    assert not violations, "import 边界违规:\n" + "\n".join(violations)
