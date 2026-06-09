from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ChunkType = Literal["module_doc", "function", "class", "method"]


@dataclass(frozen=True)
class ParsedChunk:
    name: str
    chunk_type: ChunkType
    signature: str
    docstring: str | None
    body: str
    file_path: str
    relative_path: str
    module: str
    start_line: int
    end_line: int


def _extract_module_path(relative_path: str) -> str:
    rel = relative_path.replace("\\", "/")
    if rel.endswith(".py"):
        rel = rel[: -len(".py")]
    parts = [p for p in rel.split("/") if p]
    return ".".join(parts)


def _node_start_line(node: ast.AST) -> int:
    lineno = getattr(node, "lineno", None)
    decos = getattr(node, "decorator_list", None)
    if isinstance(decos, list) and decos:
        deco_lines = [getattr(d, "lineno", lineno) for d in decos]
        deco_lines = [x for x in deco_lines if isinstance(x, int) and x > 0]
        if deco_lines:
            return min(deco_lines + ([lineno] if isinstance(lineno, int) else []))
    return int(lineno or 1)


def _node_end_line(node: ast.AST) -> int:
    end = getattr(node, "end_lineno", None)
    if isinstance(end, int) and end > 0:
        return end
    lineno = getattr(node, "lineno", None)
    return int(lineno or 1)


def _slice_lines(lines: list[str], start_line: int, end_line: int) -> str:
    s = max(1, int(start_line))
    e = max(s, int(end_line))
    return "".join(lines[s - 1 : e])


def _signature_from_lines(lines: list[str], start_line: int, header_line: int) -> str:
    # Signature 以“装饰器+def/async def 头部”作为可检索锚点
    return "".join(lines[start_line - 1 : header_line]).rstrip()


def parse_python_file(file_path: Path, *, repo_root: Path) -> list[ParsedChunk]:
    text = file_path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(file_path))
    rel = file_path.resolve().relative_to(repo_root.resolve()).as_posix()
    module = _extract_module_path(rel)
    lines = text.splitlines(keepends=True)

    out: list[ParsedChunk] = []

    # module docstring
    mod_doc = ast.get_docstring(tree)
    if mod_doc:
        # module docstring 的行号不好从 get_docstring 直接拿，这里用 AST 第一个 Expr 定位
        if tree.body and isinstance(tree.body[0], ast.Expr) and isinstance(tree.body[0].value, ast.Constant):
            n0 = tree.body[0]
            start = getattr(n0, "lineno", 1) or 1
            end = getattr(n0, "end_lineno", start) or start
        else:
            start, end = 1, 1
        out.append(
            ParsedChunk(
                name=module,
                chunk_type="module_doc",
                signature='"""module_doc"""',
                docstring=mod_doc,
                body=mod_doc,
                file_path=str(file_path),
                relative_path=rel,
                module=module,
                start_line=int(start),
                end_line=int(end),
            )
        )

    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            start = _node_start_line(node)
            end = _node_end_line(node)
            sig = _signature_from_lines(lines, start, getattr(node, "lineno", start) or start)
            body = _slice_lines(lines, start, end)
            doc = ast.get_docstring(node)
            out.append(
                ParsedChunk(
                    name=node.name,
                    chunk_type="function",
                    signature=sig,
                    docstring=doc,
                    body=body,
                    file_path=str(file_path),
                    relative_path=rel,
                    module=module,
                    start_line=start,
                    end_line=end,
                )
            )
        elif isinstance(node, ast.ClassDef):
            start = _node_start_line(node)
            end = _node_end_line(node)
            sig = _signature_from_lines(lines, start, getattr(node, "lineno", start) or start)
            body = _slice_lines(lines, start, end)
            doc = ast.get_docstring(node)
            out.append(
                ParsedChunk(
                    name=node.name,
                    chunk_type="class",
                    signature=sig,
                    docstring=doc,
                    body=body,
                    file_path=str(file_path),
                    relative_path=rel,
                    module=module,
                    start_line=start,
                    end_line=end,
                )
            )
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    cstart = _node_start_line(child)
                    cend = _node_end_line(child)
                    csig = _signature_from_lines(lines, cstart, getattr(child, "lineno", cstart) or cstart)
                    cbody = _slice_lines(lines, cstart, cend)
                    cdoc = ast.get_docstring(child)
                    out.append(
                        ParsedChunk(
                            name=f"{node.name}.{child.name}",
                            chunk_type="method",
                            signature=csig,
                            docstring=cdoc,
                            body=cbody,
                            file_path=str(file_path),
                            relative_path=rel,
                            module=module,
                            start_line=cstart,
                            end_line=cend,
                        )
                    )

    return out


def parse_project(repo_root: Path) -> list[ParsedChunk]:
    # P1：先实现最小扫描（后续按 SPEC-02 扩展 exclude patterns）
    repo = repo_root.resolve()
    chunks: list[ParsedChunk] = []
    for p in repo.rglob("*.py"):
        # 基本排除：虚拟环境与缓存、git
        rp = p.as_posix()
        if (
            "/.venv/" in rp
            or "/venv/" in rp
            or "/__pycache__/" in rp
            or "/.git/" in rp
            or "/node_modules/" in rp
            # 交付文档/验收脚本中的代码不应污染业务代码检索
            or "/docs/" in rp
        ):
            continue
        chunks.extend(parse_python_file(p, repo_root=repo))
    return chunks

