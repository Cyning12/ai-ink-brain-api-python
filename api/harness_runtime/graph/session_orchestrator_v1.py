"""session_orchestrator_v1 · S2 00 层图（与 P1 单轮图并存）。"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph

from api.harness_runtime.nodes import session_00
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
) -> Any:
    """编译 00 图 · 节点闭包绑定 session 目录。"""

    def n_plan(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_plan(state, session_dir=session_dir, task_path=task_path)

    def n_present(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_present_plan(state)

    def n_auth(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_auth_gate(state)

    def n_synthesize(state: SessionGraphState) -> SessionGraphState:
        return session_00.node_00_synthesize(state)

    graph = StateGraph(SessionGraphState)
    graph.add_node("plan", n_plan)
    graph.add_node("present", n_present)
    graph.add_node("auth_gate", n_auth)
    graph.add_node("synthesize", n_synthesize)

    graph.add_edge(START, "plan")
    graph.add_edge("plan", "present")
    graph.add_edge("present", "auth_gate")
    graph.add_conditional_edges(
        "auth_gate",
        session_00.route_after_auth,
        {"synthesize": "synthesize", "plan": "plan", "end": END},
    )
    graph.add_edge("synthesize", END)

    cp = checkpointer or get_checkpointer()
    return graph.compile(checkpointer=cp, name=GRAPH_NAME)


@lru_cache(maxsize=1)
def _cached_graph_key(session_dir_str: str, task_path_str: str) -> str:
    return f"{session_dir_str}:{task_path_str}"


def compile_for_session(session_dir: Path, task_path: Path, checkpointer: BaseCheckpointSaver | None = None) -> Any:
    """按 session 编译图（目录绑定）。"""
    return build_session_orchestrator_v1(
        session_dir=session_dir,
        task_path=task_path,
        checkpointer=checkpointer,
    )
