"""Ops Desk P3-3a · 多 Subagent 编排测试。"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

from api.ops.orchestrator.core import Intent, classify_intent, run_deep
from tests.ops_desk.test_thinking_chain_p2 import FakeQueries, FakeStore


def test_graph_module_intent() -> None:
    intent, slots = classify_intent("kimi-code 的模块依赖图长什么样？")
    assert intent == Intent.GRAPH_MODULE
    assert slots == {}


def test_scan_status_intent() -> None:
    intent, _ = classify_intent("ISSUE_SCAN 扫描状态摘要")
    assert intent == Intent.SCAN_STATUS


@patch("api.ops.orchestrator.core.analyze_graph")
@patch("api.ops.orchestrator.core.synthesize_answer")
def test_run_deep_delegates_graph_analyst(
    mock_synth: MagicMock,
    mock_graph: MagicMock,
) -> None:
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    mock_graph.return_value = {
        "found": True,
        "evidence": [{"kind": "graph_snapshot"}],
        "reasoning": "模块 A 关联 3 个 open issue",
        "suggestion": "优先处理 Read 模块",
        "confidence": 0.8,
        "citations": [],
        "_llm_usage": {"provider": "x", "model": "m", "prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2, "latency_ms": 1},
    }
    mock_synth.return_value = LlmCompletionResult(
        content="Graph 解读完成",
        usage=LlmUsage(provider="x", model="m", prompt_tokens=1, completion_tokens=1, total_tokens=2, latency_ms=1, step="synthesize"),
    )

    store = FakeStore()
    queries = FakeQueries()
    run = store.create_run("模块依赖图？", "deep")
    run_id = str(run["id"])

    result = run_deep(run_id, "模块依赖图？", {}, store, queries, intent=Intent.GRAPH_MODULE)

    assert result["agent"] == "graph_analyst"
    assert result["status"] in ("done", "partial")
    mock_graph.assert_called_once()
    events = store.events[run_id]
    delegate = next(e for e in events if e["event_type"] == "agent.delegate.start")
    assert delegate["payload"]["agent"] == "graph_analyst"


@patch("api.ops.orchestrator.core.analyze_scan")
@patch("api.ops.orchestrator.core.synthesize_answer")
def test_run_deep_delegates_scan_analyst(
    mock_synth: MagicMock,
    mock_scan: MagicMock,
) -> None:
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    mock_scan.return_value = {
        "found": True,
        "evidence": [{"kind": "scan_snapshot", "p0_count": 2}],
        "reasoning": "P0 2 条需关注",
        "suggestion": "先看 P0",
        "confidence": 0.85,
        "citations": [],
        "_llm_usage": {"provider": "x", "model": "m", "prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2, "latency_ms": 1},
    }
    mock_synth.return_value = LlmCompletionResult(
        content="Scan 摘要",
        usage=LlmUsage(provider="x", model="m", prompt_tokens=1, completion_tokens=1, total_tokens=2, latency_ms=1, step="synthesize"),
    )

    store = FakeStore()
    queries = FakeQueries()
    run = store.create_run("scan 状态", "deep")
    run_id = str(run["id"])

    result = run_deep(run_id, "scan 状态", {}, store, queries, intent=Intent.SCAN_STATUS)

    assert result["agent"] == "scan_analyst"
    mock_scan.assert_called_once()
