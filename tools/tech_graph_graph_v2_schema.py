from __future__ import annotations

"""
graph_v2 结构校验（P2-0 + P2-4a）。

P2-4a-1：`nodes[].kind` 可选。
P2-4a-2：`graphs[]`、`edges[].ref`（ref 与 from/to 互斥）。

单一真值：`docs/_tech_graph/graph_v2.schema.json`。本模块只执行加载后的校验逻辑，
禁止在 Python 中再维护一份字段表。
"""

import argparse
import json
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "docs" / "_tech_graph" / "graph_v2.schema.json"


def _load_schema(path: Path = SCHEMA_PATH) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"graph_v2 schema 缺失：{path}")
    return json.loads(path.read_text(encoding="utf-8"))


_SCHEMA = _load_schema()

SCHEMA_VERSION_V2 = _SCHEMA["schema_version"]
DEFAULT_GRAPH_ID = _SCHEMA["default_graph_id"]
ALLOWED_NODE_KINDS = frozenset(_SCHEMA["allowed_node_kinds"])

_REQUIRED_ROOT_KEYS = tuple(_SCHEMA["required_root_keys"])
_REQUIRED_NODE_KEYS = tuple(_SCHEMA["required_node_keys"])
_REQUIRED_EDGE_KEYS = tuple(_SCHEMA["required_edge_keys"])
_REQUIRED_ANCHOR_KEYS = tuple(_SCHEMA["required_anchor_keys"])
_REQUIRED_GRAPH_KEYS = tuple(_SCHEMA["required_graph_keys"])
_OPTIONAL_GRAPH_STRING_KEYS = tuple(_SCHEMA.get("optional_graph_string_keys", []))
_TYPE_MAP = _SCHEMA["type_map"]
_EDGE_MODE = _SCHEMA["edge_mode"]
_REF_SCHEMA = _SCHEMA["ref"]


class GraphV2SchemaError(ValueError):
    """schema 校验失败。"""


def graph_id_from_source_path(source_path: str) -> str:
    """自 `.graph.yaml` / `.ai.md` / 中性文件路径得到分图 id（文件名去后缀）。"""
    name = Path(source_path).name
    for suffix in (".ai.md", ".graph.yaml", ".md", ".yaml"):
        if name.endswith(suffix):
            return name[: -len(suffix)]
    return Path(source_path).stem


def _check_simple_type(value: Any, expected: str, field: str) -> None:
    """按 schema type_map 做基础类型检查；失败抛出 GraphV2SchemaError。

    错误消息与历史硬编码实现保持一致，避免下游断言抖动。
    """
    if expected == "string":
        if not isinstance(value, str):
            raise GraphV2SchemaError(f"{field} 须为 string")
        return
    if expected == "boolean":
        if not isinstance(value, bool):
            raise GraphV2SchemaError(f"{field} 须为 boolean")
        return
    if expected == "integer":
        if not isinstance(value, int):
            raise GraphV2SchemaError(f"{field} 须为 integer")
        return


