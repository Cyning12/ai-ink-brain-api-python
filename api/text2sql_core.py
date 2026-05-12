from __future__ import annotations

import os
import re
from dataclasses import dataclass
from typing import Any

from openai import OpenAI


SQL_FORBIDDEN = (
    "insert",
    "update",
    "delete",
    "alter",
    "drop",
    "truncate",
    "create",
    "grant",
    "revoke",
)


def is_text2sql_intent(query: str) -> bool:
    """极简意图识别：命中“查数/统计”语义即进入 Text2SQL。"""
    q = (query or "").strip()
    if not q:
        return False
    keywords = (
        "查询",
        "统计",
        "多少",
        "金额",
        "收入",
        "支出",
        "人数",
        "数量",
        "总数",
        "平均",
        "最大",
        "最小",
        "top",
        "排行",
        "分组",
    )
    ql = q.lower()
    return any(k in q for k in keywords) or any(k in ql for k in ("count", "sum", "avg", "group by", "top"))


def validate_sql_readonly(sql: str) -> str:
    s = (sql or "").strip()
    if not s:
        raise ValueError("Empty SQL")

    # 去掉 markdown ```sql
    s = re.sub(r"^```sql\s*", "", s, flags=re.IGNORECASE).strip()
    s = re.sub(r"```$", "", s).strip()

    # 单语句：禁止多分号
    if s.count(";") > 1:
        raise ValueError("Multiple statements are not allowed")
    s = s.rstrip(";").strip()

    low = re.sub(r"\s+", " ", s.lower()).strip()
    if not (low.startswith("select") or low.startswith("with ")):
        raise ValueError("Only SELECT is allowed")
    for kw in SQL_FORBIDDEN:
        if re.search(rf"\b{re.escape(kw)}\b", low):
            raise ValueError(f"Forbidden keyword: {kw}")
    return s


def _rows_to_dicts(cur) -> tuple[list[str], list[dict[str, Any]]]:
    cols = [d.name for d in (cur.description or [])]
    rows = cur.fetchall()
    out: list[dict[str, Any]] = []
    for r in rows:
        row = {}
        for i, c in enumerate(cols):
            v = r[i]
            # psycopg 会返回 datetime/Decimal 等，交给 JSONResponse 由 FastAPI 处理或转 str
            row[c] = v
        out.append(row)
    return cols, out


def execute_mutating_sql(
    sql: str,
    *,
    statement_timeout_ms: int | None = None,
) -> int:
    """执行单条 INSERT/UPDATE（已通过闸门）；返回 rowcount。"""
    dsn = (os.getenv("TEXT2SQL_DATABASE_URL") or "").strip()
    if not dsn:
        raise RuntimeError("Missing env: TEXT2SQL_DATABASE_URL")

    import psycopg  # type: ignore[import-not-found]

    timeout_s = float(os.getenv("TEXT2SQL_DB_CONNECT_TIMEOUT_S", "8"))
    with psycopg.connect(dsn, connect_timeout=timeout_s) as conn:
        with conn.cursor() as cur:
            if statement_timeout_ms is not None:
                st = max(1, min(int(statement_timeout_ms), 600_000))
                cur.execute(f"SET LOCAL statement_timeout = '{st}ms'")
            cur.execute(sql)
            return int(cur.rowcount or 0)


def execute_select_sql(
    sql: str,
    *,
    limit_rows: int = 200,
    statement_timeout_ms: int | None = None,
) -> tuple[list[str], list[dict[str, Any]]]:
    dsn = (os.getenv("TEXT2SQL_DATABASE_URL") or "").strip()
    if not dsn:
        raise RuntimeError("Missing env: TEXT2SQL_DATABASE_URL")

    # 依赖延迟加载：避免在仅跑单测/未安装可选依赖时 import 失败
    import psycopg  # type: ignore[import-not-found]

    # 强制加一个上限：避免返回过大
    limited_sql = sql
    if re.search(r"\blimit\b", sql, flags=re.IGNORECASE) is None:
        limited_sql = f"{sql}\nlimit {max(1, min(int(limit_rows), 200))}"

    timeout_s = float(os.getenv("TEXT2SQL_DB_CONNECT_TIMEOUT_S", "8"))
    with psycopg.connect(dsn, connect_timeout=timeout_s) as conn:
        with conn.cursor() as cur:
            if statement_timeout_ms is not None:
                st = max(1, min(int(statement_timeout_ms), 600_000))
                cur.execute(f"SET LOCAL statement_timeout = '{st}ms'")
            cur.execute(limited_sql)
            return _rows_to_dicts(cur)


@dataclass(frozen=True)
class Text2SqlResult:
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    answer: str
    retrieved: list[dict[str, Any]]


