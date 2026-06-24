"""LLM Provider 工厂。"""

from __future__ import annotations

import os

from api.ops.llm.providers.bailian import BailianProvider
from api.ops.llm.providers.base import OpsLlmProvider
from api.ops.llm.providers.siliconflow import SiliconFlowProvider

_PROVIDERS: dict[str, type[OpsLlmProvider]] = {
    "siliconflow": SiliconFlowProvider,
    "bailian": BailianProvider,
}


def get_llm_provider() -> OpsLlmProvider:
    """根据 OPS_LLM_PROVIDER 环境变量返回对应 Provider 实例。"""
    name = (os.getenv("OPS_LLM_PROVIDER") or "siliconflow").strip().lower()
    cls = _PROVIDERS.get(name)
    if cls is None:
        raise ValueError(
            f"未知的 OPS_LLM_PROVIDER={name!r}；"
            f"可选: {', '.join(_PROVIDERS.keys())}"
        )
    return cls()
