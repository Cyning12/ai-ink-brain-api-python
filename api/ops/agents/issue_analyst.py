"""Ops Desk issue_analyst 子 Agent（只读）。"""

from __future__ import annotations

from typing import Any

from api.ops.llm import chat_completion
from api.ops.queries import OpsQueries


def analyze_issue(query: str, issue_number: int, queries: OpsQueries) -> dict[str, Any]:
    """深析单个 issue；不调用任何 Git 写 API。"""
    issue = queries.fetch_issue_by_number(issue_number)
    if not issue:
        return {
            "issue_number": issue_number,
            "found": False,
            "evidence": [],
            "reasoning": f"数据库中不存在 issue #{issue_number}",
            "suggestion": "请确认 issue 编号或等待下次同步。",
            "confidence": 0.0,
            "citations": [],
        }

    evidence = [
        {
            "kind": "issue",
            "number": issue_number,
            "title": issue.get("title"),
            "state": issue.get("state"),
            "labels": issue.get("labels", []),
            "scan_tags": issue.get("scan_tags", []),
            "html_url": issue.get("html_url"),
        }
    ]

    prompt = (
        f"用户问题：{query}\n"
        f"Issue #{issue_number}：{issue.get('title')}\n"
        f"状态：{issue.get('state')} 标签：{issue.get('labels', [])}\n"
        f" scan_tags：{issue.get('scan_tags', [])}\n\n"
        "请给出简短分析（是否适合、风险、建议），并只引用存在的 #NNN。"
        "输出 JSON：{reasoning, suggestion, confidence(0-1), citations:[{number, url}]}"
    )

    raw = chat_completion([{"role": "user", "content": prompt}], temperature=0.3)
    parsed = _parse_llm_json(raw)
    return {
        "issue_number": issue_number,
        "found": True,
        "evidence": evidence,
        "reasoning": parsed.get("reasoning", raw),
        "suggestion": parsed.get("suggestion", ""),
        "confidence": float(parsed.get("confidence", 0.7)),
        "citations": parsed.get("citations", []),
    }


def _parse_llm_json(text: str) -> dict[str, Any]:
    """极简 JSON 提取：优先解析代码块，否则整个文本。"""
    import json
    import re

    if "```json" in text:
        match = re.search(r"```json\s*(.*?)\s*```", text, re.S)
        if match:
            text = match.group(1)
    elif "```" in text:
        match = re.search(r"```\s*(.*?)\s*```", text, re.S)
        if match:
            text = match.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}
