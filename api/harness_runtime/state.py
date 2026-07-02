"""Session LangGraph 状态（SPEC §7.2 最小字段）。"""

from __future__ import annotations

from typing import Any, NotRequired, TypedDict


class SessionGraphState(TypedDict, total=False):
    session_id: str
    run_id: str
    user_message: str
    messages: list[dict[str, str]]
    session_status: str
    task_draft_path: str
    plan_summary: str
    auth_action: str
    answer: str
    gate_snapshot: dict[str, Any]
    error: NotRequired[dict[str, Any]]
