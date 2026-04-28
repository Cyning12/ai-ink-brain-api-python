"""RAG 侧无状态共享工具（Legacy chat 与 Unified 共用，行为以 Unified 实现为基准）。"""

from __future__ import annotations

import os
import re


def parse_match_threshold() -> float | None:
    """解析 RAG_MATCH_THRESHOLD：默认 0.3；none/null/off 关闭过滤；非法或 <0 回退 0.3；>1 视为关闭过滤（None）。"""
    raw = os.getenv("RAG_MATCH_THRESHOLD", "").strip()
    if not raw:
        return 0.3
    if raw.lower() in ("none", "null", "off"):
        return None
    try:
        v = float(raw)
    except ValueError:
        return 0.3
    if v > 1.0:
        return None
    if v < 0:
        return 0.3
    return v


def strip_doc_context_prefix(text: str) -> str:
    """去掉 ingest 写入的文档前缀信息，避免 snippet 噪声。"""
    t = (text or "").strip()
    if not t:
        return ""
    m = re.search(r"(?m)^Content:\s*", t)
    if m:
        return t[m.end() :].strip()
    t = re.sub(r"(?m)^\[Document Context\]\s*$", "", t).strip()
    t = re.sub(r"(?m)^Title:\s*.*$", "", t).strip()
    t = re.sub(r"(?m)^Date:\s*.*$", "", t).strip()
    t = re.sub(r"(?m)^Category:\s*.*$", "", t).strip()
    t = re.sub(r"(?m)^---\s*$", "", t).strip()
    return t
