"""Intent V2 公开模型与 hints 仲裁；LLM 路径见 `intent_llm`。"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Literal

from .intent_hints import (
    arbitration_enabled,
    hints_arbitration_should_apply,
    load_resolved_hints,
)
from .intent_router import decide_intent as decide_intent_v1
from .rag_env import openai_siliconflow_client

ToolName = Literal["rag_search", "text2sql_query", "direct_answer"]
V1Mode = Literal["rag", "text2sql", "no_data"]


@dataclass(frozen=True)
class StructuredSignals:
    """用于 gating 的结构化信号（关键约束：RAG_RETRIEVE_EMPTY 的 SQL fallback 必须依赖这些信号）。"""

    llm_prefers_sql: bool
    has_aggregation_signals: bool


@dataclass(frozen=True)
class IntentDecision:
    tool: ToolName
    mode: V1Mode
    reasoning: str  # 用户级 1-2 句话摘要
    reasoning_full: str  # 内部级，用于日志/调试
    confidence: float
    fallback: ToolName | None
    structured_signals: StructuredSignals
    raw_response: dict[str, Any]


def build_intent_path_obs(raw: dict[str, Any] | None) -> dict[str, Any]:
    """Intent 决策路径可观测字段（Timeline / agent.intent；不含 prompt 正文）。"""
    rr = raw if isinstance(raw, dict) else {}
    used = rr.get("used")
    intent_path: str | None = None
    if isinstance(used, str) and used.strip():
        intent_path = used.strip()
    elif "tool" in rr and "confidence" in rr:
        intent_path = "llm"
    attempt_raw = rr.get("attempt")
    intent_attempt: int | None = None
    if isinstance(attempt_raw, (int, float)) and int(attempt_raw) >= 1:
        intent_attempt = int(attempt_raw)
    hints_arbitration: dict[str, Any] | None = None
    arb = rr.get("hints_arbitration")
    if isinstance(arb, dict) and arb.get("applied") is True:
        hints_arbitration = {
            "applied": True,
            "reason": str(arb.get("reason") or "").strip(),
        }
    return {
        "intent_path": intent_path,
        "intent_attempt": intent_attempt,
        "hints_arbitration": hints_arbitration,
    }


def apply_hints_arbitration(
    decision: IntentDecision,
    *,
    query: str,
    hints: dict[str, Any] | None = None,
) -> IntentDecision:
    """Step2：配置命中 + LLM direct → 强制 rag_search。"""
    if decision.tool != "direct_answer":
        return decision
    h = hints if hints is not None else load_resolved_hints()
    if not arbitration_enabled(h):
        return decision
    should, reason = hints_arbitration_should_apply(query, h or {})
    if not should:
        return decision
    raw = dict(decision.raw_response)
    raw["hints_arbitration"] = {"applied": True, "reason": reason}
    full = decision.reasoning_full
    if reason and reason not in full:
        full = f"{full}（{reason}）".strip()
    return replace(
        decision,
        tool="rag_search",
        mode="rag",
        reasoning=full[:260],
        reasoning_full=full,
        fallback=None,
        raw_response=raw,
    )


from . import intent_llm as _intent_llm_mod  # noqa: E402

LRUCache = _intent_llm_mod.LRUCache
_intent_cache = _intent_llm_mod._intent_cache
_llm_decide_v2 = _intent_llm_mod._llm_decide_v2
_intent_llm_retryable = _intent_llm_mod._intent_llm_retryable
_intent_composite_cache_key = _intent_llm_mod._intent_composite_cache_key
clear_intent_cache = _intent_llm_mod.clear_intent_cache
compute_history_hash = _intent_llm_mod.compute_history_hash
decide_intent_v2 = _intent_llm_mod.decide_intent_v2

__all__ = [
    "IntentDecision",
    "LRUCache",
    "StructuredSignals",
    "ToolName",
    "V1Mode",
    "apply_hints_arbitration",
    "build_intent_path_obs",
    "clear_intent_cache",
    "compute_history_hash",
    "decide_intent_v1",
    "decide_intent_v2",
    "openai_siliconflow_client",
]
