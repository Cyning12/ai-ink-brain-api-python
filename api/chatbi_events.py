from __future__ import annotations

import time
from collections.abc import Awaitable, Callable
from typing import Any

from .chatbi_agent_models import LlmPhase


def _agent_chain(typ: str, started_at: float, step_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    """与 unified_chat._event 同形，供 SSE chain 帧序列化。"""
    return {
        "type": typ,
        "ts": int((time.perf_counter() - started_at) * 1000),
        "step_id": step_id,
        "payload": payload,
    }


async def emit_simulated_llm(
    emit: Callable[[dict[str, Any]], Awaitable[None]],
    *,
    started_at: float,
    step_id: str,
    inner_step_id: str,
    phase: LlmPhase,
    text: str,
    simulated_stream: bool,
    chunk_size: int = 16,
    max_parts: int = 400,
) -> None:
    """伪流式：将整段文本切分为 agent.llm.delta 序列（上游非 stream 时）。"""
    await emit(
        _agent_chain(
            typ="agent.llm.start",
            started_at=started_at,
            step_id=step_id,
            payload={"phase": phase, "step_id": inner_step_id},
        )
    )
    body = text or ""
    part = 0
    for i in range(0, len(body), max(1, chunk_size)):
        if part >= max_parts:
            await emit(
                _agent_chain(
                    typ="agent.llm.truncated",
                    started_at=started_at,
                    step_id=step_id,
                    payload={"dropped_chars": max(0, len(body) - i), "reason": "emit_chunk_cap"},
                )
            )
            break
        chunk = body[i : i + chunk_size]
        await emit(
            _agent_chain(
                typ="agent.llm.delta",
                started_at=started_at,
                step_id=step_id,
                payload={"text": chunk, "part_index": part},
            )
        )
        part += 1
    await emit(
        _agent_chain(
            typ="agent.llm.end",
            started_at=started_at,
            step_id=step_id,
            payload={"ok": True, "phase": phase, "step_id": inner_step_id, "simulated_stream": simulated_stream},
        )
    )


# 对外别名（Graph / 测试）；契约扫描识别 `_agent_chain(`）
agent_chain = _agent_chain
