"""Ops Desk Chat 模型目录（冻结 · P2-5f）。"""

from __future__ import annotations

import os
from typing import Any, TypedDict


class OpsChatModelEntry(TypedDict):
    id: str
    label: str
    test_only: bool


# SiliconFlow：共用额度 · 不做自动换模 · 仅 UI 列表
SILICONFLOW_CHAT_MODELS: list[OpsChatModelEntry] = [
    {"id": "deepseek-ai/DeepSeek-V4-Pro", "label": "DeepSeek V4 Pro", "test_only": False},
    {"id": "moonshotai/Kimi-K2.7-Code", "label": "Kimi K2.7 Code", "test_only": False},
    {"id": "deepseek-ai/DeepSeek-V4-Flash", "label": "DeepSeek V4 Flash", "test_only": False},
    {"id": "zai-org/GLM-5.2", "label": "GLM 5.2", "test_only": False},
    {"id": "Pro/MiniMaxAI/MiniMax-M2.5", "label": "MiniMax M2.5", "test_only": False},
]

# Bailian：自动换模链（顺序即 fallback 优先级）
BAILIAN_CHAT_MODELS: list[OpsChatModelEntry] = [
    {"id": "kimi/kimi-k2.7-code", "label": "Kimi K2.7 Code（测试无额度）", "test_only": True},
    {"id": "ZHIPU/GLM-5.2", "label": "GLM 5.2（测试无额度）", "test_only": True},
    {"id": "deepseek-v4-pro", "label": "DeepSeek V4 Pro", "test_only": False},
    {"id": "deepseek-v4-flash", "label": "DeepSeek V4 Flash", "test_only": False},
    {"id": "qwen3.7-plus", "label": "Qwen 3.7 Plus", "test_only": False},
]

SILICONFLOW_DEFAULT_MODEL = "deepseek-ai/DeepSeek-V4-Pro"
BAILIAN_DEFAULT_MODEL = "deepseek-v4-pro"


def bailian_test_only_model_ids() -> set[str]:
    return {m["id"] for m in BAILIAN_CHAT_MODELS if m["test_only"]}


def siliconflow_model_ids() -> list[str]:
    return [m["id"] for m in SILICONFLOW_CHAT_MODELS]


def bailian_model_ids() -> list[str]:
    return [m["id"] for m in BAILIAN_CHAT_MODELS]


def resolve_bailian_model_chain(primary: str | None) -> list[str]:
    """从 primary 起向下 fallback；未知 id 则 primary 优先再完整链。

    若 primary 为 test_only（如 kimi 无额度测试项），配额 fallback 时跳过链中
    其余 test_only（如 ZHIPU），直达 deepseek-v4-pro 等生产模型。
    """
    chain_ids = bailian_model_ids()
    test_only = bailian_test_only_model_ids()
    if not primary or not primary.strip():
        return list(chain_ids)
    primary = primary.strip()
    if primary not in chain_ids:
        return [primary, *[mid for mid in chain_ids if mid not in test_only or mid == primary]]
    idx = chain_ids.index(primary)
    tail = chain_ids[idx:]
    if tail and tail[0] in test_only:
        prod_tail = [mid for mid in tail[1:] if mid not in test_only]
        return [tail[0], *prod_tail]
    return tail


def get_chat_models_payload() -> dict[str, Any]:
    name = (os.getenv("OPS_LLM_PROVIDER") or "siliconflow").strip().lower()
    if name == "siliconflow":
        models = SILICONFLOW_CHAT_MODELS
        default = (os.getenv("OPS_LLM_MODEL") or SILICONFLOW_DEFAULT_MODEL).strip()
    elif name == "bailian":
        models = BAILIAN_CHAT_MODELS
        default = (os.getenv("BAILIAN_MODEL") or BAILIAN_DEFAULT_MODEL).strip()
    else:
        models = []
        default = ""
    return {
        "provider": name,
        "models": models,
        "default_model": default,
        "auto_fallback": name == "bailian",
    }
