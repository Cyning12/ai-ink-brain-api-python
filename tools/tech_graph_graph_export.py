from __future__ import annotations

"""
从 `docs/_tech_graph/*.ai.md` 导出 `graph.json`（P2-1 · graph_v2）。

退出码（stderr 含 FP 标记，便于 CI / PR 说明）：
- 0：写入成功或 `--check` 与已提交文件一致
- 2：FP-1（解析失败 / 输入目录不存在）或 FP-4（写入等 OSError，环境类）
- 3：FP-2 — 已提交 `graph.json` 缺失或 JSON 根非 object / 缺 `generated_at`
- 4：FP-2 — 再生成与已提交对象语义不一致（stderr 附差异摘要）

与 `tools/tech_graph_contract_check.py` **并行互补**，禁止合并逻辑。
v1 扁平导出（`raw_edges_to_graph_dict`）仅保留供解析单测；CI 主路径为 graph_v2。
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tech_graph_graph_v2_schema import SCHEMA_VERSION_V2
DEFAULT_INPUT = REPO_ROOT / "docs" / "_tech_graph"
DEFAULT_OUTPUT = REPO_ROOT / "docs" / "_tech_graph" / "graph.json"
# 与 docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/protocol_version.yaml · graph_v2_freeze_id 对齐
FREEZE_ID = "TECH_GRAPH_S2_FREEZE_20260517_V2_1"
SCHEMA_VERSION = SCHEMA_VERSION_V2

MERMAID_FENCE = re.compile(r"```\s*mermaid\s*\n([\s\S]*?)```", re.IGNORECASE)


def _repo_rel_posix(path: Path) -> str:
    """用于 FP-1 日志：优先相对本仓根，否则退回绝对路径（pytest tmp 等）。"""
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


class TechGraphParseError(ValueError):
    """FP-1：.ai.md 不符合解析器子集。"""

    def __init__(self, *, path: Path, line_no: int | None, message: str) -> None:
        self.path = path
        self.line_no = line_no
        self.message = message
        super().__init__(message)


@dataclass(frozen=True)
class RawEdge:
    source: str
    target: str
    label: str
    source_file: str


def _stderr(msg: str) -> None:
    print(msg, file=sys.stderr)


def _utc_now_iso_z() -> str:
    return (
        datetime.now(timezone.utc)
        .replace(microsecond=0)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _skip_node_shape(s: str) -> str:
    """消费 Mermaid 节点在 id 之后的形状后缀（如 [[..]]、[..]、{..}）。"""
    t = s
    while t:
        if t.startswith("[["):
            # 同时处理标签内单层 `[...]`（如 `[err]`）与外层 `[[...]]`，避免误把 `] ]` 当成 `]]`
            i = 2
            double_depth = 1
            single_depth = 0
            while i < len(t):
                if t.startswith("[[", i):
                    double_depth += 1
                    i += 2
                    continue
                if t.startswith("]]", i) and single_depth == 0:
                    double_depth -= 1
                    i += 2
                    if double_depth == 0:
                        t = t[i:]
                        break
                    continue
                ch = t[i]
                if ch == "[" and not t.startswith("[[", i):
                    single_depth += 1
                    i += 1
                    continue
                if ch == "]" and single_depth > 0:
                    single_depth -= 1
                    i += 1
                    continue
                i += 1
            else:
                raise ValueError("unclosed [[")
            continue
        if t.startswith("["):
            depth = 0
            i = 0
            while i < len(t):
                ch = t[i]
                if ch == "[" and (i == 0 or t[i - 1] != "\\"):
                    depth += 1
                elif ch == "]" and (i == 0 or t[i - 1] != "\\"):
                    depth -= 1
                    if depth == 0:
                        t = t[i + 1 :]
                        break
                i += 1
            else:
                raise ValueError("unclosed [")
            continue
        if t.startswith("{"):
            depth = 0
            i = 0
            while i < len(t):
                ch = t[i]
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        t = t[i + 1 :]
                        break
                i += 1
            else:
                raise ValueError("unclosed {")
            continue
        if t.startswith("("):
            depth = 0
            i = 0
            while i < len(t):
                ch = t[i]
                if ch == "(":
                    depth += 1
                elif ch == ")":
                    depth -= 1
                    if depth == 0:
                        t = t[i + 1 :]
                        break
                i += 1
            else:
                raise ValueError("unclosed (")
            continue
        break
    return t


def _classify_label(label: str) -> tuple[str, bool]:
    """返回 (edge_type, sync)。SPEC：~> 异步；::xxx → 元关系名；?> condition；其余 depends_on。"""
    t = label.strip()
    if t.startswith("::") and len(t) > 2:
        return (t[2:].strip() or "meta", True)
    if "~>" in t:
        return ("async_calls", False)
    if "?>" in t or t == "?>":
        return ("condition", True)
    return ("depends_on", True)


def _parse_labeled_edge_line(*, line: str, line_no: int, path: Path) -> list[RawEdge]:
    s0 = line.strip()
    if not s0 or s0.startswith("%%") or s0.startswith("//"):
        return []
    if s0.startswith(("classDef ", "class ", "linkStyle ", "direction ", "subgraph ", "end")):
        return []
    if s0.startswith(("flowchart ", "graph ")):
        return []

    edges: list[RawEdge] = []
    s = s0
    rel = _repo_rel_posix(path)
    last_to: str | None = None

    while True:
        s = s.lstrip()
        if not s or s.startswith("//") or s.startswith("%%"):
            break

        m_edge = re.match(r'^--"([^"]*)"\s*-->\s*', s)
        if m_edge:
            if last_to is None:
                raise TechGraphParseError(
                    path=path,
                    line_no=line_no,
                    message=f"链式边缺少左侧起点：{rel}:{line_no}: {s0!r}",
                )
            frm = last_to
            lab = m_edge.group(1)
            s = s[m_edge.end() :]
        else:
            m_from = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)", s)
            if not m_from:
                break
            frm = m_from.group(1)
            s = s[m_from.end() :]
            try:
                s = _skip_node_shape(s)
            except ValueError as exc:
                raise TechGraphParseError(
                    path=path,
                    line_no=line_no,
                    message=f"源节点形状未闭合：{rel}:{line_no}: {exc}",
                ) from exc
            s = s.lstrip()
            m_edge = re.match(r'^--"([^"]*)"\s*-->\s*', s)
            if not m_edge:
                break
            lab = m_edge.group(1)
            s = s[m_edge.end() :]

        m_to = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)", s)
        if not m_to:
            raise TechGraphParseError(
                path=path,
                line_no=line_no,
                message=f"缺少箭头目标节点：{rel}:{line_no}: {s0!r}",
            )
        to = m_to.group(1)
        s = s[m_to.end() :]
        try:
            s = _skip_node_shape(s)
        except ValueError as exc:
            raise TechGraphParseError(
                path=path,
                line_no=line_no,
                message=f"目标节点形状未闭合：{rel}:{line_no}: {exc}",
            ) from exc
        edges.append(RawEdge(source=frm, target=to, label=lab, source_file=rel))
        last_to = to

    if not edges:
        m_plain = re.match(
            r"^([A-Za-z_][A-Za-z0-9_]*)\s*-->\s*([A-Za-z_][A-Za-z0-9_]*)",
            s0,
        )
        if m_plain:
            edges.append(
                RawEdge(
                    source=m_plain.group(1),
                    target=m_plain.group(2),
                    label="-->",
                    source_file=_repo_rel_posix(path),
                )
            )
            return edges

    if not edges:
        if "--" in s0 and not s0.startswith("//"):
            raise TechGraphParseError(
                path=path,
                line_no=line_no,
                message=f"无法解析的 flowchart 边（子集不支持）：{rel}:{line_no}: {s0!r}",
            )
        return []

    s = s.lstrip()
    if s and not s.startswith("//") and not s.startswith("%%"):
        raise TechGraphParseError(
            path=path,
            line_no=line_no,
            message=f"行尾存在未消费的片段：{rel}:{line_no}: 余下={s!r} 整行={s0!r}",
        )
    return edges


def _parse_class_diagram_line(*, line: str, path: Path, line_no: int) -> list[RawEdge]:
    s = line.strip()
    if not s or s.startswith("%%") or s.startswith("//") or s.startswith("class "):
        return []
    m = re.match(
        r"^([A-Za-z_][A-Za-z0-9_]*)\s*-->\s*([A-Za-z_][A-Za-z0-9_]*)(?:\s*:\s*([^\s]+))?\s*$",
        s,
    )
    if not m:
        if "-->" in s:
            raise TechGraphParseError(
                path=path,
                line_no=line_no,
                message=(
                    f"classDiagram 边无法解析：{_repo_rel_posix(path)}:"
                    f"{line_no}: {s!r}"
                ),
            )
        return []
    rel = _repo_rel_posix(path)
    return [
        RawEdge(
            source=m.group(1),
            target=m.group(2),
            label="classDiagram",
            source_file=rel,
        )
    ]


def _iter_ai_md_files(input_root: Path) -> list[Path]:
    out: list[Path] = []
    for p in sorted(input_root.glob("*.ai.md")):
        if p.name.startswith("99_"):
            continue
        out.append(p)
    return out


def collect_raw_edges(input_root: Path) -> list[RawEdge]:
    """遍历 input_root 下 *.ai.md（跳过 99_*），解析 mermaid flowchart / classDiagram 边。"""
    all_edges: list[RawEdge] = []
    for path in _iter_ai_md_files(input_root):
        text = path.read_text(encoding="utf-8")
        for m in MERMAID_FENCE.finditer(text):
            body = m.group(1)
            lines = body.splitlines()
            mode: str | None = None
            base_line = 1
            # 粗略行号：fence 内在文件中的行需加上文件偏移；此处用块内行号 + 近似
            fence_start = text[: m.start()].count("\n") + 1
            for i, line in enumerate(lines, start=1):
                stripped = line.strip()
                if not stripped or stripped.startswith("%%"):
                    continue
                if re.match(r"^(flowchart|graph)\b", stripped):
                    mode = "flowchart"
                    continue
                if stripped.startswith("classDiagram"):
                    mode = "classDiagram"
                    continue
                if mode == "flowchart":
                    try:
                        all_edges.extend(
                            _parse_labeled_edge_line(
                                line=line, line_no=fence_start + i, path=path
                            )
                        )
                    except TechGraphParseError:
                        raise
                elif mode == "classDiagram":
                    all_edges.extend(
                        _parse_class_diagram_line(line=line, path=path, line_no=fence_start + i)
                    )
            if mode is None and body.strip():
                raise TechGraphParseError(
                    path=path,
                    line_no=fence_start,
                    message=f"mermaid 块缺少 flowchart/graph 或 classDiagram 头：{path.name}",
                )
    return all_edges


def raw_edges_to_graph_dict(
    raw: Iterable[RawEdge],
    *,
    generated_at: str,
    freeze_id: str = FREEZE_ID,
) -> dict[str, Any]:
    nodes: set[str] = set()
    edge_objs: list[dict[str, Any]] = []
    for e in raw:
        nodes.add(e.source)
        nodes.add(e.target)
        typ, sync = _classify_label(e.label)
        if e.label == "classDiagram":
            typ = "has_metadata"
            sync = True
        obj: dict[str, Any] = {
            "from": e.source,
            "to": e.target,
            "type": typ,
            "sync": sync,
        }
        edge_objs.append(obj)

    sorted_nodes = sorted(nodes)
    edge_objs.sort(key=lambda x: (x["from"], x["to"], x["type"], x["sync"]))
    return {
        "schema_version": SCHEMA_VERSION,
        "freeze_id": freeze_id,
        "generated_at": generated_at,
        "nodes": sorted_nodes,
        "edges": edge_objs,
    }


def build_graph_payload(
    input_root: Path,
    *,
    generated_at: str | None = None,
    freeze_id: str = FREEZE_ID,
) -> dict[str, Any]:
    """自 *.ai.md 构建 P2-0 graph_v2 载荷（与参考图构建器一致）。"""
    from tools.tech_graph_graph_v2_reference import build_reference_graph_v2

    if generated_at is None:
        generated_at = _utc_now_iso_z()
    return build_reference_graph_v2(
        input_root, generated_at=generated_at, freeze_id=freeze_id
    )


def dumps_canonical(obj: Any) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def _node_ids_from_graph(graph: dict[str, Any]) -> set[str]:
    nodes = graph.get("nodes") or []
    if nodes and isinstance(nodes[0], str):
        return set(nodes)
    return {n["id"] for n in nodes if isinstance(n, dict) and n.get("id")}


def _graph_semantic_diff(*, committed: dict[str, Any], fresh: dict[str, Any]) -> str | None:
    """FP-2：返回人类可读差异摘要；无差异返回 None。"""
    problems: list[str] = []
    for key in ("schema_version", "freeze_id", "nodes", "edges"):
        if committed.get(key) != fresh.get(key):
            problems.append(f"field_mismatch:{key}")
    if committed.get("nodes") != fresh.get("nodes"):
        a = _node_ids_from_graph(committed)
        b = _node_ids_from_graph(fresh)
        problems.append(f"nodes_added={sorted(b - a)[:40]}")
        problems.append(f"nodes_removed={sorted(a - b)[:40]}")
    if committed.get("edges") != fresh.get("edges"):
        ce = committed.get("edges") or []
        fe = fresh.get("edges") or []
        problems.append(f"edges_count_committed={len(ce)} fresh={len(fe)}")
        # 小集合时打印前几条
        if len(ce) < 400:
            import difflib

            diff = difflib.unified_diff(
                json.dumps(ce, ensure_ascii=False, indent=2).splitlines(),
                json.dumps(fe, ensure_ascii=False, indent=2).splitlines(),
                lineterm="",
                n=2,
            )
            snippet = "\n".join(list(diff)[:40])
            if snippet:
                problems.append("edges_unified_diff_head:\n" + snippet)
    if not problems:
        return None
    return "graph.json drift (--check / FP-2):\n- " + "\n- ".join(problems)


def write_graph_json(output_path: Path, payload: dict[str, Any]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(dumps_canonical(payload), encoding="utf-8")


def run_check(*, input_root: Path, output_path: Path) -> int:
    """FP-2：与已提交 graph.json 语义对齐（复用 committed.generated_at 再比较整对象）。"""
    if not output_path.is_file():
        _stderr(f"FP-2: graph.json 缺失：{output_path}（请先在本仓根运行导出脚本生成并提交）")
        return 3
    try:
        committed = json.loads(output_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _stderr(f"FP-2: 已提交 graph.json JSON 解析失败：{output_path}: {exc}")
        return 3
    if not isinstance(committed, dict):
        _stderr("FP-2: graph.json 根类型必须是 object")
        return 3
    gen = committed.get("generated_at")
    if not isinstance(gen, str):
        _stderr("FP-2: committed.generated_at 缺失或类型错误（无法做稳定比对）")
        return 3
    try:
        fresh = build_graph_payload(input_root, generated_at=gen)
    except TechGraphParseError as exc:
        _stderr(f"FP-1: Mermaid 解析失败：{exc.path}:{exc.line_no}: {exc.message}")
        return 2
    if fresh != committed:
        msg = _graph_semantic_diff(committed=committed, fresh=fresh) or "unknown_mismatch"
        _stderr(msg)
        return 4
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="从 docs/_tech_graph/*.ai.md 导出 graph.json（graph_v2）。"
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="输入根目录（默认 docs/_tech_graph，相对本仓根）",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="输出 graph.json 路径（默认 docs/_tech_graph/graph.json）",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="再生成并与已提交 graph.json 比对（FP-2；成功退出码 0）",
    )
    args = parser.parse_args(argv)

    input_root = (REPO_ROOT / args.input).resolve() if not args.input.is_absolute() else args.input
    output_path = (REPO_ROOT / args.output).resolve() if not args.output.is_absolute() else args.output

    if not input_root.is_dir():
        _stderr(f"FP-1: 输入目录不存在：{input_root}")
        return 2

    try:
        if args.check:
            return run_check(input_root=input_root, output_path=output_path)
        payload = build_graph_payload(input_root)
        write_graph_json(output_path, payload)
    except TechGraphParseError as exc:
        _stderr(f"FP-1: Mermaid 解析失败：{exc.path}:{exc.line_no}: {exc.message}")
        return 2
    except OSError as exc:
        _stderr(f"FP-4: 写入失败（环境/权限）：{exc}")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
