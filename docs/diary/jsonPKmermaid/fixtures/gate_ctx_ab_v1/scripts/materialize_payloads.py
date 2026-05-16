#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 2：物化 gate_ctx_ab_v1 两分支主载荷（不调用 LLM）。

- CTX_JSON：复制 graph.json（禁止夹带 *.ai.md 正文）
- CTX_MERMAID：按 tech_graph_token_estimate.collect_mermaid_corpus 拼接（禁止夹带 graph.json）
- 共享附件：_manifest.json、_contract_manifest.json
"""

from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]  # …/ai-ink-brain-api-python
FIXTURE_ROOT = _REPO.parents[1]  # …/gate_ctx_ab_v1
PAYLOADS = FIXTURE_ROOT / "payloads"
TECH_GRAPH = REPO_ROOT / "docs" / "_tech_graph"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tech_graph_token_estimate import (  # noqa: E402
    _iter_ai_md_files,
    _repo_rel_posix,
    collect_mermaid_corpus,
    measure,
)


def _copy(src: Path, dst: Path) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def main() -> int:
    graph_src = TECH_GRAPH / "graph.json"
    manifest_src = TECH_GRAPH / "_manifest.json"
    contract_src = TECH_GRAPH / "_contract_manifest.json"

    for p in (graph_src, manifest_src, contract_src):
        if not p.is_file():
            print(f"缺少文件：{p}", file=sys.stderr)
            return 2

    shared = PAYLOADS / "_shared"
    arm_json = PAYLOADS / "CTX_JSON"
    arm_mmd = PAYLOADS / "CTX_MERMAID"

    # 共享附件
    _copy(manifest_src, shared / "_manifest.json")
    _copy(contract_src, shared / "_contract_manifest.json")

    # CTX_JSON：仅 graph.json
    _copy(graph_src, arm_json / "main.graph.json")

    # CTX_MERMAID：仅 Mermaid 语料总串
    corpus = collect_mermaid_corpus(TECH_GRAPH)
    arm_mmd.mkdir(parents=True, exist_ok=True)
    (arm_mmd / "main.mermaid_corpus.txt").write_text(corpus, encoding="utf-8")

    sources = [_repo_rel_posix(p) for p in _iter_ai_md_files(TECH_GRAPH)]
    (arm_mmd / "source_ai_md_files.json").write_text(
        json.dumps({"files": sources}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    a_text = graph_src.read_text(encoding="utf-8")
    ma = measure("A", a_text)
    mb = measure("B", corpus)

    report = {
        "schema": "gate_ctx_ab_payload_materialize_v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "repo_root": _repo_rel_posix(REPO_ROOT),
        "freeze_id": "TECH_GRAPH_S1_FREEZE_20260514_V1_1_3",
        "paths": {
            "CTX_JSON_main": _repo_rel_posix(arm_json / "main.graph.json"),
            "CTX_MERMAID_main": _repo_rel_posix(arm_mmd / "main.mermaid_corpus.txt"),
            "attachments": _repo_rel_posix(shared),
        },
        "forbidden_checks": {
            "CTX_JSON_has_no_ai_md": True,
            "CTX_MERMAID_has_no_graph_json": not (arm_mmd / "main.graph.json").exists(),
        },
        "stats": {
            "A_graph_json": {k: v for k, v in ma.items() if k != "label"},
            "B_mermaid_corpus": {k: v for k, v in mb.items() if k != "label"},
            "source_ai_md_count": len(sources),
        },
    }
    (PAYLOADS / "materialize_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(json.dumps(report["stats"], ensure_ascii=False))
    print(f"OK: payloads -> {_repo_rel_posix(PAYLOADS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
