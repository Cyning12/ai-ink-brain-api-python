"""Ops Desk graph_analyst 子 Agent（只读 · 模块×Issue 矩阵）。"""

from __future__ import annotations

from typing import Any

from api.ops.graph.store import OpsGraphStore
from api.ops.llm import chat_completion
from api.ops.queries import OpsQueries
from api.ops.tracing import traceable


@traceable(capture_input=False, capture_output=False)
def analyze_graph(
    query: str,
    queries: OpsQueries,
    review_feedback: dict[str, Any] | None = None,
    run_id: str | None = None,
    store: Any = None,
) -> dict[str, Any]:
    repo_id = queries._repo_id() or "unknown"
    graph_store = OpsGraphStore(repo_id=repo_id, client=queries.client)
    snapshot = graph_store.get_latest_snapshot()
    if not snapshot:
        return {
            "found": False,
            "evidence": [],
            "reasoning": "尚未 ingest graph.json 快照，请等待 sync 后重试。",
            "suggestion": "可在 Graph Tab 查看是否已有模块矩阵数据。",
            "confidence": 0.0,
            "citations": [],
        }

    payload = snapshot.get("payload") or {}
    nodes = payload.get("nodes", [])
    modules: list[dict[str, Any]] = []
    for node in nodes[:12]:
        if not isinstance(node, dict):
            continue
        module_id = node.get("id")
        if not module_id:
            continue
        issues = graph_store.get_open_issues_for_module(str(module_id))
        modules.append(
            {
                "module_id": module_id,
                "label": node.get("label"),
                "open_issue_count": len(issues),
                "sample_titles": [i.get("title") for i in issues[:3]],
            }
        )

    evidence = [
        {
            "kind": "graph_snapshot",
            "snapshot_id": snapshot.get("id"),
            "node_count": len(nodes),
            "modules": modules,
        }
    ]

    feedback_block = ""
    if review_feedback:
        feedback_block = (
            f"\n\n【Review 反馈】{review_feedback.get('rule')}: {review_feedback.get('message')}"
        )

    prompt = (
        f"用户问题：{query}\n"
        f"模块×Issue 矩阵摘要：{modules}\n"
        f"{feedback_block}\n\n"
        "请解读模块依赖与 open issue 分布，给出结构化建议。"
        "输出 JSON：{reasoning, suggestion, confidence(0-1), citations:[{number, url}]}"
    )
    raw = chat_completion([{"role": "user", "content": prompt}], step="analyze_graph", run_id=run_id, store=store)
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
