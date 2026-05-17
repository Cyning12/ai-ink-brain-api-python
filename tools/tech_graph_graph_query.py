from __future__ import annotations

"""
graph_v2 内存图查询（P2-2 · 方案2）。

加载 docs/_tech_graph/graph.json（须 schema_version=graph_v2）；
提供 downstream / upstream / neighbors 子图 + anchors。

退出码：
- 0：成功（stdout JSON）
- 2：输入/JSON 解析失败
- 4：FP-4 query 未知节点
- 5：FP-5 非 graph_v2（禁止静默整包 v1 作 query 默认）

v1 整包仅作历史对照，须显式文档化降级路径，本模块不提供默认降级。
"""

import argparse
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any

_REPO_BOOT = Path(__file__).resolve().parent.parent
if str(_REPO_BOOT) not in sys.path:
    sys.path.insert(0, str(_REPO_BOOT))

from tools.tech_graph_graph_export import REPO_ROOT
from tools.tech_graph_graph_v2_schema import (
    SCHEMA_VERSION_V2,
    GraphV2SchemaError,
    validate_graph_v2,
)

DEFAULT_GRAPH = REPO_ROOT / "docs" / "_tech_graph" / "graph.json"

EXIT_FP4 = 4
EXIT_FP5 = 5

SAMPLE_ID_LIMIT = 12


class GraphQueryError(RuntimeError):
    """查询失败（含 FP 退出码）。"""

    def __init__(
        self,
        message: str,
        *,
        exit_code: int,
        sample_ids: list[str] | None = None,
    ) -> None:
        super().__init__(message)
        self.exit_code = exit_code
        self.sample_ids = sample_ids or []


class GraphQueryStore:
    """已加载的 v2 图与邻接索引。"""

    __slots__ = (
        "graph",
        "node_by_id",
        "downstream",
        "upstream",
        "edges",
    )

    def __init__(self, graph: dict[str, Any]) -> None:
        self.graph = graph
        self.node_by_id: dict[str, dict[str, Any]] = {
            n["id"]: n for n in graph.get("nodes") or []
        }
        self.downstream: dict[str, list[str]] = {nid: [] for nid in self.node_by_id}
        self.upstream: dict[str, list[str]] = {nid: [] for nid in self.node_by_id}
        self.edges: list[dict[str, Any]] = list(graph.get("edges") or [])
        for edge in self.edges:
            f, t = edge["from"], edge["to"]
            self.downstream[f].append(t)
            self.upstream[t].append(f)

    @property
    def node_ids(self) -> list[str]:
        return sorted(self.node_by_id.keys())


def _stderr(msg: str) -> None:
    print(msg, file=sys.stderr)


def load_graph_v2(path: Path) -> GraphQueryStore:
    """加载 graph.json；非 v2 抛 GraphQueryError(FP-5)。"""
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise GraphQueryError(f"无法读取图文件：{path}", exit_code=2) from exc

    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise GraphQueryError(f"JSON 解析失败：{exc}", exit_code=2) from exc

    if not isinstance(obj, dict):
        raise GraphQueryError("graph.json 根须为 object", exit_code=2)

    ver = obj.get("schema_version")
    if ver != SCHEMA_VERSION_V2:
        raise GraphQueryError(
            f"FP-5: schema_version={ver!r}，非 graph_v2；"
            "须先 P2-1 导出升版后再使用 graph_query（禁止静默整包 v1）",
            exit_code=EXIT_FP5,
        )

    try:
        validate_graph_v2(obj)
    except GraphV2SchemaError as exc:
        raise GraphQueryError(f"graph_v2 schema 校验失败：{exc}", exit_code=2) from exc

    return GraphQueryStore(obj)


def _require_node(store: GraphQueryStore, node_id: str) -> None:
    if node_id not in store.node_by_id:
        sample = store.node_ids[:SAMPLE_ID_LIMIT]
        raise GraphQueryError(
            f"FP-4: 未知节点 id={node_id!r}；示例 id: {', '.join(sample)}",
            exit_code=EXIT_FP4,
            sample_ids=sample,
        )


