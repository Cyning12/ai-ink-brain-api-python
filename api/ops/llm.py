"""Ops Desk LLM 薄封装（可 mock）。"""

from __future__ import annotations

import os
from typing import Any

import requests


def _api_key() -> str:
    return (os.getenv("SILICONFLOW_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()


def _model() -> str:
    return (os.getenv("OPS_LLM_MODEL") or "Qwen/Qwen2.5-72B-Instruct").strip()


def _base() -> str:
    return (os.getenv("OPS_LLM_BASE") or "https://api.siliconflow.cn/v1").strip()


def chat_completion(messages: list[dict[str, str]], temperature: float = 0.3) -> str:
    """同步单轮 LLM 调用；测试时 monkeypatch 此函数。"""
    key = _api_key()
    if not key:
        raise RuntimeError("缺少 LLM API Key（SILICONFLOW_API_KEY / OPENAI_API_KEY）")
    resp = requests.post(
        f"{_base()}/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json={"model": _model(), "messages": messages, "temperature": temperature},
        timeout=60,
    )
    resp.raise_for_status()
    data = resp.json()
    return str(data["choices"][0]["message"]["content"])


def synthesize_answer(query: str, evidence: list[dict[str, Any]]) -> str:
    prompt = (
        "你是一位 Ops Desk 助手。基于以下证据回答用户问题。\n"
        "要求：\n"
        "1. 只引用 ops_issues / ops_pull_requests 中存在的 #NNN。\n"
        "2. 不要给出 commit/push/open PR 等写操作指令。\n"
        "3. 若证据不足，明确说明。\n\n"
        f"用户问题：{query}\n\n证据：\n{evidence}\n\n回答："
    )
    return chat_completion([{"role": "user", "content": prompt}])
