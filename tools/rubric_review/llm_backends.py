# -*- coding: utf-8 -*-
"""OpenAI / Anthropic / SiliconFlow(OpenAI 兼容) 调用封装：限流与指数退避重试。"""

from __future__ import annotations

import json
import logging
import re
import time
from typing import Any

logger = logging.getLogger(__name__)


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    fence = re.search(r"```(?:json)?\s*([\s\S]*?)```", text)
    if fence:
        text = fence.group(1).strip()
    return json.loads(text)


def _should_retry_http(exc: BaseException) -> bool:
    msg = str(exc).lower()
    if "429" in msg or "rate" in msg or "ratelimit" in msg:
        return True
    if "503" in msg or "502" in msg or "500" in msg:
        return True
    if "overloaded" in msg:
        return True
    return False


def _openai_compatible_chat_json(
    *,
    api_key: str,
    base_url: str | None,
    model: str,
    user_prompt: str,
    max_retries: int,
    retry_base_seconds: float,
    prefer_json_object: bool,
) -> dict[str, Any]:
    """OpenAI SDK；base_url 非空时用于 SiliconFlow 等兼容网关。"""
    from openai import OpenAI

    kwargs: dict[str, Any] = {"api_key": api_key}
    if base_url:
        kwargs["base_url"] = base_url.rstrip("/")
    client = OpenAI(**kwargs)

    modes = [True, False] if prefer_json_object else [False]
    last_exc: BaseException | None = None

    for attempt in range(max_retries):
        mode_exc: BaseException | None = None
        for use_json_object in modes:
            try:
                create_kw: dict[str, Any] = {
                    "model": model,
                    "messages": [{"role": "user", "content": user_prompt}],
                    "temperature": 0.2,
                }
                if use_json_object:
                    create_kw["response_format"] = {"type": "json_object"}
                resp = client.chat.completions.create(**create_kw)
                raw = resp.choices[0].message.content or ""
                try:
                    return json.loads(raw)
                except json.JSONDecodeError:
                    return _extract_json_object(raw)
            except json.JSONDecodeError as e:
                mode_exc = e
                logger.warning(
                    "JSON 解析失败 attempt=%s/%s json_object=%s: %s",
                    attempt + 1,
                    max_retries,
                    use_json_object,
                    e,
                )
            except Exception as e:
                mode_exc = e
                err_s = str(e).lower()
                if use_json_object and (
                    "response_format" in err_s or "json_object" in err_s or "400" in err_s
                ):
                    logger.info("json_object 不可用，降级普通输出: %s", e)
                    continue
                logger.warning(
                    "OpenAI 兼容调用失败 attempt=%s/%s json_object=%s: %s",
                    attempt + 1,
                    max_retries,
                    use_json_object,
                    e,
                )
            # 下一 mode（例如关闭 json_object 再试）
        last_exc = mode_exc
        if attempt < max_retries - 1:
            delay = retry_base_seconds * (2**attempt)
            if last_exc and _should_retry_http(last_exc):
                time.sleep(delay)
            else:
                time.sleep(min(delay, retry_base_seconds * 2))
    if last_exc:
        raise last_exc
    raise RuntimeError("OpenAI 兼容调用失败且无异常对象")


def complete_json_openai(
    *,
    api_key: str,
    model: str,
    user_prompt: str,
    max_retries: int,
    retry_base_seconds: float,
) -> dict[str, Any]:
    return _openai_compatible_chat_json(
        api_key=api_key,
        base_url=None,
        model=model,
        user_prompt=user_prompt,
        max_retries=max_retries,
        retry_base_seconds=retry_base_seconds,
        prefer_json_object=True,
    )


def complete_json_siliconflow(
    *,
    api_key: str,
    base_url: str,
    model: str,
    user_prompt: str,
    max_retries: int,
    retry_base_seconds: float,
) -> dict[str, Any]:
    return _openai_compatible_chat_json(
        api_key=api_key,
        base_url=base_url,
        model=model,
        user_prompt=user_prompt,
        max_retries=max_retries,
        retry_base_seconds=retry_base_seconds,
        prefer_json_object=True,
    )


def complete_json_anthropic(
    *,
    api_key: str,
    model: str,
    user_prompt: str,
    max_retries: int,
    retry_base_seconds: float,
) -> dict[str, Any]:
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    last: BaseException | None = None
    for attempt in range(max_retries):
        try:
            msg = client.messages.create(
                model=model,
                max_tokens=4096,
                temperature=0.2,
                messages=[{"role": "user", "content": user_prompt}],
            )
            block = msg.content[0]
            text = getattr(block, "text", "") or ""
            return _extract_json_object(text)
        except json.JSONDecodeError as e:
            last = e
            logger.warning("Anthropic JSON 解析失败 attempt=%s/%s: %s", attempt + 1, max_retries, e)
            if attempt == max_retries - 1:
                raise
            time.sleep(retry_base_seconds * (2**attempt))
        except Exception as e:
            last = e
            logger.warning("Anthropic 调用失败 attempt=%s/%s: %s", attempt + 1, max_retries, e)
            if attempt == max_retries - 1:
                raise
            if _should_retry_http(e):
                time.sleep(retry_base_seconds * (2**attempt))
            else:
                time.sleep(retry_base_seconds)
    assert last
    raise last


def complete_json(
    *,
    backend: str,
    api_key: str,
    model: str,
    user_prompt: str,
    max_retries: int,
    retry_base_seconds: float,
    siliconflow_base_url: str | None = None,
) -> dict[str, Any]:
    if backend == "siliconflow":
        if not siliconflow_base_url:
            raise ValueError("siliconflow 需要 siliconflow_base_url")
        return complete_json_siliconflow(
            api_key=api_key,
            base_url=siliconflow_base_url,
            model=model,
            user_prompt=user_prompt,
            max_retries=max_retries,
            retry_base_seconds=retry_base_seconds,
        )
    if backend == "openai":
        return complete_json_openai(
            api_key=api_key,
            model=model,
            user_prompt=user_prompt,
            max_retries=max_retries,
            retry_base_seconds=retry_base_seconds,
        )
    if backend == "anthropic":
        return complete_json_anthropic(
            api_key=api_key,
            model=model,
            user_prompt=user_prompt,
            max_retries=max_retries,
            retry_base_seconds=retry_base_seconds,
        )
    raise ValueError(f"未知 backend: {backend}")
