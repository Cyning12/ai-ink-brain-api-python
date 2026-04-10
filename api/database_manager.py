from __future__ import annotations

import asyncio
from dataclasses import dataclass
from typing import Any

from supabase import create_client

from .rag_env import pick_supabase_service_key, pick_supabase_url


@dataclass(frozen=True)
class SupabaseManager:
    """Supabase 访问封装（以 service_role 写入调试日志）。"""

    url: str
    service_key: str

    @staticmethod
    def from_env() -> "SupabaseManager":
        url = pick_supabase_url()
        key = pick_supabase_service_key()
        if not url or not key:
            raise RuntimeError(
                "缺少 Supabase 配置：请设置 NEXT_PUBLIC_SUPABASE_URL 或 SUPABASE_URL，以及 "
                "SUPABASE_SERVICE_ROLE_KEY 或 SUPABASE_SERVICE_KEY。"
            )
        return SupabaseManager(url=url, service_key=key)

    def _client(self) -> Any:
        # supabase-py 当前为同步客户端；在 async 场景使用 asyncio.to_thread 包装调用
        return create_client(self.url, self.service_key)

    async def save_debug_log(self, data: dict[str, Any]) -> None:
        """异步写入 rag_conversation_logs（避免阻塞请求主流程）。"""

        def _sync_insert() -> None:
            sb = self._client()
            sb.table("rag_conversation_logs").insert(data).execute()

        await asyncio.to_thread(_sync_insert)

    async def get_chat_history(self, session_id: str, limit: int = 5) -> list[dict[str, Any]]:
        """获取该 session 最新问答对，按时间正序返回。"""

        sid = session_id.strip()
        if not sid:
            return []

        def _sync_fetch() -> list[dict[str, Any]]:
            sb = self._client()
            res = (
                sb.table("rag_conversation_logs")
                .select("query, response, created_at")
                .eq("session_id", sid)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            return [r for r in rows if isinstance(r, dict)]

        rows_desc = await asyncio.to_thread(_sync_fetch)
        return list(reversed(rows_desc))

