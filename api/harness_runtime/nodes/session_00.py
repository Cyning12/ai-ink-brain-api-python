"""Session 00 层节点（S2 · plan · present · auth interrupt · synthesize）。"""

from __future__ import annotations

from pathlib import Path

from langgraph.types import interrupt

from api.harness_runtime.state import SessionGraphState


def build_plan_summary(*, user_message: str, title: str) -> str:
    """轻量计划摘要（测试可 monkeypatch · 生产可换 LLM）。"""
    snippet = user_message.strip()
    if len(snippet) > 200:
        snippet = snippet[:197] + "..."
    return (
        f"## 计划摘要\n\n"
        f"**主题**：{title}\n\n"
        f"**需求**：{snippet}\n\n"
        f"- 00 已生成 task 草稿与验收项\n"
        f"- 请授权后开始派工（S3 深析）"
    )


def _append_plan_section(task_path: Path, plan_summary: str) -> None:
    content = task_path.read_text(encoding="utf-8")
    marker = "## 计划（00 维护）"
    block = f"{marker}\n\n{plan_summary}\n"
    if marker in content:
        head, _, _tail = content.partition(marker)
        content = head.rstrip() + "\n\n" + block
    else:
        content = content.rstrip() + "\n\n" + block
    task_path.write_text(content, encoding="utf-8")


def node_00_plan(state: SessionGraphState, *, session_dir: Path, task_path: Path) -> SessionGraphState:
    user_message = state.get("user_message", "")
    title = task_path.parent.name
    try:
        from api.harness_runtime.session_store.io import load_meta

        meta = load_meta(session_dir)
        title = meta.title
    except Exception:
        pass

    plan_summary = build_plan_summary(user_message=user_message, title=title)
    _append_plan_section(task_path, plan_summary)

    messages = list(state.get("messages", []))
    messages.append({"role": "user", "content": user_message})
    messages.append({"role": "assistant", "content": plan_summary})

    return {
        "plan_summary": plan_summary,
        "messages": messages,
        "task_draft_path": task_path.name,
    }


def node_00_present_plan(state: SessionGraphState) -> SessionGraphState:
    plan_summary = state.get("plan_summary", "")
    return {
        "answer": plan_summary,
        "session_status": "awaiting_auth",
    }


def node_00_auth_gate(state: SessionGraphState) -> SessionGraphState:
    plan_summary = state.get("plan_summary", "")
    # resume 值来自 POST .../auth
    action = interrupt({"type": "auth_required", "plan_summary": plan_summary})
    return {"auth_action": str(action)}


def node_00_synthesize(state: SessionGraphState) -> SessionGraphState:
    action = state.get("auth_action", "")
    plan_summary = state.get("plan_summary", "")
    if action == "approve":
        answer = (
            "已授权并开始派工。\n\n"
            f"{plan_summary}\n\n"
            "Subagent 已登记 dispatch · 请在下方继续对话触发 deep/fast/ReAct 分析。"
        )
    elif action == "revise":
        answer = "已收到修改意见，请继续描述计划调整。"
    else:
        answer = "已取消授权，可重新描述需求以生成计划。"
    messages = list(state.get("messages", []))
    messages.append({"role": "assistant", "content": answer})
    return {"answer": answer, "messages": messages}


def route_after_auth(state: SessionGraphState) -> str:
    from api.harness_runtime.nodes.session_subagent import route_after_auth as s3_route

    return s3_route(state)
