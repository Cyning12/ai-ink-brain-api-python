"""P1-6 Demo Cache 测试：D1-D4 命中 / miss / TTL / write-back。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any

import pytest
from fastapi.testclient import TestClient

from api.index import app
from api.ops import chat
from api.ops.demo_cache import DemoCacheStore, DemoClassifier
from api.ops.store import OpsRunStore


class FakeQueries:
    def __init__(self) -> None:
        self.issues = {
            545: {
                "number": 545,
                "title": "Deep demo issue",
                "state": "open",
                "labels": ["bug"],
                "html_url": "https://github.com/MoonshotAI/kimi-code/issues/545",
            }
        }
        self.pulls: dict[int, dict[str, Any]] = {}

    def fetch_issue_by_number(self, number: int) -> dict[str, Any] | None:
        return self.issues.get(number)

    def fetch_pull_by_number(self, number: int) -> dict[str, Any] | None:
        return self.pulls.get(number)

    def cycle_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "cycle-time", "days": days, "summary": {"avg_hours": 48.0}}

    def review_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "review-time", "days": days, "summary": {"avg_hours": 12.0, "median_hours": 10.5}}

    def issue_throughput_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "issue-throughput", "days": days, "summary": {"total": 42, "avg_per_day": 1.4}}

    def fetch_issues(
        self,
        days: int = 30,
        state: str | None = None,
        label: str | None = None,
        module: str | None = None,
        age: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = list(self.issues.values())
        if state:
            rows = [r for r in rows if r.get("state") == state]
        return rows, len(rows)

    def fetch_pulls(
        self,
        days: int = 30,
        state: str | None = None,
        ci: str | None = None,
        author: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[dict[str, Any]], int]:
        rows = list(self.pulls.values())
        return rows, len(rows)


class FakeStore(OpsRunStore):
    def __init__(self) -> None:  # type: ignore[override]
        self.runs: dict[str, dict[str, Any]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {}
        self._counter = 0

    def create_run(
        self, query: str, route: str, repo_owner: str = "MoonshotAI", repo_name: str = "kimi-code", session_id: str | None = None
    ) -> dict[str, Any]:
        self._counter += 1
        run_id = f"run-{self._counter}"
        run = {
            "id": run_id,
            "repo_id": "repo-1",
            "query": query,
            "route": route,
            "status": "running" if route == "deep" else "done",
            "session_id": session_id,
            "retry_token": f"token-{self._counter}",
        }
        self.runs[run_id] = run
        self.events[run_id] = []
        return run

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        return self.runs.get(run_id)

    def update_run(self, run_id: str, **fields: Any) -> None:
        if run_id in self.runs:
            self.runs[run_id].update(fields)

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
            seq = len(self.events.get(run_id, [])) + 1
        evt = {
            "run_id": run_id,
            "seq": seq,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
        }
        self.events.setdefault(run_id, []).append(evt)
        return evt

    def get_events(self, run_id: str, after_seq: int = 0, limit: int = 200) -> list[dict[str, Any]]:
        return [e for e in self.events.get(run_id, []) if e["seq"] > after_seq][:limit]

    def next_seq(self, run_id: str) -> int:
        return len(self.events.get(run_id, [])) + 1


class FakeDemoCacheStore(DemoCacheStore):
    """不访问 Supabase 的内存 DemoCache；保留 classifier。"""

    def __init__(self, initial: dict[str, dict[str, Any]] | None = None) -> None:  # type: ignore[override]
        self.cache = initial or {}
        self.classifier = DemoClassifier()

    def get(self, demo_id: str) -> dict[str, Any] | None:
        row = self.cache.get(demo_id)
        if not row:
            return None
        expires_at = row.get("expires_at")
        if expires_at and self._is_expired(expires_at):
            return None
        return row

    def set(
        self,
        demo_id: str,
        answer_json: dict[str, Any],
        query_template: str | None = None,
        params: dict[str, Any] | None = None,
        ttl_hours: float = 24,
        source_sync_run_id: str | None = None,
    ) -> dict[str, Any]:
        self.cache[demo_id] = {
            "demo_id": demo_id,
            "query_template": query_template or demo_id,
            "params": params or {},
            "answer_json": answer_json,
            "expires_at": (datetime.now(timezone.utc) + timedelta(hours=ttl_hours)).isoformat(),
        }
        return self.cache[demo_id]

    def delete(self, demo_id: str) -> None:
        self.cache.pop(demo_id, None)


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    fake_queries = FakeQueries()
    fake_store = FakeStore()
    fake_demo_cache = FakeDemoCacheStore()

    app.dependency_overrides[chat._queries] = lambda: fake_queries
    app.dependency_overrides[chat._store] = lambda: fake_store
    app.dependency_overrides[chat._demo_cache] = lambda: fake_demo_cache

    llm_calls: list[dict[str, Any]] = []

    def fake_chat_completion(messages: list[dict[str, str]], temperature: float = 0.3, **kwargs: Any) -> Any:
        llm_calls.append({"messages": messages})
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content='{"reasoning": "分析完成", "suggestion": "建议参与", "confidence": 0.85, "citations": [{"number": 545, "url": "https://github.com/MoonshotAI/kimi-code/issues/545"}]}',
            usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=10, completion_tokens=5, total_tokens=15, latency_ms=100, step="analyze"),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        llm_calls.append({"query": query})
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        return LlmCompletionResult(
            content="综合建议：#545 值得参与。",
            usage=LlmUsage(provider="siliconflow", model="Qwen/Qwen2.5-72B-Instruct", prompt_tokens=8, completion_tokens=4, total_tokens=12, latency_ms=80, step="synthesize"),
        )

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    test_client = TestClient(app)
    test_client.llm_calls = llm_calls  # type: ignore[attr-defined]
    test_client.fake_demo_cache = fake_demo_cache  # type: ignore[attr-defined]
    test_client.fake_store = fake_store  # type: ignore[attr-defined]

    yield test_client
    app.dependency_overrides.clear()


def test_classifier_matches_demos() -> None:
    classifier = DemoClassifier()
    assert classifier.classify("kimi-code 最近 30 天 open issue 有多少？")["demo_id"] == "D1"
    assert classifier.classify("PR cycle time 最近 30 天趋势如何？")["demo_id"] == "D2"
    assert classifier.classify("PR review time 中位数是多少？")["demo_id"] == "D3"
    assert classifier.classify("#545 适合我做吗？")["demo_id"] == "D4"
    assert classifier.classify(" totally unrelated ") is None


def test_demo_cache_hit_d1_no_llm(client: TestClient) -> None:
    client.fake_demo_cache.set("D1", {"answer": "D1 cached", "metric": "issue-throughput"})
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "kimi-code 最近 30 天 open issue 有多少？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "fast"
    assert data["status"] == "done"
    assert data["demo_hit"] is True
    assert data["demo_id"] == "D1"
    assert data["answer"] == "D1 cached"
    assert len(client.llm_calls) == 0


def test_demo_cache_hit_d4_no_llm(client: TestClient) -> None:
    client.fake_demo_cache.set("D4", {"answer": "D4 cached", "issue_number": 545})
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我做吗？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "fast"
    assert data["status"] == "done"
    assert data["demo_hit"] is True
    assert data["demo_id"] == "D4"
    assert data["answer"] == "D4 cached"
    assert len(client.llm_calls) == 0


def test_demo_cache_miss_d1_writes_back(client: TestClient) -> None:
    assert "D1" not in client.fake_demo_cache.cache
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "kimi-code 最近 30 天 open issue 有多少？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "fast"
    assert data["status"] == "done"
    assert data["demo_hit"] is False
    assert data["demo_id"] == "D1"
    assert "answer" in data

    cached = client.fake_demo_cache.cache.get("D1")
    assert cached is not None
    assert cached["answer_json"]["answer"] == data["answer"]
    assert len(client.llm_calls) == 0
    assert "closed issue 共 42 个" in data["answer"]
    assert "cycle-time" not in data["answer"]


def test_demo_cache_miss_d2_single_metric_answer(client: TestClient) -> None:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "PR review time 中位数是多少？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["demo_id"] == "D3"
    assert data["demo_hit"] is False
    assert "review time 中位数 10.5 小时" in data["answer"]
    assert "cycle-time" not in data["answer"]


def test_demo_cache_miss_d4_deep_then_hit(client: TestClient) -> None:
    assert "D4" not in client.fake_demo_cache.cache

    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我做吗？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "deep"
    assert data["status"] in ("done", "partial")
    assert data["demo_hit"] is False
    assert data["demo_id"] == "D4"
    assert "answer" in data
    assert len(client.llm_calls) > 0

    # second request should hit cache
    client.llm_calls.clear()
    resp2 = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我做吗？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["route"] == "fast"
    assert data2["status"] == "done"
    assert data2["demo_hit"] is True
    assert data2["demo_id"] == "D4"
    assert data2["answer"] == data["answer"]
    assert len(client.llm_calls) == 0


def test_demo_cache_ttl_expire_falls_back(client: TestClient) -> None:
    client.fake_demo_cache.cache["D4"] = {
        "demo_id": "D4",
        "answer_json": {"answer": "expired"},
        "expires_at": (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat(),
    }

    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "#545 适合我做吗？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "deep"
    assert data["demo_hit"] is False
    assert len(client.llm_calls) > 0


def test_non_demo_still_uses_normal_intent(client: TestClient) -> None:
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "指标趋势"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["route"] == "fast"
    assert data["status"] == "done"
    assert "demo_id" not in data
    assert len(client.llm_calls) == 0


def test_demo_event_logged_on_hit(client: TestClient) -> None:
    client.fake_demo_cache.set("D2", {"answer": "D2 cached", "metric": "cycle-time"})
    resp = client.post(
        "/api/py/ops/chat/messages",
        json={"message": "PR cycle time 最近 30 天趋势如何？"},
        headers={"x-ops-secret": "test"},
    )
    assert resp.status_code == 200
    run_id = resp.json()["run_id"]
    event_types = [e["event_type"] for e in client.fake_store.events.get(run_id, [])]
    assert "demo.cache.hit" in event_types
    assert "run.end" in event_types
