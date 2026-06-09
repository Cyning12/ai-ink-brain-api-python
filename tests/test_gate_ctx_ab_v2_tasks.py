"""闸口 D：gate_ctx_ab_v2 题集 schema 与 v1 三题 gold 一致性。"""

from __future__ import annotations

import json
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
AB_V1 = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json"
AB_V2 = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v2/tasks.json"
PROTOCOL_PATH = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1/protocol_version.yaml"
GATE_D_FREEZE_ID = "TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0"
V1_TASK_IDS = (
    "T001_embedding_dim_default",
    "T002_unified_sse_chain_contract",
    "T003_ingest_admin_rpc",
)


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_ab_v2_schema_and_five_tasks() -> None:
    doc = _load_json(AB_V2)
    assert doc["schema_version"] == "gate_ctx_ab_tasks_v2"
    assert doc["fixture_set"] == "gate_ctx_ab_v2"
    task_ids = [t["task_id"] for t in doc["tasks"]]
    assert len(task_ids) == 5
    assert task_ids[:3] == list(V1_TASK_IDS)
    assert "T004_chatbi_text2sql_chain" in task_ids
    assert "T005_intent_routing" in task_ids


def test_v1_three_tasks_gold_unchanged() -> None:
    v1 = _load_json(AB_V1)
    v2 = _load_json(AB_V2)
    v1_by_id = {t["task_id"]: t for t in v1["tasks"]}
    for tid in V1_TASK_IDS:
        assert v1_by_id[tid]["gold"] == next(
            t["gold"] for t in v2["tasks"] if t["task_id"] == tid
        )


def test_t004_t005_gold_minimum_entry_impacts() -> None:
    doc = _load_json(AB_V2)
    for tid in ("T004_chatbi_text2sql_chain", "T005_intent_routing"):
        task = next(t for t in doc["tasks"] if t["task_id"] == tid)
        gold = task["gold"]
        assert len(gold["entrypoints"]) >= 3
        assert len(gold["impacts"]) >= 3


def test_protocol_points_to_ab_v2_and_gate_d_freeze() -> None:
    protocol = yaml.safe_load(PROTOCOL_PATH.read_text(encoding="utf-8"))
    assert protocol["tasks_ref"].endswith("gate_ctx_ab_v2/tasks.json")
    assert protocol["gate_d_v2_tasks_freeze_id"] == GATE_D_FREEZE_ID
