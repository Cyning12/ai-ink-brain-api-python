"""Ops Desk Orchestrator FSM（P1-a 手写版 · LangGraph-ready）。"""

from __future__ import annotations

import logging
import re
from typing import Any

logger = logging.getLogger(__name__)

from api.ops import intent_router as _intent_router
from api.ops.agents.graph_analyst import analyze_graph
from api.ops.agents.issue_analyst import analyze_issue
from api.ops.agents.scan_analyst import analyze_scan
from api.ops.chat_context import load_chat_transcript
from api.ops.constants import DEFAULT_DAYS
from api.ops.events_schema import handoff_payload, review_payload
from api.ops.llm import synthesize_answer
from api.ops.llm.types import LlmUsage
from api.ops.queries import OpsQueries
from api.ops.review.rules import review_result
from api.ops.store.artifacts import save_artifact_with_failure_event
from api.ops.store.runs import OpsRunStore, append_event
from api.ops.tracing import trace_span, traceable, update_current_span_metadata


class Intent:
    METRICS_TREND = "metrics_trend"
    ISSUE_LIST = "issue_list"
    PR_LIST = "pr_list"
    ISSUE_CONTRIBUTION = "issue_contribution"
    GRAPH_MODULE = "graph_module"
    SCAN_STATUS = "scan_status"
    DEMO = "demo"
    FALLBACK = "fallback"


def _rule_classify_intent(message: str) -> tuple[str, dict[str, Any]]:
    """基于规则快速分类；返回 (intent, slots)。"""
    msg = message.lower().strip()
    slots: dict[str, Any] = {}

    days_match = re.search(r"(\d+)\s*天", message)
    if days_match:
        slots["days"] = int(days_match.group(1))

    if any(k in msg for k in ("cycle time", "cycle_time", "pr cycle", "周期")):
        slots["metric"] = "cycle-time"
        return Intent.METRICS_TREND, slots

    if any(k in msg for k in ("review time", "review_time", "评审")) or (
        any(k in msg for k in ("中位数", "median"))
        and any(k in msg for k in ("pr", "review", "评审"))
    ):
        slots["metric"] = "review-time"
        return Intent.METRICS_TREND, slots

    if re.search(r"\bissues?\b", msg) or "issue" in msg:
        if any(
            k in msg
            for k in ("多少", "吞吐", "throughput", "有多少", "几个", "中位数", "median", "closed", "关闭")
        ):
            slots["metric"] = "issue-throughput"
            return Intent.METRICS_TREND, slots

    if any(k in msg for k in ("中位数", "median")):
        slots["metric"] = "review-time"
        return Intent.METRICS_TREND, slots

    if any(k in msg for k in ("cycle", "review time", "throughput", "metric", "指标", "均耗时")):
        return Intent.METRICS_TREND, slots

    if re.search(r"issues?\s*列表|issue.*列表|bug.*列表", msg) or msg in ("issues", "issue list"):
        return Intent.ISSUE_LIST, {}

    if re.search(r"pulls?\s*列表|pr.*列表|合并请求.*列表", msg) or msg in ("pulls", "pr list"):
        return Intent.PR_LIST, {}

    # P3-3a: graph / scan 专用子 Agent
    if any(k in msg for k in ("issue_scan", "issue scan", "issu_scan")) or (
        any(k in msg for k in ("scan", "扫描")) and any(k in msg for k in ("issue", "状态", "summary", "摘要"))
    ):
        return Intent.SCAN_STATUS, {}

    if any(k in msg for k in ("模块", "module", "依赖图", "graph")) and any(
        k in msg for k in ("图", "graph", "模块", "依赖", "matrix", "矩阵")
    ):
        return Intent.GRAPH_MODULE, {}

    demo_hits = {
        "p0 完成没": "P0 六任务已于 2026-06-22 全部合并并通过人类 checklist。",
        "p1 做什么": "P1 聚焦 metrics API、ops_run schema、Orchestrator Chat。",
    }
    for key, answer in demo_hits.items():
        if key in msg:
            return Intent.DEMO, {"answer": answer}

    # P3-1: 对比/多 issue 问句 → fallback → ReAct
    # 单 issue（仅 1 个 #N、无对比语义）→ ISSUE_CONTRIBUTION（deep）
    issue_numbers = re.findall(r"#(\d+)", message)
    unique_issues = sorted(set(int(n) for n in issue_numbers))
    msg_lower = message.lower()
    # 强对比词：无论 issue 数量都视为对比
    strong_comparison = ("对比", "比较", "vs", "which", "哪个", "谁更")
    # 弱对比词：仅当 ≥2 个不同 issue 号时才视为对比
    weak_comparison = ("和", "与")
    has_strong = any(k in msg_lower for k in strong_comparison)
    has_weak = any(k in msg_lower for k in weak_comparison) and len(unique_issues) >= 2
    is_comparison = has_strong or has_weak or len(unique_issues) >= 2
    if is_comparison and unique_issues:
        return Intent.FALLBACK, {"issue_numbers": unique_issues}

    if issue_numbers:
        return Intent.ISSUE_CONTRIBUTION, {"issue_number": int(issue_numbers[0])}

    # P3-1: 开放复杂问（含热点、架构等）→ fallback → ReAct
    # 但保留 misroute 防护：纯 metrics 关键词已在上面处理
    return Intent.FALLBACK, {}


