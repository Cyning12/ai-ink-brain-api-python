from __future__ import annotations

from .chatbi_agent_models import V1Mode
from .intent_agent import IntentDecision
from .intent_router import decide_intent as decide_intent_v1
from .tools import ToolName, ToolResult, tool_mode_map


def tool_failure_digest(tr: ToolResult, *, max_detail: int = 260) -> str:
    code = (tr.error_code or "UNKNOWN").strip() or "UNKNOWN"
    stage = (tr.error_stage or "").strip()
    err = (tr.error or "").strip().replace("\r", " ").replace("\n", " ")
    if len(err) > max_detail:
        err = err[: max_detail - 1] + "…"
    parts: list[str] = [f"code={code}"]
    if stage:
        parts.append(f"stage={stage}")
    if err:
        parts.append(f"msg={err}")
    return " ".join(parts)


def failure_context_suffix(tr: ToolResult) -> str:
    return f"（{tool_failure_digest(tr)}）"


def has_aggregation_signals(query: str) -> bool:
    q = (query or "").lower()
    needles = (
        "多少",
        "金额",
        "收入",
        "支出",
        "人数",
        "数量",
        "总数",
        "平均",
        "最大",
        "最小",
        "top",
        "排行",
        "排名",
        "趋势",
        "对比",
        "分组",
        "group by",
        "count",
        "sum",
        "avg",
    )
    return any(n in q for n in needles)


class FailureTypeHandler:
    """按失败类型决定下一步工具与是否继续 ReAct 循环。"""

    TEXT2SQL_DENY_FINAL_ANSWER_CODES: frozenset[str] = frozenset(
        {
            "SQL_EXEC_PERMISSION_DENIED",
            "CHATBI_SQL_DENIED",
            "CHATBI_SQL_WRITE_DENIED",
        }
    )

    @staticmethod
    def _allow_sql_fallback(*, intent: IntentDecision) -> bool:
        if intent.tool == "text2sql_query" or intent.fallback == "text2sql_query":
            return True
        if bool(intent.structured_signals.llm_prefers_sql):
            return True
        if bool(intent.structured_signals.has_aggregation_signals):
            return True
        return False

    @staticmethod
    def decide_next(
        *,
        query: str,
        tool_result: ToolResult,
        intent: IntentDecision | None,
        fallback_from_intent: ToolName,
        structured_signals: dict[str, bool],
    ) -> tuple[ToolName, V1Mode, str, bool]:
        _ = structured_signals
        code = tool_result.error_code or "UNKNOWN"
        next_tool: ToolName = fallback_from_intent
        next_mode: V1Mode = tool_mode_map()[next_tool]  # type: ignore[assignment]
        next_thought = "尝试使用备用方案继续回答。"
        stop_now = False
        sfx = failure_context_suffix(tool_result)

        if code in ("SQL_GEN_EMPTY", "SQL_GEN_SYNTAX"):
            next_tool = "rag_search"
            next_mode = "rag"
            next_thought = f"SQL 生成仍失败，改用文档检索兜底。{sfx}"
        elif code in ("SQL_EXEC_TABLE_NOT_FOUND",):
            next_tool = "rag_search"
            next_mode = "rag"
            next_thought = f"查库失败可能是表不存在或名称不匹配，改用文档检索定位信息。{sfx}"
        elif code in FailureTypeHandler.TEXT2SQL_DENY_FINAL_ANSWER_CODES:
            next_tool = "direct_answer"
            next_mode = "no_data"
            next_thought = f"数据库访问受权限或策略限制，直接输出说明并结束本回合。{sfx}"
            stop_now = True
        elif code in ("SQL_EXEC_NO_DATA",):
            next_tool = "text2sql_query"
            next_mode = "text2sql"
            next_thought = f"数据库未返回结果，直接给出未查到数据的结论。{sfx}"
            stop_now = True
        elif code == "RAG_RETRIEVE_EMPTY":
            if intent is not None and FailureTypeHandler._allow_sql_fallback(intent=intent):
                next_tool = "text2sql_query"
                next_mode = "text2sql"
                next_thought = f"文档检索无命中，但问题具有结构化统计意图，因此改查数据库。{sfx}"
            else:
                next_tool = "direct_answer"
                next_mode = "no_data"
                next_thought = f"文档检索无命中，改用直接回答或请用户澄清。{sfx}"
        elif code == "RAG_EMBEDDING_MODEL_MISMATCH":
            next_tool = "direct_answer"
            next_mode = "no_data"
            next_thought = f"向量库 Embedding 模型与运行时未对齐，请先全量 re-sync；本回合不基于检索作答。{sfx}"
            stop_now = True
        elif code == "RAG_GENERATE_UNCERTAIN":
            next_tool = "direct_answer"
            next_mode = "no_data"
            next_thought = f"检索答案不够确定，改用直接回答或进一步追问。{sfx}"
        elif code == "LLM_API_TIMEOUT":
            v1 = decide_intent_v1(query=query, prefer="auto")
            if v1.final_mode == "rag":
                next_tool = "rag_search"
            elif v1.final_mode == "text2sql":
                next_tool = "text2sql_query"
            else:
                next_tool = "direct_answer"
            next_mode = v1.final_mode  # type: ignore[assignment]
            next_thought = f"意图/模型调用超时，降级到 V1 规则路由。{sfx}"
        else:
            next_tool = fallback_from_intent
            next_mode = tool_mode_map()[next_tool]  # type: ignore[assignment]
            next_thought = f"处理工具失败，继续使用备用方案。{sfx}"

        return next_tool, next_mode, next_thought, stop_now
