"""Ops Chat · 可选 LLM tracing（Langfuse / LangSmith · env 可选 · 未开启时 no-op）。

主控开关为环境变量 `OPS_CHAT_TRACER`（值 `langfuse` 或 `langsmith`）；
未设置或未知值时不启用 tracing。

为兼容旧配置，未设置 `OPS_CHAT_TRACER` 时仍识别：
- `LANGFUSE_TRACING=true` + `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY`
- `LANGSMITH_TRACING=true`

热路径使用说明：
- `@traceable(...)`：装饰函数/类方法，在函数调用周围生成 observation/run。
- `trace_span(...)`：上下文管理器，在 with 块内生成 observation/run。
- `update_current_span_metadata(...)`：给当前 observation/run 附加结构化 metadata。
- `update_current_generation_usage(...)`：将 LLM usage 同步到当前 Langfuse generation。

默认无 env 时零成本、不报错、不引入新依赖（所有第三方 SDK 均为可选 import）。
"""

from __future__ import annotations

import os
from collections.abc import Callable, Iterator
from contextlib import contextmanager
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
        (os.getenv("LANGFUSE_PUBLIC_KEY") or "").strip()
        and (os.getenv("LANGFUSE_SECRET_KEY") or "").strip()
    )


def tracing_provider() -> Provider:
    """当前 tracing 后端；未开启时为 none。

    优先级：OPS_CHAT_TRACER > 旧 LANGFUSE_TRACING/LANGSMITH_TRACING。
    """
    chat_tracer = os.getenv("OPS_CHAT_TRACER", "").strip().lower()
    if chat_tracer == "langfuse":
        return "langfuse"
    if chat_tracer == "langsmith":
        return "langsmith"
    if chat_tracer:
        # 未知值视为关闭，避免拼写错误导致静默启用
        return "none"
    # 向后兼容旧配置
    if _truthy("LANGFUSE_TRACING") and _langfuse_configured():
        return "langfuse"
    if _truthy("LANGSMITH_TRACING"):
        return "langsmith"
    return "none"


def tracing_enabled() -> bool:
    """是否向 Langfuse / LangSmith 发送 trace。"""
    return tracing_provider() != "none"


def _run_type_to_langfuse_as_type(run_type: str | None) -> str:
    return _RUN_TYPE_TO_LANGFUSE_AS_TYPE.get(run_type or "span", "span")


def traceable(*decorator_args: Any, **decorator_kwargs: Any) -> Callable[[F], F] | F:
    """与 langsmith.traceable / langfuse.observe 签名近似；未安装或未开启时透传原函数。"""

    def _wrap(fn: F) -> F:
        provider = tracing_provider()
        if provider == "none":
            return fn
        # 裸 @traceable：decorator_args[0] 即 fn，勿再传给 observe(*args)
        observe_args = (
            ()
            if len(decorator_args) == 1 and decorator_args[0] is fn and not decorator_kwargs
            else decorator_args
        )
        if provider == "langfuse":
            return _langfuse_observe(fn, observe_args, decorator_kwargs)
        return _langsmith_traceable(fn, observe_args, decorator_kwargs)

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
        as_type = _run_type_to_langfuse_as_type(run_type)

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


@contextmanager
def trace_span(
    name: str,
    *,
    run_type: str | None = None,
    **metadata: Any,
) -> Iterator[Any]:
    """上下文管理器：创建可选 trace span；未开启时零成本。

    用法：
        with trace_span("review", run_type="tool", run_id=run_id):
            verdict, detail = review_result(...)

    返回：底层 span/run 对象或 None；调用者通常不需要使用返回值。
    """
    provider = tracing_provider()
    if provider == "none":
        yield None
        return

    if provider == "langfuse":
        yield from _trace_span_langfuse(name, run_type, metadata)
    elif provider == "langsmith":
        yield from _trace_span_langsmith(name, run_type, metadata)
    else:
        yield None


def _trace_span_langfuse(
    name: str,
    run_type: str | None,
    metadata: dict[str, Any],
) -> Iterator[Any]:
    """Langfuse 版 trace_span：用 @observe 装饰 generator，使 span 覆盖整个 with 块。"""
    try:
        from langfuse import observe
    except Exception:
        yield None
        return

    as_type = _run_type_to_langfuse_as_type(run_type)

    @observe(name=name, as_type=as_type, capture_input=False, capture_output=False)
    def _gen() -> Iterator[None]:
        if metadata:
            update_current_span_metadata(metadata)
        yield None

    gen = _gen()
    try:
        next(gen)
        try:
            yield None
        finally:
            try:
                next(gen)
            except StopIteration:
                pass
    except Exception:
        # 启动 generator 失败时，仍让 with 块正常执行
        yield None


def _trace_span_langsmith(
    name: str,
    run_type: str | None,
    metadata: dict[str, Any],
) -> Iterator[Any]:
    """LangSmith 版 trace_span：使用 langsmith.trace 上下文管理器。"""
    try:
        from langsmith import trace
    except Exception:
        yield None
        return

    try:
        with trace(name=name, run_type=run_type or "span", metadata=metadata) as span:
            yield span
    except Exception:
        yield None


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
    """为当前 observation/run 附加 metadata；未开启或失败时静默跳过。

    用于 deep/react 路径根 span 写入 run_id / session_id / agent_role 等结构化标签。
    """
    provider = tracing_provider()
    if provider == "none":
        return
    if provider == "langfuse":
        _update_current_span_metadata_langfuse(metadata)
    elif provider == "langsmith":
        _update_current_span_metadata_langsmith(metadata)


def _update_current_span_metadata_langfuse(metadata: dict[str, Any]) -> None:
    try:
        from langfuse import get_client

        get_client().update_current_span(metadata=metadata)
    except Exception:
        return


def _update_current_span_metadata_langsmith(metadata: dict[str, Any]) -> None:
    try:
        from langsmith.run_helpers import get_current_run_tree

        run_tree = get_current_run_tree()
        if run_tree is not None:
            run_tree.metadata.update(metadata)
    except Exception:
        return


def update_current_generation_usage(usage: Any) -> None:
    """将 LLM usage 同步到当前 Langfuse generation；未开启或失败时静默跳过。"""
    if tracing_provider() != "langfuse":
        return
    try:
        from langfuse import get_client

        client = get_client()
        usage_details = {
            "input": int(usage.prompt_tokens or 0),
            "output": int(usage.completion_tokens or 0),
            "total": int(usage.total_tokens or 0),
        }
        # Langfuse SDK ≥4 使用 update_current_generation + usage_details；
        # 旧版 update_current_observation(usage=...) 在 4.9.x 已不存在，会静默失败导致 UI token=0。
        if hasattr(client, "update_current_generation"):
            client.update_current_generation(
                usage_details=usage_details,
                model=getattr(usage, "model", None) or None,
            )
        elif hasattr(client, "update_current_observation"):
            client.update_current_observation(usage=usage_details)
    except Exception:
        return
