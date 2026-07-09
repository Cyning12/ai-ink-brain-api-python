"""P0-3: Ops Chat 多轮 Transcript 上下文单测与集成测。

覆盖：
- load_chat_transcript 读取最近 N 轮（每轮 user + assistant）。
- 空 session / 无 session_id 时返回空列表。
- deep / ReAct 路径透传 session_id 并注入上下文（mock store + mock LLM）。
"""

from __future__ import annotations

from typing import Any

import pytest


class FakeTranscriptStore:
    """内存版 OpsRunStore，支持 list_runs_by_session_id / get_events / append_event。"""

    def __init__(self) -> None:
        self.runs: dict[str, dict[str, Any]] = {}
        self.events: dict[str, list[dict[str, Any]]] = {}
        self._counter = 0

    def create_run(
        self,
        query: str,
        route: str,
        repo_owner: str = "MoonshotAI",
        repo_name: str = "kimi-code",
        session_id: str | None = None,
    ) -> dict[str, Any]:
        self._counter += 1
        run_id = f"run-{self._counter}"
        self.runs[run_id] = {
            "id": run_id,
            "repo_id": "repo-1",
            "query": query,
            "route": route,
            "status": "running",
            "session_id": session_id,
            "created_at": f"2026-07-09T12:{self._counter:02d}:00Z",
        }
        self.events[run_id] = []
        return self.runs[run_id]

    def add_final_answer(self, run_id: str, answer: str) -> None:
        self.events.setdefault(run_id, []).append(
            {
                "run_id": run_id,
                "seq": len(self.events.get(run_id, [])) + 1,
                "agent_role": "orchestrator",
                "event_type": "final.answer",
                "payload": {"answer": answer},
                "node_id": "synthesize",
            }
        )

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
            "seq": seq or len(self.events.get(run_id, [])) + 1,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
        }
        self.events.setdefault(run_id, []).append(evt)
        return evt

    def list_runs_by_session_id(self, session_id: str, *, limit: int = 50) -> list[dict[str, Any]]:
        runs = [r for r in self.runs.values() if r.get("session_id") == session_id]
        # Newest first (DB order)
        return sorted(runs, key=lambda r: r["created_at"], reverse=True)[:limit]

    def get_events(self, run_id: str, after_seq: int = 0, limit: int = 200) -> list[dict[str, Any]]:
        return [e for e in self.events.get(run_id, []) if e["seq"] > after_seq][:limit]

    def update_run(self, run_id: str, **fields: Any) -> None:
        if run_id in self.runs:
            self.runs[run_id].update(fields)

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        if run_id in self.runs:
            self.runs[run_id]["metrics_json"] = metrics_json


@pytest.fixture
def fake_store() -> FakeTranscriptStore:
    return FakeTranscriptStore()


# -----------------------------------------------------------------------------
# load_chat_transcript 单测
# -----------------------------------------------------------------------------


def test_load_chat_transcript_returns_recent_n_rounds(fake_store: FakeTranscriptStore) -> None:
    """最近 N 轮 = N 个 user/assistant 消息对。"""
    from api.ops.chat_context import load_chat_transcript

    session_id = "sess-abc"
    for i in range(4):
        run = fake_store.create_run(query=f"问题{i}", route="deep", session_id=session_id)
        fake_store.add_final_answer(run["id"], f"答案{i}")

    transcript = load_chat_transcript(session_id, n=2, store=fake_store)

    assert len(transcript) == 4
    assert transcript[0] == {"role": "user", "content": "问题2"}
    assert transcript[1] == {"role": "assistant", "content": "答案2"}
    assert transcript[2] == {"role": "user", "content": "问题3"}
    assert transcript[3] == {"role": "assistant", "content": "答案3"}


def test_load_chat_transcript_ignores_incomplete_runs(fake_store: FakeTranscriptStore) -> None:
    """缺少 final.answer 的 run 不计入 transcript。"""
    from api.ops.chat_context import load_chat_transcript

    session_id = "sess-incomplete"
    run1 = fake_store.create_run(query="有答案", route="deep", session_id=session_id)
    fake_store.add_final_answer(run1["id"], "答复")
    fake_store.create_run(query="无答案", route="deep", session_id=session_id)

    transcript = load_chat_transcript(session_id, n=10, store=fake_store)

    assert len(transcript) == 2
    assert transcript[0]["content"] == "有答案"
    assert transcript[1]["content"] == "答复"


def test_load_chat_transcript_empty_session(fake_store: FakeTranscriptStore) -> None:
    """session 存在但无 run 时返回空列表。"""
    from api.ops.chat_context import load_chat_transcript

    transcript = load_chat_transcript("sess-empty", n=10, store=fake_store)
    assert transcript == []


