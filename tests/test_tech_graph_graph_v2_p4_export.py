from __future__ import annotations

from pathlib import Path

from tools.tech_graph_graph_export import FREEZE_ID, build_graph_payload
from tools.tech_graph_graph_v2_schema import validate_graph_v2


def test_export_includes_graphs_and_graph_id(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "a_flow.ai.md").write_text(
        "```mermaid\nflowchart TD\n  X --\"->\"--> Y\n```\n",
        encoding="utf-8",
    )
    (d / "b_flow.ai.md").write_text(
        "```mermaid\nflowchart TD\n  Y --\"->\"--> Z\n```\n",
        encoding="utf-8",
    )
    payload = build_graph_payload(d, generated_at="2026-05-17T12:00:00Z", freeze_id=FREEZE_ID)
    validate_graph_v2(payload)
    assert "graphs" in payload
    gids = {g["id"] for g in payload["graphs"]}
    assert gids == {"a_flow", "b_flow"}
    assert all("graph_id" in n for n in payload["nodes"])
    assert all("graph_id" in e for e in payload["edges"])
