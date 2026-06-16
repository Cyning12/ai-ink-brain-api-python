#!/usr/bin/env python3
"""Compile <graph_id>.graph.yaml → <graph_id>.md (Mermaid + structured tables).

Usage:
    python scripts/graph_yaml_compile.py                          # Generate 00_main.md (default)
    python scripts/graph_yaml_compile.py --graph-id 10_flow_rag   # Generate 10_flow_rag.md
    python scripts/graph_yaml_compile.py --all                    # Generate all .graph.yaml
    python scripts/graph_yaml_compile.py --check                  # Diff 00_main vs graph.json
    python scripts/graph_yaml_compile.py --check --graph-id 10_flow_rag
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
TECH_GRAPH_DIR = REPO_ROOT / "docs" / "_tech_graph"
GRAPH_JSON_PATH = TECH_GRAPH_DIR / "graph.json"


def yaml_path_for(graph_id: str) -> Path:
    return TECH_GRAPH_DIR / f"{graph_id}.graph.yaml"


def md_path_for(graph_id: str) -> Path:
    return TECH_GRAPH_DIR / f"{graph_id}.md"


def load_yaml(graph_id: str):
    path = yaml_path_for(graph_id)
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_graph_json():
    with GRAPH_JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def extract_graph_json_slice(graph_id: str):
    data = load_graph_json()
    nodes = [n for n in data.get("nodes", []) if n.get("graph_id") == graph_id]
    edges = [
        e
        for e in data.get("edges", [])
        if e.get("graph_id") == graph_id and "from" in e and "to" in e
    ]
    return nodes, edges


def format_anchor_comment(anchor: dict) -> str:
    """Format anchor as Mermaid comment per 99_mermaid_protocol.md §3.

    Returns empty string if anchor lacks path.
    """
    path = anchor.get("path", "")
    symbol = anchor.get("symbol", "")
    line = anchor.get("line")
    if not path:
        return ""
    if line is not None:
        return f"// → {path}#L{line}"
    if symbol:
        return f"// → {path}::{symbol}"
    return f"// → {path}"


def generate_mermaid(data: dict) -> str:
    nodes = {n["id"]: n for n in data.get("nodes", [])}
    edges = data.get("edges", [])
    direction = data.get("direction", "TD")

    lines = [f"flowchart {direction}"]

    # Render nodes with shapes based on heuristic
    for nid, node in nodes.items():
        label = node.get("label", nid)
        # Heuristic shapes
        if label.startswith(">"):
            shape = f"[{label}]"
        elif "子流程" in label or label.endswith("子流程"):
            shape = f"[[{label}]]"
        elif nid in ("Q", "E"):
            shape = f"[[{label}]]"
        elif "DOC" in nid:
            shape = f"[>{label}]"
        else:
            shape = f"[{label}]"
        lines.append(f"    {nid}{shape}")

    lines.append("")

    # Render edges
    for e in edges:
        src = e["from"]
        dst = e["to"]
        mark = e.get("mark", "->")
        label = e.get("label", "")
        anchors = e.get("anchors", [])

        if label:
            edge_line = f'    {src} --"{label}"--> {dst}'
        elif mark and mark != "->":
            edge_line = f'    {src} --"{mark}"--> {dst}'
        else:
            edge_line = f"    {src} --> {dst}"

        lines.append(edge_line)

        for anchor in anchors:
            comment = format_anchor_comment(anchor)
            if comment:
                lines.append(f"    {comment}")

    lines.append("")

    # Style classes (minimal)
    lines.append("    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px")
    lines.append("    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px")
    lines.append("    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px")

    phase_nodes = [n for n in nodes if n in ("Q", "E", "U1", "U2", "RAG", "T2S", "RPC", "FTS")]
    doc_nodes = [n for n in nodes if "DOC" in n]
    infra_nodes = [n for n in nodes if n in ("AUTH", "EV_TYPES")]

    if phase_nodes:
        lines.append(f"    class {','.join(phase_nodes)} phase")
    if doc_nodes:
        lines.append(f"    class {','.join(doc_nodes)} doc")
    if infra_nodes:
        lines.append(f"    class {','.join(infra_nodes)} infra")

    return "\n".join(lines)


def generate_node_table(data: dict) -> str:
    lines = ["### Nodes", "", "| ID | Label | Kind |", "|----|-------|------|"]
    for n in data.get("nodes", []):
        nid = n.get("id", "")
        label = n.get("label", "").replace("|", "\\|")
        kind = n.get("kind", "") or ""
        lines.append(f"| {nid} | {label} | {kind} |")
    return "\n".join(lines)


def generate_edge_table(data: dict) -> str:
    lines = [
        "### Edges",
        "",
        "| From | To | Mark | Type | Label | Anchors |",
        "|------|----|------|------|-------|---------|",
    ]
    for e in data.get("edges", []):
        src = e.get("from", "")
        dst = e.get("to", "")
        mark = e.get("mark", "->")
        etype = e.get("type", "depends_on")
        label = e.get("label", "").replace("|", "\\|")
        anchors = e.get("anchors", [])
        anchor_summary = f"{len(anchors)} anchor(s)" if anchors else ""
        lines.append(f"| {src} | {dst} | {mark} | {etype} | {label} | {anchor_summary} |")
    return "\n".join(lines)


def generate_sub_graph_links(graph_id: str) -> str:
    """Return sub-graph links section; only 00_main gets the full hub."""
    if graph_id != "00_main":
        return ""
    return """## Sub-graph Links

