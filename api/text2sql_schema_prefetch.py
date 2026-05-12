"""Text2SQL：写入/更新类问题在 LLM 生成前按需预取 information_schema 列清单。"""

from __future__ import annotations

import os
import re
from typing import Any

from .chatbi_policies import ChatBiTablePolicyRow, allowed_op
from .chatbi_principal import ChatBiPrincipal

_IDENT = re.compile(r"^[a-z][a-z0-9_]{0,62}$")


def schema_prefetch_enabled() -> bool:
    """TEXT2SQL_SCHEMA_PREFETCH=0/false 关闭；未配置时若存在 TEXT2SQL_DATABASE_URL 则默认开启。"""
    raw = (os.getenv("TEXT2SQL_SCHEMA_PREFETCH") or "").strip().lower()
    if raw in ("0", "false", "no", "off"):
        return False
    if raw in ("1", "true", "yes", "on"):
        return True
    return bool((os.getenv("TEXT2SQL_DATABASE_URL") or "").strip())


def is_text2sql_mutate_intent_query(q: str) -> bool:
    """粗粒度写入/更新语义，避免纯 SELECT 分析走预取。"""
    s = (q or "").strip()
    if not s:
        return False
    sl = s.lower()
    cn_write = (
        "插入",
        "写入",
        "录入",
        "导入",
        "新增一行",
        "新增数据",
        "更新",
        "修改",
        "变更",
        "覆盖",
        "保存到",
        "upsert",
    )
    if any(k in s for k in cn_write):
        return True
    if any(k in sl for k in (" insert ", " update ", " upsert ", "merge into")):
        return True
    if re.search(r"(?i)\binsert\b", sl) or re.search(r"(?i)\bupdate\b", sl):
        return True
    # 口语：「若.*存在.*更新」「插入或更新」
    if ("存在" in s and "更新" in s) or ("插入" in s and "更新" in s):
        return True
    return False


def query_suggests_insert_update(q: str) -> tuple[bool, bool]:
    """用于与表级 min_insert / min_update 对齐。"""
    s = (q or "").strip()
    sl = s.lower()
    ins = any(k in s for k in ("插入", "新增", "导入", "录入")) or "insert" in sl
    upd = any(k in s for k in ("更新", "修改", "变更")) or "update" in sl
    if not ins and not upd and is_text2sql_mutate_intent_query(s):
        # 「写入/保存」等未显式区分时，两种权限都参考
        ins = True
        upd = True
    return ins, upd


def extract_candidate_tables_from_query(q: str) -> list[str]:
    """从自然语言中抽取候选表名（public、小写、去重保序）。"""
    s = (q or "").strip()
    if not s:
        return []
    found: list[str] = []

    def _push(name: str) -> None:
        t = name.strip().lower()
        if not _IDENT.match(t):
            return
        if t not in found:
            found.append(t)

    for m in re.finditer(r"(?i)public\.([a-z][a-z0-9_]*)", s):
        _push(m.group(1))
    for m in re.finditer(r"(?i)\binto\s+([a-z][a-z0-9_]*)\b", s):
        _push(m.group(1))
    for m in re.finditer(r"(?i)\bupdate\s+([a-z][a-z0-9_]*)\b", s):
        _push(m.group(1))
    for m in re.finditer(r"([a-z][a-z0-9_]{1,63})\s*表", s, flags=re.IGNORECASE):
        _push(m.group(1))
    return found


def _ddl_chunks_for_table(retrieved: list[dict[str, Any]], table: str) -> str:
    t = table.lower()
    parts: list[str] = []
    for r in retrieved:
        if not isinstance(r, dict) or r.get("doc_type") != "ddl":
            continue
        title = str(r.get("title") or "")
        if title.lower().startswith("ddl:"):
            name = title.split(":", 1)[1].strip().lower()
            if name == t:
                parts.append(str(r.get("content") or ""))
                continue
        body = str(r.get("content") or "")
        if re.search(rf"(?is)create\s+table\s+(?:public\.)?{re.escape(t)}\b", body):
            parts.append(body)
    return "\n\n".join(parts).strip()


