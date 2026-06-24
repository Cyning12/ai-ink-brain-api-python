"""Ops Desk · 可选 LLM tracing（Langfuse 优先 · LangSmith 兼容 · 未开启时 no-op）。

Langfuse：https://langfuse.com/docs/observability/get-started
LangSmith：https://docs.langchain.com/langsmith/annotate-code
规划：Projects/docs/harness/guides/GUIDE_ops_desk_langfuse_eval_v1_zh.md
"""

from __future__ import annotations

import os
from collections.abc import Callable
from typing import Any, Literal, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

Provider = Literal["langfuse", "langsmith", "none"]

_RUN_TYPE_TO_LANGFUSE_AS_TYPE: dict[str, str] = {
    "llm": "generation",
    "chain": "chain",
    "tool": "tool",
    "retriever": "retriever",
}


def _truthy(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in ("1", "true", "yes")


def _langfuse_configured() -> bool:
    return bool(
        (os.getenv("LANGFUSE_PUBLIC_KEY") or os.getenv("LANGFUSE_SECRET_KEY") or "").strip()
        and (os.getenv("LANGFUSE_SECRET_KEY") or "").strip()
    )


def tracing_provider() -> Provider:
    """当前 tracing 后端；未开启时为 none。"""
    if _truthy("LANGFUSE_TRACING") and _langfuse_configured():
        return "langfuse"
    if _truthy("LANGSMITH_TRACING"):
        return "langsmith"
    return "none"


def tracing_enabled() -> bool:
    """是否向 Langfuse / LangSmith 发送 trace。"""
    return tracing_provider() != "none"


def traceable(*decorator_args: Any, **decorator_kwargs: Any) -> Callable[[F], F] | F:
    """与 langsmith.traceable / langfuse.observe 签名近似；未安装或未开启时透传原函数。"""

    def _wrap(fn: F) -> F:
        provider = tracing_provider()
        if provider == "none":
            return fn
        if provider == "langfuse":
            return _langfuse_observe(fn, decorator_args, decorator_kwargs)
        return _langsmith_traceable(fn, decorator_args, decorator_kwargs)

    if len(decorator_args) == 1 and callable(decorator_args[0]) and not decorator_kwargs:
        return _wrap(decorator_args[0])
    return _wrap


def _langfuse_observe(fn: F, decorator_args: tuple[Any, ...], decorator_kwargs: dict[str, Any]) -> F:
    try:
        from langfuse import observe
    except ImportError:
        return fn

    name = decorator_kwargs.get("name")
    run_type = decorator_kwargs.get("run_type")
    as_type = decorator_kwargs.get("as_type")
    if as_type is None and isinstance(run_type, str):
        as_type = _RUN_TYPE_TO_LANGFUSE_AS_TYPE.get(run_type, "span")

    observe_kwargs: dict[str, Any] = {}
    if name is not None:
        observe_kwargs["name"] = name
    if as_type is not None:
        observe_kwargs["as_type"] = as_type
    for key in ("capture_input", "capture_output"):
        if key in decorator_kwargs:
            observe_kwargs[key] = decorator_kwargs[key]

    if decorator_args or observe_kwargs:
        return observe(*decorator_args, **observe_kwargs)(fn)
    return observe(fn)


def _langsmith_traceable(fn: F, decorator_args: tuple[Any, ...], decorator_kwargs: dict[str, Any]) -> F:
    try:
        from langsmith import traceable as ls_traceable
    except ImportError:
        return fn
    return ls_traceable(*decorator_args, **decorator_kwargs)(fn)


def flush_traces() -> None:
    """短脚本/CI 结束前 flush；未开启或无 client 时静默跳过。"""
    provider = tracing_provider()
    if provider == "langfuse":
        try:
            from langfuse import get_client

            get_client().flush()
        except Exception:
            return
    elif provider == "langsmith":
        try:
            from langsmith import Client

            Client().flush()
        except Exception:
            return


def update_current_span_metadata(metadata: dict[str, Any]) -> None:
    """为当前 Langfuse span/observation 附加 metadata；未开启或失败时静默跳过。

    用于 deep 路径根 span 写入 ops_run_id / route / intent / issue_number 等结构化标签。
    """
    if tracing_provider() != "langfuse":
        return
    try:
        from langfuse import get_client

        get_client().update_current_span(metadata=metadata)
    except Exception:
        return
