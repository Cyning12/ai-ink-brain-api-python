"""P0-4: Ops Chat Tracing 单测。

覆盖：
- 未设置 OPS_CHAT_TRACER 时 tracing 为空操作。
- OPS_CHAT_TRACER=langfuse / langsmith 时能创建 span（mock client，不依赖真实密钥）。
- run_deep / run_react_fallback 调用后产生 trace span（mock）。
- trace 元数据含 run_id / session_id / agent_role。
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import Any

import pytest


# -----------------------------------------------------------------------------
# 基础 tracer 行为
# -----------------------------------------------------------------------------


def test_tracing_provider_default_is_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """未设置 OPS_CHAT_TRACER 且旧 env 也关闭时 provider 为 none。"""
    from api.ops.tracing import tracing_enabled, tracing_provider

    monkeypatch.delenv("OPS_CHAT_TRACER", raising=False)
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    assert tracing_provider() == "none"
    assert tracing_enabled() is False


def test_tracing_provider_unknown_ops_chat_tracer_is_none(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OPS_CHAT_TRACER 为未知值时不应启用 tracing。"""
    from api.ops.tracing import tracing_provider

    monkeypatch.setenv("OPS_CHAT_TRACER", "zipkin")
    assert tracing_provider() == "none"


def test_tracing_provider_langfuse_via_ops_chat_tracer(monkeypatch: pytest.MonkeyPatch) -> None:
    """OPS_CHAT_TRACER=langfuse 时直接启用 langfuse，无需 LANGFUSE_TRACING。"""
    from api.ops.tracing import tracing_enabled, tracing_provider

    monkeypatch.setenv("OPS_CHAT_TRACER", "langfuse")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    assert tracing_provider() == "langfuse"
    assert tracing_enabled() is True


def test_tracing_provider_langsmith_via_ops_chat_tracer(monkeypatch: pytest.MonkeyPatch) -> None:
    """OPS_CHAT_TRACER=langsmith 时直接启用 langsmith。"""
    from api.ops.tracing import tracing_enabled, tracing_provider

    monkeypatch.setenv("OPS_CHAT_TRACER", "langsmith")
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)

    assert tracing_provider() == "langsmith"
    assert tracing_enabled() is True


def test_traceable_noop_when_tracing_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """未开启 tracing 时 @traceable 透传原函数。"""
    from api.ops.tracing import traceable

    monkeypatch.delenv("OPS_CHAT_TRACER", raising=False)
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    @traceable
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3


def test_trace_span_noop_when_tracing_off(monkeypatch: pytest.MonkeyPatch) -> None:
    """未开启 tracing 时 trace_span 上下文管理器零成本。"""
    from api.ops.tracing import trace_span

    monkeypatch.delenv("OPS_CHAT_TRACER", raising=False)
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    with trace_span("noop_span", run_id="run-1"):
        result = 42
    assert result == 42


# -----------------------------------------------------------------------------
# OPS_CHAT_TRACER=langfuse 时 span 创建（mock）
# -----------------------------------------------------------------------------


