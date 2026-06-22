"""Ops Desk Chat 入口。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from api.ops.demo_cache import DemoCacheStore
from api.ops.deps import get_supabase_client, require_ops_secret
from api.ops.orchestrator import classify_intent, is_fast_intent, run_deep, run_fast
from api.ops.queries import OpsQueries
from api.ops.store import OpsRunStore

router = APIRouter(prefix="/ops/chat", tags=["ops-chat"])


class ChatMessageRequest(BaseModel):
    message: str
    session_id: str | None = None


def _queries() -> OpsQueries:
    return OpsQueries(get_supabase_client())


def _store() -> OpsRunStore:
    return OpsRunStore(get_supabase_client())


def _demo_cache() -> DemoCacheStore:
    return DemoCacheStore(get_supabase_client())


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
    store.append_event(run_id, "orchestrator", "run.end", node_id="fast.end")
    return {
        "run_id": run_id,
        "route": "fast",
        "status": "done",
        "answer": answer,
        "demo_hit": True,
        "demo_id": demo_id,
    }


@router.post("/messages")
def chat_messages(
    body: ChatMessageRequest,
    queries: OpsQueries = Depends(_queries),
    store: OpsRunStore = Depends(_store),
    demo_cache: DemoCacheStore = Depends(_demo_cache),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
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
        result = run_deep(run_id, body.message, demo_match["params"], store, queries)
        if result["status"] in ("done", "partial"):
            demo_cache.set(
                demo_match["demo_id"],
                {"answer": result.get("answer", ""), **demo_match["params"]},
                query_template=demo_match["query_template"],
                params=demo_match["params"],
            )
        return {"route": "deep", **result, "demo_id": demo_match["demo_id"], "demo_hit": False}

    intent, slots = classify_intent(body.message)
    route = "fast" if is_fast_intent(intent) else "deep"

    run = store.create_run(query=body.message, route=route, session_id=body.session_id)
    run_id = str(run["id"])

    if route == "fast":
        result = run_fast(run_id, body.message, intent, slots, store, queries)
        return {"run_id": run_id, "route": route, "status": result["status"], "answer": result.get("answer")}

    result = run_deep(run_id, body.message, slots, store, queries)
    return {"run_id": run_id, "route": route, "status": result["status"]}
