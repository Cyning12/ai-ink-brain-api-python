"""P1-2 FP-1：Unified 非流式错误 envelope 契约（与 task §5 写死一致；不含 guard 实现）。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "chatbi" / "prompt_guard_fp1_unified_chat_error_envelope.json"


def test_fp1_golden_fixture_matches_unified_error_envelope_contract() -> None:
    data = json.loads(_FIXTURE.read_text(encoding="utf-8"))
    assert data.get("ok") is False
    assert isinstance(data.get("run_id"), str) and data["run_id"]
    assert "session_id" in data
    assert isinstance(data.get("mode"), str) and data["mode"]
    events = data.get("events")
    assert isinstance(events, list) and events
    err = next((e for e in events if isinstance(e, dict) and e.get("type") == "error"), None)
    assert err is not None
    payload = err.get("payload")
    assert isinstance(payload, dict)
    assert isinstance(payload.get("stage"), str) and payload["stage"]
    assert isinstance(payload.get("message"), str) and payload["message"]
