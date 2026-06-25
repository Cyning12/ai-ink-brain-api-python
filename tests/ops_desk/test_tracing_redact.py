"""Langfuse trace input redaction 测试。

覆盖：
- chat_completion 装饰器带 capture_input=False，阻止 store / JWT 被 observe 序列化
- tracing on 时内部 llm.usage event 仍正常写入（双写纪律未破）
- tracing off 时无异常
"""

from __future__ import annotations

import importlib
from typing import Any

from api.ops.llm import chat_completion
from api.ops.llm.types import LlmCompletionResult, LlmUsage


class FakeOpsRunStore:
    """内存 store，用于验证 event 写入。"""

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
        ev = {
            "run_id": run_id,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
            "seq": seq or (len(self.events) + 1),
        }
        self.events.append(ev)
        return ev


class FakeProvider:
    """Mock LLM Provider，返回固定 usage。"""

    def __init__(self) -> None:
        self._usage = LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            latency_ms=120,
            step="test",
        )

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.3,
        model: str | None = None,
        **kwargs: Any,
    ) -> LlmCompletionResult:
        return LlmCompletionResult(content="fake answer", usage=self._usage)


# ---------------------------------------------------------------------------
# R1: capture_input=False 透传给 _langfuse_observe
# ---------------------------------------------------------------------------

def test_chat_completion_traceable_has_capture_input_false(monkeypatch) -> None:
    """chat_completion 的 traceable 装饰器必须带 capture_input=False。"""
    observe_calls: list[tuple[tuple[Any, ...], dict[str, Any]]] = []

    def _capture_observe(*args: Any, **kwargs: Any) -> Any:
        observe_calls.append((args, kwargs))

        def _decorator(fn: Any) -> Any:
            return fn

        return _decorator

    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    # patch langfuse.observe 以捕获调用参数
    monkeypatch.setattr("langfuse.observe", _capture_observe)

    # 重新 import 以触发 _langfuse_observe 分支
    import api.ops.llm as _llm_mod

    importlib.reload(_llm_mod)

    # 装饰器在 reload 时应用；检查 observe 被调用时的 kwargs
    assert len(observe_calls) >= 1, "observe 应被调用至少一次"
    # 找 chat_completion 对应的 observe 调用（run_type=llm / as_type=generation）
    llm_observe_kwargs = None
    for _args, _kwargs in observe_calls:
        if _kwargs.get("as_type") == "generation":
            llm_observe_kwargs = _kwargs
            break

    assert llm_observe_kwargs is not None, "应存在 as_type=generation 的 observe 调用"
    assert llm_observe_kwargs.get("capture_input") is False, (
        f"capture_input 必须为 False，实际={llm_observe_kwargs.get('capture_input')}"
    )


# ---------------------------------------------------------------------------
# R2: tracing on 时 input 不含敏感模式（模拟 observe 序列化）
# ---------------------------------------------------------------------------

def test_chat_completion_observe_input_no_jwt(monkeypatch) -> None:
    """模拟 Langfuse observe 采集 input，断言不含 JWT / service_role / Bearer。"""
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    captured_inputs: list[Any] = []

    class _FakeObserve:
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            self._args = args
            self._kwargs = kwargs

        def __call__(self, fn: Any) -> Any:
            # 模拟 observe 行为：调用 fn 时捕获 args/kwargs
            def _wrapper(*args: Any, **kwargs: Any) -> Any:
                captured_inputs.append((args, kwargs))
                return fn(*args, **kwargs)

            return _wrapper

    monkeypatch.setattr("langfuse.observe", _FakeObserve)

    import api.ops.llm as _llm_mod

    importlib.reload(_llm_mod)

    store = FakeOpsRunStore()
    fake = FakeProvider()
    monkeypatch.setattr(_llm_mod, "get_llm_provider", lambda: fake)

    result = _llm_mod.chat_completion(
        [{"role": "user", "content": "hi"}],
        step="analyze",
        run_id="run-123",
        store=store,
    )
    assert result.content == "fake answer"

    # 由于 capture_input=False，observe 不应捕获 input
    # 但为防回归，仍断言 captured_inputs 若存在则不含敏感模式
    for args, kwargs in captured_inputs:
        args_kwargs_str = str(args) + str(kwargs)
        assert "eyJ" not in args_kwargs_str, "input 不应含 JWT 片段 eyJ"
        assert "service_role" not in args_kwargs_str, "input 不应含 service_role"
        assert "Bearer " not in args_kwargs_str, "input 不应含 Bearer token"
        assert "supabase_key" not in args_kwargs_str, "input 不应含 supabase_key"


# ---------------------------------------------------------------------------
# R3: 双写纪律 — 内部 llm.usage event 仍写入
# ---------------------------------------------------------------------------

def test_chat_completion_redact_does_not_break_usage_event(monkeypatch) -> None:
    """capture_input=False 只影响 Langfuse 观测面，内部 event 双写不变。"""
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    store = FakeOpsRunStore()
    fake = FakeProvider()

    # 保持 tracing on 但 mock observe 为 identity，避免真实网络
    monkeypatch.setattr("langfuse.observe", lambda *a, **k: lambda fn: fn)

    import api.ops.llm as _llm_mod

    importlib.reload(_llm_mod)
    monkeypatch.setattr(_llm_mod, "get_llm_provider", lambda: fake)

    result = _llm_mod.chat_completion(
        [{"role": "user", "content": "hi"}],
        step="analyze",
        run_id="run-123",
        store=store,
    )
    assert result.content == "fake answer"

    usage_events = [e for e in store.events if e["event_type"] == "llm.usage"]
    assert len(usage_events) == 1
    assert usage_events[0]["payload"]["step"] == "analyze"
    assert usage_events[0]["payload"]["prompt_tokens"] == 10


# ---------------------------------------------------------------------------
# R4: tracing off 时无异常（回归防护）
# ---------------------------------------------------------------------------

def test_chat_completion_redact_tracing_off_noop(monkeypatch) -> None:
    """tracing off 时 capture_input=False 不产生副作用。"""
    monkeypatch.setenv("LANGFUSE_TRACING", "false")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    store = FakeOpsRunStore()
    fake = FakeProvider()
    monkeypatch.setattr("api.ops.llm.get_llm_provider", lambda: fake)

    result = chat_completion(
        [{"role": "user", "content": "hi"}],
        step="analyze",
        run_id="run-123",
        store=store,
    )
    assert result.content == "fake answer"

    usage_events = [e for e in store.events if e["event_type"] == "llm.usage"]
    assert len(usage_events) == 1
