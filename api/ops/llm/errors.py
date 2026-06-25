"""Ops Desk LLM 错误类型。"""

from __future__ import annotations


class OpsLlmMisconfiguredError(RuntimeError):
    """LLM Provider 环境未配置（如缺 API Key）。"""
