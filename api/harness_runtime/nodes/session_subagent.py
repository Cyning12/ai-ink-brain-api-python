"""Session S3 subagent 节点（dispatch · router · review）。"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from api.harness_runtime.deliverables import write_deliverable, write_invoke_snapshot
from api.harness_runtime.state import SessionGraphState


@dataclass
class SubagentRuntime:
    """图节点运行时依赖（测试可空实现）。"""

    session_dir: Path
    store: Any | None = None


def node_dispatch(state: SessionGraphState, *, runtime: SubagentRuntime) -> SessionGraphState:
    run_id = str(state.get("run_id", ""))
    plan_summary = state.get("plan_summary", "")
    payload = {
        "type": "dispatch",
        "session_id": state.get("session_id"),
        "run_id": run_id,
        "plan_summary": plan_summary,
    }
    if run_id:
        rel = write_deliverable(runtime.session_dir, run_id, payload, filename="dispatch.json")
        write_invoke_snapshot(runtime.session_dir, run_id, {"node": "dispatch", "deliverable": str(rel.name)})
        if runtime.store is not None:
            runtime.store.append_event(
                run_id,
                "orchestrator",
                "session.dispatch",
                payload={"session_id": state.get("session_id")},
                node_id="n_dispatch",
            )
    deliverables = dict(state.get("deliverables") or {})
    if run_id:
        deliverables[run_id] = str(runtime.session_dir / "deliverables" / run_id)
    return {
        "session_status": "dispatched",
        "deliverables": deliverables,
        "subagent_route": "pending",
    }


def node_subagent(state: SessionGraphState, *, runtime: SubagentRuntime) -> SessionGraphState:
    """auth approve 路径 · 记录派工确认（深析由 dispatched messages 触发）。"""
    run_id = str(state.get("run_id", ""))
    route = "dispatch_ack"
    payload = {
        "type": route,
        "session_id": state.get("session_id"),
        "run_id": run_id,
        "plan_summary": state.get("plan_summary", ""),
    }
    if run_id:
        write_deliverable(runtime.session_dir, run_id, payload, filename="subagent_ack.json")
        if runtime.store is not None:
            runtime.store.append_event(
                run_id,
                "orchestrator",
                "session.subagent.ack",
                payload={"route": route},
                node_id="n_subagent",
            )
    return {"subagent_route": route}


def node_review(state: SessionGraphState, *, runtime: SubagentRuntime) -> SessionGraphState:
    run_id = str(state.get("run_id", ""))
    if run_id and runtime.store is not None:
        runtime.store.append_event(
            run_id,
            "orchestrator",
            "session.review.pass",
            payload={"rule": "s3_stub", "message": "dispatch ack reviewed"},
            node_id="n_review",
        )
    return {"review_status": "pass"}


def route_after_auth(state: SessionGraphState) -> str:
    action = state.get("auth_action", "")
    if action == "approve":
        return "dispatch"
    if action == "revise":
        return "plan"
    return "end"
