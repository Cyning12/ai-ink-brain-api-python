"""graph.json 校验器：验证结构、freeze_id、schema_version。"""

from __future__ import annotations

from typing import Any


class GraphValidationError(Exception):
    """graph.json 结构校验失败。"""

    def __init__(self, message: str, path: str | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.path = path


def _require(obj: Any, key: str, path: str = "root") -> Any:
    if not isinstance(obj, dict):
        raise GraphValidationError(f"expected dict at {path}, got {type(obj).__name__}")
    if key not in obj:
        raise GraphValidationError(f"missing required key '{key}'", path=path)
    return obj[key]


def validate_graph_json(payload: dict[str, Any]) -> dict[str, Any]:
    """校验 graph.json 结构，返回规范化元数据。

    校验项：
    - schema_version 存在且为字符串
    - freeze_id 存在且为字符串
    - nodes 为列表，每项含 id / label / graph_id
    - edges 为列表，每项含 from / to / type / graph_id
    - graphs 为列表，每项含 id / title

    返回：{"schema_version", "freeze_id", "node_count", "edge_count", "graph_count"}
    """
    schema_version = _require(payload, "schema_version", "root")
    if not isinstance(schema_version, str):
        raise GraphValidationError("schema_version must be string", path="root.schema_version")

    freeze_id = _require(payload, "freeze_id", "root")
    if not isinstance(freeze_id, str):
        raise GraphValidationError("freeze_id must be string", path="root.freeze_id")

    nodes = _require(payload, "nodes", "root")
    if not isinstance(nodes, list):
        raise GraphValidationError("nodes must be list", path="root.nodes")
    for i, node in enumerate(nodes):
        if not isinstance(node, dict):
            raise GraphValidationError(f"node[{i}] must be dict", path=f"root.nodes[{i}]")
        for k in ("id", "label", "graph_id"):
            if k not in node:
                raise GraphValidationError(f"node[{i}] missing '{k}'", path=f"root.nodes[{i}]")

    edges = _require(payload, "edges", "root")
    if not isinstance(edges, list):
        raise GraphValidationError("edges must be list", path="root.edges")
    for i, edge in enumerate(edges):
        if not isinstance(edge, dict):
            raise GraphValidationError(f"edge[{i}] must be dict", path=f"root.edges[{i}]")
        for k in ("from", "to", "type", "graph_id"):
            if k not in edge:
                raise GraphValidationError(f"edge[{i}] missing '{k}'", path=f"root.edges[{i}]")

    graphs = _require(payload, "graphs", "root")
    if not isinstance(graphs, list):
        raise GraphValidationError("graphs must be list", path="root.graphs")
    for i, graph in enumerate(graphs):
        if not isinstance(graph, dict):
            raise GraphValidationError(f"graph[{i}] must be dict", path=f"root.graphs[{i}]")
        for k in ("id", "title"):
            if k not in graph:
                raise GraphValidationError(f"graph[{i}] missing '{k}'", path=f"root.graphs[{i}]")

    return {
        "schema_version": schema_version,
        "freeze_id": freeze_id,
        "node_count": len(nodes),
        "edge_count": len(edges),
        "graph_count": len(graphs),
    }
