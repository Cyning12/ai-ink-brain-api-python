from __future__ import annotations

import time

import pytest

from api.chatbi_circuit_breaker import (
    CircuitBreaker,
    CircuitBreakerConfig,
    CircuitBreakerOpenError,
    CircuitState,
    reset_all_circuit_breakers_for_tests,
)


@pytest.fixture(autouse=True)
def _reset_breakers():
    reset_all_circuit_breakers_for_tests()
    yield
    reset_all_circuit_breakers_for_tests()


def _cfg(**overrides) -> CircuitBreakerConfig:  # noqa: ANN003
    base = {
        "enabled": True,
        "failure_threshold": 3,
        "recovery_timeout_sec": 0.05,
        "half_open_success_threshold": 1,
    }
    base.update(overrides)
    return CircuitBreakerConfig(**base)


def test_closed_allows_successful_calls():
    br = CircuitBreaker("test", _cfg())
    assert br.execute(lambda: 42) == 42
    assert br.state == CircuitState.CLOSED


def test_failures_transition_to_open():
    br = CircuitBreaker("test", _cfg(failure_threshold=2))

    def _fail() -> None:
        raise RuntimeError("downstream down")

    with pytest.raises(RuntimeError):
        br.execute(_fail)
    assert br.state == CircuitState.CLOSED

    with pytest.raises(RuntimeError):
        br.execute(_fail)
    assert br.state == CircuitState.OPEN


def test_open_fast_fails_without_calling_fn():
    br = CircuitBreaker("test", _cfg(failure_threshold=1))
    calls = {"n": 0}

    def _fail() -> None:
        calls["n"] += 1
        raise RuntimeError("fail")

    with pytest.raises(RuntimeError):
        br.execute(_fail)
    assert br.state == CircuitState.OPEN

    with pytest.raises(CircuitBreakerOpenError) as exc_info:
        br.execute(lambda: calls.__setitem__("n", calls["n"] + 1) or 1)
    assert calls["n"] == 1
    assert exc_info.value.to_error_body()["error_code"] == "CIRCUIT_BREAKER_OPEN"


def test_half_open_recovery_closes_circuit():
    br = CircuitBreaker("test", _cfg(failure_threshold=1, recovery_timeout_sec=0.02))

    with pytest.raises(RuntimeError):
        br.execute(lambda: (_ for _ in ()).throw(RuntimeError("x")))
    assert br.state == CircuitState.OPEN

    time.sleep(0.03)
    assert br.execute(lambda: "ok") == "ok"
    assert br.state == CircuitState.CLOSED


def test_half_open_probe_failure_reopens():
    br = CircuitBreaker("test", _cfg(failure_threshold=1, recovery_timeout_sec=0.02))

    with pytest.raises(RuntimeError):
        br.execute(lambda: (_ for _ in ()).throw(RuntimeError("x")))
    time.sleep(0.03)
    assert br.state == CircuitState.OPEN

    with pytest.raises(RuntimeError):
        br.execute(lambda: (_ for _ in ()).throw(RuntimeError("probe fail")))
    assert br.state == CircuitState.OPEN


def test_open_error_body_fields():
    br = CircuitBreaker("llm", _cfg(failure_threshold=1))
    with pytest.raises(RuntimeError):
        br.execute(lambda: (_ for _ in ()).throw(RuntimeError("x")))
    with pytest.raises(CircuitBreakerOpenError) as exc_info:
        br.execute(lambda: 1)
    body = exc_info.value.to_error_body()
    assert body["circuit_breaker"] == "llm"
    assert body["circuit_state"] == "open"


def test_disabled_breaker_passes_through():
    br = CircuitBreaker("test", _cfg(enabled=False, failure_threshold=1))
    with pytest.raises(RuntimeError):
        br.execute(lambda: (_ for _ in ()).throw(RuntimeError("x")))
    assert br.state == CircuitState.CLOSED
