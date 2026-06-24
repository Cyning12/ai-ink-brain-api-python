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

    @classmethod
    def from_dict(cls, data: dict[str, Any], *, step: str | None = None) -> LlmUsage:
        """从 LlmUsage.to_dict() 或嵌套 {usage: {...}} 还原。"""
        raw = data.get("usage", data) if isinstance(data.get("usage"), dict) else data
        return cls(
            provider=str(raw.get("provider", "")),
            model=str(raw.get("model", "")),
            prompt_tokens=int(raw.get("prompt_tokens", 0) or 0),
            completion_tokens=int(raw.get("completion_tokens", 0) or 0),
            total_tokens=int(raw.get("total_tokens", 0) or 0),
            latency_ms=int(raw.get("latency_ms", 0) or 0),
            step=step or str(raw.get("step", "other")),
            usage_missing=bool(raw.get("usage_missing", False)),
        )


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
