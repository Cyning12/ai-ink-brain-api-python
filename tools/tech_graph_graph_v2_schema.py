from __future__ import annotations

"""
graph_v2 结构校验（P2-0 最小集 + P2-4a 渐进扩展）。

P2-4a-1：`nodes[].kind` 可选；缺省等价 P2-0。
P2-4a-2（未启用）：`graphs[]`、`edges[].ref` 仍禁止出现。
"""

from typing import Any

SCHEMA_VERSION_V2 = "graph_v2"

# P2-4a-2 延后：首 PR 仍禁止
P2_4_DEFERRED_ROOT_KEYS = frozenset({"graphs"})
P2_4_DEFERRED_EDGE_KEYS = frozenset({"ref"})

ALLOWED_NODE_KINDS = frozenset({"flow", "struct", "external"})

REQUIRED_ROOT_KEYS = ("schema_version", "generated_at", "freeze_id", "nodes", "edges")
REQUIRED_NODE_KEYS = ("id", "label")
REQUIRED_EDGE_KEYS = ("from", "to", "mark", "type", "sync", "label", "anchors")
REQUIRED_ANCHOR_KEYS = ("path", "symbol")


class GraphV2SchemaError(ValueError):
    """schema 校验失败。"""


def validate_graph_v2(obj: Any, *, strict_version: bool = True) -> None:
    """校验 graph_v2；无 P2-4 字段时与 P2-0 兼容（FP-4-4）。"""
    if not isinstance(obj, dict):
        raise GraphV2SchemaError("根类型必须是 object")

    for key in P2_4_DEFERRED_ROOT_KEYS:
        if key in obj:
            raise GraphV2SchemaError(f"P2-4a-2 未启用，禁止根字段: {key}")

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
        for key in REQUIRED_NODE_KEYS:
            if key not in node:
                raise GraphV2SchemaError(f"nodes[{i}] 缺少 {key}")
        _validate_node_kind(node, i)
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
        for key in P2_4_DEFERRED_EDGE_KEYS:
            if key in edge:
                raise GraphV2SchemaError(f"P2-4a-2 未启用，禁止 edges[].{key}")
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


def _validate_node_kind(node: dict[str, Any], index: int) -> None:
    """P2-4a-1：kind 可选；出现则须在允许枚举内。"""
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