def classify_intent(
    message: str,
    run_id: str | None = None,
    store: Any | None = None,
) -> tuple[str, dict[str, Any]]:
    """混合意图分类：默认规则；`OPS_CHAT_LLM_ROUTER=1` 时优先 LLM router。

    当 LLM router 低置信度或异常时，自动降级为 `_rule_classify_intent`，
    并通过 `append_event` 记录 `intent_router.fallback` 事件（提供 run_id/store 时）。
    """
    return _intent_router.classify_intent_with_llm(
        message,
        _rule_classify_intent,
        run_id=run_id,
        store=store,
    )


def is_fast_intent(intent: str) -> bool:
    return intent in (Intent.METRICS_TREND, Intent.ISSUE_LIST, Intent.PR_LIST, Intent.DEMO)


def fast_respond(intent: str, slots: dict[str, Any], queries: OpsQueries) -> dict[str, Any]:
    if intent == Intent.METRICS_TREND:
        return {"type": "metrics", "metrics": _metrics_for_slots(slots, queries)}
    if intent == Intent.ISSUE_LIST:
        items, total = queries.fetch_issues()
        return {"type": "issue_list", "items": items, "total": total}
    if intent == Intent.PR_LIST:
        items, total = queries.fetch_pulls()
        return {"type": "pr_list", "items": items, "total": total}
    if intent == Intent.DEMO:
        return {"type": "demo", "answer": slots.get("answer", "你好，Ops Desk 已就绪。")}
    return {"type": "unknown", "answer": "未识别意图"}


def synthesize(
    query: str,
    result: dict[str, Any],
    *,
    run_id: str | None = None,
    store: OpsRunStore | None = None,
    transcript: list[dict[str, str]] | None = None,
) -> tuple[str, LlmUsage | None]:
    evidence = result.get("evidence", [])
    if result.get("found") is False:
        return result.get("reasoning", result.get("suggestion", "未能完成分析。")), None
    llm_result = synthesize_answer(query, evidence, run_id=run_id, store=store, transcript=transcript)
    return llm_result.content, llm_result.usage


def _resolve_subagent(intent: str | None) -> tuple[str, Any]:
    """按 intent 选择子 Agent 与 delegate 函数。"""
    if intent == Intent.GRAPH_MODULE:
        return "graph_analyst", analyze_graph
    if intent == Intent.SCAN_STATUS:
        return "scan_analyst", analyze_scan
    return "issue_analyst", analyze_issue


