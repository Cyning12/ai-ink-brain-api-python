"""P1-1: ops_run_artifacts 与 save_artifact 单测。"""

from __future__ import annotations

from typing import Any

import pytest

from api.ops.react_loop import run_react_fallback
from tests.ops_desk._llm_mocks import patch_ops_llm_imports


class FakeArtifactStore:
    """内存版 Artifact 存储，支持 save/list/events。"""

    def __init__(self) -> None:
        self.artifacts: dict[tuple[str, str], dict[str, Any]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {}
        self.runs: dict[str, dict[str, Any]] = {}
        self._fail_artifacts = False
        self._artifact_counter = 0

    def save_artifact(
        self, run_id: str, kind: str, payload: dict[str, Any], max_retries: int = 3
    ) -> dict[str, Any]:
        if self._fail_artifacts:
            raise RuntimeError("supabase connection refused")
        self._artifact_counter += 1
        row = {
            "id": f"art-{self._artifact_counter}",
            "run_id": run_id,
            "kind": kind,
            "payload": dict(payload),
            "created_at": "2026-07-09T16:22:00Z",
        }
        self.artifacts[(run_id, kind)] = row
        return row

    def list_artifacts(self, run_id: str) -> list[dict[str, Any]]:
        return [a for a in self.artifacts.values() if a["run_id"] == run_id]

    def append_event(
        self,
        run_id: str,
        agent_role: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
        seq: int | None = None,
    ) -> dict[str, Any]:
        evt: dict[str, Any] = {
            "run_id": run_id,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
        }
        self.events.setdefault(run_id, []).append(evt)
        return evt

    def update_run(self, run_id: str, **fields: Any) -> None:
        self.runs.setdefault(run_id, {}).update(fields)

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        self.update_run(run_id, metrics_json=metrics_json)


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


class FakeReactQueries(FakeQueries):
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
        return [], 0

    def cycle_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "cycle-time", "summary": {"avg_hours": 48.0}}

    def review_time_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "review-time", "summary": {"avg_hours": 12.0}}

    def issue_throughput_metric(self, days: int = 30) -> dict[str, Any]:
        return {"metric": "issue-throughput", "summary": {"total": 2}}

    def sync_status(self) -> dict[str, Any]:
        return {"status": "ok", "cursor": "c1", "as_of": "2026-06-25T00:00:00Z"}


@pytest.fixture
def store() -> FakeArtifactStore:
    return FakeArtifactStore()


# ---------------------------------------------------------------------------
# save_artifact 单元行为
# ---------------------------------------------------------------------------


def test_save_artifact_success_and_read_by_run_id(store: FakeArtifactStore) -> None:
    from api.ops.store.artifacts import save_artifact

    row = save_artifact("run-1", "deep.final_answer", {"answer": "hello"}, store=store)

    assert row["run_id"] == "run-1"
    assert row["kind"] == "deep.final_answer"
    assert row["payload"] == {"answer": "hello"}
    assert "created_at" in row
    assert "id" in row

    artifacts = store.list_artifacts("run-1")
    assert len(artifacts) == 1
    assert artifacts[0]["payload"]["answer"] == "hello"


def test_save_artifact_schema_fields(store: FakeArtifactStore) -> None:
    from api.ops.store.artifacts import save_artifact

    row = save_artifact("run-2", "kind.x", {"x": 1}, store=store)
    assert set(row.keys()) >= {"id", "run_id", "kind", "payload", "created_at"}


def test_save_artifact_idempotent_upsert(store: FakeArtifactStore) -> None:
    from api.ops.store.artifacts import save_artifact

    save_artifact("run-3", "deep.final_answer", {"answer": "first"}, store=store)
    save_artifact("run-3", "deep.final_answer", {"answer": "second"}, store=store)

    artifacts = store.list_artifacts("run-3")
    assert len(artifacts) == 1
    assert artifacts[0]["payload"]["answer"] == "second"


def test_save_artifact_raises_after_retries(store: FakeArtifactStore) -> None:
    from api.ops.store.artifacts import ArtifactStoreError, save_artifact

    store._fail_artifacts = True
    with pytest.raises(ArtifactStoreError):
        save_artifact("run-fail", "deep.final_answer", {"answer": "x"}, store=store, max_retries=2)


# ---------------------------------------------------------------------------
# 失败路径：artifact 写失败记录 event
# ---------------------------------------------------------------------------


def test_save_artifact_failure_records_write_failed_event(store: FakeArtifactStore) -> None:
    from api.ops.store.artifacts import save_artifact_with_failure_event

    store._fail_artifacts = True
    result = save_artifact_with_failure_event(
        "run-fail", "deep.final_answer", {"answer": "x"}, store=store
    )

    assert result is None
    events = store.events["run-fail"]
    fail_events = [e for e in events if e["event_type"] == "artifact.write_failed"]
    assert len(fail_events) == 1
    assert fail_events[0]["payload"]["kind"] == "deep.final_answer"
    assert "error" in fail_events[0]["payload"]


# ---------------------------------------------------------------------------
# deep / ReAct 路径调用 save_artifact
# ---------------------------------------------------------------------------


