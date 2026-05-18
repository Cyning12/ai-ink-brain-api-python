#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闸口 C：物化 CTX_V2_QUERY（子图）与 CTX_DUAL_MD（精选双轨原文）主载荷。"""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]
GRAPH_PATH = REPO_ROOT / "docs/_tech_graph/graph.json"
SEEDS_PATH = FIXTURE_ROOT / "query_seeds.json"
MANIFEST_PATH = FIXTURE_ROOT / "dual_track_manifest.json"
PROTOCOL_PATH = FIXTURE_ROOT / "protocol_version.yaml"
QUERY_OUT = FIXTURE_ROOT / "payloads" / "CTX_V2_QUERY"
DUAL_OUT = FIXTURE_ROOT / "payloads" / "CTX_DUAL_MD"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.tech_graph_token_estimate import measure  # noqa: E402

EXIT_FP3 = 4
EXIT_TOKEN_LIMIT = 5
EXIT_MANIFEST = 2


def _repo_rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _load_protocol_limits() -> tuple[int, int]:
    import yaml

    doc = yaml.safe_load(PROTOCOL_PATH.read_text(encoding="utf-8"))
    limits = doc.get("payload_limits") or {}
    per_arm = int(limits.get("max_heuristic_tokens_per_task_arm", 8192))
    mermaid_baseline = int(limits.get("d_arm_nodes_lt_whole_mermaid_heuristic_tokens", 5026))
    return per_arm, mermaid_baseline


def _run_query(node_id: str, op: str, depth: int) -> dict | str:
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
    if proc.returncode == EXIT_FP3:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(EXIT_FP3)
    if proc.returncode != 0:
        raise RuntimeError(f"graph_query failed ({proc.returncode}): {proc.stderr}")
    if op == "describe-impact":
        return proc.stdout
    return json.loads(proc.stdout)


def _materialize_dual_track(
    task_id: str,
    spec: dict,
    freeze_id: str,
    max_tokens: int,
) -> dict:
    parts: list[str] = []
    file_meta: list[dict] = []
    for track in spec["tracks"]:
        rel = track["path"]
        path = REPO_ROOT / rel
        if not path.is_file():
            print(f"FP-C-2: missing path {rel}", file=sys.stderr)
            raise SystemExit(EXIT_MANIFEST)
        text = path.read_text(encoding="utf-8")
        role = track.get("role", "ai")
        parts.append(f"<!-- gate_ctx_c dual_track role={role} path={rel} -->\n{text.rstrip()}\n")
        file_meta.append({"role": role, "path": rel, "bytes_utf8": len(text.encode("utf-8"))})

    body = "\n---\n".join(parts) + "\n"
    m = measure(f"CTX_DUAL_MD_{task_id}", body)
    if m["heuristic_tokens"] > max_tokens:
        print(
            f"FP-C-4: {task_id} CTX_DUAL_MD tokens {m['heuristic_tokens']} > {max_tokens}",
            file=sys.stderr,
        )
        raise SystemExit(EXIT_TOKEN_LIMIT)

    out_path = DUAL_OUT / f"{task_id}.dual_track.md"
    header = (
        f"---\n"
        f"schema: gate_ctx_c_dual_md_main_v1\n"
        f"arm: CTX_DUAL_MD\n"
        f"task_id: {task_id}\n"
        f"freeze_id: {freeze_id}\n"
        f"---\n\n"
    )
    out_path.write_text(header + body, encoding="utf-8")
    return {
        "path": _repo_rel(out_path),
        "files": file_meta,
        "bytes_utf8": m["bytes_utf8"],
        "heuristic_tokens": m["heuristic_tokens"],
    }


