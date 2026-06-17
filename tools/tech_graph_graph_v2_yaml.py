from __future__ import annotations

"""
自 docs/_tech_graph/*.graph.yaml 构建 graph_v2 载荷（P1）。

CI 主路径默认使用本模块；*.ai.md 解析保留在 tools/tech_graph_graph_v2_reference.py
供迁移对照与单测。
"""

import sys
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tech_graph_graph_export import (
    TechGraphParseError,
    _classify_label,
    _repo_rel_posix,
    _resolve_export_repo_root,
)
from tools.tech_graph_graph_v2_schema import SCHEMA_VERSION_V2


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        line_no = mark.line + 1 if mark is not None else None
        raise TechGraphParseError(
            path=path,
            line_no=line_no,
            message=f"YAML 解析失败: {exc}",
        ) from exc
    if not isinstance(data, dict):
        raise TechGraphParseError(
            path=path,
            line_no=None,
            message="YAML 根须为 mapping",
        )
    return data


def _all_graph_ids(input_root: Path) -> list[str]:
    return sorted(p.name[: -len(".graph.yaml")] for p in input_root.glob("*.graph.yaml"))


def _normalize_anchors(anchors: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """YAML anchors 只保证 path；补全 symbol / line 与 graph_v2 schema 对齐。"""
    out: list[dict[str, Any]] = []
    for a in anchors:
        path = a.get("path", "")
        line = a.get("line")
        symbol = a.get("symbol", "")
        if line is not None:
            symbol = f"#L{line}"
        obj: dict[str, Any] = {"path": path, "symbol": symbol}
        if line is not None:
            obj["line"] = line
        out.append(obj)
    return out


def _yaml_edge_to_graph_v2(yaml_edge: dict[str, Any]) -> tuple[str, str, bool, str]:
    """将一条 YAML edge 映射为 graph_v2 的 (mark, type, sync, label)。

    YAML 已把 mark / label / type 语义分开：mark 字段即 Mermaid 箭头；
    label 字段为语义标签；type 字段可显式覆盖推断类型。
    """
    mark = yaml_edge.get("mark", "")
    label = yaml_edge.get("label", "")
    explicit_type = yaml_edge.get("type", "")

    if mark:
        if mark == "classDiagram":
            base_mark, base_label = "classDiagram", ""
            inferred_type = "has_metadata"
        elif mark == "~>":
            base_mark, base_label = "~>", ""
            inferred_type = "async_calls"
        elif mark == "?>":
            base_mark, base_label = "?>", ""
            inferred_type = "condition"
        elif mark.startswith("::"):
            base_mark, base_label = mark, ""
            inferred_type = mark[2:] or "meta"
        elif mark.startswith("[") and mark.endswith("]"):
            base_mark, base_label = mark, ""
            inferred_type = "depends_on"
        elif mark == "->":
            base_mark, base_label = "->", label
            inferred_type, _ = _classify_label(label) if label else ("depends_on", True)
        else:
            # 未知 mark：保留 mark，按语义 label 推断类型
            base_mark, base_label = mark, label
            inferred_type, _ = _classify_label(label) if label else ("depends_on", True)
    else:
        # 无显式 mark 时默认箭头，label 作为语义标签
        base_mark = "->"
        base_label = label
        if not label:
            inferred_type = "depends_on"
        elif label == "classDiagram":
            base_mark, base_label = "classDiagram", ""
            inferred_type = "has_metadata"
        elif label == "?>":
            base_mark, base_label = "?>", ""
            inferred_type = "condition"
        elif label.startswith("::"):
            base_mark, base_label = label, ""
            inferred_type = label[2:] or "meta"
        else:
            inferred_type, _ = _classify_label(label)

    final_type = explicit_type if explicit_type else inferred_type
    sync = final_type != "async_calls"
    return base_mark, final_type, sync, base_label


def build_yaml_graph_v2(
    input_root: Path,
    *,
    generated_at: str,
    freeze_id: str,
) -> dict[str, Any]:
    """遍历 input_root 下 *.graph.yaml，合并为 graph_v2 载荷。"""
    if not input_root.is_dir():
        raise FileNotFoundError(input_root)

    export_root = _resolve_export_repo_root(input_root)
    graph_ids = _all_graph_ids(input_root)

    nodes: list[dict[str, Any]] = []
    edges: list[dict[str, Any]] = []
    graphs: list[dict[str, Any]] = []

    for graph_id in graph_ids:
        yaml_path = input_root / f"{graph_id}.graph.yaml"
        ai_path = input_root / f"{graph_id}.ai.md"
        data = _load_yaml(yaml_path)
        title = data.get("title", graph_id)

        graphs.append(
            {
                "id": graph_id,
                "title": title,
                "source_yaml_path": _repo_rel_posix(yaml_path, base=export_root),
                "source_ai_path": _repo_rel_posix(ai_path, base=export_root),
            }
        )

        for n in data.get("nodes", []):
            nodes.append(
                {
                    "id": n["id"],
                    "label": n.get("label", n["id"]),
                    "graph_id": graph_id,
                }
            )

        for e in data.get("edges", []):
            mark, typ, sync, label = _yaml_edge_to_graph_v2(e)
            edges.append(
                {
                    "from": e["from"],
                    "to": e["to"],
                    "mark": mark,
                    "type": typ,
                    "sync": sync,
                    "label": label,
                    "anchors": _normalize_anchors(e.get("anchors", [])),
                    "graph_id": graph_id,
                }
            )

    nodes.sort(key=lambda x: x["id"])
    edges.sort(
        key=lambda x: (
            x.get("graph_id", ""),
            x["from"],
            x["to"],
            x["mark"],
            x["type"],
            x["sync"],
            x["label"],
        )
    )

    return {
        "schema_version": SCHEMA_VERSION_V2,
        "freeze_id": freeze_id,
        "generated_at": generated_at,
        "nodes": nodes,
        "edges": edges,
        "graphs": graphs,
    }


if __name__ == "__main__":
    import json

    payload = build_yaml_graph_v2(
        REPO_ROOT / "docs" / "_tech_graph",
        generated_at="2026-06-17T00:00:00Z",
        freeze_id="TECH_GRAPH_S2_FREEZE_20260519_V2_3",
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
