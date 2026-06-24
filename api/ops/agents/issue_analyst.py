"""Ops Desk issue_analyst 子 Agent（只读）。"""

from __future__ import annotations

from typing import Any

from api.ops.llm import chat_completion
from api.ops.queries import OpsQueries
from api.ops.tracing import traceable


def _normalize_citations(
    citations: list[dict[str, Any]], queries: OpsQueries
) -> list[dict[str, Any]]:
    """用 DB html_url 替换 LLM 生成的 url，确保 Review V2 通过。"""
    normalized: list[dict[str, Any]] = []
    for cite in citations:
        number = cite.get("number")
        if not number:
            continue
        issue = queries.fetch_issue_by_number(int(number))
        pr = queries.fetch_pull_by_number(int(number))
        url = None
        if issue:
            url = issue.get("html_url")
        elif pr:
            url = pr.get("html_url")
        normalized.append({"number": number, "url": url or cite.get("url", "")})
    return normalized


@traceable(capture_input=False, capture_output=False)
def analyze_issue(
    query: str,
    issue_number: int,
    queries: OpsQueries,
    review_feedback: dict[str, Any] | None = None,
) -> dict[str, Any]:
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

    feedback_block = ""
    if review_feedback:
        rule = review_feedback.get("rule", "")
        message = review_feedback.get("message", "")
        feedback_block = (
            f"\n\n【上一轮 Review 未通过】\n"
            f"规则：{rule}\n"
            f"原因：{message}\n"
            f"请修正上述问题后重新分析，确保引用真实存在的 issue 且 url 正确。"
        )

    prompt = (
        f"用户问题：{query}\n"
        f"Issue #{issue_number}：{issue.get('title')}\n"
        f"状态：{issue.get('state')} 标签：{issue.get('labels', [])}\n"
        f" scan_tags：{issue.get('scan_tags', [])}\n"
        f"{feedback_block}\n\n"
        "请给出简短分析（是否适合、风险、建议），并只引用存在的 #NNN。"
        "输出 JSON：{reasoning, suggestion, confidence(0-1), citations:[{number, url}]}"
    )

    raw = chat_completion([{"role": "user", "content": prompt}], temperature=0.3)
    parsed = _parse_llm_json(raw)

    citations = parsed.get("citations", [])
    # A1: Review 前用 DB html_url 归一化
    citations = _normalize_citations(citations, queries)

    return {
        "issue_number": issue_number,
        "found": True,
        "evidence": evidence,
        "reasoning": parsed.get("reasoning", raw),
        "suggestion": parsed.get("suggestion", ""),
        "confidence": float(parsed.get("confidence", 0.7)),
        "citations": citations,
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
