from __future__ import annotations

import os
import time
import uuid
from typing import Any

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from openai import OpenAI

from .rag_env import admin_secret, siliconflow_base
from .text2sql_core import (
    build_sql_prompt,
    build_summary_prompt,
    execute_select_sql,
    is_text2sql_intent,
    llm_generate_sql,
    llm_summarize,
    validate_sql_readonly,
)
from .text2sql_store import get_text2sql_store


def _require_chain_auth(authorization: str | None, x_blog_admin_token: str | None, x_admin_token: str | None) -> None:
    expected_admin = (admin_secret() or "").strip() or None
    expected_api = (os.getenv("API_KEY") or "").strip() or None
    if not expected_admin and not expected_api:
        raise HTTPException(status_code=500, detail="未配置 NEXT_PUBLIC_ADMIN_SECRET / CHAT_API_SECRET 或 API_KEY")

    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()
    elif x_blog_admin_token:
        token = x_blog_admin_token.strip()
    elif x_admin_token:
        token = x_admin_token.strip()

    import hmac

    def _match(expected: str | None) -> bool:
        if not expected:
            return False
        if len(token) != len(expected):
            return False
        return hmac.compare_digest(token.encode("utf-8"), expected.encode("utf-8"))

    if not (_match(expected_admin) or _match(expected_api)):
        raise HTTPException(status_code=401, detail="Unauthorized")


def _now_ms(started_at: float) -> int:
    return int((time.perf_counter() - started_at) * 1000)