- `Struct`: [`01_struct.md`](01_struct.md)
- `Version`: [`02_version.md`](02_version.md)
- `RAG Flow`: [`10_flow_rag.md`](10_flow_rag.md)（[AI 协议版](10_flow_rag.ai.md)）
- `Text2SQL Flow`: [`11_flow_text2sql.md`](11_flow_text2sql.md)（[AI 协议版](11_flow_text2sql.ai.md)）
- `FTS Flow`: [`12_flow_fts.md`](12_flow_fts.md)（[AI 协议版](12_flow_fts.ai.md)）
- `Supabase RPC`: [`13_flow_supabase_rpc.md`](13_flow_supabase_rpc.md)（[AI 协议版](13_flow_supabase_rpc.ai.md)）
- `Runtime/Observability`: [`14_runtime_observability.md`](14_runtime_observability.md)（[AI 协议版](14_runtime_observability.ai.md)）
- `E2E Boundary/Contract`: [`15_e2e_boundary.md`](15_e2e_boundary.md)（[AI 协议版](15_e2e_boundary.ai.md)）
- `Spec`: [`99_spec.md`](99_spec.md)
- `Mermaid Protocol`: [`99_mermaid_protocol.md`](99_mermaid_protocol.md) — 拓扑图绘制规范（Python/FastAPI 适配版）

> **P0 决策备忘**：`00_main.md` 不嵌入 `AUTO:ENDPOINTS_AND_ANCHORS` 块（保持人类友好）；`_manifest.json` 仍由现有工具维护。
"""


def generate_notes_section(data: dict) -> str:
    """Render optional `notes` field as markdown section."""
    notes = data.get("notes")
    if not notes:
        return ""
    if isinstance(notes, str):
        body = notes
    elif isinstance(notes, list):
        body = "\n\n".join(str(n) for n in notes)
    else:
        body = str(notes)
    return f"\n\n## Notes\n\n{body}\n"


def generate_md(data: dict) -> str:
    graph_id = data.get("graph_id", "00_main")
    title = data.get("title", graph_id)
    description = data.get("description", "")
    version = data.get("version", "")
    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    frontmatter = f"""---
graph_id: {graph_id}
version: {version}
generated_at: {generated_at}
source: docs/_tech_graph/{graph_id}.graph.yaml
---
"""

    header = f"# {title}\n\n{description}".strip()

    mermaid = generate_mermaid(data)

    sub_graph_links = generate_sub_graph_links(graph_id)
    sub_graph_section = f"\n\n{sub_graph_links}" if sub_graph_links else ""

    notes_section = generate_notes_section(data)

    body = f"""{header}

## Mermaid

```mermaid
{mermaid}
```

## Structured Data

{generate_node_table(data)}

