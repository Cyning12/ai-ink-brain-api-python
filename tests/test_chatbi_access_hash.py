"""chatbi_access_tokens 哈希与闸门单测（无 Supabase）。"""

from __future__ import annotations

import uuid

import pytest

from api.chatbi_access_hash import hash_chatbi_access_token
from api.chatbi_policies import ChatBiTablePolicyRow
from api.chatbi_principal import ChatBiPrincipal
from api.chatbi_sql_gate import ChatBiSqlGateDenied, apply_chatbi_sql_gate


def test_hash_pepper_order(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("CHATBI_ACCESS_TOKEN_PEPPER", "p")
    assert hash_chatbi_access_token("t") == __import__("hashlib").sha256(b"p" + b"t").hexdigest()


def test_gate_l2_join_denied() -> None:
    p = ChatBiPrincipal(
        principal_kind="end_user",
        access_level=2,
        subject_user_id="u1",
        token_id=uuid.uuid4(),
    )
    pols: dict[tuple[str, str], ChatBiTablePolicyRow] = {
        ("public", "a"): ChatBiTablePolicyRow(
            "public",
            "a",
            min_select_level=2,
            min_insert_level=None,
            min_update_level=None,
            min_delete_level=None,
            owner_column="user_id",
        ),
    }
    with pytest.raises(ChatBiSqlGateDenied) as ei:
        apply_chatbi_sql_gate("select * from a join b on 1=1", principal=p, policies=pols)
    assert ei.value.rule == "l2_join_forbidden"


def test_gate_super_select_no_policy_when_policies_empty() -> None:
    p = ChatBiPrincipal(
        principal_kind="super",
        access_level=0,
        subject_user_id=None,
        token_id=uuid.uuid4(),
    )
    sql, kind = apply_chatbi_sql_gate(
        "select 1 as n from public.agent_info",
        principal=p,
        policies={},
    )
    assert kind == "select"
    assert "select" in sql.lower()
