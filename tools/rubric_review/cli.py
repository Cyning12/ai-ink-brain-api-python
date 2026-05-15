# -*- coding: utf-8 -*-
"""CLI：``python -m tools.rubric_review``。"""

from __future__ import annotations

import argparse
import json
import logging
import random
import re
import sys
from datetime import datetime
from pathlib import Path

from tools.rubric_review.config import (
    SILICONFLOW_REVIEWER_MODEL_POOL,
    ReviewRuntimeConfig,
)
from tools.rubric_review.report import state_to_json_dict, write_reports
from tools.rubric_review.reviewer import DoubleBlindReviewer
from tools.rubric_review.webhook import build_generic_arbitration_payload, post_webhook

REPO_ROOT = Path(__file__).resolve().parents[2]


def _slugify(s: str) -> str:
    s = re.sub(r"[^\w\-]+", "-", s, flags=re.UNICODE).strip("-")
    return s[:80] or "artifact"


def _pick_reviewer_models(cfg: ReviewRuntimeConfig, rng: random.Random) -> tuple[str, str, str]:
    """返回 (R1, R2, 仲裁)。siliconflow：池内两模型洗牌分配 R1/R2，仲裁再从池中随机选一。"""
    if cfg.backend == "siliconflow":
        pool = list(SILICONFLOW_REVIEWER_MODEL_POOL)
        if len(pool) < 2:
            raise ValueError("SILICONFLOW_REVIEWER_MODEL_POOL 至少需 2 个模型")
        rng.shuffle(pool)
        m_r1, m_r2 = pool[0], pool[1]
        m_arb = rng.choice(list(SILICONFLOW_REVIEWER_MODEL_POOL))
        return m_r1, m_r2, m_arb
    m = cfg.default_model()
    return m, m, m


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
        default=str(REPO_ROOT / "docs" / "harness" / "reviews"),
        help="Markdown/JSON 输出目录（默认本仓 docs/harness/reviews）",
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
    triple = _pick_reviewer_models(cfg, rng)
    log.info("模型分配 R1=%s R2=%s arbitration=%s seed=%s", triple[0], triple[1], triple[2], args.random_seed)

    reviewer = DoubleBlindReviewer(
        rubric,
        cfg,
        reviewer_models=triple,
        random_seed=args.random_seed,
    )
    state = reviewer.run(artifact_text, arbitration_override=override)

    slug = args.slug or _slugify(artifact_path.stem)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    stem = f"rubric_review_{slug}_{stamp}"

    out_dir = Path(args.output_dir).resolve()
    extra = {
        "artifact_file": str(artifact_path),
        "rubric_file": str(rubric_path),
        "backend": cfg.backend,
        "slug": stem,
        "reviewer_r1_model": state.meta.get("reviewer_r1_model"),
        "reviewer_r2_model": state.meta.get("reviewer_r2_model"),
        "arbitration_model": state.meta.get("arbitration_model"),
        "random_seed": state.meta.get("random_seed"),
    }

    json_path, md_path = write_reports(
        state,
        output_dir=out_dir,
        stem=stem,
        artifact_path=str(artifact_path),
        rubric_path=str(rubric_path),
        backend=cfg.backend,
        extra=extra,
    )

    webhook_url = cfg.webhook_url
    if webhook_url and state.arbitration_needed and state.disputed_dimensions:
        payload = build_generic_arbitration_payload(
            event="rubric_review.dispute_opened",
            summary_text=(
                f"Rubric 评审存在争议维度: {', '.join(state.disputed_dimensions)}\n"
                f"工件: {artifact_path}\n模式: {state.arbitration_mode}\n"
                f"R1={state.meta.get('reviewer_r1_model')} R2={state.meta.get('reviewer_r2_model')}\n"
                f"Markdown: {md_path}\nJSON: {json_path}\n"
            ),
            detail=state_to_json_dict(
                state,
                extra={**extra, "markdown": str(md_path), "json": str(json_path)},
            ),
        )
        log.info("发送 webhook（争议已打开）: %s...", webhook_url[:48])
        post_webhook(webhook_url, payload, max_retries=cfg.max_retries, retry_base_seconds=cfg.retry_base_seconds)

    if webhook_url and state.arbitration_mode == "llm" and state.arbitration_needed:
        payload2 = build_generic_arbitration_payload(
            event="rubric_review.arbitration_llm_done",
            summary_text=f"LLM 仲裁已完成。Markdown: {md_path}",
            detail=state_to_json_dict(state, extra={**extra, "markdown": str(md_path), "json": str(json_path)}),
        )
        post_webhook(webhook_url, payload2, max_retries=cfg.max_retries, retry_base_seconds=cfg.retry_base_seconds)

    if webhook_url and state.arbitration_mode == "human_pending":
        payload3 = build_generic_arbitration_payload(
            event="rubric_review.human_arbitration_required",
            summary_text="需人工仲裁（未调用 LLM）。终分含 null。",
            detail=state_to_json_dict(state, extra={**extra, "markdown": str(md_path), "json": str(json_path)}),
        )
        post_webhook(webhook_url, payload3, max_retries=cfg.max_retries, retry_base_seconds=cfg.retry_base_seconds)

    log.info("已写入: %s", md_path)
    log.info("已写入: %s", json_path)

    if state.arbitration_mode == "human_pending":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