def test_load_chat_transcript_no_session_id(fake_store: FakeTranscriptStore, caplog: Any) -> None:
    """无 session_id 时 transcript 为空且不抛异常；有 debug 日志。"""
    from api.ops.chat_context import load_chat_transcript

    with caplog.at_level("DEBUG"):
        transcript = load_chat_transcript(None, n=10, store=fake_store)

    assert transcript == []
    assert "chat_context.no_session_id" in caplog.text


def test_load_chat_transcript_default_n_is_six_rounds(fake_store: FakeTranscriptStore) -> None:
    """默认 n=6 返回最多 6 轮（12 条消息）。"""
    from api.ops.chat_context import load_chat_transcript

    session_id = "sess-many"
    for i in range(10):
        run = fake_store.create_run(query=f"q{i}", route="deep", session_id=session_id)
        fake_store.add_final_answer(run["id"], f"a{i}")

    transcript = load_chat_transcript(session_id, store=fake_store)
    assert len(transcript) == 12
    assert transcript[-2] == {"role": "user", "content": "q9"}
    assert transcript[-1] == {"role": "assistant", "content": "a9"}


# -----------------------------------------------------------------------------
# 集成测：session_id 透传与上下文注入
# -----------------------------------------------------------------------------


class FakeTranscriptQueries:
    """最小 Queries 假对象，支持 issue #123 / #545。"""

    def __init__(self) -> None:
        self.issues: dict[int, dict[str, Any]] = {
            123: {
                "number": 123,
                "title": "Demo issue",
                "state": "open",
                "labels": ["bug"],
                "html_url": "https://github.com/MoonshotAI/kimi-code/issues/123",
            },
            545: {
                "number": 545,
                "title": "Default issue",
                "state": "open",
                "labels": ["bug"],
                "html_url": "https://github.com/MoonshotAI/kimi-code/issues/545",
            },
        }
        self.pulls: dict[int, dict[str, Any]] = {}

    def fetch_issue_by_number(self, number: int) -> dict[str, Any] | None:
        return self.issues.get(number)

    def fetch_pull_by_number(self, number: int) -> dict[str, Any] | None:
        return self.pulls.get(number)


