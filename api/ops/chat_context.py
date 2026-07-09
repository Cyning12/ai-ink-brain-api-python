"""Ops Chat 多轮对话上下文读取。

P0-3: 从已有 ops_runs + ops_run_events 读取最近 N 轮用户/助手消息，
供 deep / ReAct 路径注入 LLM 上下文。
"""

from __future__ import annotations

import logging

from api.ops.store.runs import OpsRunStore
from api.rag_env import supabase_client

logger = logging.getLogger(__name__)

DEFAULT_TRANSCRIPT_ROUNDS = 6


def load_chat_transcript(
    session_id: str | None,
    n: int = DEFAULT_TRANSCRIPT_ROUNDS,
    store: OpsRunStore | None = None,
) -> list[dict[str, str]]:
    """读取 session 最近 N 轮用户/助手消息。

    从 ops_runs 按 session_id 查询，并读取每个 run 的 final.answer 事件，
    构造用户/助手消息列表。最近的 N 轮放在列表末尾（ chronological 顺序）。

    参数:
        session_id: Chat session id；为 None 时返回空列表。
        n: 最大轮数（每轮 = user + assistant 两条消息）。
        store: 可选 OpsRunStore 实例；默认使用全局 supabase_client() 构造。

    返回:
        [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}, ...]
    """
    if not session_id:
        logger.debug("chat_context.no_session_id")
        return []

    target = store if store is not None else OpsRunStore(supabase_client())
    runs = target.list_runs_by_session_id(session_id, limit=50)
    if not runs:
        return []

    # DB 返回按 created_at desc（最新在前），反转为 chronological
    runs_chronological = list(reversed(runs))

    pairs: list[list[dict[str, str]]] = []
    for run in runs_chronological:
        query = run.get("query")
        if not query:
            continue

        events = target.get_events(str(run["id"]), limit=200)
        answer = ""
        for evt in events:
            if evt.get("event_type") == "final.answer":
                payload = evt.get("payload") or {}
                answer = str(payload.get("answer", ""))

        # 只保留完整的一问一答
        if not answer:
            continue

        pairs.append([
            {"role": "user", "content": str(query)},
            {"role": "assistant", "content": answer},
        ])

    # 取最近 N 轮
    recent_pairs = pairs[-n:] if len(pairs) > n else pairs
    messages: list[dict[str, str]] = []
    for pair in recent_pairs:
        messages.extend(pair)
    return messages
