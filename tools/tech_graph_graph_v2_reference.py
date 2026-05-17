from __future__ import annotations

"""
自 docs/_tech_graph/*.ai.md 构建 graph_v2 参考载荷（P2-0）。

供等价检查对照；导出器 v2 升版（P2-1）应与此参考语义对齐。
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from tools.tech_graph_graph_export import (
    REPO_ROOT,
    TechGraphParseError,
    _classify_label,
    _iter_ai_md_files,
    _parse_labeled_edge_line,
    _repo_rel_posix,
    _skip_node_shape,
)
from tools.tech_graph_graph_v2_schema import SCHEMA_VERSION_V2

ANCHOR_LINE = re.compile(
    r"^\s*//\s*→\s*(?P<path>[^\s#]+?)(?:#L(?P<line>\d+)|::(?P<symbol>[^\s]+))?\s*$"
)
PROTOCOL_MARKS = frozenset(
    {
        "->",
        "~>",
        "?>",
        "=>",
        "[ok]",
        "[err]",
        "[timeout]",
        "classDiagram",
        "-->",
    }
)


@dataclass
class AnchorRef:
    path: str
    symbol: str = ""
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"path": self.path, "symbol": self.symbol}
        if self.line is not None:
            out["line"] = self.line
        return out


@dataclass
class RefEdge:
    source: str
    target: str
    raw_label: str
    source_file: str
    source_line: int
    anchors: list[AnchorRef] = field(default_factory=list)
    source_label: str = ""
    target_label: str = ""


def _parse_anchor_comment(line: str) -> AnchorRef | None:
    m = ANCHOR_LINE.match(line.strip())
    if not m:
        return None
    path = m.group("path")
    line_no = int(m.group("line")) if m.group("line") else None
    sym = m.group("symbol") or ""
    if line_no is not None and not sym:
        sym = f"#L{line_no}"
    return AnchorRef(path=path, symbol=sym, line=line_no)


def _extract_node_label(fragment: str) -> str:
    """从 id 后的形状片段提取 label；失败则返回空串。"""
    t = fragment.lstrip()
    if t.startswith("[["):
        end = t.find("]]")
        if end > 2:
            return t[2:end].strip()
    if t.startswith("{"):
        end = t.find("}")
        if end > 1:
            return t[1:end].strip()
    if t.startswith("["):
        depth = 0
        for i, ch in enumerate(t):
            if ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    inner = t[1:i]
                    return inner.strip()
    if t.startswith(">"):
        end = t.find("]")
        if end > 1:
            return t[1:end].strip()
    return ""


def _split_mark_label(raw: str) -> tuple[str, str]:
    t = raw.strip()
    if t.startswith("::"):
        return (t, "")
    if t in PROTOCOL_MARKS or t.startswith("[") and t.endswith("]"):
        return (t, "")
    # 语义边（HTTP、加载等）：mark 用默认协议，label 保留全文
    return ("->", t)


def _parse_edge_line_with_labels(
    *, line: str, line_no: int, path: Path
) -> list[RefEdge]:
    """扩展解析：附带节点 label 与紧随其后的锚点注释。"""
    s0 = line.strip()
    if not s0 or s0.startswith("%%") or s0.startswith("//"):
        return []
    if s0.startswith(("classDef ", "class ", "linkStyle ", "direction ", "subgraph ", "end")):
        return []
    if s0.startswith(("flowchart ", "graph ")):
        return []

    rel = _repo_rel_posix(path)
    edges: list[RefEdge] = []
    s = s0
    last_to: str | None = None
    last_to_label = ""

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
            frm_label = last_to_label
            lab = m_edge.group(1)
            s = s[m_edge.end() :]
        else:
            m_from = re.match(r"^([A-Za-z_][A-Za-z0-9_]*)", s)
            if not m_from:
                break
            frm = m_from.group(1)
            rest = s[m_from.end() :]
            frm_label = _extract_node_label(rest)
            try:
                s = _skip_node_shape(rest)
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
        rest_to = s[m_to.end() :]
        to_label = _extract_node_label(rest_to)
        try:
            s = _skip_node_shape(rest_to)
        except ValueError as exc:
            raise TechGraphParseError(
                path=path,
                line_no=line_no,
                message=f"目标节点形状未闭合：{rel}:{line_no}: {exc}",
            ) from exc

        edges.append(
            RefEdge(
                source=frm,
                target=to,
                raw_label=lab,
                source_file=rel,
                source_line=line_no,
                source_label=frm_label,
                target_label=to_label,
            )
        )
        last_to = to
        last_to_label = to_label

    if not edges:
        # 回退到 v1 解析器（裸边等）
        for raw in _parse_labeled_edge_line(line=line, line_no=line_no, path=path):
            edges.append(
                RefEdge(
                    source=raw.source,
                    target=raw.target,
                    raw_label=raw.label,
                    source_file=raw.source_file,
                    source_line=line_no,
                )
            )
    return edges


def collect_reference_edges(input_root: Path) -> list[RefEdge]:
    """遍历 *.ai.md，收集带锚点的参考边。"""
    from tools.tech_graph_graph_export import MERMAID_FENCE

    all_edges: list[RefEdge] = []
    for path in _iter_ai_md_files(input_root):
        text = path.read_text(encoding="utf-8")
        for m in MERMAID_FENCE.finditer(text):
            body = m.group(1)
            lines = body.splitlines()
            mode: str | None = None
            fence_start = text[: m.start()].count("\n") + 1
            pending_anchors: list[AnchorRef] = []
            last_edge_in_block: RefEdge | None = None

            for i, line in enumerate(lines, start=1):
                stripped = line.strip()
                if not stripped:
                    continue
                if re.match(r"^(flowchart|graph)\b", stripped):
                    mode = "flowchart"
                    pending_anchors = []
                    last_edge_in_block = None
                    continue
                if stripped.startswith("classDiagram"):
                    mode = "classDiagram"
                    pending_anchors = []
                    last_edge_in_block = None
                    continue

                anc = _parse_anchor_comment(line)
                if anc is not None:
                    if last_edge_in_block is not None:
                        last_edge_in_block.anchors.append(anc)
                    else:
                        pending_anchors.append(anc)
                    continue

                if mode == "flowchart":
                    line_no = fence_start + i
                    parsed = _parse_edge_line_with_labels(line=line, line_no=line_no, path=path)
                    if parsed:
                        for e in parsed:
                            e.anchors = list(pending_anchors)
                            pending_anchors = []
                            last_edge_in_block = e
                        all_edges.extend(parsed)
                elif mode == "classDiagram":
                    from tools.tech_graph_graph_export import _parse_class_diagram_line

                    for raw in _parse_class_diagram_line(line=line, path=path, line_no=fence_start + i):
                        all_edges.append(
                            RefEdge(
                                source=raw.source,
                                target=raw.target,
                                raw_label=raw.label,
                                source_file=raw.source_file,
                                source_line=fence_start + i,
                                anchors=list(pending_anchors),
                            )
                        )
                    pending_anchors = []
    return all_edges


def reference_edges_to_graph_v2(
    edges: list[RefEdge],
    *,
    generated_at: str,
    freeze_id: str,
) -> dict[str, Any]:
    """将参考边物化为 P2-0 graph_v2 字典。"""
    node_labels: dict[str, str] = {}
    edge_objs: list[dict[str, Any]] = []

    for e in edges:
        for nid, lab in ((e.source, e.source_label), (e.target, e.target_label)):
            if nid not in node_labels:
                node_labels[nid] = lab or nid
            elif lab and not node_labels[nid]:
                node_labels[nid] = lab

        mark, sem_label = _split_mark_label(e.raw_label)
        typ, sync = _classify_label(mark if mark != "->" or not sem_label else e.raw_label)
        if e.raw_label == "classDiagram":
            typ = "has_metadata"
            sync = True
            mark = "classDiagram"
            sem_label = ""

        edge_objs.append(
            {
                "from": e.source,
                "to": e.target,
                "mark": mark,
                "type": typ,
                "sync": sync,
                "label": sem_label,
                "anchors": [a.to_dict() for a in e.anchors],
            }
        )

    nodes = [{"id": nid, "label": node_labels[nid]} for nid in sorted(node_labels)]
    edge_objs.sort(
        key=lambda x: (x["from"], x["to"], x["mark"], x["type"], x["sync"], x["label"])
    )
    return {
        "schema_version": SCHEMA_VERSION_V2,
        "freeze_id": freeze_id,
        "generated_at": generated_at,
        "nodes": nodes,
        "edges": edge_objs,
    }


def build_reference_graph_v2(
    input_root: Path,
    *,
    generated_at: str,
    freeze_id: str = "TECH_GRAPH_S2_FREEZE_20260517_V2_1",
) -> dict[str, Any]:
    if not input_root.is_dir():
        raise FileNotFoundError(input_root)
    edges = collect_reference_edges(input_root)
    return reference_edges_to_graph_v2(edges, generated_at=generated_at, freeze_id=freeze_id)
