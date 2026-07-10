"""Ops Chat LLM intent router（P1-4）。

基于轻量 LLM JSON 输出的混合意图分类器：
- 环境变量 `OPS_CHAT_LLM_ROUTER=1` 时优先调用 LLM router。
- LLM 输出必须含 `intent`、`slots`、`confidence`（0~1）。
- 低置信度或非法 JSON / LLM 异常时降级为规则分类器，并记录
  `intent_router.fallback` 事件到 `ops_run_events`。
- 默认未开启时行为与原有规则分类器完全一致。
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from collections.abc import Callable
from typing import Any

from api.ops.llm import chat_completion

logger = logging.getLogger(__name__)

# 与 api.ops.orchestrator.core.Intent 保持一致（避免循环导入）
_ALLOWED_INTENTS = {
    "metrics_trend",
    "issue_list",
    "pr_list",
    "issue_contribution",
    "graph_module",
    "scan_status",
    "demo",
    "fallback",
}

_MIN_CONFIDENCE = float(os.getenv("OPS_CHAT_LLM_ROUTER_MIN_CONFIDENCE") or "0.7")


def _is_enabled() -> bool:
    return os.getenv("OPS_CHAT_LLM_ROUTER", "") == "1"


def _build_prompt(message: str) -> str:
    return (
        "你是 Ops Chat 意图分类助手。根据用户输入，输出严格 JSON（不要 markdown 代码块，不要解释）：\n"
        "{\n"
        '  "intent": "以下之一：metrics_trend, issue_list, pr_list, issue_contribution, '
        "graph_module, scan_status, demo, fallback\",\n"
        '  "slots": {},\n'
        '  "confidence": 0.0\n'
        "}\n"
        "slots 可包含 issue_number、days、metric 等键；没有时填 {}。\n"
        "confidence 为 0~1 的浮点数，表示分类置信度。\n\n"
        f"用户输入：{message}"
    )


def _extract_json_obj(content: str) -> dict[str, Any]:
    """从 LLM 输出中提取 JSON 对象；失败时抛出异常。"""
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.S)
        if not match:
            raise ValueError("No JSON object found in LLM response") from None
        data = json.loads(match.group(0))
    if not isinstance(data, dict):
        raise ValueError("LLM response JSON is not an object")
    return data


def _normalize_intent(value: Any) -> str:
    """规范化 intent 为允许值之一，未知则 fallback。"""
    if not isinstance(value, str):
        return "fallback"
    intent = value.strip().lower()
    if intent in _ALLOWED_INTENTS:
        return intent
    return "fallback"


def _clamp_confidence(value: Any) -> float:
    """将 confidence 限制在 [0, 1]。"""
    try:
        confidence = float(value) if value is not None else 0.0
    except (TypeError, ValueError):
        confidence = 0.0
    if not 0.0 <= confidence <= 1.0:
        confidence = 0.0
    return confidence


def _record_fallback_event(
    run_id: str | None,
    store: Any,
    reason: str,
    detail: str,
) -> None:
    """记录 intent_router.fallback 事件；store 未提供时仅记录日志。"""
    if not run_id:
        return
    try:
        from api.ops.store.runs import append_event

        append_event(
            run_id,
            "intent_router.fallback",
            {"reason": reason, "detail": detail},
            store=store,
        )
    except Exception:  # pragma: no cover - 防御性降级
        logger.exception("intent_router.fallback event write failed")


def llm_classify_intent(message: str) -> tuple[str, dict[str, Any], float]:
    """直接调用 LLM 分类意图。

    返回 (intent, slots, confidence)。失败时抛出异常，由调用方降级。
    """
    prompt = _build_prompt(message)
    start = time.perf_counter()
    try:
        result = chat_completion(
            [{"role": "user", "content": prompt}],
            step="intent_router",
            temperature=0.1,
        )
    except Exception as exc:
        latency_ms = (time.perf_counter() - start) * 1000
        logger.warning("router.latency: %.2f ms; LLM failed: %s", latency_ms, exc)
        raise

    latency_ms = (time.perf_counter() - start) * 1000
    logger.info("router.latency: %.2f ms", latency_ms)

    data = _extract_json_obj(result.content)
    intent = _normalize_intent(data.get("intent"))
    slots = data.get("slots") or {}
    if not isinstance(slots, dict):
        slots = {}
    confidence = _clamp_confidence(data.get("confidence"))
    return intent, slots, confidence


def classify_intent_with_llm(
    message: str,
    fallback_fn: Callable[[str], tuple[str, dict[str, Any]]],
    *,
    run_id: str | None = None,
    store: Any = None,
) -> tuple[str, dict[str, Any]]:
    """混合意图分类器。

    - 当 `OPS_CHAT_LLM_ROUTER=1` 时优先调用 LLM router。
    - LLM 低置信度或异常时调用 `fallback_fn` 并记录事件。
    - 默认关闭时直接返回 `fallback_fn(message)`，保持向后兼容。
    """
    if not _is_enabled():
        return fallback_fn(message)

    try:
        intent, slots, confidence = llm_classify_intent(message)
    except Exception as exc:
        result = fallback_fn(message)
        _record_fallback_event(run_id, store, "llm_error", str(exc))
        return result

    if confidence < _MIN_CONFIDENCE:
        result = fallback_fn(message)
        _record_fallback_event(run_id, store, "low_confidence", f"confidence={confidence:.3f}")
        return result

    return intent, slots
