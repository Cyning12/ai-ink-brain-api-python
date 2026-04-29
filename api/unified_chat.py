from __future__ import annotations

import hmac
import os
import re
import time
import uuid
import json
from typing import Any, Literal

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse, StreamingResponse
from openai import OpenAI

from .hybrid_fusion import RRF_K, fuse_hits_rrf
from .query_rewrite import rewrite_query_with_history
from .rag_recall_tools import keyword_query_text_with_i18n_meta, rpc_execute_with_retry, structured_recall_by_date
from .rag_env import (
    admin_secret,
    embedding_kwargs_for_inputs,
    openai_siliconflow_client,
    siliconflow_base,
    supabase_client,
)
from .text2sql_core import build_sql_prompt, build_summary_prompt, execute_select_sql, llm_generate_sql, llm_summarize, validate_sql_readonly
from .text2sql_store import get_text2sql_store
from .intent_router import decide_intent
from .rag_shared import parse_match_threshold, strip_doc_context_prefix
from .agent import ChatBIAgent
from .agent_memory import get_memory_store
from .tools import get_tool_registry


PreferMode = Literal["auto", "rag", "text2sql", "no_data"]


def _require_unified_auth(authorization: str | None, x_blog_admin_token: str | None, x_admin_token: str | None) -> None:
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

_MASK_SECRET_RE = re.compile(r"(?i)\b(sk-[A-Za-z0-9]{10,}|sf-[A-Za-z0-9]{10,}|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b")


def _safe_text_for_event(text: str, *, max_len: int) -> str:
    t = (text or "").replace("\r\n", "\n").replace("\r", "\n")
    t = _MASK_SECRET_RE.sub("***", t)
    t = t.replace("\n", "\\n")
    if len(t) <= max_len:
        return t
    return t[: max_len - 3] + "..."


def _build_query_expand_event_payload(meta: dict[str, Any] | None, *, max_raw: int, max_expanded: int) -> dict[str, Any]:
    if not meta:
        return {"raw": "", "expanded": "", "candidates": [], "source": "none", "truncated": False, "enabled": False, "mode": "off"}
    raw = meta.get("raw") if isinstance(meta.get("raw"), str) else ""
    expanded = meta.get("expanded") if isinstance(meta.get("expanded"), str) else ""
    cands = meta.get("candidates") if isinstance(meta.get("candidates"), list) else []
    safe_cands: list[str] = []
    for c in cands[:8]:
        if isinstance(c, str) and c.strip():
            safe_cands.append(_safe_text_for_event(c.strip(), max_len=48))
    return {
        "raw": _safe_text_for_event(raw, max_len=max_raw),
        "expanded": _safe_text_for_event(expanded, max_len=max_expanded),
        "candidates": safe_cands,
        "source": meta.get("source"),
        "truncated": bool(meta.get("truncated")),
        "enabled": bool(meta.get("enabled")),
        "mode": meta.get("mode"),
    }


def _parse_prefer(raw: object) -> PreferMode:
    if not isinstance(raw, str):
        return "auto"
    v = raw.strip().lower()
    # 允许 no_data：跳过检索/查库，直接生成（用于 i18n/无证据场景兜底）。
    if v in ("rag", "text2sql", "no_data", "auto"):
        return v  # type: ignore[return-value]
    # 允许 tool:* 透传给 intent_router（v1 预留，未实现时会返回 error 事件）。
    if v.startswith("tool:"):
        return v  # type: ignore[return-value]
    return "auto"


def _build_rag_sources_event(hits: list[dict[str, Any]], *, top_k: int = 10) -> dict[str, Any]:
    packed: list[dict[str, Any]] = []
    for h in hits[: max(1, int(top_k))]:
        meta = h.get("metadata") if isinstance(h.get("metadata"), dict) else {}
        content = h.get("content") if isinstance(h.get("content"), str) else ""
        snippet = strip_doc_context_prefix(content).replace("\r\n", "\n").strip()
        snippet = snippet[:400] if len(snippet) > 400 else snippet
        packed.append(
            {
                "id": h.get("id"),
                "content": snippet,
                "filename": meta.get("filename"),
                "score": h.get("fused_score"),
                "path": meta.get("relativePath"),
                "url": meta.get("original_link"),
                "relativePath": meta.get("relativePath"),
                "slug": meta.get("slug"),
                "original_link": meta.get("original_link"),
                "category": meta.get("category"),
                "chunk_index": meta.get("chunk_index"),
                "snippet": snippet,
                "fused_score": h.get("fused_score"),
            }
        )
    return {"sources": packed, "retrieval": {"top_k": int(top_k), "rrf_k": RRF_K}}


def _rag_generate_answer(*, oai: OpenAI, chat_model: str, query: str, hits: list[dict[str, Any]]) -> str:
    parts: list[str] = []
    for i, h in enumerate(hits[:12]):
        content = h.get("content")
        if not isinstance(content, str) or not content.strip():
            continue
        parts.append(f"[#{i + 1}]\n{content.strip()}")
    context = "\n\n---\n\n".join(parts)
    system = (
        "你是一个检索增强问答助手。请仅基于提供的上下文回答；若上下文不足以回答，请明确说明不确定。\n"
        "回答要求：中文、简洁、给出关键结论；必要时引用上下文要点。"
    )
    user = f"【上下文】\n{context}\n\n【问题】\n{query}\n"
    res = oai.chat.completions.create(
        model=chat_model,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0.2,
        stream=False,
    )
    return (res.choices[0].message.content or "").strip()


