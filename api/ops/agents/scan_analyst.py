"""Ops Desk scan_analyst 子 Agent（只读 · ISSUE_SCAN 摘要）。"""

from __future__ import annotations

from typing import Any

from api.ops.llm import chat_completion
from api.ops.queries import OpsQueries
from api.ops.scan.store import OpsScanStore
from api.ops.tracing import traceable


@traceable(capture_input=False, capture_output=False)
def analyze_scan(
    query: str,
    queries: OpsQueries,
    review_feedback: dict[str, Any] | None = None,
    run_id: str | None = None,
    store: Any = None,
    transcript: list[dict[str, str]] | None = None,
) -> dict[str, Any]:
    repo_id = queries._repo_id() or "unknown"
    scan_store = OpsScanStore(repo_id=repo_id, client=queries.client)
    snapshot = scan_store.get_latest_snapshot()
    if not snapshot:
        return {
            "found": False,
            "evidence": [],
            "reasoning": "尚未 ingest ISSUE_SCAN 快照。",
            "suggestion": "请等待 sync / scan ingest 完成后再问。",
            "confidence": 0.0,
            "citations": [],
        }

    evidence = [
        {
            "kind": "scan_snapshot",
            "scan_version": snapshot.get("scan_version"),
            "total_open": snapshot.get("total_open"),
            "p0_count": len(snapshot.get("p0_items") or []),
            "p1_count": len(snapshot.get("p1_items") or []),
            "p2_count": len(snapshot.get("p2_items") or []),
            "parsed_summary": snapshot.get("parsed_summary"),
        }
    ]

    feedback_block = ""
    if review_feedback:
        feedback_block = (
            f"\n\n【Review 反馈】{review_feedback.get('rule')}: {review_feedback.get('message')}"
        )

    prompt = (
        f"用户问题：{query}\n"
        f"ISSUE_SCAN 摘要：{evidence[0]}\n"
        f"{feedback_block}\n\n"
        "请解读 scan 优先级分布与风险，给出可执行建议。"
        "输出 JSON：{reasoning, suggestion, confidence(0-1), citations:[{number, url}]}"
    )
    messages: list[dict[str, str]] = []
    if transcript:
        messages.extend(transcript)
    messages.append({"role": "user", "content": prompt})
    raw = chat_completion(messages, step="analyze_scan", run_id=run_id, store=store)
    parsed = _parse_llm_json(raw.content)
    return {
        "found": True,
        "evidence": evidence,
        "reasoning": parsed.get("reasoning", raw.content),
        "suggestion": parsed.get("suggestion", ""),
        "confidence": float(parsed.get("confidence", 0.75)),
        "citations": parsed.get("citations", []),
        "_llm_usage": raw.usage.to_dict(),
    }


def _parse_llm_json(text: str) -> dict[str, Any]:
    import json
    import re

    if "```json" in text:
        match = re.search(r"```json\s*(.*?)\s*```", text, re.S)
        if match:
            text = match.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {}
