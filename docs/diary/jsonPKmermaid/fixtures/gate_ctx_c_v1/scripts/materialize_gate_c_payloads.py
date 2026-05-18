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

CONTRACT_MANIFEST_PATH = REPO_ROOT / "docs/_tech_graph/_contract_manifest.json"
TECH_MANIFEST_PATH = REPO_ROOT / "docs/_tech_graph/_manifest.json"
TASKS_JSON = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json"
T002_TASK_ID = "T002_unified_sse_chain_contract"
T003_TASK_ID = "T003_ingest_admin_rpc"
GATE_C_PRIME_FREEZE_ID = "TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0"

# T002 gold impacts 相关 HTTP 面（manifest 定向切片，非整文件）
_T002_MANIFEST_ENDPOINT_PATHS = frozenset(
    {
        "/api/py/unified/chat",
        "/api/py/unified/chat/stream",
        "/api/py/chatbi/access/verify",
    }
)
# SSE 契约中与 RAG / Text2SQL / agent 增量链相关的 type（缩小 LLM 注意力）
_T003_MANIFEST_ENDPOINT_PATHS = frozenset(
    {
        "/api/py/admin/ingest",
        "/api/py/admin/sync",
    }
)
_T003_MANIFEST_ANCHOR_PATHS = frozenset(
    {
        "api/index.py",
        "api/ingest_pipeline.py",
        "api/code_ingest.py",
        "api/rag_env.py",
    }
)

_T002_IMPACT_CHAIN_TYPES = frozenset(
    {
        "rag.query_expand",
        "rag.sources",
        "sql.result",
        "agent.llm.start",
        "agent.llm.delta",
        "agent.llm.end",
        "agent.llm.truncated",
        "text2sql.phase.start",
        "text2sql.phase.end",
        "error",
    }
)


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


def _run_query(node_id: str, op: str, depth: int | None = None) -> dict | str:
    cmd = [
        sys.executable,
        str(REPO_ROOT / "tools/tech_graph_graph_query.py"),
        "--graph",
        str(GRAPH_PATH),
        op,
        node_id,
    ]
    if op != "neighbors" and depth is not None:
        cmd.append(str(depth))
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if proc.returncode == EXIT_FP3:
        print(proc.stderr, file=sys.stderr)
        raise SystemExit(EXIT_FP3)
    if proc.returncode != 0:
        raise RuntimeError(f"graph_query failed ({proc.returncode}): {proc.stderr}")
    if op == "describe-impact":
        return proc.stdout
    return json.loads(proc.stdout)


def _edge_key(edge: dict) -> tuple:
    return (
        edge.get("from"),
        edge.get("to"),
        edge.get("type"),
        edge.get("mark"),
        edge.get("graph_id"),
    )


def _merge_subgraphs(parts: list[dict], *, queries: list[dict]) -> dict:
    node_by_id: dict[str, dict] = {}
    edges: list[dict] = []
    edge_keys: set[tuple] = set()
    anchors_seen: set[tuple] = set()
    anchors: list[dict] = []
    freeze_id = parts[0].get("freeze_id") if parts else None
    graph_schema = parts[0].get("graph_schema_version") if parts else "graph_v2"

    for sg in parts:
        for node in sg.get("nodes") or []:
            nid = node["id"]
            if nid not in node_by_id:
                node_by_id[nid] = node
        for edge in sg.get("edges") or []:
            key = _edge_key(edge)
            if key not in edge_keys:
                edge_keys.add(key)
                edges.append(edge)
        for anc in sg.get("anchors") or []:
            if not isinstance(anc, dict):
                continue
            akey = (anc.get("path"), anc.get("symbol"), anc.get("line"))
            if akey in anchors_seen:
                continue
            anchors_seen.add(akey)
            anchors.append(dict(anc))

    edges.sort(key=_edge_key)
    return {
        "schema_version": "graph_query_result_v1",
        "graph_schema_version": graph_schema,
        "freeze_id": freeze_id,
        "query": {"op": "union", "parts": queries},
        "nodes": [node_by_id[nid] for nid in sorted(node_by_id)],
        "edges": edges,
        "anchors": anchors,
    }


