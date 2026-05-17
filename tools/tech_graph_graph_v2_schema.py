from __future__ import annotations

"""
graph_v2 结构校验（P2-0 + P2-4a）。

P2-4a-1：`nodes[].kind` 可选。
P2-4a-2：`graphs[]`、`edges[].ref`（ref 与 from/to 互斥）。
"""

from pathlib import Path
from typing import Any

SCHEMA_VERSION_V2 = "graph_v2"
DEFAULT_GRAPH_ID = "main"

ALLOWED_NODE_KINDS = frozenset({"flow", "struct", "external"})

REQUIRED_ROOT_KEYS = ("schema_version", "generated_at", "freeze_id", "nodes", "edges")
REQUIRED_NODE_KEYS = ("id", "label")
REQUIRED_EDGE_KEYS = ("mark", "type", "sync", "label", "anchors")
REQUIRED_ANCHOR_KEYS = ("path", "symbol")
REQUIRED_GRAPH_KEYS = ("id", "title")


class GraphV2SchemaError(ValueError):
    """schema 校验失败。"""


def graph_id_from_source_path(source_path: str) -> str:
    """自 .ai.md 相对路径得到分图 id（文件名去 .ai.md）。"""
    name = Path(source_path).name
    if name.endswith(".ai.md"):
        return name[: -len(".ai.md")]
    return Path(source_path).stem


def validate_graph_v2(obj: Any, *, strict_version: bool = True) -> None:
    """校验 graph_v2；无 graphs/ref 时与 P2-0 兼容（FP-4-4）。"""
    if not isinstance(obj, dict):
        raise GraphV2SchemaError("根类型必须是 object")

    for key in REQUIRED_ROOT_KEYS:
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
        for key in REQUIRED_NODE_KEYS:
            if key not in node:
                raise GraphV2SchemaError(f"nodes[{i}] 缺少 {key}")
        _validate_node_kind(node, i)
        _validate_graph_id(node.get("graph_id"), graph_ids, f"nodes[{i}].graph_id")
        nid = node["id"]
        if not isinstance(nid, str) or not nid:
            raise GraphV2SchemaError(f"nodes[{i}].id 须为非空 string")
        if nid in seen_ids:
            raise GraphV2SchemaError(f"重复节点 id: {nid}")
        seen_ids.add(nid)
        if not isinstance(node["label"], str):
            raise GraphV2SchemaError(f"nodes[{i}].label 须为 string")

    edges = obj.get("edges")
    if not isinstance(edges, list):
        raise GraphV2SchemaError("edges 必须是 array")

    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise GraphV2SchemaError(f"edges[{i}] 必须是 object")
        has_ref = "ref" in edge
        has_from = "from" in edge
        has_to = "to" in edge
        if has_ref and (has_from or has_to):
            raise GraphV2SchemaError(
                f"edges[{i}]：ref 与 from/to 互斥，不能同时出现"
            )
        if has_ref:
            _validate_edge_ref(edge["ref"], i, seen_ids, graph_ids)
            for key in REQUIRED_EDGE_KEYS:
                if key not in edge:
                    raise GraphV2SchemaError(f"edges[{i}] 缺少 {key}")
        else:
            if not has_from or not has_to:
                raise GraphV2SchemaError(f"edges[{i}] 缺少 from 或 to")
            for key in REQUIRED_EDGE_KEYS:
                if key not in edge:
                    raise GraphV2SchemaError(f"edges[{i}] 缺少 {key}")
            if edge["from"] not in seen_ids or edge["to"] not in seen_ids:
                raise GraphV2SchemaError(
                    f"edges[{i}] 引用未知节点: {edge['from']!r} -> {edge['to']!r}"
                )
            _validate_graph_id(edge.get("graph_id"), graph_ids, f"edges[{i}].graph_id")
        if not isinstance(edge["sync"], bool):
            raise GraphV2SchemaError(f"edges[{i}].sync 须为 boolean")
        anchors = edge["anchors"]
        if not isinstance(anchors, list):
            raise GraphV2SchemaError(f"edges[{i}].anchors 须为 array")
        for j, anc in enumerate(anchors):
            if not isinstance(anc, dict):
                raise GraphV2SchemaError(f"edges[{i}].anchors[{j}] 须为 object")
            for key in REQUIRED_ANCHOR_KEYS:
                if key not in anc:
                    raise GraphV2SchemaError(f"edges[{i}].anchors[{j}] 缺少 {key}")
            if "line" in anc and not isinstance(anc["line"], int):
                raise GraphV2SchemaError(f"edges[{i}].anchors[{j}].line 须为 integer")


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
        for key in REQUIRED_GRAPH_KEYS:
            if key not in g:
                raise GraphV2SchemaError(f"graphs[{i}] 缺少 {key}")
        gid = g["id"]
        if not isinstance(gid, str) or not gid:
            raise GraphV2SchemaError(f"graphs[{i}].id 须为非空 string")
        if gid in ids:
            raise GraphV2SchemaError(f"重复 graphs[].id: {gid}")
        ids.add(gid)
        if not isinstance(g["title"], str):
            raise GraphV2SchemaError(f"graphs[{i}].title 须为 string")
        if "source_ai_path" in g and not isinstance(g["source_ai_path"], str):
            raise GraphV2SchemaError(f"graphs[{i}].source_ai_path 须为 string")
    return ids or {DEFAULT_GRAPH_ID}


def _validate_graph_id(
    graph_id: Any,
    allowed: set[str],
    field: str,
) -> None:
    if graph_id is None:
        return
    if not isinstance(graph_id, str) or not graph_id:
        raise GraphV2SchemaError(f"{field} 须为非空 string")
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
    node_id = ref.get("node_id")
    if not isinstance(node_id, str) or not node_id:
        raise GraphV2SchemaError(f"edges[{edge_index}].ref.node_id 须为非空 string")
    if node_id not in node_ids:
        raise GraphV2SchemaError(
            f"edges[{edge_index}].ref 指向未知节点: {node_id!r}"
        )
    if "graph_id" in ref:
        _validate_graph_id(ref.get("graph_id"), graph_ids, f"edges[{edge_index}].ref.graph_id")


def _validate_node_kind(node: dict[str, Any], index: int) -> None:
    if "kind" not in node:
        return
    kind = node["kind"]
    if not isinstance(kind, str) or not kind:
        raise GraphV2SchemaError(f"nodes[{index}].kind 须为非空 string")
    if kind not in ALLOWED_NODE_KINDS:
        allowed = ", ".join(sorted(ALLOWED_NODE_KINDS))
        raise GraphV2SchemaError(
            f"nodes[{index}].kind 非法: {kind!r}（允许: {allowed}）"
        )
