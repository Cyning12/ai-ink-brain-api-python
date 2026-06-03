# -*- coding: utf-8 -*-
"""闸口 C / C′：gate_ctx_c_v1 manifest / query 种子 / materialize 验收。

默认 **只读** 已提交的 payloads；重写 fixtures 须：
``GATE_CTX_C_UPDATE_FIXTURES=1 pytest tests/test_gate_ctx_c_v1_materialize.py``
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
import yaml

from tests.gate_ctx_c_materialize import materialize_gate_c_payloads_if_requested

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1"
GRAPH_PATH = REPO_ROOT / "docs/_tech_graph/graph.json"
PROTOCOL_PATH = FIXTURE_ROOT / "protocol_version.yaml"
GATE_C_PRIME_FREEZE_ID = "TECH_GRAPH_GATE_C_PRIME_F1_FREEZE_20260520_V1_0"
GATE_C_DOUBLE_PRIME_FREEZE_ID = "TECH_GRAPH_GATE_C_DOUBLE_PRIME_FREEZE_20260520_V1_0"
GATE_D_V2_TASKS_FREEZE_ID = "TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0"
GATE_C_CANONICAL_FREEZE_ID = "TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0"
T003_TASK_ID = "T003_ingest_admin_rpc"
T004_TASK_ID = "T004_chatbi_text2sql_chain"
T005_TASK_ID = "T005_intent_routing"
EXPECTED_TASK_IDS = (
    "T001_embedding_dim_default",
    "T002_unified_sse_chain_contract",
    T003_TASK_ID,
    T004_TASK_ID,
    T005_TASK_ID,
)


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
    assert protocol["freeze_id"] == GATE_C_CANONICAL_FREEZE_ID
    assert protocol["gate_c_prime_freeze_id"] == GATE_C_PRIME_FREEZE_ID
    assert protocol["gate_c_double_prime_freeze_id"] == GATE_C_DOUBLE_PRIME_FREEZE_ID
    assert protocol["gate_d_v2_tasks_freeze_id"] == GATE_D_V2_TASKS_FREEZE_ID
    assert protocol["tasks_ref"].endswith("gate_ctx_ab_v2/tasks.json")
    assert protocol["graph_v2_freeze_id"] == graph_doc.get("freeze_id")
    limits = protocol["payload_limits"]
    assert limits["d_arm_nodes_lt_whole_mermaid_heuristic_tokens"] == 5026


def test_materialize_exit_zero_and_payloads_nonempty() -> None:
    materialize_gate_c_payloads_if_requested()
    report = _load_json(FIXTURE_ROOT / "payloads/materialize_report.json")
    d_dir = FIXTURE_ROOT / "payloads/CTX_V2_QUERY"
    e_dir = FIXTURE_ROOT / "payloads/CTX_DUAL_MD"
    assert d_dir.is_dir() and any(d_dir.glob("*.json"))
    assert e_dir.is_dir() and any(e_dir.glob("*.md"))
    assert report["forbidden_checks"]["CTX_DUAL_MD_not_whole_corpus"] is True
    assert report["forbidden_checks"]["CTX_V2_QUERY_subgraph_below_mermaid_baseline"] is True
    assert report["freeze_id"] == GATE_D_V2_TASKS_FREEZE_ID
    per_task = report["arms_static"]["CTX_V2_QUERY"]["per_task"]
    assert set(per_task.keys()) == set(EXPECTED_TASK_IDS)


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
    materialize_gate_c_payloads_if_requested()
    payload = _load_json(
        FIXTURE_ROOT / "payloads/CTX_V2_QUERY/T002_unified_sse_chain_contract.subgraph.json"
    )
    subgraph = payload["subgraph"]
    node_ids = {n["id"] for n in subgraph.get("nodes") or []}
    required = {"U2", "U1", "AUTH", "EV_TYPES"}
    missing = required - node_ids
    assert not missing, f"T002 subgraph missing gold nodes: {sorted(missing)}"
    cs = payload.get("contract_slice") or {}
    assert cs.get("schema") == "gate_ctx_c_sse_contract_slice_v2"
    assert cs.get("envelope_keys") == ["event", "data"]
    assert cs.get("chain_data_keys") == ["type", "ts", "step_id", "payload"]
    assert "rag.sources" in (cs.get("impact_chain_type_values") or [])
    assert cs.get("contract_check_tool") == "tools/tech_graph_contract_check.py"
    ms = payload.get("manifest_slice") or {}
    ep_paths = {e.get("path") for e in ms.get("endpoints") or []}
    assert "/api/py/unified/chat/stream" in ep_paths
    assert "/api/py/unified/chat" in ep_paths
    surface = payload.get("impact_surface") or {}
    surf_paths = {c.get("path") for c in surface.get("candidates") or []}
    assert "api/agent.py" in surf_paths
    assert "tools/tech_graph_contract_check.py" in surf_paths
    per_arm = _load_protocol()["payload_limits"]["max_heuristic_tokens_per_task_arm"]
    from tools.tech_graph_token_estimate import measure

    text = json.dumps(payload, ensure_ascii=False)
    tokens = measure("T002_payload", text)["heuristic_tokens"]
    assert tokens < per_arm, f"T002 tokens {tokens} >= {per_arm}"


def test_query_seeds_gate_d_freeze_ids() -> None:
    seeds = _load_json(FIXTURE_ROOT / "query_seeds.json")
    assert seeds["freeze_id"] == GATE_D_V2_TASKS_FREEZE_ID
    assert seeds["graph_v2_freeze_id"] == "TECH_GRAPH_S2_FREEZE_20260519_V2_3"
    assert seeds.get("parent_freeze_id") == GATE_C_DOUBLE_PRIME_FREEZE_ID
    assert set(seeds["tasks"].keys()) == set(EXPECTED_TASK_IDS)


def test_t003_manifest_slice_and_impact_surface() -> None:
    """T003 D 臂须含 Admin Ingest manifest_slice + gold impact_surface。"""
    materialize_gate_c_payloads_if_requested()
    payload = _load_json(
        FIXTURE_ROOT / f"payloads/CTX_V2_QUERY/{T003_TASK_ID}.subgraph.json"
    )
    ms = payload.get("manifest_slice") or {}
    assert ms.get("schema") == "gate_ctx_c_manifest_slice_v2_compact"
    ep_paths = set(ms.get("endpoint_paths") or [])
    assert "/api/py/admin/ingest" in ep_paths
    assert "/api/py/admin/sync" in ep_paths
    anchor_paths = set(ms.get("anchor_paths") or [])
    assert "api/ingest_pipeline.py" in anchor_paths
    assert "api/rag_env.py" in anchor_paths
    surface = payload.get("impact_surface") or {}
    assert surface.get("schema") == "gate_ctx_c_impact_surface_v2_compact"
    surf_paths = {c.get("path") for c in surface.get("candidates") or []}
    assert "api/rag_env.py" in surf_paths
    assert "supabase/sql" in surf_paths
    assert "api/ingest_pipeline.py" in surf_paths
    assert "tools/tech_graph_manifest_check.py" in surf_paths
    per_arm = _load_protocol()["payload_limits"]["max_heuristic_tokens_per_task_arm"]
    from tools.tech_graph_token_estimate import measure

    text = json.dumps(payload, ensure_ascii=False)
    tokens = measure("T003_payload", text)["heuristic_tokens"]
    assert tokens < per_arm, f"T003 tokens {tokens} >= {per_arm}"


def test_t004_t005_payload_slices_and_seeds(graph_doc: dict) -> None:
    """T004/T005 D 臂须含 manifest/contract/impact 切片且种子节点 ∈ graph_v2。"""
    materialize_gate_c_payloads_if_requested()
    node_ids = {n["id"] for n in graph_doc.get("nodes") or []}
    seeds = _load_json(FIXTURE_ROOT / "query_seeds.json")
    for task_id in (T004_TASK_ID, T005_TASK_ID):
        spec = seeds["tasks"][task_id]
        for nid in _iter_seed_node_ids(spec):
            assert nid in node_ids, f"{task_id}: unknown node {nid}"
    t004 = _load_json(
        FIXTURE_ROOT / f"payloads/CTX_V2_QUERY/{T004_TASK_ID}.subgraph.json"
    )
    ms4 = t004.get("manifest_slice") or {}
    assert "/api/py/text2sql/chat" in set(ms4.get("endpoint_paths") or [])
    t005 = _load_json(
        FIXTURE_ROOT / f"payloads/CTX_V2_QUERY/{T005_TASK_ID}.subgraph.json"
    )
    assert (t005.get("impact_surface") or {}).get("candidates")
    subgraph5 = t005["subgraph"]
    assert "INT" in {n["id"] for n in subgraph5.get("nodes") or []}