async def handle_unified_chat(
    request: Request,
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> JSONResponse:
    _require_unified_auth(authorization, x_blog_admin_token, x_admin_token)

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
    prefer = _parse_prefer(body.get("prefer"))

    started_at = time.perf_counter()
    run_id = str(uuid.uuid4())
    events: list[dict[str, Any]] = []

    def finish(*, ok: bool, mode: str) -> JSONResponse:
        return JSONResponse(
            content={"ok": ok, "run_id": run_id, "session_id": session_id, "mode": mode, "events": events}
        )

    # CHATBI v2（Agent）主路径：开关开启时，输出 agent.* 事件
    use_agent = (os.getenv("CHATBI_USE_AGENT", "false") or "").strip().lower() in ("1", "true", "yes", "on")
    if use_agent:
        # prefer=tool:* 仍按 v1 路由返回 error（保持行为一致）
        if str(prefer).startswith("tool:"):
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_agent",
                    payload={"stage": "agent", "message": f"未实现的工具路由：{prefer}"},
                )
            )
            events.append(
                _event(
                    typ="latency",
                    started_at=started_at,
                    step_id="l1",
                    payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                )
            )
            return finish(ok=False, mode=str(prefer))

        tool_registry = get_tool_registry()
        agent = ChatBIAgent(tools=tool_registry.list_tools(), memory=get_memory_store())
        agent_result = await agent.run(query=query, session_id=session_id, prefer=prefer)

        mode = agent_result.final.mode
        max_steps = max(1, int(os.getenv("AGENT_MAX_STEPS", "5")))

        # router.decision：Agent 初始决策（V1 payload 结构保持一致）
        intent_decision = agent_result.intent_decision
        step1 = agent_result.steps[0] if agent_result.steps else None
        step1_mode = step1.mode if step1 else mode
        candidate_mode = intent_decision.mode if intent_decision else step1_mode
        final_mode = step1_mode

        events.append(
            _event(
                typ="router.decision",
                started_at=started_at,
                step_id="r1",
                payload={
                    "prefer": "auto" if prefer == "auto" else prefer,
                    "candidate_mode": candidate_mode,
                    "final_mode": final_mode,
                    "rule_hits": [],
                    "evidence": {"agent_reasoning": intent_decision.reasoning_full if intent_decision else ""},
                    "fallback": intent_decision.fallback if intent_decision else None,
                },
            )
        )

        # 事件流：agent.step.start → (step1) agent.intent → agent.think → tool.call.start/end → agent.step.end
        for step in agent_result.steps:
            step_id = f"a{step.step_number}"
            events.append(
                _event(
                    typ="agent.step.start",
                    started_at=started_at,
                    step_id=step_id,
                    payload={"step_number": step.step_number, "max_steps": max_steps},
                )
            )

            if step.step_number == 1 and intent_decision is not None:
                events.append(
                    _event(
                        typ="agent.intent",
                        started_at=started_at,
                        step_id="intent_1",
                        payload={
                            "tool": intent_decision.tool,
                            "mode": intent_decision.mode,
                            "reasoning": intent_decision.reasoning,
                            "confidence": intent_decision.confidence,
                            "fallback": intent_decision.fallback,
                        },
                    )
                )

            events.append(
                _event(
                    typ="agent.think",
                    started_at=started_at,
                    step_id=f"{step_id}_think",
                    payload={
                        "step_number": step.step_number,
                        "thought": step.think_payload["thought"],
                        "selected_tool": step.think_payload["selected_tool"],
                        "mode": step.think_payload["mode"],
                        "confidence": step.think_payload["confidence"],
                    },
                )
            )

            events.append(
                _event(
                    typ="tool.call.start",
                    started_at=started_at,
                    step_id=f"t_step{step.step_number}",
                    payload={"tool": step.tool_used, "input": {"query": query}},
                )
            )

            err = step.tool_result.error
            out_answer: str | None = None
            if step.tool_result.data and isinstance(step.tool_result.data.get("answer"), str):
                out_answer = step.tool_result.data.get("answer")

            events.append(
                _event(
                    typ="tool.call.end",
                    started_at=started_at,
                    step_id=f"t_step{step.step_number}",
                    payload={
                        "output": {"answer": out_answer},
                        "error": err,
                        "latency_ms": step.tool_result.latency_ms,
                    },
                )
            )

            # 可视化来源：按工具类型补齐 v1 事件
            if step.tool_used == "text2sql_query" and step.tool_result.success and step.tool_result.data:
                data = step.tool_result.data
                columns = data.get("columns") if isinstance(data.get("columns"), list) else []
                rows_any = data.get("rows") if isinstance(data.get("rows"), list) else []
                rows: list[dict[str, Any]] = [r for r in rows_any if isinstance(r, dict)]
                truncated = len(rows) > 20
                events.append(
                    _event(
                        typ="sql.result",
                        started_at=started_at,
                        step_id=f"q_step{step.step_number}",
                        payload={
                            "sql": data.get("sql") if isinstance(data.get("sql"), str) else "",
                            "columns": [c for c in columns if isinstance(c, str)],
                            "rows": rows[:20],
                            "truncated": truncated,
                        },
                    )
                )
            elif step.tool_used == "rag_search" and step.tool_result.success and step.tool_result.data:
                data = step.tool_result.data
                hits_any = data.get("hits")
                hits: list[dict[str, Any]] = hits_any if isinstance(hits_any, list) else []
                rag_sources_payload = _build_rag_sources_event(hits, top_k=10)
                events.append(
                    _event(
                        typ="rag.sources",
                        started_at=started_at,
                        step_id=f"s_step{step.step_number}",
                        payload=rag_sources_payload,
                    )
                )

            events.append(
                _event(
                    typ="agent.step.end",
                    started_at=started_at,
                    step_id=f"{step_id}_end",
                    payload={
                        "step_number": step.step_number,
                        "tool_used": step.tool_used,
                        "mode": step.mode,
                        "success": step.success,
                        "next_action": step.next_action,
                    },
                )
            )

        events.append(
            _event(
                typ="agent.final",
                started_at=started_at,
                step_id="a_final",
                payload={
                    "total_steps": agent_result.final.total_steps,
                    "tools_used": agent_result.final.tools_used,
                    "modes": agent_result.final.modes,
                    "fallback_used": agent_result.final.fallback_used,
                },
            )
        )

        events.append(
            _event(
                typ="assistant.message",
                started_at=started_at,
                step_id="s_answer",
                payload={"role": "assistant", "content": agent_result.final.answer},
            )
        )

        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
            )
        )

        # 记忆持久化：仅一轮结束写一次（JSONB：agent_steps/tool_results）
        try:
            sb = supabase_client()
            agent_steps_json: dict[str, Any] = {
                "total_steps": agent_result.final.total_steps,
                "tools_used": agent_result.final.tools_used,
                "fallback_used": agent_result.final.fallback_used,
                "steps": [
                    {
                        "step_number": s.step_number,
                        "tool_used": s.tool_used,
                        "mode": s.mode,
                        "success": s.success,
                        "next_action": s.next_action,
                        "thought": s.think_payload.get("thought"),
                    }
                    for s in agent_result.steps
                ],
            }
            tool_results_json: dict[str, Any] = {
                "results": [
                    {
                        "tool": s.tool_used,
                        "success": s.tool_result.success,
                        "error_code": s.tool_result.error_code,
                        "error_stage": s.tool_result.error_stage,
                        "latency_ms": s.tool_result.latency_ms,
                        "answer": (s.tool_result.data or {}).get("answer") if s.tool_result.data else None,
                    }
                    for s in agent_result.steps
                ]
            }
            if session_id:
                sb.table("rag_conversation_logs").insert(
                    {
                        "session_id": session_id,
                        "query": query,
                        "rewritten_query": query,
                        "retrieved_context": {},
                        "response": agent_result.final.answer,
                        "metadata": {"mode": agent_result.final.mode, "v": "chatbi_v2_agent"},
                        "agent_steps": agent_steps_json,
                        "tool_results": tool_results_json,
                    }
                ).execute()
        except Exception:
            # 记忆写入降级：不阻断对外回答
            pass

        return finish(ok=True, mode=mode)

    # mode decide (v1 router)
    decision = decide_intent(query=query, prefer=prefer)
    mode = decision.final_mode
    events.append(
        _event(
            typ="router.decision",
            started_at=started_at,
            step_id="r1",
            payload={
                "prefer": decision.prefer,
                "candidate_mode": decision.candidate_mode,
                "final_mode": decision.final_mode,
                "rule_hits": decision.rule_hits,
                "evidence": decision.evidence,
                "fallback": decision.fallback,
            },
        )
    )

    if mode.startswith("tool:"):
        events.append(
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_tool",
                payload={"stage": "router", "message": f"未实现的工具路由：{mode}"},
            )
        )
        events.append(
            _event(
                typ="latency",
                started_at=started_at,
                step_id="l1",
                payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
            )
        )
        return finish(ok=False, mode=mode)

    if mode == "no_data":
        oai = openai_siliconflow_client()
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_generate",
                payload={"tool": "no_data.generate", "input": {"query": query}},
            )
        )
        t0 = time.perf_counter()
        ans = ""
        gen_err: str | None = None
        try:
            res = oai.chat.completions.create(
                model=chat_model,
                messages=[
                    {"role": "system", "content": "你是一个中文助手。用户的问题不需要检索或查库，请直接回答。"},
                    {"role": "user", "content": query},
                ],
                temperature=0.7,
                stream=False,
            )
            ans = (res.choices[0].message.content or "").strip()
        except Exception as exc:  # noqa: BLE001
            gen_err = str(exc)
            ans = "对话生成失败。"
        t_gen_ms = int((time.perf_counter() - t0) * 1000)
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_generate",
                payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms},
            )
        )
        if gen_err:
            events.append(_event(typ="error", started_at=started_at, step_id="e_generate", payload={"stage": "no_data.generate", "message": gen_err}))
        events.append(_event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": ans}))
        events.append(_event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"generate": t_gen_ms}}))
        return finish(ok=gen_err is None, mode=mode)

    if mode == "text2sql":
        # ---- Text2SQL branch: reuse chain-like events ----
        # retrieve
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_retrieve",
                payload={"tool": "text2sql.retrieve", "input": {"query": query}},
            )
        )
        t0 = time.perf_counter()
        retrieve_err: str | None = None
        retrieved: list[dict[str, Any]] = []
        try:
            store = get_text2sql_store()
            topk = int(os.getenv("TEXT2SQL_RETRIEVE_TOPK", "6"))
            retrieved = store.search(query, top_k=topk)
        except Exception as exc:  # noqa: BLE001
            retrieve_err = str(exc)
        t_retrieve_ms = int((time.perf_counter() - t0) * 1000)
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
                    payload={"stage": "text2sql.retrieve", "message": retrieve_err},
                )
            )
            events.append(
                _event(
                    typ="latency",
                    started_at=started_at,
                    step_id="l1",
                    payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                )
            )
            return finish(ok=False, mode=mode)

        oai = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY", "").strip(), base_url=siliconflow_base())
        chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

        # generate sql
        sql_prompt = build_sql_prompt(query, retrieved)
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_generate_sql",
                payload={"tool": "text2sql.generate_sql", "input": {"query": query}},
            )
        )
        t1 = time.perf_counter()
        sql_raw = ""
        sql = ""
        gen_err: str | None = None
        try:
            sql_raw = llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
            sql = validate_sql_readonly(sql_raw)
        except Exception as exc:  # noqa: BLE001
            gen_err = str(exc)
        t_gen_ms = int((time.perf_counter() - t1) * 1000)
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
                    payload={"stage": "text2sql.generate_sql", "message": gen_err or "empty sql"},
                )
            )
            events.append(
                _event(
                    typ="latency",
                    started_at=started_at,
                    step_id="l1",
                    payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                )
            )
            return finish(ok=False, mode=mode)

        # execute sql
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_execute_sql",
                payload={"tool": "text2sql.execute_sql", "input": {"sql": sql}},
            )
        )
        t2 = time.perf_counter()
        columns: list[str] = []
        rows: list[dict[str, Any]] = []
        exec_err: str | None = None
        try:
            columns, rows = execute_select_sql(sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200")))
        except Exception as exc:  # noqa: BLE001
            exec_err = str(exc)
        t_exec_ms = int((time.perf_counter() - t2) * 1000)
        events.append(
            _event(
                typ="tool.call.end",
                started_at=started_at,
                step_id="t_execute_sql",
                payload={"output": {"columns": columns, "rows_len": len(rows)}, "error": exec_err, "latency_ms": t_exec_ms},
            )
        )
        if exec_err:
            events.append(
                _event(
                    typ="error",
                    started_at=started_at,
                    step_id="e_execute_sql",
                    payload={"stage": "text2sql.execute_sql", "message": exec_err},
                )
            )
        events.append(
            _event(
                typ="sql.result",
                started_at=started_at,
                step_id="q1",
                payload={"sql": sql, "columns": columns, "rows": rows[:20], "truncated": len(rows) > 20},
            )
        )

        # summarize
        events.append(
            _event(
                typ="tool.call.start",
                started_at=started_at,
                step_id="t_summarize",
                payload={"tool": "text2sql.summarize", "input": {"query": query}},
            )
        )
        t3 = time.perf_counter()
        answer = ""
        sum_err: str | None = None
        try:
            if rows:
                sum_prompt = build_summary_prompt(query, sql, columns, rows)
                answer = llm_summarize(oai=oai, model=chat_model, prompt=sum_prompt)
            else:
                answer = "未查到数据。"
        except Exception as exc:  # noqa: BLE001
            sum_err = str(exc)
            answer = "未查到数据。" if not rows else f"查询返回 {len(rows)} 行结果。"
        t_sum_ms = int((time.perf_counter() - t3) * 1000)
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
                    "stages_ms": {"retrieve": t_retrieve_ms, "generate_sql": t_gen_ms, "execute_sql": t_exec_ms, "summarize": t_sum_ms},
                },
            )
        )
        return finish(ok=exec_err is None and gen_err is None, mode=mode)

    # ---- RAG branch (non-streaming v1) ----
    oai = openai_siliconflow_client()
    chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

    # rewrite
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_rewrite",
            payload={"tool": "rag.rewrite", "input": {"query": query}},
        )
    )
    t_rw0 = time.perf_counter()
    rewritten = query
    rw_err: str | None = None
    try:
        rewritten = await rewrite_query_with_history(oai=oai, query=query, history=[], chat_model=chat_model)
    except Exception as exc:  # noqa: BLE001
        rw_err = str(exc)
        rewritten = query
    t_rw_ms = int((time.perf_counter() - t_rw0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_rewrite",
            payload={"output": {"rewritten_query": rewritten}, "error": rw_err, "latency_ms": t_rw_ms},
        )
    )

    # embed
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_embed",
            payload={"tool": "rag.embed", "input": {"query": rewritten}},
        )
    )
    t_emb0 = time.perf_counter()
    vec: list[float] | None = None
    emb_err: str | None = None
    try:
        emb_res = oai.embeddings.create(**embedding_kwargs_for_inputs([rewritten]))
        vec = list(emb_res.data[0].embedding)
    except Exception as exc:  # noqa: BLE001
        emb_err = str(exc)
        vec = None
    t_emb_ms = int((time.perf_counter() - t_emb0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_embed",
            payload={"output": {"vec_available": vec is not None}, "error": emb_err, "latency_ms": t_emb_ms},
        )
    )

    # retrieve
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_retrieve",
            payload={"tool": "rag.retrieve", "input": {"query": rewritten}},
        )
    )
    t_ret0 = time.perf_counter()
    vector_hits: list[dict[str, Any]] = []
    structured_hits: list[dict[str, Any]] = []
    keyword_hits_raw: list[dict[str, Any]] = []
    keyword_hits_rewrite: list[dict[str, Any]] = []
    hits: list[dict[str, Any]] = []
    ret_err: str | None = None
    retry_count = 0
    try:
        sb = supabase_client()
        # structured recall（日期类确定性召回）
        structured_hits = structured_recall_by_date(sb, query=query, rewritten=rewritten, limit_rows=6).hits
        match_threshold = parse_match_threshold()
        match_count = int(os.getenv("RAG_MATCH_COUNT", "10"))
        if vec is not None:
            vector_hits, rc_vec, err_vec = rpc_execute_with_retry(
                sb,
                "match_documents",
                {"query_embedding": vec, "match_count": match_count, "match_threshold": match_threshold},
                retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
            )
            retry_count += rc_vec
            if err_vec:
                ret_err = err_vec

        kw_qt_raw, kw_meta_raw = keyword_query_text_with_i18n_meta(query)
        kw_qt_rw, kw_meta_rw = keyword_query_text_with_i18n_meta(rewritten)
        events.append(
            _event(
                typ="rag.query_expand",
                started_at=started_at,
                step_id="q_expand",
                payload={
                    "raw": _build_query_expand_event_payload(kw_meta_raw, max_raw=160, max_expanded=220),
                    "rewrite": _build_query_expand_event_payload(kw_meta_rw, max_raw=160, max_expanded=220),
                },
            )
        )

        keyword_hits_raw, rc_raw, err_raw = rpc_execute_with_retry(
            sb,
            "keyword_documents",
            {"query_text": kw_qt_raw, "match_count": 12},
            retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
        )
        retry_count += rc_raw
        if err_raw:
            ret_err = err_raw

        keyword_hits_rewrite, rc_rw, err_rw = rpc_execute_with_retry(
            sb,
            "keyword_documents",
            {"query_text": kw_qt_rw, "match_count": 12},
            retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
        )
        retry_count += rc_rw
        if err_rw:
            ret_err = err_rw

        merged_keyword = fuse_hits_rrf(keyword_hits_raw, keyword_hits_rewrite, max_total=22)
        merged_kw2 = fuse_hits_rrf(structured_hits, merged_keyword, max_total=22)
        hits = fuse_hits_rrf(vector_hits, merged_kw2, max_total=22)
    except Exception as exc:  # noqa: BLE001
        ret_err = str(exc)
        hits = []
    t_ret_ms = int((time.perf_counter() - t_ret0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_retrieve",
            payload={
                "output": {
                    "vector_hits": len(vector_hits),
                    "structured_hits": len(structured_hits),
                    "keyword_hits_raw": len(keyword_hits_raw),
                    "keyword_hits_rewrite": len(keyword_hits_rewrite),
                    "hits": len(hits),
                    "retry_count": retry_count,
                    "embedding_error": emb_err,
                },
                "error": ret_err,
                "latency_ms": t_ret_ms,
            },
        )
    )

    sources_payload = _build_rag_sources_event(hits, top_k=10)
    events.append(
        _event(
            typ="rag.sources",
            started_at=started_at,
            step_id="s_sources",
            payload=sources_payload,
        )
    )

    # generate
    events.append(
        _event(
            typ="tool.call.start",
            started_at=started_at,
            step_id="t_generate",
            payload={"tool": "rag.generate", "input": {"query": query}},
        )
    )
    t_gen0 = time.perf_counter()
    ans = ""
    gen_err: str | None = None
    try:
        ans = _rag_generate_answer(oai=oai, chat_model=chat_model, query=query, hits=hits)
        if not ans:
            ans = "我暂时无法根据现有资料给出确定回答。"
    except Exception as exc:  # noqa: BLE001
        gen_err = str(exc)
        ans = "对话生成失败。"
    t_gen_ms = int((time.perf_counter() - t_gen0) * 1000)
    events.append(
        _event(
            typ="tool.call.end",
            started_at=started_at,
            step_id="t_generate",
            payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms},
        )
    )
    if gen_err:
        events.append(
            _event(
                typ="error",
                started_at=started_at,
                step_id="e_generate",
                payload={"stage": "rag.generate", "message": gen_err},
            )
        )

    events.append(
        _event(
            typ="assistant.message",
            started_at=started_at,
            step_id="s_answer",
            payload={"role": "assistant", "content": ans},
        )
    )
    events.append(
        _event(
            typ="latency",
            started_at=started_at,
            step_id="l1",
            payload={"total_ms": _now_ms(started_at), "stages_ms": {"rewrite": t_rw_ms, "embed": t_emb_ms, "retrieve": t_ret_ms, "generate": t_gen_ms}},
        )
    )
    return finish(ok=gen_err is None, mode=mode)


