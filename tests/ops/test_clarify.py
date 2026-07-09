"""P1-3: Ops Chat FALLBACK 澄清模块单测。

覆盖：
- clarify 返回 needs_clarification=true 时给出澄清问题。
- clarify 返回 needs_clarification=false 时给出补齐的 intent/slots。
- LLM 调用失败时降级为直接 ReAct fallback。
- clarify 利用 transcript 提供上下文。
- 规则兜底：多 issue 号时询问澄清。
- 无 session_id 时单轮工作。
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from api.ops.llm.types import LlmCompletionResult, LlmUsage
from api.ops.orchestrator.core import Intent


def _make_llm_result(content: str, step: str = "clarify") -> LlmCompletionResult:
    return LlmCompletionResult(
        content=content,
        usage=LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            latency_ms=100,
            step=step,
        ),
    )


def test_clarify_asks_when_needs_clarification(monkeypatch: pytest.MonkeyPatch) -> None:
    """clarify 返回 needs_clarification=true 时应给出澄清问题。"""
    from api.ops.orchestrator import clarify

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return _make_llm_result(
            json.dumps(
                {
                    "needs_clarification": True,
                    "clarify_question": "你想比较 #123 和 #545 的哪方面？",
                    "intent": None,
                    "slots": {},
                },
                ensure_ascii=False,
            )
        )

    monkeypatch.setattr(clarify, "chat_completion", fake_chat_completion)
    result = clarify.clarify_if_fallback("比较 #123 和 #545", "sess-1", [], {"issue_numbers": [123, 545]})

    assert result.needs_clarification is True
    assert result.clarify_question == "你想比较 #123 和 #545 的哪方面？"
    assert result.intent is None
    assert result.slots is None


def test_clarify_resolves_intent_and_slots(monkeypatch: pytest.MonkeyPatch) -> None:
    """clarify 返回 needs_clarification=false 时应给出补齐的 intent/slots。"""
    from api.ops.orchestrator import clarify

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return _make_llm_result(
            json.dumps(
                {
                    "needs_clarification": False,
                    "clarify_question": None,
                    "intent": "issue_contribution",
                    "slots": {"issue_number": 123},
                },
                ensure_ascii=False,
            )
        )

    monkeypatch.setattr(clarify, "chat_completion", fake_chat_completion)
    result = clarify.clarify_if_fallback("这个 issue 适合我吗", "sess-1", [], {})

    assert result.needs_clarification is False
    assert result.intent == "issue_contribution"
    assert result.slots == {"issue_number": 123}


def test_clarify_degrades_to_react_on_llm_failure(monkeypatch: pytest.MonkeyPatch) -> None:
    """LLM 调用失败时降级为直接 ReAct fallback。"""
    from api.ops.orchestrator import clarify

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        raise RuntimeError("LLM timeout")

    monkeypatch.setattr(clarify, "chat_completion", fake_chat_completion)
    result = clarify.clarify_if_fallback("模糊问题", None, [], {})

    assert result.needs_clarification is False
    assert result.intent == Intent.FALLBACK
    assert result.slots == {}


def test_clarify_uses_transcript_in_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    """clarify 应将 transcript 拼接到 prompt 中传给 LLM。"""
    from api.ops.orchestrator import clarify

    captured: list[list[dict[str, str]]] = []

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        captured.append(messages)
        return _make_llm_result(
            json.dumps(
                {"needs_clarification": True, "clarify_question": "请补充 issue 号。"},
                ensure_ascii=False,
            )
        )

    monkeypatch.setattr(clarify, "chat_completion", fake_chat_completion)
    transcript = [
        {"role": "user", "content": "之前问 #123"},
        {"role": "assistant", "content": "#123 是 bug。"},
    ]
    clarify.clarify_if_fallback("它呢", "sess-1", transcript, {})

    assert len(captured) == 1
    prompt = captured[0][0]["content"]
    assert "之前问 #123" in prompt
    assert "#123 是 bug。" in prompt
    assert "它呢" in prompt


def test_clarify_rule_fallback_for_multiple_issues(monkeypatch: pytest.MonkeyPatch) -> None:
    """LLM 失败且存在多个 issue 号时，规则兜底询问澄清。"""
    from api.ops.orchestrator import clarify

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        raise RuntimeError("LLM timeout")

    monkeypatch.setattr(clarify, "chat_completion", fake_chat_completion)
    result = clarify.clarify_if_fallback("比较一下", "sess-1", [], {"issue_numbers": [123, 545]})

    assert result.needs_clarification is True
    assert "#123" in (result.clarify_question or "")
    assert "#545" in (result.clarify_question or "")


def test_clarify_no_session_id_works(monkeypatch: pytest.MonkeyPatch) -> None:
    """无 session_id 时 clarify 仍能单轮工作。"""
    from api.ops.orchestrator import clarify

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return _make_llm_result(
            json.dumps(
                {
                    "needs_clarification": False,
                    "intent": "issue_contribution",
                    "slots": {"issue_number": 545},
                },
                ensure_ascii=False,
            )
        )

    monkeypatch.setattr(clarify, "chat_completion", fake_chat_completion)
    result = clarify.clarify_if_fallback("545 适合吗", None, [], {})

    assert result.needs_clarification is False
    assert result.intent == "issue_contribution"
