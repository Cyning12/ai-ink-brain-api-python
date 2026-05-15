# -*- coding: utf-8 -*-
"""环境变量与默认模型（可通过 CLI 覆盖）。"""

from __future__ import annotations

import os
from dataclasses import dataclass


# 双人盲审固定池（不使用 SILICONFLOW_CHAT_MODEL）；顺序由 CLI 随机洗牌后赋给 R1/R2。
SILICONFLOW_REVIEWER_MODEL_POOL: tuple[str, ...] = (
    "deepseek-ai/DeepSeek-V4-Flash",
    "Pro/moonshotai/Kimi-K2.6",
)


@dataclass
class ReviewRuntimeConfig:
    """运行时配置（API Key 仅从环境读取，禁止硬编码）。"""

    backend: str  # siliconflow | openai | anthropic
    model: str | None
    siliconflow_api_key: str | None
    siliconflow_base_url: str
    openai_api_key: str | None
    anthropic_api_key: str | None
    webhook_url: str | None
    max_retries: int
    retry_base_seconds: float

    @classmethod
    def from_env(
        cls,
        backend: str | None = None,
        model: str | None = None,
        webhook_url: str | None = None,
        max_retries: int = 5,
        retry_base_seconds: float = 1.5,
    ) -> ReviewRuntimeConfig:
        # 默认走 SiliconFlow（与 chain_chat 一致使用 SILICONFLOW_API_KEY）
        b = (backend or os.environ.get("RUBRIC_REVIEW_BACKEND") or "siliconflow").strip().lower()
        if b not in ("siliconflow", "openai", "anthropic"):
            raise ValueError("backend 必须是 siliconflow、openai 或 anthropic")

        sf_base = os.getenv("SILICONFLOW_BASE_URL", "https://api.siliconflow.cn/v1").rstrip("/")
        sf_key = os.getenv("SILICONFLOW_API_KEY", "").strip() or None
        if b == "siliconflow":
            try:
                from api.rag_env import must_siliconflow_api_key, siliconflow_base

                sf_key = must_siliconflow_api_key()
                sf_base = siliconflow_base()
            except Exception:  # noqa: BLE001
                pass

        return cls(
            backend=b,
            model=model or os.environ.get("RUBRIC_REVIEW_MODEL"),
            siliconflow_api_key=sf_key,
            siliconflow_base_url=sf_base,
            openai_api_key=os.environ.get("OPENAI_API_KEY"),
            anthropic_api_key=os.environ.get("ANTHROPIC_API_KEY"),
            webhook_url=(webhook_url or os.environ.get("RUBRIC_REVIEW_WEBHOOK_URL") or "").strip() or None,
            max_retries=max_retries,
            retry_base_seconds=retry_base_seconds,
        )

    def default_model(self) -> str:
        """openai/anthropic 单模型模式；siliconflow 双人盲审不在此取模型。"""
        if self.model:
            return self.model
        if self.backend == "openai":
            return os.environ.get("RUBRIC_REVIEW_OPENAI_MODEL", "gpt-4o-mini")
        if self.backend == "anthropic":
            return os.environ.get("RUBRIC_REVIEW_ANTHROPIC_MODEL", "claude-3-5-sonnet-20241022")
        # siliconflow：占位，真实模型见 meta reviewer_r1_model / reviewer_r2_model
        return "siliconflow:see-meta"
