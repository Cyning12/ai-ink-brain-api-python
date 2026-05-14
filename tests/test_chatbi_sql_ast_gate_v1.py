"""P1-1：Text2SQL 后闸 SQL AST 硬化（负例 / 正例 / 顺序 / JSON 日志）。"""

from __future__ import annotations

import json
import uuid

import pytest

from api.chatbi_policies import ChatBiTablePolicyRow
from api.chatbi_principal import ChatBiPrincipal
from api.chatbi_sql_gate import ChatBiSqlGateDenied, apply_chatbi_sql_gate


def _super_principal() -> ChatBiPrincipal:
    return ChatBiPrincipal(
        principal_kind="super",
        access_level=0,
        subject_user_id=None,
        token_id=uuid.uuid4(),
    )


def _l2_principal(*, subject: str = "u_demo") -> ChatBiPrincipal:
    return ChatBiPrincipal(
        principal_kind="end_user",
        access_level=2,
        subject_user_id=subject,
        token_id=uuid.uuid4(),
    )


def _portrait_policy() -> dict[tuple[str, str], ChatBiTablePolicyRow]:
    return {
        ("public", "chatbi_user_portrait"): ChatBiTablePolicyRow(
            "public",
            "chatbi_user_portrait",
            min_select_level=2,
            min_insert_level=None,
            min_update_level=2,
            min_delete_level=None,
            owner_column="user_id",
        ),
    }


class TestSqlAstGateNegatives:
    """负例：多语句、禁止 DDL、绕过朴素前缀的恶意等价。"""

    def test_neg_multi_statement_single_semicolon(self) -> None:
        """标题样例：SELECT 1; SELECT 2 — 单分号双语句须被 AST 拦截（非仅靠分号计数）。"""
        p = _super_principal()
        with pytest.raises(ChatBiSqlGateDenied) as ei:
            apply_chatbi_sql_gate("SELECT 1; SELECT 2", principal=p, policies={})
        assert ei.value.rule == "ast_multi_statement"
        assert ei.value.ast_rule_id == "AST_MULTI"

    def test_neg_forbidden_ddl_drop(self) -> None:
        """标题样例：DROP TABLE … — 顶语句 DDL 拒绝。"""
        p = _super_principal()
        with pytest.raises(ChatBiSqlGateDenied) as ei:
            apply_chatbi_sql_gate("DROP TABLE public.agent_info", principal=p, policies={})
        assert ei.value.rule == "ast_forbidden_ddl"
        assert ei.value.ast_rule_id == "AST_FORBIDDEN_DDL"

    def test_neg_comment_prefix_select_was_other(self) -> None:
        """绕过朴素前缀：块注释前缀的 SELECT 不得误判为 unsupported_stmt；应在后续阶段因无表失败。"""
        p = _super_principal()
        with pytest.raises(ChatBiSqlGateDenied) as ei:
            apply_chatbi_sql_gate("/*hint*/select 1", principal=p, policies={})
        assert ei.value.rule == "no_table_resolved"


class TestSqlAstGatePositives:
    """正例：SELECT / 允许的 L2 肖像 UPDATE。"""

    def test_pos_comment_prefix_select_with_table(self) -> None:
        p = _super_principal()
        sql, kind = apply_chatbi_sql_gate(
            "/* ok */ select 1 as n from public.agent_info",
            principal=p,
            policies={},
        )
        assert kind == "select"
        assert "agent_info" in sql.lower()

    def test_pos_l2_portrait_update(self) -> None:
        p = _l2_principal(subject="u_demo")
        pols = _portrait_policy()
        sql, kind = apply_chatbi_sql_gate(
            (
                "UPDATE public.chatbi_user_portrait SET long_term_prompt = 'x', updated_at = now() "
                "WHERE user_id = 'u_demo'"
            ),
            principal=p,
            policies=pols,
        )
        assert kind == "update"
        assert "chatbi_user_portrait" in sql.lower()


class TestSqlAstGatePhaseOrder:
    """顺序：AST → table_allowlist → access_level。"""

    def test_apply_gate_phase_trace_order(self) -> None:
        trace: list[str] = []
        p = _l2_principal()
        pols = {
            ("public", "agent_info"): ChatBiTablePolicyRow(
                "public",
                "agent_info",
                min_select_level=2,
                min_insert_level=None,
                min_update_level=None,
                min_delete_level=None,
                owner_column="user_id",
            ),
        }
        apply_chatbi_sql_gate(
            "select 1 from public.agent_info where user_id = 'u_demo'",
            principal=p,
            policies=pols,
            _phase_trace=trace,
        )
        assert trace == ["ast", "table_allowlist", "access_level"]


class TestSqlAstGateJsonLog:
    """CHATBI_JSON_LOG=1 下 sql_gate_deny 含 ast_rule_id 与 run_id。"""

    def test_sql_gate_deny_json_has_ast_fields(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("CHATBI_JSON_LOG", "1")
        captured: list[dict] = []

        def _cap(**kwargs: object) -> None:
            captured.append(dict(kwargs))

        monkeypatch.setattr("api.chatbi_sql_gate.log_chatbi_record", _cap)

        p = _super_principal()
        with pytest.raises(ChatBiSqlGateDenied):
            apply_chatbi_sql_gate(
                "CREATE TABLE evil (id int)",
                principal=p,
                policies={},
                run_id="run-test-ast",
                request_id="req-test-ast",
            )
        deny_rows = [x for x in captured if x.get("event") == "sql_gate_deny"]
        assert len(deny_rows) == 1
        row = deny_rows[0]
        assert row.get("rule") == "ast_forbidden_ddl"
        assert row.get("ast_rule_id") == "AST_FORBIDDEN_DDL"
        assert row.get("run_id") == "run-test-ast"
        assert row.get("deny_code") == "CHATBI_SQL_DENIED"
        # 可解析为一行 JSON 结构（与 log_chatbi_record 一致）
        json.dumps(row, ensure_ascii=False)
