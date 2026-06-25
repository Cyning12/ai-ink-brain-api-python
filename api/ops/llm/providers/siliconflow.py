"""SiliconFlow Provider（从 api/ops/llm.py 迁入）。"""

from __future__ import annotations

import os
from typing import Any

from api.ops.llm.errors import OpsLlmMisconfiguredError
from api.ops.llm.model_catalog import SILICONFLOW_DEFAULT_MODEL
from api.ops.llm.providers.base import OpsLlmProvider
from api.ops.llm.providers.openai_compatible import openai_compatible_complete
from api.ops.llm.types import LlmCompletionResult


class SiliconFlowProvider(OpsLlmProvider):
    """SiliconFlow OpenAI 兼容 API Provider。"""

    @property
    def name(self) -> str:
        return "siliconflow"

    def _api_key(self) -> str:
        return (os.getenv("SILICONFLOW_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()

    def _model(self, override: str | None = None) -> str:
        if override:
            return override.strip()
        return (os.getenv("OPS_LLM_MODEL") or SILICONFLOW_DEFAULT_MODEL).strip()

    def _base(self) -> str:
        return (os.getenv("OPS_LLM_BASE") or "https://api.siliconflow.cn/v1").strip()

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.3,
        model: str | None = None,
        **kwargs: Any,
    ) -> LlmCompletionResult:
        key = self._api_key()
        if not key:
            raise OpsLlmMisconfiguredError("缺少 LLM API Key（SILICONFLOW_API_KEY / OPENAI_API_KEY）")

        resolved_model = self._model(model)
        return openai_compatible_complete(
            provider=self.name,
            base_url=self._base(),
            api_key=key,
            model=resolved_model,
            messages=messages,
            temperature=temperature,
            step=str(kwargs.get("step", "other")),
        )
