"""Ops Desk Demo Cache：D1-D4 预置题缓存与分类器。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

from api.ops.constants import REPO_NAME, REPO_OWNER
from api.rag_env import supabase_execute_with_retry


class DemoClassifier:
    """把用户消息映射到预置 demo_id；仅做字符串规则匹配。"""

    QUESTIONS: dict[str, dict[str, Any]] = {
        "D1": {
            "patterns": ["open issue", "issue 有多少", "issue 数"],
            "intent": "metrics_trend",
            "params": {"metric": "issue-throughput", "days": 30},
            "query_template": "kimi-code 最近 30 天 open issue 有多少？",
        },
        "D2": {
            "patterns": ["cycle time", "cycle_time", "pr cycle"],
            "intent": "metrics_trend",
            "params": {"metric": "cycle-time", "days": 30},
            "query_template": "PR cycle time 最近 30 天趋势如何？",
        },
        "D3": {
            "patterns": ["review time", "review_time"],
            "intent": "metrics_trend",
            "params": {"metric": "review-time", "days": 30},
            "query_template": "PR review time 中位数是多少？",
        },
        "D4": {
            "patterns": ["#545", "# 545", "545 适合"],
            "intent": "issue_contribution",
            "params": {"issue_number": 545},
            "query_template": "#545 适合我做吗？",
        },
    }

    def classify(self, message: str) -> dict[str, Any] | None:
        msg = message.lower()
        for demo_id, cfg in self.QUESTIONS.items():
            for pattern in cfg["patterns"]:
                if pattern in msg:
                    return {
                        "demo_id": demo_id,
                        "intent": cfg["intent"],
                        "params": cfg["params"],
                        "query_template": cfg["query_template"],
                    }
        return None


class DemoCacheStore:
    """ops_demo_answers 读写；TTL 默认 24h。"""

    def __init__(self, client: Any) -> None:
        self.client = client
        self.classifier = DemoClassifier()

    def _repo_id(self) -> str | None:
        def _once() -> Any:
            res = (
                self.client.table("ops_repos")
                .select("id")
                .eq("owner", REPO_OWNER)
                .eq("name", REPO_NAME)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if rows and isinstance(rows[0], dict):
                return rows[0].get("id")
            return None

        return supabase_execute_with_retry(_once)

    def get(self, demo_id: str) -> dict[str, Any] | None:
        repo_id = self._repo_id()
        if not repo_id:
            return None

        def _once() -> dict[str, Any] | None:
            res = (
                self.client.table("ops_demo_answers")
                .select("*")
                .eq("repo_id", repo_id)
                .eq("demo_id", demo_id)
                .limit(1)
                .execute()
            )
            rows = res.data if isinstance(res.data, list) else []
            if not rows or not isinstance(rows[0], dict):
                return None
            row = rows[0]
            expires_at = row.get("expires_at")
            if expires_at and self._is_expired(expires_at):
                return None
            return row

        return supabase_execute_with_retry(_once)

    def set(
        self,
        demo_id: str,
        answer_json: dict[str, Any],
        query_template: str | None = None,
        params: dict[str, Any] | None = None,
        ttl_hours: float = 24,
        source_sync_run_id: str | None = None,
    ) -> dict[str, Any]:
        repo_id = self._repo_id()
        if not repo_id:
            raise ValueError(f"repo {REPO_OWNER}/{REPO_NAME} not found")

        cfg = DemoClassifier.QUESTIONS.get(demo_id, {})
        row: dict[str, Any] = {
            "repo_id": repo_id,
            "demo_id": demo_id,
            "query_template": query_template or cfg.get("query_template", demo_id),
            "params": params or cfg.get("params", {}),
            "answer_json": answer_json,
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).isoformat(),
        }
        if source_sync_run_id:
            row["source_sync_run_id"] = source_sync_run_id

        def _once() -> dict[str, Any]:
            res = (
                self.client.table("ops_demo_answers")
                .upsert(row, on_conflict="repo_id,demo_id")
                .execute()
            )
            data = res.data if isinstance(res.data, list) else []
            if data and isinstance(data[0], dict):
                return data[0]
            raise RuntimeError("ops_demo_answers upsert did not return row")

        return supabase_execute_with_retry(_once)

    def delete(self, demo_id: str) -> None:
        repo_id = self._repo_id()
        if not repo_id:
            return

        def _once() -> None:
            self.client.table("ops_demo_answers").delete().eq("repo_id", repo_id).eq("demo_id", demo_id).execute()

        supabase_execute_with_retry(_once)

    @staticmethod
    def _is_expired(expires_at: Any) -> bool:
        parsed = _parse_ts(expires_at)
        if not parsed:
            return True
        return datetime.now(timezone.utc) >= parsed


def _parse_ts(value: Any) -> datetime | None:
    if not value:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        value = value.replace("Z", "+00:00")
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            return None
    return None
