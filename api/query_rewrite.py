from __future__ import annotations

import asyncio
from typing import Any

from openai import OpenAI


def history_to_rewrite_block(history: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for h in history:
        q = h.get("query") if isinstance(h.get("query"), str) else ""
        a = h.get("response") if isinstance(h.get("response"), str) else ""
        if not q:
            continue
        if a:
            lines.append(f"Q: {q}\nA: {a}")
        else:
            lines.append(f"Q: {q}")
    return "\n\n".join(lines).strip()


async def rewrite_query_with_history(
    *,
    oai: OpenAI,
    query: str,
    history: list[dict[str, Any]],
    chat_model: str,
) -> str:
    """将用户问题改写为可独立检索的查询（注入 session 历史）。"""
    history_block = history_to_rewrite_block(history)
    if not history_block:
        return query

    def _sync_rewrite() -> str:
        prompt = (
            "你是检索查询改写器。给定一段对话历史和用户最新问题，"
            "请将“最新问题”改写为一条自包含、适合向量检索的中文查询。\n"
            "要求：\n"
            "- 只输出改写后的查询本身，不要解释；\n"
            "- 保留用户提到的关键实体、时间/日期、约束条件；\n"
            "- 不要凭空添加事实。\n"
        )
        user = f"【对话历史】\n{history_block}\n\n【最新问题】\n{query}".strip()
        res = oai.chat.completions.create(
            model=chat_model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": user},
            ],
            temperature=0.0,
            stream=False,
        )
        try:
            content = (res.choices[0].message.content or "").strip()
        except Exception:  # noqa: BLE001
            content = ""
        return content or query

    return await asyncio.to_thread(_sync_rewrite)

