# -*- coding: utf-8 -*-
"""单次 Rubric 评审执行（供 CLI 与多轮批跑复用）。"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from tools.rubric_review.config import (
    SILICONFLOW_REVIEWER_MODEL_POOL,
    ReviewRuntimeConfig,
)
from tools.rubric_review.report import state_to_json_dict, write_reports
from tools.rubric_review.reviewer import DoubleBlindReviewer, FullReviewState
from tools.rubric_review.webhook import build_generic_arbitration_payload, post_webhook

logger = logging.getLogger(__name__)


def slugify(s: str) -> str:
    s = re.sub(r"[^\w\-]+", "-", s, flags=re.UNICODE).strip("-")
    return s[:80] or "artifact"


def pick_reviewer_models(cfg: ReviewRuntimeConfig, rng: random.Random) -> tuple[str, str, str]:
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


@dataclass
class SingleReviewResult:
    state: FullReviewState
    md_path: Path
    json_path: Path
    stem: str
    extra: dict[str, Any]


def execute_single_review(
    *,
    artifact_text: str,
    artifact_path_display: str,
    rubric: dict[str, Any],
    rubric_path: Path,
    cfg: ReviewRuntimeConfig,
    reviewer_models: tuple[str, str, str],
    random_seed: int | None,
    arbitration_override: str | None,
    output_dir: Path,
    stem: str,
    send_webhooks: bool,
) -> SingleReviewResult:
    """执行一轮双人评审 + 写盘 + 可选 webhook。"""
    reviewer = DoubleBlindReviewer(
        rubric,
        cfg,
        reviewer_models=reviewer_models,
        random_seed=random_seed,
    )
    state = reviewer.run(artifact_text, arbitration_override=arbitration_override)

    extra: dict[str, Any] = {
        "artifact_file": artifact_path_display,
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
        output_dir=output_dir,
        stem=stem,
        artifact_path=artifact_path_display,
        rubric_path=str(rubric_path),
        backend=cfg.backend,
        extra=extra,
    )

    webhook_url = cfg.webhook_url
    if send_webhooks and webhook_url and state.arbitration_needed and state.disputed_dimensions:
        payload = build_generic_arbitration_payload(
            event="rubric_review.dispute_opened",
            summary_text=(
                f"Rubric 评审存在争议维度: {', '.join(state.disputed_dimensions)}\n"
                f"工件: {artifact_path_display}\n模式: {state.arbitration_mode}\n"
                f"R1={state.meta.get('reviewer_r1_model')} R2={state.meta.get('reviewer_r2_model')}\n"
                f"Markdown: {md_path}\nJSON: {json_path}\n"
            ),
            detail=state_to_json_dict(state, extra={**extra, "markdown": str(md_path), "json": str(json_path)}),
        )
        post_webhook(webhook_url, payload, max_retries=cfg.max_retries, retry_base_seconds=cfg.retry_base_seconds)

    if send_webhooks and webhook_url and state.arbitration_mode == "llm" and state.arbitration_needed:
        payload2 = build_generic_arbitration_payload(
            event="rubric_review.arbitration_llm_done",
            summary_text=f"LLM 仲裁已完成。Markdown: {md_path}",
            detail=state_to_json_dict(state, extra={**extra, "markdown": str(md_path), "json": str(json_path)}),
        )
        post_webhook(webhook_url, payload2, max_retries=cfg.max_retries, retry_base_seconds=cfg.retry_base_seconds)

    if send_webhooks and webhook_url and state.arbitration_mode == "human_pending":
        payload3 = build_generic_arbitration_payload(
            event="rubric_review.human_arbitration_required",
            summary_text="需人工仲裁（未调用 LLM）。终分含 null。",
            detail=state_to_json_dict(state, extra={**extra, "markdown": str(md_path), "json": str(json_path)}),
        )
        post_webhook(webhook_url, payload3, max_retries=cfg.max_retries, retry_base_seconds=cfg.retry_base_seconds)

    logger.info("已写入: %s", md_path)
    return SingleReviewResult(state=state, md_path=md_path, json_path=json_path, stem=stem, extra=extra)
