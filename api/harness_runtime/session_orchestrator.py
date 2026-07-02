"""Session 00 编排服务（messages · auth · 双写）。"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Literal

from langgraph.types import Command

from api.harness_runtime.errors import HarnessRuntimeError, SessionStatusInvalidError
from api.harness_runtime.gate_sync.human_gate import patch_gate_and_sync
from api.harness_runtime.graph.session_orchestrator_v1 import compile_for_session
from api.harness_runtime.session_store.io import save_meta, transition_status
from api.harness_runtime.session_store.schema import SessionMeta, SessionStatus
from api.ops.store import OpsRunStore

AuthAction = Literal["approve", "revise", "cancel"]
HG_SESSION_PLAN = "HG-SESSION-PLAN"


def thread_config(session_id: str, run_id: str) -> dict[str, Any]:
    return {"configurable": {"thread_id": f"{session_id}:{run_id}"}}


def _checkpoint_payload(meta: SessionMeta, state: dict[str, Any]) -> dict[str, Any]:
    return {
        "session_id": meta.session_id,
        "status": meta.status.value,
        "plan_summary": state.get("plan_summary"),
        "auth_action": state.get("auth_action"),
        "run_id": state.get("run_id"),
    }


def _save_checkpoint(store: OpsRunStore, run_id: str, meta: SessionMeta, state: dict[str, Any]) -> None:
    store.save_checkpoint(run_id, f"{meta.session_id}:latest", _checkpoint_payload(meta, state))


def _is_interrupt_result(result: dict[str, Any]) -> bool:
    return bool(result.get("__interrupt__"))


def handle_planning_message(
    *,
    session_dir: Path,
    meta: SessionMeta,
    message: str,
    store: OpsRunStore,
) -> dict[str, Any]:
    """planning / awaiting_auth · 走 00 图至 interrupt。"""
    task_path = session_dir / meta.primary_task_path
    run = store.create_run(query=message, route="session_00", session_id=meta.session_id)
    run_id = str(run["id"])

    graph = compile_for_session(session_dir, task_path)
    config = thread_config(meta.session_id, run_id)
    initial = {
        "session_id": meta.session_id,
        "run_id": run_id,
        "user_message": message,
        "messages": [],
        "session_status": meta.status.value,
        "task_draft_path": meta.primary_task_path,
    }

    store.append_event(
        run_id,
        "orchestrator",
        "session.graph.start",
        payload={"graph": "session_orchestrator_v1"},
        node_id="n00.start",
    )

    result = graph.invoke(initial, config)

    if _is_interrupt_result(result):
        meta = transition_status(session_dir, SessionStatus.AWAITING_AUTH)
        meta.latest_run_id = run_id
        meta.updated_at = datetime.now(timezone.utc)
        save_meta(session_dir, meta)
        _save_checkpoint(store, run_id, meta, result)

        plan_summary = result.get("plan_summary") or result.get("answer", "")
        store.append_event(
            run_id,
            "orchestrator",
            "session.awaiting_auth",
            payload={"plan_summary": plan_summary},
            node_id="n00.auth_gate",
        )
        store.update_run(
            run_id,
            status="done",
            final_answer={"answer": plan_summary, "awaiting_auth": True},
        )
        store.append_event(run_id, "orchestrator", "run.end", node_id="n00.interrupt")

        return {
            "run_id": run_id,
            "route": "session_00",
            "status": "done",
            "answer": plan_summary,
            "awaiting_auth": True,
            "plan_summary": plan_summary,
        }

    answer = str(result.get("answer", ""))
    store.update_run(run_id, status="done", final_answer={"answer": answer})
    store.append_event(run_id, "orchestrator", "run.end", node_id="n00.end")
    return {
        "run_id": run_id,
        "route": "session_00",
        "status": "done",
        "answer": answer,
    }


def handle_dispatched_message(
    *,
    session_dir: Path,
    meta: SessionMeta,
    message: str,
    store: OpsRunStore,
) -> dict[str, Any]:
    """dispatched · S2 占位 synthesize。"""
    _ = session_dir
    run = store.create_run(query=message, route="session_00", session_id=meta.session_id)
    run_id = str(run["id"])
    answer = (
        "已授权 · 当前 Session 处于 dispatched。\n"
        "深度分析与 subagent 派工将在 S3 提供；本条为 S2 占位回复。"
    )
    store.update_run(run_id, status="done", final_answer={"answer": answer})
    store.append_event(
        run_id,
        "orchestrator",
        "session.s2_placeholder",
        payload={"status": meta.status.value},
        node_id="n00.synthesize.placeholder",
    )
    store.append_event(run_id, "orchestrator", "run.end", node_id="n00.end")
    meta.latest_run_id = run_id
    meta.updated_at = datetime.now(timezone.utc)
    save_meta(session_dir, meta)
    return {
        "run_id": run_id,
        "route": "session_00",
        "status": "done",
        "answer": answer,
    }


def handle_session_auth(
    *,
    session_dir: Path,
    meta: SessionMeta,
    action: AuthAction,
    store: OpsRunStore,
) -> dict[str, Any]:
    """POST .../auth · 双写 + resume 图。"""
    if action == "approve":
        if meta.status == SessionStatus.DISPATCHED and HG_SESSION_PLAN in meta.gate_summary.approved:
            return {
                "session_id": meta.session_id,
                "action": action,
                "status": meta.status.value,
                "idempotent": True,
                "message": "已授权，幂等返回。",
            }
        if meta.status != SessionStatus.AWAITING_AUTH:
            raise SessionStatusInvalidError(
                f"approve requires awaiting_auth, got {meta.status.value}"
            )

        meta = patch_gate_and_sync(session_dir, HG_SESSION_PLAN, "approved")
        meta = transition_status(session_dir, SessionStatus.DISPATCHED)

        run_id = meta.latest_run_id
        if not run_id:
            raise HarnessRuntimeError("RUN_ID_MISSING", "latest_run_id required for auth resume")

        store.append_event(
            run_id,
            "orchestrator",
            "gate.approved",
            payload={"gate_id": HG_SESSION_PLAN, "session_id": meta.session_id},
            node_id="n00.auth",
        )
        store.append_event(
            run_id,
            "orchestrator",
            "session.status_changed",
            payload={"session_id": meta.session_id, "status": meta.status.value},
            node_id="session.status",
        )

        task_path = session_dir / meta.primary_task_path
        graph = compile_for_session(session_dir, task_path)
        config = thread_config(meta.session_id, run_id)
        result = graph.invoke(Command(resume=action), config)

        answer = str(result.get("answer", "已授权并开始派工。"))
        _save_checkpoint(store, run_id, meta, result)
        store.update_run(run_id, status="done", final_answer={"answer": answer, "auth_action": action})
        store.append_event(run_id, "orchestrator", "run.end", node_id="n00.synthesize")

        return {
            "session_id": meta.session_id,
            "action": action,
            "status": meta.status.value,
            "run_id": run_id,
            "answer": answer,
            "gate_summary": meta.gate_summary.model_dump(),
        }

    if action in ("revise", "cancel"):
        if meta.status not in (SessionStatus.AWAITING_AUTH, SessionStatus.PLANNING):
            raise SessionStatusInvalidError(
                f"{action} requires awaiting_auth or planning, got {meta.status.value}"
            )
        meta = transition_status(session_dir, SessionStatus.PLANNING)
        if meta.latest_run_id:
            store.append_event(
                meta.latest_run_id,
                "orchestrator",
                "session.auth_revise" if action == "revise" else "session.auth_cancel",
                payload={"session_id": meta.session_id, "action": action},
                node_id="n00.auth",
            )
        msg = "已回到 planning，请重新描述计划。" if action == "revise" else "已取消，可重新发起需求。"
        return {
            "session_id": meta.session_id,
            "action": action,
            "status": meta.status.value,
            "message": msg,
        }

    raise HarnessRuntimeError("AUTH_ACTION_INVALID", f"unknown action: {action}")