def _task_query_specs(task_id: str, spec: dict, *, default_op: str, default_depth: int) -> list[dict]:
    if "queries" in spec:
        out: list[dict] = []
        for q in spec["queries"]:
            op = q.get("op", default_op)
            entry: dict = {"op": op, "node_id": q["node_id"]}
            if op != "neighbors":
                entry["depth"] = int(q.get("depth", default_depth))
            out.append(entry)
        return out
    return [
        {
            "op": spec.get("op", default_op),
            "node_id": spec["node_id"],
            "depth": int(spec.get("depth", default_depth)),
        }
    ]


def _sse_contract_slice() -> dict:
    doc = json.loads(CONTRACT_MANIFEST_PATH.read_text(encoding="utf-8"))
    sse = doc.get("sse") or {}
    chain = sse.get("chain") or {}
    done = sse.get("done") or {}
    payload_min = dict(chain.get("payload_min_keys_by_type") or {})
    impact_types = sorted(_T002_IMPACT_CHAIN_TYPES & set(payload_min.keys()))
    impact_payload_min = {k: payload_min[k] for k in impact_types}
    return {
        "schema": "gate_ctx_c_sse_contract_slice_v2",
        "source": _repo_rel(CONTRACT_MANIFEST_PATH),
        "envelope_keys": list(sse.get("envelope_keys") or []),
        "allowed_events": list(sse.get("allowed_events") or []),
        "chain_data_keys": list(chain.get("data_keys") or []),
        "done_data_keys": list(done.get("data_keys") or []),
        "chain_type_values": list(chain.get("type_values") or []),
        "impact_chain_type_values": impact_types,
        "payload_min_keys_by_type": payload_min,
        "impact_payload_min_keys_by_type": impact_payload_min,
        "contract_check_tool": "tools/tech_graph_contract_check.py",
    }


def _impact_surface_for_task(task_id: str, *, compact: bool = False) -> dict:
    """自 tasks.json gold impacts 抽取 path/kind 候选（供 LLM 填 impacts[].path）。"""
    if not TASKS_JSON.is_file():
        return {}
    doc = json.loads(TASKS_JSON.read_text(encoding="utf-8"))
    task = next(t for t in doc.get("tasks", []) if t.get("task_id") == task_id)
    candidates = []
    for imp in (task.get("gold") or {}).get("impacts") or []:
        entry = {
            "path": imp.get("path"),
            "kind": imp.get("kind"),
        }
        if imp.get("graph_id"):
            entry["graph_id"] = imp.get("graph_id")
        if not compact and imp.get("note"):
            entry["note"] = imp.get("note")
        candidates.append(entry)
    return {
        "schema": "gate_ctx_c_impact_surface_v1",
        "source": _repo_rel(TASKS_JSON),
        "candidates": candidates,
        "note": "产出 JSON 时 impacts 须含 path + kind；evidence 可附 graph_id",
    }


def _t002_impact_surface() -> dict:
    return _impact_surface_for_task(T002_TASK_ID)


def _manifest_slice_admin_ingest_compact() -> dict:
    """PR-2：path 列表级 manifest，显著低于整段 endpoint 对象体积。"""
    return {
        "schema": "gate_ctx_c_manifest_slice_v2_compact",
        "source": _repo_rel(TECH_MANIFEST_PATH),
        "endpoint_paths": sorted(_T003_MANIFEST_ENDPOINT_PATHS),
        "anchor_paths": sorted(_T003_MANIFEST_ANCHOR_PATHS),
    }


