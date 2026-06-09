"""ChatBI V3 P2-1c：外呼熔断（closed / open / half-open）。"""

from __future__ import annotations

import logging
import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum
from threading import Lock
from typing import Any, TypeVar

logger = logging.getLogger(__name__)

T = TypeVar("T")

_DEFAULT_FAILURE_THRESHOLD = 3
_DEFAULT_RECOVERY_TIMEOUT_SEC = 30.0
_DEFAULT_HALF_OPEN_SUCCESS_THRESHOLD = 1


class CircuitState(str, Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreakerOpenError(RuntimeError):
    """熔断器 open 时快速失败；携带结构化 error_code。"""

    def __init__(self, *, breaker_name: str, state: CircuitState) -> None:
        self.breaker_name = breaker_name
        self.state = state
        super().__init__(f"circuit_breaker_open:{breaker_name}")

    def to_error_body(self) -> dict[str, Any]:
        return {
            "ok": False,
            "error_code": "CIRCUIT_BREAKER_OPEN",
            "message": f"依赖 {self.breaker_name} 暂时不可用（熔断 {self.state.value}）",
            "circuit_breaker": self.breaker_name,
            "circuit_state": self.state.value,
        }


@dataclass(frozen=True)
class CircuitBreakerConfig:
    enabled: bool
    failure_threshold: int
    recovery_timeout_sec: float
    half_open_success_threshold: int


def _parse_bool(raw: str | None, *, default: bool) -> bool:
    if raw is None or not str(raw).strip():
        return default
    val = str(raw).strip().lower()
    if val in {"1", "true", "yes", "on"}:
        return True
    if val in {"0", "false", "no", "off"}:
        return False
    return default


def _parse_positive_int(raw: str | None, *, default: int, field: str) -> int:
    if raw is None or not str(raw).strip():
        return default
    try:
        val = int(str(raw).strip())
    except ValueError:
        logger.warning("chatbi_circuit_breaker: invalid %s=%r, fallback %s", field, raw, default)
        return default
    if val < 1:
        logger.warning("chatbi_circuit_breaker: invalid %s=%s, fallback %s", field, val, default)
        return default
    return val


def _parse_positive_float(raw: str | None, *, default: float, field: str) -> float:
    if raw is None or not str(raw).strip():
        return default
    try:
        val = float(str(raw).strip())
    except ValueError:
        logger.warning("chatbi_circuit_breaker: invalid %s=%r, fallback %s", field, raw, default)
        return default
    if val <= 0:
        logger.warning("chatbi_circuit_breaker: invalid %s=%s, fallback %s", field, val, default)
        return default
    return val


def load_circuit_breaker_config() -> CircuitBreakerConfig:
    enabled = _parse_bool(os.getenv("CHATBI_CIRCUIT_BREAKER_ENABLED"), default=True)
    failure_threshold = _parse_positive_int(
        os.getenv("CHATBI_CB_FAILURE_THRESHOLD"),
        default=_DEFAULT_FAILURE_THRESHOLD,
        field="CHATBI_CB_FAILURE_THRESHOLD",
    )
    recovery_timeout_sec = _parse_positive_float(
        os.getenv("CHATBI_CB_RECOVERY_TIMEOUT_SEC"),
        default=_DEFAULT_RECOVERY_TIMEOUT_SEC,
        field="CHATBI_CB_RECOVERY_TIMEOUT_SEC",
    )
    half_open_success_threshold = _parse_positive_int(
        os.getenv("CHATBI_CB_HALF_OPEN_SUCCESS_THRESHOLD"),
        default=_DEFAULT_HALF_OPEN_SUCCESS_THRESHOLD,
        field="CHATBI_CB_HALF_OPEN_SUCCESS_THRESHOLD",
    )
    return CircuitBreakerConfig(
        enabled=enabled,
        failure_threshold=failure_threshold,
        recovery_timeout_sec=recovery_timeout_sec,
        half_open_success_threshold=half_open_success_threshold,
    )


class CircuitBreaker:
    def __init__(self, name: str, config: CircuitBreakerConfig | None = None) -> None:
        self.name = name
        self._config = config or load_circuit_breaker_config()
        self._lock = Lock()
        self._state = CircuitState.CLOSED
        self._consecutive_failures = 0
        self._half_open_successes = 0
        self._opened_at: float | None = None

    @property
    def state(self) -> CircuitState:
        with self._lock:
            return self._state

    def reset_for_tests(self) -> None:
        with self._lock:
            self._state = CircuitState.CLOSED
            self._consecutive_failures = 0
            self._half_open_successes = 0
            self._opened_at = None

    def _transition(self, new_state: CircuitState, *, reason: str) -> None:
        if self._state == new_state:
            return
        old = self._state
        self._state = new_state
        logger.warning(
            "chatbi_circuit_breaker: %s %s -> %s (%s)",
            self.name,
            old.value,
            new_state.value,
            reason,
        )

    def _maybe_enter_half_open(self) -> None:
        if self._state != CircuitState.OPEN or self._opened_at is None:
            return
        elapsed = time.monotonic() - self._opened_at
        if elapsed >= self._config.recovery_timeout_sec:
            self._half_open_successes = 0
            self._transition(CircuitState.HALF_OPEN, reason="recovery_timeout_elapsed")

    def execute(self, fn: Callable[[], T]) -> T:
        if not self._config.enabled:
            return fn()

        with self._lock:
            self._maybe_enter_half_open()
            if self._state == CircuitState.OPEN:
                raise CircuitBreakerOpenError(breaker_name=self.name, state=self._state)

        try:
            result = fn()
        except Exception:
            self._record_failure()
            raise

        self._record_success()
        return result

    def _record_failure(self) -> None:
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._consecutive_failures = self._config.failure_threshold
                self._opened_at = time.monotonic()
                self._transition(CircuitState.OPEN, reason="half_open_probe_failed")
                return
            self._consecutive_failures += 1
            if self._consecutive_failures >= self._config.failure_threshold:
                self._opened_at = time.monotonic()
                self._transition(CircuitState.OPEN, reason="failure_threshold_reached")

    def _record_success(self) -> None:
        with self._lock:
            if self._state == CircuitState.HALF_OPEN:
                self._half_open_successes += 1
                if self._half_open_successes >= self._config.half_open_success_threshold:
                    self._consecutive_failures = 0
                    self._opened_at = None
                    self._transition(CircuitState.CLOSED, reason="half_open_probe_succeeded")
                return
            self._consecutive_failures = 0
            if self._state != CircuitState.CLOSED:
                self._opened_at = None
                self._transition(CircuitState.CLOSED, reason="call_succeeded")


_breakers: dict[str, CircuitBreaker] = {}
_breakers_lock = Lock()


def get_circuit_breaker(name: str) -> CircuitBreaker:
    with _breakers_lock:
        br = _breakers.get(name)
        if br is None:
            br = CircuitBreaker(name)
            _breakers[name] = br
        return br


def reset_all_circuit_breakers_for_tests() -> None:
    with _breakers_lock:
        for br in _breakers.values():
            br.reset_for_tests()


def execute_with_circuit_breaker(name: str, fn: Callable[[], T]) -> T:
    return get_circuit_breaker(name).execute(fn)
