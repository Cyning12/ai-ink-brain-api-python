# -*- coding: utf-8 -*-
"""多轮 Rubric 批跑：读 manifest，每轮写单轮报告，再生成合并总报告。"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from tools.rubric_review.config import ReviewRuntimeConfig
from tools.rubric_review.report import state_to_json_dict
from tools.rubric_review.runner import execute_single_review, pick_reviewer_models, slugify

from tools.rubric_review.paths import default_rubric_runs_dir


def _load_manifest(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in (".yaml", ".yml"):
        data = yaml.safe_load(text)
    else:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError("manifest 根必须是对象")
    return data


def _resolve_path(manifest_dir: Path, p: str) -> Path:
    raw = Path(p)
    if raw.is_absolute():
        return raw.resolve()
    return (manifest_dir / raw).resolve()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="多轮 Rubric 评审：manifest 列出每轮 artifact，一键生成各轮报告 + 合并总览",
    )
    parser.add_argument("--manifest", required=True, help="manifest 路径（.json / .yaml）")
    parser.add_argument("--rubric", help="覆盖 manifest 内的 rubric 路径")
    parser.add_argument(
        "--output-dir",
        default=str(default_rubric_runs_dir()),
        help="单轮与合并报告输出目录（默认 docs/diary/jsonPKmermaid/rubric_runs）",
    )
    parser.add_argument(
        "--backend",
        choices=("siliconflow", "openai", "anthropic"),
        help="覆盖 RUBRIC_REVIEW_BACKEND",
    )
    parser.add_argument("--model", help="仅 openai/anthropic")
    parser.add_argument("--webhook-url", help="覆盖 RUBRIC_REVIEW_WEBHOOK_URL")
    parser.add_argument(
        "--arbitration-override",
        choices=("llm", "human_webhook"),
        default=None,
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=None,
        help="整次多轮共用：模型分配种子；各轮 stem 仍带序号区分",
    )
    parser.add_argument(
        "--webhook-per-round",
        action="store_true",
        help="每轮结束后发送 webhook（默认关闭，避免刷屏）",
    )
    parser.add_argument("--max-retries", type=int, default=5)
    parser.add_argument("--log-file", help="追加日志")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    if args.log_file:
        handlers.append(logging.FileHandler(args.log_file, encoding="utf-8"))
    logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s", handlers=handlers)
    log = logging.getLogger("tools.rubric_review.multi_round")

    manifest_path = Path(args.manifest).resolve()
    if not manifest_path.is_file():
        log.error("manifest 不存在: %s", manifest_path)
        return 2

    man = _load_manifest(manifest_path)
    manifest_dir = manifest_path.parent

    run_name = str(man.get("run_name") or slugify(manifest_path.stem))
    rounds_raw = man.get("rounds")
    if not isinstance(rounds_raw, list) or not rounds_raw:
        log.error("manifest.rounds 必须为非空数组")
        return 2

    rubric_rel = args.rubric or man.get("rubric")
    if not rubric_rel or not isinstance(rubric_rel, str):
        log.error("请提供 rubric：manifest.rubric 或 --rubric")
        return 2
    rubric_path = _resolve_path(manifest_dir, rubric_rel)
    if not rubric_path.is_file():
        log.error("Rubric 不存在: %s", rubric_path)
        return 2
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))

    cfg = ReviewRuntimeConfig.from_env(
        backend=args.backend,
        model=args.model,
        webhook_url=args.webhook_url,
        max_retries=max(1, args.max_retries),
    )

    seed = args.random_seed
    if seed is None and man.get("random_seed") is not None:
        seed = int(man["random_seed"])
    rng = random.Random(seed) if seed is not None else random.Random()
    triple = pick_reviewer_models(cfg, rng)
    log.info(
        "多轮共用模型分配 R1=%s R2=%s arbitration=%s seed=%s",
        triple[0],
        triple[1],
        triple[2],
        seed,
    )

    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    batch_stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    round_rows: list[dict[str, Any]] = []
    exit_max = 0

    for idx, item in enumerate(rounds_raw):
        if not isinstance(item, dict):
            log.error("rounds[%s] 必须为对象", idx)
            return 2
        rid = str(item.get("id") or f"R{idx}")
        art_rel = item.get("artifact_file")
        if not art_rel or not isinstance(art_rel, str):
            log.error("rounds[%s] 缺少 artifact_file", idx)
            return 2
        art_path = _resolve_path(manifest_dir, art_rel)
        if not art_path.is_file():
            log.error("工件不存在: %s", art_path)
            return 2
        artifact_text = art_path.read_text(encoding="utf-8")
        stem = f"rubric_review_{slugify(run_name)}_{slugify(rid)}_{batch_stamp}_{idx:02d}"

        res = execute_single_review(
            artifact_text=artifact_text,
            artifact_path_display=str(art_path),
            rubric=rubric,
            rubric_path=rubric_path,
            cfg=cfg,
            reviewer_models=triple,
            random_seed=seed,
            arbitration_override=args.arbitration_override,
            output_dir=out_dir,
            stem=stem,
            send_webhooks=bool(args.webhook_per_round),
        )
        if res.state.arbitration_mode == "human_pending":
            exit_max = max(exit_max, 3)

        round_rows.append(
            {
                "round_id": rid,
                "artifact_file": str(art_path),
                "stem": stem,
                "markdown": str(res.md_path),
                "json": str(res.json_path),
                "final_scores": res.state.final_scores,
                "arbitration_needed": res.state.arbitration_needed,
                "detail": state_to_json_dict(res.state, extra=res.extra),
            }
        )

    # 合并总报告
    summary_stem = f"rubric_multiround_{slugify(run_name)}_{batch_stamp}"
    summary_md = out_dir / f"{summary_stem}.md"
    summary_json = out_dir / f"{summary_stem}.json"

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    dim_ids = [d["id"] for d in rubric.get("dimensions", [])]

    md_lines: list[str] = [
        "# Rubric 多轮评审 — 合并总报告",
        "",
        "## 元信息",
        "",
        "| 字段 | 值 |",
        "|------|-----|",
        f"| 生成时间（UTC） | {now} |",
        f"| manifest | `{manifest_path}` |",
        f"| run_name | `{run_name}` |",
        f"| rubric | `{rubric_path}` |",
        f"| 后端 | `{cfg.backend}` |",
        f"| R1 模型 | `{triple[0]}` |",
        f"| R2 模型 | `{triple[1]}` |",
        f"| 仲裁模型 | `{triple[2]}` |",
        f"| random_seed | `{seed if seed is not None else '（未固定）'}` |",
        f"| 轮数 | {len(round_rows)} |",
        "",
        "## 各轮索引",
        "",
        "| 轮次 id | 工件 | 单轮 Markdown | 单轮 JSON |",
        "|---------|------|---------------|-----------|",
    ]
    for row in round_rows:
        md_name = Path(row["markdown"]).name
        js_name = Path(row["json"]).name
        md_lines.append(
            f"| `{row['round_id']}` | `{row['artifact_file']}` | "
            f"[{md_name}](./{md_name}) | [{js_name}](./{js_name}) |"
        )

    md_lines.extend(["", "## 各轮终分汇总", ""])
    if dim_ids:
        headers = ["轮次"] + [f"`{d}`" for d in dim_ids]
        md_lines.append("| " + " | ".join(headers) + " |")
        md_lines.append("| " + " | ".join(["---"] * len(headers)) + " |")
        for row in round_rows:
            fs = row.get("final_scores") or {}
            cells = [f"`{row['round_id']}`"] + [str(fs.get(d, "")) for d in dim_ids]
            md_lines.append("| " + " | ".join(cells) + " |")
    else:
        md_lines.append("（Rubric 无 dimensions，跳过矩阵）")

    md_lines.extend(
        [
            "",
            "## 说明",
            "",
            "- 各轮完整双人评审与仲裁细节见上表 **单轮 Markdown / JSON**；本文件仅做索引与分数矩阵。",
            "- 多轮共用 **同一组** R1/R2/仲裁模型分配（便于横向对比各轮工件）。",
            "",
        ]
    )
    summary_md.write_text("\n".join(md_lines), encoding="utf-8")

    summary_payload = {
        "run_name": run_name,
        "manifest": str(manifest_path),
        "rubric": str(rubric_path),
        "backend": cfg.backend,
        "reviewer_r1_model": triple[0],
        "reviewer_r2_model": triple[1],
        "arbitration_model": triple[2],
        "random_seed": seed,
        "batch_stamp": batch_stamp,
        "rounds": round_rows,
        "summary_markdown": str(summary_md),
    }
    summary_json.write_text(json.dumps(summary_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    log.info("合并报告: %s", summary_md)
    log.info("合并 JSON: %s", summary_json)
    return exit_max if exit_max else 0


if __name__ == "__main__":
    raise SystemExit(main())
