from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .intent_agent import IntentDecision
from .tools import ToolName, ToolResult

V1Mode = Literal["rag", "text2sql", "no_data"]

LlmPhase = Literal["intent", "rag_generate", "text2sql_sql", "text2sql_summary", "direct"]

# agent.think / AgentStepView.thought 截断上限（含失败原因摘要，略放宽便于 Timeline 排查）
AGENT_THINK_TEXT_CLIP = 420


@dataclass(frozen=True)
class AgentStepView:
    step_number: int
    think_payload: dict[str, Any]
    tool_used: ToolName
    mode: V1Mode
    success: bool
    next_action: Literal["continue", "final_answer"]
    tool_result: ToolResult


@dataclass(frozen=True)
class AgentFinalView:
    answer: str
    mode: V1Mode
    total_steps: int
    tools_used: list[ToolName]
    modes: list[V1Mode]
    fallback_used: bool


@dataclass(frozen=True)
class AgentRunView:
    intent_decision: IntentDecision | None
    steps: list[AgentStepView]
    final: AgentFinalView
    clarify_short_circuit: bool = False
    clarify_user_payload: dict[str, Any] | None = None
    clarify_plan_preview_payload: dict[str, Any] | None = None


def make_tool_call_input(query: str) -> dict[str, Any]:
    return {"query": query}
