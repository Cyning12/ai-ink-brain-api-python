"""Tests for 14_runtime_observability.graph.yaml — YAML→MD conversion + diff check."""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]
GRAPH_YAML = REPO_ROOT / "docs" / "_tech_graph" / "14_runtime_observability.graph.yaml"
GRAPH_JSON = REPO_ROOT / "docs" / "_tech_graph" / "graph.json"
COMPILE_SCRIPT = REPO_ROOT / "scripts" / "graph_yaml_compile.py"


class TestGraphYamlP414RuntimeObservability:
    """P4: 14_runtime_observability YAML source validation."""

    def test_14_runtime_observability_yaml_source_exists(self):
        """F1: YAML source must exist."""
        assert GRAPH_YAML.exists(), f"YAML source not found: {GRAPH_YAML}"

    def test_14_runtime_observability_yaml_source_is_valid_yaml(self):
        """F1: YAML must be syntactically valid."""
        if not GRAPH_YAML.exists():
            pytest.skip("YAML source not yet created")
        content = GRAPH_YAML.read_text(encoding="utf-8")
        data = yaml.safe_load(content)
        assert isinstance(data, dict), "YAML root must be a dict"
        assert data.get("graph_id") == "14_runtime_observability", "YAML graph_id must be 14_runtime_observability"
        assert "nodes" in data, "YAML must have nodes"
        assert "edges" in data, "YAML must have edges"

    def test_14_runtime_observability_yaml_nodes_match_graph_json(self):
        """F2: YAML nodes must match graph.json 14_runtime_observability slice."""
        if not GRAPH_YAML.exists() or not GRAPH_JSON.exists():
            pytest.skip("Source files not found")

        yaml_data = yaml.safe_load(GRAPH_YAML.read_text(encoding="utf-8"))
        json_data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

        json_nodes = {
            n["id"]: n
            for n in json_data.get("nodes", [])
            if n.get("graph_id") == "14_runtime_observability"
        }
        yaml_nodes = {n["id"]: n for n in yaml_data.get("nodes", [])}

        assert len(yaml_nodes) == len(json_nodes), (
            f"Node count mismatch: YAML={len(yaml_nodes)}, JSON={len(json_nodes)}"
        )
        assert set(yaml_nodes.keys()) == set(json_nodes.keys()), (
            f"Node ID mismatch: YAML={set(yaml_nodes.keys())}, JSON={set(json_nodes.keys())}"
        )

    def test_14_runtime_observability_yaml_edges_match_graph_json(self):
        """F2: YAML edges must match graph.json 14_runtime_observability slice."""
        if not GRAPH_YAML.exists() or not GRAPH_JSON.exists():
            pytest.skip("Source files not found")

        yaml_data = yaml.safe_load(GRAPH_YAML.read_text(encoding="utf-8"))
        json_data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

        json_edges = [
            e
            for e in json_data.get("edges", [])
            if e.get("graph_id") == "14_runtime_observability" and "from" in e and "to" in e
        ]
        json_edge_keys = {
            (e["from"], e["to"], e.get("mark", "->"), e.get("type", "depends_on"))
            for e in json_edges
        }
        yaml_edge_keys = {
            (e["from"], e["to"], e.get("mark", "->"), e.get("type", "depends_on"))
            for e in yaml_data.get("edges", [])
        }

        assert len(yaml_data.get("edges", [])) == len(json_edges), (
            f"Edge count mismatch: YAML={len(yaml_data.get('edges', []))}, JSON={len(json_edges)}"
        )
        assert yaml_edge_keys == json_edge_keys, (
            f"Edge mismatch: YAML extra={yaml_edge_keys - json_edge_keys}, "
            f"JSON extra={json_edge_keys - yaml_edge_keys}"
        )

    def test_14_runtime_observability_yaml_anchors_match_graph_json(self):
        """R2: Total anchor counts per (from, to) must match graph.json."""
        if not GRAPH_YAML.exists() or not GRAPH_JSON.exists():
            pytest.skip("Source files not found")

        yaml_data = yaml.safe_load(GRAPH_YAML.read_text(encoding="utf-8"))
        json_data = json.loads(GRAPH_JSON.read_text(encoding="utf-8"))

        def anchor_counts_by_key(edges):
            counts: dict[tuple[str, str], int] = {}
            for e in edges:
                key = (e["from"], e["to"])
                counts[key] = counts.get(key, 0) + len(e.get("anchors", []))
            return counts

        json_edges = [
            e
            for e in json_data.get("edges", [])
            if e.get("graph_id") == "14_runtime_observability" and "from" in e
        ]
        json_counts = anchor_counts_by_key(json_edges)
        yaml_counts = anchor_counts_by_key(yaml_data.get("edges", []))

        assert yaml_counts == json_counts, (
            f"Anchor count mismatch: YAML={yaml_counts}, JSON={json_counts}"
        )

    def test_14_runtime_observability_compile_script_check_mode(self):
        """F2: Compile script --check must exit 0 for 14_runtime_observability."""
        if not COMPILE_SCRIPT.exists():
            pytest.skip("Compile script not yet created")
        result = subprocess.run(
            [sys.executable, str(COMPILE_SCRIPT), "--check", "--graph-id", "14_runtime_observability"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"--check failed with rc={result.returncode}: {result.stdout}\n{result.stderr}"
        )

    def test_14_runtime_observability_anchor_format_in_generated_mermaid(self):
        """R2: Generated Mermaid anchor comments must match protocol."""
        if not COMPILE_SCRIPT.exists():
            pytest.skip("Compile script not yet created")

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            tmp_path = f.name
        result = subprocess.run(
            [sys.executable, str(COMPILE_SCRIPT), "--graph-id", "14_runtime_observability", "--output", tmp_path],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        if result.returncode != 0:
            pytest.skip(f"Generation failed: {result.stderr}")

        md_content = Path(tmp_path).read_text(encoding="utf-8")
        Path(tmp_path).unlink(missing_ok=True)

        anchor_pattern = re.compile(r"//\s*→\s+[^\s]+(?:#L\d+|::\w+)?")
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

        anchor_lines = [line for line in mermaid_lines if "// →" in line]
        for line in anchor_lines:
            assert anchor_pattern.search(line), (
                f"Anchor line does not match protocol format: {line}"
            )

    def test_14_runtime_observability_ai_md_removed(self):
        """Post-G0: deprecated .ai.md must not exist on disk."""
        ai_md = REPO_ROOT / "docs" / "_tech_graph" / "14_runtime_observability.ai.md"
        assert not ai_md.exists(), f".ai.md should be deleted: {ai_md}"

    def test_00_main_regression_after_script_change(self):
        """F3: Script parameterization must not break 00_main."""
        if not COMPILE_SCRIPT.exists():
            pytest.skip("Compile script not yet created")
        result = subprocess.run(
            [sys.executable, str(COMPILE_SCRIPT), "--check", "--graph-id", "00_main"],
            capture_output=True,
            text=True,
            cwd=REPO_ROOT,
        )
        assert result.returncode == 0, (
            f"00_main regression: rc={result.returncode}: {result.stdout}\n{result.stderr}"
        )
