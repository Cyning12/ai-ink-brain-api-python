from __future__ import annotations

import asyncio
from pathlib import Path
from typing import Any

import pytest

from api.intent_agent import (
    IntentDecision,
    StructuredSignals,
    apply_hints_arbitration,
    decide_intent_v2,
)
from api.intent_hints import (
    arbitration_enabled,
    clear_intent_hints_cache,
    hints_arbitration_should_apply,
    load_hints,
    match_person_rag_signal,
    rag_rule_hits_from_hints,
)
from api.tools import Tool


async def _dummy_execute(*, query: str, history: list[dict[str, Any]] | None = None) -> Any:  # noqa: ANN401
    _ = (query, history)
    return {"ok": True}


def _make_tools() -> list[Tool]:
    async def _exec(query: str, *, history: list[dict[str, Any]] | None = None) -> Any:  # noqa: ANN401
        return await _dummy_execute(query=query, history=history)

    return [
        Tool(
            name="text2sql_query",
            description="执行结构化数据查询与聚合统计，返回具体数值/表格结果。",
            parameters={},
            execute=_exec,
        ),
        Tool(
            name="rag_search",
            description="检索项目内部文档/知识库来回答概念、方法、原理、对比、操作步骤等问题。",
            parameters={},
            execute=_exec,
        ),
        Tool(
            name="direct_answer",
            description="不依赖内部数据或文档，直接完成翻译、润色、写作、代码生成、通用知识解释等任务。",
            parameters={},
            execute=_exec,
        ),
    ]


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def _default_hints() -> dict[str, Any]:
    data = load_hints(_repo_root() / "docs/chatbi/v1/intent_hints.yaml")
    assert data is not None
    return data


def _direct_decision() -> IntentDecision:
    return IntentDecision(
        tool="direct_answer",
        mode="no_data",
        reasoning="通识",
        reasoning_full="通识解释",
        confidence=0.9,
        fallback=None,
        structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=False),
        raw_response={"tool": "direct_answer", "confidence": 0.9},
    )


Q4 = "11 年经历里 AI Coding 相关成果？"
Q_INTENT = "聊聊你对刘新宁的看法，他在 AI coding 岗位有什么优势"
Q_NEGATIVE = "解释一下量子计算，用通俗语言"


def _patch_openai(monkeypatch: pytest.MonkeyPatch) -> None:
    import api.intent_agent as ia

    class _DummyOAI:
        pass

    monkeypatch.setattr(ia, "openai_siliconflow_client", lambda: _DummyOAI())


def test_rag_rule_hits_from_hints_q4() -> None:
    hints = _default_hints()
    hits = rag_rule_hits_from_hints(Q4, hints)
    assert "rule:portfolio_keyword" in hits
    assert any(h.startswith("rule:portfolio_regex:") for h in hits)


def test_match_person_rag_signal_q_intent() -> None:
    hints = _default_hints()
    assert match_person_rag_signal(Q_INTENT, hints) is True
    assert hints_arbitration_should_apply(Q_INTENT, hints)[0] is True


def test_arbitration_negative_quantum() -> None:
    hints = _default_hints()
    assert hints_arbitration_should_apply(Q_NEGATIVE, hints)[0] is False


def test_apply_hints_arbitration_q4() -> None:
    out = apply_hints_arbitration(_direct_decision(), query=Q4, hints=_default_hints())
    assert out.tool == "rag_search"
    assert out.mode == "rag"
    arb = out.raw_response.get("hints_arbitration") or {}
    assert arb.get("applied") is True


def test_apply_hints_arbitration_disabled_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("INTENT_HINTS_ARBITRATION", "0")
    clear_intent_hints_cache()
    hints = _default_hints()
    assert arbitration_enabled(hints) is False
    out = apply_hints_arbitration(_direct_decision(), query=Q4, hints=hints)
    assert out.tool == "direct_answer"
    assert "hints_arbitration" not in out.raw_response


def test_decide_intent_v2_mock_llm_direct_arbitrates_q4(monkeypatch: pytest.MonkeyPatch) -> None:
    import api.intent_agent as ia

    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")
    monkeypatch.setenv("INTENT_HINTS_ENABLED", "true")
    monkeypatch.setenv("INTENT_HINTS_ARBITRATION", "true")
    ia.clear_intent_cache()
    clear_intent_hints_cache()
    _patch_openai(monkeypatch)

    async def _mock_direct(**kwargs: Any) -> tuple[dict[str, Any], None]:
        return {"tool": "direct_answer", "reasoning": "误判", "confidence": 0.95}, None

    monkeypatch.setattr(ia, "_llm_decide_v2", _mock_direct)

    d = asyncio.run(
        decide_intent_v2(query=Q4, history=[], tools=_make_tools(), timeout=3.0)
    )
    assert d.tool == "rag_search"
    assert (d.raw_response.get("hints_arbitration") or {}).get("applied") is True


def test_decide_intent_v2_mock_llm_direct_arbitrates_q_intent(monkeypatch: pytest.MonkeyPatch) -> None:
    import api.intent_agent as ia

    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")
    monkeypatch.setenv("INTENT_HINTS_ENABLED", "true")
    ia.clear_intent_cache()
    clear_intent_hints_cache()
    _patch_openai(monkeypatch)

    async def _mock_direct(**kwargs: Any) -> tuple[dict[str, Any], None]:
        return {"tool": "direct_answer", "reasoning": "误判", "confidence": 0.95}, None

    monkeypatch.setattr(ia, "_llm_decide_v2", _mock_direct)

    d = asyncio.run(
        decide_intent_v2(query=Q_INTENT, history=[], tools=_make_tools(), timeout=3.0)
    )
    assert d.tool == "rag_search"
    assert (d.raw_response.get("hints_arbitration") or {}).get("applied") is True


def test_decide_intent_v2_mock_llm_direct_no_arbitration_negative(monkeypatch: pytest.MonkeyPatch) -> None:
    import api.intent_agent as ia

    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")
    monkeypatch.setenv("INTENT_HINTS_ENABLED", "true")
    ia.clear_intent_cache()
    clear_intent_hints_cache()
    _patch_openai(monkeypatch)

    async def _mock_direct(**kwargs: Any) -> tuple[dict[str, Any], None]:
        return {"tool": "direct_answer", "reasoning": "通识", "confidence": 0.88}, None

    monkeypatch.setattr(ia, "_llm_decide_v2", _mock_direct)

    d = asyncio.run(
        decide_intent_v2(query=Q_NEGATIVE, history=[], tools=_make_tools(), timeout=3.0)
    )
    assert d.tool == "direct_answer"
    assert "hints_arbitration" not in d.raw_response


def test_decide_intent_v2_timeout_v1_portfolio_q4(monkeypatch: pytest.MonkeyPatch) -> None:
    import api.intent_agent as ia

    monkeypatch.setenv("CHATBI_V2_INTENT_LLM", "true")
    monkeypatch.setenv("INTENT_HINTS_ENABLED", "true")
    ia.clear_intent_cache()
    clear_intent_hints_cache()
    _patch_openai(monkeypatch)

    async def _timeout(**kwargs: Any) -> tuple[dict[str, Any], None]:
        raise asyncio.TimeoutError

    monkeypatch.setattr(ia, "_llm_decide_v2", _timeout)

    d = asyncio.run(
        decide_intent_v2(query=Q4, history=[], tools=_make_tools(), timeout=3.0)
    )
    assert d.tool == "rag_search"
    assert d.raw_response.get("used") == "v1_fallback"
