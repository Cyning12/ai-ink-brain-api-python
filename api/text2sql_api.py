from __future__ import annotations

import os
import time
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
    try_summarize_aggregate,
    validate_sql_readonly,
)
from .text2sql_store import get_text2sql_store
from .text2sql_value_hints import build_value_hints_block_for_text2sql


def _require_text2sql_auth(authorization: str | None, x_blog_admin_token: str | None, x_admin_token: str | None) -> None:
    expected_admin = (admin_secret() or "").strip() or None
    expected_api = (os.getenv("API_KEY") or "").strip() or None
    if not expected_admin and not expected_api:
        raise HTTPException(status_code=500, detail="未配置 SYNC_ADMIN_SECRET 或 API_KEY")

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


def _t2s_debug(msg: str) -> None:
    if (os.getenv("TEXT2SQL_DEBUG") or "").strip().lower() in ("1", "true", "yes", "on"):
        print(f"[text2sql] {msg}", flush=True)


async def handle_text2sql_chat(
    request: Request,
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> JSONResponse:
    _require_text2sql_auth(authorization, x_blog_admin_token, x_admin_token)

    try:
        body = await request.json()
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail="Invalid JSON") from exc

    if not isinstance(body, dict):
        raise HTTPException(status_code=400, detail="Invalid JSON")

    query = body.get("query")
    if not isinstance(query, str) or not query.strip():
        return JSONResponse(status_code=400, content={"ok": False, "error": "Missing required field: query"})

    session_id = body.get("session_id") if isinstance(body.get("session_id"), str) else None

    if not is_text2sql_intent(query):
        return JSONResponse(
            status_code=200,
            content={
                "ok": True,
                "mode": "non_text2sql",
                "answer": "该问题不像结构化查数问题（Text2SQL v1 仅处理查库类问题）。请换一种提问方式或走普通聊天/RAG。",
                "sql": "",
                "columns": [],
                "rows": [],
                "retrieved": [],
                "session_id": session_id,
            },
        )

    t0 = time.perf_counter()
    try:
        store = get_text2sql_store()
        topk = int(os.getenv("TEXT2SQL_RETRIEVE_TOPK", "6"))
        retrieved = store.search(query, top_k=topk)
    except Exception as exc:  # noqa: BLE001
        _t2s_debug(f"store init/search failed: {exc!s}")
        raise HTTPException(status_code=500, detail=f"Text2SQL store init failed: {exc!s}") from exc
    _t2s_debug(f"query={query!r} retrieved={len(retrieved)} topk={topk}")

    api_key = os.getenv("SILICONFLOW_API_KEY", "").strip()
    chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")
    oai = OpenAI(api_key=api_key, base_url=siliconflow_base())

    sql_prompt = build_sql_prompt(
        query,
        retrieved,
        value_hints_block=build_value_hints_block_for_text2sql(retrieved, history=None),
    )
    sql_raw = ""
    sql = ""
    gen_err: str | None = None
    try:
        sql_raw = llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
        sql = validate_sql_readonly(sql_raw)
    except Exception as exc:  # noqa: BLE001
        gen_err = str(exc)
        sql = ""

    columns: list[str] = []
    rows: list[dict[str, Any]] = []
    exec_err: str | None = None
    if sql:
        try:
            columns, rows = execute_select_sql(sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200")))
        except Exception as exc:  # noqa: BLE001
            exec_err = str(exc)

    answer = ""
    sum_err: str | None = None
    try:
        agg = try_summarize_aggregate(query, columns, rows) if rows else None
        if agg:
            answer = agg
        elif rows:
            sum_prompt = build_summary_prompt(query, sql or sql_raw, columns, rows)
            answer = llm_summarize(oai=oai, model=chat_model, prompt=sum_prompt)
        else:
            answer = "未查到数据。"
    except Exception as exc:  # noqa: BLE001
        sum_err = str(exc)
        # 兜底：不依赖 LLM 的简短回答
        if rows:
            answer = f"查询返回 {len(rows)} 行结果。"
        else:
            answer = "未查到数据。"

    latency_ms = int((time.perf_counter() - t0) * 1000)
    return JSONResponse(
        content={
            "ok": True,
            "mode": "text2sql",
            "session_id": session_id,
            "query": query,
            "answer": answer,
            "sql": sql or sql_raw,
            "columns": columns,
            "rows": rows,
            "retrieved": retrieved,
            "errors": {"generate_sql": gen_err, "execute_sql": exec_err, "summarize": sum_err},
            "latency_ms": latency_ms,
        }
    )

