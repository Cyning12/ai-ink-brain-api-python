"""Ops Desk LLM 错误类型。"""

from __future__ import annotations


class OpsLlmMisconfiguredError(RuntimeError):
    """LLM Provider 环境未配置（如缺 API Key）。"""


class OpsLlmRequestError(RuntimeError):
    """LLM 上游调用失败（重试 / fallback 耗尽）。"""

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
