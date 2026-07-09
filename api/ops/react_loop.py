"""Ops Desk ReAct Loop — fallback 路径。"""

from __future__ import annotations

import json
import os
from typing import Any

from api.ops.chat_context import load_chat_transcript
from api.ops.events_schema import handoff_payload, review_payload
from api.ops.llm import chat_completion
from api.ops.llm.types import LlmUsage
from api.ops.orchestrator.core import synthesize
from api.ops.queries import OpsQueries
from api.ops.react_tools import _build_v0_registry, _truncate_summary
from api.ops.review.rules import review_result
from api.ops.store.artifacts import save_artifact_with_failure_event
from api.ops.store.runs import OpsRunStore, append_event
from api.ops.tracing import trace_span, traceable, update_current_span_metadata

MAX_STEPS_DEFAULT = int(os.getenv("OPS_REACT_MAX_STEPS", "6"))
MAX_RETRIES_DEFAULT = 2


@traceable(capture_input=False, capture_output=False)
def run_react_fallback(
    run_id: str,
    query: str,
    store: OpsRunStore,
    queries: OpsQueries,
    max_steps: int = MAX_STEPS_DEFAULT,
    max_retries: int = MAX_RETRIES_DEFAULT,
    session_id: str | None = None,
) -> dict[str, Any]:
    """ReAct fallback 循环：think → tool_call → observe → … → review → synthesize。

    与 FSM 路径共用 ops_runs / ops_run_events / Review 闸。
    超限 → status partial + 仍 synthesize（非 500）。
    """
    transcript = load_chat_transcript(session_id, store=store)

    update_current_span_metadata(
        {
            "ops_run_id": run_id,
            "run_id": run_id,
            "agent_role": "react",
            "route": "react",
            "intent": "fallback",
            "max_steps": max_steps,
            "session_id": session_id,
        }
    )

    registry = _build_v0_registry(queries)
    tools_json = registry.list_tools()

    store.append_event(run_id, "orchestrator", "run.start", node_id="react.start")
    store.append_event(
        run_id,
        "orchestrator",
        "router.decision",
        payload={"route": "react", "intent": "fallback", "max_steps": max_steps},
        node_id="classify",
    )
    with trace_span(
        "handoff",
        run_type="tool",
        run_id=run_id,
        session_id=session_id,
        agent_role="react",
        from_route="classify",
        to_route="react",
        intent="fallback",
    ):
        append_event(
            run_id,
            "handoff",
            handoff_payload(
                from_route="classify",
                to_route="react",
                intent="fallback",
                slots={},
                agent=None,
            ),
            store=store,
        )

    # System prompt for ReAct
    system_prompt = _build_react_system_prompt(tools_json)
    messages: list[dict[str, str]] = [
        {"role": "system", "content": system_prompt},
    ]
    if transcript:
        messages.extend(transcript)
    messages.append({"role": "user", "content": query})

    step = 0
    final_answer = ""
    llm_calls = 0
    llm_usages: list[LlmUsage] = []
    tool_evidence: list[dict[str, Any]] = []
    final_verdict = "partial"

    while step < max_steps:
        step += 1

        # LLM think
        llm_result = chat_completion(
            messages,
            step=f"react.step.{step}",
            run_id=run_id,
            store=store,
            temperature=0.3,
        )
        llm_calls += 1
        llm_usages.append(llm_result.usage)

        raw_content = llm_result.content.strip()
        parsed = _parse_react_output(raw_content)

        # Log react_step
        thought = parsed.get("thought", "")
        store.append_event(
            run_id,
            "react",
            "agent.react_step",
            payload={
                "step": step,
                "thought": thought[:500] if thought else "",
            },
            node_id=f"react.step.{step}",
        )

        # Check for final answer
        if parsed.get("final_answer"):
            final_answer = parsed["final_answer"]
            store.append_event(
                run_id,
                "react",
                "agent.final_answer",
                payload={"step": step, "answer": final_answer[:1000]},
                node_id=f"react.final.{step}",
            )
            break

        # Tool call
        tool_name = parsed.get("tool")
        tool_args = parsed.get("arguments", {})
        if not tool_name:
            # No tool requested, treat as partial
            final_answer = raw_content
            break

        store.append_event(
            run_id,
            "react",
            "agent.tool_call",
            payload={"tool": tool_name, "arguments": tool_args},
            node_id=f"react.tool_call.{step}",
        )

        # Execute tool
        tool_result = registry.execute(tool_name, tool_args)
        summary = _truncate_summary(tool_result)
        store.append_event(
            run_id,
            "react",
            "agent.tool_result",
            payload={
                "tool": tool_name,
                "ok": tool_result["ok"],
                "summary": summary,
            },
            node_id=f"react.tool_result.{step}",
        )

        if tool_result["ok"] and tool_result["data"] is not None:
            tool_evidence.append({
                "tool": tool_name,
                "arguments": tool_args,
                "result": tool_result["data"],
            })

        # Append tool result to conversation
        tool_msg = json.dumps(
            {"tool": tool_name, "result": tool_result},
            ensure_ascii=False,
            default=str,
        )
        messages.append({"role": "assistant", "content": raw_content})
        messages.append({"role": "user", "content": f"Tool result:\n{tool_msg}"})

    else:
        # max_steps exceeded
        final_verdict = "partial"
        store.append_event(
            run_id,
            "orchestrator",
            "react.max_steps",
            payload={"max_steps": max_steps, "steps_taken": step},
            node_id="react.max_steps",
        )
        if not final_answer:
            final_answer = f"已尝试 {step} 步，尚未得出完整结论。基于已收集信息："

    # Review + synthesize (reuse deep path logic)
    # Build a result dict compatible with review_result
    react_result = {
        "reasoning": final_answer,
        "suggestion": "",
        "confidence": 0.7 if tool_evidence else 0.4,
        "citations": [],
        "evidence": tool_evidence,
        "found": bool(tool_evidence),
    }

    # Extract any issue numbers from evidence for citations
    for ev in tool_evidence:
        data = ev.get("result", {})
        if isinstance(data, dict):
            issue = data.get("issue")
            if issue and isinstance(issue, dict):
                num = issue.get("number")
                url = issue.get("html_url")
                if num:
                    react_result["citations"].append({"number": num, "url": url or ""})
            items = data.get("items", [])
            if isinstance(items, list):
                for item in items[:3]:
                    if isinstance(item, dict) and item.get("number"):
                        react_result["citations"].append({
                            "number": item["number"],
                            "url": item.get("html_url", ""),
                        })

    # Review loop
    attempt = 0
    review_feedback: dict[str, Any] | None = None
    while attempt <= max_retries:
        verdict, detail = review_result(react_result, queries)
        with trace_span(
            "review",
            run_type="tool",
            run_id=run_id,
            session_id=session_id,
            agent_role="react",
            verdict=verdict,
            rule=detail.get("rule"),
            attempt=attempt,
        ):
            store.append_event(
                run_id,
                "review",
                f"review.{verdict}",
                payload={"rule": detail.get("rule"), "message": detail.get("message"), "attempt": attempt},
                node_id="review",
            )
            append_event(
                run_id,
                "review",
                review_payload(
                    verdict=verdict,
                    rule=detail.get("rule"),
                    message=detail.get("message"),
                    attempt=attempt,
                ),
                store=store,
            )

        if verdict == "pass":
            final_verdict = "done"
            break
        if verdict == "partial":
            final_verdict = "partial"
            break
        attempt += 1
        if attempt > max_retries:
            final_verdict = "partial"
            break
        review_feedback = detail
        # If review fails, re-synthesize with feedback
        if review_feedback:
            feedback_msg = f"\n\n【Review 反馈】规则：{review_feedback.get('rule', '')}，原因：{review_feedback.get('message', '')}。请修正。"
            final_answer = final_answer + feedback_msg
            react_result["reasoning"] = final_answer
            # Re-synthesize with feedback
            if tool_evidence:
                answer, synth_usage = synthesize(query, react_result, run_id=run_id, store=store)
                if synth_usage is not None:
                    llm_calls += 1
                    llm_usages.append(synth_usage)
                final_answer = answer
                react_result["reasoning"] = final_answer

    # Synthesize final answer (only if not already synthesized in review retry loop)
    if not review_feedback or not tool_evidence:
        if tool_evidence:
            answer, synth_usage = synthesize(query, react_result, run_id=run_id, store=store)
            if synth_usage is not None:
                llm_calls += 1
                llm_usages.append(synth_usage)
        else:
            answer = final_answer
    else:
        answer = final_answer

    store.append_event(
        run_id,
        "orchestrator",
        "final.answer",
        payload={"answer": answer, "confidence": react_result.get("confidence", 0)},
        node_id="synthesize",
    )
    store.update_run(
        run_id,
        status=final_verdict,
        final_answer={"answer": answer, "verdict": final_verdict},
    )
    save_artifact_with_failure_event(
        run_id,
        "react.final_answer",
        {
            "answer": answer,
            "verdict": final_verdict,
            "intent": "fallback",
            "route": "react",
            "steps_taken": step,
        },
        store=store,
    )
    store.append_event(run_id, "orchestrator", "run.end", node_id="react.end")

    # Run metrics
    metrics_json = _build_metrics_json(
        route="react",
        intent="fallback",
        llm_calls=llm_calls,
        llm_usages=llm_usages,
    )
    store.update_run_metrics_json(run_id, metrics_json)
    store.append_event(
        run_id,
        "orchestrator",
        "run.metrics",
        payload=metrics_json,
        node_id="react.metrics",
    )

    return {
        "run_id": run_id,
        "status": final_verdict,
        "answer": answer,
        "route": "react",
    }


