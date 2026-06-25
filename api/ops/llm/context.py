"""Ops Desk LLM 请求级上下文（单次 chat 选模）。"""

from __future__ import annotations

from contextvars import ContextVar

ops_chat_model_override: ContextVar[str | None] = ContextVar("ops_chat_model_override", default=None)
# 单次 chat 请求内：首次 LLM 成功后固定模型，避免多步 orchestrator 重复从 test 模型重走链
ops_chat_resolved_model: ContextVar[str | None] = ContextVar("ops_chat_resolved_model", default=None)
