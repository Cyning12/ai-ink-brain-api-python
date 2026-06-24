"""Ops Desk LLM 子模块初始化。

注意：api/ops/llm.py 与 api/ops/llm/ 目录共存时，
from api.ops.llm import xxx 优先解析目录（__init__.py）。
因此将 chat_completion / synthesize_answer 从 llm.py 迁入 __init__.py，
llm.py 仅保留向后兼容的 re-export。
"""

from __future__ import annotations

from typing import Any

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
        },
        node_id=f"llm.{usage.step}",
    )


@traceable(run_type="llm")
def chat_completion(
    messages: list[dict[str, str]],
    *,
    temperature: float = 0.3,
    step: str = "other",
    run_id: str | None = None,
    store: Any = None,
) -> LlmCompletionResult:
    """同步单轮 LLM 调用；返回 content + usage。

    测试时 monkeypatch 此函数或 get_llm_provider() 返回值。
    """
    provider = get_llm_provider()
    result = provider.complete(messages, temperature=temperature, step=step)
    # 确保 usage 携带 step
    result.usage.step = step
    if tracing_enabled():
        update_current_generation_usage(result.usage)
    if run_id and store:
        _write_usage_event(run_id, result.usage, store)
    return result


def synthesize_answer(query: str, evidence: list[dict[str, Any]]) -> LlmCompletionResult:
    prompt = (
        "你是一位 Ops Desk 助手。基于以下证据回答用户问题。\n"
        "要求：\n"
        "1. 只引用 ops_issues / ops_pull_requests 中存在的 #NNN。\n"
        "2. 不要给出 commit/push/open PR 等写操作指令。\n"
        "3. 若证据不足，明确说明。\n\n"
        f"用户问题：{query}\n\n证据：\n{evidence}\n\n回答："
    )
    return chat_completion([{"role": "user", "content": prompt}], step="synthesize")


__all__ = ["LlmCompletionResult", "LlmUsage", "chat_completion", "synthesize_answer"]
