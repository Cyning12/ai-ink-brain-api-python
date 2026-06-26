"""Orchestrator 意图分类（中文 metrics 问句 + P3-1 对比/多 issue fallback）。"""

from __future__ import annotations

from api.ops.orchestrator.core import Intent, classify_intent, is_fast_intent


def test_issue_median_routes_to_throughput_fast() -> None:
    intent, slots = classify_intent("最近30天的issue中位数是多少")
    assert intent == Intent.METRICS_TREND
    assert slots.get("metric") == "issue-throughput"
    assert slots.get("days") == 30
    assert is_fast_intent(intent)


def test_review_median_routes_to_review_time() -> None:
    intent, slots = classify_intent("PR review time 中位数是多少？")
    assert intent == Intent.METRICS_TREND
    assert slots.get("metric") == "review-time"
    assert is_fast_intent(intent)


def test_bare_median_defaults_review_time() -> None:
    intent, slots = classify_intent("最近30天的中位数是多少")
    assert intent == Intent.METRICS_TREND
    assert slots.get("metric") == "review-time"


def test_single_issue_still_issue_contribution() -> None:
    """单 issue（仅 1 个 #N、无对比语义）→ ISSUE_CONTRIBUTION（deep）。"""
    intent, slots = classify_intent("#545 适合我吗")
    assert intent == Intent.ISSUE_CONTRIBUTION
    assert slots.get("issue_number") == 545
    assert not is_fast_intent(intent)


def test_comparison_with_keyword_returns_fallback() -> None:
    """含对比关键词 + 多个 #N → FALLBACK（react）。"""
    intent, slots = classify_intent("对比 #545 和 #600 哪个更适合新手")
    assert intent == Intent.FALLBACK
    assert slots.get("issue_numbers") == [545, 600]


def test_comparison_vs_returns_fallback() -> None:
    """含 vs 语义 + 多个 #N → FALLBACK。"""
    intent, slots = classify_intent("#545 vs #600 谁更适合新手")
    assert intent == Intent.FALLBACK
    assert slots.get("issue_numbers") == [545, 600]


def test_multiple_issues_without_keyword_returns_fallback() -> None:
    """无显式对比词但 ≥2 个不同 issue 号 → FALLBACK。"""
    intent, slots = classify_intent("看看 #545 #600 的情况")
    assert intent == Intent.FALLBACK
    assert slots.get("issue_numbers") == [545, 600]


def test_single_issue_with_and_still_issue_contribution() -> None:
    """单 issue 即使含 '和' 也走 ISSUE_CONTRIBUTION（仅 1 个号）。"""
    intent, slots = classify_intent("#545 和最近的问题")
    assert intent == Intent.ISSUE_CONTRIBUTION
    assert slots.get("issue_number") == 545
