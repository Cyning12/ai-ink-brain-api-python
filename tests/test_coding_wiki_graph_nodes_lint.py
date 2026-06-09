from __future__ import annotations

from pathlib import Path

from tools.coding_wiki_graph_nodes_lint import (
    DEFAULT_SYNTH_DIR,
    lint_markdown_file,
    lint_paths,
    main,
)
from tools.tech_graph_graph_query import DEFAULT_GRAPH, load_graph_v2


def _write_synthesis(tmp_path: Path, name: str, body: str) -> Path:
    p = tmp_path / name
    p.write_text(body, encoding="utf-8")
    return p


class TestInvalidNodeId:
    def test_unknown_graph_node_id_fails(self, tmp_path: Path) -> None:
        md = _write_synthesis(
            tmp_path,
            "bad-slug.md",
            """---
title: Bad
slug: bad-slug
layer: L2
status: compiled
graph_nodes:
  - id: __NOT_A_REAL_NODE_ID__
    relation: documents
---

# Bad
""",
        )
        store = load_graph_v2(DEFAULT_GRAPH)
        findings = lint_markdown_file(md, store=store)
        assert findings
        assert any("无效" in f.message or "FP-4" in f.message for f in findings)

    def test_cli_unknown_id_exit_1(self, tmp_path: Path) -> None:
        md = _write_synthesis(
            tmp_path,
            "bad-cli.md",
            """---
title: Bad CLI
slug: bad-cli
layer: L2
status: compiled
graph_nodes:
  - id: __NOT_A_REAL_NODE_ID__
    relation: documents
---

# Bad CLI
""",
        )
        rc = main([str(md)])
        assert rc == 1


class TestValidCases:
    def test_empty_graph_nodes_passes(self, tmp_path: Path) -> None:
        md = _write_synthesis(
            tmp_path,
            "empty-nodes.md",
            """---
title: Empty
slug: empty-nodes
layer: L2
status: compiled
graph_nodes: []
---

# Empty
""",
        )
        store = load_graph_v2(DEFAULT_GRAPH)
        findings = lint_markdown_file(md, store=store)
        assert not findings

    def test_missing_key_fails_by_default(self, tmp_path: Path) -> None:
        md = _write_synthesis(
            tmp_path,
            "missing-key.md",
            """---
title: Missing
slug: missing-key
layer: L2
status: compiled
---

# Missing
""",
        )
        store = load_graph_v2(DEFAULT_GRAPH)
        findings = lint_markdown_file(md, store=store, require_key=True)
        assert any("缺少 graph_nodes" in f.message for f in findings)

    def test_known_node_id_passes(self, tmp_path: Path) -> None:
        md = _write_synthesis(
            tmp_path,
            "good-node.md",
            """---
title: Good
slug: good-node
layer: L2
status: compiled
graph_nodes:
  - id: C1
    relation: documents
---

# Good
""",
        )
        store = load_graph_v2(DEFAULT_GRAPH)
        findings = lint_markdown_file(md, store=store)
        assert not findings


class TestProductionSmoke:
    def test_main_syntheses_tree_exit_0(self) -> None:
        rc = main(["--root", str(DEFAULT_SYNTH_DIR)])
        assert rc == 0

    def test_production_tree_no_findings(self) -> None:
        paths = sorted(DEFAULT_SYNTH_DIR.glob("*.md"))
        report = lint_paths(paths)
        assert report.ok, report.findings
