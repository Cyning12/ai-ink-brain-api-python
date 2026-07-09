"""P1-2: ops_run_checkpoints 与 ReAct 续跑单测。"""

from __future__ import annotations

from typing import Any

import pytest

from api.ops.react_loop import run_react_fallback
from tests.ops_desk._llm_mocks import patch_ops_llm_imports


class FakeCheckpointStore:
    """内存版 Checkpoint 存储，支持 save/load/按 session 查找。"""

    def __init__(self) -> None:
        self.checkpoints: dict[tuple[str, str], dict[str, Any]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {}
        self.runs: dict[str, dict[str, Any]] = {}
        self._checkpoint_counter = 0

    def save_checkpoint(
        self, run_id: str, checkpoint_id: str, state_json: dict[str, Any]
    ) -> dict[str, Any]:
        self._checkpoint_counter += 1
        row = {
            "id": f"chk-{self._checkpoint_counter}",
            "run_id": run_id,
            "checkpoint_id": checkpoint_id,
            "state_json": dict(state_json),
            "created_at": f"2026-07-09T17:33:{self._checkpoint_counter:02d}Z",
        }
        self.checkpoints[(run_id, checkpoint_id)] = row
        return row

    def load_checkpoint(self, run_id: str, checkpoint_id: str) -> dict[str, Any] | None:
        row = self.checkpoints.get((run_id, checkpoint_id))
        if not row:
            return None
        return dict(row)

    def find_latest_checkpoint_for_session(self, session_id: str) -> dict[str, Any] | None:
        """模拟按 checkpoint_id=session_id 取最新一条（跨 run）。"""
        candidates = [
            row for (_run_id, cp_id), row in self.checkpoints.items() if cp_id == session_id
        ]
        if not candidates:
            return None
        # 按 created_at 降序（字符串即可，时间戳格式一致）
        latest = max(candidates, key=lambda r: r["created_at"])
        return dict(latest)

    def get_run(self, run_id: str) -> dict[str, Any] | None:
        return self.runs.get(run_id)

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

    def list_runs_by_session_id(self, session_id: str, *, limit: int = 50) -> list[dict[str, Any]]:
        return [r for r in self.runs.values() if r.get("session_id") == session_id][:limit]


class FakeReactQueries:
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
def store() -> FakeCheckpointStore:
    return FakeCheckpointStore()


# ---------------------------------------------------------------------------
# save_checkpoint / load_checkpoint 单元行为
# ---------------------------------------------------------------------------


def test_save_checkpoint_success_and_read(store: FakeCheckpointStore) -> None:
    from api.ops.store.checkpoints import load_checkpoint, save_checkpoint

    state = {"step": 1, "messages": [{"role": "user", "content": "hi"}]}
    row = save_checkpoint("run-1", "thread-1", state, store=store)

    assert row["run_id"] == "run-1"
    assert row["checkpoint_id"] == "thread-1"
    assert row["state_json"] == state
    assert "id" in row
    assert "created_at" in row

    loaded = load_checkpoint("run-1", "thread-1", store=store)
    assert loaded == state


def test_load_checkpoint_returns_none_when_missing(store: FakeCheckpointStore) -> None:
    from api.ops.store.checkpoints import load_checkpoint

    assert load_checkpoint("run-x", "thread-x", store=store) is None


def test_find_latest_checkpoint_for_session(store: FakeCheckpointStore) -> None:
    from api.ops.store.checkpoints import find_latest_checkpoint_for_session

    save = store.save_checkpoint
    save("run-a", "sess-1", {"step": 1})
    save("run-b", "sess-1", {"step": 2})
    save("run-c", "sess-2", {"step": 3})

    latest = find_latest_checkpoint_for_session("sess-1", store=store)
    assert latest is not None
    assert latest["run_id"] == "run-b"
    assert latest["state_json"] == {"step": 2}

    assert find_latest_checkpoint_for_session("sess-none", store=store) is None


# ---------------------------------------------------------------------------
# ReAct 路径：checkpoint 损坏时冷启动且不 500
# ---------------------------------------------------------------------------


def _final_answer_chat(content: str = '{"thought":"直接回答","final_answer":"完成"}') -> Any:
    from api.ops.llm.types import LlmCompletionResult, LlmUsage

    def _chat(*args: Any, **kwargs: Any) -> Any:
        return LlmCompletionResult(
            content=content,
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

    return _chat


def test_checkpoint_corrupted_cold_start_records_event(
    monkeypatch: pytest.MonkeyPatch, store: FakeCheckpointStore
) -> None:
    """损坏 checkpoint → 新 run 冷启动、不抛 500、记录 checkpoint.corrupted event。"""

    def _bad_checkpoint(*args: Any, **kwargs: Any) -> dict[str, Any] | None:
        return {
            "run_id": "run-prev",
            "checkpoint_id": "sess-corrupt",
            "state_json": {"foo": "bar"},
            "created_at": "2026-07-09T17:33:00Z",
        }

    monkeypatch.setattr(
        "api.ops.react_loop.find_latest_checkpoint_for_session", _bad_checkpoint
    )
    monkeypatch.setattr("api.ops.react_loop.load_chat_transcript", lambda *args, **kwargs: [])

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=_final_answer_chat(),
        synthesize_answer=lambda *args, **kwargs: ("综合建议。", None),
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    result = run_react_fallback(
        "run-corrupt", "hello", store, FakeReactQueries(), session_id="sess-corrupt", max_steps=2
    )

    assert result["answer"]
    assert result["status"] in ("done", "partial")
    events = store.events["run-corrupt"]
    corrupted = [e for e in events if e["event_type"] == "checkpoint.corrupted"]
    assert len(corrupted) == 1
    assert corrupted[0]["payload"].get("session_id") == "sess-corrupt"
    assert "error" in corrupted[0]["payload"]

    # 冷启动应出现 router.decision / run.start 等正常事件
    assert any(e["event_type"] == "run.start" for e in events)


def test_checkpoint_corrupted_with_invalid_state_schema(
    monkeypatch: pytest.MonkeyPatch, store: FakeCheckpointStore
) -> None:
    """state_json 缺少关键字段同样视为 corrupted。"""

    def _bad_checkpoint(*args: Any, **kwargs: Any) -> dict[str, Any] | None:
        return {
            "run_id": "run-prev",
            "checkpoint_id": "sess-missing",
            "state_json": {
                "route": "react",
                "query": "hello",
                # 缺少 step / messages / tool_evidence
            },
            "created_at": "2026-07-09T17:33:00Z",
        }

    monkeypatch.setattr(
        "api.ops.react_loop.find_latest_checkpoint_for_session", _bad_checkpoint
    )
    monkeypatch.setattr("api.ops.react_loop.load_chat_transcript", lambda *args, **kwargs: [])

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=_final_answer_chat(),
        synthesize_answer=lambda *args, **kwargs: ("综合建议。", None),
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    result = run_react_fallback(
        "run-missing", "hello", store, FakeReactQueries(), session_id="sess-missing", max_steps=2
    )

    assert result["answer"]
    corrupted = [e for e in store.events["run-missing"] if e["event_type"] == "checkpoint.corrupted"]
    assert len(corrupted) == 1


# ---------------------------------------------------------------------------
# ReAct 路径：同 session 续跑完成
# ---------------------------------------------------------------------------


def test_same_session_resumes_from_checkpoint(
    monkeypatch: pytest.MonkeyPatch, store: FakeCheckpointStore
) -> None:
    """第一跑被 max_steps 中断并落 checkpoint；同 session 第二跑隐式恢复并完成。"""

    responses = [
        # 第一跑 step 1：调用工具
        '{"thought":"搜索相关 issue","tool":"fetch_issues","arguments":{}}',
        # 第二跑恢复后：直接给出最终答案
        '{"thought":"基于结果回答","final_answer":"已完成续跑"}',
    ]
    call_index = 0

    def _sequenced_chat(*args: Any, **kwargs: Any) -> Any:
        nonlocal call_index
        from api.ops.llm.types import LlmCompletionResult, LlmUsage

        content = responses[call_index]
        call_index += 1
        return LlmCompletionResult(
            content=content,
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
        chat_completion=_sequenced_chat,
        synthesize_answer=lambda *args, **kwargs: ("综合建议。", None),
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    # 为了隔离 checkpoint 行为，不加载历史 transcript
    import api.ops.react_loop

    original_load_transcript = api.ops.react_loop.load_chat_transcript
    api.ops.react_loop.load_chat_transcript = lambda *args, **kwargs: []  # type: ignore[assignment]

    try:
        # 第一跑：max_steps=1，执行一步工具后中断，留下 checkpoint
        result1 = run_react_fallback(
            "run-1", "hello", store, FakeReactQueries(), session_id="sess-resume", max_steps=1
        )
        assert result1["answer"]
        assert any(
            e["event_type"] == "agent.tool_call" for e in store.events["run-1"]
        )
        assert ("run-1", "sess-resume") in store.checkpoints

        # 第二跑：同 session，应恢复 checkpoint 并一步完成
        result2 = run_react_fallback(
            "run-2", "hello", store, FakeReactQueries(), session_id="sess-resume", max_steps=3
        )
        assert result2["answer"] == "已完成续跑"

        resume_events = [e for e in store.events["run-2"] if e["event_type"] == "checkpoint.resume"]
        assert len(resume_events) == 1
        assert resume_events[0]["payload"].get("from_run_id") == "run-1"
        assert resume_events[0]["payload"].get("step") == 1

        # 续跑应直接使用 checkpoint 中的 tool_evidence，无需再次 tool_call
        assert not any(
            e["event_type"] == "agent.tool_call" for e in store.events["run-2"]
        )
    finally:
        api.ops.react_loop.load_chat_transcript = original_load_transcript  # type: ignore[assignment]


# ---------------------------------------------------------------------------
# 失败路径硬性检查：checkpoint.corrupted 验证命令
# ---------------------------------------------------------------------------


def test_checkpoint_corrupted_failure_path_verification(
    monkeypatch: pytest.MonkeyPatch, store: FakeCheckpointStore
) -> None:
    """task §失败路径验证命令：`pytest tests/ops/test_checkpoint.py -k corrupted`。"""

    def _bad_checkpoint(*args: Any, **kwargs: Any) -> dict[str, Any] | None:
        return {
            "run_id": "run-prev",
            "checkpoint_id": "sess-verify",
            "state_json": "not-a-dict",
            "created_at": "2026-07-09T17:33:00Z",
        }

    monkeypatch.setattr(
        "api.ops.react_loop.find_latest_checkpoint_for_session", _bad_checkpoint
    )
    monkeypatch.setattr("api.ops.react_loop.load_chat_transcript", lambda *args, **kwargs: [])

    patch_ops_llm_imports(
        monkeypatch,
        chat_completion=_final_answer_chat(),
        synthesize_answer=lambda *args, **kwargs: ("综合建议。", None),
        synthesize=lambda *args, **kwargs: ("综合建议。", None),
    )

    result = run_react_fallback(
        "run-verify", "hello", store, FakeReactQueries(), session_id="sess-verify", max_steps=2
    )

    assert result["answer"]
    corrupted = [e for e in store.events["run-verify"] if e["event_type"] == "checkpoint.corrupted"]
    assert len(corrupted) == 1
    assert corrupted[0]["payload"].get("session_id") == "sess-verify"
