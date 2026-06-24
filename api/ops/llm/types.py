"""Ops Desk LLM Provider 类型定义。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class LlmUsage:
    """单次 LLM 调用用量。"""

    provider: str = ""
    model: str = ""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: int = 0
    step: str = "other"
    usage_missing: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "prompt_tokens": self.prompt_tokens,
            "completion_tokens": self.completion_tokens,
            "total_tokens": self.total_tokens,
            "latency_ms": self.latency_ms,
            "step": self.step,
            "usage_missing": self.usage_missing,
        }


@dataclass
class LlmCompletionResult:
    """LLM 调用结果：content + usage。"""

    content: str = ""
    usage: LlmUsage = field(default_factory=LlmUsage)

    def to_dict(self) -> dict[str, Any]:
        return {
            "content": self.content,
            "usage": self.usage.to_dict(),
        }
