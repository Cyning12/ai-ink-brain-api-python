"""Ops Session REST（S1 · multiturn · 文件 + ops_runs 双真值）。"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel, Field

from api.harness_runtime.errors import (
    HarnessRuntimeError,
    SessionIdMismatchError,
    SessionSchemaUnsupportedError,
)
from api.harness_runtime.session_store.io import (
    create_session,
    default_sessions_root,
    list_sessions,
    load_meta,
    save_meta,
    session_dir_for_id,
)
from api.harness_runtime.session_store.schema import SessionMeta, SessionStatus
from api.ops.chat_service import ChatMessageRequest, handle_ops_chat_message
from api.ops.demo_cache import DemoCacheStore
from api.ops.deps import get_supabase_client, require_ops_secret
from api.ops.llm.context import ops_chat_model_override, ops_chat_resolved_model
from api.ops.queries import OpsQueries
from api.ops.store import OpsRunStore

router = APIRouter(prefix="/ops/sessions", tags=["ops-sessions"])


class CreateSessionRequest(BaseModel):
    slug: str = Field(min_length=1, max_length=120)
    title: str = Field(min_length=1, max_length=200)


class SessionMessageRequest(BaseModel):
    message: str = Field(min_length=1)
    model: str | None = None


def _queries() -> OpsQueries:
    return OpsQueries(get_supabase_client())


def _store() -> OpsRunStore:
    return OpsRunStore(get_supabase_client())


def _demo_cache() -> DemoCacheStore:
    return DemoCacheStore(get_supabase_client())


def _sessions_root() -> Path:
    return default_sessions_root()


def _meta_to_dict(meta: SessionMeta) -> dict[str, Any]:
    return meta.model_dump(mode="json")


def _http_error_from_harness(exc: HarnessRuntimeError) -> HTTPException:
    status = 409 if exc.code in {
        "SESSION_SCHEMA_UNSUPPORTED",
        "SESSION_ID_MISMATCH",
        "SESSION_STATUS_INVALID",
    } else 400
    return HTTPException(status_code=status, detail={"code": exc.code, "message": str(exc)})


def _require_session_meta(session_id: str, root: Path) -> tuple[Path, SessionMeta]:
    session_dir = session_dir_for_id(session_id, root)
    if not session_dir.is_dir():
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND"})
    try:
        return session_dir, load_meta(session_dir)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail={"code": "SESSION_NOT_FOUND"}) from exc
    except (SessionSchemaUnsupportedError, SessionIdMismatchError) as exc:
        raise _http_error_from_harness(exc) from exc


def _recent_messages(store: OpsRunStore, session_id: str, *, limit: int = 10) -> list[dict[str, Any]]:
    runs = store.list_runs_by_session_id(session_id, limit=limit)
    items: list[dict[str, Any]] = []
    for run in reversed(runs):
        query = str(run.get("query") or "")
        preview = query if len(query) <= 120 else query[:117] + "..."
        answer = ""
        final = run.get("final_answer")
        if isinstance(final, dict) and isinstance(final.get("answer"), str):
            answer = final["answer"]
        items.append(
            {
                "run_id": str(run.get("id")),
                "role": "user",
                "content_preview": preview,
                "answer_preview": answer[:120] if answer else None,
                "route": run.get("route"),
                "status": run.get("status"),
                "created_at": run.get("created_at"),
            }
        )
    return items


@router.post("")
def create_session_route(
    body: CreateSessionRequest,
    root: Path = Depends(_sessions_root),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    try:
        _session_dir, meta = create_session(slug=body.slug.strip(), title=body.title.strip(), sessions_root=root)
    except FileExistsError as exc:
        raise HTTPException(status_code=409, detail={"code": "SESSION_ALREADY_EXISTS", "message": str(exc)}) from exc
    except HarnessRuntimeError as exc:
        raise _http_error_from_harness(exc) from exc

    return {"session_id": meta.session_id, "meta": _meta_to_dict(meta)}


@router.get("")
def list_sessions_route(
    status: str | None = None,
    limit: Annotated[int, Query(ge=1, le=200)] = 50,
    offset: Annotated[int, Query(ge=0)] = 0,
    root: Path = Depends(_sessions_root),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    status_enum: SessionStatus | None = None
    if status:
        try:
            status_enum = SessionStatus(status)
        except ValueError as exc:
            raise HTTPException(
                status_code=422,
                detail={"code": "SESSION_STATUS_INVALID", "message": f"invalid status: {status}"},
            ) from exc

    try:
        items, total = list_sessions(sessions_root=root, status=status_enum, limit=limit, offset=offset)
    except HarnessRuntimeError as exc:
        raise _http_error_from_harness(exc) from exc

    return {
        "items": [_meta_to_dict(m) for m in items],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@router.get("/{session_id}")
def get_session_route(
    session_id: str,
    store: OpsRunStore = Depends(_store),
    root: Path = Depends(_sessions_root),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    _session_dir, meta = _require_session_meta(session_id, root)
    return {
        "session_id": session_id,
        "meta": _meta_to_dict(meta),
        "gate_summary": meta.gate_summary.model_dump(),
        "recent_messages": _recent_messages(store, session_id),
    }


@router.post("/{session_id}/messages")
def post_session_message(
    session_id: str,
    body: SessionMessageRequest,
    queries: OpsQueries = Depends(_queries),
    store: OpsRunStore = Depends(_store),
    demo_cache: DemoCacheStore = Depends(_demo_cache),
    root: Path = Depends(_sessions_root),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    session_dir, meta = _require_session_meta(session_id, root)
    prior_runs = store.list_runs_by_session_id(session_id, limit=1)

    token = ops_chat_model_override.set(body.model.strip() if body.model else None)
    sticky_token = ops_chat_resolved_model.set(None)
    try:
        chat_body = ChatMessageRequest(message=body.message, session_id=session_id, model=body.model)
        result = handle_ops_chat_message(chat_body, queries, store, demo_cache)
    finally:
        ops_chat_resolved_model.reset(sticky_token)
        ops_chat_model_override.reset(token)

    run_id = str(result.get("run_id", ""))
    if run_id:
        if not prior_runs:
            store.append_event(
                run_id,
                "orchestrator",
                "session.created",
                payload={"session_id": session_id, "slug": meta.slug},
                node_id="session.create",
            )
        meta.latest_run_id = run_id
        meta.updated_at = datetime.now(timezone.utc)
        save_meta(session_dir, meta)
        store.append_event(
            run_id,
            "orchestrator",
            "session.status_changed",
            payload={"session_id": session_id, "status": meta.status.value},
            node_id="session.status",
        )

    return {**result, "session_id": session_id}


@router.get("/{session_id}/events")
def get_session_events(
    session_id: str,
    after_seq: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=500)] = 200,
    store: OpsRunStore = Depends(_store),
    root: Path = Depends(_sessions_root),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    _require_session_meta(session_id, root)
    events = store.list_events_for_session(session_id, after_seq=after_seq, limit=limit)
    return {"session_id": session_id, "after_seq": after_seq, "events": events}
