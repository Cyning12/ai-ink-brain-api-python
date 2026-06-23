"""Ops Desk Orchestrator FSM（P1-a 手写版 · LangGraph-ready）。"""

from __future__ import annotations

import re
from typing import Any

from api.ops.agents.issue_analyst import analyze_issue
from api.ops.constants import DEFAULT_DAYS
from api.ops.llm import synthesize_answer
from api.ops.queries import OpsQueries
from api.ops.store.runs import OpsRunStore


class Intent:
    METRICS_TREND = "metrics_trend"
    ISSUE_LIST = "issue_list"
    PR_LIST = "pr_list"
    ISSUE_CONTRIBUTION = "issue_contribution"
    DEMO = "demo"
    FALLBACK = "fallback"


def classify_intent(message: str) -> tuple[str, dict[str, Any]]:
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

    demo_hits = {
        "p0 完成没": "P0 六任务已于 2026-06-22 全部合并并通过人类 checklist。",
        "p1 做什么": "P1 聚焦 metrics API、ops_run schema、Orchestrator Chat。",
    }
    for key, answer in demo_hits.items():
        if key in msg:
            return Intent.DEMO, {"answer": answer}

    issue_match = re.search(r"#(\d+)", message)
    if issue_match:
        return Intent.ISSUE_CONTRIBUTION, {"issue_number": int(issue_match.group(1))}

    return Intent.FALLBACK, {}


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


def review_result(result: dict[str, Any], queries: OpsQueries) -> tuple[str, dict[str, Any]]:
    """Review V1–V4；返回 (verdict, detail)。"""
    citations = result.get("citations", [])
    for cite in citations:
        number = cite.get("number")
        if not number:
            continue
        issue = queries.fetch_issue_by_number(int(number))
        pr = queries.fetch_pull_by_number(int(number))
        if not issue and not pr:
            return "fail", {"rule": "V1", "message": f"#{number} 不存在于同步表"}
        url = cite.get("url")
        if url:
            expected_issue = issue.get("html_url") if issue else None
            expected_pr = pr.get("html_url") if pr else None
            if url not in (expected_issue, expected_pr):
                return "fail", {"rule": "V2", "message": f"#{number} url 不匹配"}

    text = result.get("reasoning", "") + " " + result.get("suggestion", "")
    if re.search(r"\b(commit|push|open\s+PR|merge)\b", text, re.I):
        return "fail", {"rule": "V3", "message": "包含 Git 写操作指令"}

    confidence = float(result.get("confidence", 0))
    evidence = result.get("evidence", [])
    if confidence < 0.5 and not evidence:
        return "partial", {"rule": "V4", "message": "置信度低且缺少证据"}

    return "pass", {}


def synthesize(query: str, result: dict[str, Any]) -> str:
    evidence = result.get("evidence", [])
    if result.get("found") is False:
        return result.get("reasoning", "未能找到相关 issue。")
    return synthesize_answer(query, evidence)


def run_deep(
    run_id: str,
    query: str,
    slots: dict[str, Any],
    store: OpsRunStore,
    queries: OpsQueries,
    max_retries: int = 2,
) -> dict[str, Any]:
    """deep path：issue_analyst → review → synthesize → events。"""
    store.append_event(run_id, "orchestrator", "run.start", node_id="deep.start")
    store.append_event(
        run_id,
        "orchestrator",
        "router.decision",
        payload={"route": "deep", "intent": "issue_contribution", "slots": slots},
        node_id="classify",
    )

    issue_number = slots.get("issue_number", 545)
    store.append_event(
        run_id,
        "orchestrator",
        "agent.delegate.start",
        payload={"agent": "issue_analyst", "issue_number": issue_number},
        node_id="delegate",
    )

    attempt = 0
    final_verdict = "partial"
    analyst_result: dict[str, Any] = {}
    review_feedback: dict[str, Any] | None = None
    while attempt <= max_retries:
        analyst_result = analyze_issue(query, issue_number, queries, review_feedback=review_feedback)
        # A4: expanded payload
        store.append_event(
            run_id,
            "issue_analyst",
            "agent.tool.result",
            payload={
                "issue_number": issue_number,
                "confidence": analyst_result.get("confidence"),
                "reasoning": analyst_result.get("reasoning"),
                "suggestion": analyst_result.get("suggestion"),
                "citations": analyst_result.get("citations", []),
            },
            node_id="issue_analyst",
        )

        verdict, detail = review_result(analyst_result, queries)
        store.append_event(
            run_id,
            "review",
            f"review.{verdict}",
            payload={"rule": detail.get("rule"), "message": detail.get("message"), "attempt": attempt},
            node_id="review",
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

    answer = synthesize(query, analyst_result)
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
        final_answer={"answer": answer, "issue_number": issue_number, "verdict": final_verdict},
    )
    store.append_event(run_id, "orchestrator", "run.end", node_id="deep.end")
    return {
        "run_id": run_id,
        "status": final_verdict,
        "answer": answer,
        "issue_number": issue_number,
    }


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