def _invoke_subagent(
    agent_name: str,
    delegate_fn: Any,
    query: str,
    slots: dict[str, Any],
    queries: OpsQueries,
    review_feedback: dict[str, Any] | None,
    run_id: str,
    store: OpsRunStore,
    transcript: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    if agent_name == "issue_analyst":
        issue_number = int(slots.get("issue_number", 545))
        return delegate_fn(
            query,
            issue_number,
            queries,
            review_feedback=review_feedback,
            run_id=run_id,
            store=store,
            transcript=transcript,
        )
    return delegate_fn(
        query,
        queries,
        review_feedback=review_feedback,
        run_id=run_id,
        store=store,
        transcript=transcript,
    )


@traceable(capture_input=False, capture_output=False)
def run_deep(
    run_id: str,
    query: str,
    slots: dict[str, Any],
    store: OpsRunStore,
    queries: OpsQueries,
    max_retries: int = 2,
    intent: str | None = None,
    session_id: str | None = None,
) -> dict[str, Any]:
    """deep path：子 Agent → review → synthesize → events（P3-3a 多 Subagent）。"""
    transcript = load_chat_transcript(session_id, store=store)

    agent_name, delegate_fn = _resolve_subagent(intent)
    issue_number = slots.get("issue_number")
    update_current_span_metadata(
        {
            "ops_run_id": run_id,
            "run_id": run_id,
            "agent_role": "deep",
            "route": "deep",
            "intent": intent or "issue_contribution",
            "agent": agent_name,
            "issue_number": issue_number,
            "session_id": session_id,
        }
    )

    store.append_event(run_id, "orchestrator", "run.start", node_id="deep.start")
    store.append_event(
        run_id,
        "orchestrator",
        "router.decision",
        payload={"route": "deep", "intent": intent or "issue_contribution", "slots": slots, "agent": agent_name},
        node_id="classify",
    )
    with trace_span(
        "handoff",
        run_type="tool",
        run_id=run_id,
        session_id=session_id,
        agent_role="deep",
        from_route="classify",
        to_route="deep",
        intent=intent or "issue_contribution",
        agent=agent_name,
    ):
        append_event(
            run_id,
            "handoff",
            handoff_payload(
                from_route="classify",
                to_route="deep",
                intent=intent or "issue_contribution",
                slots=slots,
                agent=agent_name,
            ),
            store=store,
        )

    store.append_event(
        run_id,
        "orchestrator",
        "agent.delegate.start",
        payload={"agent": agent_name, "slots": slots},
        node_id="delegate",
    )

    attempt = 0
    final_verdict = "partial"
    analyst_result: dict[str, Any] = {}
    review_feedback: dict[str, Any] | None = None
    llm_calls = 0
    llm_usages: list[Any] = []
    while attempt <= max_retries:
        analyst_result = _invoke_subagent(
            agent_name,
            delegate_fn,
            query,
            slots,
            queries,
            review_feedback,
            run_id,
            store,
            transcript=transcript,
        )
        _usage_raw = analyst_result.get("_llm_usage", {})
        if _usage_raw:
            u = LlmUsage.from_dict(_usage_raw, step="analyze")
            llm_calls += 1
            llm_usages.append(u)
        store.append_event(
            run_id,
            agent_name,
            "agent.tool.result",
            payload={
                "agent": agent_name,
                "confidence": analyst_result.get("confidence"),
                "reasoning": analyst_result.get("reasoning"),
                "suggestion": analyst_result.get("suggestion"),
                "citations": analyst_result.get("citations", []),
                "issue_number": analyst_result.get("issue_number"),
            },
            node_id=agent_name,
        )

        verdict, detail = review_result(analyst_result, queries)
        with trace_span(
            "review",
            run_type="tool",
            run_id=run_id,
            session_id=session_id,
            agent_role="deep",
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
        # A3: 携带 feedback 进入下一轮
        review_feedback = detail

    answer, synth_usage = synthesize(query, analyst_result, run_id=run_id, store=store, transcript=transcript)
    if synth_usage is not None:
        llm_calls += 1
        llm_usages.append(synth_usage)
    store.append_event(
        run_id,
        "orchestrator",
        "final.answer",
        payload={"answer": answer, "confidence": analyst_result.get("confidence", 0)},
        node_id="synthesize",
    )
    store.update_run(
        run_id,
        status=final_verdict,
        final_answer={
            "answer": answer,
            "agent": agent_name,
            "issue_number": analyst_result.get("issue_number"),
            "verdict": final_verdict,
        },
    )
    # 答案已落 update_run；后续 artifact / metrics 写失败不得拖垮 chat 500
    try:
        save_artifact_with_failure_event(
            run_id,
            "deep.final_answer",
            {
                "answer": answer,
                "agent": agent_name,
                "issue_number": analyst_result.get("issue_number"),
                "verdict": final_verdict,
                "intent": intent or "issue_contribution",
                "route": "deep",
            },
            store=store,
        )
        store.append_event(run_id, "orchestrator", "run.end", node_id="deep.end")
        metrics_json = _build_metrics_json(
            route="deep",
            intent=intent or "issue_contribution",
            llm_calls=llm_calls,
            llm_usages=llm_usages,
        )
        store.update_run_metrics_json(run_id, metrics_json)
        store.append_event(
            run_id,
            "orchestrator",
            "run.metrics",
            payload=metrics_json,
            node_id="deep.metrics",
        )
    except Exception as exc:  # noqa: BLE001 — 收尾旁路；答案已可返回
        logger.warning("deep post-answer store writes failed run_id=%s: %s", run_id, exc)
    return {
        "run_id": run_id,
        "status": final_verdict,
        "answer": answer,
        "agent": agent_name,
        "issue_number": analyst_result.get("issue_number"),
    }


def _build_metrics_json(
    route: str,
    intent: str,
    llm_calls: int,
    llm_usages: list[Any],
    cache_hit: bool = False,
    demo_id: str | None = None,
) -> dict[str, Any]:
    """汇总 run 级 metrics_json。"""
    total_prompt = sum(u.prompt_tokens for u in llm_usages)
    total_completion = sum(u.completion_tokens for u in llm_usages)
    total_tokens = sum(u.total_tokens for u in llm_usages)
    total_latency = sum(u.latency_ms for u in llm_usages)
    provider_cache_hit = sum(u.prompt_cache_hit_tokens for u in llm_usages)
    provider_cache_miss = sum(u.prompt_cache_miss_tokens for u in llm_usages)
    provider_cache_cached = sum(u.cached_tokens for u in llm_usages)
    provider_cache = {
        "hit_tokens": provider_cache_hit,
        "miss_tokens": provider_cache_miss,
        "cached_tokens": provider_cache_cached,
    }
    metrics: dict[str, Any] = {
        "route": route,
        "intent": intent,
    }
    if cache_hit:
        metrics["cache"] = {"demo_id": demo_id or "", "hit": True, "source": "ops_demo_answers"}
        metrics["llm"] = {
            "provider": llm_usages[0].provider if llm_usages else "",
            "model": llm_usages[0].model if llm_usages else "",
            "calls": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "latency_ms": 0,
            "provider_cache": provider_cache,
        }
    else:
        provider = llm_usages[0].provider if llm_usages else ""
        model = llm_usages[0].model if llm_usages else ""
        metrics["llm"] = {
            "provider": provider,
            "model": model,
            "calls": llm_calls,
            "prompt_tokens": total_prompt,
            "completion_tokens": total_completion,
            "total_tokens": total_tokens,
            "latency_ms": total_latency,
            "provider_cache": provider_cache,
        }
    return metrics


def run_fast(
    run_id: str,
    query: str,
    intent: str,
    slots: dict[str, Any],
    store: OpsRunStore,
    queries: OpsQueries,
) -> dict[str, Any]:
    store.append_event(run_id, "orchestrator", "run.start", node_id="fast.start")
    store.append_event(
        run_id,
        "orchestrator",
        "router.decision",
        payload={"route": "fast", "intent": intent, "slots": slots},
        node_id="classify",
    )

    result = fast_respond(intent, slots, queries)
    answer = _render_fast_answer(intent, result)
    store.append_event(
        run_id,
        "orchestrator",
        "final.answer",
        payload={"answer": answer, "type": result.get("type")},
        node_id="fast.respond",
    )
    store.update_run(
        run_id,
        status="done",
        final_answer={"answer": answer, "type": result.get("type")},
    )
    store.append_event(run_id, "orchestrator", "run.end", node_id="fast.end")
    # B5: fast 路径也写 metrics_json（无 LLM 调用）
    metrics_json = _build_metrics_json(
        route="fast",
        intent=intent,
        llm_calls=0,
        llm_usages=[],
    )
    store.update_run_metrics_json(run_id, metrics_json)
    store.append_event(
        run_id,
        "orchestrator",
        "run.metrics",
        payload=metrics_json,
        node_id="fast.metrics",
    )
    return {"run_id": run_id, "status": "done", "answer": answer, "route": "fast"}


def _metrics_for_slots(slots: dict[str, Any], queries: OpsQueries) -> list[dict[str, Any]]:
    """Demo / fast path：slots 指定 metric 时只查单指标。"""
    days = int(slots.get("days") or DEFAULT_DAYS)
    metric = slots.get("metric")
    fetchers = {
        "issue-throughput": queries.issue_throughput_metric,
        "cycle-time": queries.cycle_time_metric,
        "review-time": queries.review_time_metric,
    }
    if metric in fetchers:
        return [fetchers[metric](days)]
    return [
        queries.cycle_time_metric(days),
        queries.review_time_metric(days),
        queries.issue_throughput_metric(days),
    ]


def _format_metric_line(metric_payload: dict[str, Any]) -> str:
    name = metric_payload.get("metric", "")
    days = metric_payload.get("days", DEFAULT_DAYS)
    summary = metric_payload.get("summary") or {}
    if name == "issue-throughput":
        total = summary.get("total", 0)
        avg = summary.get("avg_per_day", 0)
        return f"最近 {days} 天 closed issue 共 {total} 个，平均每天 {avg} 个。"
    if name == "cycle-time":
        avg = summary.get("avg_hours", 0)
        return f"最近 {days} 天 PR cycle time 平均 {avg} 小时。"
    if name == "review-time":
        median = summary.get("median_hours", summary.get("avg_hours", 0))
        return f"最近 {days} 天 PR review time 中位数 {median} 小时。"
    return f"{name}: {summary}"


def _render_fast_answer(intent: str, result: dict[str, Any]) -> str:
    if intent == Intent.DEMO:
        return result.get("answer", "")
    if intent == Intent.METRICS_TREND:
        metrics = result.get("metrics", [])
        return "\n".join(_format_metric_line(m) for m in metrics)
    if intent in (Intent.ISSUE_LIST, Intent.PR_LIST):
        return f"共 {result.get('total', 0)} 条记录"
    return str(result)
