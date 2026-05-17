#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汇总 Phase·P1 双人盲审 CSV，标出需 Reviewer·R3 仲裁的样本。"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

_REPO = Path(__file__).resolve()
P1_ROOT = _REPO.parents[1] / "p1"
RUBRIC_PATH = P1_ROOT / "rubric_v1.yaml"
THRESHOLD = 15


def _load_threshold() -> int:
    if not RUBRIC_PATH.is_file():
        return THRESHOLD
    text = RUBRIC_PATH.read_text(encoding="utf-8")
    for line in text.splitlines():
        if line.strip().startswith("arbitration_threshold:"):
            raw = line.split(":", 1)[1].strip().split("#", 1)[0].strip()
            return int(raw)
    return THRESHOLD


def _read_scores(path: Path) -> dict[str, dict[str, int]]:
    out: dict[str, dict[str, int]] = {}
    with path.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = row["sample_id"].strip()
            out[sid] = {
                "p1_total": int(row["p1_total"]),
                "p2_total": int(row["p2_total"]),
            }
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scores-dir",
        type=Path,
        default=P1_ROOT / "scores",
    )
    parser.add_argument(
        "--out-md",
        type=Path,
        default=P1_ROOT / "scores" / "aggregate_p1.md",
    )
    args = parser.parse_args()
    scores_dir = args.scores_dir.resolve()
    r1_path = scores_dir / "reviewer_R1.csv"
    r2_path = scores_dir / "reviewer_R2.csv"
    if not r1_path.is_file() or not r2_path.is_file():
        print("缺少 reviewer_R1.csv 或 reviewer_R2.csv", file=__import__("sys").stderr)
        return 2

    threshold = _load_threshold()
    s1 = _read_scores(r1_path)
    s2 = _read_scores(r2_path)
    all_ids = sorted(set(s1) | set(s2))
    lines = [
        "# Phase·P1 盲审汇总",
        "",
        f"- **仲裁阈值**：|Reviewer·R1 − R2| ≥ {threshold}（分 P1 或 P2）",
        "",
        "| sample_id | R1 P1 | R1 P2 | R2 P1 | R2 P2 | ΔP1 | ΔP2 | 需仲裁 |",
        "| --- | ---:| ---:| ---:| ---:| ---:| ---:| --- |",
    ]
    need_arb = 0
    for sid in all_ids:
        a, b = s1.get(sid), s2.get(sid)
        if not a or not b:
            lines.append(f"| `{sid}` | — | — | — | — | — | — | 缺行 |")
            continue
        d1 = abs(a["p1_total"] - b["p1_total"])
        d2 = abs(a["p2_total"] - b["p2_total"])
        arb = d1 >= threshold or d2 >= threshold
        if arb:
            need_arb += 1
        lines.append(
            f"| `{sid}` | {a['p1_total']} | {a['p2_total']} | {b['p1_total']} | {b['p2_total']} | {d1} | {d2} | {'是' if arb else '否'} |"
        )
    lines.extend(["", f"**需仲裁**：{need_arb} / {len(all_ids)}", ""])

    manifest_path = P1_ROOT / "admin" / "sample_manifest.json"
    if manifest_path.is_file():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        arm_rows: dict[str, list[tuple[int, int, int, int]]] = {}
        for item in manifest.get("samples", []):
            sid = item["sample_id"]
            arm = item["arm"]
            a, b = s1.get(sid), s2.get(sid)
            if not a or not b:
                continue
            mid_p1 = round((a["p1_total"] + b["p1_total"]) / 2)
            mid_p2 = round((a["p2_total"] + b["p2_total"]) / 2)
            arm_rows.setdefault(arm, []).append(
                (mid_p1, mid_p2, a["p1_total"], b["p1_total"])
            )
        lines.extend(
            [
                "",
                "## 按 arm 粗算（R1/R2 中位数；仲裁前 provisional）",
                "",
                "| arm | 样本 n | P1 均值 | P2 均值 | 说明 |",
                "| --- | ---:| ---:| ---:| --- |",
            ]
        )
        for arm in sorted(arm_rows):
            rows = arm_rows[arm]
            p1m = round(sum(r[0] for r in rows) / len(rows))
            p2m = round(sum(r[1] for r in rows) / len(rows))
            lines.append(
                f"| `{arm}` | {len(rows)} | {p1m} | {p2m} | 各样本 (R1+P2)/2 再题均 |"
            )
        lines.append("")
        lines.append(
            "> 有仲裁项时，终值应以 Reviewer·R3 或双人合议为准；本节不改动 Rule·R1–R6。"
        )

    args.out_md.write_text("\n".join(lines), encoding="utf-8")
    print(f"OK -> {args.out_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
