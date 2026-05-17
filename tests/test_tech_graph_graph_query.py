from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from tools.tech_graph_graph_query import (
    EXIT_FP4,
    EXIT_FP5,
    GraphQueryError,
    GraphQueryStore,
    load_graph_v2,
    query_downstream,
    query_neighbors,
    query_upstream,
)


def _minimal_v2_graph() -> dict:
    return {
        "schema_version": "graph_v2",
        "freeze_id": "TEST",
        "generated_at": "2026-05-17T00:00:00Z",
        "nodes": [
            {"id": "AUTH", "label": "鉴权"},
            {"id": "POOL", "label": "连接池"},
            {"id": "RAG", "label": "RAG"},
            {"id": "E", "label": "入口"},
        ],
        "edges": [
            {
                "from": "AUTH",
                "to": "POOL",
                "mark": "->",
                "type": "depends_on",
                "sync": True,
                "label": "",
                "anchors": [{"path": "api/auth.py", "symbol": "#L1", "line": 1}],
            },
            {
                "from": "POOL",
                "to": "RAG",
                "mark": "->",
                "type": "depends_on",
                "sync": True,
                "label": "",
                "anchors": [{"path": "api/pool.py", "symbol": "#L2"}],
            },
            {
                "from": "E",
                "to": "RAG",
                "mark": "->",
                "type": "depends_on",
                "sync": True,
                "label": "POST /chat",
                "anchors": [{"path": "api/index.py", "symbol": "chat"}],
            },
        ],
    }


@pytest.fixture
def minimal_store(tmp_path: Path) -> GraphQueryStore:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(_minimal_v2_graph(), indent=2), encoding="utf-8")
    return load_graph_v2(p)


def test_downstream_golden_depth2(minimal_store: GraphQueryStore) -> None:
    """golden：AUTH depth=2 含 POOL、RAG 与锚点。"""
    result = query_downstream(minimal_store, "AUTH", 2)
    ids = {n["id"] for n in result["nodes"]}
    assert ids == {"AUTH", "POOL", "RAG"}
    assert len(result["edges"]) == 2
    paths = {a["path"] for a in result["anchors"]}
    assert paths == {"api/auth.py", "api/pool.py"}


def test_upstream_golden(minimal_store: GraphQueryStore) -> None:
    result = query_upstream(minimal_store, "RAG", 2)
    ids = {n["id"] for n in result["nodes"]}
    assert ids == {"AUTH", "POOL", "RAG", "E"}


def test_neighbors_golden(minimal_store: GraphQueryStore) -> None:
    result = query_neighbors(minimal_store, "RAG")
    ids = {n["id"] for n in result["nodes"]}
    assert ids == {"POOL", "RAG", "E"}
    assert result["query"]["op"] == "neighbors"


def test_fp4_unknown_node(minimal_store: GraphQueryStore) -> None:
    with pytest.raises(GraphQueryError) as exc:
        query_downstream(minimal_store, "NO_SUCH", 1)
    assert exc.value.exit_code == EXIT_FP4
    assert "NO_SUCH" in str(exc.value)
    assert exc.value.sample_ids


def test_fp5_v1_graph_rejected(tmp_path: Path) -> None:
    """失败路径：graph_v1 禁止静默走 query（FP-5）。"""
    p = tmp_path / "graph.json"
    p.write_text(
        json.dumps(
            {
                "schema_version": "graph_v1",
                "generated_at": "2026-01-01T00:00:00Z",
                "nodes": ["AUTH"],
                "edges": [],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(GraphQueryError) as exc:
        load_graph_v2(p)
    assert exc.value.exit_code == EXIT_FP5


def test_committed_graph_auth_rag_e_non_empty() -> None:
    """验收：仓内 v2 对 AUTH / RAG / E 返回非空子图。"""
    repo_graph = Path(__file__).resolve().parents[1] / "docs" / "_tech_graph" / "graph.json"
    if not repo_graph.is_file():
        pytest.skip("无已提交 graph.json")
    data = json.loads(repo_graph.read_text(encoding="utf-8"))
    if data.get("schema_version") != "graph_v2":
        pytest.skip("graph.json 尚未升 graph_v2")

    store = load_graph_v2(repo_graph)
    for nid in ("AUTH", "RAG", "E"):
        r = query_downstream(store, nid, 1)
        assert r["nodes"], f"{nid} downstream 应非空"
        assert r["edges"], f"{nid} downstream 边应非空"


def test_cli_downstream_auth2() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "tech_graph_graph_query.py"
    proc = subprocess.run(
        [sys.executable, str(script), "downstream", "AUTH", "2"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 and "graph_v2" in (proc.stderr or ""):
        pytest.skip("graph.json 非 v2")
    assert proc.returncode == 0, proc.stderr
    payload = json.loads(proc.stdout)
    assert payload["query"] == {"op": "downstream", "root": "AUTH", "depth": 2}
    assert any(n["id"] == "POOL" for n in payload["nodes"])


def test_cli_fp4_unknown_node() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    script = repo_root / "tools" / "tech_graph_graph_query.py"
    proc = subprocess.run(
        [sys.executable, str(script), "downstream", "__UNKNOWN__", "1"],
        cwd=repo_root,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == EXIT_FP4
    assert "FP-4" in proc.stderr
