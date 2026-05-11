"""Text2SQL 列值域与口语映射（YAML）；供 build_sql_prompt 注入；可选 DISTINCT 探针与 YAML 并集防漂移。"""

from __future__ import annotations

import copy
import os
import re
from pathlib import Path
from typing import Any

from .text2sql_core import execute_select_sql, validate_sql_readonly

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_HINTS_REL = Path("docs/text2sql/v1/value_hints.yaml")

_loaded: dict[str, tuple[float, dict[str, Any]]] = {}

_RE_SAFE_IDENT = re.compile(r"^[a-zA-Z0-9_]+$")


def _truthy_env(name: str, default: bool = True) -> bool:
    raw = (os.getenv(name) or "").strip().lower()
    if raw in ("0", "false", "no", "off"):
        return False
    if raw in ("1", "true", "yes", "on"):
        return True
    return default


def _resolve_hints_path() -> Path | None:
    """返回待加载的 YAML 路径；显式关闭或未找到文件时返回 None。"""
    if not _truthy_env("TEXT2SQL_VALUE_HINTS_ENABLED", default=True):
        return None
    env_p = (os.getenv("TEXT2SQL_VALUE_HINTS_PATH") or "").strip()
    if env_p:
        p = Path(env_p)
        if not p.is_absolute():
            p = (_REPO_ROOT / p).resolve()
    else:
        p = (_REPO_ROOT / _DEFAULT_HINTS_REL).resolve()
    return p if p.is_file() else None


