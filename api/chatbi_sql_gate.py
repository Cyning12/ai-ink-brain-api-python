"""ChatBI Text2SQL 后闸：AST/正则 + 表策略 + access_level（OpenItems §1.4 / §1.5）。"""

from __future__ import annotations

import hashlib
import re
from typing import Literal

import sqlparse

from .chatbi_json_log import chatbi_json_log_enabled, log_chatbi_record
from .chatbi_policies import ChatBiTablePolicyRow, allowed_op
from .chatbi_principal import ChatBiPrincipal

StmtKind = Literal["select", "update", "insert", "delete", "truncate", "other"]


class ChatBiSqlGateDenied(Exception):
    """越权 SQL；HTTP 层映射为 403 + 结构化 body。"""

    def __init__(
        self,
        *,
        deny_code: str,
        rule: str,
        message_zh: str = "您无此权限",
        access_level: int | None = None,
        target_table: str | None = None,
        stmt_class: str | None = None,
    ) -> None:
        super().__init__(message_zh)
        self.deny_code = deny_code
        self.rule = rule
        self.message_zh = message_zh
        self.access_level = access_level
        self.target_table = target_table
        self.stmt_class = stmt_class


def _strip_md_fences(sql_raw: str) -> str:
    s = (sql_raw or "").strip()
    s = re.sub(r"^```sql\s*", "", s, flags=re.IGNORECASE).strip()
    s = re.sub(r"^```\s*", "", s).strip()
    s = re.sub(r"```$", "", s).strip()
    return s


def normalize_single_sql(sql_raw: str) -> str:
    """去围栏、单语句、去尾分号。"""
    s = _strip_md_fences(sql_raw)
    if not s:
        raise ChatBiSqlGateDenied(deny_code="CHATBI_SQL_DENIED", rule="empty_sql", stmt_class="other")
    if s.count(";") > 1:
        raise ChatBiSqlGateDenied(deny_code="CHATBI_SQL_DENIED", rule="multi_statement", stmt_class="other")
    s = s.rstrip(";").strip()
    return s


def _classify_stmt(sql: str) -> StmtKind:
    low = re.sub(r"\s+", " ", sql.strip()).lower()
    if low.startswith("select") or low.startswith("with "):
        return "select"
    if low.startswith("update"):
        return "update"
    if low.startswith("insert"):
        return "insert"
    if low.startswith("delete"):
        return "delete"
    if low.startswith("truncate"):
        return "truncate"
    return "other"


def _forbidden_ddl_dml(sql: str) -> str | None:
    low = re.sub(r"\s+", " ", sql.lower())
    for kw in (
        "create ",
        "alter ",
        "drop ",
        "grant ",
        "revoke ",
        "merge ",
        "call ",
        "execute ",
    ):
        if kw in low:
            return kw.strip()
    return None


def _has_join(sql: str) -> bool:
    for st in sqlparse.parse(sql):
        txt = str(st).lower()
        if re.search(r"\bjoin\b", txt):
            return True
    return False


def _iter_physical_tables(sql: str) -> list[tuple[str, str]]:
    """从 FROM/JOIN/UPDATE/INSERT INTO/DELETE FROM 抽取 (schema, table) 小写。"""
    out: list[tuple[str, str]] = []
    s = sqlparse.format(sql, strip_comments=True)
    for m in re.finditer(
        r"(?is)\b(?:from|join|update)\s+(?:only\s+)?(?:(\"?)([a-z0-9_]+)\1\.)?(\"?)([a-z0-9_]+)\3",
        s,
    ):
        sch = (m.group(2) or "public").lower()
        tbl = (m.group(4) or "").lower()
        if tbl:
            out.append((sch, tbl))
    for m in re.finditer(
        r"(?is)\binsert\s+into\s+(?:(\"?)([a-z0-9_]+)\1\.)?(\"?)([a-z0-9_]+)\3",
        s,
    ):
        sch = (m.group(2) or "public").lower()
        tbl = (m.group(4) or "").lower()
        if tbl:
            out.append((sch, tbl))
    dm = re.search(r"(?is)\bdelete\s+from\s+(?:(\"?)([a-z0-9_]+)\1\.)?(\"?)([a-z0-9_]+)\3", s)
    if dm:
        sch = (dm.group(2) or "public").lower()
        tbl = (dm.group(4) or "").lower()
        if tbl:
            out.append((sch, tbl))
    tm = re.search(r"(?is)\btruncate\s+(?:table\s+)?(?:(\"?)([a-z0-9_]+)\1\.)?(\"?)([a-z0-9_]+)\3", s)
    if tm:
        sch = (tm.group(2) or "public").lower()
        tbl = (tm.group(4) or "").lower()
        if tbl:
            out.append((sch, tbl))
    # 去重保序
    seen: set[tuple[str, str]] = set()
    uniq: list[tuple[str, str]] = []
    for t in out:
        if t not in seen:
            seen.add(t)
            uniq.append(t)
    return uniq


