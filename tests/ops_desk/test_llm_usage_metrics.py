"""Ops Desk LLM usage metrics 测试。

覆盖：
- usage 解析与 event 写入
- cache hit 无 llm.usage event
- OPS_LLM_PROVIDER=bailian mock HTTP / 缺 key → 503
- metrics summary API 零值
- 内部 metrics 始终写（tracing off 也写）
- Langfuse 仅镜像（tracing on 才同步）
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from api.index import app
from api.ops import chat
from api.ops.llm import chat_completion
from api.ops.llm.errors import OpsLlmMisconfiguredError
from api.ops.llm.factory import get_llm_provider
from api.ops.llm.providers.bailian import BailianProvider
from api.ops.llm.providers.siliconflow import SiliconFlowProvider
from api.ops.llm.types import LlmCompletionResult, LlmUsage
from api.ops.orchestrator.core import _build_metrics_json


class FakeOpsRunStore:
    """内存 store，用于验证 event 写入。"""

    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self.runs: dict[str, dict[str, Any]] = {}

    def append_event(
        self,
        run_id: str,
        agent_role: str,
        event_type: str,
        payload: dict[str, Any] | None = None,
        node_id: str | None = None,
        seq: int | None = None,
    ) -> dict[str, Any]:
        ev = {
            "run_id": run_id,
            "agent_role": agent_role,
            "event_type": event_type,
            "payload": payload or {},
            "node_id": node_id,
            "seq": seq or (len(self.events) + 1),
        }
        self.events.append(ev)
        return ev

    def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
        if run_id not in self.runs:
            self.runs[run_id] = {}
        self.runs[run_id]["metrics_json"] = metrics_json

    def update_run(self, run_id: str, **fields: Any) -> None:
        if run_id not in self.runs:
            self.runs[run_id] = {}
        self.runs[run_id].update(fields)


class FakeProvider:
    """Mock LLM Provider，返回固定 usage。"""

    def __init__(self, usage: LlmUsage | None = None) -> None:
        self._usage = usage or LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=10,
            completion_tokens=5,
            total_tokens=15,
            latency_ms=120,
            step="test",
        )

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        temperature: float = 0.3,
        model: str | None = None,
        **kwargs: Any,
    ) -> LlmCompletionResult:
        return LlmCompletionResult(content="fake answer", usage=self._usage)

    @property
    def name(self) -> str:
        return "fake"


# ---------------------------------------------------------------------------
# B1: usage 解析
# ---------------------------------------------------------------------------

def test_llm_usage_dataclass_defaults() -> None:
    u = LlmUsage()
    assert u.provider == ""
    assert u.prompt_tokens == 0
    assert u.completion_tokens == 0
    assert u.total_tokens == 0
    assert u.latency_ms == 0
    assert u.step == "other"
    assert u.usage_missing is False
    assert u.prompt_cache_hit_tokens == 0
    assert u.prompt_cache_miss_tokens == 0
    assert u.cached_tokens == 0


def test_llm_completion_result_to_dict() -> None:
    u = LlmUsage(provider="sf", model="m", prompt_tokens=1, completion_tokens=2, total_tokens=3, latency_ms=10, step="s")
    r = LlmCompletionResult(content="hello", usage=u)
    d = r.to_dict()
    assert d["content"] == "hello"
    assert d["usage"]["provider"] == "sf"
    assert d["usage"]["prompt_tokens"] == 1


# ---------------------------------------------------------------------------
# B2: chat_completion 写 llm.usage event
# ---------------------------------------------------------------------------

def test_chat_completion_writes_usage_event(monkeypatch) -> None:
    """tracing off 时内部 metrics 仍写入。"""
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    store = FakeOpsRunStore()
    fake = FakeProvider()
    monkeypatch.setattr("api.ops.llm.get_llm_provider", lambda: fake)

    result = chat_completion([{"role": "user", "content": "hi"}], step="analyze", run_id="run-123", store=store)

    assert result.content == "fake answer"
    assert result.usage.prompt_tokens == 10
    assert result.usage.completion_tokens == 5
    assert result.usage.total_tokens == 15

    # event 写入验证
    usage_events = [e for e in store.events if e["event_type"] == "llm.usage"]
    assert len(usage_events) == 1
    assert usage_events[0]["payload"]["prompt_tokens"] == 10
    assert usage_events[0]["payload"]["step"] == "analyze"
    assert usage_events[0]["payload"]["prompt_cache_hit_tokens"] == 0
    assert usage_events[0]["payload"]["prompt_cache_miss_tokens"] == 0
    assert usage_events[0]["payload"]["cached_tokens"] == 0


def test_chat_completion_no_store_no_event(monkeypatch) -> None:
    """store=None 时不抛异常，也不写 event。"""
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    fake = FakeProvider()
    monkeypatch.setattr("api.ops.llm.get_llm_provider", lambda: fake)

    result = chat_completion([{"role": "user", "content": "hi"}], step="test")
    assert result.content == "fake answer"


# ---------------------------------------------------------------------------
# B3: usage_missing 标记
# ---------------------------------------------------------------------------

def test_usage_missing_flag_when_api_returns_no_usage(monkeypatch) -> None:
    """API 无 usage 时 usage_missing=True，token 记 0。"""
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    store = FakeOpsRunStore()
    fake = FakeProvider(
        usage=LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=0,
            completion_tokens=0,
            total_tokens=0,
            latency_ms=100,
            step="test",
            usage_missing=True,
        )
    )
    monkeypatch.setattr("api.ops.llm.get_llm_provider", lambda: fake)

    result = chat_completion([{"role": "user", "content": "hi"}], step="test", run_id="run-456", store=store)
    assert result.usage.usage_missing is True
    assert result.usage.total_tokens == 0

    usage_events = [e for e in store.events if e["event_type"] == "llm.usage"]
    assert len(usage_events) == 1
    assert usage_events[0]["payload"]["usage_missing"] is True


# ---------------------------------------------------------------------------
# B4: cache hit 无 llm.usage event
# ---------------------------------------------------------------------------

def test_cache_hit_no_llm_usage_event() -> None:
    """cache hit 时 metrics_json 有 cache.hit，但无 llm.usage event。"""
    store = FakeOpsRunStore()
    run_id = "run-cache-001"

    # 模拟 chat.py 中 _run_demo_cache_hit 的行为
    metrics_json = {
        "cache": {"demo_id": "D4", "hit": True, "source": "ops_demo_answers"},
        "llm": {
            "provider": "",
            "model": "",
            "calls": 0,
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "latency_ms": 0,
        },
        "route": "fast",
        "intent": "demo",
    }
    store.update_run_metrics_json(run_id, metrics_json)
    store.append_event(run_id, "orchestrator", "demo.cache.hit", payload={"demo_id": "D4"}, node_id="demo.cache")
    store.append_event(run_id, "orchestrator", "run.metrics", payload=metrics_json, node_id="fast.metrics")

    # 验证：无 llm.usage event
    usage_events = [e for e in store.events if e["event_type"] == "llm.usage"]
    assert len(usage_events) == 0

    # 验证：metrics_json 正确
    assert store.runs[run_id]["metrics_json"]["cache"]["hit"] is True
    assert store.runs[run_id]["metrics_json"]["llm"]["calls"] == 0


# ---------------------------------------------------------------------------
# B5: _build_metrics_json 汇总
# ---------------------------------------------------------------------------

def test_build_metrics_json_with_usage() -> None:
    u1 = LlmUsage(provider="sf", model="m1", prompt_tokens=10, completion_tokens=5, total_tokens=15, latency_ms=100, step="analyze")
    u2 = LlmUsage(provider="sf", model="m1", prompt_tokens=8, completion_tokens=4, total_tokens=12, latency_ms=80, step="synthesize")
    metrics = _build_metrics_json(route="deep", intent="issue_contribution", llm_calls=2, llm_usages=[u1, u2])

    assert metrics["route"] == "deep"
    assert metrics["intent"] == "issue_contribution"
    assert metrics["llm"]["calls"] == 2
    assert metrics["llm"]["prompt_tokens"] == 18
    assert metrics["llm"]["completion_tokens"] == 9
    assert metrics["llm"]["total_tokens"] == 27
    assert metrics["llm"]["latency_ms"] == 180
    assert metrics["llm"]["provider"] == "sf"
    assert metrics["llm"]["provider_cache"] == {
        "hit_tokens": 0,
        "miss_tokens": 0,
        "cached_tokens": 0,
    }


def test_build_metrics_json_provider_cache_sums() -> None:
    u1 = LlmUsage(
        provider="sf",
        model="m1",
        prompt_tokens=100,
        completion_tokens=50,
        total_tokens=150,
        latency_ms=100,
        step="analyze",
        prompt_cache_hit_tokens=80,
        prompt_cache_miss_tokens=20,
        cached_tokens=80,
    )
    u2 = LlmUsage(
        provider="sf",
        model="m1",
        prompt_tokens=50,
        completion_tokens=25,
        total_tokens=75,
        latency_ms=80,
        step="synthesize",
        prompt_cache_hit_tokens=30,
        prompt_cache_miss_tokens=20,
        cached_tokens=30,
    )
    metrics = _build_metrics_json(route="deep", intent="issue_contribution", llm_calls=2, llm_usages=[u1, u2])

    assert metrics["llm"]["provider_cache"] == {
        "hit_tokens": 110,
        "miss_tokens": 40,
        "cached_tokens": 110,
    }


def test_build_metrics_json_cache_hit() -> None:
    """cache hit 时 token 为 0，calls 为 0。"""
    metrics = _build_metrics_json(route="fast", intent="demo", llm_calls=0, llm_usages=[], cache_hit=True, demo_id="D4")

    assert metrics["cache"]["hit"] is True
    assert metrics["llm"]["calls"] == 0
    assert metrics["llm"]["total_tokens"] == 0


# ---------------------------------------------------------------------------
# B6: OPS_LLM_PROVIDER=bailian
# ---------------------------------------------------------------------------

def test_bailian_provider_missing_key_raises_misconfigured_error(monkeypatch) -> None:
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.delenv("BAILIAN_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    provider = get_llm_provider()
    assert isinstance(provider, BailianProvider)
    with pytest.raises(OpsLlmMisconfiguredError, match="BAILIAN_API_KEY"):
        provider.complete([{"role": "user", "content": "hi"}])


def test_siliconflow_provider_missing_key_raises_misconfigured_error(monkeypatch) -> None:
    monkeypatch.setenv("OPS_LLM_PROVIDER", "siliconflow")
    monkeypatch.delenv("SILICONFLOW_API_KEY", raising=False)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    provider = get_llm_provider()
    assert isinstance(provider, SiliconFlowProvider)
    with pytest.raises(OpsLlmMisconfiguredError, match="SILICONFLOW_API_KEY"):
        provider.complete([{"role": "user", "content": "hi"}])


def test_chat_completion_missing_key_raises_http_503(monkeypatch) -> None:
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.delenv("BAILIAN_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    with pytest.raises(HTTPException) as exc_info:
        chat_completion([{"role": "user", "content": "hi"}])
    assert exc_info.value.status_code == 503
    assert exc_info.value.detail == {
        "code": "LLM_PROVIDER_MISCONFIGURED",
        "message": "缺少 LLM API Key（BAILIAN_API_KEY / DASHSCOPE_API_KEY）",
    }


def test_chat_messages_bailian_missing_key_returns_503(monkeypatch) -> None:
    """deep 路径触发真实 chat_completion → 缺 key 时 HTTP 503 结构化错误。"""
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.delenv("BAILIAN_API_KEY", raising=False)
    monkeypatch.delenv("DASHSCOPE_API_KEY", raising=False)
    monkeypatch.delenv("OPS_DESK_SECRET", raising=False)
    monkeypatch.delenv("OPS_DESK_SECRET_TEST", raising=False)

    class _FakeDemoCache:
        def __init__(self) -> None:
            from api.ops.demo_cache import DemoClassifier

            self.classifier = DemoClassifier()

        def get(self, demo_id: str) -> dict[str, Any] | None:
            return None

        def set(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            return {"demo_id": args[0] if args else None}

    class _FakeQueries:
        def fetch_issue_by_number(self, number: int) -> dict[str, Any] | None:
            return {
                "number": number,
                "title": "Test issue",
                "state": "open",
                "labels": [],
                "scan_tags": [],
                "html_url": f"https://github.com/test/issues/{number}",
            }

        def fetch_pull_by_number(self, number: int) -> dict[str, Any] | None:
            return None

    class _FakeStore:
        def __init__(self) -> None:
            self.runs: dict[str, dict[str, Any]] = {}
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
            self.runs[run_id] = {"id": run_id, "query": query, "route": route, "status": "running"}
            return self.runs[run_id]

        def append_event(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
            return {"event_type": kwargs.get("event_type") or (args[2] if len(args) > 2 else "")}

        def update_run(self, run_id: str, **fields: Any) -> None:
            if run_id in self.runs:
                self.runs[run_id].update(fields)

        def update_run_metrics_json(self, run_id: str, metrics_json: dict[str, Any]) -> None:
            if run_id in self.runs:
                self.runs[run_id]["metrics_json"] = metrics_json

    fake_store = _FakeStore()
    app.dependency_overrides[chat._queries] = lambda: _FakeQueries()
    app.dependency_overrides[chat._store] = lambda: fake_store
    app.dependency_overrides[chat._demo_cache] = lambda: _FakeDemoCache()
    try:
        client = TestClient(app)
        resp = client.post(
            "/api/py/ops/chat/messages",
            json={"message": "#545 适合我吗"},
            headers={"x-ops-secret": "test"},
        )
    finally:
        app.dependency_overrides.clear()

    assert resp.status_code == 503
    assert resp.json()["detail"]["code"] == "LLM_PROVIDER_MISCONFIGURED"
    assert "BAILIAN_API_KEY" in resp.json()["detail"]["message"]


def test_bailian_provider_complete_mock_http_success(monkeypatch) -> None:
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.setenv("BAILIAN_API_KEY", "test-bailian-key")
    monkeypatch.delenv("BAILIAN_MODEL", raising=False)

    class FakeResponse:
        status_code = 200
        ok = True
        text = ""

        def json(self) -> dict[str, Any]:
            return {
                "choices": [{"message": {"content": "百炼回答"}}],
                "usage": {
                    "prompt_tokens": 20,
                    "completion_tokens": 10,
                    "total_tokens": 30,
                },
            }

    monkeypatch.setattr(
        "api.ops.llm.providers.openai_compatible.requests.post",
        lambda *args, **kwargs: FakeResponse(),
    )

    provider = get_llm_provider()
    assert isinstance(provider, BailianProvider)
    result = provider.complete([{"role": "user", "content": "hi"}], step="analyze")

    assert result.content == "百炼回答"
    assert result.usage.provider == "bailian"
    assert result.usage.model == "deepseek-v4-pro"
    assert result.usage.prompt_tokens == 20
    assert result.usage.completion_tokens == 10
    assert result.usage.total_tokens == 30
    assert result.usage.step == "analyze"
    assert result.usage.prompt_cache_hit_tokens == 0
    assert result.usage.prompt_cache_miss_tokens == 0
    assert result.usage.cached_tokens == 0
    assert result.usage.usage_missing is False


def test_factory_default_is_siliconflow(monkeypatch) -> None:
    monkeypatch.delenv("OPS_LLM_PROVIDER", raising=False)
    provider = get_llm_provider()
    assert isinstance(provider, SiliconFlowProvider)


def test_factory_unknown_provider_raises(monkeypatch) -> None:
    monkeypatch.setenv("OPS_LLM_PROVIDER", "unknown")
    with pytest.raises(ValueError, match="未知的 OPS_LLM_PROVIDER"):
        get_llm_provider()


# ---------------------------------------------------------------------------
# B7: metrics summary API 结构验证
# ---------------------------------------------------------------------------

def test_metrics_summary_structure(monkeypatch) -> None:
    """metrics summary 返回正确结构；无数据时各字段为零值。"""
    from api.ops.metrics import metrics_summary

    # Mock supabase client to return empty rows (zero-value scenario)
    mock_client = MagicMock()
    mock_res = MagicMock()
    mock_res.data = []
    mock_client.table.return_value.select.return_value.gte.return_value.execute.return_value = mock_res
    monkeypatch.setattr("api.ops.metrics.get_supabase_client", lambda: mock_client)

    result = metrics_summary(days=7)
    assert result["window_days"] == 7
    assert result["cache_hit_rate"] == 0.0
    assert result["total_tokens"] == 0
    assert result["total_llm_calls"] == 0
    assert result["total_runs"] == 0
    assert result["by_route"] == {}
    assert result["provider_cache_hit_tokens"] == 0
    assert result["provider_cache_miss_tokens"] == 0
    assert "provider_cache_hit_rate" not in result


def test_metrics_summary_with_data(monkeypatch) -> None:
    """metrics summary 正确聚合 metrics_json 数据。"""
    from api.ops.metrics import metrics_summary

    mock_client = MagicMock()
    mock_res = MagicMock()
    mock_res.data = [
        {
            "metrics_json": {
                "route": "deep",
                "llm": {"calls": 2, "total_tokens": 30, "prompt_tokens": 20, "completion_tokens": 10},
            },
            "created_at": "2026-06-20T00:00:00Z",
        },
        {
            "metrics_json": {
                "route": "fast",
                "cache": {"hit": True, "demo_id": "D4"},
                "llm": {"calls": 0, "total_tokens": 0},
            },
            "created_at": "2026-06-21T00:00:00Z",
        },
    ]
    mock_client.table.return_value.select.return_value.gte.return_value.execute.return_value = mock_res
    monkeypatch.setattr("api.ops.metrics.get_supabase_client", lambda: mock_client)

    result = metrics_summary(days=7)
    assert result["window_days"] == 7
    assert result["total_runs"] == 2
    assert result["total_tokens"] == 30
    assert result["total_llm_calls"] == 2
    assert result["cache_hits"] == 1
    assert result["cache_misses"] == 1
    assert result["cache_hit_rate"] == 0.5

    # by_route
    assert "deep" in result["by_route"]
    assert result["by_route"]["deep"]["runs"] == 1
    assert result["by_route"]["deep"]["tokens"] == 30
    assert result["by_route"]["deep"]["llm_calls"] == 2
    assert result["by_route"]["fast"]["runs"] == 1
    assert result["by_route"]["fast"]["cache_hits"] == 1


def test_metrics_summary_provider_cache_aggregation(monkeypatch) -> None:
    """metrics summary 聚合 provider_cache 字段，不影响 cache_hit_rate。"""
    from api.ops.metrics import metrics_summary

    mock_client = MagicMock()
    mock_res = MagicMock()
    mock_res.data = [
        {
            "metrics_json": {
                "route": "deep",
                "llm": {
                    "calls": 2,
                    "total_tokens": 100,
                    "provider_cache": {"hit_tokens": 60, "miss_tokens": 40, "cached_tokens": 60},
                },
            },
            "created_at": "2026-06-20T00:00:00Z",
        },
        {
            "metrics_json": {
                "route": "deep",
                "llm": {
                    "calls": 1,
                    "total_tokens": 50,
                    "provider_cache": {"hit_tokens": 20, "miss_tokens": 30, "cached_tokens": 20},
                },
            },
            "created_at": "2026-06-21T00:00:00Z",
        },
    ]
    mock_client.table.return_value.select.return_value.gte.return_value.execute.return_value = mock_res
    monkeypatch.setattr("api.ops.metrics.get_supabase_client", lambda: mock_client)

    result = metrics_summary(days=7)
    assert result["provider_cache_hit_tokens"] == 80
    assert result["provider_cache_miss_tokens"] == 70
    assert result["provider_cache_hit_rate"] == round(80 / 150, 4)
    assert result["cache_hits"] == 0
    assert result["cache_misses"] == 2
    assert result["cache_hit_rate"] == 0.0


# ---------------------------------------------------------------------------
# B10: SiliconFlow provider cache 字段解析
# ---------------------------------------------------------------------------

def test_siliconflow_parses_provider_cache_fields(monkeypatch) -> None:
    """SiliconFlow usage 含 cache 字段时正确解析。"""
    monkeypatch.setenv("SILICONFLOW_API_KEY", "test-key")

    class FakeResponse:
        status_code = 200
        ok = True
        text = ""

        def json(self) -> dict[str, Any]:
            return {
                "choices": [{"message": {"content": "ok"}}],
                "usage": {
                    "prompt_tokens": 128,
                    "completion_tokens": 64,
                    "total_tokens": 192,
                    "prompt_cache_hit_tokens": 100,
                    "prompt_cache_miss_tokens": 28,
                    "prompt_tokens_details": {"cached_tokens": 100},
                },
            }

    monkeypatch.setattr(
        "api.ops.llm.providers.openai_compatible.requests.post",
        lambda *args, **kwargs: FakeResponse(),
    )

    provider = SiliconFlowProvider()
    result = provider.complete([{"role": "user", "content": "hi"}], step="analyze")

    assert result.usage.prompt_cache_hit_tokens == 100
    assert result.usage.prompt_cache_miss_tokens == 28
    assert result.usage.cached_tokens == 100
    assert result.usage.usage_missing is False


def test_bailian_parses_provider_cache_fields(monkeypatch) -> None:
    """百炼 usage 含嵌套 cache 字段时正确映射到 LlmUsage。"""
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.setenv("BAILIAN_API_KEY", "test-bailian-key")
    monkeypatch.delenv("BAILIAN_MODEL", raising=False)

    class FakeResponse:
        status_code = 200
        ok = True
        text = ""

        def json(self) -> dict[str, Any]:
            return {
                "choices": [{"message": {"content": "百炼 cache 回答"}}],
                "usage": {
                    "prompt_tokens": 200,
                    "completion_tokens": 50,
                    "total_tokens": 250,
                    "prompt_tokens_details": {
                        "cached_tokens": 120,
                        "cache_creation_input_tokens": 80,
                    },
                },
            }

    monkeypatch.setattr(
        "api.ops.llm.providers.openai_compatible.requests.post",
        lambda *args, **kwargs: FakeResponse(),
    )

    provider = get_llm_provider()
    assert isinstance(provider, BailianProvider)
    result = provider.complete([{"role": "user", "content": "hi"}], step="analyze")

    assert result.usage.provider == "bailian"
    assert result.usage.prompt_cache_hit_tokens == 120
    assert result.usage.prompt_cache_miss_tokens == 80
    assert result.usage.cached_tokens == 120
    assert result.usage.usage_missing is False


def test_bailian_missing_cache_fields_defaults_zero(monkeypatch) -> None:
    """百炼 usage 无 cache 嵌套字段时记 0，不标 usage_missing。"""
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.setenv("BAILIAN_API_KEY", "test-bailian-key")
    monkeypatch.delenv("BAILIAN_MODEL", raising=False)

    class FakeResponse:
        status_code = 200
        ok = True
        text = ""

        def json(self) -> dict[str, Any]:
            return {
                "choices": [{"message": {"content": "百炼回答"}}],
                "usage": {
                    "prompt_tokens": 20,
                    "completion_tokens": 10,
                    "total_tokens": 30,
                },
            }

    monkeypatch.setattr(
        "api.ops.llm.providers.openai_compatible.requests.post",
        lambda *args, **kwargs: FakeResponse(),
    )

    provider = get_llm_provider()
    result = provider.complete([{"role": "user", "content": "hi"}], step="analyze")

    assert result.usage.prompt_cache_hit_tokens == 0
    assert result.usage.prompt_cache_miss_tokens == 0
    assert result.usage.cached_tokens == 0
    assert result.usage.usage_missing is False


def test_siliconflow_missing_cache_fields_defaults_zero(monkeypatch) -> None:
    """SiliconFlow usage 无 cache 字段时记 0，不标 usage_missing。"""
    monkeypatch.setenv("SILICONFLOW_API_KEY", "test-key")

    class FakeResponse:
        status_code = 200
        ok = True
        text = ""

        def json(self) -> dict[str, Any]:
            return {
                "choices": [{"message": {"content": "ok"}}],
                "usage": {
                    "prompt_tokens": 15,
                    "completion_tokens": 10,
                    "total_tokens": 25,
                },
            }

    monkeypatch.setattr(
        "api.ops.llm.providers.openai_compatible.requests.post",
        lambda *args, **kwargs: FakeResponse(),
    )

    provider = SiliconFlowProvider()
    result = provider.complete([{"role": "user", "content": "hi"}], step="analyze")

    assert result.usage.prompt_cache_hit_tokens == 0
    assert result.usage.prompt_cache_miss_tokens == 0
    assert result.usage.cached_tokens == 0
    assert result.usage.usage_missing is False


def test_chat_completion_writes_provider_cache_in_event(monkeypatch) -> None:
    """chat_completion 将 provider cache 字段写入 llm.usage event。"""
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    store = FakeOpsRunStore()
    fake = FakeProvider(
        usage=LlmUsage(
            provider="siliconflow",
            model="Qwen/Qwen2.5-72B-Instruct",
            prompt_tokens=128,
            completion_tokens=64,
            total_tokens=192,
            latency_ms=500,
            step="analyze",
            prompt_cache_hit_tokens=100,
            prompt_cache_miss_tokens=28,
            cached_tokens=100,
        )
    )
    monkeypatch.setattr("api.ops.llm.get_llm_provider", lambda: fake)

    chat_completion([{"role": "user", "content": "hi"}], step="analyze", run_id="run-pc-001", store=store)

    usage_events = [e for e in store.events if e["event_type"] == "llm.usage"]
    assert len(usage_events) == 1
    payload = usage_events[0]["payload"]
    assert payload["prompt_cache_hit_tokens"] == 100
    assert payload["prompt_cache_miss_tokens"] == 28
    assert payload["cached_tokens"] == 100


# ---------------------------------------------------------------------------
# B8: Langfuse 仅镜像（tracing on 才同步）
# ---------------------------------------------------------------------------

def test_tracing_off_does_not_call_update_generation_usage(monkeypatch) -> None:
    """tracing off 时 update_current_generation_usage 不抛异常，也不影响结果。"""
    monkeypatch.delenv("LANGFUSE_TRACING", raising=False)
    monkeypatch.delenv("LANGSMITH_TRACING", raising=False)

    from api.ops.tracing import update_current_generation_usage

    u = LlmUsage(prompt_tokens=10, completion_tokens=5, total_tokens=15)
    # 不应抛异常
    update_current_generation_usage(u)


def test_langfuse_usage_mirror_calls_update_current_generation(monkeypatch) -> None:
    """Langfuse on 时使用 update_current_generation(usage_details=...)。"""
    monkeypatch.setenv("LANGFUSE_TRACING", "true")
    monkeypatch.setenv("LANGFUSE_PUBLIC_KEY", "pk-test")
    monkeypatch.setenv("LANGFUSE_SECRET_KEY", "sk-test")

    calls: list[dict[str, Any]] = []

    class FakeClient:
        def update_current_generation(self, **kwargs: Any) -> None:
            calls.append(kwargs)

    monkeypatch.setattr("api.ops.tracing.tracing_provider", lambda: "langfuse")
    monkeypatch.setattr("langfuse.get_client", lambda: FakeClient())

    from api.ops.tracing import update_current_generation_usage

    u = LlmUsage(
        provider="siliconflow",
        model="Qwen/Qwen2.5-72B-Instruct",
        prompt_tokens=128,
        completion_tokens=194,
        total_tokens=322,
    )
    update_current_generation_usage(u)

    assert len(calls) == 1
    assert calls[0]["usage_details"] == {"input": 128, "output": 194, "total": 322}
    assert calls[0]["model"] == "Qwen/Qwen2.5-72B-Instruct"


# ---------------------------------------------------------------------------
# B9: run_deep 集成 — 验证 analyze_issue 返回的 _llm_usage 被正确消费
# ---------------------------------------------------------------------------

def test_llm_usage_from_dict_flat_and_nested() -> None:
    flat = LlmUsage(
        provider="siliconflow",
        model="Qwen/Qwen2.5-72B-Instruct",
        prompt_tokens=128,
        completion_tokens=216,
        total_tokens=344,
        latency_ms=7805,
        step="analyze",
    ).to_dict()
    u_flat = LlmUsage.from_dict(flat, step="analyze")
    assert u_flat.provider == "siliconflow"
    assert u_flat.total_tokens == 344

    nested = {"usage": flat}
    u_nested = LlmUsage.from_dict(nested, step="analyze")
    assert u_nested.total_tokens == 344


def test_run_deep_metrics_collects_analyze_usage_shape(monkeypatch) -> None:
    """run_deep 消费 analyze_issue 的扁平 _llm_usage，写入非零 metrics_json。"""
    from api.ops.orchestrator.core import run_deep

    store = FakeOpsRunStore()
    run_id = "run-deep-metrics"
    store.runs[run_id] = {}

    analyze_usage = LlmUsage(
        provider="siliconflow",
        model="Qwen/Qwen2.5-72B-Instruct",
        prompt_tokens=128,
        completion_tokens=216,
        total_tokens=344,
        latency_ms=7805,
        step="analyze",
    )
    synth_usage = LlmUsage(
        provider="siliconflow",
        model="Qwen/Qwen2.5-72B-Instruct",
        prompt_tokens=50,
        completion_tokens=30,
        total_tokens=80,
        latency_ms=1200,
        step="synthesize",
    )

    def fake_analyze_issue(*args: Any, **kwargs: Any) -> dict[str, Any]:
        return {
            "found": True,
            "evidence": [{"issue_number": 545}],
            "reasoning": "ok",
            "suggestion": "s",
            "confidence": 0.9,
            "citations": [],
            "_llm_usage": analyze_usage.to_dict(),
        }

    def fake_synthesize_answer(
        query: str,
        evidence: list[dict[str, Any]],
        *,
        run_id: str | None = None,
        store: Any = None,
        transcript: list[dict[str, str]] | None = None,
    ) -> LlmCompletionResult:
        if run_id and store:
            from api.ops.llm import _write_usage_event

            _write_usage_event(run_id, synth_usage, store)
        return LlmCompletionResult(content="final answer", usage=synth_usage)

    mock_queries = MagicMock()
    mock_queries.fetch_issue_by_number.return_value = {
        "title": "Test",
        "state": "open",
        "labels": [],
        "scan_tags": [],
        "html_url": "https://github.com/test/issues/545",
    }
    mock_queries.fetch_pull_by_number.return_value = None

    monkeypatch.setattr("api.ops.orchestrator.core.analyze_issue", fake_analyze_issue)
    monkeypatch.setattr("api.ops.orchestrator.core.synthesize_answer", fake_synthesize_answer)

    run_deep(run_id, "test", {"issue_number": 545}, store, mock_queries, intent="issue_contribution")

    metrics = store.runs[run_id]["metrics_json"]
    assert metrics["llm"]["calls"] == 2
    assert metrics["llm"]["total_tokens"] == 424
    assert metrics["llm"]["provider"] == "siliconflow"
    assert metrics["route"] == "deep"
    assert metrics["intent"] == "issue_contribution"

    usage_events = [e for e in store.events if e["event_type"] == "llm.usage"]
    assert len(usage_events) == 1
    assert usage_events[0]["payload"]["step"] == "synthesize"


def test_analyze_issue_returns_llm_usage_shape(monkeypatch) -> None:
    """analyze_issue 返回的 _llm_usage 可被 run_deep 消费。"""
    from api.ops.agents.issue_analyst import analyze_issue

    fake_usage = LlmUsage(
        provider="siliconflow",
        model="Qwen/Qwen2.5-72B-Instruct",
        prompt_tokens=20,
        completion_tokens=10,
        total_tokens=30,
        latency_ms=200,
        step="analyze",
    )
    fake_result = LlmCompletionResult(
        content='{"reasoning": "test", "suggestion": "ok", "confidence": 0.9, "citations": []}',
        usage=fake_usage,
    )
    monkeypatch.setattr("api.ops.agents.issue_analyst.chat_completion", lambda *args, **kwargs: fake_result)

    mock_queries = MagicMock()
    mock_queries.fetch_issue_by_number.return_value = {
        "title": "Test Issue",
        "state": "open",
        "labels": [],
        "scan_tags": [],
        "html_url": "https://github.com/test/issues/1",
    }
    mock_queries.fetch_pull_by_number.return_value = None

    result = analyze_issue("test query", 1, mock_queries, run_id="run-001", store=None)

    assert result["found"] is True
    assert "_llm_usage" in result
    usage_dict = result["_llm_usage"]
    assert usage_dict["prompt_tokens"] == 20
    assert usage_dict["total_tokens"] == 30
    assert usage_dict["step"] == "analyze"


# ---------------------------------------------------------------------------
# P2-5f: 模型链 · 百炼 quota fallback
# ---------------------------------------------------------------------------

def test_resolve_bailian_model_chain_from_primary() -> None:
    from api.ops.llm.model_catalog import resolve_bailian_model_chain

    chain = resolve_bailian_model_chain("deepseek-v4-flash")
    assert chain[0] == "deepseek-v4-flash"
    assert chain[-1] == "qwen3.7-plus"
    assert "kimi/kimi-k2.7-code" not in chain


def test_resolve_bailian_model_chain_qwen_fallbacks_to_prod_models() -> None:
    from api.ops.llm.model_catalog import resolve_bailian_model_chain

    chain = resolve_bailian_model_chain("qwen3.7-plus")
    assert chain == ["qwen3.7-plus", "deepseek-v4-pro", "deepseek-v4-flash"]


def test_resolve_bailian_model_chain_skips_test_only_after_kimi() -> None:
    from api.ops.llm.model_catalog import resolve_bailian_model_chain

    chain = resolve_bailian_model_chain("kimi/kimi-k2.7-code")
    assert chain[0] == "kimi/kimi-k2.7-code"
    assert "ZHIPU/GLM-5.2" not in chain
    assert chain[1] == "deepseek-v4-pro"
    assert chain[-1] == "qwen3.7-plus"


def test_bailian_quota_error_switches_model(monkeypatch) -> None:
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.setenv("BAILIAN_API_KEY", "test-key")

    class QuotaResponse:
        status_code = 403
        ok = False
        text = "AllocationQuota.FreeTierOnly"

        def json(self) -> dict[str, Any]:
            return {"error": {"code": "AllocationQuota.FreeTierOnly", "message": "no quota"}}

    class FreeQuotaExhaustedResponse:
        status_code = 403
        ok = False
        text = '{"error":{"message":"The free quota has been exhausted."}}'

        def json(self) -> dict[str, Any]:
            return {"error": {"message": "The free quota has been exhausted."}}

    class OkResponse:
        status_code = 200
        ok = True
        text = ""

        def __init__(self, model: str) -> None:
            self._model = model

        def json(self) -> dict[str, Any]:
            return {
                "choices": [{"message": {"content": f"ok:{self._model}"}}],
                "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3},
            }

    def fake_post(*args: Any, **kwargs: Any) -> Any:
        model = kwargs["json"]["model"]
        if model in ("kimi/kimi-k2.7-code",):
            return QuotaResponse()
        if model == "qwen3.7-plus":
            return FreeQuotaExhaustedResponse()
        return OkResponse(model)

    monkeypatch.setattr(
        "api.ops.llm.providers.openai_compatible.requests.post",
        fake_post,
    )

    provider = get_llm_provider()
    result = provider.complete(
        [{"role": "user", "content": "hi"}],
        model="kimi/kimi-k2.7-code",
        step="analyze",
    )
    assert result.content == "ok:deepseek-v4-pro"
    assert result.usage.model == "deepseek-v4-pro"

    result2 = provider.complete(
        [{"role": "user", "content": "hi"}],
        model="qwen3.7-plus",
        step="analyze",
    )
    assert result2.content == "ok:deepseek-v4-pro"
    assert result2.usage.model == "deepseek-v4-pro"


def test_chat_models_endpoint_bailian(monkeypatch) -> None:
    monkeypatch.setenv("OPS_LLM_PROVIDER", "bailian")
    monkeypatch.setenv("OPS_DESK_SECRET_TEST", "test")
    monkeypatch.delenv("BAILIAN_MODEL", raising=False)
    client = TestClient(app)
    resp = client.get("/api/py/ops/chat/models", headers={"x-ops-secret": "test"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["provider"] == "bailian"
    assert data["auto_fallback"] is True
    assert len(data["models"]) == 5
    assert data["default_model"] == "deepseek-v4-pro"
