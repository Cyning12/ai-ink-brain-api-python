#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从 P0-B 批跑抽取 6 条段·S0 输出，生成 Phase·P1 盲审包。"""

from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

_REPO = Path(__file__).resolve()
FIXTURE_ROOT = _REPO.parents[1]
JSONPK_ROOT = FIXTURE_ROOT.parent.parent  # docs/diary/jsonPKmermaid
P1_ROOT = FIXTURE_ROOT / "p1"
TASKS_PATH = FIXTURE_ROOT / "tasks.json"
DEFAULT_BATCH = (
    JSONPK_ROOT / "runs" / "gate_ctx_ab_v1_s1s2_20260516_152126"
)

# 固定种子：盲审序号可复现；admin  manifest 记录真实 arm
_BLIND_ORDER_SEED = 20260517


def _load_tasks() -> dict[str, dict]:
    data = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    return {t["task_id"]: t for t in data["tasks"]}


def _collect_s0_records(batch_dir: Path) -> list[dict]:
    records: list[dict] = []
    for path in sorted(batch_dir.glob("**/raw/*_S0.jsonl")):
        line = path.read_text(encoding="utf-8").strip().splitlines()[0]
        rec = json.loads(line)
        if rec.get("status") != "ok" or not rec.get("parse_ok"):
            raise RuntimeError(f"无效 S0 记录: {path}")
        records.append(
            {
                "source_jsonl": str(path.relative_to(JSONPK_ROOT)),
                "arm": rec["arm"],
                "primary_task_id": rec["primary_task_id"],
                "topic_id": rec["topic_id"],
                "response": rec.get("response") or {},
                "usage": rec.get("usage") or {},
            }
        )
    if len(records) != 6:
        raise RuntimeError(f"期望 6 条 S0，实际 {len(records)} @ {batch_dir}")
    return records


def main() -> int:
    parser = argparse.ArgumentParser(description="生成 P1 盲审包")
    parser.add_argument(
        "--batch-dir",
        type=Path,
        default=DEFAULT_BATCH,
        help="P0-B 全量目录（含 6×S0 jsonl）",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=P1_ROOT,
        help="输出根目录（默认 fixtures/.../p1）",
    )
    args = parser.parse_args()
    batch_dir = args.batch_dir.resolve()
    out_dir = args.out_dir.resolve()
    blind_dir = out_dir / "blind"
    admin_dir = out_dir / "admin"
    scores_dir = out_dir / "scores"
    for d in (blind_dir, admin_dir, scores_dir):
        d.mkdir(parents=True, exist_ok=True)

    tasks = _load_tasks()
    records = _collect_s0_records(batch_dir)

    # 按 task_id、arm 排序后，用固定种子打乱盲审序号（非打乱题内顺序）
    records.sort(key=lambda r: (r["primary_task_id"], r["arm"]))
    indexed = list(enumerate(records))
    rng = random.Random(_BLIND_ORDER_SEED)
    rng.shuffle(indexed)

    manifest: list[dict] = []
    for blind_idx, (_orig_i, rec) in enumerate(indexed, start=1):
        sample_id = f"P1-{blind_idx:03d}"
        task_id = rec["primary_task_id"]
        task = tasks[task_id]
        blind_doc = {
            "schema": "gate_ctx_p1_blind_sample_v1",
            "sample_id": sample_id,
            "task_id": task_id,
            "topic_id": rec["topic_id"],
            "segment": "S0",
            "prompt_zh": task["prompt_zh"],
            "gold": task["gold"],
            "response": rec["response"],
            "reviewer_note": "盲审：不得根据措辞猜测 arm；仅对照 gold 与 rubric_v1.yaml",
        }
        (blind_dir / f"{sample_id}_{task_id[:4]}.json").write_text(
            json.dumps(blind_doc, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        manifest.append(
            {
                "sample_id": sample_id,
                "task_id": task_id,
                "arm": rec["arm"],
                "source_jsonl": rec["source_jsonl"],
                "usage_total_tokens": (rec.get("usage") or {}).get("total_tokens"),
            }
        )

    (admin_dir / "sample_manifest.json").write_text(
        json.dumps(
            {
                "schema": "gate_ctx_p1_admin_manifest_v1",
                "batch_dir": str(batch_dir),
                "blind_order_seed": _BLIND_ORDER_SEED,
                "samples": manifest,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"OK blind samples -> {blind_dir} ({len(manifest)} files)")
    print(f"OK admin manifest -> {admin_dir / 'sample_manifest.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
