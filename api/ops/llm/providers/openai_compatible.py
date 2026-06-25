"""OpenAI 兼容 Chat Completions 共用逻辑（SiliconFlow / Bailian）。"""

from __future__ import annotations

import time

import requests

from api.ops.llm.types import LlmCompletionResult, LlmUsage


def openai_compatible_complete(
    *,
    provider: str,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float = 0.3,
    step: str = "other",
    timeout: int = 60,
) -> LlmCompletionResult:
    """POST {base_url}/chat/completions 并解析 usage。"""
    started_at = time.time()
    resp = requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "temperature": temperature},
        timeout=timeout,
    )
    resp.raise_for_status()
    data = resp.json()
    latency_ms = int((time.time() - started_at) * 1000)

    content = str(data["choices"][0]["message"]["content"])
    usage_raw = data.get("usage") or {}

    prompt_tokens_details = usage_raw.get("prompt_tokens_details") or {}
    usage = LlmUsage(
        provider=provider,
        model=model,
        prompt_tokens=int(usage_raw.get("prompt_tokens", 0)),
        completion_tokens=int(usage_raw.get("completion_tokens", 0)),
        total_tokens=int(usage_raw.get("total_tokens", 0)),
        latency_ms=latency_ms,
        step=step,
        usage_missing=not bool(usage_raw),
        prompt_cache_hit_tokens=int(usage_raw.get("prompt_cache_hit_tokens", 0) or 0),
        prompt_cache_miss_tokens=int(usage_raw.get("prompt_cache_miss_tokens", 0) or 0),
        cached_tokens=int(prompt_tokens_details.get("cached_tokens", 0) or 0),
    )
    return LlmCompletionResult(content=content, usage=usage)
