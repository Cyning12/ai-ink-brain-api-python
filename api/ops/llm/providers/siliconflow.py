"""SiliconFlow Provider（从 api/ops/llm.py 迁入）。"""

from __future__ import annotations

import os
import time
from typing import Any

import requests

from api.ops.llm.providers.base import OpsLlmProvider
from api.ops.llm.types import LlmCompletionResult, LlmUsage


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
        return (os.getenv("OPS_LLM_MODEL") or "Qwen/Qwen2.5-72B-Instruct").strip()

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
            raise RuntimeError("缺少 LLM API Key（SILICONFLOW_API_KEY / OPENAI_API_KEY）")

        started_at = time.time()
        resp = requests.post(
            f"{self._base()}/chat/completions",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={"model": self._model(model), "messages": messages, "temperature": temperature},
            timeout=60,
        )
        resp.raise_for_status()
        data = resp.json()
        latency_ms = int((time.time() - started_at) * 1000)

        content = str(data["choices"][0]["message"]["content"])
        usage_raw = data.get("usage") or {}

        usage = LlmUsage(
            provider=self.name,
            model=self._model(model),
            prompt_tokens=int(usage_raw.get("prompt_tokens", 0)),
            completion_tokens=int(usage_raw.get("completion_tokens", 0)),
            total_tokens=int(usage_raw.get("total_tokens", 0)),
            latency_ms=latency_ms,
            step=kwargs.get("step", "other"),
            usage_missing=not bool(usage_raw),
        )
        return LlmCompletionResult(content=content, usage=usage)
