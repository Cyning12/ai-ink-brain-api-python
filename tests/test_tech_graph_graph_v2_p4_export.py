from __future__ import annotations

from pathlib import Path

from tools.tech_graph_graph_export import FREEZE_ID, build_graph_payload
from tools.tech_graph_graph_v2_schema import validate_graph_v2


def _write_yaml_graph(d: Path, graph_id: str, body: str) -> None:
    (d / f"{graph_id}.graph.yaml").write_text(body, encoding="utf-8")


def test_export_includes_graphs_and_graph_id(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    _write_yaml_graph(
        d,
        "a_flow",
        '''graph_id: "a_flow"
title: "A Flow"
nodes:
  - id: "X"
  - id: "Y"
edges:
  - from: "X"
    to: "Y"
''',
    )
    _write_yaml_graph(
        d,
        "b_flow",
        '''graph_id: "b_flow"
title: "B Flow"
nodes:
  - id: "P"
  - id: "Z"
edges:
  - from: "P"
    to: "Z"
''',
    )
    payload = build_graph_payload(d, generated_at="2026-05-17T12:00:00Z", freeze_id=FREEZE_ID)
    validate_graph_v2(payload)
    assert "graphs" in payload
    gids = {g["id"] for g in payload["graphs"]}
    assert gids == {"a_flow", "b_flow"}
    assert all("graph_id" in n for n in payload["nodes"])
    assert all("graph_id" in e for e in payload["edges"])
