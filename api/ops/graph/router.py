"""Graph summary 与 module-issues 矩阵路由。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends, HTTPException

from api.ops.deps import get_supabase_client, require_ops_secret

from .store import OpsGraphStore

router = APIRouter(prefix="/ops/graph", tags=["ops-graph"])


def get_graph_store(client: Any = Depends(get_supabase_client)) -> OpsGraphStore:
    """解析默认 repo 并返回 GraphStore；测试时可通过 dependency_overrides 替换。"""
    from api.ops.sync.store import OpsSyncStore

    repo_id = OpsSyncStore().ensure_repo()
    return OpsGraphStore(repo_id=repo_id, client=client)


@router.get("/summary")
def graph_summary(
    store: OpsGraphStore = Depends(get_graph_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    snapshot = store.get_latest_snapshot()
    if not snapshot:
        raise HTTPException(
            status_code=404,
            detail={"code": "GRAPH_SNAPSHOT_NOT_FOUND"},
        )

    payload = snapshot.get("payload") or {}
    graphs = payload.get("graphs", [])
    nodes = payload.get("nodes", [])

    return {
        "snapshot_id": snapshot["id"],
        "source_branch": snapshot.get("source_branch"),
        "source_commit": snapshot.get("source_commit"),
        "manifest_version": snapshot.get("manifest_version"),
        "schema_version": payload.get("schema_version"),
        "freeze_id": payload.get("freeze_id"),
        "node_count": len(nodes),
        "edge_count": len(payload.get("edges", [])),
        "graph_count": len(graphs),
        "graphs": [
            {"id": g["id"], "title": g.get("title")}
            for g in graphs
            if isinstance(g, dict)
        ],
        "created_at": snapshot.get("created_at"),
    }


@router.get("/module-issues")
def module_issues(
    state: str = "open",
    store: OpsGraphStore = Depends(get_graph_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    snapshot = store.get_latest_snapshot()
    if not snapshot:
        raise HTTPException(
            status_code=404,
            detail={"code": "GRAPH_SNAPSHOT_NOT_FOUND"},
        )

    payload = snapshot.get("payload") or {}
    modules = store.get_module_matrix(payload, state=state)

    return {"modules": modules}
