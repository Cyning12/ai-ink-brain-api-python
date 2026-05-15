from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.tech_graph_graph_export import (
    TechGraphParseError,
    build_graph_payload,
    collect_raw_edges,
    run_check,
)


def test_collect_edges_golden_minimal(tmp_path: Path) -> None:
    """golden：链式边 + 异步标签 + :: 元关系。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "00_demo.ai.md").write_text(
        "```mermaid\n"
        "flowchart TD\n"
        '  FE --"->"--> FE_STREAM --"~>"--> FE_PARSE\n'
        '  A --"::branches"--> B\n'
        "```\n",
        encoding="utf-8",
    )
    raw = collect_raw_edges(d)
    by_pair = {(e.source, e.target, e.label) for e in raw}
    assert ("FE", "FE_STREAM", "->") in by_pair
    assert ("FE_STREAM", "FE_PARSE", "~>") in by_pair
    assert ("A", "B", "::branches") in by_pair

    payload = build_graph_payload(d, generated_at="2026-05-14T00:00:00Z")
    types = {(e["from"], e["to"], e["type"], e["sync"]) for e in payload["edges"]}
    assert ("FE", "FE_STREAM", "depends_on", True) in types
    assert ("FE_STREAM", "FE_PARSE", "async_calls", False) in types
    assert ("A", "B", "branches", True) in types


def test_collect_edges_empty_flowchart(tmp_path: Path) -> None:
    """空图：仅有 flowchart 头与注释，无边。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "01_empty.ai.md").write_text(
        "```mermaid\nflowchart TD\n  %% no edges\n```\n",
        encoding="utf-8",
    )
    assert collect_raw_edges(d) == []
    payload = build_graph_payload(d, generated_at="2026-01-01T00:00:00Z")
    assert payload["nodes"] == []
    assert payload["edges"] == []


def test_parse_failure_fp1_unknown_edge_syntax(tmp_path: Path) -> None:
    """FP-1：无法识别的边语法须抛出带路径/行号的信息。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "02_bad.ai.md").write_text(
        "```mermaid\nflowchart TD\n  X --\"oops\n```\n",
        encoding="utf-8",
    )
    with pytest.raises(TechGraphParseError) as excinfo:
        collect_raw_edges(d)
    err = excinfo.value
    assert "02_bad.ai.md" in str(err.path)
    assert err.line_no is not None


def test_run_check_missing_file_fp2(tmp_path: Path) -> None:
    """FP-2：--check 且 graph.json 不存在 → 非 0。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    out = d / "graph.json"
    assert run_check(input_root=d, output_path=out) == 3


def test_run_check_json_matches(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "z.ai.md").write_text(
        "```mermaid\nflowchart TD\n  A --\"->\"--> B\n```\n",
        encoding="utf-8",
    )
    out = d / "graph.json"
    p = build_graph_payload(d, generated_at="2026-05-14T12:00:00Z")
    out.write_text(json.dumps(p, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert run_check(input_root=d, output_path=out) == 0


def test_class_diagram_golden_has_metadata(tmp_path: Path) -> None:
    """golden：classDiagram --> 归一为 has_metadata。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "03_class.ai.md").write_text(
        "```mermaid\n"
        "classDiagram\n"
        "  documents --> FileMeta : metadata\n"
        "```\n",
        encoding="utf-8",
    )
    raw = collect_raw_edges(d)
    assert len(raw) == 1
    assert raw[0].source == "documents" and raw[0].target == "FileMeta"
    payload = build_graph_payload(d, generated_at="2026-05-15T00:00:00Z")
    types = {(e["from"], e["to"], e["type"], e["sync"]) for e in payload["edges"]}
    assert ("documents", "FileMeta", "has_metadata", True) in types
    assert "documents" in payload["nodes"] and "FileMeta" in payload["nodes"]
