from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.tech_graph_graph_equivalence_check import (
    compute_equivalence_metrics,
    run_equivalence_check,
)
from tools.tech_graph_graph_v2_reference import (
    build_reference_graph_v2,
    collect_reference_edges,
)
from tools.tech_graph_graph_v2_schema import GraphV2SchemaError, validate_graph_v2


def _minimal_v2(*, generated_at: str = "2026-05-17T00:00:00Z") -> dict:
    return {
        "schema_version": "graph_v2",
        "freeze_id": "TECH_GRAPH_S2_FREEZE_20260517_V2_2",
        "generated_at": generated_at,
        "nodes": [
            {"id": "A", "label": "Alpha"},
            {"id": "B", "label": "Beta"},
        ],
        "edges": [
            {
                "from": "A",
                "to": "B",
                "mark": "->",
                "type": "depends_on",
                "sync": True,
                "label": "",
                "anchors": [{"path": "api/x.py", "symbol": "#L1", "line": 1}],
            }
        ],
    }


def test_validate_graph_v2_rejects_invalid_p2_4a2_graphs() -> None:
    """P2-4a-2：graphs[] 须含 id/title；非法条目拒绝。"""
    base = _minimal_v2()
    with pytest.raises(GraphV2SchemaError, match="title"):
        validate_graph_v2({**base, "graphs": [{"id": "main"}]})
    ref_only = {
        "ref": {"node_id": "missing"},
        "mark": "->",
        "type": "depends_on",
        "sync": True,
        "label": "",
        "anchors": [],
    }
    with pytest.raises(GraphV2SchemaError, match="未知节点"):
        validate_graph_v2({**base, "edges": [ref_only]})


def test_validate_graph_v2_accepts_minimal() -> None:
    validate_graph_v2(_minimal_v2())


def test_reference_collects_anchors_golden(tmp_path: Path) -> None:
    """golden：边后 // → 注释进入 anchors[]。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "00_demo.ai.md").write_text(
        "```mermaid\n"
        "flowchart TD\n"
        '  AUTH --"->"--> POOL[[连接池]]\n'
        "  // → api/index.py#L100\n"
        "```\n",
        encoding="utf-8",
    )
    edges = collect_reference_edges(d, export_root=d.parent.parent)
    assert len(edges) == 1
    assert edges[0].source == "AUTH" and edges[0].target == "POOL"
    assert len(edges[0].anchors) == 1
    assert edges[0].anchors[0].path == "api/index.py"
    assert edges[0].anchors[0].line == 100

    ref = build_reference_graph_v2(d, generated_at="2026-05-17T12:00:00Z")
    validate_graph_v2(ref)
    assert ref["nodes"] == [
        {"id": "AUTH", "label": "AUTH", "graph_id": "00_demo"},
        {"id": "POOL", "label": "连接池", "graph_id": "00_demo"},
    ]
    assert len(ref["graphs"]) == 1
    assert ref["graphs"][0]["id"] == "00_demo"
    assert ref["graphs"][0]["source_ai_path"].endswith("docs/_tech_graph/00_demo.ai.md")
    assert ref["edges"][0]["anchors"][0]["path"] == "api/index.py"


def test_reference_splits_semantic_label(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "01_http.ai.md").write_text(
        "```mermaid\n"
        "flowchart TD\n"
        '  E --"POST /api/py/chat"--> C1[[RAG Chat]]\n'
        "```\n",
        encoding="utf-8",
    )
    ref = build_reference_graph_v2(d, generated_at="2026-05-17T00:00:00Z")
    edge = ref["edges"][0]
    assert edge["mark"] == "->"
    assert edge["label"] == "POST /api/py/chat"
    labels = {n["id"]: n["label"] for n in ref["nodes"]}
    assert labels["C1"] == "RAG Chat"
    assert labels["E"] == "E"


def test_equivalence_metrics_detects_missing_anchors() -> None:
    ref = _minimal_v2()
    exported = _minimal_v2()
    exported["edges"][0]["anchors"] = []
    m = compute_equivalence_metrics(ref, exported)
    assert m.anchor_coverage == 0.0
    assert not m.topology_ok or m.missing_anchor_edges


def test_equivalence_metrics_pass_when_aligned() -> None:
    ref = _minimal_v2()
    m = compute_equivalence_metrics(ref, ref)
    assert m.topology_ok
    assert m.anchor_coverage == 1.0
    assert m.edge_label_coverage == 1.0


def test_run_check_passes_on_committed_v2_when_upgraded() -> None:
    """P2-1：仓内 graph.json 为 graph_v2 时等价检查须 PASS。"""
    repo_graph = Path(__file__).resolve().parents[1] / "docs" / "_tech_graph" / "graph.json"
    if not repo_graph.is_file():
        pytest.skip("无已提交 graph.json")
    data = json.loads(repo_graph.read_text(encoding="utf-8"))
    if data.get("schema_version") != "graph_v2":
        pytest.skip("graph.json 尚未升 graph_v2")

    code = run_equivalence_check(
        input_root=repo_graph.parent,
        graph_path=repo_graph,
        freeze_id="TECH_GRAPH_S2_FREEZE_20260517_V2_2",
    )
    assert code == 0


def test_run_check_fp5_on_committed_v1(tmp_path: Path) -> None:
    """失败路径：仓库仍为 graph_v1 时等价检查须 FP-5（非静默降级）。"""
    repo_graph = Path(__file__).resolve().parents[1] / "docs" / "_tech_graph" / "graph.json"
    if not repo_graph.is_file():
        pytest.skip("无已提交 graph.json")
    data = json.loads(repo_graph.read_text(encoding="utf-8"))
    if data.get("schema_version") == "graph_v2":
        pytest.skip("已升 graph_v2，改测 v2 路径")

    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    real_input = repo_graph.parent
    code = run_equivalence_check(
        input_root=real_input,
        graph_path=repo_graph,
        freeze_id="TECH_GRAPH_S2_FREEZE_20260517_V2_2",
        require_v2=True,
    )
    assert code == 5


def test_equivalence_fails_below_anchor_threshold() -> None:
    """失败路径：锚点覆盖率低于 95% → FP-3。"""
    ref = _minimal_v2()
    exported = _minimal_v2()
    exported["edges"][0]["anchors"] = []
    m = compute_equivalence_metrics(ref, exported)
    assert m.anchor_coverage < 0.95


def test_run_check_passes_on_synthetic_v2(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "z.ai.md").write_text(
        "```mermaid\nflowchart TD\n  A --\"->\"--> B\n  // → api/a.py#L1\n```\n",
        encoding="utf-8",
    )
    ref = build_reference_graph_v2(d, generated_at="2026-05-17T00:00:00Z")
    out = d / "graph.json"
    out.write_text(json.dumps(ref, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert (
        run_equivalence_check(
            input_root=d,
            graph_path=out,
            freeze_id="TECH_GRAPH_S2_FREEZE_20260517_V2_2",
        )
        == 0
    )
