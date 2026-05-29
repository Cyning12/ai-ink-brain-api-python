#!/usr/bin/env python3
"""Harness P1-3：结构化错误响应必填键检查（候选 C）。

与 ``tech_graph_contract_check`` 互补：校验已知错误工厂返回的 JSON shape，
非 SSE 事件白名单。

Usage::

    python tools/harness_structured_error_shape_check.py
    python tools/harness_structured_error_shape_check.py --check  # CI 等价
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "docs" / "harness" / "linters" / "structured_error_registry_v1.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def rate_limit_response_body_sample() -> dict[str, Any]:
    from api.chatbi_rate_limit import rate_limit_response_body

    return rate_limit_response_body(3)


def circuit_breaker_open_error_body_sample() -> dict[str, Any]:
    from api.chatbi_circuit_breaker import CircuitBreakerOpenError, CircuitState

    return CircuitBreakerOpenError(
        breaker_name="llm_outbound",
        state=CircuitState.OPEN,
    ).to_error_body()


_FACTORIES: dict[str, Callable[[], dict[str, Any]]] = {
    "rate_limit_response_body_sample": rate_limit_response_body_sample,
    "circuit_breaker_open_error_body_sample": circuit_breaker_open_error_body_sample,
}


def _load_registry() -> dict[str, Any]:
    raw = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError("registry root must be object")
    return raw


def run_check() -> list[str]:
    registry = _load_registry()
    required = list(registry.get("required_keys") or [])
    if not required:
        return ["registry: required_keys is empty"]

    errors: list[str] = []
    for case in registry.get("cases") or []:
        case_id = case.get("id", "?")
        factory_name = case.get("factory")
        if not factory_name or factory_name not in _FACTORIES:
            errors.append(f"{case_id}: unknown factory {factory_name!r}")
            continue
        body = _FACTORIES[factory_name]()
        if not isinstance(body, dict):
            errors.append(f"{case_id}: factory did not return dict")
            continue
        missing = [k for k in required if k not in body]
        if missing:
            errors.append(f"{case_id}: missing keys {missing} in {sorted(body.keys())}")
        for key in ("error_code", "message"):
            if key in body and body[key] in (None, ""):
                errors.append(f"{case_id}: key {key!r} is empty")
        if "ok" in body and body["ok"] is not False:
            errors.append(f"{case_id}: ok must be False for error body")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Harness structured error shape check")
    parser.add_argument("--check", action="store_true", help="CI mode (non-zero on failure)")
    args = parser.parse_args()

    errors = run_check()
    if errors:
        print("harness_structured_error_shape_check: FAIL")
        for line in errors:
            print(f"  - {line}")
        print(f"registry: {REGISTRY_PATH.relative_to(ROOT)}")
        print("remediation: fix api/ + tests/ or registry; do not bypass linter.")
        sys.exit(1)

    print("harness_structured_error_shape_check: OK")
    if not args.check:
        print(f"registry: {REGISTRY_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