def _sql_fingerprint(sql: str) -> str:
    return hashlib.sha256(re.sub(r"\s+", " ", sql).encode("utf-8", errors="ignore")).hexdigest()[:16]


def _log_deny(
    *,
    principal: ChatBiPrincipal,
    deny: ChatBiSqlGateDenied,
    run_id: str | None,
    request_id: str | None,
    sql: str,
) -> None:
    if not chatbi_json_log_enabled():
        return
    log_chatbi_record(
        message="sql_gate_deny",
        event="sql_gate_deny",
        deny_code=deny.deny_code,
        access_level=principal.access_level,
        target_table=deny.target_table,
        stmt_class=deny.stmt_class,
        rule=deny.rule,
        request_id=request_id,
        run_id=run_id,
        sql_fp=_sql_fingerprint(sql),
    )


def filter_text2sql_retrieved(
    retrieved: list[dict],
    *,
    principal: ChatBiPrincipal,
    policies: dict[tuple[str, str], ChatBiTablePolicyRow],
) -> list[dict]:
    """前闸：仅保留策略允许 SELECT 的 DDL 片段。若 `policies` 为空则不做裁剪（本地/CI 无策略表时的引导模式）。"""

    if not policies:
        return retrieved

    def _ddl_table_name(doc: dict) -> str | None:
        t = doc.get("title")
        if not isinstance(t, str) or not t.lower().startswith("ddl:"):
            return None
        name = t.split(":", 1)[1].strip().lower()
        return name or None

    out: list[dict] = []
    for r in retrieved:
        if r.get("doc_type") != "ddl":
            out.append(r)
            continue
        tn = _ddl_table_name(r)
        if not tn:
            out.append(r)
            continue
        key = ("public", tn)
        pol = policies.get(key)
        if pol is None:
            if principal.access_level == 0:
                out.append(r)
            continue
        if allowed_op(access_level=principal.access_level, min_level=pol.min_select_level):
            out.append(r)
    return out


_L2_PORTRAIT = ("public", "chatbi_user_portrait")
_L2_UPDATEABLE_COLS = frozenset({"long_term_prompt", "updated_at"})


def _parse_update_target(sql: str) -> tuple[str, str] | None:
    m = re.match(
        r"(?is)\s*update\s+(?:only\s+)?(?:(\"?)([a-z0-9_]+)\1\.)?(\"?)([a-z0-9_]+)\3",
        sql.strip(),
    )
    if not m:
        return None
    sch = (m.group(2) or "public").lower()
    tbl = (m.group(4) or "").lower()
    return (sch, tbl)


