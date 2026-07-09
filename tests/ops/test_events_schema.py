"""P0-2: ops run events schema v1 与 append_event 辅助函数单测。"""

from __future__ import annotations

from typing import Any

import pytest


class FakeOpsRunStore:
    """内存版 OpsRunStore，仅记录 append_event 调用并返回带 id 的行。"""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self._seq = 0

    def append_event(
        self,
        run_id: str,
        agent_role: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
        seq: int | None = None,
    ) -> dict[str, Any]:
        self._seq += 1
        row = {
            "id": f"evt_{self._seq}",
            "run_id": run_id,
            "seq": seq or self._seq,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
        }
        self.events.append(row)
        return row


@pytest.fixture
def fake_store() -> FakeOpsRunStore:
    return FakeOpsRunStore()


def test_schema_version_constant_exists() -> None:
    from api.ops.events_schema import SCHEMA_VERSION

    assert SCHEMA_VERSION == "v1"


def test_handoff_payload_structure() -> None:
    from api.ops.events_schema import handoff_payload

    payload = handoff_payload(
        from_route="classify",
        to_route="deep",
        intent="issue_contribution",
        slots={"issue_number": 545},
        agent="issue_analyst",
    )
    assert payload["schema_version"] == "v1"
    assert payload["from_route"] == "classify"
    assert payload["to_route"] == "deep"
    assert payload["intent"] == "issue_contribution"
    assert payload["slots"] == {"issue_number": 545}
    assert payload["agent"] == "issue_analyst"


def test_review_payload_structure() -> None:
    from api.ops.events_schema import review_payload

    payload = review_payload(
        verdict="pass",
        rule="V4",
        message="置信度足够",
        attempt=1,
    )
    assert payload["schema_version"] == "v1"
    assert payload["verdict"] == "pass"
    assert payload["rule"] == "V4"
    assert payload["message"] == "置信度足够"
    assert payload["attempt"] == 1


def test_append_event_wraps_schema_version(fake_store: FakeOpsRunStore) -> None:
    from api.ops.store.runs import append_event

    row = append_event(
        "run-123",
        "handoff",
        {"from_route": "classify", "to_route": "deep"},
        store=fake_store,
    )
    assert row["run_id"] == "run-123"
    assert row["agent_role"] == "orchestrator"
    assert row["event_type"] == "handoff"
    assert row["payload"]["schema_version"] == "v1"
    assert row["payload"]["from_route"] == "classify"


def test_append_event_review_kind(fake_store: FakeOpsRunStore) -> None:
    from api.ops.store.runs import append_event

    row = append_event(
        "run-456",
        "review",
        {"verdict": "partial", "rule": "V4", "message": "低置信", "attempt": 0},
        store=fake_store,
    )
    assert row["agent_role"] == "review"
    assert row["event_type"] == "review"
    assert row["payload"]["schema_version"] == "v1"
    assert row["payload"]["verdict"] == "partial"


def test_append_event_preserves_existing_schema_version(fake_store: FakeOpsRunStore) -> None:
    from api.ops.store.runs import append_event

    row = append_event(
        "run-789",
        "handoff",
        {"schema_version": "v1", "to_route": "react"},
        store=fake_store,
    )
    assert row["payload"]["schema_version"] == "v1"


def test_append_event_default_store_uses_supabase_client(monkeypatch: Any) -> None:
    """未传 store 时，append_event 应通过 supabase_client() 构造 OpsRunStore 并写入。"""
    from api.ops.store import runs as runs_module
    from api.ops.store.runs import OpsRunStore, append_event

    class FakeResult:
        data = [{"id": "real-1"}]

    class FakeQuery:
        def select(self, *_args, count=None):
            return self

        def eq(self, *_args):
            return self

        def order(self, *_args, **kwargs):
            return self

        def limit(self, *_args):
            return self

        def insert(self, _row):
            return self

        def execute(self):
            return FakeResult()

    class FakeClient:
        def table(self, _name: str):
            return FakeQuery()

    fake_client = FakeClient()

    def fake_supabase_client() -> Any:
        return fake_client

    monkeypatch.setattr(runs_module, "supabase_client", fake_supabase_client)

    original_init = OpsRunStore.__init__
    captured: dict[str, Any] = {}

    def patched_init(self: Any, client: Any) -> None:
        captured["client"] = client
        original_init(self, client)

    monkeypatch.setattr(OpsRunStore, "__init__", patched_init)

    row = append_event("run-abc", "handoff", {"to_route": "deep"})
    assert row is not None
    assert captured["client"] is fake_client
    assert row["id"] == "real-1"


@pytest.mark.skip(reason="需要真实 Supabase 连接；本地/CI 环境缺失时跳过")
def test_append_event_integration_with_real_store() -> None:
    """真实存储读写验证；默认跳过，避免阻塞本地无连接环境。"""
    from api.ops.store.runs import OpsRunStore, append_event
    from api.rag_env import supabase_client

    store = OpsRunStore(supabase_client())
    row = append_event(
        "run-integration",
        "handoff",
        {"from_route": "classify", "to_route": "deep", "intent": "test"},
        store=store,
    )
    assert row["id"]
    events = store.get_events(row["run_id"])
    assert any(e["event_type"] == "handoff" for e in events)
