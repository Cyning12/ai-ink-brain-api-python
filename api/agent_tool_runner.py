from __future__ import annotations

from typing import Any

from .chatbi_agent_models import V1Mode
from .chatbi_failure import has_aggregation_signals as _has_aggregation_signals
from .text2sql_core import is_text2sql_intent
from .tools import Tool, ToolName, tool_mode_map


def select_tool(*, tools_map: dict[str, Tool], tool_name: ToolName) -> Tool:
    t = tools_map.get(tool_name)
    if not t:
        raise RuntimeError(f"Unknown tool: {tool_name}")
    return t


def tool_to_mode(tool: ToolName) -> V1Mode:
    m = tool_mode_map()[tool]
    return m  # type: ignore[return-value]


def next_tool_after_success(*, query: str, tool_used: ToolName) -> ToolName | None:
    """多步 ReAct 的 P0 最小"继续条件"。

    仅在明显需要"数值 + 解释/原因"的语义下，允许从 SQL 成功继续调用 RAG。
    """
    q = (query or "").lower()
    if tool_used == "text2sql_query":
        if any(k in q for k in ["原因", "下降", "解释", "为什么", "提升", "增长", "减少", "增加"]):
            return "rag_search"
        return None
    if tool_used == "rag_search":
        if is_text2sql_intent(query):
            return "text2sql_query"
        return None
    return None


def intent_signals_from_query(query: str) -> Any:
    # 复用 intent gating 字段语义：用于 prefer 强制时也能正确 gated_sql fallback
    llm_prefers_sql = is_text2sql_intent(query)
    has_aggregation_signals = _has_aggregation_signals(query)
    # StructuredSignals 是 IntentDecision 内部类型；为了避免循环依赖，这里用 Any 传入其结构
    # unified_chat/agent.py 只按属性访问：llm_prefers_sql / has_aggregation_signals
    return type(
        "StructuredSignalsLite",
        (),
        {"llm_prefers_sql": llm_prefers_sql, "has_aggregation_signals": has_aggregation_signals},
    )()
