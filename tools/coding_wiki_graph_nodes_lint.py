from __future__ import annotations

"""Coding Wiki syntheses · graph_nodes frontmatter lint（T4 运营化）。

扫描 `docs/coding_wiki/syntheses/*.md` frontmatter：
- 缺省 `graph_nodes` 键 → fail（syntheses 强制存在键）
- `graph_nodes: []` → pass
- 非空：逐 id 调 graph_v2 neighbors；`relation` 须在 Bridge SPEC §3.1 枚举内

退出码：0 全绿 · 1 有违规
"""

import argparse
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
DEFAULT_SYNTH_DIR = _REPO_ROOT / "docs" / "coding_wiki" / "syntheses"

# Bridge SPEC §3.1 · YAML 无 :: 前缀
VALID_RELATIONS = frozenset(
    {
        "yields",
        "triggers",
        "gates",
        "branches",
        "merges",
        "signoff",
        "archives",
        "documents",
        "evidence",
    }
)

_FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---", re.DOTALL)
_GRAPH_NODES_KEY_RE = re.compile(r"^graph_nodes\s*:", re.MULTILINE)
_GRAPH_NODES_EMPTY_RE = re.compile(r"^graph_nodes\s*:\s*\[\]\s*$", re.MULTILINE)
_ID_LINE_RE = re.compile(r'^\s*-\s+id:\s*"?([^"\n]+)"?\s*$')
_RELATION_LINE_RE = re.compile(r'^\s+relation:\s*"?([^"\n]+)"?\s*$')


@dataclass
class GraphNodeEntry:
    id: str
    relation: str | None = None


@dataclass
class LintFinding:
    path: Path
    level: str  # error | warn
    message: str


@dataclass
class LintReport:
    findings: list[LintFinding] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not any(f.level == "error" for f in self.findings)

    def add(self, path: Path, level: str, message: str) -> None:
        self.findings.append(LintFinding(path=path, level=level, message=message))


def _split_frontmatter(text: str) -> tuple[str | None, str]:
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    return m.group(1), text[m.end() :]


def _parse_graph_nodes(frontmatter: str) -> tuple[bool, list[GraphNodeEntry]]:
    """返回 (has_key, entries)。"""
    if not _GRAPH_NODES_KEY_RE.search(frontmatter):
        return False, []
    if _GRAPH_NODES_EMPTY_RE.search(frontmatter):
        return True, []

    entries: list[GraphNodeEntry] = []
    current: GraphNodeEntry | None = None
    in_block = False

    for line in frontmatter.splitlines():
        if re.match(r"^graph_nodes\s*:", line):
            in_block = True
            continue
        if not in_block:
            continue
        if line and not line.startswith((" ", "\t")):
            break

        m_id = _ID_LINE_RE.match(line)
        if m_id:
            if current is not None:
                entries.append(current)
            current = GraphNodeEntry(id=m_id.group(1).strip())
            continue
        m_rel = _RELATION_LINE_RE.match(line)
        if m_rel and current is not None:
            current.relation = m_rel.group(1).strip()

    if current is not None:
        entries.append(current)
    return True, entries


def _validate_node_id(store, node_id: str) -> str | None:
    from tools.tech_graph_graph_query import GraphQueryError, query_neighbors

    try:
        query_neighbors(store, node_id)
    except GraphQueryError as exc:
        return str(exc)
    return None


def lint_markdown_file(
    path: Path,
    *,
    store,
    require_key: bool = True,
) -> list[LintFinding]:
    findings: list[LintFinding] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [LintFinding(path=path, level="error", message=f"无法读取：{exc}")]

    frontmatter, _ = _split_frontmatter(text)
    if frontmatter is None:
        return [LintFinding(path=path, level="error", message="缺少 YAML frontmatter")]

    has_key, entries = _parse_graph_nodes(frontmatter)
    if require_key and not has_key:
        findings.append(
            LintFinding(path=path, level="error", message="frontmatter 缺少 graph_nodes 键")
        )
        return findings

    if not has_key:
        return findings

    if not entries:
        return findings

    for entry in entries:
        if not entry.id:
            findings.append(
                LintFinding(path=path, level="error", message="graph_nodes 项缺少 id")
            )
            continue
        err = _validate_node_id(store, entry.id)
        if err:
            findings.append(
                LintFinding(
                    path=path,
                    level="error",
                    message=f"graph_nodes.id={entry.id!r} 无效：{err}",
                )
            )
        if entry.relation is None:
            findings.append(
                LintFinding(
                    path=path,
                    level="error",
                    message=f"graph_nodes.id={entry.id!r} 缺少 relation",
                )
            )
        elif entry.relation not in VALID_RELATIONS:
            findings.append(
                LintFinding(
                    path=path,
                    level="error",
                    message=(
                        f"graph_nodes.id={entry.id!r} relation={entry.relation!r} "
                        f"不在 Bridge SPEC §3.1 枚举内"
                    ),
                )
            )
    return findings


def lint_directory(
    root: Path,
    *,
    require_key: bool = True,
    graph_path: Path | None = None,
) -> LintReport:
    md_files = sorted(root.glob("*.md"))
    if not md_files:
        report = LintReport()
        report.add(root, "error", "目录下无 *.md")
        return report
    return lint_paths(
        md_files,
        require_key=require_key,
        graph_path=graph_path,
    )


def lint_paths(
    paths: list[Path],
    *,
    require_key: bool = True,
    graph_path: Path | None = None,
) -> LintReport:
    from tools.tech_graph_graph_query import DEFAULT_GRAPH, GraphQueryError, load_graph_v2

    report = LintReport()
    gpath = graph_path or DEFAULT_GRAPH
    try:
        store = load_graph_v2(gpath)
    except GraphQueryError as exc:
        report.add(gpath, "error", str(exc))
        return report

    for path in paths:
        for finding in lint_markdown_file(path, store=store, require_key=require_key):
            report.findings.append(finding)
    return report


def _print_report(report: LintReport) -> None:
    if not report.findings:
        print("coding_wiki_graph_nodes_lint: OK")
        return
    for f in report.findings:
        try:
            rel = f.path.relative_to(_REPO_ROOT)
        except ValueError:
            rel = f.path
        print(f"{f.level.upper()}: {rel}: {f.message}", file=sys.stderr)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Lint Coding Wiki syntheses graph_nodes frontmatter（T4）"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="待检 Markdown（默认 docs/coding_wiki/syntheses/ 下全部 *.md）",
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=DEFAULT_SYNTH_DIR,
        help="syntheses 目录（未指定 paths 时扫描此目录）",
    )
    parser.add_argument(
        "--no-require-key",
        action="store_true",
        help="缺 graph_nodes 键时不 fail（默认 syntheses 强制存在键）",
    )
    parser.add_argument(
        "--graph",
        type=Path,
        default=None,
        help="graph.json 路径（默认 docs/_tech_graph/graph.json）",
    )
    args = parser.parse_args(argv)

    require_key = not args.no_require_key
    if args.paths:
        paths = [p if p.is_absolute() else (_REPO_ROOT / p).resolve() for p in args.paths]
        report = lint_paths(
            paths,
            require_key=require_key,
            graph_path=args.graph.resolve() if args.graph else None,
        )
    else:
        root = args.root if args.root.is_absolute() else (_REPO_ROOT / args.root).resolve()
        gpath = args.graph.resolve() if args.graph else None
        report = lint_directory(root, require_key=require_key, graph_path=gpath)

    _print_report(report)
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