def _bfs_reachable(
    store: GraphQueryStore,
    start: str,
    depth: int,
    adj: dict[str, list[str]],
) -> set[str]:
    if depth < 0:
        raise GraphQueryError("depth 须 >= 0", exit_code=2)
    visited: set[str] = {start}
    frontier: set[str] = {start}
    for _ in range(depth):
        nxt: set[str] = set()
        for u in frontier:
            for v in adj.get(u, []):
                if v not in visited:
                    visited.add(v)
                    nxt.add(v)
        frontier = nxt
        if not frontier:
            break
    return visited


def _collect_anchors(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[tuple[Any, ...]] = set()
    out: list[dict[str, Any]] = []
    for edge in edges:
        for anc in edge.get("anchors") or []:
            if not isinstance(anc, dict):
                continue
            key = (anc.get("path"), anc.get("symbol"), anc.get("line"))
            if key in seen:
                continue
            seen.add(key)
            out.append(dict(anc))
    return out


def _subgraph_result(
    store: GraphQueryStore,
    *,
    op: str,
    root: str,
    depth: int | None,
    node_ids: set[str],
) -> dict[str, Any]:
    nodes = [store.node_by_id[nid] for nid in sorted(node_ids)]
    edges = [
        e
        for e in store.edges
        if e["from"] in node_ids and e["to"] in node_ids
    ]
    query: dict[str, Any] = {"op": op, "root": root}
    if depth is not None:
        query["depth"] = depth
    return {
        "schema_version": "graph_query_result_v1",
        "graph_schema_version": store.graph.get("schema_version"),
        "freeze_id": store.graph.get("freeze_id"),
        "query": query,
        "nodes": nodes,
        "edges": edges,
        "anchors": _collect_anchors(edges),
    }


def query_downstream(
    store: GraphQueryStore, node_id: str, depth: int
) -> dict[str, Any]:
    _require_node(store, node_id)
    reachable = _bfs_reachable(store, node_id, depth, store.downstream)
    return _subgraph_result(
        store, op="downstream", root=node_id, depth=depth, node_ids=reachable
    )


def query_upstream(store: GraphQueryStore, node_id: str, depth: int) -> dict[str, Any]:
    _require_node(store, node_id)
    reachable = _bfs_reachable(store, node_id, depth, store.upstream)
    return _subgraph_result(
        store, op="upstream", root=node_id, depth=depth, node_ids=reachable
    )


def query_neighbors(store: GraphQueryStore, node_id: str) -> dict[str, Any]:
    _require_node(store, node_id)
    neighbor_ids: set[str] = {node_id}
    for tgt in store.downstream.get(node_id, []):
        neighbor_ids.add(tgt)
    for src in store.upstream.get(node_id, []):
        neighbor_ids.add(src)
    return _subgraph_result(
        store, op="neighbors", root=node_id, depth=None, node_ids=neighbor_ids
    )


def run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="graph_v2 子图查询（downstream / upstream / neighbors）"
    )
    parser.add_argument(
        "--graph",
        type=Path,
        default=DEFAULT_GRAPH,
        help="graph.json 路径（默认 docs/_tech_graph/graph.json）",
    )
    parser.add_argument(
        "op",
        choices=("downstream", "upstream", "neighbors"),
        help="查询类型",
    )
    parser.add_argument("node_id", help="起点节点 id")
    parser.add_argument(
        "depth",
        nargs="?",
        type=int,
        help="hop 深度（neighbors 可省略）",
    )
    args = parser.parse_args(argv)

    graph_path = (
        (REPO_ROOT / args.graph).resolve()
        if not args.graph.is_absolute()
        else args.graph
    )

    try:
        store = load_graph_v2(graph_path)
    except GraphQueryError as exc:
        _stderr(str(exc))
        return exc.exit_code

    try:
        if args.op == "neighbors":
            result = query_neighbors(store, args.node_id)
        else:
            if args.depth is None:
                _stderr(f"{args.op} 需要 depth 参数")
                return 2
            if args.op == "downstream":
                result = query_downstream(store, args.node_id, args.depth)
            else:
                result = query_upstream(store, args.node_id, args.depth)
    except GraphQueryError as exc:
        _stderr(str(exc))
        return exc.exit_code

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_cli(argv)


if __name__ == "__main__":
    raise SystemExit(main())
