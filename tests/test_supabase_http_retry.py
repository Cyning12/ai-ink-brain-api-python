"""Supabase HTTP 客户端：可重试网络错误判定与重试循环。"""

from __future__ import annotations

import errno

import pytest

from api.rag_env import supabase_execute_with_retry, transient_supabase_network_error


def test_transient_oserror_connreset() -> None:
    exc = OSError(errno.ECONNRESET, "Connection reset by peer")
    assert transient_supabase_network_error(exc) is True


def test_transient_errno_54_macos_style() -> None:
    exc = OSError(54, "Connection reset by peer")
    assert transient_supabase_network_error(exc) is True


def test_transient_message_connection_reset() -> None:
    class E(Exception):
        pass

    assert transient_supabase_network_error(E("[Errno 54] Connection reset by peer")) is True


def test_non_transient_value_error() -> None:
    assert transient_supabase_network_error(ValueError("bad payload")) is False


def test_supabase_execute_with_retry_succeeds_second_call(monkeypatch) -> None:
    monkeypatch.setenv("SUPABASE_HTTP_RETRIES", "4")
    monkeypatch.setenv("SUPABASE_HTTP_RETRY_BASE_DELAY_S", "0")
    calls = {"n": 0}

    def fn() -> int:
        calls["n"] += 1
        if calls["n"] < 2:
            raise OSError(errno.ECONNRESET, "reset")
        return 42

    assert supabase_execute_with_retry(fn) == 42
    assert calls["n"] == 2


def test_supabase_execute_with_retry_raises_when_not_transient(monkeypatch) -> None:
    monkeypatch.setenv("SUPABASE_HTTP_RETRIES", "3")
    monkeypatch.setenv("SUPABASE_HTTP_RETRY_BASE_DELAY_S", "0")

    def fn() -> None:
        raise ValueError("schema")

    with pytest.raises(ValueError, match="schema"):
        supabase_execute_with_retry(fn)
