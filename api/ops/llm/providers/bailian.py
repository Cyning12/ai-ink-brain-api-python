"""Bailian (DashScope) Provider — Phase 1 stub。"""

from __future__ import annotations

from typing import Any

from api.ops.llm.providers.base import OpsLlmProvider
from api.ops.llm.types import LlmCompletionResult


class BailianProvider(OpsLlmProvider):
    """百炼 DashScope Provider — 当前仅 stub，Phase 2 实现真实调用。"""

    @property
    def name(self) -> str:
        return "bailian"

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.3,
        model: str | None = None,
        **kwargs: Any,
    ) -> LlmCompletionResult:
        raise NotImplementedError(
            "BailianProvider 尚未实现。"
            "请使用 OPS_LLM_PROVIDER=siliconflow，"
            "或等待 Phase 2 接入 DashScope OpenAI 兼容接口。"
        )
