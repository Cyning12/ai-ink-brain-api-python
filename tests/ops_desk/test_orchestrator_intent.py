"""Orchestrator 意图分类（中文 metrics 问句）。"""

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
