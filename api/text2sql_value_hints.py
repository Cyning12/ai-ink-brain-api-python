"""Text2SQL 列值域与口语映射（YAML）；供 build_sql_prompt 注入。"""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_HINTS_REL = Path("docs/text2sql/v1/value_hints.yaml")

_loaded: dict[str, tuple[float, dict[str, Any]]] = {}


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
        data = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
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
    body = format_hints_for_prompt(hints, target_tables)
    if not body.strip():
        return None
    header = "\n".join(
        [
            "【业务术语与库内取值】",
            "以下为业务字典补充，不替代上方 DDL；WHERE / CASE / GROUP BY 中的枚举字面量须与下列「库内取值」一致。",
            "【值域与口语映射】",
        ]
    )
    return f"{header}\n{body}".strip()
