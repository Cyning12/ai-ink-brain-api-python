#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
闸口 B S0：对指定 task 跑 CTX_MERMAID / CTX_JSON / CTX_QUERY（默认仅 CTX_QUERY）。

A/B 行为真值可沿用闸口 A；本脚本用于补跑 CTX_QUERY 或三臂复现。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]
GATE_A_FIXTURE = REPO_ROOT / "docs/diary/jsonPKmermaid/fixtures/gate_ctx_ab_v1"
PROTOCOL_PATH = FIXTURE_ROOT / "protocol_version.yaml"
RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_s0_module():
    path = GATE_A_FIXTURE / "scripts" / "run_s0_minimal.py"
    spec = importlib.util.spec_from_file_location("gate_ctx_s0_minimal", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _gate_b_arm_specs(task_id: str) -> dict[str, tuple[str, Path]]:
    return {
        "CTX_JSON": (
            "graph_v1 整包（闸口 A 冻结 payload）",
            GATE_A_FIXTURE / "payloads" / "CTX_JSON" / "main.graph.json",
        ),
        "CTX_MERMAID": (
            "Mermaid 语料总串（闸口 A 冻结 payload）",
            GATE_A_FIXTURE / "payloads" / "CTX_MERMAID" / "main.mermaid_corpus.txt",
        ),
        "CTX_QUERY": (
            f"v2 graph_query 子图（task={task_id}）",
            FIXTURE_ROOT / "payloads" / "CTX_QUERY" / f"{task_id}.subgraph.json",
        ),
    }


def _parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="gate_ctx_b_v1 S0")
    p.add_argument("--task-id", required=True)
    p.add_argument(
        "--arms",
        default="CTX_QUERY",
        help="逗号分隔臂，默认仅 CTX_QUERY",
    )
    p.add_argument("--parallel", action="store_true")
    p.add_argument("--model", default=None)
    p.add_argument("--request-timeout", type=float, default=300.0)
    p.add_argument("--batch-id", default=None)
    p.add_argument("--batch-round", type=int, default=None)
    p.add_argument("--quiet", action="store_true")
    return p.parse_args()


def execute_gate_b_s0(
    *,
    run_dir: Path,
    task_id: str,
    arms: list[str],
    parallel: bool = False,
    model: str | None = None,
    request_timeout: float = 300.0,
    batch_id: str | None = None,
    batch_round: int | None = None,
    quiet: bool = False,
) -> tuple[Path, dict[str, Any], int]:
    s0 = _load_s0_module()
    protocol = s0.load_protocol(PROTOCOL_PATH)
    tasks_doc = json.loads((GATE_A_FIXTURE / "tasks.json").read_text(encoding="utf-8"))
    task = next(t for t in tasks_doc["tasks"] if t["task_id"] == task_id)

    from tools.rubric_review.config import ReviewRuntimeConfig

    cfg = ReviewRuntimeConfig.from_env()
    if cfg.backend != "siliconflow":
        raise RuntimeError("需要 RUBRIC_REVIEW_BACKEND=siliconflow")
    api_key = cfg.siliconflow_api_key
    if not api_key:
        raise RuntimeError("缺少 SILICONFLOW_API_KEY")

    model_resolved = (model or protocol.get("model") or "").strip()
    temperature = float(protocol.get("temperature") or 0.2)
    max_tokens = int(protocol.get("max_tokens") or 4096)
    protocol_version = str(protocol.get("protocol_version") or "gate_ctx_b_v1")
    freeze_id = str(protocol.get("freeze_id") or "")

    specs = _gate_b_arm_specs(task_id)
    for arm in arms:
        if arm not in specs:
            raise ValueError(f"未知臂 {arm}")
        path = specs[arm][1]
        if not path.is_file():
            raise FileNotFoundError(f"缺少载荷 {path}；先运行 materialize_gate_b_payloads.py")

    manifest = s0._load_text(GATE_A_FIXTURE / "payloads" / "_shared" / "_manifest.json")
    contract = s0._load_text(
        GATE_A_FIXTURE / "payloads" / "_shared" / "_contract_manifest.json"
    )
    system = s0._load_text(GATE_A_FIXTURE / "system.md")

    run_id = run_dir.name
    raw_dir = run_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    execution_mode = "parallel" if parallel else "sequential"

    common_kw = {
        "manifest": manifest,
        "contract": contract,
        "task_prompt": task["prompt_zh"],
        "system": system,
        "model": model_resolved,
        "api_key": api_key,
        "base_url": cfg.siliconflow_base_url,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "request_timeout": request_timeout,
        "run_id": run_id,
        "arm_ids": arms,
        "task_id": task_id,
        "protocol_version": protocol_version,
        "provider": cfg.backend,
        "execution_mode": execution_mode,
    }

    arm_items = [(a, specs[a][0], s0._load_text(specs[a][1])) for a in arms]
    results_by_arm: dict[str, tuple[dict, dict]] = {}
    batch_wall_s: float | None = None

    if parallel:
        batch_t0 = time.perf_counter()

        def _job(item: tuple[str, str, str]):
            arm, label, text = item
            return arm, s0._execute_arm(
                call_index=arms.index(arm) + 1,
                arm=arm,
                main_label=label,
                main_text=text,
                **common_kw,
            )

        with ThreadPoolExecutor(max_workers=len(arm_items)) as pool:
            for fut in as_completed(pool.submit(_job, it) for it in arm_items):
                arm, rec, summ = fut.result()
                results_by_arm[arm] = (rec, summ)
        batch_wall_s = round(time.perf_counter() - batch_t0, 3)
    else:
        for i, (arm, label, text) in enumerate(arm_items, start=1):
            rec, summ = s0._execute_arm(
                call_index=i,
                arm=arm,
                main_label=label,
                main_text=text,
                **common_kw,
            )
            results_by_arm[arm] = (rec, summ)

    summary_rows = []
    for arm in arms:
        record, summary = results_by_arm[arm]
        record["schema"] = "gate_ctx_b_s0_record_v1"
        record["freeze_id"] = freeze_id
        out_path = raw_dir / summary["file"]
        out_path.write_text(json.dumps(record, ensure_ascii=False) + "\n", encoding="utf-8")
        summary_rows.append(summary)

    index = {
        "schema": "gate_ctx_b_run_index_v1",
        "run_id": run_id,
        "task_id": task_id,
        "segment": "S0",
        "protocol_version": protocol_version,
        "freeze_id": freeze_id,
        "model_requested": model_resolved,
        "arms_order": arms,
        "execution_mode": execution_mode,
        "batch_wall_total_s": batch_wall_s,
        "arms": summary_rows,
    }
    if batch_id:
        index["parent_batch_id"] = batch_id
    if batch_round is not None:
        index["batch_round"] = batch_round

    (run_dir / "index.json").write_text(
        json.dumps(index, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if not quiet:
        print(f"OK: {run_dir}")
    code = 0 if all(r["parse_ok"] for r in summary_rows) else 1
    return run_dir, index, code


def main() -> int:
    args = _parse_args()
    arms = [a.strip() for a in args.arms.split(",") if a.strip()]
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_dir = RUNS_ROOT / f"gate_ctx_b_v1_{args.task_id}_{ts}"
    try:
        _, _, code = execute_gate_b_s0(
            run_dir=run_dir,
            task_id=args.task_id,
            arms=arms,
            parallel=args.parallel,
            model=args.model,
            request_timeout=args.request_timeout,
            batch_id=args.batch_id,
            batch_round=args.batch_round,
            quiet=args.quiet,
        )
        return code
    except (RuntimeError, FileNotFoundError, ValueError) as e:
        print(str(e), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
