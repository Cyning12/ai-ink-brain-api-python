from __future__ import annotations

"""
graph_v2 结构校验（P2-0）。

禁止 P2-0 字段：graphs[]、edges[].ref、nodes[].kind。
"""

from typing import Any

SCHEMA_VERSION_V2 = "graph_v2"

# P2-4 字段；P2-0 出现即校验失败
FORBIDDEN_ROOT_KEYS = frozenset({"graphs"})
FORBIDDEN_NODE_KEYS = frozenset({"kind"})
FORBIDDEN_EDGE_KEYS = frozenset({"ref"})

REQUIRED_ROOT_KEYS = ("schema_version", "generated_at", "freeze_id", "nodes", "edges")
REQUIRED_NODE_KEYS = ("id", "label")
REQUIRED_EDGE_KEYS = ("from", "to", "mark", "type", "sync", "label", "anchors")
REQUIRED_ANCHOR_KEYS = ("path", "symbol")


class GraphV2SchemaError(ValueError):
    """schema 校验失败。"""


def validate_graph_v2(obj: Any, *, strict_version: bool = True) -> None:
    """校验对象为 P2-0 graph_v2；失败抛 GraphV2SchemaError。"""
    if not isinstance(obj, dict):
        raise GraphV2SchemaError("根类型必须是 object")

    for key in FORBIDDEN_ROOT_KEYS:
        if key in obj:
            raise GraphV2SchemaError(f"P2-0 禁止根字段: {key}")

    for key in REQUIRED_ROOT_KEYS:
        if key not in obj:
            raise GraphV2SchemaError(f"缺少根字段: {key}")

    ver = obj.get("schema_version")
    if strict_version and ver != SCHEMA_VERSION_V2:
        raise GraphV2SchemaError(f"schema_version 须为 {SCHEMA_VERSION_V2!r}，实际 {ver!r}")

    nodes = obj.get("nodes")
    if not isinstance(nodes, list):
        raise GraphV2SchemaError("nodes 必须是 array")

    seen_ids: set[str] = set()
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise GraphV2SchemaError(f"nodes[{i}] 必须是 object")
        for key in FORBIDDEN_NODE_KEYS:
            if key in node:
                raise GraphV2SchemaError(f"P2-0 禁止 nodes[].{key}")
        for key in REQUIRED_NODE_KEYS:
            if key not in node:
                raise GraphV2SchemaError(f"nodes[{i}] 缺少 {key}")
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
        for key in FORBIDDEN_EDGE_KEYS:
            if key in edge:
                raise GraphV2SchemaError(f"P2-0 禁止 edges[].{key}")
        for key in REQUIRED_EDGE_KEYS:
            if key not in edge:
                raise GraphV2SchemaError(f"edges[{i}] 缺少 {key}")
        if edge["from"] not in seen_ids or edge["to"] not in seen_ids:
            raise GraphV2SchemaError(
                f"edges[{i}] 引用未知节点: {edge['from']!r} -> {edge['to']!r}"
            )
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
