from __future__ import annotations

import asyncio
from typing import Any

from openai import OpenAI

from .text2sql_grounding import grounding_line_for_history_block

# 与 rewrite_query_with_history 内原逻辑一致，便于单测与调试拉取完整 messages
REWRITE_SYSTEM_INSTRUCTION = (
    "你是检索查询改写器。给定一段对话历史和用户最新问题，"
    "请将“最新问题”改写为一条自包含、适合向量检索的查询。\n"
    "要求：\n"
    "- 只输出改写后的查询本身，不要解释；\n"
    "- 保持与用户原始问题一致的语言（中文就中文、英文就英文、混合就混合）；\n"
    "- 必须原样保留用户给出的英文关键词、专有名词、标识符（如函数名/类名/包名/文件名/版本号）；\n"
    "- 若问题是中英混合或疑似跨语言检索需求：可在不改变原关键词的前提下，追加括号内同义/翻译词作为补充检索词；\n"
    "- 保留用户提到的关键实体、时间/日期、约束条件；\n"
    "- 不要凭空添加事实。\n"
)


def history_to_rewrite_block(history: list[dict[str, Any]]) -> str:
    lines: list[str] = []
    for h in history:
        q = h.get("query") if isinstance(h.get("query"), str) else ""
        a = h.get("response") if isinstance(h.get("response"), str) else ""
        if not q:
            continue
        gx = grounding_line_for_history_block(h.get("text2sql_grounding") if isinstance(h.get("text2sql_grounding"), dict) else None)
        if a:
            block = f"Q: {q}\nA: {a}"
        else:
            block = f"Q: {q}"
        if gx:
            block = f"{block}\n{gx}"
        lines.append(block)
    return "\n\n".join(lines).strip()


def build_rewrite_llm_messages(*, history: list[dict[str, Any]], query: str) -> list[dict[str, str]] | None:
    """构造检索改写 LLM 的 messages；无历史可改写时返回 None（调用方应跳过改写 LLM）。"""
    history_block = history_to_rewrite_block(history)
    if not history_block:
        return None
    user = f"【对话历史】\n{history_block}\n\n【最新问题】\n{query}".strip()
    return [
        {"role": "system", "content": REWRITE_SYSTEM_INSTRUCTION},
        {"role": "user", "content": user},
    ]


async def rewrite_query_with_history(
    *,
    oai: OpenAI,
    query: str,
    history: list[dict[str, Any]],
    chat_model: str,
) -> str:
    """将用户问题改写为可独立检索的查询（注入 session 历史）。"""
    messages = build_rewrite_llm_messages(history=history, query=query)
    if messages is None:
        return query

    def _sync_rewrite() -> str:
        res = oai.chat.completions.create(
            model=chat_model,
            messages=messages,
            temperature=0.0,
            stream=False,
        )
        try:
            content = (res.choices[0].message.content or "").strip()
        except Exception:  # noqa: BLE001
            content = ""
        return content or query

    return await asyncio.to_thread(_sync_rewrite)
