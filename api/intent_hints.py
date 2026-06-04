"""Intent 站点上下文（YAML）；供 _llm_decide_v2 Prompt 注入。"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parents[1]
_DEFAULT_HINTS_REL = Path("docs/chatbi/v1/intent_hints.yaml")

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
    if not _truthy_env("INTENT_HINTS_ENABLED", default=True):
        return None
    env_p = (os.getenv("INTENT_HINTS_PATH") or "").strip()
    if env_p:
        p = Path(env_p)
        if not p.is_absolute():
            p = (_REPO_ROOT / p).resolve()
    else:
        p = (_REPO_ROOT / _DEFAULT_HINTS_REL).resolve()
    return p if p.is_file() else None


def load_hints(path: str | Path) -> dict[str, Any] | None:
    """读取 YAML；文件不存在或解析失败返回 None。按 mtime 进程内缓存。"""
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


def clear_intent_hints_cache() -> None:
    """供单测切换 env / 文件后清空 mtime 缓存。"""
    _loaded.clear()


def _person_names(hints: dict[str, Any]) -> list[str]:
    persons = hints.get("persons")
    if not isinstance(persons, list):
        return []
    names: list[str] = []
    for item in persons:
        if not isinstance(item, dict):
            continue
        name = item.get("name")
        if isinstance(name, str) and name.strip():
            names.append(name.strip())
    return names


def _person_rag_triggers(hints: dict[str, Any]) -> list[str]:
    triggers: set[str] = set()
    persons = hints.get("persons")
    if not isinstance(persons, list):
        return []
    for item in persons:
        if not isinstance(item, dict):
            continue
        raw = item.get("rag_triggers")
        if isinstance(raw, list):
            for t in raw:
                if isinstance(t, str) and t.strip():
                    triggers.add(t.strip())
    return sorted(triggers)


def _format_few_shots(hints: dict[str, Any]) -> str:
    shots = hints.get("few_shots")
    if not isinstance(shots, list) or not shots:
        return ""
    lines: list[str] = []
    for shot in shots:
        if not isinstance(shot, dict):
            continue
        q = shot.get("query")
        tool = shot.get("tool")
        reasoning = shot.get("reasoning")
        if not isinstance(q, str) or not isinstance(tool, str):
            continue
        conf = shot.get("confidence")
        conf_s = f", \"confidence\": {float(conf)}" if conf is not None else ""
        reason_s = str(reasoning or "").strip()
        lines.append(
            f'Q: {q}\n{{"tool": "{tool.strip()}", "reasoning": "{reason_s}"{conf_s}}}'
        )
    return "\n\n".join(lines)


def build_intent_hints_prompt_block(hints: dict[str, Any] | None) -> str:
    """将 YAML 配置格式化为 Prompt 注入块；无配置或空块返回 \"\"。"""
    if not hints:
        return ""

    lines: list[str] = ["## 站点上下文（配置 · intent_hints.yaml）"]

    summary = hints.get("product_summary")
    if isinstance(summary, str) and summary.strip():
        lines.append("")
        lines.append(summary.strip())

    site_mode = hints.get("site_mode")
    if isinstance(site_mode, str) and site_mode.strip():
        lines.append("")
        lines.append(f"（site_mode: {site_mode.strip()}）")

    names = _person_names(hints)
    triggers = _person_rag_triggers(hints)
    if names or triggers:
        lines.append("")
        lines.append("### 须走 rag_search 的 Portfolio 场景")
        if names:
            joined = "、".join(names)
            lines.append(f"- 问个人经历、履历、成果、评价、优势、看法（尤其涉及下列人物：{joined}）")
        if triggers:
            lines.append(f"- 与人名共现时倾向检索的触发词：{'、'.join(triggers)}")
        lines.append("- 问「N 年经历 / AI Coding 成果 / 混合检索 / 冷温热分层」等 Portfolio 文稿主题时，优先 rag_search")

    exceptions = hints.get("direct_answer_exceptions")
    if isinstance(exceptions, list) and exceptions:
        lines.append("")
        lines.append("### 仍选 direct_answer 的例外")
        for ex in exceptions:
            if isinstance(ex, str) and ex.strip():
                lines.append(f"- {ex.strip()}")

    few = _format_few_shots(hints)
    if few:
        lines.append("")
        lines.append("### 配置 few-shot 补充")
        lines.append(few)

    body = "\n".join(lines).strip()
    if body == "## 站点上下文（配置 · intent_hints.yaml）":
        return ""
    return body
