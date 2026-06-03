from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

# V2 总规 §2.4 主路径 error_code（边表草案覆盖子集；P0 仅结构分表）
_COMMON_EDGE_CODES = (
    "LLM_API_TIMEOUT",
    "RAG_RETRIEVE_EMPTY",
    "RAG_GENERATE_UNCERTAIN",
    "SQL_GEN_EMPTY",
    "SQL_GEN_SYNTAX",
    "SQL_EXEC_TABLE_NOT_FOUND",
    "SQL_EXEC_NO_DATA",
    "SQL_EXEC_PERMISSION_DENIED",
    "CHATBI_SQL_DENIED",
    "CHATBI_SQL_WRITE_DENIED",
    "UNKNOWN",
)


@dataclass
class ChatBIState:
    """Graph 节点间共享状态（P0 草案）。"""

    run_id: str
    query: str
    session_id: str | None = None
    error_code: str | None = None
    current_node: str = "start"
    partial: dict[str, Any] = field(default_factory=dict)


def failure_edges_legacy() -> dict[str, str]:
    """旧 Agent / Unified：Intent 超时走 V1 规则路由（D-3 legacy）。"""
    edges = {code: "tool_fallback" for code in _COMMON_EDGE_CODES}
    edges["LLM_API_TIMEOUT"] = "intent_v1_fallback"
    edges["RAG_RETRIEVE_EMPTY"] = "gated_tool_fallback"
    edges["SQL_EXEC_PERMISSION_DENIED"] = "direct_answer_final"
    edges["CHATBI_SQL_DENIED"] = "direct_answer_final"
    edges["CHATBI_SQL_WRITE_DENIED"] = "direct_answer_final"
    edges["SQL_EXEC_NO_DATA"] = "direct_answer_final"
    return edges


def failure_edges_graph() -> dict[str, str]:
    """Graph 边表：Intent 超时方案 A → direct_answer + error/think（D-3）。"""
    edges = {code: "tool_fallback" for code in _COMMON_EDGE_CODES}
    edges["LLM_API_TIMEOUT"] = "direct_answer"
    edges["RAG_RETRIEVE_EMPTY"] = "direct_answer"
    edges["RAG_GENERATE_UNCERTAIN"] = "direct_answer"
    edges["SQL_EXEC_PERMISSION_DENIED"] = "direct_answer"
    edges["CHATBI_SQL_DENIED"] = "direct_answer"
    edges["CHATBI_SQL_WRITE_DENIED"] = "direct_answer"
    return edges


def resolve_failure_edge(*, error_code: str | None, graph: bool) -> str:
    code = (error_code or "UNKNOWN").strip() or "UNKNOWN"
    table = failure_edges_graph() if graph else failure_edges_legacy()
    return table.get(code, table["UNKNOWN"])
