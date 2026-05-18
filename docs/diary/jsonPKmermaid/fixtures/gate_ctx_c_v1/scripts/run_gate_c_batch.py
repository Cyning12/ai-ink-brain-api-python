#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""闸口 C：对三题批量跑 CTX_V2_QUERY + CTX_DUAL_MD S0，并调用 score_gold_f1。"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))
RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"
MATERIALIZE_SCRIPT = FIXTURE_ROOT / "scripts/materialize_gate_c_payloads.py"
TASKS_JSON = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json"
SCORE_SCRIPT = (
    REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/scripts/score_gold_f1.py"
)

TASKS = [
    "T001_embedding_dim_default",
    "T002_unified_sse_chain_contract",
    "T003_ingest_admin_rpc",
]
DEFAULT_ARMS = ["CTX_V2_QUERY", "CTX_DUAL_MD"]


def _load_run_s0():
    path = _REPO.parent / "run_s0_gate_c.py"
    spec = importlib.util.spec_from_file_location("run_s0_gate_c", path)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(mod)
    return mod


def _batch_dir_label(batch_dir: Path) -> str:
    try:
        return batch_dir.resolve().relative_to(REPO_ROOT.resolve()).as_posix()
    except ValueError:
        return batch_dir.resolve().as_posix()


def _reproduce_commands(*, batch_dir: Path, arms: list[str], dry_run: bool) -> dict[str, str]:
    arms_csv = ",".join(arms)
    rel_batch = _batch_dir_label(batch_dir)
    mat = MATERIALIZE_SCRIPT.relative_to(REPO_ROOT).as_posix()
    batch_py = Path(__file__).relative_to(REPO_ROOT).as_posix()
    score_py = SCORE_SCRIPT.relative_to(REPO_ROOT).as_posix()
    return {
        "materialize": f"python {mat}",
        "batch": (
            f"RUBRIC_REVIEW_BACKEND=siliconflow python {batch_py} --arms {arms_csv}"
            + (" --dry-run" if dry_run else "")
        ),
        "score_gold_f1": f"python {score_py} --batch-dir {rel_batch} --tasks docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1/tasks.json",
        "note": "模型/温度见 gate_ctx_c_v1/protocol_version.yaml（DeepSeek-V4-Flash · 0.2）",
    }


def _preflight_llm_env() -> None:
    from tools.rubric_review.config import ReviewRuntimeConfig

    cfg = ReviewRuntimeConfig.from_env()
    if cfg.backend != "siliconflow":
        raise RuntimeError("需要 RUBRIC_REVIEW_BACKEND=siliconflow")
    if not cfg.siliconflow_api_key:
        raise RuntimeError("缺少 SILICONFLOW_API_KEY（FP-C-5）")


def run_materialize() -> int:
    proc = subprocess.run(
        [sys.executable, str(MATERIALIZE_SCRIPT)],
        cwd=REPO_ROOT,
        check=False,
    )
    return proc.returncode


def run_gate_c_batch(
    *,
    batch_dir: Path | None = None,
    arms: list[str] | None = None,
    parallel: bool = False,
    request_timeout: float = 300.0,
    dry_run: bool = False,
    skip_materialize: bool = False,
    skip_score: bool = False,
) -> int:
    arms = arms or list(DEFAULT_ARMS)
    run_mod = _load_run_s0()
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    batch_id = f"gate_ctx_c_v1_batch_{ts}"
    if batch_dir is None:
        batch_dir = RUNS_ROOT / batch_id
    else:
        batch_id = batch_dir.name
    batch_dir.mkdir(parents=True, exist_ok=True)

    if not dry_run:
        try:
            _preflight_llm_env()
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            return 2

    if not skip_materialize:
        mat_code = run_materialize()
        if mat_code != 0:
            print("materialize 失败", file=sys.stderr)
            return mat_code

    task_dirs: list[Path] = []
    exit_code = 0
    for i, task_id in enumerate(TASKS, start=1):
        run_dir = batch_dir / f"round_{i:02d}"
        _, index, code = run_mod.execute_gate_c_s0(
            run_dir=run_dir,
            task_id=task_id,
            arms=arms,
            parallel=parallel,
            request_timeout=request_timeout,
            batch_id=batch_id,
            batch_round=i,
            quiet=False,
            dry_run=dry_run,
        )
        task_dirs.append(run_dir)
        if code != 0:
            exit_code = code

    repro = _reproduce_commands(batch_dir=batch_dir, arms=arms, dry_run=dry_run)
    batch_index = {
        "schema": "gate_ctx_c_batch_v1",
        "batch_id": batch_id,
        "protocol_version": "gate_ctx_c_v1",
        "freeze_id": "TECH_GRAPH_GATE_C_FREEZE_20260518_V1_0",
        "tasks": TASKS,
        "arms": arms,
        "dry_run": dry_run,
        "run_dirs": [d.name for d in task_dirs],
        "reproduce_commands": repro,
    }
    (batch_dir / "batch_index.json").write_text(
        json.dumps(batch_index, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    readme_lines = [
        f"# {batch_id}",
        "",
        f"- **arms**：`{','.join(arms)}`",
        f"- **dry_run**：`{dry_run}`",
        "",
        "## 复现",
        "",
        "```bash",
        repro["materialize"],
        repro["batch"],
        repro["score_gold_f1"],
        "```",
        "",
        repro.get("note", ""),
    ]
    (batch_dir / "README.md").write_text("\n".join(readme_lines) + "\n", encoding="utf-8")

    if not dry_run and not skip_score:
        proc = subprocess.run(
            [
                sys.executable,
                str(SCORE_SCRIPT),
                "--batch-dir",
                str(batch_dir),
                "--tasks",
                str(TASKS_JSON),
            ],
            check=False,
        )
        if proc.returncode != 0:
            exit_code = proc.returncode

    print(f"BATCH_OK: {batch_dir}")
    return exit_code


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--arms", default="CTX_V2_QUERY,CTX_DUAL_MD")
    p.add_argument("--parallel", action="store_true", help="单题内多臂并行")
    p.add_argument("--request-timeout", type=float, default=300.0)
    p.add_argument("--dry-run", action="store_true", help="无 LLM；仅验证目录与 batch_index")
    p.add_argument("--skip-materialize", action="store_true")
    p.add_argument("--skip-score", action="store_true")
    args = p.parse_args()
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    if not args.dry_run:
        try:
            _preflight_llm_env()
        except RuntimeError as e:
            print(str(e), file=sys.stderr)
            return 2
    return run_gate_c_batch(
        arms=arms,
        parallel=args.parallel,
        request_timeout=args.request_timeout,
        dry_run=args.dry_run,
        skip_materialize=args.skip_materialize,
        skip_score=args.skip_score,
    )


if __name__ == "__main__":
    raise SystemExit(main())
