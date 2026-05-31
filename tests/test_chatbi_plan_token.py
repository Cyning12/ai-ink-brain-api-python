"""api.chatbi_plan_token 环境门闸单测。"""

from __future__ import annotations

import pytest

from api.chatbi_plan_token import (
    mint_clarify_plan_bypass_token,
    mint_clarify_text2sql_bypass_token,
    plan_preview_confirm_enabled,
    verify_clarify_plan_bypass_token,
    verify_clarify_text2sql_bypass_token,
)


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


def test_clarify_bypass_token_mint_verify_roundtrip_stable(monkeypatch: pytest.MonkeyPatch) -> None:
    """无填充 urlsafe token 须 100% 可验签（曾用固定 ``+==`` 会在部分长度下偶发失败）。"""
    monkeypatch.setenv("NEXT_PUBLIC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.delenv("CHATBI_PLAN_EXEC_TOKEN_SECRET", raising=False)
    for i in range(256):
        q = f"低置信令牌放行探针{i}"
        for _ in range(8):
            tok = mint_clarify_text2sql_bypass_token(session_id=None, query=q)
            assert verify_clarify_text2sql_bypass_token(tok, session_id=None, query=q)


def test_clarify_plan_bypass_token_rag_roundtrip(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NEXT_PUBLIC_ADMIN_SECRET", "secret-token-1234567890")
    monkeypatch.delenv("CHATBI_PLAN_EXEC_TOKEN_SECRET", raising=False)
    q = "低置信 RAG 令牌探针"
    tok = mint_clarify_plan_bypass_token(session_id="s1", query=q, tool="rag_search")
    assert verify_clarify_plan_bypass_token(tok, session_id="s1", query=q, expected_tool="rag_search")
    assert not verify_clarify_plan_bypass_token(tok, session_id="s1", query=q, expected_tool="text2sql_query")
