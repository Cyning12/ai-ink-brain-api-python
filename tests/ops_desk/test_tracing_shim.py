"""Langfuse / LangSmith tracing shim 测试。"""

from __future__ import annotations

from api.ops.tracing import (
    traceable,
    tracing_enabled,
    tracing_provider,
    update_current_span_metadata,
)


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


def test_traceable_with_capture_options_when_tracing_off(monkeypatch) -> None:
    """capture_input/capture_output 透传给底层 observe；关闭时仍为 no-op。"""
    monkeypatch.setenv("LANGFUSE_TRACING", "false")
    monkeypatch.setenv("LANGSMITH_TRACING", "false")

    @traceable(capture_input=False, capture_output=False)
    def identity(x: str) -> str:
        return x

    assert identity("hidden") == "hidden"


def test_update_current_span_metadata_noop_when_tracing_off(monkeypatch) -> None:
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    # 不应抛出，也不应改变 provider
    update_current_span_metadata({"ops_run_id": "run-123", "route": "deep"})
    assert tracing_provider() == "none"


def test_langfuse_provider_when_configured(monkeypatch) -> None:
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    assert tracing_provider() == "langfuse"
    assert tracing_enabled() is True


def test_langfuse_provider_missing_secret_key_is_noop(monkeypatch) -> None:
    """仅有 PUBLIC_KEY 没有 SECRET_KEY 时不应启用 langfuse。"""
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.delenv("LANGFUSE_SECRET_KEY", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    assert tracing_provider() == "none"


def test_langfuse_provider_respects_base_url(monkeypatch) -> None:
    """BASE_URL 透传：配置完整时 provider 为 langfuse（不校验可达性）。"""
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-lf-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-lf-test")
    monkeypatch.setenv("LANGFUSE_BASE_URL", "https://jp.cloud.langfuse.com")
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    assert tracing_provider() == "langfuse"
    assert tracing_enabled() is True