def ddl_fragment_has_column_anchor(retrieved: list[dict[str, Any]], table: str) -> bool:
    """判断检索到的 DDL 是否含足够列级锚点（防短片段/无列）。"""
    blob = _ddl_chunks_for_table(retrieved, table)
    if not blob:
        return False
    m = re.search(
        r"(?is)create\s+table\s+(?:public\.)?[a-z0-9_]+\s*\(\s*(.*)\)\s*(?:;|\s*$)",
        blob,
    )
    if not m:
        return False
    body = m.group(1)
    lines = [
        ln.strip()
        for ln in body.splitlines()
        if ln.strip() and not ln.strip().lower().startswith(("constraint ", "primary key", "unique ("))
    ]
    col_like = 0
    for ln in lines:
        if re.match(r"(?i)^[a-z_][a-z0-9_]*\s+[a-z]", ln):
            col_like += 1
    return col_like >= 2


def _policy_allows_table_for_prefetch(
    table: str,
    *,
    principal: ChatBiPrincipal | None,
    policies: dict[tuple[str, str], ChatBiTablePolicyRow] | None,
    needs_insert: bool,
    needs_update: bool,
) -> bool:
    if principal is None or not policies:
        return True
    key = ("public", table.lower())
    pol = policies.get(key)
    if pol is None:
        return principal.access_level == 0
    ok = False
    if needs_insert and allowed_op(access_level=principal.access_level, min_level=pol.min_insert_level):
        ok = True
    if needs_update and allowed_op(access_level=principal.access_level, min_level=pol.min_update_level):
        ok = True
    return ok


def format_prefetched_columns_block(rows_by_table: dict[str, list[dict[str, Any]]]) -> str:
    lines: list[str] = []
    for tbl in sorted(rows_by_table.keys()):
        lines.append(f"### public.{tbl}")
        for r in rows_by_table[tbl]:
            cn = str(r.get("column_name") or "")
            dt = str(r.get("data_type") or "")
            nul = str(r.get("is_nullable") or "")
            lines.append(f"- `{cn}` : {dt} (nullable: {nul})")
        lines.append("")
    return "\n".join(lines).strip()


def fetch_public_table_columns_sync(
    tables: list[str],
    *,
    statement_timeout_ms: int | None = None,
    max_rows: int | None = None,
) -> tuple[dict[str, list[dict[str, Any]]], str | None]:
    """只读查询 information_schema.columns；tables 须已通过标识符校验。"""
    if not tables:
        return {}, None
    dsn = (os.getenv("TEXT2SQL_DATABASE_URL") or "").strip()
    if not dsn:
        return {}, "缺少环境变量 TEXT2SQL_DATABASE_URL，无法在写入前拉取列结构。"

    st_ms = statement_timeout_ms
    if st_ms is None:
        try:
            st_ms = int(os.getenv("TEXT2SQL_SCHEMA_PREFETCH_TIMEOUT_MS", "8000"))
        except ValueError:
            st_ms = 8000
    st_ms = max(200, min(int(st_ms), 60_000))

    cap = max_rows
    if cap is None:
        try:
            cap = int(os.getenv("TEXT2SQL_SCHEMA_PREFETCH_MAX_ROWS", "2000"))
        except ValueError:
            cap = 2000
    cap = max(10, min(int(cap), 20_000))

    import psycopg  # type: ignore[import-not-found]

    timeout_s = float(os.getenv("TEXT2SQL_DB_CONNECT_TIMEOUT_S", "8"))
    sql = (
        "SELECT table_name, column_name, data_type, is_nullable, ordinal_position\n"
        "FROM information_schema.columns\n"
        "WHERE table_schema = 'public' AND table_name = ANY(%s)\n"
        "ORDER BY table_name, ordinal_position\n"
        f"LIMIT {cap}"
    )
    try:
        with psycopg.connect(dsn, connect_timeout=timeout_s) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SET LOCAL statement_timeout = '{st_ms}ms'")
                cur.execute(sql, (list(tables),))
                cols = [d.name for d in (cur.description or [])]
                raw_rows = cur.fetchall()
    except Exception as exc:  # noqa: BLE001
        return {}, f"预取表结构失败：{exc}"

    out: dict[str, list[dict[str, Any]]] = {}
    for row in raw_rows:
        rec = {cols[i]: row[i] for i in range(len(cols))}
        tn = str(rec.get("table_name") or "").lower()
        if not tn:
            continue
        out.setdefault(tn, []).append(rec)

    missing = [t for t in tables if t not in out or not out[t]]
    if missing:
        return {}, f"以下表在 public schema 未找到列定义（请确认表名）：{', '.join(missing)}"

    return out, None


