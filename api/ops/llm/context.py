"""Ops Desk LLM 请求级上下文（单次 chat 选模）。"""

from __future__ import annotations

from contextvars import ContextVar

ops_chat_model_override: ContextVar[str | None] = ContextVar("ops_chat_model_override", default=None)