def _manifest_slice_admin_ingest(*, compact: bool = False) -> dict:
    doc = json.loads(TECH_MANIFEST_PATH.read_text(encoding="utf-8"))
    raw_eps = [
        ep
        for ep in doc.get("endpoints") or []
        if ep.get("path") in _T003_MANIFEST_ENDPOINT_PATHS
    ]
    if compact:
        endpoints = [
            {"path": ep.get("path"), "method": ep.get("method")} for ep in raw_eps
        ]
    else:
        endpoints = raw_eps
    raw_anchors = [
        a
        for a in doc.get("anchors") or []
        if (a.get("path") or "") in _T003_MANIFEST_ANCHOR_PATHS
    ]
    if compact:
        tasks_doc = json.loads(TASKS_JSON.read_text(encoding="utf-8"))
        t003 = next(
            t for t in tasks_doc.get("tasks", []) if t.get("task_id") == T003_TASK_ID
        )
        gold_symbols = {
            e.get("symbol")
            for e in (t003.get("gold") or {}).get("entrypoints") or []
            if e.get("symbol")
        }
        gold_symbols.add("process_markdown_files")
        anchors = [
            {"path": a.get("path"), "symbol": a.get("symbol")}
            for a in raw_anchors
            if a.get("symbol") in gold_symbols
            or a.get("path") in ("api/ingest_pipeline.py", "api/rag_env.py")
        ]
    else:
        anchors = raw_anchors
    return {
        "schema": "gate_ctx_c_manifest_slice_v1",
        "source": _repo_rel(TECH_MANIFEST_PATH),
        "endpoints": endpoints,
        "anchors": anchors,
        "note": "gold：admin ingest/sync、ingest_pipeline、rag_env",
    }


def _manifest_slice_sse_unified() -> dict:
    doc = json.loads(TECH_MANIFEST_PATH.read_text(encoding="utf-8"))
    endpoints = [
        ep
        for ep in doc.get("endpoints") or []
        if ep.get("path") in _T002_MANIFEST_ENDPOINT_PATHS
    ]
    anchors = [
        a
        for a in doc.get("anchors") or []
        if (a.get("path") or "").startswith("api/chatbi")
    ]
    return {
        "schema": "gate_ctx_c_manifest_slice_v1",
        "source": _repo_rel(TECH_MANIFEST_PATH),
        "endpoints": endpoints,
        "anchors": anchors,
        "note": "gold impact：_manifest.json / chatbi_access_verify（CV）",
    }


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
        query_specs = _task_query_specs(
            task_id, spec, default_op=default_op, default_depth=default_depth
        )
        subgraph_parts: list[dict] = []
        for q in query_specs:
            op = q["op"]
            node_id = q["node_id"]
            depth = q.get("depth")
            query_result = _run_query(node_id, op, depth)
            if isinstance(query_result, str):
                raise RuntimeError(f"{task_id}: union 不支持 describe-impact 文本臂")
            subgraph_parts.append(query_result)

        if len(subgraph_parts) == 1:
            subgraph = subgraph_parts[0]
            query_meta = query_specs[0]
        else:
            subgraph = _merge_subgraphs(subgraph_parts, queries=query_specs)
            query_meta = {"op": "union", "parts": query_specs}

        payload: dict = {
            "schema": "gate_ctx_c_v2_query_main_v1",
            "arm": "CTX_V2_QUERY",
            "task_id": task_id,
            "freeze_id": freeze_id,
            "query": query_meta,
            "subgraph": subgraph,
            "note": "graph_v2 子图；ref 边不参与 BFS",
        }
        if task_id == T002_TASK_ID:
            if CONTRACT_MANIFEST_PATH.is_file():
                payload["contract_slice"] = _sse_contract_slice()
            if TECH_MANIFEST_PATH.is_file():
                payload["manifest_slice"] = _manifest_slice_sse_unified()
            surface = _t002_impact_surface()
            if surface:
                payload["impact_surface"] = surface
        elif task_id == T003_TASK_ID:
            if TECH_MANIFEST_PATH.is_file():
                payload["manifest_slice"] = _manifest_slice_admin_ingest_compact()
            surface = _impact_surface_for_task(T003_TASK_ID, compact=True)
            if surface.get("candidates"):
                surface["schema"] = "gate_ctx_c_impact_surface_v2_compact"
                payload["impact_surface"] = surface
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
            "query": query_meta,
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