def main() -> int:
    per_arm_limit, mermaid_baseline = _load_protocol_limits()
    seeds_doc = json.loads(SEEDS_PATH.read_text(encoding="utf-8"))
    manifest_doc = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    default_op = seeds_doc.get("default_op", "downstream")
    default_depth = int(seeds_doc.get("default_depth", 2))
    freeze_id = seeds_doc.get("freeze_id", "")
    manifest_max = int(manifest_doc.get("max_heuristic_tokens_per_task", per_arm_limit))

    QUERY_OUT.mkdir(parents=True, exist_ok=True)
    DUAL_OUT.mkdir(parents=True, exist_ok=True)

    per_task_d: dict[str, dict] = {}
    per_task_e: dict[str, dict] = {}

    for task_id, spec in seeds_doc["tasks"].items():
        node_id = spec["node_id"]
        op = spec.get("op", default_op)
        depth = int(spec.get("depth", default_depth))
        query_result = _run_query(node_id, op, depth)
        if isinstance(query_result, str):
            payload = {
                "schema": "gate_ctx_c_v2_query_main_v1",
                "arm": "CTX_V2_QUERY",
                "task_id": task_id,
                "freeze_id": freeze_id,
                "query": {"op": op, "node_id": node_id, "depth": depth},
                "describe_impact_text": query_result,
            }
            node_count = 0
        else:
            subgraph = query_result
            payload = {
                "schema": "gate_ctx_c_v2_query_main_v1",
                "arm": "CTX_V2_QUERY",
                "task_id": task_id,
                "freeze_id": freeze_id,
                "query": {"op": op, "node_id": node_id, "depth": depth},
                "subgraph": subgraph,
                "note": "graph_v2 子图；ref 边不参与 BFS",
            }
            node_count = len(subgraph.get("nodes") or [])
        out_path = QUERY_OUT / f"{task_id}.subgraph.json"
        text = json.dumps(payload, ensure_ascii=False, indent=2) + "\n"
        out_path.write_text(text, encoding="utf-8")
        m = measure(f"CTX_V2_QUERY_{task_id}", text)
        if m["heuristic_tokens"] > per_arm_limit:
            print(
                f"FP-C-4: {task_id} CTX_V2_QUERY tokens {m['heuristic_tokens']} > {per_arm_limit}",
                file=sys.stderr,
            )
            return EXIT_TOKEN_LIMIT
        per_task_d[task_id] = {
            "path": _repo_rel(out_path),
            "node_id": node_id,
            "op": op,
            "depth": depth,
            "nodes": node_count,
            "bytes_utf8": m["bytes_utf8"],
            "heuristic_tokens": m["heuristic_tokens"],
        }

    dual_tasks = manifest_doc.get("tasks") or {}
    ai_md_whole_count = len(
        [
            p
            for p in (REPO_ROOT / "docs/_tech_graph").glob("*.ai.md")
            if not p.name.startswith("99_")
        ]
    )
    selected_ai_count = sum(
        1
        for spec in dual_tasks.values()
        for t in spec.get("tracks", [])
        if t.get("path", "").endswith(".ai.md")
    )

    for task_id, spec in dual_tasks.items():
        e_limit = min(per_arm_limit, manifest_max)
        per_task_e[task_id] = _materialize_dual_track(task_id, spec, freeze_id, e_limit)

    d_below_mermaid = all(
        t["heuristic_tokens"] < mermaid_baseline for t in per_task_d.values()
    )
    dual_not_whole = selected_ai_count < ai_md_whole_count

    report = {
        "schema": "gate_ctx_c_payload_materialize_v1",
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "freeze_id": freeze_id,
        "graph_v2_path": _repo_rel(GRAPH_PATH),
        "graph_v2_freeze_id": seeds_doc.get("graph_v2_freeze_id"),
        "arms_static": {
            "CTX_V2_QUERY": {
                "per_task": per_task_d,
                "heuristic_tokens_median": sorted(
                    t["heuristic_tokens"] for t in per_task_d.values()
                )[len(per_task_d) // 2]
                if per_task_d
                else 0,
            },
            "CTX_DUAL_MD": {
                "per_task": per_task_e,
                "heuristic_tokens_median": sorted(
                    t["heuristic_tokens"] for t in per_task_e.values()
                )[len(per_task_e) // 2]
                if per_task_e
                else 0,
                "selected_ai_md_count": selected_ai_count,
                "repo_ai_md_count": ai_md_whole_count,
            },
        },
        "forbidden_checks": {
            "CTX_V2_QUERY_subgraph_below_mermaid_baseline": d_below_mermaid,
            "CTX_V2_QUERY_uses_graph_query_cli": True,
            "CTX_DUAL_MD_not_whole_corpus": dual_not_whole,
        },
    }
    report_path = FIXTURE_ROOT / "payloads" / "materialize_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(report["arms_static"], ensure_ascii=False, indent=2))
    print(f"OK: {report_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