def _sse(event: str, data: dict[str, Any]) -> str:
    # SSE 要求每条消息以空行结束
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    return f"event: {event}\ndata: {payload}\n\n"


async def handle_unified_chat_stream(
    request: Request,
    *,
    authorization: str | None,
    x_blog_admin_token: str | None,
    x_admin_token: str | None,
) -> StreamingResponse:
    """SSE：实时输出 chain 事件，最终输出 done。v1 不强制 token 级文本流。"""
    _require_unified_auth(authorization, x_blog_admin_token, x_admin_token)

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
    prefer = _parse_prefer(body.get("prefer"))

    started_at = time.perf_counter()
    run_id = str(uuid.uuid4())

    # CHATBI v2（Agent）SSE 主路径
    use_agent = (os.getenv("CHATBI_USE_AGENT", "false") or "").strip().lower() in ("1", "true", "yes", "on")
    if use_agent:
        if str(prefer).startswith("tool:"):
            ok = False
            mode = str(prefer)

            async def event_stream():
                try:
                    yield _sse(
                        "chain",
                        {"type": "meta", "ts": _now_ms(started_at), "step_id": "m1", "payload": {"run_id": run_id, "mode": mode, "session_id": session_id}},
                    )
                    yield _sse(
                        "chain",
                        _event(
                            typ="error",
                            started_at=started_at,
                            step_id="e_agent",
                            payload={"stage": "agent", "message": f"未实现的工具路由：{prefer}"},
                        ),
                    )
                except GeneratorExit:
                    return
                except Exception as exc:  # noqa: BLE001
                    ok_local = False
                    _ = exc
                    ok = False
                finally:
                    yield _sse(
                        "done",
                        {
                            "ok": ok,
                            "mode": mode,
                            "run_id": run_id,
                            "request_id": run_id,
                            "session_id": session_id,
                        },
                    )

            headers = {"Cache-Control": "no-cache"}
            return StreamingResponse(event_stream(), media_type="text/event-stream; charset=utf-8", headers=headers)

        tool_registry = get_tool_registry()
        agent = ChatBIAgent(tools=tool_registry.list_tools(), memory=get_memory_store())
        agent_result = await agent.run(query=query, session_id=session_id, prefer=prefer)
        mode = agent_result.final.mode
        max_steps = max(1, int(os.getenv("AGENT_MAX_STEPS", "5")))

        # 可选：一轮结束写一次 memory（失败不阻断 SSE）
        try:
            if session_id:
                sb = supabase_client()
                agent_steps_json: dict[str, Any] = {
                    "total_steps": agent_result.final.total_steps,
                    "tools_used": agent_result.final.tools_used,
                    "fallback_used": agent_result.final.fallback_used,
                    "steps": [
                        {
                            "step_number": s.step_number,
                            "tool_used": s.tool_used,
                            "mode": s.mode,
                            "success": s.success,
                            "next_action": s.next_action,
                            "thought": s.think_payload.get("thought"),
                        }
                        for s in agent_result.steps
                    ],
                }
                tool_results_json: dict[str, Any] = {
                    "results": [
                        {
                            "tool": s.tool_used,
                            "success": s.tool_result.success,
                            "error_code": s.tool_result.error_code,
                            "error_stage": s.tool_result.error_stage,
                            "latency_ms": s.tool_result.latency_ms,
                            "answer": (s.tool_result.data or {}).get("answer") if s.tool_result.data else None,
                        }
                        for s in agent_result.steps
                    ]
                }
                sb.table("rag_conversation_logs").insert(
                    {
                        "session_id": session_id,
                        "query": query,
                        "rewritten_query": query,
                        "retrieved_context": {},
                        "response": agent_result.final.answer,
                        "metadata": {"mode": agent_result.final.mode, "v": "chatbi_v2_agent"},
                        "agent_steps": agent_steps_json,
                        "tool_results": tool_results_json,
                    }
                ).execute()
        except Exception:
            pass

        ok = True

        async def event_stream():
            nonlocal ok
            try:
                yield _sse(
                    "chain",
                    {"type": "meta", "ts": _now_ms(started_at), "step_id": "m1", "payload": {"run_id": run_id, "mode": mode, "session_id": session_id}},
                )

                intent_decision = agent_result.intent_decision
                step1 = agent_result.steps[0] if agent_result.steps else None
                step1_mode = step1.mode if step1 else mode
                candidate_mode = intent_decision.mode if intent_decision else step1_mode
                final_mode = step1_mode

                yield _sse(
                    "chain",
                    _event(
                        typ="router.decision",
                        started_at=started_at,
                        step_id="r1",
                        payload={
                            "prefer": "auto" if prefer == "auto" else prefer,
                            "candidate_mode": candidate_mode,
                            "final_mode": final_mode,
                            "rule_hits": [],
                            "evidence": {"agent_reasoning": intent_decision.reasoning_full if intent_decision else ""},
                            "fallback": intent_decision.fallback if intent_decision else None,
                        },
                    ),
                )

                for step in agent_result.steps:
                    step_id = f"a{step.step_number}"
                    yield _sse(
                        "chain",
                        _event(
                            typ="agent.step.start",
                            started_at=started_at,
                            step_id=step_id,
                            payload={"step_number": step.step_number, "max_steps": max_steps},
                        ),
                    )

                    if step.step_number == 1 and intent_decision is not None:
                        yield _sse(
                            "chain",
                            _event(
                                typ="agent.intent",
                                started_at=started_at,
                                step_id="intent_1",
                                payload={
                                    "tool": intent_decision.tool,
                                    "mode": intent_decision.mode,
                                    "reasoning": intent_decision.reasoning,
                                    "confidence": intent_decision.confidence,
                                    "fallback": intent_decision.fallback,
                                },
                            ),
                        )

                    yield _sse(
                        "chain",
                        _event(
                            typ="agent.think",
                            started_at=started_at,
                            step_id=f"{step_id}_think",
                            payload={
                                "step_number": step.step_number,
                                "thought": step.think_payload["thought"],
                                "selected_tool": step.think_payload["selected_tool"],
                                "mode": step.think_payload["mode"],
                                "confidence": step.think_payload["confidence"],
                            },
                        ),
                    )

                    yield _sse(
                        "chain",
                        _event(
                            typ="tool.call.start",
                            started_at=started_at,
                            step_id=f"t_step{step.step_number}",
                            payload={"tool": step.tool_used, "input": {"query": query}},
                        ),
                    )

                    err = step.tool_result.error
                    out_answer: str | None = None
                    if step.tool_result.data and isinstance(step.tool_result.data.get("answer"), str):
                        out_answer = step.tool_result.data.get("answer")

                    yield _sse(
                        "chain",
                        _event(
                            typ="tool.call.end",
                            started_at=started_at,
                            step_id=f"t_step{step.step_number}",
                            payload={
                                "output": {"answer": out_answer},
                                "error": err,
                                "latency_ms": step.tool_result.latency_ms,
                            },
                        ),
                    )

                    if step.tool_used == "text2sql_query" and step.tool_result.success and step.tool_result.data:
                        data = step.tool_result.data
                        columns_any = data.get("columns")
                        columns = columns_any if isinstance(columns_any, list) else []
                        rows_any = data.get("rows")
                        rows_any2 = rows_any if isinstance(rows_any, list) else []
                        rows: list[dict[str, Any]] = [r for r in rows_any2 if isinstance(r, dict)]
                        truncated = len(rows) > 20
                        yield _sse(
                            "chain",
                            _event(
                                typ="sql.result",
                                started_at=started_at,
                                step_id=f"q_step{step.step_number}",
                                payload={
                                    "sql": data.get("sql") if isinstance(data.get("sql"), str) else "",
                                    "columns": [c for c in columns if isinstance(c, str)],
                                    "rows": rows[:20],
                                    "truncated": truncated,
                                },
                            ),
                        )
                    elif step.tool_used == "rag_search" and step.tool_result.success and step.tool_result.data:
                        data = step.tool_result.data
                        hits_any = data.get("hits")
                        hits: list[dict[str, Any]] = hits_any if isinstance(hits_any, list) else []
                        yield _sse(
                            "chain",
                            _event(
                                typ="rag.sources",
                                started_at=started_at,
                                step_id=f"s_step{step.step_number}",
                                payload=_build_rag_sources_event(hits, top_k=10),
                            ),
                        )

                    yield _sse(
                        "chain",
                        _event(
                            typ="agent.step.end",
                            started_at=started_at,
                            step_id=f"{step_id}_end",
                            payload={
                                "step_number": step.step_number,
                                "tool_used": step.tool_used,
                                "mode": step.mode,
                                "success": step.success,
                                "next_action": step.next_action,
                            },
                        ),
                    )

                yield _sse(
                    "chain",
                    _event(
                        typ="agent.final",
                        started_at=started_at,
                        step_id="a_final",
                        payload={
                            "total_steps": agent_result.final.total_steps,
                            "tools_used": agent_result.final.tools_used,
                            "modes": agent_result.final.modes,
                            "fallback_used": agent_result.final.fallback_used,
                        },
                    ),
                )

                yield _sse(
                    "chain",
                    _event(
                        typ="assistant.message",
                        started_at=started_at,
                        step_id="s_answer",
                        payload={"role": "assistant", "content": agent_result.final.answer},
                    ),
                )

                yield _sse(
                    "chain",
                    _event(
                        typ="latency",
                        started_at=started_at,
                        step_id="l1",
                        payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                    ),
                )
            except GeneratorExit:
                return
            except Exception:  # noqa: BLE001
                ok = False
                yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_unhandled", payload={"stage": "agent", "message": "SSE V2 运行异常"}))
            finally:
                yield _sse(
                    "done",
                    {
                        "ok": ok,
                        "mode": mode,
                        "run_id": run_id,
                        "request_id": run_id,
                        "session_id": session_id,
                    },
                )

        headers = {"Cache-Control": "no-cache"}
        return StreamingResponse(event_stream(), media_type="text/event-stream; charset=utf-8", headers=headers)

    decision = decide_intent(query=query, prefer=prefer)
    mode = decision.final_mode

    async def event_stream():
        ok = True
        try:
            # 首包：让前端先拿到 run_id/mode
            yield _sse("chain", {"type": "meta", "ts": _now_ms(started_at), "step_id": "m1", "payload": {"run_id": run_id, "mode": mode, "session_id": session_id}})
            yield _sse(
                "chain",
                _event(
                    typ="router.decision",
                    started_at=started_at,
                    step_id="r1",
                    payload={
                        "prefer": decision.prefer,
                        "candidate_mode": decision.candidate_mode,
                        "final_mode": decision.final_mode,
                        "rule_hits": decision.rule_hits,
                        "evidence": decision.evidence,
                        "fallback": decision.fallback,
                    },
                ),
            )

            if mode.startswith("tool:"):
                ok = False
                yield _sse(
                    "chain",
                    _event(
                        typ="error",
                        started_at=started_at,
                        step_id="e_tool",
                        payload={"stage": "router", "message": f"未实现的工具路由：{mode}"},
                    ),
                )
                yield _sse(
                    "chain",
                    _event(
                        typ="latency",
                        started_at=started_at,
                        step_id="l1",
                        payload={"total_ms": _now_ms(started_at), "stages_ms": {}},
                    ),
                )
                return

            if mode == "no_data":
                oai = openai_siliconflow_client()
                chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")
                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.start",
                        started_at=started_at,
                        step_id="t_generate",
                        payload={"tool": "no_data.generate", "input": {"query": query}},
                    ),
                )
                t0 = time.perf_counter()
                ans = ""
                gen_err: str | None = None
                try:
                    res = oai.chat.completions.create(
                        model=chat_model,
                        messages=[
                            {"role": "system", "content": "你是一个中文助手。用户的问题不需要检索或查库，请直接回答。"},
                            {"role": "user", "content": query},
                        ],
                        temperature=0.7,
                        stream=False,
                    )
                    ans = (res.choices[0].message.content or "").strip()
                except Exception as exc:  # noqa: BLE001
                    gen_err = str(exc)
                    ans = "对话生成失败。"
                    ok = False
                t_gen_ms = int((time.perf_counter() - t0) * 1000)
                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.end",
                        started_at=started_at,
                        step_id="t_generate",
                        payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms},
                    ),
                )
                if gen_err:
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_generate", payload={"stage": "no_data.generate", "message": gen_err}))
                yield _sse("chain", _event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": ans}))
                yield _sse("chain", _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"generate": t_gen_ms}}))
                return

            if mode == "text2sql":
                # retrieve
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_retrieve", payload={"tool": "text2sql.retrieve", "input": {"query": query}}))
                t0 = time.perf_counter()
                retrieve_err: str | None = None
                retrieved: list[dict[str, Any]] = []
                try:
                    store = get_text2sql_store()
                    topk = int(os.getenv("TEXT2SQL_RETRIEVE_TOPK", "6"))
                    retrieved = store.search(query, top_k=topk)
                except Exception as exc:  # noqa: BLE001
                    retrieve_err = str(exc)
                t_retrieve_ms = int((time.perf_counter() - t0) * 1000)
                yield _sse(
                    "chain",
                    _event(
                        typ="tool.call.end",
                        started_at=started_at,
                        step_id="t_retrieve",
                        payload={"output": {"retrieved_count": len(retrieved), "retrieved": retrieved[:6]}, "error": retrieve_err, "latency_ms": t_retrieve_ms},
                    ),
                )
                if retrieve_err:
                    ok = False
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_retrieve", payload={"stage": "text2sql.retrieve", "message": retrieve_err}))
                    return

                oai = OpenAI(api_key=os.getenv("SILICONFLOW_API_KEY", "").strip(), base_url=siliconflow_base())
                chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

                # generate sql
                sql_prompt = build_sql_prompt(query, retrieved)
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_generate_sql", payload={"tool": "text2sql.generate_sql", "input": {"query": query}}))
                t1 = time.perf_counter()
                sql_raw = ""
                sql = ""
                gen_err: str | None = None
                try:
                    sql_raw = llm_generate_sql(oai=oai, model=chat_model, prompt=sql_prompt)
                    sql = validate_sql_readonly(sql_raw)
                except Exception as exc:  # noqa: BLE001
                    gen_err = str(exc)
                t_gen_ms = int((time.perf_counter() - t1) * 1000)
                yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_generate_sql", payload={"output": {"sql": sql or sql_raw}, "error": gen_err, "latency_ms": t_gen_ms}))
                if gen_err or not (sql or sql_raw):
                    ok = False
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_generate_sql", payload={"stage": "text2sql.generate_sql", "message": gen_err or "empty sql"}))
                    return

                # execute sql
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_execute_sql", payload={"tool": "text2sql.execute_sql", "input": {"sql": sql}}))
                t2 = time.perf_counter()
                columns: list[str] = []
                rows: list[dict[str, Any]] = []
                exec_err: str | None = None
                try:
                    columns, rows = execute_select_sql(sql, limit_rows=int(os.getenv("TEXT2SQL_MAX_ROWS", "200")))
                except Exception as exc:  # noqa: BLE001
                    exec_err = str(exc)
                t_exec_ms = int((time.perf_counter() - t2) * 1000)
                yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_execute_sql", payload={"output": {"columns": columns, "rows_len": len(rows)}, "error": exec_err, "latency_ms": t_exec_ms}))
                if exec_err:
                    ok = False
                    yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_execute_sql", payload={"stage": "text2sql.execute_sql", "message": exec_err}))
                yield _sse("chain", _event(typ="sql.result", started_at=started_at, step_id="q1", payload={"sql": sql, "columns": columns, "rows": rows[:20], "truncated": len(rows) > 20}))

                # summarize
                yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_summarize", payload={"tool": "text2sql.summarize", "input": {"query": query}}))
                t3 = time.perf_counter()
                answer = ""
                sum_err: str | None = None
                try:
                    if rows:
                        sum_prompt = build_summary_prompt(query, sql, columns, rows)
                        answer = llm_summarize(oai=oai, model=chat_model, prompt=sum_prompt)
                    else:
                        answer = "未查到数据。"
                except Exception as exc:  # noqa: BLE001
                    sum_err = str(exc)
                    answer = "未查到数据。" if not rows else f"查询返回 {len(rows)} 行结果。"
                    ok = False
                t_sum_ms = int((time.perf_counter() - t3) * 1000)
                yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_summarize", payload={"output": {"answer": answer}, "error": sum_err, "latency_ms": t_sum_ms}))
                yield _sse("chain", _event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": answer}))
                yield _sse("chain", _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"retrieve": t_retrieve_ms, "generate_sql": t_gen_ms, "execute_sql": t_exec_ms, "summarize": t_sum_ms}}))
                return

            # ---- RAG branch (non-streaming answer v1) ----
            oai = openai_siliconflow_client()
            chat_model = os.getenv("SILICONFLOW_CHAT_MODEL", "deepseek-ai/DeepSeek-V3")

            # rewrite
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_rewrite", payload={"tool": "rag.rewrite", "input": {"query": query}}))
            t_rw0 = time.perf_counter()
            rewritten = query
            rw_err: str | None = None
            try:
                rewritten = await rewrite_query_with_history(oai=oai, query=query, history=[], chat_model=chat_model)
            except Exception as exc:  # noqa: BLE001
                rw_err = str(exc)
                rewritten = query
                ok = False
            t_rw_ms = int((time.perf_counter() - t_rw0) * 1000)
            yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_rewrite", payload={"output": {"rewritten_query": rewritten}, "error": rw_err, "latency_ms": t_rw_ms}))

            # embed
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_embed", payload={"tool": "rag.embed", "input": {"query": rewritten}}))
            t_emb0 = time.perf_counter()
            vec: list[float] | None = None
            emb_err: str | None = None
            try:
                emb_res = oai.embeddings.create(**embedding_kwargs_for_inputs([rewritten]))
                vec = list(emb_res.data[0].embedding)
            except Exception as exc:  # noqa: BLE001
                emb_err = str(exc)
                vec = None
                ok = False
            t_emb_ms = int((time.perf_counter() - t_emb0) * 1000)
            yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_embed", payload={"output": {"vec_available": vec is not None}, "error": emb_err, "latency_ms": t_emb_ms}))

            # retrieve
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_retrieve", payload={"tool": "rag.retrieve", "input": {"query": rewritten}}))
            t_ret0 = time.perf_counter()
            vector_hits: list[dict[str, Any]] = []
            structured_hits: list[dict[str, Any]] = []
            keyword_hits_raw: list[dict[str, Any]] = []
            keyword_hits_rewrite: list[dict[str, Any]] = []
            hits: list[dict[str, Any]] = []
            ret_err: str | None = None
            retry_count = 0
            try:
                sb = supabase_client()
                structured_hits = structured_recall_by_date(sb, query=query, rewritten=rewritten, limit_rows=6).hits
                match_threshold = parse_match_threshold()
                match_count = int(os.getenv("RAG_MATCH_COUNT", "10"))
                if vec is not None:
                    vector_hits, rc_vec, err_vec = rpc_execute_with_retry(
                        sb,
                        "match_documents",
                        {"query_embedding": vec, "match_count": match_count, "match_threshold": match_threshold},
                        retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
                    )
                    retry_count += rc_vec
                    if err_vec:
                        ret_err = err_vec

                kw_qt_raw, kw_meta_raw = keyword_query_text_with_i18n_meta(query)
                kw_qt_rw, kw_meta_rw = keyword_query_text_with_i18n_meta(rewritten)
                yield _sse(
                    "chain",
                    _event(
                        typ="rag.query_expand",
                        started_at=started_at,
                        step_id="q_expand",
                        payload={
                            "raw": _build_query_expand_event_payload(kw_meta_raw, max_raw=160, max_expanded=220),
                            "rewrite": _build_query_expand_event_payload(kw_meta_rw, max_raw=160, max_expanded=220),
                        },
                    ),
                )

                keyword_hits_raw, rc_raw, err_raw = rpc_execute_with_retry(
                    sb,
                    "keyword_documents",
                    {"query_text": kw_qt_raw, "match_count": 12},
                    retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
                )
                retry_count += rc_raw
                if err_raw:
                    ret_err = err_raw

                keyword_hits_rewrite, rc_rw, err_rw = rpc_execute_with_retry(
                    sb,
                    "keyword_documents",
                    {"query_text": kw_qt_rw, "match_count": 12},
                    retries=int(os.getenv("RAG_RPC_RETRIES", "2")),
                )
                retry_count += rc_rw
                if err_rw:
                    ret_err = err_rw

                merged_keyword = fuse_hits_rrf(keyword_hits_raw, keyword_hits_rewrite, max_total=22)
                merged_kw2 = fuse_hits_rrf(structured_hits, merged_keyword, max_total=22)
                hits = fuse_hits_rrf(vector_hits, merged_kw2, max_total=22)
            except Exception as exc:  # noqa: BLE001
                ret_err = str(exc)
                hits = []
                ok = False
            t_ret_ms = int((time.perf_counter() - t_ret0) * 1000)
            yield _sse(
                "chain",
                _event(
                    typ="tool.call.end",
                    started_at=started_at,
                    step_id="t_retrieve",
                    payload={
                        "output": {
                            "vector_hits": len(vector_hits),
                            "structured_hits": len(structured_hits),
                            "keyword_hits_raw": len(keyword_hits_raw),
                            "keyword_hits_rewrite": len(keyword_hits_rewrite),
                            "hits": len(hits),
                            "retry_count": retry_count,
                            "embedding_error": emb_err,
                        },
                        "error": ret_err,
                        "latency_ms": t_ret_ms,
                    },
                ),
            )

            # sources
            yield _sse("chain", _event(typ="rag.sources", started_at=started_at, step_id="s_sources", payload=_build_rag_sources_event(hits, top_k=10)))

            # generate
            yield _sse("chain", _event(typ="tool.call.start", started_at=started_at, step_id="t_generate", payload={"tool": "rag.generate", "input": {"query": query}}))
            t_gen0 = time.perf_counter()
            ans = ""
            gen_err: str | None = None
            try:
                ans = _rag_generate_answer(oai=oai, chat_model=chat_model, query=query, hits=hits)
                if not ans:
                    ans = "我暂时无法根据现有资料给出确定回答。"
            except Exception as exc:  # noqa: BLE001
                gen_err = str(exc)
                ans = "对话生成失败。"
                ok = False
            t_gen_ms = int((time.perf_counter() - t_gen0) * 1000)
            yield _sse("chain", _event(typ="tool.call.end", started_at=started_at, step_id="t_generate", payload={"output": {"answer": ans}, "error": gen_err, "latency_ms": t_gen_ms}))
            if gen_err:
                yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_generate", payload={"stage": "rag.generate", "message": gen_err}))
            yield _sse("chain", _event(typ="assistant.message", started_at=started_at, step_id="s_answer", payload={"role": "assistant", "content": ans}))
            yield _sse("chain", _event(typ="latency", started_at=started_at, step_id="l1", payload={"total_ms": _now_ms(started_at), "stages_ms": {"rewrite": t_rw_ms, "embed": t_emb_ms, "retrieve": t_ret_ms, "generate": t_gen_ms}}))
        except GeneratorExit:
            return
        except Exception as exc:  # noqa: BLE001
            ok = False
            yield _sse("chain", _event(typ="error", started_at=started_at, step_id="e_unhandled", payload={"stage": "unhandled", "message": str(exc)}))
        finally:
            # done must be the last message if client still connected
            try:
                # request_id：端到端链路标识（当前与 run_id 等价，便于逐步在前后端统一命名）
                yield _sse(
                    "done",
                    {
                        "ok": ok,
                        "mode": mode,
                        "run_id": run_id,
                        "request_id": run_id,
                        "session_id": session_id,
                    },
                )
            except Exception:
                return

    headers = {"Cache-Control": "no-cache"}
    return StreamingResponse(event_stream(), media_type="text/event-stream; charset=utf-8", headers=headers)