def _non_empty_string(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise GraphV2SchemaError(f"{field} 须为非空 string")
    return value


def validate_graph_v2(obj: Any, *, strict_version: bool = True) -> None:
    """校验 graph_v2；无 graphs/ref 时与 P2-0 兼容（FP-4-4）。"""
    if not isinstance(obj, dict):
        raise GraphV2SchemaError("根类型必须是 object")

    for key in _REQUIRED_ROOT_KEYS:
        if key not in obj:
            raise GraphV2SchemaError(f"缺少根字段: {key}")

    ver = obj.get("schema_version")
    if strict_version and ver != SCHEMA_VERSION_V2:
        raise GraphV2SchemaError(f"schema_version 须为 {SCHEMA_VERSION_V2!r}，实际 {ver!r}")

    graph_ids = _validate_graphs(obj.get("graphs"))

    nodes = obj.get("nodes")
    if not isinstance(nodes, list):
        raise GraphV2SchemaError("nodes 必须是 array")

    seen_ids: set[str] = set()
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise GraphV2SchemaError(f"nodes[{i}] 必须是 object")
        for key in _REQUIRED_NODE_KEYS:
            if key not in node:
                raise GraphV2SchemaError(f"nodes[{i}] 缺少 {key}")
        _validate_node_kind(node, i)
        _validate_graph_id(node.get("graph_id"), graph_ids, f"nodes[{i}].graph_id")
        nid = node["id"]
        _non_empty_string(nid, f"nodes[{i}].id")
        if nid in seen_ids:
            raise GraphV2SchemaError(f"重复节点 id: {nid}")
        seen_ids.add(nid)
        _check_simple_type(node["label"], _TYPE_MAP["label"], f"nodes[{i}].label")

    edges = obj.get("edges")
    if not isinstance(edges, list):
        raise GraphV2SchemaError("edges 必须是 array")

    topo_keys = _EDGE_MODE["topological_keys"]
    ref_key = _EDGE_MODE["reference_key"]
    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise GraphV2SchemaError(f"edges[{i}] 必须是 object")
        has_ref = ref_key in edge
        has_from = topo_keys[0] in edge
        has_to = topo_keys[1] in edge
        if has_ref and (has_from or has_to):
            raise GraphV2SchemaError(
                f"edges[{i}]：ref 与 from/to 互斥，不能同时出现"
            )
        if has_ref:
            _validate_edge_ref(edge[ref_key], i, seen_ids, graph_ids)
            for key in _REQUIRED_EDGE_KEYS:
                if key not in edge:
                    raise GraphV2SchemaError(f"edges[{i}] 缺少 {key}")
        else:
            if not has_from or not has_to:
                raise GraphV2SchemaError(f"edges[{i}] 缺少 from 或 to")
            for key in _REQUIRED_EDGE_KEYS:
                if key not in edge:
                    raise GraphV2SchemaError(f"edges[{i}] 缺少 {key}")
            if edge["from"] not in seen_ids or edge["to"] not in seen_ids:
                raise GraphV2SchemaError(
                    f"edges[{i}] 引用未知节点: {edge['from']!r} -> {edge['to']!r}"
                )
            _validate_graph_id(edge.get("graph_id"), graph_ids, f"edges[{i}].graph_id")
        _check_simple_type(edge["sync"], _TYPE_MAP["sync"], f"edges[{i}].sync")
        anchors = edge["anchors"]
        if not isinstance(anchors, list):
            raise GraphV2SchemaError(f"edges[{i}].anchors 须为 array")
        for j, anc in enumerate(anchors):
            if not isinstance(anc, dict):
                raise GraphV2SchemaError(f"edges[{i}].anchors[{j}] 须为 object")
            for key in _REQUIRED_ANCHOR_KEYS:
                if key not in anc:
                    raise GraphV2SchemaError(f"edges[{i}].anchors[{j}] 缺少 {key}")
            for key in _REQUIRED_ANCHOR_KEYS:
                _check_simple_type(
                    anc[key], _TYPE_MAP[key], f"edges[{i}].anchors[{j}].{key}"
                )
            if "line" in anc:
                _check_simple_type(
                    anc["line"], _TYPE_MAP["line"], f"edges[{i}].anchors[{j}].line"
                )


def _validate_graphs(graphs: Any) -> set[str]:
    """校验 graphs[]；缺失时仅含默认 main。"""
    if graphs is None:
        return {DEFAULT_GRAPH_ID}
    if not isinstance(graphs, list):
        raise GraphV2SchemaError("graphs 必须是 array")
    ids: set[str] = set()
    for i, g in enumerate(graphs):
        if not isinstance(g, dict):
            raise GraphV2SchemaError(f"graphs[{i}] 必须是 object")
        for key in _REQUIRED_GRAPH_KEYS:
            if key not in g:
                raise GraphV2SchemaError(f"graphs[{i}] 缺少 {key}")
        gid = g["id"]
        _non_empty_string(gid, f"graphs[{i}].id")
        if gid in ids:
            raise GraphV2SchemaError(f"重复 graphs[].id: {gid}")
        ids.add(gid)
        _check_simple_type(g["title"], _TYPE_MAP["title"], f"graphs[{i}].title")
        for key in _OPTIONAL_GRAPH_STRING_KEYS:
            if key in g:
                _check_simple_type(g[key], _TYPE_MAP[key], f"graphs[{i}].{key}")
    return ids or {DEFAULT_GRAPH_ID}


def _validate_graph_id(
    graph_id: Any,
    allowed: set[str],
    field: str,
) -> None:
    if graph_id is None:
        return
    _non_empty_string(graph_id, field)
    if graph_id not in allowed:
        raise GraphV2SchemaError(f"{field} 未知 graph_id: {graph_id!r}")


def _validate_edge_ref(
    ref: Any,
    edge_index: int,
    node_ids: set[str],
    graph_ids: set[str],
) -> None:
    if not isinstance(ref, dict):
        raise GraphV2SchemaError(f"edges[{edge_index}].ref 必须是 object")
    for key in _REF_SCHEMA["required_keys"]:
        if key not in ref:
            raise GraphV2SchemaError(f"edges[{edge_index}].ref 缺少 {key}")
    node_id = ref["node_id"]
    _non_empty_string(node_id, f"edges[{edge_index}].ref.node_id")
    if node_id not in node_ids:
        raise GraphV2SchemaError(
            f"edges[{edge_index}].ref 指向未知节点: {node_id!r}"
        )
    if "graph_id" in ref:
        _validate_graph_id(
            ref.get("graph_id"), graph_ids, f"edges[{edge_index}].ref.graph_id"
        )


def _validate_node_kind(node: dict[str, Any], index: int) -> None:
    if "kind" not in node:
        return
    kind = node["kind"]
    _non_empty_string(kind, f"nodes[{index}].kind")
    if kind not in ALLOWED_NODE_KINDS:
        allowed = ", ".join(sorted(ALLOWED_NODE_KINDS))
        raise GraphV2SchemaError(
            f"nodes[{index}].kind 非法: {kind!r}（允许: {allowed}）"
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="校验 graph.json 是否符合 graph_v2.schema.json"
    )
    parser.add_argument(
        "--graph",
        type=Path,
        default=REPO_ROOT / "docs" / "_tech_graph" / "graph.json",
        help="待校验的 graph.json 路径（默认 docs/_tech_graph/graph.json）",
    )
    args = parser.parse_args(argv)

    graph_path: Path = args.graph
    if not graph_path.is_file():
        print(f"graph.json 不存在：{graph_path}", file=__import__("sys").stderr)
        return 2
    try:
        obj = json.loads(graph_path.read_text(encoding="utf-8"))
        validate_graph_v2(obj)
    except json.JSONDecodeError as exc:
        print(f"JSON 解析失败：{exc}", file=__import__("sys").stderr)
        return 2
    except GraphV2SchemaError as exc:
        print(f"schema 校验失败：{exc}", file=__import__("sys").stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
