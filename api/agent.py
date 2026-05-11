from __future__ import annotations

import os
import time
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any, Literal

from .agent_memory import AgentMemoryStore
from .chatbi_json_log import chatbi_json_log_enabled, log_chatbi_record
from .intent_agent import IntentDecision, decide_intent_v2
from .intent_router import decide_intent as decide_intent_v1
from .tools import Tool, ToolName, ToolResult, tool_mode_map
from .text2sql_core import is_text2sql_intent
from .text2sql_grounding import grounding_prefix_for_intent


V1Mode = Literal["rag", "text2sql", "no_data"]

LlmPhase = Literal["intent", "rag_generate", "text2sql_sql", "text2sql_summary", "direct"]

# agent.think / AgentStepView.thought 截断上限（含失败原因摘要，略放宽便于 Timeline 排查）
AGENT_THINK_TEXT_CLIP = 420


def _tool_failure_digest(tr: ToolResult, *, max_detail: int = 260) -> str:
    """从 ToolResult 抽取单行可读的失败摘要（供 think 与 FailureTypeHandler 拼接）。"""
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


def _failure_context_suffix(tr: ToolResult) -> str:
    """拼在 next_thought 末尾，便于确认「为何失败、当前 error_code 是什么」。"""
    return f"（{_tool_failure_digest(tr)}）"


