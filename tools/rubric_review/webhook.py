# -*- coding: utf-8 -*-
"""人工仲裁回调：通用 JSON POST（飞书/钉钉机器人等自行解析 msg_type）。"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

import requests

logger = logging.getLogger(__name__)


def post_webhook(
    url: str,
    payload: dict[str, Any],
    *,
    max_retries: int = 4,
    retry_base_seconds: float = 1.0,
    timeout: int = 15,
) -> requests.Response | None:
    """向 webhook POST JSON；失败时指数退避重试。"""
    last_exc: BaseException | None = None
    for attempt in range(max_retries):
        try:
            r = requests.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=timeout,
            )
            if r.status_code >= 500 or r.status_code == 429:
                raise RuntimeError(f"webhook HTTP {r.status_code}: {r.text[:500]}")
            return r
        except Exception as e:
            last_exc = e
            logger.warning("webhook POST 失败 attempt=%s/%s: %s", attempt + 1, max_retries, e)
            if attempt < max_retries - 1:
                time.sleep(retry_base_seconds * (2**attempt))
    if last_exc:
        logger.error("webhook 最终失败: %s", last_exc)
    return None


def build_feishu_text_payload(text: str) -> dict[str, Any]:
    """飞书群机器人 text 消息体（若机器人只接受该格式可在外层替换 payload）。"""
    return {"msg_type": "text", "content": {"text": text[:18000]}}


def build_dingtalk_text_payload(text: str) -> dict[str, Any]:
    """钉钉 text 机器人（keyword 安全策略需用户在 text 中含关键词）。"""
    return {"msgtype": "text", "text": {"content": text[:18000]}}


def build_generic_arbitration_payload(
    *,
    event: str,
    summary_text: str,
    detail: dict[str, Any],
) -> dict[str, Any]:
    """默认发送通用 JSON；接收端可用 n8n/自建服务转发到飞书/钉钉。"""
    return {
        "event": event,
        "summary": summary_text[:8000],
        "detail": detail,
    }