def test_run_deep_injects_transcript_into_subagent_prompt(
    monkeypatch: pytest.MonkeyPatch,
    fake_store: FakeTranscriptStore,
) -> None:
    """同一 session 第二轮问题，LLM prompt 中须包含第一轮内容。"""
    from api.ops.orchestrator.core import run_deep

    queries = FakeTranscriptQueries()
    session_id = "sess-deep"

    # 第一轮：明确提到 #123
    run1 = fake_store.create_run(query="#123 适合参与吗", route="deep", session_id=session_id)
    fake_store.add_final_answer(run1["id"], "#123 是个简单的 bug，适合新手。")

    captured_prompts: list[list[dict[str, str]]] = []

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        captured_prompts.append(messages)
        return LlmCompletionResult(
            content='{"reasoning": "继承上下文 #123", "suggestion": "适合", "confidence": 0.9, "citations": [{"number": 123, "url": "https://github.com/MoonshotAI/kimi-code/issues/123"}]}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "analyze"),
            ),
        )

    def fake_synthesize_answer(query: str, evidence: list[dict[str, Any]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        captured_prompts.append([{"role": "user", "content": f"SYNTHESIZE:{query}"}])
        return LlmCompletionResult(
            content="综合建议：#123 适合新手。",
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

    monkeypatch.setattr("api.ops.llm.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.llm.synthesize_answer", fake_synthesize_answer)
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", fake_chat_completion)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    run2 = fake_store.create_run(query="它呢", route="deep", session_id=session_id)
    result = run_deep(
        run2["id"],
        "它呢",
        {},
        fake_store,  # type: ignore[arg-type]
        queries,  # type: ignore[arg-type]
        session_id=session_id,
    )

    assert result["status"] in ("done", "partial")

    # 找到 subagent analyze 调用（第一条带 system 外的消息列表）
    analyze_messages = [m for m in captured_prompts if len(m) > 1]
    assert analyze_messages, "transcript 应作为独立消息注入，消息列表长度应 > 1"
    prompt_text = "\n".join(m["content"] for m in analyze_messages[0])
    assert "#123 适合参与吗" in prompt_text
    assert "#123 是个简单的 bug" in prompt_text
    assert "它呢" in prompt_text


def test_run_react_fallback_injects_transcript_into_messages(
    monkeypatch: pytest.MonkeyPatch,
    fake_store: FakeTranscriptStore,
) -> None:
    """ReAct fallback 须在 system prompt 之后、当前问题之前插入 transcript 消息。"""
    from api.ops.react_loop import run_react_fallback

    queries = FakeTranscriptQueries()
    session_id = "sess-react"

    run1 = fake_store.create_run(query="先问 #123", route="react", session_id=session_id)
    fake_store.add_final_answer(run1["id"], "#123 是 bug。")

    captured_messages: list[list[dict[str, str]]] = []

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        captured_messages.append(messages)
        return LlmCompletionResult(
            content='{"thought": "直接回答", "final_answer": "#123 是 bug。"}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "react"),
            ),
        )

    monkeypatch.setattr("api.ops.react_loop.chat_completion", fake_chat_completion)

    run2 = fake_store.create_run(query="它呢", route="react", session_id=session_id)
    result = run_react_fallback(
        run2["id"],
        "它呢",
        fake_store,  # type: ignore[arg-type]
        queries,  # type: ignore[arg-type]
        session_id=session_id,
    )

    assert result["status"] in ("done", "partial")
    assert captured_messages
    first_call = captured_messages[0]
    assert first_call[0]["role"] == "system"
    assert first_call[1] == {"role": "user", "content": "先问 #123"}
    assert first_call[2] == {"role": "assistant", "content": "#123 是 bug。"}
    assert first_call[-1] == {"role": "user", "content": "它呢"}


def test_chat_service_passes_session_id_to_run_deep(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """chat_service.handle_ops_chat_message 须将 session_id 透传给 run_deep。"""
    from api.ops.chat_service import ChatMessageRequest, handle_ops_chat_message
    from api.ops.demo_cache import DemoClassifier

    class FakeDemoCache:
        def __init__(self) -> None:
            self.classifier = DemoClassifier()

        def get(self, demo_id: str) -> dict[str, Any] | None:
            return None

        def set(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            return {"demo_id": args[0] if args else None}

    store = FakeTranscriptStore()
    queries = FakeTranscriptQueries()
    demo_cache = FakeDemoCache()

    captured: dict[str, Any] = {}

    def fake_run_deep(*args: Any, **kwargs: Any) -> dict[str, Any]:
        captured["args"] = args
        captured["kwargs"] = kwargs
        return {"run_id": args[0], "status": "done", "answer": "ok"}

    monkeypatch.setattr("api.ops.chat_service.run_deep", fake_run_deep)

    body = ChatMessageRequest(message="#123 适合吗", session_id="sess-service")
    handle_ops_chat_message(body, queries, store, demo_cache)

    assert captured["kwargs"].get("session_id") == "sess-service"


def test_react_fallback_inherits_issue_number_via_transcript(
    monkeypatch: pytest.MonkeyPatch,
    fake_store: FakeTranscriptStore,
) -> None:
    """同一 session 的 ReAct fallback 第二轮，通过 transcript 继承第一轮 issue 号。"""
    from api.ops.react_loop import run_react_fallback

    queries = FakeTranscriptQueries()
    session_id = "sess-react-inherit"

    run1 = fake_store.create_run(query="#123 状态如何", route="react", session_id=session_id)
    fake_store.add_final_answer(run1["id"], "#123 是 open 的 bug。")

    captured_messages: list[list[dict[str, str]]] = []

    def fake_chat_completion(messages: list[dict[str, str]], **kwargs: Any) -> Any:
        from api.ops.llm.types import LlmCompletionResult, LlmUsage
        captured_messages.append(messages)
        # 第二轮 LLM 从上下文中识别 #123
        return LlmCompletionResult(
            content='{"thought": "上下文提到 #123", "final_answer": "#123 仍然 open，值得跟进。"}',
            usage=LlmUsage(
                provider="siliconflow",
                model="Qwen/Qwen2.5-72B-Instruct",
                prompt_tokens=10,
                completion_tokens=5,
                total_tokens=15,
                latency_ms=100,
                step=kwargs.get("step", "react"),
            ),
        )

    monkeypatch.setattr("api.ops.react_loop.chat_completion", fake_chat_completion)

    run2 = fake_store.create_run(query="它呢", route="react", session_id=session_id)
    result = run_react_fallback(
        run2["id"],
        "它呢",
        fake_store,  # type: ignore[arg-type]
        queries,  # type: ignore[arg-type]
        session_id=session_id,
    )

    assert result["status"] in ("done", "partial")
    assert "#123" in result.get("answer", "")
    assert captured_messages
    first_call = captured_messages[0]
    assert first_call[0]["role"] == "system"
    assert first_call[1] == {"role": "user", "content": "#123 状态如何"}
    assert first_call[2] == {"role": "assistant", "content": "#123 是 open 的 bug。"}
    assert first_call[-1] == {"role": "user", "content": "它呢"}
