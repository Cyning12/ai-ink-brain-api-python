"""Ops Desk LLM 薄封装（向后兼容 re-export）。

真实实现已迁入 api/ops/llm/__init__.py（目录包优先）。
"""

from __future__ import annotations

from api.ops.llm import chat_completion, synthesize_answer  # noqa: F401
from api.ops.llm.types import LlmCompletionResult, LlmUsage  # noqa: F401

__all__ = ["chat_completion", "synthesize_answer", "LlmCompletionResult", "LlmUsage"]
