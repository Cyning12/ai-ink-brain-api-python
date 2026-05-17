#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闸口 B：对三题批量跑 CTX_QUERY S0，并调用 score_gold_f1。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]
RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"
TASKS = [
    "T001_embedding_dim_default",
    "T002_unified_sse_chain_contract",
    "T003_ingest_admin_rpc",
]


def _load_run_s0():
    path = _REPO.parent / "run_s0_gate_b.py"
    spec = importlib.util.spec_from_file_location("run_s0_gate_b", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--arms", default="CTX_QUERY")
    p.add_argument("--parallel", action="store_true", help="单题内多臂并行")
    p.add_argument("--request-timeout", type=float, default=300.0)
    args = p.parse_args()
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]

    run_mod = _load_run_s0()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    batch_id = f"gate_ctx_b_v1_batch_{ts}"
    batch_dir = RUNS_ROOT / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)

    task_dirs: list[Path] = []
    exit_code = 0
    for i, task_id in enumerate(TASKS, start=1):
        run_dir = batch_dir / f"round_{i:02d}"
        _, index, code = run_mod.execute_gate_b_s0(
            run_dir=run_dir,
            task_id=task_id,
            arms=arms,
            parallel=args.parallel,
            request_timeout=args.request_timeout,
            batch_id=batch_id,
            batch_round=i,
            quiet=False,
        )
        task_dirs.append(run_dir)
        if code != 0:
            exit_code = code

    (batch_dir / "batch_index.json").write_text(
        json.dumps(
            {
                "schema": "gate_ctx_b_batch_v1",
                "batch_id": batch_id,
                "tasks": TASKS,
                "arms": arms,
                "run_dirs": [d.name for d in task_dirs],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    score_script = (
        REPO_ROOT
        / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py"
    )
    import subprocess

    proc = subprocess.run(
        [sys.executable, str(score_script), "--batch-dir", str(batch_dir)],
        check=False,
    )
    if proc.returncode != 0:
        exit_code = proc.returncode
    print(f"BATCH_OK: {batch_dir}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
