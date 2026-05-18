from __future__ import annotations

"""
graph_v2 内存图查询（P2-2 · 方案2）。

加载 docs/_tech_graph/graph.json（须 schema_version=graph_v2）；
提供 downstream / upstream / neighbors / has_path / describe_impact。

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
            # P2-4a-2：ref 边不参与单图 BFS（默认 query 路径不变）
            if "ref" in edge:
                continue
            f, t = edge.get("from"), edge.get("to")
            if not f or not t:
                continue
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


def has_path(store: GraphQueryStore, from_id: str, to_id: str) -> bool:
    """有向路径存在性（沿 downstream；ref 边已在 store 构建时排除）。"""
    _require_node(store, from_id)
    _require_node(store, to_id)
    if from_id == to_id:
        return True
    visited: set[str] = {from_id}
    frontier: deque[str] = deque([from_id])
    while frontier:
        u = frontier.popleft()
        for v in store.downstream.get(u, []):
            if v == to_id:
                return True
            if v not in visited:
                visited.add(v)
                frontier.append(v)
    return False


def _format_node_refs(store: GraphQueryStore, node_ids: set[str]) -> str:
    if not node_ids:
        return "无"
    parts: list[str] = []
    for nid in sorted(node_ids):
        label = store.node_by_id[nid].get("label") or nid
        parts.append(f"{label}({nid})")
    return "、".join(parts)


def describe_impact(store: GraphQueryStore, node_id: str, depth: int = 2) -> str:
    """组合 downstream/upstream 子图，输出人类可读影响描述（非裸 JSON）。"""
    _require_node(store, node_id)
    down = query_downstream(store, node_id, depth)
    up = query_upstream(store, node_id, depth)
    down_ids = {n["id"] for n in down["nodes"]} - {node_id}
    up_ids = {n["id"] for n in up["nodes"]} - {node_id}
    root_label = store.node_by_id[node_id].get("label") or node_id
    return (
        f"节点 {root_label}({node_id}) 影响分析（depth={depth}）：\n"
        f"- 下游（直接/间接）: {_format_node_refs(store, down_ids)}\n"
        f"- 上游（依赖方）: {_format_node_refs(store, up_ids)}"
    )


def run_cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "graph_v2 子图查询（downstream / upstream / neighbors / "
            "has-path / describe-impact）"
        )
    )
    parser.add_argument(
        "--graph",
        type=Path,
        default=DEFAULT_GRAPH,
        help="graph.json 路径（默认 docs/_tech_graph/graph.json）",
    )
    parser.add_argument(
        "op",
        choices=(
            "downstream",
            "upstream",
            "neighbors",
            "has-path",
            "describe-impact",
        ),
        help="查询类型",
    )
    parser.add_argument(
        "arg1",
        help="node_id（子图）或 from_id（has-path）",
    )
    parser.add_argument(
        "arg2",
        nargs="?",
        help="depth / to_id（has-path 时为 to_id）",
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
            result = query_neighbors(store, args.arg1)
            json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
            sys.stdout.write("\n")
            return 0
        if args.op == "has-path":
            if args.arg2 is None:
                _stderr("has-path 需要 to_id 参数")
                return 2
            path_ok = has_path(store, args.arg1, args.arg2)
            json.dump(
                {
                    "schema_version": "graph_query_result_v1",
                    "graph_schema_version": store.graph.get("schema_version"),
                    "freeze_id": store.graph.get("freeze_id"),
                    "query": {
                        "op": "has-path",
                        "from": args.arg1,
                        "to": args.arg2,
                    },
                    "has_path": path_ok,
                },
                sys.stdout,
                ensure_ascii=False,
                indent=2,
            )
            sys.stdout.write("\n")
            return 0
        if args.op == "describe-impact":
            depth = int(args.arg2) if args.arg2 is not None else 2
            text = describe_impact(store, args.arg1, depth)
            sys.stdout.write(text)
            if not text.endswith("\n"):
                sys.stdout.write("\n")
            return 0
        if args.arg2 is None:
            _stderr(f"{args.op} 需要 depth 参数")
            return 2
        depth = int(args.arg2)
        if args.op == "downstream":
            result = query_downstream(store, args.arg1, depth)
        else:
            result = query_upstream(store, args.arg1, depth)
    except GraphQueryError as exc:
        _stderr(str(exc))
        return exc.exit_code
    except ValueError:
        _stderr("depth 须为整数")
        return 2

    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return 0


def main(argv: list[str] | None = None) -> int:
    return run_cli(argv)


if __name__ == "__main__":
    raise SystemExit(main())
