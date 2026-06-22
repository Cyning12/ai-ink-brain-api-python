"""LangSmith tracing shim 测试。"""

from __future__ import annotations

from api.ops.tracing import traceable, tracing_enabled


def test_traceable_noop_when_tracing_off(monkeypatch) -> None:
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    @traceable
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3
    assert tracing_enabled() is False


def test_traceable_with_run_type_when_tracing_off(monkeypatch) -> None:
    monkeypatch.setenv("LANGSMITH_TRACING", "false")

    @traceable(run_type="llm")
    def echo(x: str) -> str:
        return x

    assert echo("ok") == "ok"
