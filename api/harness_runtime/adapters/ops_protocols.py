"""Ops 业务层适配协议（S5 边界隔离）。

`harness_runtime` 通过 Protocol 注入 `api.ops` 的具体实现，避免在 import 阶段
加载 RAG / ingest / 业务 ORM 等黑盒依赖。
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class RunStoreProtocol(Protocol):
    """Session Orchestrator 对 `api.ops.store.OpsRunStore` 的最小需求。"""

    def create_run(
        self,
        *,
        query: str,
        route: str,
        session_id: str | None = None,
    ) -> dict[str, Any]: ...

    def append_event(
        self,
        run_id: str,
        source: str,
        event_type: str,
        *,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
    ) -> dict[str, Any]: ...

    def update_run(
        self,
        run_id: str,
        *,
        status: str | None = None,
        final_answer: dict[str, Any] | None = None,
    ) -> dict[str, Any]: ...

    def save_checkpoint(
        self,
        run_id: str,
        checkpoint_id: str,
        state_json: dict[str, Any],
    ) -> dict[str, Any]: ...


class QueriesProtocol(Protocol):
    """RAG 查询适配占位；Runtime 内部不调用具体方法，仅透传给 subagent。"""


class DemoCacheProtocol(Protocol):
    """Demo 缓存适配占位；Runtime 内部不调用具体方法，仅透传给 subagent。"""
