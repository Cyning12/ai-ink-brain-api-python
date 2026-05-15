from __future__ import annotations

import json
from pathlib import Path

from tools.tech_graph_token_estimate import collect_mermaid_corpus, measure


def test_measure_heuristic(tmp_path: Path) -> None:
    m = measure("x", "abcd")
    assert m["chars"] == 4
    assert m["heuristic_tokens"] == 1  # max(1, 4//4)


def test_collect_mermaid_two_files(tmp_path: Path) -> None:
    d = tmp_path / "docs" / "_tech_graph"
    d.mkdir(parents=True)
    (d / "a.ai.md").write_text(
        "```mermaid\nflowchart TD\n  A --> B\n```\n",
        encoding="utf-8",
    )
    (d / "b.ai.md").write_text(
        "```mermaid\nflowchart LR\n  X --> Y\n```\n",
        encoding="utf-8",
    )
    corpus = collect_mermaid_corpus(d)
    assert "A --> B" in corpus and "X --> Y" in corpus


def test_main_json_smoke(tmp_path: Path) -> None:
    from tools import tech_graph_token_estimate as mod

    d = tmp_path / "in"
    d.mkdir()
    (d / "z.ai.md").write_text(
        "```mermaid\nflowchart TD\n  A --\"->\"--> B\n```\n",
        encoding="utf-8",
    )
    g = tmp_path / "graph.json"
    g.write_text(
        json.dumps({"nodes": ["A", "B"], "edges": []}, ensure_ascii=False),
        encoding="utf-8",
    )
    assert mod.main(["--input", str(d), "--graph-json", str(g), "--json"]) == 0
