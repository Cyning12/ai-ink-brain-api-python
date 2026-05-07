"""IntentCache（LRU+TTL+history key）单元测试：不触网。"""

from __future__ import annotations

import asyncio
import time
from typing import Any

import pytest

import api.intent_agent as ia
from api.intent_agent import IntentDecision, clear_intent_cache, compute_history_hash, decide_intent_v2
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
    """每条用例独立缓存实例，避免串扰。"""
    fresh = ia.LRUCache(maxsize=1000, ttl_s=300.0)
    monkeypatch.setattr(ia, "_intent_cache", fresh)
    yield


def test_history_hash_isolates_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    """相同 query、不同 history 不得命中同一缓存条目。"""

    async def _run() -> None:
        monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")
        calls: list[int] = []

        async def _fake_llm(*, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float) -> dict[str, Any]:
            _ = (oai, tools, timeout_s)
            calls.append(1)
            return {"tool": "rag_search", "reasoning": "ok", "confidence": 0.9}

        monkeypatch.setattr(ia, "_llm_decide_v2", _fake_llm)
        monkeypatch.setattr(ia, "openai_siliconflow_client", lambda: object())
        tools = _make_tools()
        q = "昨天销售额是多少"
        h1: list[dict[str, Any]] = [{"role": "user", "content": "你好"}]
        h2: list[dict[str, Any]] = [{"role": "user", "content": "再见"}]

        assert compute_history_hash(h1) != compute_history_hash(h2)

        d1 = await decide_intent_v2(query=q, history=h1, tools=tools, timeout=3.0)
        d2 = await decide_intent_v2(query=q, history=h2, tools=tools, timeout=3.0)
        assert d1.raw_response.get("cache") == "miss"
        assert d2.raw_response.get("cache") == "miss"
        assert len(calls) == 2

        d1b = await decide_intent_v2(query=q, history=h1, tools=tools, timeout=3.0)
        assert d1b.raw_response.get("cache") == "hit"
        assert len(calls) == 2

    asyncio.run(_run())


def test_ttl_expires(monkeypatch: pytest.MonkeyPatch) -> None:
    """TTL 到期后同一 key 不得再命中。"""

    async def _run() -> None:
        tiny = ia.LRUCache(maxsize=100, ttl_s=0.05)
        monkeypatch.setattr(ia, "_intent_cache", tiny)
        monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
        tools = _make_tools()

        d1 = await decide_intent_v2(query="仅用于 TTL 测试", history=[], tools=tools, timeout=3.0)
        assert d1.raw_response.get("cache") == "miss"
        d2 = await decide_intent_v2(query="仅用于 TTL 测试", history=[], tools=tools, timeout=3.0)
        assert d2.raw_response.get("cache") == "hit"

        time.sleep(0.08)
        d3 = await decide_intent_v2(query="仅用于 TTL 测试", history=[], tools=tools, timeout=3.0)
        assert d3.raw_response.get("cache") == "miss"

    asyncio.run(_run())


def test_lru_eviction(monkeypatch: pytest.MonkeyPatch) -> None:
    """超 maxsize 后按 LRU 淘汰最早条目。"""

    async def _run() -> None:
        tiny = ia.LRUCache(maxsize=2, ttl_s=300.0)
        monkeypatch.setattr(ia, "_intent_cache", tiny)
        monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")
        calls: list[str] = []

        async def _fake_llm(*, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float) -> dict[str, Any]:
            _ = (oai, history, tools, timeout_s)
            calls.append(query)
            return {"tool": "rag_search", "reasoning": query, "confidence": 0.8}

        monkeypatch.setattr(ia, "_llm_decide_v2", _fake_llm)
        monkeypatch.setattr(ia, "openai_siliconflow_client", lambda: object())
        tools = _make_tools()

        await decide_intent_v2(query="k-a", history=[], tools=tools, timeout=3.0)
        await decide_intent_v2(query="k-b", history=[], tools=tools, timeout=3.0)
        await decide_intent_v2(query="k-c", history=[], tools=tools, timeout=3.0)
        assert len(calls) == 3

        await decide_intent_v2(query="k-a", history=[], tools=tools, timeout=3.0)
        assert len(calls) == 4, "k-a 应已被淘汰，再次请求应走 miss 并调用 LLM"

    asyncio.run(_run())


def test_cache_hit_latency_under_10ms(monkeypatch: pytest.MonkeyPatch) -> None:
    """第二次同 key：命中路径 wall-clock 与 raw_response.latency_ms 均极低。"""

    async def _run() -> None:
        monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")

        async def _fake_llm(*, oai: Any, query: str, history: list[dict[str, Any]], tools: list[Tool], timeout_s: float) -> dict[str, Any]:
            _ = (oai, query, history, tools, timeout_s)
            return {"tool": "direct_answer", "reasoning": "x", "confidence": 0.9}

        monkeypatch.setattr(ia, "_llm_decide_v2", _fake_llm)
        monkeypatch.setattr(ia, "openai_siliconflow_client", lambda: object())
        tools = _make_tools()

        await decide_intent_v2(query="latency probe", history=[], tools=tools, timeout=3.0)
        t0 = time.perf_counter()
        d = await decide_intent_v2(query="latency probe", history=[], tools=tools, timeout=3.0)
        wall_ms = (time.perf_counter() - t0) * 1000.0
        assert d.raw_response.get("cache") == "hit"
        assert int(d.raw_response.get("latency_ms", 999)) < 10
        assert wall_ms < 10.0

    asyncio.run(_run())


def test_clear_intent_cache() -> None:
    clear_intent_cache()
    assert ia._intent_cache.get("no_such_key") is None


def test_raw_response_has_cache_key_hash(monkeypatch: pytest.MonkeyPatch) -> None:
    async def _run() -> None:
        monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
        tools = _make_tools()
        d = await decide_intent_v2(query="hello", history=[], tools=tools, timeout=3.0)
        assert d.raw_response.get("cache") == "miss"
        assert isinstance(d.raw_response.get("cache_key_hash"), str)
        assert len(d.raw_response.get("cache_key_hash", "")) == 16

    asyncio.run(_run())


def test_stored_decision_strips_volatile_raw_keys(monkeypatch: pytest.MonkeyPatch) -> None:
    """缓存内副本不应长期携带上一轮 cache/latency，避免命中时污染。"""

    async def _run() -> None:
        monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "false")
        tools = _make_tools()
        await decide_intent_v2(query="strip test", history=[], tools=tools, timeout=3.0)
        ck = ia._intent_composite_cache_key(query="strip test", history=[])
        raw_stored = ia._intent_cache.get(ck)
        assert isinstance(raw_stored, IntentDecision)
        assert "cache" not in raw_stored.raw_response
        assert "latency_ms" not in raw_stored.raw_response

    asyncio.run(_run())
