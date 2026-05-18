# -*- coding: utf-8 -*-
"""闸口 C P0：gate_ctx_c_v1 manifest / query 种子 / materialize 验收。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1"
GRAPH_PATH = REPO_ROOT / "docs/_tech_graph/graph.json"
MATERIALIZE_SCRIPT = FIXTURE_ROOT / "scripts/materialize_gate_c_payloads.py"
PROTOCOL_PATH = FIXTURE_ROOT / "protocol_version.yaml"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_protocol() -> dict:
    return yaml.safe_load(PROTOCOL_PATH.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def graph_doc() -> dict:
    return _load_json(GRAPH_PATH)


@pytest.fixture(scope="module")
def protocol() -> dict:
    return _load_protocol()


def test_dual_track_manifest_paths_exist() -> None:
    manifest = _load_json(FIXTURE_ROOT / "dual_track_manifest.json")
    for task_id, spec in manifest["tasks"].items():
        for track in spec["tracks"]:
            rel = track["path"]
            path = REPO_ROOT / rel
            assert path.is_file(), f"{task_id}: missing {rel}"


def _iter_seed_node_ids(spec: dict) -> list[str]:
    if "queries" in spec:
        return [q["node_id"] for q in spec["queries"]]
    return [spec["node_id"]]


def test_query_seed_nodes_exist_in_graph_v2(graph_doc: dict) -> None:
    seeds = _load_json(FIXTURE_ROOT / "query_seeds.json")
    node_ids = {n["id"] for n in graph_doc.get("nodes") or []}
    assert graph_doc.get("schema_version") == "graph_v2"
    for task_id, spec in seeds["tasks"].items():
        for nid in _iter_seed_node_ids(spec):
            assert nid in node_ids, f"{task_id}: unknown node {nid}"


def test_protocol_freeze_ids_locked(protocol: dict, graph_doc: dict) -> None:
    assert protocol["freeze_id"] == "TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0"
    assert protocol["graph_v2_freeze_id"] == graph_doc.get("freeze_id")
    limits = protocol["payload_limits"]
    assert limits["d_arm_nodes_lt_whole_mermaid_heuristic_tokens"] == 5026


def test_materialize_exit_zero_and_payloads_nonempty() -> None:
    proc = subprocess.run(
        [sys.executable, str(MATERIALIZE_SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    report = _load_json(FIXTURE_ROOT / "payloads/materialize_report.json")
    d_dir = FIXTURE_ROOT / "payloads/CTX_V2_QUERY"
    e_dir = FIXTURE_ROOT / "payloads/CTX_DUAL_MD"
    assert d_dir.is_dir() and any(d_dir.glob("*.json"))
    assert e_dir.is_dir() and any(e_dir.glob("*.md"))
    assert report["forbidden_checks"]["CTX_DUAL_MD_not_whole_corpus"] is True
    assert report["forbidden_checks"]["CTX_V2_QUERY_subgraph_below_mermaid_baseline"] is True


def test_d_arm_heuristic_tokens_below_mermaid_threshold(protocol: dict) -> None:
    report = _load_json(FIXTURE_ROOT / "payloads/materialize_report.json")
    baseline = protocol["payload_limits"]["d_arm_nodes_lt_whole_mermaid_heuristic_tokens"]
    per_task = report["arms_static"]["CTX_V2_QUERY"]["per_task"]
    for task_id, stats in per_task.items():
        assert stats["heuristic_tokens"] < baseline, (
            f"{task_id}: D arm tokens {stats['heuristic_tokens']} >= {baseline}"
        )


def test_t002_subgraph_covers_gold_graph_ids() -> None:
    """T002 D 臂 union 子图须含 tasks.json gold 关键 graph_id。"""
    proc = subprocess.run(
        [sys.executable, str(MATERIALIZE_SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    payload = _load_json(
        FIXTURE_ROOT / "payloads/CTX_V2_QUERY/T002_unified_sse_chain_contract.subgraph.json"
    )
    subgraph = payload["subgraph"]
    node_ids = {n["id"] for n in subgraph.get("nodes") or []}
    required = {"U2", "U1", "AUTH", "EV_TYPES"}
    missing = required - node_ids
    assert not missing, f"T002 subgraph missing gold nodes: {sorted(missing)}"
    assert payload.get("contract_slice"), "T002 应有 SSE contract 小切片"
    per_arm = _load_protocol()["payload_limits"]["max_heuristic_tokens_per_task_arm"]
    from tools.tech_graph_token_estimate import measure

    text = json.dumps(payload, ensure_ascii=False)
    tokens = measure("T002_payload", text)["heuristic_tokens"]
    assert tokens < per_arm, f"T002 tokens {tokens} >= {per_arm}"


def test_query_seeds_coverage_freeze_ids() -> None:
    seeds = _load_json(FIXTURE_ROOT / "query_seeds.json")
    assert seeds["freeze_id"] == "TECH_GRAPH_QUERY_COVERAGE_FREEZE_20260519_V1_0"
    assert seeds["graph_v2_freeze_id"] == "TECH_GRAPH_S2_FREEZE_20260519_V2_3"
