"""Ops Desk Chat 入口。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel

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


@router.post("/messages")
def chat_messages(
    body: ChatMessageRequest,
    queries: OpsQueries = Depends(_queries),
    store: OpsRunStore = Depends(_store),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    intent, slots = classify_intent(body.message)
    route = "fast" if is_fast_intent(intent) else "deep"

    run = store.create_run(query=body.message, route=route, session_id=body.session_id)
    run_id = str(run["id"])

    if route == "fast":
        result = run_fast(run_id, body.message, intent, slots, store, queries)
        return {"run_id": run_id, "route": route, "status": result["status"], "answer": result.get("answer")}

    result = run_deep(run_id, body.message, slots, store, queries)
    return {"run_id": run_id, "route": route, "status": result["status"]}
