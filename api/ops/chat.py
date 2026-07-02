"""Ops Desk Chat 入口。"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends

from api.ops.chat_service import ChatMessageRequest, handle_ops_chat_message
from api.ops.demo_cache import DemoCacheStore
from api.ops.deps import get_supabase_client, require_ops_secret
from api.ops.llm.context import ops_chat_model_override, ops_chat_resolved_model
from api.ops.llm.model_catalog import get_chat_models_payload
from api.ops.queries import OpsQueries
from api.ops.store import OpsRunStore

router = APIRouter(prefix="/ops/chat", tags=["ops-chat"])


@router.get("/models")
def chat_models(_: None = Depends(require_ops_secret)) -> dict[str, Any]:
    """当前 Provider 可选 Chat 模型列表（前端下拉）。"""
    return get_chat_models_payload()


def _queries() -> OpsQueries:
    return OpsQueries(get_supabase_client())


def _store() -> OpsRunStore:
    return OpsRunStore(get_supabase_client())


def _demo_cache() -> DemoCacheStore:
    return DemoCacheStore(get_supabase_client())


@router.post("/messages")
def chat_messages(
    body: ChatMessageRequest,
    queries: OpsQueries = Depends(_queries),
    store: OpsRunStore = Depends(_store),
    demo_cache: DemoCacheStore = Depends(_demo_cache),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    token = ops_chat_model_override.set(body.model.strip() if body.model else None)
    sticky_token = ops_chat_resolved_model.set(None)
    try:
        return handle_ops_chat_message(body, queries, store, demo_cache)
    finally:
        ops_chat_resolved_model.reset(sticky_token)
        ops_chat_model_override.reset(token)