def _l2_portrait_update_ok(sql: str, principal: ChatBiPrincipal) -> bool:
    tgt = _parse_update_target(sql)
    if tgt != _L2_PORTRAIT:
        return False
    mset = re.search(r"(?is)\bset\s+(.+)$", sql)
    if not mset:
        return False
    set_clause = mset.group(1)
    set_clause = re.split(r"(?is)\bwhere\b", set_clause, maxsplit=1)[0]
    for part in set_clause.split(","):
        pm = re.match(r"(?is)\s*([a-z0-9_]+)\s*=", part)
        if not pm:
            continue
        col = pm.group(1).lower()
        if col not in _L2_UPDATEABLE_COLS:
            return False
    wh = re.search(r"(?is)\bwhere\b(.+)$", sql)
    if not wh:
        return False
    sid = (principal.subject_user_id or "").strip()
    if not sid:
        return False
    rest = wh.group(1)
    if not re.search(r"(?is)\buser_id\s*=\s*'[^']*'", rest) and not re.search(r"(?is)\buser_id\s*=\s*[^;\s]+", rest):
        return False
    # 字面量须包含 subject（防改他人行）
    if sid not in rest:
        return False
    return True


def apply_chatbi_sql_gate(
    sql_raw: str,
    *,
    principal: ChatBiPrincipal,
    policies: dict[tuple[str, str], ChatBiTablePolicyRow],
    run_id: str | None = None,
    request_id: str | None = None,
) -> tuple[str, Literal["select", "update", "insert"]]:
    """返回 (规范化 SQL, 语句类)；拒绝时抛 ChatBiSqlGateDenied 并写 JSON 日志。"""
    sql = normalize_single_sql(sql_raw)
    bad = _forbidden_ddl_dml(sql)
    if bad:
        d = ChatBiSqlGateDenied(
            deny_code="CHATBI_SQL_DENIED",
            rule="ddl_forbidden",
            stmt_class="other",
            access_level=principal.access_level,
        )
        _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
        raise d

    kind = _classify_stmt(sql)
    if kind == "other":
        d = ChatBiSqlGateDenied(
            deny_code="CHATBI_SQL_DENIED",
            rule="unsupported_stmt",
            stmt_class="other",
            access_level=principal.access_level,
        )
        _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
        raise d

    tables = _iter_physical_tables(sql)
    if not tables:
        d = ChatBiSqlGateDenied(
            deny_code="CHATBI_SQL_DENIED",
            rule="no_table_resolved",
            stmt_class=kind,
            access_level=principal.access_level,
        )
        _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
        raise d

    if principal.access_level == 2 and _has_join(sql):
        d = ChatBiSqlGateDenied(
            deny_code="CHATBI_SQL_DENIED",
            rule="l2_join_forbidden",
            stmt_class="select" if kind == "select" else kind,
            access_level=2,
        )
        _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
        raise d

    # Text2SQL 本路径不执行物理 DELETE/TRUNCATE（Admin 禁令 + 执行面收口）
    if kind in ("delete", "truncate"):
        d = ChatBiSqlGateDenied(
            deny_code="CHATBI_SQL_DENIED",
            rule="physical_delete_trunc_text2sql_forbidden",
            stmt_class=kind,
            access_level=principal.access_level,
            target_table=tables[0][1] if tables else None,
        )
        _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
        raise d

    if kind == "insert" and principal.access_level == 2:
        d = ChatBiSqlGateDenied(
            deny_code="CHATBI_SQL_DENIED",
            rule="l2_insert_forbidden",
            stmt_class="insert",
            access_level=2,
        )
        _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
        raise d

    if kind == "update" and principal.access_level == 2:
        if not _l2_portrait_update_ok(sql, principal):
            d = ChatBiSqlGateDenied(
                deny_code="CHATBI_SQL_DENIED",
                rule="l2_update_portrait_only",
                stmt_class="update",
                access_level=2,
                target_table="chatbi_user_portrait",
            )
            _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
            raise d

    # 策略：有行则按 min_*；无行时仅 Super 放行写类；Admin/L2 对无策略表禁止 DML
    def _policy_pair(t: tuple[str, str]) -> ChatBiTablePolicyRow | None:
        return policies.get(t) or policies.get(("public", t[1]))

    if kind == "select":
        if policies:
            for sch, tbl in tables:
                pol = _policy_pair((sch, tbl))
                if pol is None:
                    if principal.access_level > 0:
                        d = ChatBiSqlGateDenied(
                            deny_code="CHATBI_SQL_DENIED",
                            rule="no_policy_row",
                            stmt_class="select",
                            access_level=principal.access_level,
                            target_table=tbl,
                        )
                        _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
                        raise d
                    continue
                if not allowed_op(access_level=principal.access_level, min_level=pol.min_select_level):
                    d = ChatBiSqlGateDenied(
                        deny_code="CHATBI_SQL_DENIED",
                        rule="below_min_level",
                        stmt_class="select",
                        access_level=principal.access_level,
                        target_table=tbl,
                    )
                    _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
                    raise d
        if principal.access_level == 2:
            sid = (principal.subject_user_id or "").strip()
            if sid and sid not in sql:
                d = ChatBiSqlGateDenied(
                    deny_code="CHATBI_SQL_DENIED",
                    rule="l2_subject_predicate_required",
                    stmt_class="select",
                    access_level=2,
                )
                _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
                raise d

    elif kind == "insert":
        if policies:
            for sch, tbl in tables:
                pol = _policy_pair((sch, tbl))
                if pol is None and principal.access_level > 0:
                    d = ChatBiSqlGateDenied(
                        deny_code="CHATBI_SQL_DENIED",
                        rule="no_policy_row",
                        stmt_class="insert",
                        target_table=tbl,
                        access_level=principal.access_level,
                    )
                    _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
                    raise d
                if pol and not allowed_op(access_level=principal.access_level, min_level=pol.min_insert_level):
                    d = ChatBiSqlGateDenied(
                        deny_code="CHATBI_SQL_DENIED",
                        rule="below_min_level",
                        stmt_class="insert",
                        target_table=tbl,
                        access_level=principal.access_level,
                    )
                    _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
                    raise d

    elif kind == "update":
        if policies:
            for sch, tbl in tables:
                pol = _policy_pair((sch, tbl))
                if pol is None and principal.access_level > 0:
                    d = ChatBiSqlGateDenied(
                        deny_code="CHATBI_SQL_DENIED",
                        rule="no_policy_row",
                        stmt_class="update",
                        target_table=tbl,
                        access_level=principal.access_level,
                    )
                    _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
                    raise d
                if pol and not allowed_op(access_level=principal.access_level, min_level=pol.min_update_level):
                    d = ChatBiSqlGateDenied(
                        deny_code="CHATBI_SQL_DENIED",
                        rule="below_min_level",
                        stmt_class="update",
                        target_table=tbl,
                        access_level=principal.access_level,
                    )
                    _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
                    raise d

    if kind == "select":
        if chatbi_json_log_enabled():
            log_chatbi_record(
                message="sql_gate_allow",
                event="sql_gate_allow",
                access_level=principal.access_level,
                stmt_class="select",
                target_table=tables[0][1],
                request_id=request_id,
                run_id=run_id,
                sql_fp=_sql_fingerprint(sql),
            )
        return sql, "select"
    if kind == "update":
        if chatbi_json_log_enabled():
            log_chatbi_record(
                message="sql_gate_allow",
                event="sql_gate_allow",
                access_level=principal.access_level,
                stmt_class="update",
                target_table=tables[0][1],
                request_id=request_id,
                run_id=run_id,
                sql_fp=_sql_fingerprint(sql),
            )
        return sql, "update"

    if kind == "insert":
        if chatbi_json_log_enabled():
            log_chatbi_record(
                message="sql_gate_allow",
                event="sql_gate_allow",
                access_level=principal.access_level,
                stmt_class="insert",
                target_table=tables[0][1],
                request_id=request_id,
                run_id=run_id,
                sql_fp=_sql_fingerprint(sql),
            )
        return sql, "insert"

    d = ChatBiSqlGateDenied(
        deny_code="CHATBI_SQL_DENIED",
        rule="stmt_not_allowed_here",
        stmt_class=kind,
        access_level=principal.access_level,
    )
    _log_deny(principal=principal, deny=d, run_id=run_id, request_id=request_id, sql=sql)
    raise d
