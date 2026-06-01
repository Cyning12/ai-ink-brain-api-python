#!/usr/bin/env python3
"""导出 §5-3 RAG 低置信 diary Timeline JSON（TestClient + stub，与 pytest 同形）。

用法（仓根）：
  python scripts/export_lowconf_rag_diary_sample.py

落盘：docs/diary/samples/chatbi-v3-lowconf-rag-preview/round{1,2}_*.json
"""
from __future__ import annotations

import importlib
import json
import os
import uuid
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = REPO_ROOT / "docs/diary/samples/chatbi-v3-lowconf-rag-preview"

QUERY = "2026年4月日记里关于项目进展有哪些记录"
SESSION = "211d54b7-f806-4265-b46e-fc1a897f51e2"


def _env() -> None:
    os.environ.setdefault("NEXT_PUBLIC_ADMIN_SECRET", "secret-token-1234567890")
    os.environ.setdefault("API_KEY", "api-key-123")
    os.environ.setdefault("SILICONFLOW_API_KEY", "sf-dummy-key")
    os.environ.setdefault("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    os.environ.setdefault("TEXT2SQL_DATABASE_URL", "postgresql://u:p@localhost:5432/postgres")
    os.environ["CHATBI_USE_AGENT"] = "true"
    os.environ["CHATBI_V2_INTENT_LLM"] = "false"
    os.environ["CHATBI_V3_LOW_CONFIDENCE_CLARIFY"] = "1"
    os.environ["CHATBI_V3_PLAN_PREVIEW_CONFIRM"] = "1"


def main() -> int:
    _env()
    from fastapi.testclient import TestClient

    from api.intent_agent import IntentDecision, StructuredSignals
    from api.tools import Tool, ToolResult

    import api.tools as tools_mod
    import api.unified_chat as unified_chat
    import api.agent as agent_module
    import api.index as index

    importlib.reload(unified_chat)
    importlib.reload(index)

    from tests._chatbi_auth_overrides import install_unified_chat_auth_override

    install_unified_chat_auth_override(index.app)

    async def _rag_full(
        query: str,
        *,
        history: list[dict[str, Any]] | None = None,
        debug_llm_prompts: bool = False,
        preview_only: bool = False,
    ) -> ToolResult:
        if preview_only:
            return ToolResult(
                success=True,
                data={
                    "rewritten": "2026年4月 项目进展 日记 检索",
                    "planned_top_k": 10,
                    "preview_headlines": ["2026-04-diary.md", "project-notes.md"],
                },
                latency_ms=1,
            )
        return ToolResult(
            success=True,
            data={
                "answer": "根据日记，4月项目进展包括…",
                "hits": [
                    {"id": "h1", "content": "4月项目里程碑…", "filename": "2026-04-diary.md", "score": 0.9},
                ],
            },
            latency_ms=2,
        )

    async def _t2s_ok(*_a: Any, **_k: Any) -> ToolResult:
        return ToolResult(success=True, data={"sql": "SELECT 1", "answer": ""}, latency_ms=1)

    async def _direct_ok(*, query: str, history: list[dict[str, Any]] | None = None, debug_llm_prompts: bool = False) -> ToolResult:
        _ = (query, history, debug_llm_prompts)
        return ToolResult(success=True, data={"answer": "d"}, latency_ms=1)

    def _make_tool(name: str, execute: Any) -> Tool:
        async def _exec(query: str, *, history: list[dict[str, Any]] | None = None, debug_llm_prompts: bool = False, **__: Any) -> ToolResult:
            return await execute(query=query, history=history, debug_llm_prompts=debug_llm_prompts)

        return Tool(name=name, description=f"dummy-{name}", parameters={}, execute=_exec)  # type: ignore[arg-type]

    async def _fake_rag_lowconf(
        *,
        query: str,
        history: list[dict[str, Any]],
        tools: list[Tool],
        min_confidence: float,
        timeout: float,
        **kwargs: Any,
    ) -> IntentDecision:
        _ = (query, history, tools, min_confidence, timeout, kwargs)
        return IntentDecision(
            tool="rag_search",
            mode="rag",
            reasoning="日记类问句，倾向文档检索",
            reasoning_full="日记类问句，倾向文档检索",
            confidence=0.35,
            fallback="direct_answer",
            structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=False),
            raw_response={"used": "diary_sample_export"},
        )

    class _Registry:
        def list_tools(self) -> list[Tool]:
            return [
                _make_tool("direct_answer", _direct_ok),
                _make_tool("rag_search", _rag_full),
                _make_tool("text2sql_query", _t2s_ok),
            ]

    tools_mod.rag_search_execute = _rag_full
    tools_mod.text2sql_execute = _t2s_ok
    agent_module.decide_intent_v2 = _fake_rag_lowconf
    unified_chat.get_tool_registry = lambda: _Registry()

    client = TestClient(index.app)
    headers = {"Authorization": "Bearer api-key-123"}
    body_base = {"query": QUERY, "prefer": "auto", "session_id": SESSION}

    r1 = client.post("/api/py/unified/chat", headers=headers, json=body_base)
    r1.raise_for_status()
    data1 = r1.json()
    run1 = data1.get("run_id") or str(uuid.uuid4())
    tok = next(e for e in data1["events"] if e.get("type") == "agent.plan.preview")["payload"]["plan_execution_token"]

    r2 = client.post(
        "/api/py/unified/chat",
        headers=headers,
        json={**body_base, "plan_execution_token": tok},
    )
    r2.raise_for_status()
    data2 = r2.json()
    run2 = data2.get("run_id") or str(uuid.uuid4())

    def _wrap(sample_id: str, events: list[dict[str, Any]], *, run_id: str, notes: str) -> dict[str, Any]:
        timeline = [{**e, "run_id": e.get("run_id") or run_id} for e in events]
        return {
            "meta": {
                "sample_id": sample_id,
                "captured_at": "2026-05-31",
                "run_id": run_id,
                "event_count": len(timeline),
                "query": QUERY,
                "session_id": SESSION,
                "source": "scripts/export_lowconf_rag_diary_sample.py",
                "notes": notes,
            },
            "timeline": timeline,
        }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p1 = OUT_DIR / "round1_preview_clarify_timeline.json"
    p2 = OUT_DIR / "round2_token_bypass_execute_timeline.json"
    p1.write_text(
        json.dumps(
            _wrap(
                "chatbi-v3-lowconf-rag-preview-round1",
                data1["events"],
                run_id=run1,
                notes="首轮：RAG agent.plan.preview + agent.clarify；无 rag.sources",
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    p2.write_text(
        json.dumps(
            _wrap(
                "chatbi-v3-lowconf-rag-preview-round2",
                data2["events"],
                run_id=run2,
                notes="第二轮：token 放行；含 rag.sources",
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"OK: {p1.name} ({len(data1['events'])} events)")
    print(f"OK: {p2.name} ({len(data2['events'])} events)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
