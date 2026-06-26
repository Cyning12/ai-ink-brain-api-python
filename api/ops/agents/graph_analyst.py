"""Ops Desk graph_analyst 子 Agent（只读 · 模块×Issue 矩阵 + 依赖边）。"""

from __future__ import annotations

from typing import Any

from api.ops.graph.module_matrix import ModuleMatrixService
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
    service = ModuleMatrixService(repo_id=repo_id, client=queries.client)
    snapshot = service._sb().table("ops_graph_snapshots").select("*").eq("repo_id", repo_id).order("created_at", desc=True).limit(1).execute()
    rows = snapshot.data if isinstance(snapshot.data, list) else []
    row = rows[0] if rows and isinstance(rows[0], dict) else None
    if not row:
        return {
            "found": False,
            "evidence": [],
            "reasoning": "尚未 ingest graph.json 快照，请等待 sync 后重试。",
            "suggestion": "可在 Graph Tab 查看是否已有模块矩阵数据。",
            "confidence": 0.0,
            "citations": [],
        }

    payload = row.get("payload") or {}
    modules = service.build_matrix(payload, state="open")
    module_edges = service.get_module_edges(payload, relation="depends_on")

    evidence = [
        {
            "kind": "graph_snapshot",
            "snapshot_id": row.get("id"),
            "node_count": len(payload.get("nodes", [])),
            "modules": modules,
            "module_edges": module_edges,
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
        f"模块依赖边摘要：{module_edges}\n"
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