def build_sql_prompt(
    query: str,
    retrieved: list[dict[str, Any]],
    *,
    dialogue_context: str | None = None,
    value_hints_block: str | None = None,
    prefetched_schema_block: str | None = None,
    chatbi_access_level: int | None = None,
    chatbi_subject_user_id: str | None = None,
) -> str:
    ddl = "\n\n".join([r["content"] for r in retrieved if r.get("doc_type") == "ddl"][:4])
    examples = "\n\n".join([r["content"] for r in retrieved if r.get("doc_type") == "example"][:3])
    vh = (value_hints_block or "").strip()
    ctx = (dialogue_context or "").strip()
    ctx_block = (
        "\n\n".join(
            [
                "【近期对话（指代消解）】",
                "若当前问题含「刚刚/该表/那张表/其中/上面」等，须结合下文继承**具体表名、统计对象**，不得臆造其它表。",
                ctx,
            ]
        ).strip()
        if ctx
        else ""
    )
    pfb = (prefetched_schema_block or "").strip()
    pref_block = ""
    if pfb:
        pref_block = "\n\n".join(
            [
                "【系统预取表结构（列名以数据库为准）】",
                "以下列名由系统只读查询 information_schema 拉取，**须逐列使用**；不得臆造未列出的字段。",
                "若与上方 DDL 片段冲突，以本段为准。",
                pfb,
            ]
        ).strip()

    parts: list[str] = [
        "你是 Text2SQL 生成器。请根据用户问题生成可在 Postgres(Supabase) 执行的 SQL。",
        "硬性约束：",
        "- 只输出一条 SQL；不要包含解释文字；默认使用 SELECT（或 WITH ... SELECT）；",
        "- 若下方「当前主体权限」允许 UPDATE/INSERT，方可输出对应单条语句；",
        "- 只能使用下方提供的表与字段；不要编造不存在的表/字段；",
        "- 尽量使用 snake_case 小写表/字段名。",
        "",
        f"【可用表结构(DDL)】\n{ddl}".strip(),
    ]
    if pref_block:
        parts.append(pref_block)
    parts.append(f"【示例问答与SQL】\n{examples}".strip())
    if vh:
        parts.append(vh)
    if ctx_block:
        parts.append(ctx_block)
    parts.extend(
        [
            f"【用户问题】\n{query}".strip(),
            "",
            "只输出 SQL：",
        ]
    )
    if chatbi_access_level is not None:
        if chatbi_access_level >= 2:
            sid = (chatbi_subject_user_id or "").strip()
            parts.insert(
                -2,
                "\n".join(
                    [
                        "【当前主体权限：终端用户 L2】",
                        "- 仅允许一条 SELECT 或（在明确要求修改个人肖像/长久习惯时）单条 UPDATE；",
                        "- SELECT：单表、禁止 JOIN；WHERE 必须包含你本人归属键（与 subject_user_id 一致）的字面量过滤；",
                        "- 禁止 INSERT；禁止 DELETE/TRUNCATE；",
                        "- UPDATE 仅允许 `public.chatbi_user_portrait`，且只能 SET `long_term_prompt` / `updated_at`，WHERE 必须 `user_id = '<你的subject_user_id>'`；",
                        *(["", f"- 你的 subject_user_id 为：`{sid}`（须在 SQL 中显式出现）。"] if sid else []),
                    ]
                ),
            )
        elif chatbi_access_level == 1:
            parts.insert(
                -2,
                "\n".join(
                    [
                        "【当前主体权限：Admin】",
                        "- 默认输出 SELECT；若用户明确要求软删/置失效，可使用 UPDATE 修改标志位或 deleted_at；",
                        "- 禁止使用 DELETE 与 TRUNCATE；禁止 DDL。",
                    ]
                ),
            )
        else:
            parts.insert(
                -2,
                "\n".join(
                    [
                        "【当前主体权限：Super】",
                        "- 默认 SELECT；写操作须符合表级策略；本工具链不执行物理 DELETE/TRUNCATE（请用运维迁移）。",
                    ]
                ),
            )
    return "\n\n".join(parts).strip()


def try_summarize_aggregate(query: str, columns: list[str], rows: list[dict[str, Any]]) -> str | None:
    """对 count/sum 等聚合结果做确定性总结，避免 LLM 把 0 行误判成「未查到数据」。

    仅在结果形态极明确时生效：单行 + 单列数字。
    """
    if len(rows) != 1:
        return None
    if not rows[0] or len(rows[0]) != 1:
        return None
    (col, val), = rows[0].items()
    if val is None:
        return None
    if isinstance(val, bool):
        return None
    try:
        val_f = float(val)
        val_i = int(val)
    except Exception:  # noqa: BLE001
        return None
    name = (col or "").lower()
    if name in ("count", "cnt", "total", "sum", "avg", "min", "max"):
        if name in ("count", "cnt"):
            return f"共有 {val_i} 条。"
        return f"结果为 {val_f:g}。"
    return None


def build_summary_prompt(query: str, sql: str, columns: list[str], rows: list[dict[str, Any]]) -> str:
    preview = rows[:20]
    return "\n\n".join(
        [
            "你是数据分析助手。请根据用户问题、SQL 和查询结果，输出简洁的中文回答。",
            "要求：",
            "- 只输出回答正文；",
            "- 若结果为空，说明“未查到数据”；",
            "- 数字可适度格式化。",
            "",
            f"【用户问题】\n{query}".strip(),
            f"【SQL】\n{sql}".strip(),
            f"【列】\n{columns}".strip(),
            f"【结果预览(最多20行)】\n{preview}".strip(),
        ]
    ).strip()


def llm_generate_sql(*, oai: OpenAI, model: str, prompt: str) -> str:
    res = oai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        stream=False,
    )
    content = (res.choices[0].message.content or "").strip()
    return content


def llm_summarize(*, oai: OpenAI, model: str, prompt: str) -> str:
    res = oai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        stream=False,
    )
    return (res.choices[0].message.content or "").strip()

