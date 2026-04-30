from __future__ import annotations

import os
import time
from dataclasses import dataclass
from typing import Any, Literal

from .agent_memory import AgentMemoryStore
from .intent_agent import IntentDecision, decide_intent_v2
from .intent_router import decide_intent as decide_intent_v1
from .tools import Tool, ToolName, ToolResult, tool_mode_map
from .text2sql_core import is_text2sql_intent


V1Mode = Literal["rag", "text2sql", "no_data"]


def _env_int(name: str, default: int) -> int:
    raw = (os.getenv(name, "") or "").strip()
    if not raw:
        return default
    try:
        v = int(raw)
    except Exception:  # noqa: BLE001
        return default
    return v


def _env_float(name: str, default: float) -> float:
    raw = (os.getenv(name, "") or "").strip()
    if not raw:
        return default
    try:
        return float(raw)
    except Exception:  # noqa: BLE001
        return default


def _has_aggregation_signals(query: str) -> bool:
    # gating C：聚合语义特征（非关键词匹配强依赖，但这里用轻量启发式）
    # TODO(P1): 替换为轻量 LLM 语义判定，当前为启发式关键词匹配
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


@dataclass(frozen=True)
class AgentStepView:
    step_number: int
    # agent.think payload（用户级摘要）
    think_payload: dict[str, Any]
    # 本 step 实际执行的工具（包含 fallback/switch）
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
    # 用于统一生成 router.decision + agent.intent（仅 Step 1）
    intent_decision: IntentDecision | None
    steps: list[AgentStepView]
    final: AgentFinalView


def _make_tool_call_input(query: str) -> dict[str, Any]:
    # tool.call.start contract：只需 input 字段存在即可
    return {"query": query}


class FailureTypeHandler:
    """按失败类型决定下一步工具与是否继续 ReAct 循环。"""

    @staticmethod
    def _allow_sql_fallback(*, intent: IntentDecision) -> bool:
        # gating：满足任一即可
        # 条件 A：Intent 原始决策含 SQL 特征
        if intent.tool == "text2sql_query" or intent.fallback == "text2sql_query":
            return True
        # 条件 B：结构化二次判定倾向 SQL
        if bool(intent.structured_signals.llm_prefers_sql):
            return True
        # 条件 C：聚合语义信号
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
        """
        返回：
        - next_tool
        - next_mode
        - next_thought（用户级，1-2 句）
        - stop_now：True 表示无需再走下一步工具，直接给 final_answer（如 SQL 无数据）
        """
        code = tool_result.error_code or "UNKNOWN"

        # 默认：继续用 intent 的 fallback tool
        next_tool: ToolName = fallback_from_intent
        next_mode: V1Mode = tool_mode_map()[next_tool]  # type: ignore[assignment]
        next_thought = "尝试使用备用方案继续回答。"
        stop_now = False

        # SQL：生成/执行失败映射
        if code in ("SQL_GEN_EMPTY", "SQL_GEN_SYNTAX"):
            # 已在本 step 内重试过；仍失败则切换到 RAG 兜底
            next_tool = "rag_search"
            next_mode = "rag"
            next_thought = "SQL 生成仍失败，改用文档检索兜底。"
        elif code in ("SQL_EXEC_TABLE_NOT_FOUND", "SQL_EXEC_PERMISSION_DENIED"):
            next_tool = "rag_search"
            next_mode = "rag"
            next_thought = "查库失败可能是表/权限问题，改用文档检索定位信息。"
        elif code in ("SQL_EXEC_NO_DATA",):
            # 不换工具：直接回答“未查到数据”
            next_tool = "text2sql_query"
            next_mode = "text2sql"
            next_thought = "数据库未返回结果，直接给出未查到数据的结论。"
            stop_now = True
        # RAG：检索无命中必须 gated
        elif code == "RAG_RETRIEVE_EMPTY":
            if intent is not None and FailureTypeHandler._allow_sql_fallback(intent=intent):
                next_tool = "text2sql_query"
                next_mode = "text2sql"
                next_thought = "文档检索无命中，但问题具有结构化统计意图，因此改查数据库。"
            else:
                next_tool = "direct_answer"
                next_mode = "no_data"
                next_thought = "文档检索无命中，改用直接回答或请用户澄清。"
        elif code == "RAG_GENERATE_UNCERTAIN":
            next_tool = "direct_answer"
            next_mode = "no_data"
            next_thought = "检索答案不够确定，改用直接回答或进一步追问。"
        # LLM：超时降级到 V1 rule router（由 agent.py 执行最终工具）
        elif code == "LLM_API_TIMEOUT":
            v1 = decide_intent_v1(query=query, prefer="auto")
            if v1.final_mode == "rag":
                next_tool = "rag_search"
            elif v1.final_mode == "text2sql":
                next_tool = "text2sql_query"
            else:
                next_tool = "direct_answer"
            next_mode = v1.final_mode  # type: ignore[assignment]
            next_thought = "意图/模型调用超时，降级到 V1 规则路由。"
        else:
            next_tool = fallback_from_intent
            next_mode = tool_mode_map()[next_tool]  # type: ignore[assignment]
            next_thought = "处理工具失败，继续使用备用方案。"

        return next_tool, next_mode, next_thought, stop_now