def load_hints(path: str | Path) -> dict[str, Any] | None:
    """读取 YAML；文件不存在返回 None。按 mtime 进程内缓存。"""
    p = Path(path).resolve()
    key = str(p)
    try:
        mtime = p.stat().st_mtime
    except OSError:
        return None
    hit = _loaded.get(key)
    if hit and hit[0] == mtime:
        return hit[1]
    try:
        import yaml  # type: ignore[import-untyped]
    except ImportError:
        return None
    try:
        # utf-8-sig：避免 Windows/编辑器写入的 BOM 导致 safe_load 异常或解析异常
        data = yaml.safe_load(p.read_text(encoding="utf-8-sig"))
    except yaml.YAMLError:
        return None
    except (OSError, UnicodeDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    _loaded[key] = (mtime, data)
    return data


def load_resolved_hints() -> dict[str, Any] | None:
    rp = _resolve_hints_path()
    return load_hints(rp) if rp else None


def ddl_table_names_from_retrieved(retrieved: list[dict[str, Any]]) -> set[str]:
    """从检索到的 DDL 块解析表名（小写）。"""
    names: set[str] = set()
    for r in retrieved:
        if not isinstance(r, dict) or r.get("doc_type") != "ddl":
            continue
        title = r.get("title")
        if isinstance(title, str):
            m = re.match(r"DDL:\s*([a-z0-9_]+)\s*$", title.strip(), flags=re.IGNORECASE)
            if m:
                names.add(m.group(1).lower())
        content = r.get("content")
        if isinstance(content, str):
            m2 = re.search(r"create\s+table\s+public\.([a-z0-9_]+)\s*\(", content, flags=re.IGNORECASE)
            if m2:
                names.add(m2.group(1).lower())
    return names


def _last_primary_table_from_history(history: list[dict[str, Any]] | None) -> str | None:
    if not history:
        return None
    for item in reversed(history):
        if not isinstance(item, dict):
            continue
        g = item.get("text2sql_grounding")
        if not isinstance(g, dict):
            continue
        pt = g.get("primary_table")
        if isinstance(pt, str) and pt.strip():
            return pt.strip().lower()
    return None


def tables_for_value_hints(ddl_names: set[str], primary_table: str | None) -> set[str]:
    """表级裁剪：优先 grounding 主表与 DDL 的交集；否则用全部 DDL 命中表。"""
    if not ddl_names:
        return set()
    pt = (primary_table or "").strip().lower()
    if pt and pt in ddl_names:
        return {pt}
    return set(ddl_names)


def parse_distinct_allowlist() -> list[tuple[str, str, str]]:
    """解析 `TEXT2SQL_DISTINCT_COLUMNS`，返回 [(schema, table, column), ...]（小写表名、列名，用于与 YAML 对齐）。"""
    raw = (os.getenv("TEXT2SQL_DISTINCT_COLUMNS") or "").strip()
    if not raw:
        return []
    out: list[tuple[str, str, str]] = []
    for part in raw.split(","):
        p = part.strip()
        if not p:
            continue
        bits = p.split(".")
        if len(bits) != 3:
            continue
        sch, tbl, col = bits[0], bits[1], bits[2]
        if not (_RE_SAFE_IDENT.match(sch) and _RE_SAFE_IDENT.match(tbl) and _RE_SAFE_IDENT.match(col)):
            continue
        out.append((sch.lower(), tbl.lower(), col.lower()))
    return out


def _is_distinct_probe_enabled() -> bool:
    return _truthy_env("TEXT2SQL_DISTINCT_PROBE", default=False)


def _distinct_row_limit() -> int:
    try:
        return max(1, min(int(os.getenv("TEXT2SQL_DISTINCT_MAX", "64")), 500))
    except ValueError:
        return 64


def _distinct_max_probes() -> int:
    try:
        return max(1, min(int(os.getenv("TEXT2SQL_DISTINCT_MAX_PROBES", "8")), 32))
    except ValueError:
        return 8


def _distinct_statement_timeout_ms() -> int | None:
    raw = (os.getenv("TEXT2SQL_DISTINCT_STMT_TIMEOUT_MS") or "").strip()
    if not raw:
        return None
    try:
        return max(1, min(int(raw), 600_000))
    except ValueError:
        return None


def _quote_ident(ident: str) -> str:
    return '"' + ident.replace('"', '""') + '"'


def _distinct_values_from_execute(cols: list[str], rows: list[dict[str, Any]]) -> list[str]:
    if not cols:
        return []
    key = cols[0]
    out: list[str] = []
    for r in rows:
        v = r.get(key)
        if v is None:
            continue
        out.append(str(v).strip())
    return [x for x in out if x]


def run_distinct_probe_values(schema: str, table: str, column: str, *, limit_n: int) -> list[str] | None:
    """执行只读 DISTINCT；成功返回字符串列表，失败返回 None（调用方降级为仅 YAML）。"""
    sql_raw = (
        f"SELECT DISTINCT {_quote_ident(column)} "
        f"FROM {_quote_ident(schema)}.{_quote_ident(table)} "
        f"LIMIT {int(limit_n)}"
    )
    try:
        sql_ok = validate_sql_readonly(sql_raw)
    except Exception:
        return None
    try:
        cols, rows = execute_select_sql(
            sql_ok,
            limit_rows=limit_n,
            statement_timeout_ms=_distinct_statement_timeout_ms(),
        )
    except Exception:
        return None
    return _distinct_values_from_execute(cols, rows)


def merge_hints_with_distinct_probes(hints: dict[str, Any], target_tables: set[str]) -> dict[str, Any]:
    """在 allowlist 与 YAML 列匹配且表在 target_tables 内时，执行 DISTINCT 并与 values 并集；失败列保留 YAML。"""
    if not _is_distinct_probe_enabled():
        return hints
    allow = parse_distinct_allowlist()
    if not allow:
        return hints
    max_calls = _distinct_max_probes()
    candidates: list[tuple[str, str, str]] = []
    for tri in allow:
        if tri[1] in target_tables:
            candidates.append(tri)
        if len(candidates) >= max_calls:
            break
    if not candidates:
        return hints

    merged = copy.deepcopy(hints)
    tables = merged.get("tables")
    if not isinstance(tables, dict):
        return hints

    limit_n = _distinct_row_limit()
    for sch, tbl, col in candidates:
        tcfg = tables.get(tbl)
        if not isinstance(tcfg, dict):
            continue
        for _logical, coldef in tcfg.items():
            if not isinstance(coldef, dict):
                continue
            cn = coldef.get("column")
            if not isinstance(cn, str) or cn.strip().lower() != col:
                continue
            raw_vals = coldef.get("values")
            yaml_strs: list[str] = []
            if isinstance(raw_vals, list):
                yaml_strs = [str(v) for v in raw_vals if isinstance(v, (str, int, float))]
            # 防漂移：即使 YAML 已配置仍执行 DISTINCT（任务 B.0-5）
            sampled = run_distinct_probe_values(sch, tbl, col, limit_n=limit_n)
            if sampled is None:
                continue
            merged_set = set(yaml_strs) | set(sampled)
            coldef["values"] = sorted(merged_set, key=lambda x: str(x))
            break

    return merged


def _distinct_merge_disclaimer() -> str | None:
    if not _is_distinct_probe_enabled():
        return None
    if not parse_distinct_allowlist():
        return None
    return (
        "以下为库内 DISTINCT 采样与业务字典「库内取值」的并集（LIMIT 条件下非全量闭集）；"
        "口语映射以同义词表为准。"
    )


def format_hints_for_prompt(hints: dict[str, Any], table_names: set[str]) -> str:
    """将命中的表/列格式化为 prompt 正文（不含外层标题）。"""
    tables = hints.get("tables")
    if not isinstance(tables, dict) or not table_names:
        return ""
    lines: list[str] = []
    for tname in sorted(table_names):
        tcfg = tables.get(tname)
        if not isinstance(tcfg, dict):
            continue
        lines.append(f"表 public.{tname}")
        for _logical, coldef in sorted(tcfg.items(), key=lambda x: str(x[0])):
            if not isinstance(coldef, dict):
                continue
            col = coldef.get("column")
            if not isinstance(col, str) or not col.strip():
                continue
            vals = coldef.get("values")
            val_list: list[str] = []
            if isinstance(vals, list):
                val_list = [str(v) for v in vals if isinstance(v, (str, int, float))]
            syns = coldef.get("synonyms")
            syn_parts: list[str] = []
            if isinstance(syns, dict):
                for k, v in sorted(syns.items(), key=lambda kv: (str(kv[0]), str(kv[1]))):
                    if isinstance(k, str) and isinstance(v, str) and k.strip() and v.strip():
                        syn_parts.append(f"{k}→{v}")
            vtxt = "、".join(val_list) if val_list else "（未配置）"
            stxt = ("；口语同义词：" + "；".join(syn_parts)) if syn_parts else ""
            lines.append(f"  - 列 {col.strip()}：库内取值：{vtxt}{stxt}")
        lines.append("")
    return "\n".join(lines).strip()


def build_value_hints_block_for_text2sql(
    retrieved: list[dict[str, Any]],
    *,
    history: list[dict[str, Any]] | None = None,
) -> str | None:
    """加载字典并按 DDL（及可选 grounding）裁剪；无配置或空块返回 None。"""
    hints = load_resolved_hints()
    if not hints:
        return None
    ddl_names = ddl_table_names_from_retrieved(retrieved)
    primary = _last_primary_table_from_history(history)
    target_tables = tables_for_value_hints(ddl_names, primary)
    hints_for_body = merge_hints_with_distinct_probes(hints, target_tables)
    body = format_hints_for_prompt(hints_for_body, target_tables)
    if not body.strip():
        return None
    dis = _distinct_merge_disclaimer()
    header_lines = [
        "【业务术语与库内取值】",
        "以下为业务字典补充，不替代上方 DDL；WHERE / CASE / GROUP BY 中的枚举字面量须与下列「库内取值」一致。",
    ]
    if dis:
        header_lines.append(dis)
    header_lines.append("【值域与口语映射】")
    header = "\n".join(header_lines)
    return f"{header}\n{body}".strip()
