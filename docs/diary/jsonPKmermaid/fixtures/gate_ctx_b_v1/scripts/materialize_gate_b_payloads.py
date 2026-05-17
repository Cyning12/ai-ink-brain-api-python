#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闸口 B：物化 CTX_QUERY 主载荷（v2 graph_query 子图 + 元数据）；统计三臂静态 token。"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]
GATE_A_PAYLOADS = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/payloads"
QUERY_OUT = FIXTURE_ROOT / "payloads" / "CTX_QUERY"
SEEDS_PATH = FIXTURE_ROOT / "query_seeds.json"
GRAPH_PATH = REPO_ROOT / "docs/_tech_graph/graph.json"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tech_graph_token_estimate import measure  # noqa: E402


def _repo_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _run_query(node_id: str, op: str, depth: int) -> dict:
    cmd = [
        sys.executable,
        str(REPO_ROOT / "tools/tech_graph_graph_query.py"),
        "--graph",
        str(GRAPH_PATH),
        op,
        node_id,
        str(depth),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        raise RuntimeError(f"graph_query failed ({proc.returncode}): {proc.stderr}")
    return json.loads(proc.stdout)


def main() -> int:
    seeds_doc = json.loads(SEEDS_PATH.read_text(encoding="utf-8"))
    default_op = seeds_doc.get("default_op", "downstream")
    default_depth = int(seeds_doc.get("default_depth", 2))
    freeze_id = seeds_doc.get("freeze_id", "")

    QUERY_OUT.mkdir(parents=True, exist_ok=True)
    per_task: dict[str, dict] = {}

    for task_id, spec in seeds_doc["tasks"].items():
        node_id = spec["node_id"]
        op = spec.get("op", default_op)
        depth = int(spec.get("depth", default_depth))
        subgraph = _run_query(node_id, op, depth)
        payload = {
            "schema": "gate_ctx_b_ctx_query_main_v1",
            "arm": "CTX_QUERY",
            "task_id": task_id,
            "freeze_id": freeze_id,
            "query": {"op": op, "node_id": node_id, "depth": depth},
            "subgraph": subgraph,
            "note": "非整包 graph_v2；仅 query 子图 + 附件 manifest/contract",
        }
        out_path = QUERY_OUT / f"{task_id}.subgraph.json"
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        out_path.write_text(text, encoding="utf-8")
        m = measure(f"CTX_QUERY_{task_id}", text)
        per_task[task_id] = {
            "path": _repo_rel(out_path),
            "node_id": node_id,
            "op": op,
            "depth": depth,
            "nodes": len(subgraph.get("nodes") or []),
            "edges": len(subgraph.get("edges") or []),
            "bytes_utf8": m["bytes_utf8"],
            "heuristic_tokens": m["heuristic_tokens"],
        }

    # 静态对照：A/B 沿用闸口 A 物化报告
    gate_a_report_path = GATE_A_PAYLOADS / "materialize_report.json"
    gate_a_stats = {}
    if gate_a_report_path.is_file():
        gate_a_stats = json.loads(gate_a_report_path.read_text(encoding="utf-8")).get(
            "stats", {}
        )

    report = {
        "schema": "gate_ctx_b_payload_materialize_v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "freeze_id": freeze_id,
        "graph_v2_path": _repo_rel(GRAPH_PATH),
        "arms_static": {
            "CTX_MERMAID": gate_a_stats.get("B_mermaid_corpus", {}),
            "CTX_JSON": gate_a_stats.get("A_graph_json", {}),
            "CTX_QUERY": {
                "per_task": per_task,
                "heuristic_tokens_median": sorted(
                    t["heuristic_tokens"] for t in per_task.values()
                )[len(per_task) // 2]
                if per_task
                else 0,
            },
        },
        "forbidden_checks": {
            "CTX_QUERY_not_whole_graph_v2": all(
                t["heuristic_tokens"] < 5000 for t in per_task.values()
            ),
            "CTX_QUERY_uses_graph_query_cli": True,
        },
    }
    report_path = FIXTURE_ROOT / "payloads" / "materialize_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report["arms_static"], ensure_ascii=False, indent=2))
    print(f"OK: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
