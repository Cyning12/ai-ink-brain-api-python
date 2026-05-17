# -*- coding: utf-8 -*-
"""CLI：``python -m tools.rubric_review``。"""

from __future__ import annotations

import argparse
import json
import logging
import random
import sys
from datetime import datetime
from pathlib import Path

from tools.rubric_review.config import ReviewRuntimeConfig
from tools.rubric_review.paths import default_rubric_runs_dir
from tools.rubric_review.runner import execute_single_review, pick_reviewer_models, slugify


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rubric 双人 LLM 评审 + 可选仲裁与 webhook（默认 SiliconFlow / OpenAI 兼容 / Anthropic）",
    )
    parser.add_argument("--artifact-file", required=True, help="待评审工件（UTF-8 文本）路径")
    parser.add_argument("--rubric", required=True, help="Rubric JSON 路径")
    parser.add_argument(
        "--backend",
        choices=("siliconflow", "openai", "anthropic"),
        help="覆盖环境变量 RUBRIC_REVIEW_BACKEND（默认 siliconflow）",
    )
    parser.add_argument(
        "--model",
        help="仅 openai/anthropic：单模型（R1/R2/仲裁 同源）；siliconflow 忽略 SILICONFLOW_CHAT_MODEL，改用内置池",
    )
    parser.add_argument(
        "--output-dir",
        default=str(default_rubric_runs_dir()),
        help="Markdown/JSON 输出目录（默认 docs/diary/jsonPKmermaid/rubric_runs）",
    )
    parser.add_argument("--slug", help="输出文件名 slug；默认取工件文件名")
    parser.add_argument("--webhook-url", help="覆盖环境变量 RUBRIC_REVIEW_WEBHOOK_URL")
    parser.add_argument(
        "--arbitration-override",
        choices=("llm", "human_webhook"),
        default=None,
        help="默认按 rubric.adjudication_rules.fallback；llm=强制模型仲裁；human_webhook=仅人工 webhook、争议维度终分为 null",
    )
    parser.add_argument(
        "--random-seed",
        type=int,
        default=None,
        help="固定随机种子（可复现 R1/R2/仲裁 模型分配）；默认每次不同",
    )
    parser.add_argument("--max-retries", type=int, default=5, help="API 调用最大重试次数")
    parser.add_argument("--log-file", help="追加日志文件路径（可选）")
    parser.add_argument("-v", "--verbose", action="store_true", help="DEBUG 日志")
    args = parser.parse_args(argv)

    log_level = logging.DEBUG if args.verbose else logging.INFO
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    if args.log_file:
        handlers.append(logging.FileHandler(args.log_file, encoding="utf-8"))
    logging.basicConfig(level=log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s", handlers=handlers)
    log = logging.getLogger("tools.rubric_review.cli")

    artifact_path = Path(args.artifact_file).resolve()
    rubric_path = Path(args.rubric).resolve()
    if not artifact_path.is_file():
        log.error("工件不存在: %s", artifact_path)
        return 2
    if not rubric_path.is_file():
        log.error("Rubric 不存在: %s", rubric_path)
        return 2

    artifact_text = artifact_path.read_text(encoding="utf-8")
    rubric = json.loads(rubric_path.read_text(encoding="utf-8"))

    override = args.arbitration_override
    cfg = ReviewRuntimeConfig.from_env(
        backend=args.backend,
        model=args.model,
        webhook_url=args.webhook_url,
        max_retries=max(1, args.max_retries),
    )

    rng = random.Random(args.random_seed) if args.random_seed is not None else random.Random()
    triple = pick_reviewer_models(cfg, rng)
    log.info("模型分配 R1=%s R2=%s arbitration=%s seed=%s", triple[0], triple[1], triple[2], args.random_seed)

    slug = args.slug or slugify(artifact_path.stem)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"rubric_review_{slug}_{stamp}"

    out_dir = Path(args.output_dir).resolve()
    res = execute_single_review(
        artifact_text=artifact_text,
        artifact_path_display=str(artifact_path),
        rubric=rubric,
        rubric_path=rubric_path,
        cfg=cfg,
        reviewer_models=triple,
        random_seed=args.random_seed,
        arbitration_override=override,
        output_dir=out_dir,
        stem=stem,
        send_webhooks=True,
    )

    log.info("已写入: %s", res.md_path)
    log.info("已写入: %s", res.json_path)

    if res.state.arbitration_mode == "human_pending":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
