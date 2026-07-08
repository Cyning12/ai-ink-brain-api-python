"""Ops Chat 共享 Review 规则（deep / ReAct 共用 V1–V4）。"""

from __future__ import annotations

import re
from typing import Any

from api.ops.tracing import traceable, update_current_span_metadata

REVIEW_VERDICT_PASS = "pass"
REVIEW_VERDICT_PARTIAL = "partial"
REVIEW_VERDICT_FAIL = "fail"


class ReviewRule:
    """Review 规则常量。"""

    V1_EXISTS = "V1"
    V2_URL = "V2"
    V3_WRITE_OP = "V3"
    V4_CONFIDENCE = "V4"


@traceable(capture_input=False, capture_output=False)
def review_result(result: dict[str, Any], queries: Any) -> tuple[str, dict[str, Any]]:
    """Review V1–V4；返回 (verdict, detail)。

    V1: 引用的 issue / PR 必须存在于同步表。
    V2: 引用的 issue / PR URL 必须与同步表一致。
    V3: 回答中不能包含 Git 写操作指令。
    V4: 置信度低（<0.5）且缺少证据时返回 partial。
    """
    update_current_span_metadata({"review.rules": "V1-V4"})

    citations = result.get("citations", []) or []
    for cite in citations:
        number = cite.get("number")
        if not number:
            continue
        issue = queries.fetch_issue_by_number(int(number))
        pr = queries.fetch_pull_by_number(int(number))
        if not issue and not pr:
            return REVIEW_VERDICT_FAIL, {
                "rule": ReviewRule.V1_EXISTS,
                "message": f"#{number} 不存在于同步表",
            }
        url = cite.get("url")
        if url:
            expected_issue = issue.get("html_url") if issue else None
            expected_pr = pr.get("html_url") if pr else None
            if url not in (expected_issue, expected_pr):
                return REVIEW_VERDICT_FAIL, {
                    "rule": ReviewRule.V2_URL,
                    "message": f"#{number} url 不匹配",
                }

    text = result.get("reasoning", "") + " " + result.get("suggestion", "")
    if re.search(r"\b(commit|push|open\s+PR|merge)\b", text, re.I):
        return REVIEW_VERDICT_FAIL, {
            "rule": ReviewRule.V3_WRITE_OP,
            "message": "包含 Git 写操作指令",
        }

    confidence = float(result.get("confidence", 0))
    evidence = result.get("evidence", []) or []
    if confidence < 0.5 and not evidence:
        return REVIEW_VERDICT_PARTIAL, {
            "rule": ReviewRule.V4_CONFIDENCE,
            "message": "置信度低且缺少证据",
        }

    return REVIEW_VERDICT_PASS, {}
