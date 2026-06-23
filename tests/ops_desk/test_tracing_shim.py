"""Langfuse / LangSmith tracing shim 测试。"""

from __future__ import annotations

from api.ops.tracing import traceable, tracing_enabled, tracing_provider


def test_traceable_noop_when_tracing_off(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    @traceable
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3
    assert tracing_enabled() is False
    assert tracing_provider() == "none"


def test_traceable_with_run_type_when_tracing_off(monkeypatch) -> None:
    monkeypatch.setenv("LANGFUSE_TRACING", "false")
    monkeypatch.setenv("LANGSMITH_TRACING", "false")

    @traceable(run_type="llm")
    def echo(x: str) -> str:
        return x

    assert echo("ok") == "ok"


def test_langfuse_provider_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    assert tracing_provider() == "langfuse"
    assert tracing_enabled() is True
