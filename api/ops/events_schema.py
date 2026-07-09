"""Ops Chat 标准化 run events schema v1。

定义 deep / ReAct 路径共用的 handoff、review 等事件 payload 结构，
所有标准事件 payload 必须携带 schema_version 字段。
"""

from __future__ import annotations

from typing import Any, TypedDict

SCHEMA_VERSION = "v1"


class HandoffPayload(TypedDict):
    """handoff 事件 payload：路由决策/子 Agent 委派。"""

    schema_version: str
    from_route: str
    to_route: str
    intent: str
    slots: dict[str, Any]
    agent: str | None


class ReviewPayload(TypedDict):
    """review 事件 payload：V1–V4 审核结果。"""

    schema_version: str
    verdict: str
    rule: str | None
    message: str | None
    attempt: int


def handoff_payload(
    *,
    from_route: str,
    to_route: str,
    intent: str,
    slots: dict[str, Any],
    agent: str | None = None,
) -> HandoffPayload:
    """构造标准化 handoff 事件 payload。"""
    return {
        "schema_version": SCHEMA_VERSION,
        "from_route": from_route,
        "to_route": to_route,
        "intent": intent,
        "slots": dict(slots),
        "agent": agent,
    }


def review_payload(
    *,
    verdict: str,
    rule: str | None,
    message: str | None,
    attempt: int,
) -> ReviewPayload:
    """构造标准化 review 事件 payload。"""
    return {
        "schema_version": SCHEMA_VERSION,
        "verdict": verdict,
        "rule": rule,
        "message": message,
        "attempt": attempt,
    }
