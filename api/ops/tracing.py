"""Ops Desk · LangSmith 可选 tracing（未开启时 no-op）。

官方：https://docs.langchain.com/langsmith/annotate-code
规划：Projects/docs/harness/guides/GUIDE_ops_desk_langsmith_eval_v1_zh.md
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def tracing_enabled() -> bool:
    """是否向 LangSmith 发送 trace。"""
    return os.getenv("LANGSMITH_TRACING", "").strip().lower() in ("1", "true", "yes")


def traceable(*decorator_args: Any, **decorator_kwargs: Any) -> Callable[[F], F] | F:
    """与 langsmith.traceable 签名兼容；未安装或未开启时透传原函数。"""

    def _wrap(fn: F) -> F:
        if not tracing_enabled():
            return fn
        try:
            from langsmith import traceable as ls_traceable
        except ImportError:
            return fn
        return ls_traceable(*decorator_args, **decorator_kwargs)(fn)

    if len(decorator_args) == 1 and callable(decorator_args[0]) and not decorator_kwargs:
        return _wrap(decorator_args[0])
    return _wrap


def flush_traces() -> None:
    """短脚本/CI 结束前 flush；未开启或无 client 时静默跳过。"""
    if not tracing_enabled():
        return
    try:
        from langsmith import Client
    except ImportError:
        return
    Client().flush()