class FakeLangfuseObserve:
    """记录 langfuse.observe 的调用与装饰行为，不触发网络。"""

    def __init__(self) -> None:
        self.calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []
        self.decorated: list[Callable[..., Any]] = []

    def __call__(self, *args: Any, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
        self.calls.append((args, kwargs))

        def _decorator(fn: Callable[..., Any]) -> Callable[..., Any]:
            self.decorated.append(fn)
            return fn

        return _decorator


class FakeUpdateCurrentSpanMetadata:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(self, metadata: dict[str, Any]) -> None:
        self.calls.append(metadata)


def test_trace_span_langfuse_creates_span_with_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OPS_CHAT_TRACER=langfuse 时 trace_span 调用 langfuse.observe 并写入 metadata。"""
    from api.ops import tracing as tracing_module
    from api.ops.tracing import trace_span

    monkeypatch.setenv("OPS_CHAT_TRACER", "langfuse")

    fake_observe = FakeLangfuseObserve()
    fake_update = FakeUpdateCurrentSpanMetadata()
    monkeypatch.setattr("langfuse.observe", fake_observe)
    monkeypatch.setattr(tracing_module, "update_current_span_metadata", fake_update)

    with trace_span(
        "review",
        run_type="tool",
        run_id="run-123",
        session_id="sess-abc",
        agent_role="deep",
        verdict="pass",
    ):
        pass

    assert len(fake_observe.calls) == 1
    _args, kwargs = fake_observe.calls[0]
    assert kwargs.get("name") == "review"
    assert kwargs.get("as_type") == "tool"
    assert kwargs.get("capture_input") is False
    assert kwargs.get("capture_output") is False

    # generator 启动时会调用 update_current_span_metadata 写入 metadata
    assert len(fake_update.calls) == 1
    assert fake_update.calls[0] == {
        "run_id": "run-123",
        "session_id": "sess-abc",
        "agent_role": "deep",
        "verdict": "pass",
    }


# -----------------------------------------------------------------------------
# OPS_CHAT_TRACER=langsmith 时 span 创建（mock）
# -----------------------------------------------------------------------------


class FakeLangsmithTrace:
    """模拟 langsmith.trace 上下文管理器，记录调用参数。"""

    def __init__(self) -> None:
        self.calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    @contextmanager
    def __call__(self, *args: Any, **kwargs: Any) -> Iterator[Any]:
        self.calls.append((args, kwargs))
        yield None


def test_trace_span_langsmith_creates_span_with_metadata(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """OPS_CHAT_TRACER=langsmith 时 trace_span 调用 langsmith.trace 并传入 metadata。"""
    from api.ops.tracing import trace_span

    monkeypatch.setenv("OPS_CHAT_TRACER", "langsmith")
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)

    fake_trace = FakeLangsmithTrace()
    monkeypatch.setattr("langsmith.trace", fake_trace)

    with trace_span(
        "handoff",
        run_type="tool",
        run_id="run-456",
        session_id="sess-xyz",
        agent_role="react",
    ):
        pass

    assert len(fake_trace.calls) == 1
    _args, kwargs = fake_trace.calls[0]
    assert kwargs.get("name") == "handoff"
    assert kwargs.get("run_type") == "tool"
    assert kwargs.get("metadata") == {
        "run_id": "run-456",
        "session_id": "sess-xyz",
        "agent_role": "react",
    }


# -----------------------------------------------------------------------------
# run_deep / run_react_fallback 调用后产生 trace span（mock）
# -----------------------------------------------------------------------------


class FakeTracingStore:
    """内存版 OpsRunStore，支持 run_deep / run_react_fallback 所需接口。"""

    def __init__(self) -> None:
        self.runs: dict[str, dict[str, Any]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {}
        self._counter = 0

    def create_run(
        self,
        query: str,
        route: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        self._counter += 1
        run_id = f"run-{self._counter}"
        self.runs[run_id] = {
            "id": run_id,
            "query": query,
            "route": route,
            "session_id": session_id,
        }
        self.events[run_id] = []
        return self.runs[run_id]

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
            "seq": seq or len(self.events.get(run_id, [])) + 1,
        }
        self.events.setdefault(run_id, []).append(evt)
        return evt

    def list_runs_by_session_id(self, session_id: str, *, limit: int = 50) -> list[dict[str, Any]]:
        runs = [r for r in self.runs.values() if r.get("session_id") == session_id]
        return sorted(runs, key=lambda r: r["id"], reverse=True)[:limit]

    def get_events(self, run_id: str, after_seq: int = 0, limit: int = 200) -> list[dict[str, Any]]:
        return [e for e in self.events.get(run_id, []) if e["seq"] > after_seq][:limit]

    def update_run(self, run_id: str, **fields: Any) -> None:
        if run_id in self.runs:
            self.runs[run_id].update(fields)

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        if run_id in self.runs:
            self.runs[run_id]["metrics_json"] = metrics_json


class FakeTracingQueries:
    """最小 Queries 假对象，支持 issue #123。"""

    def __init__(self) -> None:
        self.issues: dict[int, dict[str, Any]] = {
            123: {
                "number": 123,
                "title": "Demo issue",
                "state": "open",
                "labels": ["bug"],
                "html_url": "https://github.com/MoonshotAI/kimi-code/issues/123",
            },
        }

    def fetch_issue_by_number(self, number: int) -> dict[str, Any] | None:
        return self.issues.get(number)


@pytest.fixture
def fake_tracing_store() -> FakeTracingStore:
    return FakeTracingStore()


@contextmanager
def _record_trace_span(
    calls: list[dict[str, Any]],
    name: str,
    *,
    run_type: str | None = None,
    **metadata: Any,
) -> Iterator[None]:
    calls.append({"name": name, "run_type": run_type, "metadata": metadata})
    yield None


def test_run_deep_records_trace_span_metadata(
    monkeypatch: pytest.MonkeyPatch,
    fake_tracing_store: FakeTracingStore,
) -> None:
    """run_deep 调用后，trace_span 与 update_current_span_metadata 均记录 run_id/session_id/agent_role。"""
    from api.ops.orchestrator import core as orchestrator_core
    from api.ops.orchestrator.core import run_deep
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    span_calls: list[dict[str, Any]] = []
    metadata_calls: list[dict[str, Any]] = []

    def fake_update(metadata: dict[str, Any]) -> None:
        metadata_calls.append(metadata)

    monkeypatch.setattr(orchestrator_core, "trace_span", lambda name, *, run_type=None, **metadata: _record_trace_span(span_calls, name, run_type=run_type, **metadata))
    monkeypatch.setattr(orchestrator_core, "update_current_span_metadata", fake_update)

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return LlmCompletionResult(
            content='{"reasoning": "适合", "suggestion": "适合", "confidence": 0.9, "citations": []}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "analyze"),
            ),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> LlmCompletionResult:
        return LlmCompletionResult(
            content="综合建议：适合新手。",
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=8,
                completion_tokens=4,
                total_tokens=12,
                latency_ms=80,
                step="synthesize",
            ),
        )

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    queries = FakeTracingQueries()
    run = fake_tracing_store.create_run(query="#123 适合吗", route="deep", session_id="sess-deep")
    result = run_deep(
        run["id"],
        "#123 适合吗",
        {"issue_number": 123},
        fake_tracing_store,  # type: ignore[arg-type]
        queries,  # type: ignore[arg-type]
        session_id="sess-deep",
    )

    assert result["run_id"] == run["id"]

    # update_current_span_metadata 在入口被调用一次
    assert len(metadata_calls) >= 1
    assert metadata_calls[0]["run_id"] == run["id"]
    assert metadata_calls[0]["session_id"] == "sess-deep"
    assert metadata_calls[0]["agent_role"] == "deep"

    # trace_span 至少包含 handoff 与 review
    span_names = [c["name"] for c in span_calls]
    assert "handoff" in span_names
    assert "review" in span_names

    handoff_call = next(c for c in span_calls if c["name"] == "handoff")
    assert handoff_call["metadata"]["run_id"] == run["id"]
    assert handoff_call["metadata"]["session_id"] == "sess-deep"
    assert handoff_call["metadata"]["agent_role"] == "deep"

    review_call = next(c for c in span_calls if c["name"] == "review")
    assert review_call["metadata"]["run_id"] == run["id"]
    assert review_call["metadata"]["session_id"] == "sess-deep"
    assert review_call["metadata"]["agent_role"] == "deep"
    assert "verdict" in review_call["metadata"]


