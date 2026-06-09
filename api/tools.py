from __future__ import annotations

import asyncio
import time
from typing import Any

from .rag_env import openai_siliconflow_client
from .tool_models import Tool, ToolName, ToolRegistry, ToolResult
from .tools_rag import rag_search_execute
from .tools_shared import _elapsed_ms, _pick_chat_model
from .tools_text2sql import text2sql_execute


async def direct_answer_execute(
    query: str,
    *,
    history: list[dict[str, Any]] | None = None,
    debug_llm_prompts: bool = False,
) -> ToolResult:
    started_at = time.perf_counter()
    _ = history
    try:
        oai = openai_siliconflow_client()
        chat_model = _pick_chat_model()

        system = "你是一个中文助手。请直接回答用户问题。"
        user = query
        msgs = [{"role": "system", "content": system}, {"role": "user", "content": user}]

        def _sync_generate() -> str:
            res = oai.chat.completions.create(
                model=chat_model,
                messages=msgs,
                temperature=0.7,
                stream=False,
            )
            return (res.choices[0].message.content or "").strip()

        answer = await asyncio.to_thread(_sync_generate)
        if not answer:
            return ToolResult(
                success=False,
                data=None,
                error="direct answer 为空",
                error_code="UNKNOWN",
                error_stage="direct_answer.generate",
                latency_ms=_elapsed_ms(started_at),
            )
        out: dict[str, Any] = {"answer": answer}
        if debug_llm_prompts:
            out["llm_prompts"] = [{"phase": "direct_answer", "model": chat_model, "messages": msgs}]
        return ToolResult(success=True, data=out, latency_ms=_elapsed_ms(started_at))
    except asyncio.TimeoutError:
        return ToolResult(
            success=False,
            data=None,
            error="DirectAnswer 超时",
            error_code="LLM_API_TIMEOUT",
            error_stage="llm.call",
            latency_ms=_elapsed_ms(started_at),
        )
    except Exception as exc:  # noqa: BLE001
        return ToolResult(
            success=False,
            data=None,
            error=str(exc),
            error_code="UNKNOWN",
            error_stage="direct_answer.tool",
            latency_ms=_elapsed_ms(started_at),
        )


def get_tool_registry() -> ToolRegistry:
    # 懒加载注册：避免导入即执行重载（对单测更友好）
    registry = ToolRegistry()
    registry.register(
        Tool(
            name="rag_search",
            description=(
                "从文档库中检索信息，适合概念解释与非结构化内容问题；"
                "Portfolio 模式下含 methodology/resume/evidence 站点文稿与个人履历。"
            ),
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "用户问题"}},
                "required": ["query"],
            },
            execute=rag_search_execute,
        )
    )
    registry.register(
        Tool(
            name="text2sql_query",
            description=(
                "执行数据库查询，获取结构化数据结果。适合以下场景：\n"
                "- 用户要求查数据、统计数据、计算金额（如'有多少条'、'总和多少'、'排名第几'）\n"
                "- 用户问具体数值（如'昨天销售额是多少'）\n"
                "- 需要时间趋势、分组汇总、排序排名\n"
                "不适合：解释 SQL 语法、教用户怎么写 SQL、概念解释"
            ),
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "自然语言查询"}},
                "required": ["query"],
            },
            execute=text2sql_execute,
        )
    )
    registry.register(
        Tool(
            name="direct_answer",
            description="无需检索或查库，直接用 LLM 生成回答。",
            parameters={
                "type": "object",
                "properties": {"query": {"type": "string", "description": "用户问题"}},
                "required": ["query"],
            },
            execute=direct_answer_execute,
        )
    )
    return registry


def tool_mode_map() -> dict[ToolName, str]:
    return {"rag_search": "rag", "text2sql_query": "text2sql", "direct_answer": "no_data"}