{generate_edge_table(data)}{notes_section}{sub_graph_section}
"""
    return frontmatter + "\n" + body


def diff_check(graph_id: str) -> tuple[bool, str]:
    """Return (ok, diff_text)."""
    yaml_data = load_yaml(graph_id)
    json_nodes, json_edges = extract_graph_json_slice(graph_id)

    yaml_nodes = {n["id"]: n for n in yaml_data.get("nodes", [])}
    yaml_node_ids = set(yaml_nodes.keys())
    json_node_ids = {n["id"] for n in json_nodes}

    diffs = []

    if yaml_node_ids != json_node_ids:
        only_yaml = yaml_node_ids - json_node_ids
        only_json = json_node_ids - yaml_node_ids
        if only_yaml:
            diffs.append(f"Nodes only in YAML: {sorted(only_yaml)}")
        if only_json:
            diffs.append(f"Nodes only in JSON: {sorted(only_json)}")

    if len(yaml_data.get("nodes", [])) != len(json_nodes):
        diffs.append(
            f"Node count mismatch: YAML={len(yaml_data.get('nodes', []))}, JSON={len(json_nodes)}"
        )

    yaml_edge_set = {
        (e["from"], e["to"], e.get("mark", "->"), e.get("type", "depends_on"))
        for e in yaml_data.get("edges", [])
    }
    json_edge_set = {
        (e["from"], e["to"], e.get("mark", "->"), e.get("type", "depends_on"))
        for e in json_edges
    }

    if yaml_edge_set != json_edge_set:
        only_yaml = yaml_edge_set - json_edge_set
        only_json = json_edge_set - yaml_edge_set
        if only_yaml:
            diffs.append(f"Edges only in YAML: {sorted(only_yaml)}")
        if only_json:
            diffs.append(f"Edges only in JSON: {sorted(only_json)}")

    if len(yaml_data.get("edges", [])) != len(json_edges):
        diffs.append(
            f"Edge count mismatch: YAML={len(yaml_data.get('edges', []))}, JSON={len(json_edges)}"
        )

    # Anchor check
    yaml_edges_by_key = {
        (e["from"], e["to"]): e for e in yaml_data.get("edges", [])
    }
    json_edges_by_key = {
        (e["from"], e["to"]): e for e in json_edges
    }
    for key in set(yaml_edges_by_key.keys()) & set(json_edges_by_key.keys()):
        ya = yaml_edges_by_key[key].get("anchors", [])
        ja = json_edges_by_key[key].get("anchors", [])
        if len(ya) != len(ja):
            diffs.append(f"Anchor count mismatch for {key}: YAML={len(ya)}, JSON={len(ja)}")

    if diffs:
        return False, "\n".join(diffs)
    return True, ""


def compile_graph(graph_id: str, output: Path | None = None) -> None:
    data = load_yaml(graph_id)
    md = generate_md(data)
    out_path = output if output else md_path_for(graph_id)
    out_path.write_text(md, encoding="utf-8")
    print(f"Generated: {out_path}")


def check_graph(graph_id: str) -> bool:
    ok, diff_text = diff_check(graph_id)
    if ok:
        print(f"OK: YAML matches graph.json {graph_id} slice")
        return True
    print(f"ERROR: Diff detected for {graph_id}:", file=sys.stderr)
    print(diff_text, file=sys.stderr)
    return False


def all_graph_ids() -> list[str]:
    return sorted(p.name[: -len(".graph.yaml")] for p in TECH_GRAPH_DIR.glob("*.graph.yaml"))


def main():
    parser = argparse.ArgumentParser(description="Compile <graph_id>.graph.yaml to <graph_id>.md")
    parser.add_argument("--graph-id", default="00_main", help="Graph ID to compile (default: 00_main)")
    parser.add_argument("--all", action="store_true", help="Compile all *.graph.yaml files")
    parser.add_argument("--check", action="store_true", help="Diff YAML against graph.json")
    parser.add_argument("--output", type=Path, default=None, help="Output MD path (single graph only)")
    args = parser.parse_args()

    if args.all:
        if args.output:
            print("ERROR: --output cannot be used with --all", file=sys.stderr)
            sys.exit(2)
        graph_ids = all_graph_ids()
        failed = False
        for graph_id in graph_ids:
            if args.check:
                if not check_graph(graph_id):
                    failed = True
            else:
                compile_graph(graph_id)
        sys.exit(1 if failed else 0)

    graph_id = args.graph_id
    yaml_path = yaml_path_for(graph_id)
    if not yaml_path.exists():
        print(f"ERROR: YAML source not found: {yaml_path}", file=sys.stderr)
        sys.exit(1)

    if args.check:
        ok = check_graph(graph_id)
        sys.exit(0 if ok else 1)

    compile_graph(graph_id, output=args.output)


if __name__ == "__main__":
    main()
