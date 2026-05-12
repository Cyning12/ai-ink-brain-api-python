"""Unified Chat 请求内 ChatBI 主体与日志上下文的 ContextVar（供 tools 等读取）。"""

from __future__ import annotations

from contextvars import ContextVar, Token
from typing import Any

from .chatbi_principal import ChatBiPrincipal

_principal: ContextVar[ChatBiPrincipal | None] = ContextVar("chatbi_principal", default=None)
_log_ctx: ContextVar[dict[str, Any] | None] = ContextVar("chatbi_log_ctx", default=None)


def set_chatbi_principal(p: ChatBiPrincipal | None) -> Token[ChatBiPrincipal | None]:
    return _principal.set(p)


def reset_chatbi_principal(token: Token[ChatBiPrincipal | None]) -> None:
    _principal.reset(token)


def get_chatbi_principal() -> ChatBiPrincipal | None:
    return _principal.get()


def set_chatbi_log_ctx(ctx: dict[str, Any] | None) -> Token[dict[str, Any] | None]:
    return _log_ctx.set(ctx)


def reset_chatbi_log_ctx(token: Token[dict[str, Any] | None]) -> None:
    _log_ctx.reset(token)


def get_chatbi_log_ctx() -> dict[str, Any] | None:
    return _log_ctx.get()