def test_run_react_fallback_records_trace_span_metadata(
    monkeypatch: pytest.MonkeyPatch,
    fake_tracing_store: FakeTracingStore,
) -> None:
    """run_react_fallback 调用后，trace span 元数据含 run_id/session_id/agent_role。"""
    from api.ops import react_loop as react_module
    from api.ops.react_loop import run_react_fallback
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    span_calls: list[dict[str, Any]] = []
    metadata_calls: list[dict[str, Any]] = []

    def fake_update(metadata: dict[str, Any]) -> None:
        metadata_calls.append(metadata)

    monkeypatch.setattr(react_module, "trace_span", lambda name, *, run_type=None, **metadata: _record_trace_span(span_calls, name, run_type=run_type, **metadata))
    monkeypatch.setattr(react_module, "update_current_span_metadata", fake_update)

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> LlmCompletionResult:
        return LlmCompletionResult(
            content='{"thought": "直接回答", "final_answer": "#123 是 bug。"}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "react"),
            ),
        )

    monkeypatch.setattr("api.ops.react_loop.chat_completion", fake_chat_completion)

    queries = FakeTracingQueries()
    run = fake_tracing_store.create_run(query="#123 状态", route="react", session_id="sess-react")
    result = run_react_fallback(
        run["id"],
        "#123 状态",
        fake_tracing_store,  # type: ignore[arg-type]
        queries,  # type: ignore[arg-type]
        session_id="sess-react",
    )

    assert result["run_id"] == run["id"]

    assert len(metadata_calls) >= 1
    assert metadata_calls[0]["run_id"] == run["id"]
    assert metadata_calls[0]["session_id"] == "sess-react"
    assert metadata_calls[0]["agent_role"] == "react"

    span_names = [c["name"] for c in span_calls]
    assert "handoff" in span_names
    assert "review" in span_names

    handoff_call = next(c for c in span_calls if c["name"] == "handoff")
    assert handoff_call["metadata"]["run_id"] == run["id"]
    assert handoff_call["metadata"]["session_id"] == "sess-react"
    assert handoff_call["metadata"]["agent_role"] == "react"

    review_call = next(c for c in span_calls if c["name"] == "review")
    assert review_call["metadata"]["run_id"] == run["id"]
    assert review_call["metadata"]["session_id"] == "sess-react"
    assert review_call["metadata"]["agent_role"] == "react"


# -----------------------------------------------------------------------------
# 向后兼容：旧 LANGFUSE_TRACING/LANGSMITH_TRACING 仍生效
# -----------------------------------------------------------------------------


def test_tracing_provider_langfuse_via_legacy_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """未设置 OPS_CHAT_TRACER 但旧 LANGFUSE_TRACING 配置完整时仍启用 langfuse。"""
    from api.ops.tracing import tracing_provider

    monkeypatch.delenv("OPS_CHAT_TRACER", raising=False)
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    assert tracing_provider() == "langfuse"


def test_tracing_provider_langsmith_via_legacy_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """未设置 OPS_CHAT_TRACER 但旧 LANGSMITH_TRACING=true 时仍启用 langsmith。"""
    from api.ops.tracing import tracing_provider

    monkeypatch.delenv("OPS_CHAT_TRACER", raising=False)
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.setenv("LANGSMITH_TRACING", "true")

    assert tracing_provider() == "langsmith"
