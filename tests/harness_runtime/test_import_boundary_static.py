"""harness_runtime import 边界静态扫描（AST）。

覆盖 SPEC §11.2 与 BLOCKERS B5/B7：
- 禁止 import：`api.ingest_*` · `api.rag_*` · `api.index` chat 路径 · `public.documents` 等业务 ORM · `harness_probe`
- 允许：标准库 · pydantic · langgraph · langchain_core · `api.ops` Protocol/DTO（注入）
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
RUNTIME_ROOT = REPO_ROOT / "api" / "harness_runtime"

# Scenario IDs 对应 task 失败路径 F1/F2/F4
FORBIDDEN_IMPORT_ROOTS = (
    "api.ingest",
    "api.rag",
    "api.index",
    "public.documents",
    "harness_probe",
)


def _runtime_py_files() -> list[Path]:
    return sorted(RUNTIME_ROOT.rglob("*.py"))


def _import_module_names(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    names: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.append((node.lineno, alias.name))
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.append((node.lineno, node.module))
    return names


def _is_forbidden(name: str) -> str | None:
    for forbidden in FORBIDDEN_IMPORT_ROOTS:
        if name == forbidden or name.startswith(forbidden + "."):
            return forbidden
    return None


@pytest.mark.parametrize(
    "path",
    _runtime_py_files(),
    ids=lambda p: p.relative_to(REPO_ROOT).as_posix(),
)
def test_import_boundary_no_forbidden_modules(path: Path) -> None:
    """fp-import-rag-static / fp-import-ingest-static / fp-import-probe"""
    for lineno, name in _import_module_names(path):
        forbidden = _is_forbidden(name)
        assert forbidden is None, (
            f"Scenario fp-import-boundary-static: "
            f"{path.relative_to(REPO_ROOT)}:{lineno} imports forbidden module {name!r} "
            f"(matched {forbidden!r})"
        )
