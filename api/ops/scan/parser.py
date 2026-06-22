"""ISSUE_SCAN markdown → 结构化 scan snapshot。"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

# 匹配 #123 或 #100-#110（连字符/短横线范围）；跳过 [#123](url) 里的 PR 链接
_ISSUE_REF_RE = re.compile(r"(?<!\[)#(\d+)(?:[–\-]#(\d+))?(?!\])")
_OPEN_COUNT_RE = re.compile(r"open\s+\*\*(\d+)\*\*")
_VERSION_RE = re.compile(r"\|\s*\*\*版本\*\*\s*\|\s*(v[\d.]+)\s*\|")
_OVERVIEW_RE = re.compile(r"^##\s*1\.\s*总览", re.MULTILINE)


def _tier_for_label(label: str) -> str | None:
    """根据 overview 表格第一列标签映射到标准 tier。"""
    norm = label.strip().upper()
    if "P0" in norm:
        return "C3-P0"
    if "P1" in norm:
        return "C3-P1"
    if "P2" in norm:
        return "C3-P2"
    if "P3" in norm or "观察" in label or "OBSERVE" in norm:
        return "OBSERVE"
    if "C2" in norm:
        return "C2"
    return None


def _expand_issue_refs(text: str) -> list[dict[str, Any]]:
    """从文本中提取 #NNN 引用，展开范围。"""
    items: list[dict[str, Any]] = []
    seen: set[int] = set()
    for match in _ISSUE_REF_RE.finditer(text):
        start = int(match.group(1))
        end_raw = match.group(2)
        end = int(end_raw) if end_raw else start
        for number in range(start, end + 1):
            if number in seen:
                continue
            seen.add(number)
            items.append({"number": number})
    return items


def _extract_version(markdown: str) -> str | None:
    match = _VERSION_RE.search(markdown)
    return match.group(1) if match else None


def _extract_total_open(markdown: str) -> int | None:
    match = _OPEN_COUNT_RE.search(markdown)
    return int(match.group(1)) if match else None


def _extract_overview_tiers(markdown: str) -> dict[str, Any]:
    """解析 ## 1. 总览 表格，返回 tier → items 及 tags_by_number。"""
    sections: dict[str, list[dict[str, Any]]] = {
        "C2": [],
        "C3-P0": [],
        "C3-P1": [],
        "C3-P2": [],
        "OBSERVE": [],
    }
    tags_by_number: dict[int, list[str]] = {}

    match = _OVERVIEW_RE.search(markdown)
    if not match:
        return {"sections": sections, "tags_by_number": tags_by_number}

    overview_text = markdown[match.start() :]
    # 截取到下一个 ## 标题之前
    next_heading = re.search(r"\n##\s+", overview_text[1:])
    if next_heading:
        overview_text = overview_text[: next_heading.start() + 1]

    for line in overview_text.splitlines():
        if line.count("|") < 3:
            continue
        cells = [c.strip() for c in line.split("|")]
        if len(cells) < 3:
            continue
        label = cells[1]
        content = cells[2]
        tier = _tier_for_label(label)
        if not tier:
            continue
        items = _expand_issue_refs(content)
        for item in items:
            number = item["number"]
            tags_by_number.setdefault(number, []).append(tier)
        sections[tier].extend(items)

    return {"sections": sections, "tags_by_number": tags_by_number}


def parse_issue_scan(markdown: str, *, raw_url: str | None = None) -> dict[str, Any]:
    """解析 ISSUE_SCAN 主索引 markdown。"""
    version = _extract_version(markdown) or "unknown"
    total_open = _extract_total_open(markdown)
    overview = _extract_overview_tiers(markdown)
    sections = overview["sections"]
    tags_by_number = overview["tags_by_number"]

    section_summary = [
        {"tier": tier, "count": len(items)}
        for tier, items in sections.items()
    ]

    return {
        "scan_version": version,
        "total_open": total_open,
        "p0_items": sections["C3-P0"],
        "p1_items": sections["C3-P1"],
        "p2_items": sections["C3-P2"],
        "deferred_items": sections["OBSERVE"],
        "raw_markdown_url": raw_url,
        "parsed_summary": {
            "version": version,
            "scanned_at": datetime.now(timezone.utc).isoformat(),
            "sections": section_summary,
        },
        "tags_by_number": tags_by_number,
    }


def load_issue_scan(path: Path) -> str:
    return path.read_text(encoding="utf-8")
