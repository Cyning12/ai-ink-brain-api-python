from __future__ import annotations

from api.intent_agent import IntentDecision, StructuredSignals, build_intent_path_obs
from api.unified_chat import _agent_intent_obs_payload


def test_build_intent_path_obs_llm_first_attempt() -> None:
    obs = build_intent_path_obs({"used": "llm", "attempt": 1, "tool": "rag_search", "confidence": 0.92})
    assert obs["intent_path"] == "llm"
    assert obs["intent_attempt"] == 1
    assert obs["hints_arbitration"] is None


def test_build_intent_path_obs_llm_retry_and_arbitration() -> None:
    obs = build_intent_path_obs(
        {
            "used": "llm_retry",
            "attempt": 2,
            "hints_arbitration": {"applied": True, "reason": "配置：站点人物须查 resume"},
        }
    )
    assert obs["intent_path"] == "llm_retry"
    assert obs["intent_attempt"] == 2
    assert obs["hints_arbitration"]["applied"] is True


def test_build_intent_path_obs_v1_fallback() -> None:
    obs = build_intent_path_obs({"used": "v1_fallback", "confidence": 0.6})
    assert obs["intent_path"] == "v1_fallback"
    assert obs["intent_attempt"] is None


def test_agent_intent_obs_payload_includes_path_fields() -> None:
    d = IntentDecision(
        tool="rag_search",
        mode="rag",
        reasoning="r",
        reasoning_full="r",
        confidence=0.9,
        fallback=None,
        structured_signals=StructuredSignals(llm_prefers_sql=False, has_aggregation_signals=False),
        raw_response={"used": "llm", "attempt": 1, "cache": "hit", "cache_key_hash": "abc"},
    )
    p = _agent_intent_obs_payload(d, debug_router=False)
    assert p["intent_path"] == "llm"
    assert p["intent_attempt"] == 1
    assert p["cache"] == "hit"
    assert p.get("cache_key_hash") is None
