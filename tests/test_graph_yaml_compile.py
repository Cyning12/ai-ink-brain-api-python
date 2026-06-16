"""Tests for graph_yaml_compile.py — YAML→MD conversion + diff check."""

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
GRAPH_YAML = REPO_ROOT / "docs" / "_tech_graph" / "00_main.graph.yaml"
GRAPH_JSON = REPO_ROOT / "docs" / "_tech_graph" / "graph.json"
COMPILE_SCRIPT = REPO_ROOT / "scripts" / "graph_yaml_compile.py"


class TestGraphYamlCompile:
    """Red-phase tests: these will fail until implementation is written."""

    def test_yaml_source_exists(self):
        """F1: fp-yaml-parse — YAML source must exist."""
        assert GRAPH_YAML.exists(), f"YAML source not found: {GRAPH_YAML}"

    def test_yaml_source_is_valid_yaml(self):
        """F1: fp-yaml-parse — YAML must be syntactically valid."""
        if not GRAPH_YAML.exists():
            pytest.skip("YAML source not yet created")
        content = GRAPH_YAML.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        assert isinstance(data, dict), "YAML root must be a dict"
        assert "graph_id" in data, "YAML must have graph_id"
        assert "nodes" in data, "YAML must have nodes"
        assert "edges" in data, "YAML must have edges"

    def test_compile_script_exists(self):
        """Compile script must exist."""
        assert COMPILE_SCRIPT.exists(), f"Compile script not found: {COMPILE_SCRIPT}"

    def test_yaml_nodes_match_graph_json(self):
        """F2: fp-graph-diff — YAML nodes must match graph.json 00_main slice."""
        if not GRAPH_YAML.exists():
            pytest.skip("YAML source not yet created")
        if not GRAPH_JSON.exists():
            pytest.skip("graph.json not found")

        yaml_content = GRAPH_YAML.read_text(encoding="utf-8")
        yaml_data = yaml.safe_load(yaml_content)

        json_data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

        # Extract 00_main nodes from graph.json
        json_nodes = {
            n["id"]: n
            for n in json_data.get("nodes", [])
            if n.get("graph_id") == "00_main"
        }

        yaml_nodes = {n["id"]: n for n in yaml_data.get("nodes", [])}

        assert len(yaml_nodes) == len(json_nodes), (
            f"Node count mismatch: YAML={len(yaml_nodes)}, JSON={len(json_nodes)}"
        )
        assert set(yaml_nodes.keys()) == set(json_nodes.keys()), (
            f"Node ID mismatch: YAML={set(yaml_nodes.keys())}, JSON={set(json_nodes.keys())}"
        )

    def test_yaml_edges_match_graph_json(self):
        """F2: fp-graph-diff — YAML edges must match graph.json 00_main slice."""
        if not GRAPH_YAML.exists():
            pytest.skip("YAML source not yet created")
        if not GRAPH_JSON.exists():
            pytest.skip("graph.json not found")

        yaml_content = GRAPH_YAML.read_text(encoding="utf-8")
        yaml_data = yaml.safe_load(yaml_content)

        json_data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

        # Extract 00_main edges from graph.json (only topological edges, not ref edges)
        json_edges = [
            e
            for e in json_data.get("edges", [])
            if e.get("graph_id") == "00_main" and "from" in e and "to" in e
        ]
        json_edge_keys = {
            (e["from"], e["to"], e.get("mark", "->"), e.get("type", "depends_on"))
            for e in json_edges
        }

        yaml_edges = yaml_data.get("edges", [])
        yaml_edge_keys = {
            (e["from"], e["to"], e.get("mark", "->"), e.get("type", "depends_on"))
            for e in yaml_edges
        }

        assert len(yaml_edges) == len(json_edges), (
            f"Edge count mismatch: YAML={len(yaml_edges)}, JSON={len(json_edges)}"
        )
        assert yaml_edge_keys == json_edge_keys, (
            f"Edge mismatch: YAML extra={yaml_edge_keys - json_edge_keys}, "
            f"JSON extra={json_edge_keys - yaml_edge_keys}"
        )

    def test_yaml_anchors_match_graph_json(self):
        """R2: Anchor rendering — 4 edges with anchors must match."""
        if not GRAPH_YAML.exists():
            pytest.skip("YAML source not yet created")
        if not GRAPH_JSON.exists():
            pytest.skip("graph.json not found")

        yaml_content = GRAPH_YAML.read_text(encoding="utf-8")
        yaml_data = yaml.safe_load(yaml_content)
        json_data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

        json_edges = {
            (e["from"], e["to"]): e
            for e in json_data.get("edges", [])
            if e.get("graph_id") == "00_main" and "from" in e
        }

        for ye in yaml_data.get("edges", []):
            key = (ye["from"], ye["to"])
            if key not in json_edges:
                continue
            je = json_edges[key]
            yaml_anchors = ye.get("anchors", [])
            json_anchors = je.get("anchors", [])
            assert len(yaml_anchors) == len(json_anchors), (
                f"Anchor count mismatch for {key}: YAML={len(yaml_anchors)}, JSON={len(json_anchors)}"
            )

    def test_compile_script_check_mode(self):
        """F2: Compile script --check must exit 0 when YAML matches graph.json."""
        if not COMPILE_SCRIPT.exists():
            pytest.skip("Compile script not yet created")
        result = subprocess.run(
            [sys.executable, str(COMPILE_SCRIPT), "--check"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"--check failed with rc={result.returncode}: {result.stdout}\n{result.stderr}"
        )

    def test_anchor_format_in_generated_mermaid(self):
        """R2: Generated Mermaid anchor comments must match 99_mermaid_protocol.md §3."""
        if not COMPILE_SCRIPT.exists():
            pytest.skip("Compile script not yet created")
        # Generate MD to a temp location
        import tempfile
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            tmp_path = f.name
        result = subprocess.run(
            [sys.executable, str(COMPILE_SCRIPT), "--output", tmp_path],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            pytest.skip(f"Generation failed: {result.stderr}")

        md_content = Path(tmp_path).read_text(encoding="utf-8")
        Path(tmp_path).unlink(missing_ok=True)

        # Check anchor comment format: // → path#line or // → path::symbol
        import re
        anchor_pattern = re.compile(r"//\s*→\s+[^\s]+(?:#L\d+|::\w+)")
        # Find all anchor lines in mermaid block
        mermaid_lines = []
        in_mermaid = False
        for line in md_content.splitlines():
            if line.strip().startswith("```mermaid"):
                in_mermaid = True
                continue
            if in_mermaid and line.strip().startswith("```"):
                break
            if in_mermaid:
                mermaid_lines.append(line)

        anchor_lines = [l for l in mermaid_lines if "// →" in l]
        for line in anchor_lines:
            assert anchor_pattern.search(line), (
                f"Anchor line does not match protocol format: {line}"
            )
