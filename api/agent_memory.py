from __future__ import annotations

import asyncio
import os
import time
from dataclasses import dataclass
from typing import Any

from .rag_env import supabase_client


def _memory_debug() -> bool:
    v = (os.getenv("DEBUG_RAG") or "").strip().lower()
    return v in ("1", "true", "yes", "on")


@dataclass(frozen=True)
class AgentMemorySavePayload:
    query: str
    response: str
    mode: str
    agent_steps: dict[str, Any]
    tool_results: dict[str, Any]


class AgentMemoryStore:
    """V2 会话记忆：仅负责加载历史与轻量缓存。

    P0 约束：持久化由 `unified_chat.py` 在一轮结束时统一写入（只写一次），本模块避免每步/每轮写 DB。
    """

    def __init__(self) -> None:
        self._cache: dict[str, list[dict[str, Any]]] = {}

    async def load(self, session_id: str | None) -> list[dict[str, Any]]:
        if not session_id or not isinstance(session_id, str):
            return []
        sid = session_id.strip()
        if not sid:
            return []

        if sid in self._cache:
            return self._cache[sid]

        def _sync_fetch() -> list[dict[str, Any]]:
            sb = supabase_client()
            res = (
                sb.table("rag_conversation_logs")
                .select("query, response, created_at, agent_steps, tool_results")
                .eq("session_id", sid)
                .order("created_at", desc=True)
                .limit(5)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return [r for r in rows if isinstance(r, dict)]

        try:
            rows_desc = await asyncio.to_thread(_sync_fetch)
        except Exception as exc:  # noqa: BLE001
            if _memory_debug():
                print(f"[agent-memory] load failed: {exc!s}", flush=True)
            history: list[dict[str, Any]] = []
            self._cache[sid] = history
            return history

        # 返回给工具侧的历史格式：{query, response}
        history: list[dict[str, Any]] = []
        for row in reversed(rows_desc):
            q = row.get("query") if isinstance(row.get("query"), str) else ""
            r = row.get("response") if isinstance(row.get("response"), str) else ""
            if not q.strip():
                continue
            history.append({"query": q.strip(), "response": r.strip()})

        self._cache[sid] = history
        return history

    async def save(self, session_id: str | None, payload: AgentMemorySavePayload) -> None:
        """只更新内存缓存，不写 DB。

        持久化由 unified_chat.py 统一完成，避免每步 insert。
        """
        if not session_id or not isinstance(session_id, str):
            return
        sid = session_id.strip()
        if not sid:
            return
        self._cache.setdefault(sid, [])
        self._cache[sid].append({"role": "user", "content": payload.query})
        self._cache[sid].append({"role": "assistant", "content": payload.response})


def get_memory_store() -> AgentMemoryStore:
    return AgentMemoryStore()

