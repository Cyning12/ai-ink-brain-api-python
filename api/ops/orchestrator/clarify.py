"""Ops Chat FALLBACK 澄清模块（P1-3）。

当规则意图分类器返回 FALLBACK 时，先通过 LLM 进行 1 轮澄清，或基于规则兜底：
- needs_clarification=true：向用户展示澄清问题，等待补充。
- needs_clarification=false：给出补齐后的 intent/slots，继续走原 deep/fast/react 路由。

LLM 调用失败时，降级为直接 ReAct fallback（保持可用性）。
"""

from __future__ import annotations

import json
import logging
import re
from dataclasses import dataclass
from typing import Any

from api.ops.llm import chat_completion
from api.ops.orchestrator.core import Intent

logger = logging.getLogger(__name__)


@dataclass
class ClarifyResult:
    """澄清结果。

    - needs_clarification=true：须展示 clarify_question 给用户。
    - needs_clarification=false：使用 intent/slots 继续路由；
      若 intent 仍为 FALLBACK，则进入 ReAct fallback。
    """

    needs_clarification: bool
    clarify_question: str | None = None
    intent: str | None = None
    slots: dict[str, Any] | None = None


def _build_clarify_prompt(
    query: str,
    transcript: list[dict[str, str]],
    slots: dict[str, Any],
) -> str:
    """构造澄清 LLM 的 prompt。"""
    transcript_text = "\n".join(f"{msg['role']}: {msg['content']}" for msg in transcript) or "（无）"
    return (
        "你是 Ops Desk 意图澄清助手。当规则分类器无法确定用户意图时，"
        "你负责决定：1) 向用户提出 1 轮简洁澄清问题；或 2) 直接推断出最可能的意图与 slots。\n\n"
        "可用意图：metrics_trend, issue_list, pr_list, issue_contribution, "
        "graph_module, scan_status, fallback。"
        "如果信息仍不足，intent 请填 fallback。\n\n"
        f"历史对话：\n{transcript_text}\n\n"
        f"当前用户输入：{query}\n"
        f"当前 slots：{json.dumps(slots, ensure_ascii=False)}\n\n"
        "请输出 JSON：\n"
        "{\n"
        '  "needs_clarification": true/false,\n'
        '  "clarify_question": "问题文本或 null",\n'
        '  "intent": "意图字符串",\n'
        '  "slots": {}\n'
        "}"
    )


def _rule_fallback(query: str, slots: dict[str, Any]) -> ClarifyResult:
    """规则兜底：多个 issue 号时询问澄清，否则降级为直接 ReAct fallback。"""
    issue_numbers = slots.get("issue_numbers") or []
    if len(issue_numbers) >= 2:
        nums = " / ".join(f"#{n}" for n in issue_numbers)
        return ClarifyResult(
            needs_clarification=True,
            clarify_question=f"你想比较 {nums} 的哪方面？（例如贡献度、状态、关联模块）",
        )
    return ClarifyResult(needs_clarification=False, intent=Intent.FALLBACK, slots={})


def _parse_clarify_response(content: str) -> ClarifyResult:
    """解析 LLM 返回的 JSON，生成 ClarifyResult。"""
    data: dict[str, Any]
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", content, re.S)
        if not match:
            raise ValueError("No JSON object found in clarify response") from None
        data = json.loads(match.group(0))

    if not isinstance(data, dict):
        raise ValueError("Clarify response is not a JSON object")

    needs = bool(data.get("needs_clarification"))
    if needs:
        question = data.get("clarify_question")
        return ClarifyResult(
            needs_clarification=True,
            clarify_question=str(question) if question is not None else None,
        )

    intent = data.get("intent") or Intent.FALLBACK
    slots = data.get("slots") or {}
    if not isinstance(slots, dict):
        slots = {}
    return ClarifyResult(needs_clarification=False, intent=str(intent), slots=slots)


def clarify_if_fallback(
    query: str,
    session_id: str | None,
    transcript: list[dict[str, str]],
    slots: dict[str, Any],
) -> ClarifyResult:
    """对 FALLBACK 意图进行 1 轮澄清或补齐。

    参数:
        query: 当前用户消息。
        session_id: 可选 session id（仅用于日志/跟踪，不决定行为）。
        transcript: 最近 N 轮对话上下文。
        slots: 当前规则分类器提取的 slots。

    返回:
        ClarifyResult。
    """
    prompt = _build_clarify_prompt(query, transcript, slots)
    messages = [{"role": "user", "content": prompt}]
    try:
        result = chat_completion(messages, step="clarify", temperature=0.3)
        parsed = _parse_clarify_response(result.content)
        if parsed.needs_clarification and not parsed.clarify_question:
            # LLM 表示需要澄清但没有给问题，回退到规则兜底
            return _rule_fallback(query, slots)
        return parsed
    except Exception as exc:  # pragma: no cover - 防御性降级
        logger.warning("clarify.llm_failed: %s", exc)
        return _rule_fallback(query, slots)
