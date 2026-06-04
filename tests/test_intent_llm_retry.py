"""Intent LLM 外呼重试（U1.5）：不触网。"""

from __future__ import annotations

import asyncio
from typing import Any

import pytest

import api.intent_agent as ia
from api.intent_agent import clear_intent_cache, decide_intent_v2
from api.tools import Tool


async def _noop_exec(query: str, *, history: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    _ = (query, history)
    return {"ok": True}


def _make_tools() -> list[Tool]:
    return [
        Tool(name="text2sql_query", description="结构化查数。", parameters={}, execute=_noop_exec),
        Tool(name="rag_search", description="检索文档。", parameters={}, execute=_noop_exec),
        Tool(name="direct_answer", description="直接回答。", parameters={}, execute=_noop_exec),
    ]


@pytest.fixture(autouse=True)
def _reset_intent_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    fresh = ia.LRUCache(maxsize=1000, ttl_s=300.0)
    monkeypatch.setattr(ia, "_intent_cache", fresh)
    clear_intent_cache()
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM_RETRIES", "3")
    monkeypatch.setenv("CHATBI_V2_INTENT_LLM_RETRY_BACKOFF_S", "0")
    monkeypatch.setattr(ia, "openai_siliconflow_client", lambda: object())
    yield


def test_intent_llm_retry_succeeds_on_third_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[int] = []

    async def _flaky_llm(
        *, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float, capture_prompts: bool = False
    ) -> tuple[dict[str, Any], list[dict[str, Any]] | None]:
        _ = (oai, query, history, tools, timeout_s, capture_prompts)
        calls.append(1)
        if len(calls) < 3:
            raise asyncio.TimeoutError()
        return {"tool": "rag_search", "reasoning": "ok", "confidence": 0.91}, None

    monkeypatch.setattr(ia, "_llm_decide_v2", _flaky_llm)

    async def _run() -> None:
        d = await decide_intent_v2(query="Portfolio 优势", history=[], tools=_make_tools(), timeout=3.0)
        assert d.tool == "rag_search"
        assert d.raw_response.get("used") == "llm_retry"
        assert d.raw_response.get("attempt") == 3
        assert len(calls) == 3

    asyncio.run(_run())


def test_intent_llm_retry_exhausted_falls_back_v1(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[int] = []

    async def _always_timeout(
        *, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float, capture_prompts: bool = False
    ) -> tuple[dict[str, Any], list[dict[str, Any]] | None]:
        _ = (oai, query, history, tools, timeout_s, capture_prompts)
        calls.append(1)
        raise asyncio.TimeoutError()

    class _V1:
        final_mode = "rag"

    monkeypatch.setattr(ia, "_llm_decide_v2", _always_timeout)
    monkeypatch.setattr(ia, "decide_intent_v1", lambda *, query, prefer: _V1())  # noqa: ARG005

    async def _run() -> None:
        d = await decide_intent_v2(query="任意问句", history=[], tools=_make_tools(), timeout=3.0)
        assert d.tool == "rag_search"
        assert d.raw_response.get("used") == "v1_fallback"
        assert len(calls) == 3

    asyncio.run(_run())


def test_intent_llm_json_error_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[int] = []

    async def _bad_json(
        *, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float, capture_prompts: bool = False
    ) -> tuple[dict[str, Any], list[dict[str, Any]] | None]:
        _ = (oai, query, history, tools, timeout_s, capture_prompts)
        calls.append(1)
        raise ValueError("LLM intent 输出不是合法 JSON")

    monkeypatch.setattr(ia, "_llm_decide_v2", _bad_json)

    async def _run() -> None:
        d = await decide_intent_v2(query="坏 JSON", history=[], tools=_make_tools(), timeout=3.0)
        assert d.raw_response.get("used") == "heuristic"
        assert len(calls) == 1

    asyncio.run(_run())


def test_intent_llm_retry_timeout_decreases_per_attempt(monkeypatch: pytest.MonkeyPatch) -> None:
    timeouts: list[float] = []

    async def _flaky_with_timeout(
        *, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float, capture_prompts: bool = False
    ) -> tuple[dict[str, Any], list[dict[str, Any]] | None]:
        _ = (oai, query, history, tools, capture_prompts)
        timeouts.append(timeout_s)
        if len(timeouts) < 3:
            raise asyncio.TimeoutError()
        return {"tool": "rag_search", "reasoning": "ok", "confidence": 0.9}, None

    monkeypatch.setenv("CHATBI_V2_INTENT_TIMEOUT_S", "60")
    monkeypatch.setattr(ia, "_llm_decide_v2", _flaky_with_timeout)

    async def _run() -> None:
        d = await decide_intent_v2(query="timeout 阶梯", history=[], tools=_make_tools(), timeout=3.0)
        assert d.raw_response.get("timeout_s") == 24.0
        assert timeouts == [60.0, 39.0, 24.0]

    asyncio.run(_run())


def test_intent_llm_retry_logs_without_debug_intent_cache(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    import logging

    calls: list[int] = []

    async def _flaky_llm(
        *, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float, capture_prompts: bool = False
    ) -> tuple[dict[str, Any], list[dict[str, Any]] | None]:
        _ = (oai, query, history, tools, timeout_s, capture_prompts)
        calls.append(1)
        if len(calls) < 2:
            raise asyncio.TimeoutError()
        return {"tool": "rag_search", "reasoning": "ok", "confidence": 0.9}, None

    monkeypatch.delenv("DEBUG_INTENT_CACHE", raising=False)
    monkeypatch.setattr(ia, "_llm_decide_v2", _flaky_llm)

    with caplog.at_level(logging.INFO, logger="api.intent_agent"):
        asyncio.run(
            decide_intent_v2(query="重试日志", history=[], tools=_make_tools(), timeout=3.0)
        )

    text = caplog.text
    assert "[intent-retry]" in text
    assert "will_retry" in text
    assert "success attempt=2" in text


def test_intent_llm_retryable_classifier() -> None:
    assert ia._intent_llm_retryable(asyncio.TimeoutError()) is True
    assert ia._intent_llm_retryable(ValueError("bad json")) is False
