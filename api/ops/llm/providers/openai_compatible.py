"""OpenAI 兼容 Chat Completions 共用逻辑（SiliconFlow / Bailian）。"""

from __future__ import annotations

import time
from typing import Any

import requests

from api.ops.llm.errors import OpsLlmRequestError
from api.ops.llm.types import LlmCompletionResult, LlmUsage

_BAILIAN_QUOTA_MARKER = "AllocationQuota.FreeTierOnly"
_DEFAULT_MAX_ATTEMPTS = 3


def is_bailian_quota_error(response: requests.Response) -> bool:
    """百炼无额度：403 且 body 含 AllocationQuota.FreeTierOnly。"""
    if response.status_code != 403:
        return False
    try:
        data = response.json()
    except ValueError:
        return _BAILIAN_QUOTA_MARKER in response.text
    err = data.get("error")
    if isinstance(err, dict):
        code = str(err.get("code") or err.get("type") or "")
        message = str(err.get("message") or "")
        if _BAILIAN_QUOTA_MARKER in code or _BAILIAN_QUOTA_MARKER in message:
            return True
    return _BAILIAN_QUOTA_MARKER in str(data)


def _is_retryable_status(status_code: int) -> bool:
    return status_code >= 500 or status_code in (408, 429)


def _parse_completion_response(
    data: dict[str, Any],
    *,
    provider: str,
    model: str,
    step: str,
    latency_ms: int,
) -> LlmCompletionResult:
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


def _single_post(
    *,
    base_url: str,
    api_key: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    timeout: int,
) -> requests.Response:
    return requests.post(
        f"{base_url.rstrip('/')}/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": model, "messages": messages, "temperature": temperature},
        timeout=timeout,
    )


def openai_compatible_complete_with_policy(
    *,
    provider: str,
    base_url: str,
    api_key: str,
    model_chain: list[str],
    messages: list[dict[str, str]],
    temperature: float = 0.3,
    step: str = "other",
    timeout: int = 60,
    max_attempts: int = _DEFAULT_MAX_ATTEMPTS,
    quota_model_switch: bool = False,
) -> LlmCompletionResult:
    """按策略调用：同模型最多 max_attempts 次；百炼额度错误可换下一模型。"""
    if not model_chain:
        raise OpsLlmRequestError("模型链为空")

    last_error: Exception | None = None

    for model in model_chain:
        for _ in range(max_attempts):
            started_at = time.time()
            try:
                resp = _single_post(
                    base_url=base_url,
                    api_key=api_key,
                    model=model,
                    messages=messages,
                    temperature=temperature,
                    timeout=timeout,
                )
            except requests.RequestException as exc:
                last_error = OpsLlmRequestError(f"LLM 请求失败: {exc}")
                continue

            latency_ms = int((time.time() - started_at) * 1000)

            if resp.ok:
                data = resp.json()
                return _parse_completion_response(
                    data,
                    provider=provider,
                    model=model,
                    step=step,
                    latency_ms=latency_ms,
                )

            if quota_model_switch and is_bailian_quota_error(resp):
                last_error = OpsLlmRequestError(
                    f"百炼模型 {model} 无额度（AllocationQuota.FreeTierOnly）",
                    status_code=403,
                )
                break

            if _is_retryable_status(resp.status_code):
                last_error = OpsLlmRequestError(
                    f"LLM 上游错误 {resp.status_code}: {resp.text[:200]}",
                    status_code=resp.status_code,
                )
                continue

            last_error = OpsLlmRequestError(
                f"LLM 上游错误 {resp.status_code}: {resp.text[:200]}",
                status_code=resp.status_code,
            )
            raise last_error

    if last_error is not None:
        raise last_error
    raise OpsLlmRequestError("LLM 调用失败")


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
    """单模型 + 重试（SiliconFlow 默认路径）。"""
    return openai_compatible_complete_with_policy(
        provider=provider,
        base_url=base_url,
        api_key=api_key,
        model_chain=[model],
        messages=messages,
        temperature=temperature,
        step=step,
        timeout=timeout,
        quota_model_switch=False,
    )
