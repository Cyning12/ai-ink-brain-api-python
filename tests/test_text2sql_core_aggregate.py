"""text2sql_core：确定性聚合总结（Agent / API 共用）。"""
from __future__ import annotations

from api.text2sql_core import try_summarize_aggregate


def test_try_summarize_aggregate_count() -> None:
    assert try_summarize_aggregate("有多少条", ["count"], [{"count": 3}]) == "共有 3 条。"


def test_try_summarize_aggregate_non_aggregate_returns_none() -> None:
    assert try_summarize_aggregate("q", ["a", "b"], [{"a": 1, "b": 2}]) is None