def _event(*, typ: str, started_at: float, step_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    return {"type": typ, "ts": _now_ms(started_at), "step_id": step_id, "payload": payload}


async def handle_chain_chat(
    request: Request,
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> JSONResponse:
    """v1：返回可用于前端时间线渲染的 events[]。当前先覆盖 Text2SQL 链路。"""
    _require_chain_auth(authorization, x_blog_admin_token, x_admin_token)

    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc
    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    query = body.get("query")
    if not isinstance(query, str) or not query.strip():
        raise HTTPException(status_code=400, detail="Missing required field: query")

    session_id = body.get("session_id") if isinstance(body.get("session_id"), str) else None
    run_id = str(uuid.uuid4())
    started_at = time.perf_counter()

    events: list[dict[str, Any]] = []

    # v1：只做 text2sql intent；非意图则返回一条 assistant.message
    if not is_text2sql_intent(query):
        events.append(
            _event(
                typ="assistant.message",
                started_at=started_at,
                step_id="s1",
                payload={
                    "role": "assistant",
                    "content": "该问题不像结构化查数问题（Chain Chat v1 当前仅展示 Text2SQL 链路）。",
                },
            )
        )
        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at)},
            )
        )
        return JSONResponse(content={"ok": True, "run_id": run_id, "session_id": session_id, "events": events})

    # 1) retrieve (DDL + examples)
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_retrieve",
            payload={"tool": "text2sql.retrieve", "input": {"query": query}},
        )
    )
    retrieve_err: str | None = None
    retrieved: list[dict[str, Any]] = []
    t_retrieve0 = time.perf_counter()
    try:
        store = get_text2sql_store()
        topk = int(os.getenv("TEXT2SQL_RETRIEVE_TOPK", "6"))
        retrieved = store.search(query, top_k=topk)
    except Exception as exc:  # noqa: BLE001
        retrieve_err = str(exc)
    t_retrieve_ms = int((time.perf_counter() - t_retrieve0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_retrieve",
            payload={
                "output": {"retrieved_count": len(retrieved), "retrieved": retrieved[:6]},
                "error": retrieve_err,
                "latency_ms": t_retrieve_ms,
            },
        )
    )
    if retrieve_err:
        events.append(
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_retrieve",
                payload={"stage": "retrieve", "message": retrieve_err},
            )
        )
        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at)},
            )
        )
        return JSONResponse(status_code=200, content={"ok": False, "run_id": run_id, "session_id": session_id, "events": events})

    # init LLM client
    api_key = os.getenv("SILICONFLOW_API_KEY", "").strip()
    chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")
    oai = OpenAI(api_key=api_key, base_url=siliconflow_base())

    # 2) generate sql
    sql_prompt = build_sql_prompt(query, retrieved)
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_generate_sql",
            payload={"tool": "text2sql.generate_sql", "input": {"query": query}},
        )
    )
    sql_raw = ""
    sql = ""
    gen_err: str | None = None
    t_gen0 = time.perf_counter()
    try:
        sql_raw = llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
        sql = validate_sql_readonly(sql_raw)
    except Exception as exc:  # noqa: BLE001
        gen_err = str(exc)
    t_gen_ms = int((time.perf_counter() - t_gen0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_generate_sql",
            payload={"output": {"sql": sql or sql_raw}, "error": gen_err, "latency_ms": t_gen_ms},
        )
    )
    if gen_err or not (sql or sql_raw):
        events.append(
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_generate_sql",
                payload={"stage": "generate_sql", "message": gen_err or "empty sql"},
            )
        )
        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at)},
            )
        )
        return JSONResponse(status_code=200, content={"ok": False, "run_id": run_id, "session_id": session_id, "events": events})

    # 3) execute sql
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_execute_sql",
            payload={"tool": "text2sql.execute_sql", "input": {"sql": sql}},
        )
    )
    columns: list[str] = []
    rows: list[dict[str, Any]] = []
    exec_err: str | None = None
    t_exec0 = time.perf_counter()
    try:
        columns, rows = execute_select_sql(sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200")))
    except Exception as exc:  # noqa: BLE001
        exec_err = str(exc)
    t_exec_ms = int((time.perf_counter() - t_exec0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_execute_sql",
            payload={
                "output": {"columns": columns, "rows_len": len(rows)},
                "error": exec_err,
                "latency_ms": t_exec_ms,
            },
        )
    )
    if exec_err:
        events.append(
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_execute_sql",
                payload={"stage": "execute_sql", "message": exec_err},
            )
        )
    truncated = len(rows) > 20
    events.append(
        _event(
            typ="sql.result",
            started_at=started_at,
            step_id="q1",
            payload={"sql": sql, "columns": columns, "rows": rows[:20], "truncated": truncated},
        )
    )

    # 4) summarize
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_summarize",
            payload={"tool": "text2sql.summarize", "input": {"query": query}},
        )
    )
    answer = ""
    sum_err: str | None = None
    t_sum0 = time.perf_counter()
    try:
        if rows:
            sum_prompt = build_summary_prompt(query, sql, columns, rows)
            answer = llm_summarize(oai=oai, model=chat_model, prompt=sum_prompt)
        else:
            answer = "未查到数据。"
    except Exception as exc:  # noqa: BLE001
        sum_err = str(exc)
        answer = "未查到数据。" if not rows else f"查询返回 {len(rows)} 行结果。"
    t_sum_ms = int((time.perf_counter() - t_sum0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_summarize",
            payload={"output": {"answer": answer}, "error": sum_err, "latency_ms": t_sum_ms},
        )
    )
    events.append(
        _event(
            typ="assistant.message",
            started_at=started_at,
            step_id="s_answer",
            payload={"role": "assistant", "content": answer},
        )
    )

    events.append(
        _event(
            typ="latency",
            started_at=started_at,
            step_id="l1",
            payload={
                "total_ms": _now_ms(started_at),
                "stages_ms": {
                    "retrieve": t_retrieve_ms,
                    "generate_sql": t_gen_ms,
                    "execute_sql": t_exec_ms,
                    "summarize": t_sum_ms,
                },
            },
        )
    )

    return JSONResponse(
        content={
            "ok": exec_err is None and gen_err is None and retrieve_err is None,
            "run_id": run_id,
            "session_id": session_id,
            "events": events,
        }
    )

