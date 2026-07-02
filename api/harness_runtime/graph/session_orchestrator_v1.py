"""session_orchestrator_v1 · S2 00 + S3 dispatch/subagent 段。"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from api.harness_runtime.nodes import session_00, session_subagent
from api.harness_runtime.nodes.session_subagent import SubagentRuntime
from api.harness_runtime.state import SessionGraphState

GRAPH_NAME = "session_orchestrator_v1"

_memory_saver = MemorySaver()


def get_checkpointer() -> BaseCheckpointSaver:
    """默认 MemorySaver · 生产 runner 可注入 OpsRun 适配。"""
    return _memory_saver


def reset_checkpointer_for_tests() -> None:
    global _memory_saver
    _memory_saver = MemorySaver()


def build_session_orchestrator_v1(
    *,
    session_dir: Path,
    task_path: Path,
    checkpointer: BaseCheckpointSaver | None = None,
    runtime: SubagentRuntime | None = None,
) -> Any:
    """编译图 · 节点闭包绑定 session 目录。"""
    sub_runtime = runtime or SubagentRuntime(session_dir=session_dir)

    def n_plan(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_plan(state, session_dir=session_dir, task_path=task_path)

    def n_present(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_present_plan(state)

    def n_auth(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_auth_gate(state)

    def n_dispatch(state: SessionGraphState) -> SessionGraphState:
        return session_subagent.node_dispatch(state, runtime=sub_runtime)

    def n_subagent(state: SessionGraphState) -> SessionGraphState:
        return session_subagent.node_subagent(state, runtime=sub_runtime)

    def n_review(state: SessionGraphState) -> SessionGraphState:
        return session_subagent.node_review(state, runtime=sub_runtime)

    def n_synthesize(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_synthesize(state)

    graph = StateGraph(SessionGraphState)
    graph.add_node("plan", n_plan)
    graph.add_node("present", n_present)
    graph.add_node("auth_gate", n_auth)
    graph.add_node("dispatch", n_dispatch)
    graph.add_node("subagent", n_subagent)
    graph.add_node("review", n_review)
    graph.add_node("synthesize", n_synthesize)

    graph.add_edge(START, "plan")
    graph.add_edge("plan", "present")
    graph.add_edge("present", "auth_gate")
    graph.add_conditional_edges(
        "auth_gate",
        session_00.route_after_auth,
        {"dispatch": "dispatch", "plan": "plan", "end": END},
    )
    graph.add_edge("dispatch", "subagent")
    graph.add_edge("subagent", "review")
    graph.add_edge("review", "synthesize")
    graph.add_edge("synthesize", END)

    cp = checkpointer or get_checkpointer()
    return graph.compile(checkpointer=cp, name=GRAPH_NAME)


def compile_for_session(
    session_dir: Path,
    task_path: Path,
    checkpointer: BaseCheckpointSaver | None = None,
    runtime: SubagentRuntime | None = None,
) -> Any:
    """按 session 编译图（目录绑定）。"""
    return build_session_orchestrator_v1(
        session_dir=session_dir,
        task_path=task_path,
        checkpointer=checkpointer,
        runtime=runtime,
    )
