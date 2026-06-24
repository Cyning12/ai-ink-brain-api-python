"""Ops Desk LLM Provider 抽象基类。"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from api.ops.llm.types import LlmCompletionResult


class OpsLlmProvider(ABC):
    """LLM Provider 协议；所有 provider 须实现此接口。"""

    @abstractmethod
    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.3,
        model: str | None = None,
        **kwargs: Any,
    ) -> LlmCompletionResult:
        """同步单轮 LLM 调用；返回 content + usage。"""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Provider 标识名，如 siliconflow / bailian。"""
        ...
