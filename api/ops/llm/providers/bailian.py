"""Bailian (DashScope OpenAI 兼容) Provider。"""

from __future__ import annotations

import os
from typing import Any

from api.ops.llm.errors import OpsLlmMisconfiguredError
from api.ops.llm.model_catalog import BAILIAN_DEFAULT_MODEL, resolve_bailian_model_chain
from api.ops.llm.providers.base import OpsLlmProvider
from api.ops.llm.providers.openai_compatible import openai_compatible_complete_with_policy
from api.ops.llm.types import LlmCompletionResult

_DEFAULT_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"


class BailianProvider(OpsLlmProvider):
    """百炼 DashScope OpenAI 兼容 Chat Completions Provider。"""

    @property
    def name(self) -> str:
        return "bailian"

    def _api_key(self) -> str:
        return (os.getenv("BAILIAN_API_KEY") or os.getenv("DASHSCOPE_API_KEY") or "").strip()

    def _model(self, override: str | None = None) -> str:
        if override:
            return override.strip()
        return (os.getenv("BAILIAN_MODEL") or BAILIAN_DEFAULT_MODEL).strip()

    def _base(self) -> str:
        return (os.getenv("BAILIAN_BASE_URL") or _DEFAULT_BASE_URL).strip()

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
            raise OpsLlmMisconfiguredError("缺少 LLM API Key（BAILIAN_API_KEY / DASHSCOPE_API_KEY）")

        primary = self._model(model)
        model_chain = resolve_bailian_model_chain(primary)
        return openai_compatible_complete_with_policy(
            provider=self.name,
            base_url=self._base(),
            api_key=key,
            model_chain=model_chain,
            messages=messages,
            temperature=temperature,
            step=str(kwargs.get("step", "other")),
            quota_model_switch=True,
        )
