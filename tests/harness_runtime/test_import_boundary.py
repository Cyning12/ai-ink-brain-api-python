"""harness_runtime import 边界静态扫描。"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "api" / "harness_runtime"

FORBIDDEN_IMPORT_ROOTS = (
    "api.ingest",
    "api.rag",
    "harness_probe",
    "harness_sdk",
)


def _runtime_py_files() -> list[Path]:
    return sorted(RUNTIME_ROOT.rglob("*.py"))


def _import_module_names(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append(node.module)
    return names


@pytest.mark.parametrize("path", _runtime_py_files(), ids=lambda p: p.relative_to(REPO_ROOT).as_posix())
def test_import_boundary_no_forbidden_modules(path: Path) -> None:
    for name in _import_module_names(path):
        for forbidden in FORBIDDEN_IMPORT_ROOTS:
            assert not (
                name == forbidden or name.startswith(forbidden + ".")
            ), f"{path}: forbidden import {name!r}"


def test_harness_runtime_package_importable() -> None:
    import api.harness_runtime  # noqa: F401
    import api.harness_runtime.adapters.probe_runner  # noqa: F401
    import api.harness_runtime.gate_sync.human_gate  # noqa: F401
    import api.harness_runtime.session_store.io  # noqa: F401
