from __future__ import annotations

import pytest

from tools.tech_graph_graph_v2_schema import (
    ALLOWED_NODE_KINDS,
    GraphV2SchemaError,
    validate_graph_v2,
)


def _minimal_v2(*, with_graphs: bool = False) -> dict:
    payload: dict = {
        "schema_version": "graph_v2",
        "freeze_id": "TECH_GRAPH_S2_FREEZE_20260517_V2_2",
        "generated_at": "2026-05-17T00:00:00Z",
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
                "anchors": [],
            }
        ],
    }
    if with_graphs:
        payload["graphs"] = [{"id": "main", "title": "main"}]
    return payload


def test_fp44_minimal_without_p2_4_still_valid() -> None:
    """无 graphs/ref 时与 P2-0 兼容（FP-4-4）。"""
    validate_graph_v2(_minimal_v2())


def test_p4a1_accepts_optional_kind() -> None:
    base = _minimal_v2()
    for kind in ALLOWED_NODE_KINDS:
        nodes = [
            {"id": "A", "label": "a", "kind": kind},
            {"id": "B", "label": "b"},
        ]
        validate_graph_v2({**base, "nodes": nodes})


def test_p4a1_rejects_invalid_kind() -> None:
    base = _minimal_v2()
    with pytest.raises(GraphV2SchemaError, match="kind 非法"):
        validate_graph_v2(
            {
                **base,
                "nodes": [{"id": "A", "label": "a", "kind": "phase"}, {"id": "B", "label": "b"}],
            }
        )


def test_p4a2_accepts_graphs_catalog() -> None:
    base = _minimal_v2(with_graphs=True)
    base["nodes"] = [
        {"id": "A", "label": "a", "graph_id": "main"},
        {"id": "B", "label": "b", "graph_id": "main"},
    ]
    base["edges"][0]["graph_id"] = "main"
    validate_graph_v2(base)


def test_p4a2_rejects_unknown_graph_id_on_node() -> None:
    base = _minimal_v2(with_graphs=True)
    base["nodes"][0]["graph_id"] = "missing"
    with pytest.raises(GraphV2SchemaError, match="graph_id"):
        validate_graph_v2(base)


def test_p4a2_accepts_ref_edge_without_from_to() -> None:
    base = _minimal_v2(with_graphs=True)
    base["edges"].append(
        {
            "ref": {"node_id": "B", "graph_id": "main"},
            "mark": "->",
            "type": "depends_on",
            "sync": True,
            "label": "",
            "anchors": [],
        }
    )
    validate_graph_v2(base)


def test_fp42_rejects_unknown_ref_node() -> None:
    base = _minimal_v2(with_graphs=True)
    base["edges"].append(
        {
            "ref": {"node_id": "Z"},
            "mark": "->",
            "type": "depends_on",
            "sync": True,
            "label": "",
            "anchors": [],
        }
    )
    with pytest.raises(GraphV2SchemaError, match="未知节点"):
        validate_graph_v2(base)


def test_p4a2_rejects_ref_and_from_to_together() -> None:
    base = _minimal_v2(with_graphs=True)
    bad = {
        **base["edges"][0],
        "ref": {"node_id": "B"},
    }
    with pytest.raises(GraphV2SchemaError, match="互斥"):
        validate_graph_v2({**base, "edges": [bad]})
