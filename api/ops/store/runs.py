"""Ops Desk Run / Event / Checkpoint 仓储层。"""

from __future__ import annotations

import time
from typing import Any

from api.ops.events_schema import SCHEMA_VERSION
from api.rag_env import supabase_client, supabase_execute_with_retry


class OpsRunStore:
    """ops_runs / ops_run_events / ops_run_checkpoints 读写。"""

    def __init__(self, client: Any) -> None:
        self.client = client

    def _repo_id(self, owner: str, name: str) -> str | None:
        def _once() -> Any:
            res = (
                self.client.table("ops_repos")
                .select("id")
                .eq("owner", owner)
                .eq("name", name)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if rows and isinstance(rows[0], dict):
                return rows[0].get("id")
            return None

        return supabase_execute_with_retry(_once)

    def create_run(
        self,
        query: str,
        route: str,
        repo_owner: str = "MoonshotAI",
        repo_name: str = "kimi-code",
        session_id: str | None = None,
    ) -> dict[str, Any]:
        repo_id = self._repo_id(repo_owner, repo_name)
        if not repo_id:
            raise ValueError(f"repo {repo_owner}/{repo_name} not found")

        row = {
            "repo_id": repo_id,
            "query": query,
            "route": route,
            "status": "running" if route == "deep" else "done",
            "session_id": session_id,
        }

        def _once() -> dict[str, Any]:
            res = self.client.table("ops_runs").insert(row).execute()
            data = res.data if isinstance(res.data, list) else []
            if not data or not isinstance(data[0], dict):
                raise RuntimeError("ops_runs insert did not return row")
            return data[0]

        return supabase_execute_with_retry(_once)

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        def _once() -> dict[str, Any] | None:
            res = self.client.table("ops_runs").select("*").eq("id", run_id).limit(1).execute()
            rows = res.data if isinstance(res.data, list) else []
            if rows and isinstance(rows[0], dict):
                return rows[0]
            return None

        return supabase_execute_with_retry(_once)

    def update_run(self, run_id: str, **fields: Any) -> None:
        def _once() -> None:
            self.client.table("ops_runs").update(fields).eq("id", run_id).execute()

        supabase_execute_with_retry(_once)

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        """写 run 级 metrics_json；与 update_run 区分以便追踪。"""
        self.update_run(run_id, metrics_json=metrics_json)

    def next_seq(self, run_id: str) -> int:
        def _once() -> int:
            res = (
                self.client.table("ops_run_events")
                .select("seq", count="exact")
                .eq("run_id", run_id)
                .order("seq", desc=True)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if rows and isinstance(rows[0], dict) and rows[0].get("seq") is not None:
                return int(rows[0]["seq"]) + 1
            return 1

        return supabase_execute_with_retry(_once)

    def append_event(
        self,
        run_id: str,
        agent_role: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
        seq: int | None = None,
    ) -> dict[str, Any]:
        if seq is None:
            seq = self.next_seq(run_id)
        row = {
            "run_id": run_id,
            "seq": seq,
            "ts_ms": int(time.time() * 1000),
            "node_id": node_id,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
        }

        def _once() -> dict[str, Any]:
            res = self.client.table("ops_run_events").insert(row).execute()
            data = res.data if isinstance(res.data, list) else []
            if not data or not isinstance(data[0], dict):
                raise RuntimeError("ops_run_events insert did not return row")
            return data[0]

        return supabase_execute_with_retry(_once)

    def get_events(self, run_id: str, after_seq: int = 0, limit: int = 200) -> list[dict[str, Any]]:
        def _once() -> list[dict[str, Any]]:
            res = (
                self.client.table("ops_run_events")
                .select("*")
                .eq("run_id", run_id)
                .gt("seq", after_seq)
                .order("seq")
                .limit(limit)
                .execute()
            )
            return res.data if isinstance(res.data, list) else []

        return supabase_execute_with_retry(_once)

    def validate_retry_token(self, run_id: str, retry_token: str) -> bool:
        run = self.get_run(run_id)
        if not run:
            return False
        token = run.get("retry_token")
        return bool(token) and str(token) == retry_token

    def retry_run(self, run_id: str, retry_token: str) -> dict[str, Any] | None:
        if not self.validate_retry_token(run_id, retry_token):
            return None
        self.update_run(run_id, status="running")
        return self.get_run(run_id)

    def list_runs_by_session_id(self, session_id: str, *, limit: int = 50) -> list[dict[str, Any]]:
        def _once() -> list[dict[str, Any]]:
            res = (
                self.client.table("ops_runs")
                .select("*")
                .eq("session_id", session_id)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return res.data if isinstance(res.data, list) else []

        return supabase_execute_with_retry(_once)

    def list_events_for_session(
        self,
        session_id: str,
        *,
        after_seq: int = 0,
        limit: int = 500,
    ) -> list[dict[str, Any]]:
        runs = self.list_runs_by_session_id(session_id, limit=50)
        if not runs:
            return []
        run_ids = [str(r["id"]) for r in runs if r.get("id")]
        if not run_ids:
            return []

        def _once() -> list[dict[str, Any]]:
            res = (
                self.client.table("ops_run_events")
                .select("*")
                .in_("run_id", run_ids)
                .gt("seq", after_seq)
                .order("ts_ms")
                .limit(limit)
                .execute()
            )
            return res.data if isinstance(res.data, list) else []

        return supabase_execute_with_retry(_once)

    def save_checkpoint(
        self, run_id: str, checkpoint_id: str, state_json: dict[str, Any]
    ) -> dict[str, Any]:
        row = {"run_id": run_id, "checkpoint_id": checkpoint_id, "state_json": state_json}

        def _once() -> dict[str, Any]:
            res = (
                self.client.table("ops_run_checkpoints")
                .upsert(row, on_conflict="run_id,checkpoint_id")
                .execute()
            )
            data = res.data if isinstance(res.data, list) else []
            if data and isinstance(data[0], dict):
                return data[0]
            raise RuntimeError("ops_run_checkpoints upsert failed")

        return supabase_execute_with_retry(_once)


def append_event(
    run_id: str,
    kind: str,
    payload: dict[str, Any],
    store: OpsRunStore | None = None,
) -> dict[str, Any]:
    """标准化事件写入辅助函数（P0-2）。

    - 自动注入 `schema_version` 到 payload（若不存在）。
    - `kind` 映射为 `event_type`；`agent_role` 按 kind 语义映射：
      - handoff -> orchestrator
      - review  -> review
      - 其他    -> kind
    - 未提供 store 时，使用全局 supabase_client() 构造 OpsRunStore。
    """
    normalized = dict(payload)
    if "schema_version" not in normalized:
        normalized["schema_version"] = SCHEMA_VERSION

    agent_role = {"handoff": "orchestrator", "review": "review"}.get(kind, kind)
    target = store if store is not None else OpsRunStore(supabase_client())
    return target.append_event(run_id, agent_role, kind, payload=normalized)
