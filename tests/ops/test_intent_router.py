"""P1-4: Ops Chat LLM intent router 单测。

覆盖：
- OPS_CHAT_LLM_ROUTER=1 时 LLM router 返回合法 JSON intent。
- 低置信度时降级为规则 fallback。
- LLM 超时 / 非法 JSON 时降级为规则 fallback。
- 默认未开启时走原有规则。
- 通过 classify_intent 走 LLM router 的集成路径。
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from api.ops.llm.types import LlmCompletionResult, LlmUsage


def _make_llm_result(
    content: str,
    step: str = "intent_router",
    latency_ms: float = 80.0,
) -> LlmCompletionResult:
    return LlmCompletionResult(
        content=content,
        usage=LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=20,
            completion_tokens=10,
            total_tokens=30,
            latency_ms=latency_ms,
            step=step,
        ),
    )


class FakeStore:
    """内存版 OpsRunStore，仅记录 append_event。"""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []

    def append_event(
        self,
        run_id: str,
        agent_role: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
        seq: int | None = None,
    ) -> dict[str, Any]:
        evt: dict[str, Any] = {
            "run_id": run_id,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
            "seq": seq or len(self.events) + 1,
        }
        self.events.append(evt)
        return evt


def test_llm_router_enabled_returns_valid_intent(monkeypatch: pytest.MonkeyPatch) -> None:
    """OPS_CHAT_LLM_ROUTER=1 且 LLM 返回合法 JSON 时，优先采用 LLM 结果。"""
    monkeypatch.setenv("OPS_CHAT_LLM_ROUTER", "1")
    from api.ops import intent_router

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return _make_llm_result(
            json.dumps(
                {"intent": "issue_contribution", "slots": {"issue_number": 123}, "confidence": 0.95},
                ensure_ascii=False,
            )
        )

    monkeypatch.setattr(intent_router, "chat_completion", fake_chat_completion)

    intent, slots = intent_router.classify_intent_with_llm("分析 #123", lambda _msg: ("fallback", {}))

    assert intent == "issue_contribution"
    assert slots == {"issue_number": 123}


def test_llm_router_low_confidence_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """置信度低于阈值时降级为规则 fallback，并记录 intent_router.fallback 事件。"""
    monkeypatch.setenv("OPS_CHAT_LLM_ROUTER", "1")
    from api.ops import intent_router

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return _make_llm_result(
            json.dumps(
                {"intent": "issue_contribution", "slots": {"issue_number": 123}, "confidence": 0.2},
                ensure_ascii=False,
            )
        )

    monkeypatch.setattr(intent_router, "chat_completion", fake_chat_completion)

    fallback_calls: list[str] = []

    def rule_fallback(msg: str) -> tuple[str, dict[str, Any]]:
        fallback_calls.append(msg)
        return "metrics_trend", {"days": 7}

    store = FakeStore()
    intent, slots = intent_router.classify_intent_with_llm(
        "比较含糊的问题",
        rule_fallback,
        run_id="run-low-conf",
        store=store,
    )

    assert intent == "metrics_trend"
    assert slots == {"days": 7}
    assert fallback_calls == ["比较含糊的问题"]

    fallback_events = [e for e in store.events if e["event_type"] == "intent_router.fallback"]
    assert len(fallback_events) == 1
    assert fallback_events[0]["payload"]["reason"] == "low_confidence"
    assert "0.2" in fallback_events[0]["payload"]["detail"]


def test_llm_router_invalid_json_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """LLM 返回非法 JSON 时降级为规则 fallback，并记录 intent_router.fallback 事件。"""
    monkeypatch.setenv("OPS_CHAT_LLM_ROUTER", "1")
    from api.ops import intent_router

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return _make_llm_result("这不是 JSON")

    monkeypatch.setattr(intent_router, "chat_completion", fake_chat_completion)

    def rule_fallback(_msg: str) -> tuple[str, dict[str, Any]]:
        return "fallback", {}

    store = FakeStore()
    intent, slots = intent_router.classify_intent_with_llm(
        "模糊问题",
        rule_fallback,
        run_id="run-bad-json",
        store=store,
    )

    assert intent == "fallback"
    assert slots == {}

    fallback_events = [e for e in store.events if e["event_type"] == "intent_router.fallback"]
    assert len(fallback_events) == 1
    assert fallback_events[0]["payload"]["reason"] == "llm_error"


def test_llm_router_timeout_fallback(monkeypatch: pytest.MonkeyPatch) -> None:
    """LLM 调用超时/抛异常时降级为规则 fallback，并记录 intent_router.fallback 事件。"""
    monkeypatch.setenv("OPS_CHAT_LLM_ROUTER", "1")
    from api.ops import intent_router

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        raise TimeoutError("LLM timeout")

    monkeypatch.setattr(intent_router, "chat_completion", fake_chat_completion)

    def rule_fallback(_msg: str) -> tuple[str, dict[str, Any]]:
        return "metrics_trend", {"metric": "cycle-time"}

    store = FakeStore()
    intent, slots = intent_router.classify_intent_with_llm(
        "最近 PR 周期多少",
        rule_fallback,
        run_id="run-timeout",
        store=store,
    )

    assert intent == "metrics_trend"
    assert slots == {"metric": "cycle-time"}

    fallback_events = [e for e in store.events if e["event_type"] == "intent_router.fallback"]
    assert len(fallback_events) == 1
    assert fallback_events[0]["payload"]["reason"] == "llm_error"
    assert "LLM timeout" in fallback_events[0]["payload"]["detail"]


def test_llm_router_disabled_uses_rule(monkeypatch: pytest.MonkeyPatch) -> None:
    """默认未开启 OPS_CHAT_LLM_ROUTER 时，走原有规则，不调用 LLM。"""
    monkeypatch.delenv("OPS_CHAT_LLM_ROUTER", raising=False)
    from api.ops import intent_router

    llm_calls: list[Any] = []

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        llm_calls.append(messages)
        return _make_llm_result(json.dumps({"intent": "issue_list", "slots": {}, "confidence": 0.9}))

    monkeypatch.setattr(intent_router, "chat_completion", fake_chat_completion)

    def rule_fallback(_msg: str) -> tuple[str, dict[str, Any]]:
        return "pr_list", {}

    intent, slots = intent_router.classify_intent_with_llm("列出 PR", rule_fallback)

    assert intent == "pr_list"
    assert slots == {}
    assert llm_calls == []


def test_classify_intent_uses_llm_router(monkeypatch: pytest.MonkeyPatch) -> None:
    """集成测：通过 api.ops.orchestrator.classify_intent 走 LLM router。"""
    monkeypatch.setenv("OPS_CHAT_LLM_ROUTER", "1")
    from api.ops import intent_router
    from api.ops.orchestrator import classify_intent

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return _make_llm_result(
            json.dumps(
                {"intent": "issue_list", "slots": {}, "confidence": 0.88},
                ensure_ascii=False,
            )
        )

    monkeypatch.setattr(intent_router, "chat_completion", fake_chat_completion)

    store = FakeStore()
    intent, slots = classify_intent("列出所有 issues", run_id="run-integration", store=store)

    assert intent == "issue_list"
    assert slots == {}
    fallback_events = [e for e in store.events if e["event_type"] == "intent_router.fallback"]
    assert fallback_events == []
