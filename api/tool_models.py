from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class ToolResult:
    """Tool 执行结果（Agent 仅依赖 error_code/error_stage 做失败类型判定）。"""

    success: bool
    data: dict[str, Any] | None = None
    error: str | None = None
    error_code: str | None = None
    error_stage: str | None = None
    latency_ms: int = 0


ToolName = Literal["rag_search", "text2sql_query", "direct_answer"]


@dataclass(frozen=True)
class Tool:
    name: ToolName
    description: str
    parameters: dict[str, Any]
    execute: Callable[..., Awaitable[ToolResult]]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def list_tools(self) -> list[Tool]:
        return list(self._tools.values())
