from __future__ import annotations

from .state import ChatBIState, resolve_failure_edge


async def run_graph_stub(state: ChatBIState) -> ChatBIState:
    """P0 最小 runner：单 stub 节点，非完整 ReAct。"""
    state.current_node = "stub"
    if state.error_code:
        state.current_node = resolve_failure_edge(error_code=state.error_code, graph=True)
    state.partial["graph_stub"] = True
    state.partial["message"] = "ChatBI Graph P0 skeleton"
    return state