def run_text2sql_schema_prefetch_sync(
    *,
    user_query: str,
    retrieved: list[dict[str, Any]],
    principal: ChatBiPrincipal | None,
    policies: dict[tuple[str, str], ChatBiTablePolicyRow] | None,
) -> tuple[str | None, str | None, dict[str, Any]]:
    """返回 (prompt_block, error_zh, meta)。无预取需求时 block 与 error 均为 None。"""
    meta: dict[str, Any] = {"schema_prefetch_source": "skipped", "schema_prefetch_tables": []}
    if not schema_prefetch_enabled():
        meta["schema_prefetch_source"] = "disabled"
        return None, None, meta

    q = (user_query or "").strip()
    if not is_text2sql_mutate_intent_query(q):
        meta["schema_prefetch_source"] = "skipped_not_mutate"
        return None, None, meta

    candidates = extract_candidate_tables_from_query(q)
    needs_ins, needs_upd = query_suggests_insert_update(q)
    meta["schema_prefetch_candidates"] = list(candidates)
    meta["schema_prefetch_needs_insert"] = needs_ins
    meta["schema_prefetch_needs_update"] = needs_upd

    if not candidates:
        meta["schema_prefetch_source"] = "error_no_table"
        return (
            None,
            "当前问题疑似写入/更新操作，但无法从描述中解析出明确的 public 表名；请写明表名（例如 agent_info 表）。",
            meta,
        )

    pols = policies or {}
    allowed: list[str] = []
    for t in candidates:
        if _policy_allows_table_for_prefetch(
            t,
            principal=principal,
            policies=pols,
            needs_insert=needs_ins,
            needs_update=needs_upd,
        ):
            allowed.append(t)

    need_fetch: list[str] = []
    ddl_ok: list[str] = []
    for t in allowed:
        if ddl_fragment_has_column_anchor(retrieved, t):
            ddl_ok.append(t)
        else:
            need_fetch.append(t)

    meta["schema_prefetch_allowed_tables"] = list(allowed)
    meta["schema_prefetch_ddl_sufficient"] = ddl_ok
    meta["schema_prefetch_need_fetch"] = list(need_fetch)

    extra_blocked = [t for t in candidates if t not in allowed]
    if extra_blocked:
        meta["schema_prefetch_source"] = "error_policy"
        meta["schema_prefetch_blocked_tables"] = extra_blocked
        return (
            None,
            "无法在缺少可靠 DDL 的情况下生成写入类 SQL：以下表不在当前账号 INSERT/UPDATE 策略内："
            + ", ".join(extra_blocked),
            meta,
        )

    if not need_fetch:
        meta["schema_prefetch_source"] = "retrieved_ddl_only"
        return None, None, meta

    rows_by_tbl, err = fetch_public_table_columns_sync(need_fetch)
    if err:
        meta["schema_prefetch_source"] = "error_db"
        return None, err, meta

    block = format_prefetched_columns_block(rows_by_tbl)
    meta["schema_prefetch_source"] = "information_schema_prefetch"
    meta["schema_prefetch_tables"] = list(need_fetch)
    return block, None, meta
