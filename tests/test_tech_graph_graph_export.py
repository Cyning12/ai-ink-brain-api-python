from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.tech_graph_graph_export import (
    FREEZE_ID,
    TechGraphParseError,
    build_graph_payload,
    collect_raw_edges,
    raw_edges_to_graph_dict,
    run_check,
)
from tools.tech_graph_graph_v2_schema import SCHEMA_VERSION_V2, validate_graph_v2


def _write_yaml_graph(d: Path, graph_id: str, body: str) -> None:
    (d / f"{graph_id}.graph.yaml").write_text(body, encoding="utf-8")


def test_collect_edges_golden_minimal(tmp_path: Path) -> None:
    """golden：链式边 + 异步标签 + :: 元关系（ai.md 解析保留）。"""
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

    payload = raw_edges_to_graph_dict(
        raw, generated_at="2026-05-14T00:00:00Z"
    )
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
    _write_yaml_graph(
        d,
        "01_empty",
        'graph_id: "01_empty"\ntitle: "Empty"\nnodes: []\nedges: []\n',
    )
    payload = build_graph_payload(d, generated_at="2026-01-01T00:00:00Z")
    assert payload["nodes"] == []
    assert payload["edges"] == []
    assert payload["schema_version"] == SCHEMA_VERSION_V2


def test_parse_failure_fp1_unknown_edge_syntax(tmp_path: Path) -> None:
    """FP-1：无法识别的边语法须抛出带路径/行号的信息（ai.md 解析保留）。"""
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


def test_build_graph_payload_from_yaml_golden(tmp_path: Path) -> None:
    """P1 golden：YAML 编辑源直接构建 graph_v2。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    _write_yaml_graph(
        d,
        "00_demo",
        '''graph_id: "00_demo"
title: "Demo"
nodes:
  - id: "AUTH"
    label: "AUTH"
  - id: "POOL"
    label: "连接池"
edges:
  - from: "AUTH"
    to: "POOL"
    anchors:
      - path: "api/index.py"
        line: 100
''',
    )
    payload = build_graph_payload(d, generated_at="2026-05-17T12:00:00Z")
    assert payload["schema_version"] == SCHEMA_VERSION_V2
    assert payload["freeze_id"] == FREEZE_ID
    validate_graph_v2(payload)
    edge = payload["edges"][0]
    assert edge["mark"] == "->"
    assert edge["anchors"][0]["path"] == "api/index.py"
    assert edge["anchors"][0]["symbol"] == "#L100"
    assert edge["anchors"][0]["line"] == 100
    node_labels = {n["id"]: n["label"] for n in payload["nodes"]}
    assert node_labels["POOL"] == "连接池"


def test_build_graph_payload_yaml_protocol_marks(tmp_path: Path) -> None:
    """YAML 显式 mark / type 映射与 ai.md 参考语义对齐。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    _write_yaml_graph(
        d,
        "01_protocol",
        '''graph_id: "01_protocol"
title: "Protocol"
nodes:
  - id: "A"
  - id: "B"
  - id: "C"
  - id: "D"
  - id: "E"
edges:
  - from: "A"
    to: "B"
    mark: "~>"
    type: "async_calls"
  - from: "B"
    to: "C"
    mark: "?>"
    type: "condition"
  - from: "C"
    to: "D"
    mark: "::branches"
    type: "branches"
  - from: "D"
    to: "E"
    mark: "[ok]"
''',
    )
    payload = build_graph_payload(d, generated_at="2026-05-17T12:00:00Z")
    by_pair = {(e["from"], e["to"]): e for e in payload["edges"]}
    assert by_pair[("A", "B")]["mark"] == "~>"
    assert by_pair[("A", "B")]["type"] == "async_calls"
    assert by_pair[("A", "B")]["sync"] is False
    assert by_pair[("B", "C")]["mark"] == "?>"
    assert by_pair[("B", "C")]["type"] == "condition"
    assert by_pair[("C", "D")]["mark"] == "::branches"
    assert by_pair[("C", "D")]["type"] == "branches"
    assert by_pair[("D", "E")]["mark"] == "[ok]"
    assert by_pair[("D", "E")]["type"] == "depends_on"


def test_build_graph_payload_yaml_class_diagram(tmp_path: Path) -> None:
    """golden：classDiagram mark 归一为 has_metadata。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    _write_yaml_graph(
        d,
        "03_class",
        '''graph_id: "03_class"
title: "Class"
nodes:
  - id: "documents"
    label: "documents"
  - id: "FileMeta"
    label: "FileMeta"
edges:
  - from: "documents"
    to: "FileMeta"
    mark: "classDiagram"
''',
    )
    payload = build_graph_payload(d, generated_at="2026-05-15T00:00:00Z")
    types = {(e["from"], e["to"], e["type"], e["sync"]) for e in payload["edges"]}
    assert ("documents", "FileMeta", "has_metadata", True) in types
    node_ids = {n["id"] for n in payload["nodes"]}
    assert "documents" in node_ids and "FileMeta" in node_ids
    validate_graph_v2(payload)


def test_run_check_yaml_matches(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    _write_yaml_graph(
        d,
        "z",
        '''graph_id: "z"
title: "Z"
nodes:
  - id: "A"
  - id: "B"
edges:
  - from: "A"
    to: "B"
''',
    )
    out = d / "graph.json"
    p = build_graph_payload(d, generated_at="2026-05-14T12:00:00Z")
    out.write_text(json.dumps(p, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert run_check(input_root=d, output_path=out) == 0


def test_run_check_ignores_ai_md_drift(tmp_path: Path) -> None:
    """F3 回归：仅污染 .ai.md 不影响 export --check（YAML 单源）。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    _write_yaml_graph(
        d,
        "z",
        '''graph_id: "z"
title: "Z"
nodes:
  - id: "A"
  - id: "B"
edges:
  - from: "A"
    to: "B"
''',
    )
    # ai.md 存在但与 YAML 拓扑不同；export 主路径不应读取它
    (d / "z.ai.md").write_text(
        "```mermaid\nflowchart TD\n  A --\"->\"--> B\n  B --\"->\"--> C\n```\n",
        encoding="utf-8",
    )
    out = d / "graph.json"
    p = build_graph_payload(d, generated_at="2026-05-14T12:00:00Z")
    out.write_text(json.dumps(p, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # 污染 ai.md：新增节点/边
    (d / "z.ai.md").write_text(
        "```mermaid\nflowchart TD\n  A --\"->\"--> B\n  B --\"->\"--> C\n  C --\"->\"--> D\n```\n",
        encoding="utf-8",
    )
    assert run_check(input_root=d, output_path=out) == 0


def test_run_check_drift_fp2(tmp_path: Path) -> None:
    """FP-2：--check 语义漂移 → 退出码 4。"""
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    _write_yaml_graph(
        d,
        "z",
        '''graph_id: "z"
title: "Z"
nodes:
  - id: "A"
  - id: "B"
edges:
  - from: "A"
    to: "B"
''',
    )
    out = d / "graph.json"
    p = build_graph_payload(d, generated_at="2026-05-14T12:00:00Z")
    out.write_text(json.dumps(p, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert run_check(input_root=d, output_path=out) == 0
    tampered = json.loads(out.read_text(encoding="utf-8"))
    tampered["edges"][0]["mark"] = "tampered"
    out.write_text(json.dumps(tampered, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    assert run_check(input_root=d, output_path=out) == 4
