#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 gate_ctx_ab S1/S2 batch 的 batch_index.json 生成 aggregate.md / aggregate.json。"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Any

_REPO = Path(__file__).resolve()
REPO_ROOT = _REPO.parents[6]


def _median(vals: list[float]) -> float | None:
    return float(statistics.median(vals)) if vals else None


def aggregate(batch_dir: Path) -> dict[str, Any]:
    bi = json.loads((batch_dir / "batch_index.json").read_text(encoding="utf-8"))
    sessions = bi.get("sessions") or []
    rows: list[dict[str, Any]] = []
    for s in sessions:
        rounds = s.get("rounds") or []
        s0 = next((r for r in rounds if r.get("segment") == "S0"), {})
        s2 = [r for r in rounds if r.get("segment") == "S2"]
        leak = sum(int(r.get("leakage_count_heuristic") or 0) for r in s2)
        rows.append(
            {
                "task_id": s.get("primary_task_id"),
                "topic_id": s.get("topic_id"),
                "arm": s.get("arm"),
                "s0_wall_s": s0.get("wall_total_s"),
                "s0_tokens": s0.get("total_tokens"),
                "cumulative_tokens_final": s.get("cumulative_tokens_final"),
                "s2_leakage_sum": leak,
                "parse_ok_all": all(r.get("parse_ok") for r in rounds),
            }
        )

    by_arm: dict[str, list[dict[str, Any]]] = {}
    for r in rows:
        by_arm.setdefault(r["arm"], []).append(r)

    per_arm: dict[str, Any] = {}
    for arm, arm_rows in by_arm.items():
        per_arm[arm] = {
            "n_sessions": len(arm_rows),
            "cumulative_tokens_median": _median([float(r["cumulative_tokens_final"]) for r in arm_rows]),
            "s0_tokens_median": _median([float(r["s0_tokens"]) for r in arm_rows if r.get("s0_tokens")]),
            "s2_leakage_sum_mean": round(
                statistics.mean([r["s2_leakage_sum"] for r in arm_rows]), 2
            )
            if arm_rows
            else None,
        }

    return {
        "schema": "gate_ctx_ab_s1s2_aggregate_v1",
        "parent_run_id": bi.get("parent_run_id"),
        "context_strategy": bi.get("context_strategy"),
        "sessions": rows,
        "per_arm": per_arm,
    }


def render_md(agg: dict[str, Any]) -> str:
    lines = [
        f"# S1/S2 batch aggregate — `{agg.get('parent_run_id')}`",
        "",
        f"- **策略**：{agg.get('context_strategy')}",
        f"- **会话数**：{len(agg.get('sessions') or [])}（3 题 × 2 arm）",
        "",
        "## 会话一览",
        "",
        "| task | arm | S0 wall_s | S0 tokens | 累计 tokens | S2 泄漏合计 |",
        "| --- | --- | ---:| ---:| ---:| ---:|",
    ]
    for r in agg.get("sessions") or []:
        lines.append(
            f"| `{r['task_id']}` | `{r['arm']}` | {r.get('s0_wall_s')} | {r.get('s0_tokens')} | "
            f"**{r.get('cumulative_tokens_final')}** | {r.get('s2_leakage_sum')} |"
        )
    lines.extend(["", "## 按 arm 中位数", "", "| arm | 累计 token 中位数 | S0 token 中位数 | S2 泄漏均值 |", "| --- | ---:| ---:| ---:|"])
    for arm, v in (agg.get("per_arm") or {}).items():
        lines.append(
            f"| `{arm}` | {v.get('cumulative_tokens_median')} | {v.get('s0_tokens_median')} | {v.get('s2_leakage_sum_mean')} |"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("batch_dir", type=Path)
    args = p.parse_args()
    agg = aggregate(args.batch_dir)
    (args.batch_dir / "aggregate.json").write_text(
        json.dumps(agg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (args.batch_dir / "aggregate.md").write_text(render_md(agg), encoding="utf-8")
    print(render_md(agg))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