def _fake_deep_llm_result() -> Any:
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    return LlmCompletionResult(
        content='{"reasoning":"分析完成","suggestion":"建议参与","confidence":0.85,"citations":[{"number":545,"url":"https://github.com/MoonshotAI/kimi-code/issues/545"}]}',
        usage=LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            latency_ms=100,
            step="analyze",
        ),
    )


def _fake_synth_result(content: str = "综合建议。") -> Any:
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    return LlmCompletionResult(
        content=content,
        usage=LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=8,
            completion_tokens=4,
            total_tokens=12,
            latency_ms=80,
            step="synthesize",
        ),
    )


def test_run_deep_saves_final_answer_artifact(
    monkeypatch: pytest.MonkeyPatch, store: FakeArtifactStore
) -> None:
    from api.ops.orchestrator.core import run_deep

    queries = FakeQueries()

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=lambda *args, **kwargs: _fake_deep_llm_result(),
        synthesize_answer=lambda *args, **kwargs: _fake_synth_result("综合建议：#545 值得参与。"),
        synthesize=lambda *args, **kwargs: ("综合建议：#545 值得参与。", None),
    )

    result = run_deep("run-deep", "#545 适合我吗", {"issue_number": 545}, store, queries)

    assert result["answer"]
    artifacts = store.list_artifacts("run-deep")
    assert any(a["kind"] == "deep.final_answer" for a in artifacts)
    art = next(a for a in artifacts if a["kind"] == "deep.final_answer")
    assert art["payload"]["answer"] == result["answer"]
    assert art["payload"]["agent"] == "issue_analyst"


def test_run_deep_artifact_failure_records_write_failed_event(
    monkeypatch: pytest.MonkeyPatch, store: FakeArtifactStore
) -> None:
    from api.ops.orchestrator.core import run_deep

    store._fail_artifacts = True
    queries = FakeQueries()

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=lambda *args, **kwargs: _fake_deep_llm_result(),
        synthesize_answer=lambda *args, **kwargs: _fake_synth_result("综合建议：#545 值得参与。"),
        synthesize=lambda *args, **kwargs: ("综合建议：#545 值得参与。", None),
    )

    result = run_deep("run-deep-fail", "#545 适合我吗", {"issue_number": 545}, store, queries)

    assert result["answer"]
    events = store.events["run-deep-fail"]
    fail_events = [e for e in events if e["event_type"] == "artifact.write_failed"]
    assert len(fail_events) == 1
    assert fail_events[0]["payload"]["kind"] == "deep.final_answer"


def test_run_react_saves_final_answer_artifact(
    monkeypatch: pytest.MonkeyPatch, store: FakeArtifactStore
) -> None:
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    queries = FakeReactQueries()

    def final_answer_chat(*args: Any, **kwargs: Any) -> Any:
        return LlmCompletionResult(
            content='{"thought":"直接回答","final_answer":"这是一个直接答案。"}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step="react",
            ),
        )

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=final_answer_chat,
        synthesize_answer=lambda *args, **kwargs: _fake_synth_result("综合建议。"),
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    result = run_react_fallback("run-react", "hello", store, queries, max_steps=2)

    assert result["answer"]
    artifacts = store.list_artifacts("run-react")
    assert any(a["kind"] == "react.final_answer" for a in artifacts)
    art = next(a for a in artifacts if a["kind"] == "react.final_answer")
    assert art["payload"]["answer"] == result["answer"]


def test_run_react_artifact_failure_records_write_failed_event(
    monkeypatch: pytest.MonkeyPatch, store: FakeArtifactStore
) -> None:
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    store._fail_artifacts = True
    queries = FakeReactQueries()

    def final_answer_chat(*args: Any, **kwargs: Any) -> Any:
        return LlmCompletionResult(
            content='{"thought":"直接回答","final_answer":"这是一个直接答案。"}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step="react",
            ),
        )

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=final_answer_chat,
        synthesize_answer=lambda *args, **kwargs: _fake_synth_result("综合建议。"),
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    result = run_react_fallback("run-react-fail", "hello", store, queries, max_steps=2)

    assert result["answer"]
    events = store.events["run-react-fail"]
    fail_events = [e for e in events if e["event_type"] == "artifact.write_failed"]
    assert len(fail_events) == 1
    assert fail_events[0]["payload"]["kind"] == "react.final_answer"


# ---------------------------------------------------------------------------
# Migration SQL 字段覆盖
# ---------------------------------------------------------------------------


def test_migration_sql_contains_required_fields() -> None:
    from pathlib import Path

    sql_path = Path(__file__).parents[2] / "supabase" / "sql" / "ops_desk_p1_artifacts.sql"
    sql = sql_path.read_text(encoding="utf-8")
    assert "CREATE TABLE IF NOT EXISTS public.ops_run_artifacts" in sql
    assert "run_id uuid" in sql
    assert "kind text" in sql
    assert "payload jsonb" in sql
    assert "created_at timestamptz" in sql
    assert "REFERENCES public.ops_runs(id)" in sql

    rollback_path = Path(__file__).parents[2] / "supabase" / "sql" / "ops_desk_p1_artifacts_rollback.sql"
    rollback = rollback_path.read_text(encoding="utf-8")
    assert "DROP TABLE IF EXISTS public.ops_run_artifacts" in rollback
