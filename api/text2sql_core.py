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


def execute_select_sql(sql: str, *, limit_rows: int = 200) -> tuple[list[str], list[dict[str, Any]]]:
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
            cur.execute(limited_sql)
            return _rows_to_dicts(cur)


@dataclass(frozen=True)
class Text2SqlResult:
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    answer: str
    retrieved: list[dict[str, Any]]


def build_sql_prompt(query: str, retrieved: list[dict[str, Any]]) -> str:
    ddl = "\n\n".join([r["content"] for r in retrieved if r.get("doc_type") == "ddl"][:4])
    examples = "\n\n".join([r["content"] for r in retrieved if r.get("doc_type") == "example"][:3])
    return "\n\n".join(
        [
            "你是 Text2SQL 生成器。请根据用户问题生成可在 Postgres(Supabase) 执行的 SQL。",
            "硬性约束：",
            "- 只输出一条 SQL；只允许 SELECT（或 WITH ... SELECT）；不要包含解释文字；",
            "- 只能使用下方提供的表与字段；不要编造不存在的表/字段；",
            "- 尽量使用 snake_case 小写表/字段名。",
            "",
            f"【可用表结构(DDL)】\n{ddl}".strip(),
            f"【示例问答与SQL】\n{examples}".strip(),
            f"【用户问题】\n{query}".strip(),
            "",
            "只输出 SQL：",
        ]
    ).strip()


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