def _build_react_system_prompt(tools: list[dict[str, Any]]) -> str:
    tools_str = json.dumps(tools, ensure_ascii=False, indent=2)
    return (
        "你是 Ops Desk 助手，可以通过工具查询仓库数据。"
        "你只能使用以下只读工具，不能执行任何写操作（commit/push/open PR/merge）。\n\n"
        f"可用工具：\n{tools_str}\n\n"
        "每次回复必须输出 JSON，格式如下：\n"
        "1. 如果需要调用工具：{\"thought\": \"思考摘要\", \"tool\": \"工具名\", \"arguments\": {参数}}\n"
        "2. 如果已得出最终答案：{\"thought\": \"思考摘要\", \"final_answer\": \"最终答案\"}\n\n"
        "要求：\n"
        "- 只引用 ops_issues / ops_pull_requests 中存在的 #NNN\n"
        "- 若证据不足，明确说明\n"
        "- 不要给出 commit/push/open PR 等写操作指令"
    )


def _parse_react_output(text: str) -> dict[str, Any]:
    """解析 LLM 输出的 ReAct JSON。"""
    import re

    # Try to extract JSON from code blocks
    if "```json" in text:
        match = re.search(r"```json\s*(.*?)\s*```", text, re.S)
        if match:
            text = match.group(1)
    elif "```" in text:
        match = re.search(r"```\s*(.*?)\s*```", text, re.S)
        if match:
            text = match.group(1)

    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in text
        match = re.search(r"\{.*\}", text, re.S)
        if match:
            try:
                parsed = json.loads(match.group(0))
            except json.JSONDecodeError:
                return {"thought": text[:200], "final_answer": text}
        else:
            return {"thought": text[:200], "final_answer": text}

    return {
        "thought": str(parsed.get("thought", "")),
        "tool": parsed.get("tool"),
        "arguments": parsed.get("arguments", {}),
        "final_answer": parsed.get("final_answer"),
    }


def _build_metrics_json(
    route: str,
    intent: str,
    llm_calls: int,
    llm_usages: list[LlmUsage],
    cache_hit: bool = False,
    demo_id: str | None = None,
) -> dict[str, Any]:
    """汇总 run 级 metrics_json。"""
    from api.ops.orchestrator.core import _build_metrics_json as _orig_build

    return _orig_build(
        route=route,
        intent=intent,
        llm_calls=llm_calls,
        llm_usages=llm_usages,
        cache_hit=cache_hit,
        demo_id=demo_id,
    )
