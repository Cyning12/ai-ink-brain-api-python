#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多轮 S0 批跑：每轮 --parallel 双分支，汇总后按规则剔除干扰再对比。

默认 **3 轮**（最小可剔除 1 个离群值的奇数轮次；推荐稳健可改为 5）。

落盘：docs/diary/jsonPKmermaid/runs/<batch_id>/
  round_01/ … round_NN/
  batch_index.json
  aggregate.json
  aggregate.md
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]
FIXTURE_ROOT = _REPO.parents[1]
RUNS_ROOT = REPO_ROOT / "docs" / "diary" / "jsonPKmermaid" / "runs"

# 最小轮次：3（可剔除 1 个离群）；正式对比建议 5
DEFAULT_ROUNDS = 3

# 墙钟硬上限（秒）：超过且相对中位数异常则标为干扰（如 104123 的 612s）
WALL_ABS_CAP_S = 120.0
WALL_MEDIAN_MULTIPLIER = 2.5


def _load_s0_module():
    path = _REPO.parent / "run_s0_minimal.py"
    spec = importlib.util.spec_from_file_location("gate_ctx_s0_minimal", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"无法加载 {path}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _median(vals: list[float]) -> float:
    return float(statistics.median(vals))


def _round_row(index: dict[str, Any], round_dir: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for arm in index.get("arms", []):
        pt = arm.get("prompt_tokens") or 0
        ct = arm.get("completion_tokens") or 0
        rows.append(
            {
                "round": index.get("batch_round"),
                "round_dir": round_dir,
                "arm": arm["arm"],
                "status": arm.get("status"),
                "parse_ok": arm.get("parse_ok"),
                "wall_total_s": arm.get("wall_total_s"),
                "prompt_tokens": pt,
                "completion_tokens": ct,
                "total_tokens": pt + ct,
                "batch_wall_total_s": index.get("batch_wall_total_s"),
            }
        )
    return rows


def _exclusion_reason(row: dict[str, Any], median_wall: float | None) -> str | None:
    if row.get("status") != "ok" or not row.get("parse_ok"):
        return "not_ok_or_invalid_schema"
    wall = row.get("wall_total_s")
    if wall is None:
        return "missing_wall"
    w = float(wall)
    if w > WALL_ABS_CAP_S:
        return f"wall_abs_cap>{WALL_ABS_CAP_S}"
    if median_wall is not None and median_wall > 0 and w > median_wall * WALL_MEDIAN_MULTIPLIER:
        return f"wall>{WALL_MEDIAN_MULTIPLIER}x_median"
    return None


def _summarize_arm(rows: list[dict[str, Any]], *, use_clean_only: bool) -> dict[str, Any]:
    subset = [r for r in rows if r.get("_include")] if use_clean_only else rows
    walls = [float(r["wall_total_s"]) for r in subset if r.get("wall_total_s") is not None]
    totals = [int(r["total_tokens"]) for r in subset]
    if not walls:
        return {"n": 0}
    return {
        "n": len(subset),
        "wall_median_s": round(_median(walls), 3),
        "wall_min_s": round(min(walls), 3),
        "wall_max_s": round(max(walls), 3),
        "total_tokens_median": int(statistics.median(totals)) if totals else None,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="gate_ctx_ab_v1 多轮 S0 批跑（默认并行）")
    p.add_argument("--rounds", type=int, default=DEFAULT_ROUNDS, help=f"轮次数（默认 {DEFAULT_ROUNDS}）")
    p.add_argument("--pause-between-rounds", type=float, default=3.0, help="轮间暂停秒数")
    p.add_argument("--request-timeout", type=float, default=300.0)
    p.add_argument("--model", default=None)
    args = p.parse_args()

    if args.rounds < 3:
        print("rounds 建议 ≥3 以便剔除离群；已拒绝 <3", file=sys.stderr)
        return 2

    s0 = _load_s0_module()
    batch_id = f"gate_ctx_ab_v1_batch_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}"
    batch_dir = RUNS_ROOT / batch_id
    batch_dir.mkdir(parents=True, exist_ok=True)

    print(f"batch_id={batch_id} rounds={args.rounds} mode=parallel", flush=True)

    round_indexes: list[dict[str, Any]] = []
    all_rows: list[dict[str, Any]] = []

    for r in range(1, args.rounds + 1):
        round_dir = batch_dir / f"round_{r:02d}"
        print(f"\n=== 第 {r}/{args.rounds} 轮 ===", flush=True)
        try:
            _, index, code = s0.execute_s0_round(
                run_dir=round_dir,
                parallel=True,
                model=args.model,
                request_timeout=args.request_timeout,
                batch_id=batch_id,
                batch_round=r,
                quiet=False,
            )
            index["exit_code"] = code
            round_indexes.append(index)
            for row in _round_row(index, round_dir.name):
                all_rows.append(row)
        except RuntimeError as e:
            print(f"第 {r} 轮失败: {e}", file=sys.stderr)
            round_indexes.append({"batch_round": r, "error": str(e)})
        if r < args.rounds and args.pause_between_rounds > 0:
            time.sleep(args.pause_between_rounds)

    # 按 arm 标干扰
    for arm_id in ("CTX_JSON", "CTX_MERMAID"):
        arm_rows = [x for x in all_rows if x["arm"] == arm_id and x.get("wall_total_s") is not None]
        med = _median([float(x["wall_total_s"]) for x in arm_rows]) if arm_rows else None
        for row in all_rows:
            if row["arm"] != arm_id:
                continue
            reason = _exclusion_reason(row, med)
            row["_exclude_reason"] = reason
            row["_include"] = reason is None

    clean_rows = [r for r in all_rows if r.get("_include")]
    json_rows = [r for r in all_rows if r["arm"] == "CTX_JSON"]
    mmd_rows = [r for r in all_rows if r["arm"] == "CTX_MERMAID"]

    aggregate = {
        "schema": "gate_ctx_ab_batch_aggregate_v1",
        "batch_id": batch_id,
        "rounds_requested": args.rounds,
        "rounds_completed": len([i for i in round_indexes if "arms" in i]),
        "execution_mode": "parallel",
        "exclusion_rules": {
            "wall_abs_cap_s": WALL_ABS_CAP_S,
            "wall_median_multiplier": WALL_MEDIAN_MULTIPLIER,
            "also_exclude": "status!=ok or parse_ok==false",
        },
        "all_measurements": all_rows,
        "per_arm_raw": {
            "CTX_JSON": _summarize_arm(json_rows, use_clean_only=False),
            "CTX_MERMAID": _summarize_arm(mmd_rows, use_clean_only=False),
        },
        "per_arm_clean": {
            "CTX_JSON": _summarize_arm(json_rows, use_clean_only=True),
            "CTX_MERMAID": _summarize_arm(mmd_rows, use_clean_only=True),
        },
        "comparison_clean": {},
        "round_indexes": round_indexes,
    }

    cj = aggregate["per_arm_clean"]["CTX_JSON"]
    cm = aggregate["per_arm_clean"]["CTX_MERMAID"]
    if cj.get("n", 0) > 0 and cm.get("n", 0) > 0:
        aggregate["comparison_clean"] = {
            "wall_median_s": {
                "CTX_JSON": cj["wall_median_s"],
                "CTX_MERMAID": cm["wall_median_s"],
                "faster_arm": (
                    "CTX_JSON"
                    if cj["wall_median_s"] < cm["wall_median_s"]
                    else "CTX_MERMAID"
                ),
            },
            "total_tokens_median": {
                "CTX_JSON": cj.get("total_tokens_median"),
                "CTX_MERMAID": cm.get("total_tokens_median"),
                "lower_arm": (
                    "CTX_JSON"
                    if (cj.get("total_tokens_median") or 0) < (cm.get("total_tokens_median") or 0)
                    else "CTX_MERMAID"
                ),
            },
        }

    (batch_dir / "aggregate.json").write_text(
        json.dumps(aggregate, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (batch_dir / "batch_index.json").write_text(
        json.dumps(
            {
                "batch_id": batch_id,
                "rounds": args.rounds,
                "round_dirs": [f"round_{i:02d}" for i in range(1, args.rounds + 1)],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    md: list[str] = [
        f"# gate_ctx_ab_v1 batch — `{batch_id}`",
        "",
        f"- **轮次**：{args.rounds}（每轮 `--parallel`）",
        f"- **剔除规则**：`wall>{WALL_ABS_CAP_S}s` 或 `>{WALL_MEDIAN_MULTIPLIER}×` 该 arm 当轮中位数；或 `status!=ok`",
        "",
        "## 全量测量",
        "",
        "| round | arm | wall_s | total_tokens | include | exclude_reason |",
        "| ---:| --- | ---:| ---:| --- | --- |",
    ]
    for row in sorted(all_rows, key=lambda x: (x.get("round") or 0, x["arm"])):
        md.append(
            f"| {row.get('round')} | `{row['arm']}` | {row.get('wall_total_s')} | "
            f"{row.get('total_tokens')} | {row.get('_include')} | {row.get('_exclude_reason') or ''} |"
        )
    md.extend(
        [
            "",
            "## 剔除后对比（中位数）",
            "",
            "| 指标 | CTX_JSON | CTX_MERMAID |",
            "| --- | ---:| ---:|",
            f"| wall_median_s | {cj.get('wall_median_s', '—')} | {cm.get('wall_median_s', '—')} |",
            f"| total_tokens_median | {cj.get('total_tokens_median', '—')} | {cm.get('total_tokens_median', '—')} |",
            f"| 有效样本数 n | {cj.get('n', 0)} | {cm.get('n', 0)} |",
            "",
            f"详见 [`aggregate.json`](./aggregate.json)",
        ]
    )
    (batch_dir / "aggregate.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"\nOK: {batch_dir}")
    print(f"aggregate.md 已写；clean JSON wall 中位数={cj.get('wall_median_s')} Mermaid={cm.get('wall_median_s')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
