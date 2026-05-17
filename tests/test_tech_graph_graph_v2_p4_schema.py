from __future__ import annotations

import pytest

from tools.tech_graph_graph_v2_schema import (
    ALLOWED_NODE_KINDS,
    GraphV2SchemaError,
    validate_graph_v2,
)


def _minimal_v2() -> dict:
    return {
        "schema_version": "graph_v2",
        "freeze_id": "TECH_GRAPH_S2_FREEZE_20260517_V2_1",
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


def test_fp44_minimal_without_kind_still_valid() -> None:
    """无 P2-4 字段时与 P2-0 等价（FP-4-4）。"""
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


def test_p4a2_deferred_graphs_still_forbidden() -> None:
    with pytest.raises(GraphV2SchemaError, match="graphs"):
        validate_graph_v2({**_minimal_v2(), "graphs": [{"id": "main", "title": "Main"}]})


def test_p4a2_deferred_ref_still_forbidden() -> None:
    base = _minimal_v2()
    bad_edge = {**base["edges"][0], "ref": {"node_id": "X"}}
    with pytest.raises(GraphV2SchemaError, match="ref"):
        validate_graph_v2({**base, "edges": [bad_edge]})
