from __future__ import annotations

import os
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any, Literal

from .agent_memory import AgentMemoryStore
from .chatbi_json_log import chatbi_json_log_enabled, log_chatbi_record
from .intent_agent import IntentDecision, decide_intent_v2
from .intent_router import decide_intent as decide_intent_v1
from .tools import Tool, ToolName, ToolResult, tool_mode_map
from .text2sql_core import is_text2sql_intent
from .text2sql_grounding import grounding_prefix_for_intent
from .chatbi_agent_models import (
    AGENT_THINK_TEXT_CLIP,
    AgentFinalView,
    AgentRunView,
    AgentStepView,
    LlmPhase,
    V1Mode,
    make_tool_call_input as _make_tool_call_input,
)
from .chatbi_events import agent_chain as _agent_chain
from .chatbi_events import emit_simulated_llm as _emit_simulated_llm
from .chatbi_failure import FailureTypeHandler, has_aggregation_signals as _has_aggregation_signals


# 契约静态扫描锚点：实现已迁至 chatbi_events，锚点字面量须保留于本文件供 contract check
_CONTRACT_ANCHOR_AGENT_CLARIFY = _agent_chain(
    typ="agent.clarify",
    started_at=0.0,
    step_id="__contract_anchor_clarify__",
    payload={"step_number": 1, "message": "", "prompt_for_user": ""},
)
_CONTRACT_ANCHOR_AGENT_PLAN_PREVIEW = _agent_chain(
    typ="agent.plan.preview",
    started_at=0.0,
    step_id="__contract_anchor_plan_preview__",
    payload={
        "plan_id": "",
        "tool": "text2sql_query",
        "sql_draft": "",
        "rewrite_query": "",
        "planned_top_k": 10,
        "preview_headlines": [],
        "warnings": [],
        "plan_execution_token": "",
        "expires_in_sec": 120,
    },
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
        plan_execution_token: str | None = None,
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

        # P2 延伸 / 方案 B：即将走 P1-4 澄清短路时，G2 的 router.decision.final_mode 须与意图候选一致，
        # 不得沿用「已切到 fallback 工具」的 step1_mode（常见 rag），否则 Timeline 像已转 RAG 却无任何工具执行。
        clarify_gate = os.getenv("CHATBI_V3_LOW_CONFIDENCE_CLARIFY", "").strip().lower() in (
            "1",
            "true",
            "yes",
            "on",
        )
        from .chatbi_plan_token import (
            mint_clarify_plan_bypass_token,
            plan_preview_confirm_enabled,
            plan_token_ttl_s,
            verify_clarify_plan_bypass_token,
        )

        _plan_bypass_tool: ToolName | None = None
        if plan_preview_confirm_enabled():
            if verify_clarify_plan_bypass_token(
                plan_execution_token,
                session_id=session_id,
                query=query,
                expected_tool="text2sql_query",
            ):
                _plan_bypass_tool = "text2sql_query"
            elif verify_clarify_plan_bypass_token(
                plan_execution_token,
                session_id=session_id,
                query=query,
                expected_tool="rag_search",
            ):
                _plan_bypass_tool = "rag_search"

        _clarify_tool: ToolName | None = None
        if (
            clarify_gate
            and prefer == "auto"
            and intent is not None
            and intent.confidence < self._min_confidence
            and _plan_bypass_tool is None
        ):
            if intent.tool == "text2sql_query":
                _clarify_tool = "text2sql_query"
            elif intent.tool == "rag_search":
                _clarify_tool = "rag_search"
        _clarify_eligible = _clarify_tool is not None

        # 用户已持有效 plan_execution_token：本轮回放首步须回到确认时的工具，而非低置信 fallback。
        if _plan_bypass_tool:
            step1_tool = _plan_bypass_tool
            step1_mode = self._tool_to_mode(step1_tool)
            if _plan_bypass_tool == "rag_search":
                step1_reasoning = "已校验 plan_execution_token，按用户确认放行执行 RAG 检索。"
            else:
                step1_reasoning = "已校验 plan_execution_token，按用户确认放行执行 Text2SQL。"

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
            _final_mode = intent.mode if _clarify_eligible else step1_mode
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
            # 成功：走总结模拟流；终态短路（无权限 / SQL 无数据等）：工具失败但已有对用户可见的 answer_text 时仍 emit，避免仅见 error 而无 agent.llm / 增量正文
            _ans_for_stream = (answer_text_for_llm or "").strip()
            if _ans_for_stream and (tr.success or next_action_val == "final_answer"):
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

        # P1-4 §4.3：低置信 + text2sql/rag 候选时可选「澄清短路」（默认关，避免改变现网行为）
        if _clarify_eligible and _clarify_tool is not None:
            _cl_msg = "待您澄清（低置信度）"
            plan_preview_payload: dict[str, Any] | None = None
            plan_ttl_s = plan_token_ttl_s()
            _clarify_mode = self._tool_to_mode(_clarify_tool)
            if _clarify_tool == "rag_search":
                ttl_notice = (
                    f"若确认按预览检索方案继续：请在 {plan_ttl_s} 秒内在**下一轮同一问题**的请求 JSON 中带 "
                    f"`\"plan_execution_token\": \"…\"`（见 `agent.plan.preview` 中的 `plan_execution_token`）。"
                    "若未及时附带令牌，本预览方案与该令牌均失效，须**重新发起本问题**才能再次预览。"
                )
                _preview_fail_hint = (
                    "（本轮未能生成可放行的 RAG 方案预览，无法签发 plan_execution_token；请改问或补充检索范围。）"
                )
            else:
                ttl_notice = (
                    f"若确认按预览 SQL 继续查数：请在 {plan_ttl_s} 秒内在**下一轮同一问题**的请求 JSON 中带 "
                    f"`\"plan_execution_token\": \"…\"`（见 `agent.plan.preview` 中的 `plan_execution_token`）。"
                    "若未及时附带令牌，本预览 SQL 与该令牌均失效，须**重新发起本问题**才能再次预览。"
                )
                _preview_fail_hint = (
                    "（本轮未能生成可放行的 SQL 预览，无法签发 plan_execution_token；请改问或使用 prefer=text2sql。）"
                )
            use_reasoning = (os.getenv("CHATBI_V3_CLARIFY_PROMPT_USE_REASONING", "") or "").strip().lower() in (
                "1",
                "true",
                "yes",
                "on",
            )
            _generic = (
                "请补充您关心的指标、时间范围或具体业务对象。"
                " 若涉及具体表/字段，请在确认权限与口径后再发起查数。"
            )
            if use_reasoning:
                _raw_prompt = (intent.reasoning or intent.reasoning_full or "").strip()
                _cl_prompt = (_raw_prompt[:900] + "…") if len(_raw_prompt) > 900 else _raw_prompt
                if not _cl_prompt:
                    _cl_prompt = _generic
            else:
                _cl_prompt = _generic
            if plan_preview_confirm_enabled():
                _cl_prompt = (_cl_prompt.rstrip() + "\n\n" + ttl_notice).strip()
                _prev_hist: list[dict[str, Any]] = turn_history[-6:]
                plan_prev_id = str(uuid.uuid4()).replace("-", "")[:20]
                if _clarify_tool == "text2sql_query":
                    from .tools import text2sql_execute as _t2s_preview  # noqa: PLC0415

                    _t2s_json_ctx: dict[str, Any] | None = None
                    if run_id:
                        _t2s_json_ctx = {"request_id": run_id, "run_id": run_id, "session_id": session_id}
                    _pr = await _t2s_preview(
                        query,
                        history=_prev_hist,
                        debug_llm_prompts=debug_llm_prompts,
                        chain_emit=emit,
                        chain_started_at=ts_ref,
                        json_log_ctx=_t2s_json_ctx,
                        preview_only=True,
                    )
                    sql_pv = ""
                    if _pr.success and isinstance(_pr.data, dict) and isinstance(_pr.data.get("sql"), str):
                        sql_pv = (_pr.data.get("sql") or "").strip()
                    if sql_pv:
                        exec_tok = mint_clarify_plan_bypass_token(
                            session_id=session_id, query=query, tool="text2sql_query"
                        )
                        plan_preview_payload = {
                            "plan_id": plan_prev_id,
                            "tool": "text2sql_query",
                            "sql_draft": sql_pv,
                            "warnings": [ttl_notice],
                            "plan_execution_token": exec_tok,
                            "expires_in_sec": plan_ttl_s,
                        }
                else:
                    from .tools import rag_search_execute as _rag_preview  # noqa: PLC0415

                    _pr_rag = await _rag_preview(
                        query,
                        history=_prev_hist,
                        debug_llm_prompts=debug_llm_prompts,
                        preview_only=True,
                    )
                    rewrite_pv = ""
                    planned_k = 10
                    headlines: list[str] = []
                    if _pr_rag.success and isinstance(_pr_rag.data, dict):
                        rw = _pr_rag.data.get("rewritten")
                        if isinstance(rw, str):
                            rewrite_pv = rw.strip()
                        try:
                            planned_k = int(_pr_rag.data.get("planned_top_k") or 10)
                        except Exception:  # noqa: BLE001
                            planned_k = 10
                        ph = _pr_rag.data.get("preview_headlines")
                        if isinstance(ph, list):
                            headlines = [str(x) for x in ph if x][:6]
                    if rewrite_pv:
                        exec_tok = mint_clarify_plan_bypass_token(
                            session_id=session_id, query=query, tool="rag_search"
                        )
                        plan_preview_payload = {
                            "plan_id": plan_prev_id,
                            "tool": "rag_search",
                            "rewrite_query": rewrite_pv,
                            "planned_top_k": planned_k,
                            "preview_headlines": headlines,
                            "warnings": [ttl_notice],
                            "plan_execution_token": exec_tok,
                            "expires_in_sec": plan_ttl_s,
                        }
                if plan_preview_payload:
                    if emit is not None:
                        await emit(
                            _agent_chain(
                                typ="agent.plan.preview",
                                started_at=ts_ref,
                                step_id="a1_plan_prev",
                                payload=plan_preview_payload,
                            )
                        )
                    if chatbi_json_log_enabled() and run_id:
                        log_chatbi_record(
                            message="agent_plan_preview_minted",
                            request_id=run_id,
                            run_id=run_id,
                            session_id=session_id,
                            route="agent",
                            mode=_clarify_mode,
                            plan_id=plan_prev_id,
                            gate_bypass_reason="plan_preview_token_minted",
                        )
                else:
                    _cl_prompt = (_cl_prompt.rstrip() + "\n\n" + _preview_fail_hint).strip()

            clarify_pl: dict[str, Any] = {"step_number": 1, "message": _cl_msg, "prompt_for_user": _cl_prompt}
            if chatbi_json_log_enabled() and run_id:
                log_chatbi_record(
                    message="agent_clarify_short_circuit",
                    request_id=run_id,
                    run_id=run_id,
                    session_id=session_id,
                    route="agent",
                    mode=_clarify_mode,
                    intent_tool=_clarify_tool,
                    intent_confidence=float(intent.confidence),
                    clarify_gate=True,
                )
            _final_answer = (
                "系统在继续查数前需要先与您对齐语义。请查看 Timeline 中「待您澄清」条目并补充说明；"
                "也可改用 prefer=text2sql / prefer=rag 强制路径或改写问题后重试。"
            )
            final_cl = AgentFinalView(
                answer=_final_answer,
                mode=_clarify_mode,
                total_steps=0,
                tools_used=[],
                modes=[_clarify_mode],
                fallback_used=False,
            )
            if emit is not None:
                await emit(
                    _agent_chain(
                        typ="agent.clarify",
                        started_at=ts_ref,
                        step_id="a1_clarify",
                        payload=clarify_pl,
                    )
                )
                await _emit_final_chains(final_cl, final_cl.answer)
                return AgentRunView(intent_decision=intent, steps=[], final=final_cl)
            return AgentRunView(
                intent_decision=intent,
                steps=[],
                final=final_cl,
                clarify_short_circuit=True,
                clarify_user_payload=clarify_pl,
                clarify_plan_preview_payload=plan_preview_payload,
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
                trf = current_tool_result
                ec_f = (trf.error_code or "").strip()
                if ec_f == "SQL_EXEC_NO_DATA":
                    ans3 = "未查到数据。"
                elif ec_f in FailureTypeHandler.TEXT2SQL_DENY_FINAL_ANSWER_CODES:
                    ans3 = (trf.error or "").strip() or "当前账号无权执行该数据库操作。"
                else:
                    ans3 = (trf.error or "").strip() or "未查到数据。"
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

