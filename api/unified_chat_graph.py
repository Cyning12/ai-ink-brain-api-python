from __future__ import annotations

import json
import time
import uuid
from typing import Any, AsyncIterator

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse

from .chatbi_principal import ChatBiPrincipal
from .chatbi_request_ctx import set_chatbi_log_ctx, set_chatbi_principal
from .graph.runner import run_graph_stub
from .graph.state import ChatBIState


def _parse_graph_body(body: dict[str, Any]) -> tuple[str, str | None, str]:
    query = body.get("query")
    if not isinstance(query, str) or not query.strip():
        raise HTTPException(status_code=400, detail="Missing required field: query")
    session_id = body.get("session_id")
    if session_id is not None and not isinstance(session_id, str):
        raise HTTPException(status_code=400, detail="Invalid field: session_id")
    run_id = body.get("run_id")
    if isinstance(run_id, str) and run_id.strip():
        rid = run_id.strip()
    else:
        rid = str(uuid.uuid4())
    return query.strip(), session_id, rid


async def handle_unified_chat_graph(
    request: Request,
    *,
    principal: ChatBiPrincipal,
) -> JSONResponse:
    """Graph 骨架 JSON：HTTP 200 + 最小可核对载荷（Q-8 · 项 5 选项 A）。"""
    set_chatbi_principal(principal)
    set_chatbi_log_ctx({"request_id": (request.headers.get("x-request-id") or "").strip() or None})
    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    query, session_id, run_id = _parse_graph_body(body)
    state = ChatBIState(run_id=run_id, query=query, session_id=session_id)
    state = await run_graph_stub(state)
    return JSONResponse(
        {
            "ok": True,
            "graph_stub": True,
            "run_id": run_id,
            "session_id": session_id,
            "mode": "no_data",
            "answer": state.partial.get("message", ""),
            "current_node": state.current_node,
        }
    )


def _sse(event: str, data: dict[str, Any]) -> str:
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"), default=str)
    return f"event: {event}\ndata: {payload}\n\n"


async def _graph_stream_events(*, run_id: str, session_id: str | None) -> AsyncIterator[str]:
    started_at = time.perf_counter()
    step_id = f"graph-stub-{run_id[:8]}"
    yield _sse(
        "chain",
        {
            "type": "meta",
            "ts": 0,
            "step_id": step_id,
            "payload": {"run_id": run_id, "session_id": session_id, "graph_stub": True},
        },
    )
    yield _sse(
        "done",
        {
            "ok": True,
            "mode": "no_data",
            "run_id": run_id,
            "graph_stub": True,
            "latency_ms": int((time.perf_counter() - started_at) * 1000),
        },
    )


async def handle_unified_chat_graph_stream(
    request: Request,
    *,
    principal: ChatBiPrincipal,
) -> StreamingResponse:
    """Graph 骨架 SSE：meta + done 心跳（不新增 graph.* type · D-5）。"""
    set_chatbi_principal(principal)
    set_chatbi_log_ctx({"request_id": (request.headers.get("x-request-id") or "").strip() or None})
    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    _, session_id, run_id = _parse_graph_body(body)

    return StreamingResponse(
        _graph_stream_events(run_id=run_id, session_id=session_id),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )
