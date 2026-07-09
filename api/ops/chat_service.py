"""Ops Chat 消息编排（单轮与 session 多轮复用）。"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from api.ops.demo_cache import DemoCacheStore
from api.ops.orchestrator import classify_intent, is_fast_intent, run_deep, run_fast, run_react_fallback
from api.ops.orchestrator.core import Intent
from api.ops.queries import OpsQueries
from api.ops.store import OpsRunStore
from api.ops.tracing import flush_traces


class ChatMessageRequest(BaseModel):
    message: str
    session_id: str | None = None
    model: str | None = None


def _answer_from_cache(cached: dict[str, Any]) -> str:
    answer_json = cached.get("answer_json") or {}
    return str(answer_json.get("answer", ""))


def _run_demo_cache_hit(
    demo_id: str,
    message: str,
    session_id: str | None,
    store: OpsRunStore,
    cached: dict[str, Any],
) -> dict[str, Any]:
    run = store.create_run(query=message, route="fast", session_id=session_id)
    run_id = str(run["id"])
    store.append_event(
        run_id,
        "orchestrator",
        "demo.cache.hit",
        payload={"demo_id": demo_id},
        node_id="demo.cache",
    )
    answer = _answer_from_cache(cached)
    store.update_run(
        run_id,
        status="done",
        final_answer={"answer": answer, "demo_id": demo_id, "demo_hit": True},
    )
    metrics_json = {
        "cache": {"demo_id": demo_id, "hit": True, "source": "ops_demo_answers"},
        "llm": {
            "provider": "",
            "model": "",
            "calls": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "latency_ms": 0,
        },
        "route": "fast",
        "intent": "demo",
    }
    store.update_run_metrics_json(run_id, metrics_json)
    store.append_event(run_id, "orchestrator", "run.metrics", payload=metrics_json, node_id="fast.metrics")
    store.append_event(run_id, "orchestrator", "run.end", node_id="fast.end")
    return {
        "run_id": run_id,
        "route": "fast",
        "status": "done",
        "answer": answer,
        "demo_hit": True,
        "demo_id": demo_id,
    }


def handle_ops_chat_message(
    body: ChatMessageRequest,
    queries: OpsQueries,
    store: OpsRunStore,
    demo_cache: DemoCacheStore,
) -> dict[str, Any]:
    """执行 classify → fast/deep/react 编排（与 legacy /ops/chat/messages 同逻辑）。"""
    demo_match = demo_cache.classifier.classify(body.message)
    if demo_match:
        cached = demo_cache.get(demo_match["demo_id"])
        if cached:
            return _run_demo_cache_hit(
                demo_match["demo_id"],
                body.message,
                body.session_id,
                store,
                cached,
            )

        if is_fast_intent(demo_match["intent"]):
            run = store.create_run(query=body.message, route="fast", session_id=body.session_id)
            run_id = str(run["id"])
            result = run_fast(run_id, body.message, demo_match["intent"], demo_match["params"], store, queries)
            demo_cache.set(
                demo_match["demo_id"],
                {"answer": result.get("answer", ""), **demo_match["params"]},
                query_template=demo_match["query_template"],
                params=demo_match["params"],
            )
            return {**result, "demo_id": demo_match["demo_id"], "demo_hit": False}

        run = store.create_run(query=body.message, route="deep", session_id=body.session_id)
        run_id = str(run["id"])
        result = run_deep(
            run_id, body.message, demo_match["params"], store, queries, intent=demo_match["intent"], session_id=body.session_id
        )
        try:
            if result["status"] in ("done", "partial"):
                demo_cache.set(
                    demo_match["demo_id"],
                    {"answer": result.get("answer", ""), **demo_match["params"]},
                    query_template=demo_match["query_template"],
                    params=demo_match["params"],
                )
            return {"route": "deep", **result, "demo_id": demo_match["demo_id"], "demo_hit": False}
        finally:
            flush_traces()

    intent, slots = classify_intent(body.message)

    if intent == Intent.FALLBACK:
        run = store.create_run(query=body.message, route="react", session_id=body.session_id)
        run_id = str(run["id"])
        result = run_react_fallback(run_id, body.message, store, queries, session_id=body.session_id)
        try:
            return {"run_id": run_id, "route": "react", "status": result["status"], "answer": result.get("answer")}
        finally:
            flush_traces()

    route = "fast" if is_fast_intent(intent) else "deep"

    run = store.create_run(query=body.message, route=route, session_id=body.session_id)
    run_id = str(run["id"])

    if route == "fast":
        result = run_fast(run_id, body.message, intent, slots, store, queries)
        return {"run_id": run_id, "route": route, "status": result["status"], "answer": result.get("answer")}

    result = run_deep(run_id, body.message, slots, store, queries, intent=intent, session_id=body.session_id)
    try:
        return {"run_id": run_id, "route": route, "status": result["status"]}
    finally:
        flush_traces()