def _agent_chain(typ: str, started_at: float, step_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """与 unified_chat._event 同形，供 SSE chain 帧序列化。"""
    return {"type": typ, "ts": int((time.perf_counter() - started_at) * 1000), "step_id": step_id, "payload": payload}


async def _emit_simulated_llm(
    emit: Callable[[dict[str, Any]], Awaitable[None]],
    *,
    started_at: float,
    step_id: str,
    inner_step_id: str,
    phase: LlmPhase,
    text: str,
    simulated_stream: bool,
    chunk_size: int = 16,
    max_parts: int = 400,
) -> None:
    """伪流式：将整段文本切分为 agent.llm.delta 序列（上游非 stream 时）。"""
    await emit(
        _agent_chain(
            typ="agent.llm.start",
            started_at=started_at,
            step_id=step_id,
            payload={"phase": phase, "step_id": inner_step_id},
        )
    )
    body = text or ""
    part = 0
    for i in range(0, len(body), max(1, chunk_size)):
        if part >= max_parts:
            await emit(
                _agent_chain(
                    typ="agent.llm.truncated",
                    started_at=started_at,
                    step_id=step_id,
                    payload={"dropped_chars": max(0, len(body) - i), "reason": "emit_chunk_cap"},
                )
            )
            break
        chunk = body[i : i + chunk_size]
        await emit(
            _agent_chain(
                typ="agent.llm.delta",
                started_at=started_at,
                step_id=step_id,
                payload={"text": chunk, "part_index": part},
            )
        )
        part += 1
    await emit(
        _agent_chain(
            typ="agent.llm.end",
            started_at=started_at,
            step_id=step_id,
            payload={"ok": True, "phase": phase, "step_id": inner_step_id, "simulated_stream": simulated_stream},
        )
    )


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
    """按失败类型决定下一步工具与是否继续 ReAct 循环。

    L5 / 单测 mock：**勿**在本类内硬改 error 分支、**勿**对 IntentDecision 原地赋值（frozen dataclass）。
    请在 pytest 中：monkeypatch get_tool_registry 注入 dummy 工具；在 dummy execute 的 ToolResult.error_code
    上模拟失败码（如 RAG_RETRIEVE_EMPTY）；monkeypatch decide_intent_v2 返回完整 IntentDecision 覆盖 gating。
    参考：tests/test_unified_chat_backend_v2_agent.py::test_v2_rag_empty_gated_fallback；
    SPEC-ChatBI-V2-Agent-Overview.md §7.5.4。
    """

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
        sfx = _failure_context_suffix(tool_result)

        # SQL：生成/执行失败映射
        if code in ("SQL_GEN_EMPTY", "SQL_GEN_SYNTAX"):
            # 已在本 step 内重试过；仍失败则切换到 RAG 兜底
            next_tool = "rag_search"
            next_mode = "rag"
            next_thought = f"SQL 生成仍失败，改用文档检索兜底。{sfx}"
        elif code in ("SQL_EXEC_TABLE_NOT_FOUND", "SQL_EXEC_PERMISSION_DENIED"):
            next_tool = "rag_search"
            next_mode = "rag"
            next_thought = f"查库失败可能是表/权限问题，改用文档检索定位信息。{sfx}"
        elif code in ("SQL_EXEC_NO_DATA",):
            # 不换工具：直接回答“未查到数据”
            next_tool = "text2sql_query"
            next_mode = "text2sql"
            next_thought = f"数据库未返回结果，直接给出未查到数据的结论。{sfx}"
            stop_now = True
        # RAG：检索无命中必须 gated
        elif code == "RAG_RETRIEVE_EMPTY":
            if intent is not None and FailureTypeHandler._allow_sql_fallback(intent=intent):
                next_tool = "text2sql_query"
                next_mode = "text2sql"
                next_thought = f"文档检索无命中，但问题具有结构化统计意图，因此改查数据库。{sfx}"
            else:
                next_tool = "direct_answer"
                next_mode = "no_data"
                next_thought = f"文档检索无命中，改用直接回答或请用户澄清。{sfx}"
        elif code == "RAG_GENERATE_UNCERTAIN":
            next_tool = "direct_answer"
            next_mode = "no_data"
            next_thought = f"检索答案不够确定，改用直接回答或进一步追问。{sfx}"
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
            next_thought = f"意图/模型调用超时，降级到 V1 规则路由。{sfx}"
        else:
            next_tool = fallback_from_intent
            next_mode = tool_mode_map()[next_tool]  # type: ignore[assignment]
            next_thought = f"处理工具失败，继续使用备用方案。{sfx}"

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

    async def run(
        self,
        *,
        query: str,
        session_id: str | None,
        prefer: str,
        sse_started_at: float | None = None,
        run_id: str | None = None,
        emit: Callable[[dict[str, Any]], Awaitable[None]] | None = None,
        debug_router: bool = False,
        debug_llm_prompts: bool = False,
        intent_obs_payload_fn: Callable[[IntentDecision], dict[str, Any]] | None = None,
    ) -> AgentRunView:
        loop_started = time.perf_counter()
        ts_ref = sse_started_at if sse_started_at is not None else loop_started
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
                pre = grounding_prefix_for_intent(h if isinstance(h, dict) else {})
                body = f"{pre}\n{r.strip()}" if pre else r.strip()
                intent_history.append({"role": "assistant", "content": body})

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
                capture_llm_prompts=debug_llm_prompts,
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

        rid_short = (run_id or "run").replace("-", "")[:12] or "run"

        # vNext 增量 SSE：在首步工具执行前下发 intent / router（G2 emit）
        if emit is not None:
            if intent is None or intent_obs_payload_fn is None:
                raise RuntimeError("emit 路径需要 intent 与 intent_obs_payload_fn")
            await emit(
                _agent_chain(
                    typ="agent.step.start",
                    started_at=ts_ref,
                    step_id="a1",
                    payload={"step_number": 1, "max_steps": max_steps},
                )
            )
            _intent_llm_text = (intent.reasoning_full or intent.reasoning or "").strip()
            if not _intent_llm_text:
                _intent_llm_text = "（意图简述不可用）"
            await _emit_simulated_llm(
                emit,
                started_at=ts_ref,
                step_id=f"{rid_short}_s1_intent",
                inner_step_id="s1",
                phase="intent",
                text=_intent_llm_text,
                simulated_stream=True,
            )
            await emit(
                _agent_chain(
                    typ="agent.intent",
                    started_at=ts_ref,
                    step_id="intent_1",
                    payload=intent_obs_payload_fn(intent),
                )
            )
            _cand_mode = intent.mode
            _final_mode = step1_mode
            await emit(
                _agent_chain(
                    typ="router.decision",
                    started_at=ts_ref,
                    step_id="r1",
                    payload={
                        "prefer": "auto" if prefer == "auto" else prefer,
                        "candidate_mode": _cand_mode,
                        "final_mode": _final_mode,
                        "rule_hits": [],
                        "evidence": {"agent_reasoning": intent.reasoning_full or intent.reasoning},
                        "fallback": intent.fallback,
                    },
                )
            )
            if debug_llm_prompts and intent and isinstance(intent.raw_response, dict):
                _ilp = intent.raw_response.get("llm_prompts")
                if isinstance(_ilp, list) and _ilp:
                    await emit(
                        _agent_chain(
                            typ="agent.debug.llm_prompts",
                            started_at=ts_ref,
                            step_id=f"{rid_short}_intent_llm",
                            payload={"scope": "intent", "items": _ilp},
                        )
                    )

        async def _emit_post_tool_chains(
            *,
            step_number: int,
            tool_used: ToolName,
            mode_for_step: V1Mode,
            tr: ToolResult,
            answer_text_for_llm: str,
            next_action_val: Literal["continue", "final_answer"],
            success_val: bool,
        ) -> None:
            if emit is None:
                return
            from .unified_chat import _build_rag_sources_event  # noqa: PLC0415

            if tool_used == "text2sql_query" and tr.success and tr.data:
                data = tr.data
                columns_any = data.get("columns")
                columns = columns_any if isinstance(columns_any, list) else []
                rows_any = data.get("rows")
                rows_any2 = rows_any if isinstance(rows_any, list) else []
                rows2: list[dict[str, Any]] = [r for r in rows_any2 if isinstance(r, dict)]
                truncated = len(rows2) > 20
                await emit(
                    _agent_chain(
                        typ="sql.result",
                        started_at=ts_ref,
                        step_id=f"q_step{step_number}",
                        payload={
                            "sql": data.get("sql") if isinstance(data.get("sql"), str) else "",
                            "columns": [c for c in columns if isinstance(c, str)],
                            "rows": rows2[:20],
                            "truncated": truncated,
                        },
                    )
                )
            elif tool_used == "rag_search" and tr.success and tr.data:
                hits_any = tr.data.get("hits")
                hits2: list[dict[str, Any]] = hits_any if isinstance(hits_any, list) else []
                await emit(
                    _agent_chain(
                        typ="rag.sources",
                        started_at=ts_ref,
                        step_id=f"s_step{step_number}",
                        payload=_build_rag_sources_event(hits2, top_k=10),
                    )
                )
            if tr.success and (answer_text_for_llm or "").strip():
                llm_phase: LlmPhase = (
                    "rag_generate"
                    if tool_used == "rag_search"
                    else ("text2sql_summary" if tool_used == "text2sql_query" else "direct")
                )
                await _emit_simulated_llm(
                    emit,
                    started_at=ts_ref,
                    step_id=f"{rid_short}_s{step_number}_{llm_phase}",
                    inner_step_id=f"s{step_number}",
                    phase=llm_phase,
                    text=answer_text_for_llm,
                    simulated_stream=True,
                )
            await emit(
                _agent_chain(
                    typ="agent.step.end",
                    started_at=ts_ref,
                    step_id=f"a{step_number}_end",
                    payload={
                        "step_number": step_number,
                        "tool_used": tool_used,
                        "mode": mode_for_step,
                        "success": success_val,
                        "next_action": next_action_val,
                    },
                )
            )

        async def _emit_final_chains(fin: AgentFinalView, answer: str) -> None:
            if emit is None:
                return
            await emit(
                _agent_chain(
                    typ="agent.final",
                    started_at=ts_ref,
                    step_id="a_final",
                    payload={
                        "total_steps": fin.total_steps,
                        "tools_used": fin.tools_used,
                        "modes": fin.modes,
                        "fallback_used": fin.fallback_used,
                    },
                )
            )
            await emit(
                _agent_chain(
                    typ="assistant.message",
                    started_at=ts_ref,
                    step_id="s_answer",
                    payload={"role": "assistant", "content": answer},
                )
            )

        for step_idx in range(1, max_steps + 1):
            elapsed_ms = int((time.perf_counter() - loop_started) * 1000)
            # 软超时 + V1 覆盖：仅允许在「尚未执行过任何工具」时生效（len(tools_used)==0）。
            # 若在每步开头无差别覆盖，则首轮意图+rag 已超过 AGENT_MAX_LATENCY_MS 后，后续步会反复
            # 把 current_tool 打回 V1 的 rag（日记类 query 常见），从而覆盖 FailureTypeHandler 给出的
            # direct_answer/text2sql，造成 rag_search 死循环直至 max_steps。
            if elapsed_ms > self._max_latency_ms and len(tools_used) == 0:
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
            if emit is not None:
                if step_idx > 1:
                    await emit(
                        _agent_chain(
                            typ="agent.step.start",
                            started_at=ts_ref,
                            step_id=f"a{step_idx}",
                            payload={"step_number": step_idx, "max_steps": max_steps},
                        )
                    )
                await emit(
                    _agent_chain(
                        typ="agent.think",
                        started_at=ts_ref,
                        step_id=f"a{step_idx}_think",
                        payload={
                            "step_number": step_idx,
                            "thought": current_thought[:AGENT_THINK_TEXT_CLIP],
                            "selected_tool": current_tool,
                            "mode": current_mode,
                            "confidence": step1_conf if step_idx == 1 else 1.0,
                        },
                    )
                )
                if current_tool == "rag_search":
                    await emit(
                        _agent_chain(
                            typ="tool.call.start",
                            started_at=ts_ref,
                            step_id=f"t_step{step_idx}_rewrite",
                            payload={"tool": "rag.rewrite", "input": {"query": query}},
                        )
                    )
                else:
                    await emit(
                        _agent_chain(
                            typ="tool.call.start",
                            started_at=ts_ref,
                            step_id=f"t_step{step_idx}",
                            payload={"tool": current_tool, "input": {"query": query}},
                        )
                    )
            # tool.call.end 在 emit 路径下由本处与 execute 结果一并下发
            _t2s_json_ctx: dict[str, Any] | None = None
            if run_id:
                _t2s_json_ctx = {"request_id": run_id, "run_id": run_id, "session_id": session_id}
            if current_tool == "text2sql_query":
                current_tool_result = await tool.execute(  # type: ignore[call-arg]
                    query,
                    history=call_history,
                    debug_llm_prompts=debug_llm_prompts,
                    chain_emit=emit,
                    chain_started_at=ts_ref if emit is not None else None,
                    json_log_ctx=_t2s_json_ctx,
                )
            else:
                current_tool_result = await tool.execute(  # type: ignore[call-arg]
                    query,
                    history=call_history,
                    debug_llm_prompts=debug_llm_prompts,
                )

            tools_used.append(current_tool)

            if current_tool == "text2sql_query" and chatbi_json_log_enabled() and run_id:
                _dlog = current_tool_result.data if isinstance(current_tool_result.data, dict) else {}
                _phlog = _dlog.get("text2sql_phases_ms") if isinstance(_dlog.get("text2sql_phases_ms"), dict) else None
                log_chatbi_record(
                    message="text2sql_tool_call_end",
                    request_id=run_id,
                    run_id=run_id,
                    session_id=session_id,
                    route="agent",
                    mode="text2sql",
                    tool="text2sql_query",
                    latency_ms=current_tool_result.latency_ms,
                    text2sql_phases_ms=_phlog,
                    error_code=current_tool_result.error_code,
                    step_number=step_idx,
                )

            if emit is not None:
                _out_ans0: str | None = None
                _data = current_tool_result.data if isinstance(current_tool_result.data, dict) else {}
                if current_tool_result.data and isinstance(current_tool_result.data.get("answer"), str):
                    _out_ans0 = current_tool_result.data.get("answer")
                if current_tool == "rag_search":
                    _rw = _data.get("rewritten") if isinstance(_data.get("rewritten"), str) else ""
                    _rw_ms = int(_data.get("rewrite_latency_ms") or 0)
                    await emit(
                        _agent_chain(
                            typ="tool.call.end",
                            started_at=ts_ref,
                            step_id=f"t_step{step_idx}_rewrite",
                            payload={
                                "output": {"rewritten_query": _rw or query},
                                "error": None,
                                "latency_ms": _rw_ms,
                            },
                        )
                    )
                    await emit(
                        _agent_chain(
                            typ="tool.call.start",
                            started_at=ts_ref,
                            step_id=f"t_step{step_idx}",
                            payload={"tool": "rag_search", "input": {"query": query, "rewritten_query": _rw or query}},
                        )
                    )
                _out_payload: dict[str, Any] = {}
                if _out_ans0 is not None:
                    _out_payload["answer"] = _out_ans0
                if current_tool == "rag_search" and isinstance(_data.get("rewritten"), str):
                    _out_payload["rewritten_query"] = _data["rewritten"]
                if current_tool == "text2sql_query" and isinstance(_data.get("text2sql_phases_ms"), dict):
                    _out_payload["text2sql_phases_ms"] = _data["text2sql_phases_ms"]
                await emit(
                    _agent_chain(
                        typ="tool.call.end",
                        started_at=ts_ref,
                        step_id=f"t_step{step_idx}",
                        payload={
                            "output": _out_payload,
                            "error": current_tool_result.error,
                            "latency_ms": current_tool_result.latency_ms,
                        },
                    )
                )
                if debug_llm_prompts and isinstance(_data.get("llm_prompts"), list) and _data.get("llm_prompts"):
                    await emit(
                        _agent_chain(
                            typ="agent.debug.llm_prompts",
                            started_at=ts_ref,
                            step_id=f"{rid_short}_s{step_idx}_tool_llm",
                            payload={
                                "scope": "tool",
                                "tool": current_tool,
                                "step_number": step_idx,
                                "items": _data["llm_prompts"],
                            },
                        )
                    )

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
                                "thought": current_thought[:AGENT_THINK_TEXT_CLIP],
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
                    if emit is not None:
                        await _emit_post_tool_chains(
                            step_number=step_idx,
                            tool_used=current_tool,
                            mode_for_step=current_mode,
                            tr=current_tool_result,
                            answer_text_for_llm=ans,
                            next_action_val="continue",
                            success_val=True,
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
                            "thought": current_thought[:AGENT_THINK_TEXT_CLIP],
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
                if emit is not None:
                    await _emit_post_tool_chains(
                        step_number=step_idx,
                        tool_used=current_tool,
                        mode_for_step=current_mode,
                        tr=current_tool_result,
                        answer_text_for_llm=ans,
                        next_action_val="final_answer",
                        success_val=True,
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
                if emit is not None:
                    await _emit_final_chains(final, final.answer)
                return AgentRunView(intent_decision=intent, steps=steps, final=final)

            # 失败：根据失败类型决定下一步
            # SQL retry 逻辑：针对 SQL_GEN_* 允许在同 step 内重试一次
            code = current_tool_result.error_code or "UNKNOWN"
            if code in ("SQL_GEN_EMPTY", "SQL_GEN_SYNTAX"):
                # 重试一次同工具
                if emit is not None:
                    await emit(
                        _agent_chain(
                            typ="tool.call.start",
                            started_at=ts_ref,
                            step_id=f"t_step{step_idx}_retry",
                            payload={"tool": current_tool, "input": {"query": query}},
                        )
                    )
                retry_tool_result = await tool.execute(  # type: ignore[call-arg]
                    query,
                    history=call_history,
                    debug_llm_prompts=debug_llm_prompts,
                )
                if emit is not None:
                    _oa_r: str | None = None
                    if retry_tool_result.data and isinstance(retry_tool_result.data.get("answer"), str):
                        _oa_r = retry_tool_result.data.get("answer")
                    await emit(
                        _agent_chain(
                            typ="tool.call.end",
                            started_at=ts_ref,
                            step_id=f"t_step{step_idx}_retry",
                            payload={
                                "output": {"answer": _oa_r},
                                "error": retry_tool_result.error,
                                "latency_ms": retry_tool_result.latency_ms,
                            },
                        )
                    )
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
                    if emit is not None:
                        await _emit_post_tool_chains(
                            step_number=step_idx,
                            tool_used=current_tool,
                            mode_for_step=current_mode,
                            tr=retry_tool_result,
                            answer_text_for_llm=ans2,
                            next_action_val="final_answer",
                            success_val=True,
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
                    if emit is not None:
                        await _emit_final_chains(final, final.answer)
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
                            "thought": current_thought[:AGENT_THINK_TEXT_CLIP],
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
                if emit is not None:
                    await _emit_post_tool_chains(
                        step_number=step_idx,
                        tool_used=current_tool,
                        mode_for_step=current_mode,
                        tr=current_tool_result,
                        answer_text_for_llm=ans3,
                        next_action_val="final_answer",
                        success_val=False,
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
                if emit is not None:
                    await _emit_final_chains(final, final.answer)
                return AgentRunView(intent_decision=intent, steps=steps, final=final)

            next_action = "continue"
            steps.append(
                AgentStepView(
                    step_number=step_idx,
                    think_payload={
                        "step_number": step_idx,
                        "thought": current_thought[:AGENT_THINK_TEXT_CLIP],
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
            if emit is not None:
                await _emit_post_tool_chains(
                    step_number=step_idx,
                    tool_used=current_tool,
                    mode_for_step=current_mode,
                    tr=current_tool_result,
                    answer_text_for_llm="",
                    next_action_val="continue",
                    success_val=False,
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
        if emit is not None:
            await _emit_final_chains(final, final.answer)
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

