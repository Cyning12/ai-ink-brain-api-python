"""api.chatbi_plan_token 环境门闸单测。"""

from __future__ import annotations

import pytest

from api.chatbi_plan_token import plan_preview_confirm_enabled


def test_plan_preview_confirm_default_on_when_unset(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("CHATBI_V3_PLAN_PREVIEW_CONFIRM", raising=False)
    assert plan_preview_confirm_enabled() is True


@pytest.mark.parametrize(
    "value",
    ("0", "false", "no", "off", "FALSE", "OFF"),
)
def test_plan_preview_confirm_explicit_off(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("CHATBI_V3_PLAN_PREVIEW_CONFIRM", value)
    assert plan_preview_confirm_enabled() is False


def test_plan_preview_confirm_explicit_on_still_true(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHATBI_V3_PLAN_PREVIEW_CONFIRM", "1")
    assert plan_preview_confirm_enabled() is True