class ChatBIAgent:
    """ChatBI V2 Agent 核心：ReAct 多步循环 + 失败类型 fallback + gated 决策。"""

    def __init__(
        self,
        *,
        tools: list[Tool],
        memory: AgentMemoryStore,
    ) -> None:
        self._tools = {t.name: t for t in tools}
        self._memory = memory
        self._max_steps = max(1, int(os.getenv("AGENT_MAX_STEPS", "5")))
        self._max_latency_ms = max(1000, int(os.getenv("AGENT_MAX_LATENCY_MS", "15000")))
        self._min_confidence = float(os.getenv("INTENT_MIN_CONFIDENCE", "0.6"))

    def _select_tool(self, tool_name: ToolName) -> Tool:
        t = self._tools.get(tool_name)
        if not t:
            # 类型上不应发生：因为工具来自 registry
            raise RuntimeError(f"Unknown tool: {tool_name}")
        return t

    def _tool_to_mode(self, tool: ToolName) -> V1Mode:
        m = tool_mode_map()[tool]
        return m  # type: ignore[return-value]

    async def run(self, *, query: str, session_id: str | None, prefer: str) -> AgentRunView:
        started_at = time.perf_counter()
        # tools 侧历史格式：[{query, response}, ...]
        history = await self._memory.load(session_id)
        turn_history: list[dict[str, Any]] = list(history)
        # intent 侧历史格式：[{role, content}, ...]
        intent_history: list[dict[str, Any]] = []
        for h in history:
            q = h.get("query") if isinstance(h, dict) else None
            r = h.get("response") if isinstance(h, dict) else None
            if isinstance(q, str) and q.strip():
                intent_history.append({"role": "user", "content": q.strip()})
            if isinstance(r, str) and r.strip():
                intent_history.append({"role": "assistant", "content": r.strip()})

        tools_used: list[ToolName] = []
        steps: list[AgentStepView] = []

        # Step 1：Intent Agent 决策（仅此一步 emit agent.intent）
        intent: IntentDecision | None = None
        step1_tool: ToolName
        step1_mode: V1Mode
        step1_conf: float
        step1_reasoning: str
        step1_fallback: ToolName | None

        if prefer in ("rag", "text2sql", "no_data"):
            # prefer 强制：绕过 intent（仍需 structured_signals 供 gating）
            step1_mode = prefer if prefer in ("rag", "text2sql") else "no_data"
            if prefer == "rag":
                step1_tool = "rag_search"
            elif prefer == "text2sql":
                step1_tool = "text2sql_query"
            else:
                step1_tool = "direct_answer"
            step1_conf = 1.0
            step1_reasoning = f"用户指定 prefer={prefer}，选择对应工具开始处理。"
            step1_fallback = None
            # 构建 IntentDecision 的最小替代
            intent = IntentDecision(
                tool=step1_tool,
                mode=step1_mode,  # type: ignore[arg-type]
                reasoning=step1_reasoning,
                reasoning_full=step1_reasoning,
                confidence=step1_conf,
                fallback=step1_fallback,
                structured_signals=intent_signals_from_query(query),
                raw_response={"used": "prefer_override"},
            )
        else:
            intent = await decide_intent_v2(
                query=query,
                history=intent_history,
                tools=list(self._tools.values()),
                min_confidence=self._min_confidence,
                timeout=3.0,
            )
            # intent.fallback：低置信度时预置 fallback 工具
            if intent.confidence < self._min_confidence and intent.fallback:
                step1_tool = intent.fallback
            else:
                step1_tool = intent.tool
            step1_mode = self._tool_to_mode(step1_tool)
            step1_conf = intent.confidence
            step1_reasoning = intent.reasoning
            step1_fallback = intent.fallback

        # Step 循环：必须多步（允许成功在 2 步内结束，但失败应触发继续）
        current_tool: ToolName = step1_tool
        current_mode: V1Mode = self._tool_to_mode(current_tool)
        current_tool_result: ToolResult
        current_thought = step1_reasoning[:200]

        max_steps = self._max_steps
        intent_tool_original = intent.tool if intent else step1_tool

        for step_idx in range(1, max_steps + 1):
            elapsed_ms = int((time.perf_counter() - started_at) * 1000)
            if elapsed_ms > self._max_latency_ms:
                # 超时：降级到 V1 rule router 并最终执行一次工具
                v1 = decide_intent_v1(query=query, prefer="auto")
                final_mode = v1.final_mode
                if final_mode == "rag":
                    current_tool = "rag_search"
                elif final_mode == "text2sql":
                    current_tool = "text2sql_query"
                else:
                    current_tool = "direct_answer"
                current_mode = self._tool_to_mode(current_tool)
                current_thought = "Agent 超时，降级到 V1 规则路由。"

            tool = self._select_tool(current_tool)
            call_history: list[dict[str, Any]] = turn_history[-6:]
            # tool.call.start/end 由 unified_chat 产生，这里只负责执行与返回结果
            current_tool_result = await tool.execute(query, history=call_history)  # type: ignore[arg-type]

            tools_used.append(current_tool)

            success = bool(current_tool_result.success)
            next_action: Literal["continue", "final_answer"] = "continue"

            if success:
                # 成功：直接用 tool_result.data.answer 作为最终答案
                ans = ""
                if current_tool_result.data and isinstance(current_tool_result.data.get("answer"), str):
                    ans = current_tool_result.data["answer"]
                else:
                    ans = "对话生成失败。"
                # 把“当前工具结果”作为对话历史注入，供后续工具 rewrite 使用
                turn_history.append({"query": query, "response": ans})

                # 成功后仍可继续：若问题语义需要“数值 + 原因/解释”双证据，则进入下一工具
                next_tool = _next_tool_after_success(query=query, tool_used=current_tool)
                if next_tool and step_idx < max_steps:
                    next_action2: Literal["continue", "final_answer"] = "continue"
                    next_mode2 = self._tool_to_mode(next_tool)
                    next_thought2 = "已获取结构化数据，继续调用文档检索解释原因并整合回答。"
                    steps.append(
                        AgentStepView(
                            step_number=step_idx,
                            think_payload={
                                "step_number": step_idx,
                                "thought": current_thought[:120],
                                "selected_tool": current_tool,
                                "mode": current_mode,
                                "confidence": step1_conf if step_idx == 1 else 1.0,
                            },
                            tool_used=current_tool,
                            mode=current_mode,
                            success=True,
                            next_action=next_action2,
                            tool_result=current_tool_result,
                        )
                    )
                    current_tool = next_tool
                    current_mode = next_mode2
                    current_thought = next_thought2
                    continue

                next_action_final: Literal["continue", "final_answer"] = "final_answer"
                steps.append(
                    AgentStepView(
                        step_number=step_idx,
                        think_payload={
                            "step_number": step_idx,
                            "thought": current_thought[:120],
                            "selected_tool": current_tool,
                            "mode": current_mode,
                            "confidence": step1_conf if step_idx == 1 else 1.0,
                        },
                        tool_used=current_tool,
                        mode=current_mode,
                        success=True,
                        next_action=next_action_final,
                        tool_result=current_tool_result,
                    )
                )
                fallback_used = any(t != intent_tool_original for t in tools_used)
                final = AgentFinalView(
                    answer=ans,
                    mode=current_mode,
                    total_steps=step_idx,
                    tools_used=tools_used,
                    modes=[s.mode for s in steps],
                    fallback_used=fallback_used,
                )
                return AgentRunView(intent_decision=intent, steps=steps, final=final)

            # 失败：根据失败类型决定下一步
            # SQL retry 逻辑：针对 SQL_GEN_* 允许在同 step 内重试一次
            code = current_tool_result.error_code or "UNKNOWN"
            if code in ("SQL_GEN_EMPTY", "SQL_GEN_SYNTAX"):
                # 重试一次同工具
                retry_tool_result = await tool.execute(query, history=call_history)  # type: ignore[arg-type]
                if retry_tool_result.success:
                    # 重试成功：直接 final
                    ans2 = ""
                    if retry_tool_result.data and isinstance(retry_tool_result.data.get("answer"), str):
                        ans2 = retry_tool_result.data["answer"]
                    else:
                        ans2 = "对话生成失败。"
                    steps.append(
                        AgentStepView(
                            step_number=step_idx,
                            think_payload={
                                "step_number": step_idx,
                                "thought": "SQL 生成失败后重试成功，继续回答。",
                                "selected_tool": current_tool,
                                "mode": current_mode,
                                "confidence": step1_conf if step_idx == 1 else 1.0,
                            },
                            tool_used=current_tool,
                            mode=current_mode,
                            success=True,
                            next_action="final_answer",
                            tool_result=retry_tool_result,
                        )
                    )
                    fallback_used = any(t != intent_tool_original for t in tools_used)
                    final = AgentFinalView(
                        answer=ans2,
                        mode=current_mode,
                        total_steps=step_idx,
                        tools_used=tools_used,
                        modes=[s.mode for s in steps],
                        fallback_used=fallback_used,
                    )
                    return AgentRunView(intent_decision=intent, steps=steps, final=final)
                current_tool_result = retry_tool_result

            # 默认 next_tool：沿用 intent fallback 或当前工具回环
            fallback_from_intent = "rag_search"
            if intent and intent.fallback:
                fallback_from_intent = intent.fallback

            structured_flags = {
                "llm_prefers_sql": bool(intent.structured_signals.llm_prefers_sql) if intent else is_text2sql_intent(query),
                "has_aggregation_signals": _has_aggregation_signals(query),
            }

            next_tool, next_mode, next_thought, stop_now = FailureTypeHandler.decide_next(
                query=query,
                tool_result=current_tool_result,
                intent=intent,
                fallback_from_intent=fallback_from_intent,
                structured_signals=structured_flags,
            )

            if stop_now:
                # SQL 无数据：直接回答，不换工具
                ans3 = "未查到数据。"
                steps.append(
                    AgentStepView(
                        step_number=step_idx,
                        think_payload={
                            "step_number": step_idx,
                            "thought": current_thought[:120],
                            "selected_tool": current_tool,
                            "mode": current_mode,
                            "confidence": step1_conf if step_idx == 1 else 1.0,
                        },
                        tool_used=current_tool,
                        mode=current_mode,
                        success=False,
                        next_action="final_answer",
                        tool_result=current_tool_result,
                    )
                )
                fallback_used = any(t != intent_tool_original for t in tools_used)
                final = AgentFinalView(
                    answer=ans3,
                    mode=current_mode,
                    total_steps=step_idx,
                    tools_used=tools_used,
                    modes=[s.mode for s in steps],
                    fallback_used=fallback_used,
                )
                return AgentRunView(intent_decision=intent, steps=steps, final=final)

            next_action = "continue"
            steps.append(
                AgentStepView(
                    step_number=step_idx,
                    think_payload={
                        "step_number": step_idx,
                        "thought": current_thought[:180],
                        "selected_tool": current_tool,
                        "mode": current_mode,
                        "confidence": step1_conf if step_idx == 1 else 1.0,
                    },
                    tool_used=current_tool,
                    mode=current_mode,
                    success=False,
                    next_action=next_action,
                    tool_result=current_tool_result,
                )
            )

            # 进入下一步
            current_tool = next_tool
            current_mode = next_mode
            current_thought = next_thought

        # max_steps 到达仍未成功：兜底回答
        ans4 = "问题太复杂，建议拆分后重试。"
        fallback_used = any(t != intent_tool_original for t in tools_used)
        final = AgentFinalView(
            answer=ans4,
            mode=current_mode,
            total_steps=len(steps),
            tools_used=tools_used,
            modes=[s.mode for s in steps] or [current_mode],
            fallback_used=fallback_used,
        )
        return AgentRunView(intent_decision=intent, steps=steps, final=final)


def _next_tool_after_success(*, query: str, tool_used: ToolName) -> ToolName | None:
    """多步 ReAct 的 P0 最小“继续条件”。

    仅在明显需要“数值 + 解释/原因”的语义下，允许从 SQL 成功继续调用 RAG。
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


__all__ = ["ChatBIAgent", "AgentRunView", "AgentFinalView", "AgentStepView"]

