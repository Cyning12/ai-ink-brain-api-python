# -*- coding: utf-8 -*-
"""闸口 C P1：batch runner 臂路径映射与 dry-run batch_index 结构。"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURE_ROOT = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_c_v1"
RUN_S0_PATH = FIXTURE_ROOT / "scripts/run_s0_gate_c.py"
RUN_BATCH_PATH = FIXTURE_ROOT / "scripts/run_gate_c_batch.py"
MATERIALIZE_SCRIPT = FIXTURE_ROOT / "scripts/materialize_gate_c_payloads.py"
TASKS_REF = FIXTURE_ROOT / "tasks_ref.json"

DEFAULT_ARMS = ["CTX_V2_QUERY", "CTX_DUAL_MD"]
TASK_IDS = [
    "T001_embedding_dim_default",
    "T002_unified_sse_chain_contract",
    "T003_ingest_admin_rpc",
    "T004_chatbi_text2sql_chain",
    "T005_intent_routing",
]


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def gate_c_s0():
    return _load_module(RUN_S0_PATH, "run_s0_gate_c_test")


@pytest.fixture(scope="module")
def gate_c_batch():
    return _load_module(RUN_BATCH_PATH, "run_gate_c_batch_test")


@pytest.fixture(scope="module", autouse=True)
def _materialize_once() -> None:
    proc = subprocess.run(
        [sys.executable, str(MATERIALIZE_SCRIPT)],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_tasks_ref_lists_five_tasks() -> None:
    doc = json.loads(TASKS_REF.read_text(encoding="utf-8"))
    assert doc["task_ids"] == TASK_IDS
    assert doc["tasks_ref"].endswith("gate_ctx_ab_v2/tasks.json")


def test_gate_c_arm_specs_paths_exist(gate_c_s0) -> None:
    for task_id in TASK_IDS:
        specs = gate_c_s0.gate_c_arm_specs(task_id)
        assert set(specs) == set(DEFAULT_ARMS)
        for arm in DEFAULT_ARMS:
            label, path = specs[arm]
            assert path.is_file(), f"{task_id}/{arm}: missing {path}"
            assert label


def test_gate_c_arm_payload_suffixes(gate_c_s0) -> None:
    specs = gate_c_s0.gate_c_arm_specs(TASK_IDS[0])
    assert specs["CTX_V2_QUERY"][1].name.endswith(".subgraph.json")
    assert specs["CTX_DUAL_MD"][1].name.endswith(".dual_track.md")


def test_dry_run_batch_index_and_round_layout(tmp_path: Path, gate_c_batch) -> None:
    batch_dir = tmp_path / "gate_ctx_c_v1_batch_test"
    code = gate_c_batch.run_gate_c_batch(
        batch_dir=batch_dir,
        arms=DEFAULT_ARMS,
        dry_run=True,
        skip_materialize=True,
        skip_score=True,
    )
    assert code == 0
    index_path = batch_dir / "batch_index.json"
    assert index_path.is_file()
    index = json.loads(index_path.read_text(encoding="utf-8"))
    assert index["schema"] == "gate_ctx_c_batch_v2"
    assert index["tasks"] == TASK_IDS
    assert index["arms"] == DEFAULT_ARMS
    assert "reproduce_commands" in index
    assert len(index["run_dirs"]) == 5
    for i in range(1, 6):
        round_dir = batch_dir / f"round_{i:02d}"
        assert (round_dir / "index.json").is_file()
        raw_files = list((round_dir / "raw").glob("*_S0.jsonl"))
        assert len(raw_files) == 2
        for jp in raw_files:
            rec = json.loads(jp.read_text(encoding="utf-8").strip())
            assert rec["schema"] == "gate_ctx_c_s0_record_v1"
            assert rec["arm"] in DEFAULT_ARMS
            assert rec.get("dry_run") is True
