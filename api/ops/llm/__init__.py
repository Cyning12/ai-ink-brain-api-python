"""Ops Desk LLM 子模块初始化。

注意：api/ops/llm.py 与 api/ops/llm/ 目录共存时，
from api.ops.llm import xxx 优先解析目录（__init__.py）。
因此将 chat_completion / synthesize_answer 从 llm.py 迁入 __init__.py，
llm.py 仅保留向后兼容的 re-export。
"""

from __future__ import annotations

from typing import Any

from fastapi import HTTPException

from api.ops.llm.context import ops_chat_model_override, ops_chat_resolved_model
from api.ops.llm.errors import OpsLlmMisconfiguredError, OpsLlmRequestError
from api.ops.llm.factory import get_llm_provider
from api.ops.llm.types import LlmCompletionResult, LlmUsage
from api.ops.tracing import traceable, tracing_enabled, update_current_generation_usage


def _write_usage_event(run_id: str, usage: LlmUsage, store: Any) -> None:
    """写 llm.usage event 到 ops_run_events；store 为 OpsRunStore 实例。"""
    if store is None:
        return
    store.append_event(
        run_id,
        "llm",
        "llm.usage",
        payload={
            "provider": usage.provider,
            "model": usage.model,
            "prompt_tokens": usage.prompt_tokens,
            "completion_tokens": usage.completion_tokens,
            "total_tokens": usage.total_tokens,
            "latency_ms": usage.latency_ms,
            "step": usage.step,
            "usage_missing": usage.usage_missing,
            "prompt_cache_hit_tokens": usage.prompt_cache_hit_tokens,
            "prompt_cache_miss_tokens": usage.prompt_cache_miss_tokens,
            "cached_tokens": usage.cached_tokens,
        },
        node_id=f"llm.{usage.step}",
    )


def _write_model_fallback_event(
    run_id: str,
    store: Any,
    *,
    from_model: str,
    to_model: str,
    step: str,
) -> None:
    store.append_event(
        run_id,
        "llm",
        "llm.model.fallback",
        payload={
            "from_model": from_model,
            "to_model": to_model,
            "reason": "AllocationQuota.FreeTierOnly",
            "step": step,
        },
        node_id=f"llm.fallback.{step}",
    )


@traceable(run_type="llm", capture_input=False)
def chat_completion(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.3,
    step: str = "other",
    run_id: str | None = None,
    store: Any = None,
    model: str | None = None,
) -> LlmCompletionResult:
    """同步单轮 LLM 调用；返回 content + usage。

    测试时 monkeypatch 此函数或 get_llm_provider() 返回值。
    """
    provider = get_llm_provider()
    sticky = ops_chat_resolved_model.get()
    resolved_model = sticky or model or ops_chat_model_override.get()

    def on_quota_switch(from_model: str, to_model: str) -> None:
        if run_id and store:
            _write_model_fallback_event(
                run_id,
                store,
                from_model=from_model,
                to_model=to_model,
                step=step,
            )

    try:
        result = provider.complete(
            messages,
            temperature=temperature,
            step=step,
            model=resolved_model,
            on_quota_model_switch=on_quota_switch if not sticky else None,
        )
    except OpsLlmMisconfiguredError as exc:
        raise HTTPException(
            status_code=503,
            detail={"code": "LLM_PROVIDER_MISCONFIGURED", "message": str(exc)},
        ) from exc
    except OpsLlmRequestError as exc:
        raise HTTPException(
            status_code=502,
            detail={"code": "LLM_REQUEST_FAILED", "message": str(exc)},
        ) from exc
    # 确保 usage 携带 step
    result.usage.step = step
    ops_chat_resolved_model.set(result.usage.model)
    if tracing_enabled():
        update_current_generation_usage(result.usage)
    if run_id and store:
        _write_usage_event(run_id, result.usage, store)
    return result


def synthesize_answer(
    query: str,
    evidence: list[dict[str, Any]],
    *,
    run_id: str | None = None,
    store: Any = None,
    transcript: list[dict[str, str]] | None = None,
) -> LlmCompletionResult:
    prompt = (
        "你是一位 Ops Desk 助手。基于以下证据回答用户问题。\n"
        "要求：\n"
        "1. 只引用 ops_issues / ops_pull_requests 中存在的 #NNN。\n"
        "2. 不要给出 commit/push/open PR 等写操作指令。\n"
        "3. 若证据不足，明确说明。\n\n"
        f"用户问题：{query}\n\n证据：\n{evidence}\n\n回答："
    )
    messages: list[dict[str, str]] = []
    if transcript:
        messages.extend(transcript)
    messages.append({"role": "user", "content": prompt})
    return chat_completion(
        messages,
        step="synthesize",
        run_id=run_id,
        store=store,
    )


__all__ = ["LlmCompletionResult", "LlmUsage", "chat_completion", "synthesize_answer"]
