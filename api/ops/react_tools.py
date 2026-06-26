"""Ops Desk ReAct Tool Protocol — v0 只读工具集。"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from api.ops.queries import OpsQueries


class ToolSchema:
    """单个工具的 JSON Schema 描述。"""

    def __init__(
        self,
        name: str,
        description: str,
        parameters: dict[str, Any],
        read_only: bool = True,
    ) -> None:
        self.name = name
        self.description = description
        self.parameters = parameters
        self.read_only = read_only

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }


ToolHandler = Callable[..., dict[str, Any]]


class OpsToolRegistry:
    """声明式只读工具注册表。"""

    def __init__(self) -> None:
        self._tools: dict[str, tuple[ToolSchema, ToolHandler]] = {}

    def register(
        self,
        name: str,
        schema: ToolSchema,
        handler: ToolHandler,
        read_only: bool = True,
    ) -> None:
        schema.read_only = read_only
        self._tools[name] = (schema, handler)

    def get(self, name: str) -> tuple[ToolSchema, ToolHandler] | None:
        return self._tools.get(name)

    def list_tools(self) -> list[dict[str, Any]]:
        return [s.to_dict() for s, _ in self._tools.values()]

    def list_names(self) -> list[str]:
        return list(self._tools.keys())

    def execute(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        entry = self.get(name)
        if entry is None:
            return {"ok": False, "error": f"tool_not_found: {name}", "data": None}
        schema, handler = entry
        try:
            result = handler(**arguments)
            return {"ok": True, "error": None, "data": result}
        except Exception as exc:
            return {"ok": False, "error": str(exc), "data": None}


def _build_v0_registry(queries: OpsQueries) -> OpsToolRegistry:
    """构建 v0 只读工具注册表。"""
    registry = OpsToolRegistry()

    # ops_list_issues
    registry.register(
        "ops_list_issues",
        ToolSchema(
            name="ops_list_issues",
            description="列出最近 N 天的 issues，支持按状态、标签、模块过滤。",
            parameters={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "最近多少天", "default": 30},
                    "state": {"type": "string", "description": "状态：open/closed", "enum": ["open", "closed"]},
                    "label": {"type": "string", "description": "标签过滤"},
                    "limit": {"type": "integer", "description": "返回条数上限", "default": 20},
                },
            },
        ),
        lambda days=30, state=None, label=None, limit=20: {
            "items": queries.fetch_issues(days=days, state=state, label=label, limit=limit)[0],
            "total": queries.fetch_issues(days=days, state=state, label=label, limit=limit)[1],
        },
    )

    # ops_list_pulls
    registry.register(
        "ops_list_pulls",
        ToolSchema(
            name="ops_list_pulls",
            description="列出最近 N 天的 pull requests。",
            parameters={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "最近多少天", "default": 30},
                    "state": {"type": "string", "description": "状态：open/closed/merged", "enum": ["open", "closed", "merged"]},
                    "limit": {"type": "integer", "description": "返回条数上限", "default": 20},
                },
            },
        ),
        lambda days=30, state=None, limit=20: {
            "items": queries.fetch_pulls(days=days, state=state, limit=limit)[0],
            "total": queries.fetch_pulls(days=days, state=state, limit=limit)[1],
        },
    )

    # ops_get_issue
    registry.register(
        "ops_get_issue",
        ToolSchema(
            name="ops_get_issue",
            description="根据 issue 编号获取单条 issue 详情。",
            parameters={
                "type": "object",
                "properties": {
                    "number": {"type": "integer", "description": "Issue 编号"},
                },
                "required": ["number"],
            },
        ),
        lambda number: {"issue": queries.fetch_issue_by_number(number)},
    )

    # ops_metrics_summary
    registry.register(
        "ops_metrics_summary",
        ToolSchema(
            name="ops_metrics_summary",
            description="获取最近 N 天的指标摘要（cycle time / review time / issue throughput）。",
            parameters={
                "type": "object",
                "properties": {
                    "days": {"type": "integer", "description": "最近多少天", "default": 30},
                },
            },
        ),
        lambda days=30: {
            "metrics": [
                queries.cycle_time_metric(days),
                queries.review_time_metric(days),
                queries.issue_throughput_metric(days),
            ],
        },
    )

    # ops_scan_status
    registry.register(
        "ops_scan_status",
        ToolSchema(
            name="ops_scan_status",
            description="获取最近一次数据同步扫描的状态摘要。",
            parameters={"type": "object", "properties": {}},
        ),
        lambda **kwargs: queries.sync_status(),
    )

    return registry


def _truncate_summary(data: dict[str, Any], max_len: int = 500) -> str:
    """截断工具结果用于 event summary。"""
    text = json.dumps(data, ensure_ascii=False, default=str)
    if len(text) > max_len:
        return text[:max_len] + "..."
    return text
