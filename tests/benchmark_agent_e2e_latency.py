from __future__ import annotations

import importlib
import os
import random
from dataclasses import dataclass
from typing import Any, Callable

from fastapi.testclient import TestClient

from api.tools import Tool, ToolName, ToolResult


def _env_int(name: str, default: int) -> int:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except Exception:  # noqa: BLE001
        return default


def _reload_api_index() -> Any:  # noqa: ANN401
    # 说明：与 pytest 保持一致的最小启动 env（避免缺配置直接 500）。
    os.environ.setdefault("SYNC_ADMIN_SECRET", "secret-token-1234567890")
    os.environ.setdefault("API_KEY", "api-key-123")
    os.environ.setdefault("SILICONFLOW_API_KEY", "sf-dummy-key")
    os.environ.setdefault("NEXT_PUBLIC_SUPABASE_URL", "http://supabase.test")
    os.environ.setdefault("SUPABASE_SERVICE_ROLE_KEY", "service-role-dummy")
    os.environ.setdefault("TEXT2SQL_DATABASE_URL", "postgresql://u:p@localhost:5432/postgres")

    import api.unified_chat as unified_chat
    import api.index as index

    importlib.reload(unified_chat)
    importlib.reload(index)
    from tests._chatbi_auth_overrides import install_unified_chat_auth_override

    install_unified_chat_auth_override(index.app)
    return index


def _make_tool(name: ToolName, execute: Callable[..., Any]) -> Tool:
    async def _exec(
        query: str, *, history: list[dict[str, Any]] | None = None, **_: Any
    ) -> ToolResult:  # noqa: ANN001
        return await execute(query=query, history=history)

    return Tool(name=name, description=f"dummy-{name}", parameters={}, execute=_exec)


async def _ok_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
    _ = (query, history)
    return ToolResult(success=True, data={"answer": "ok", "hits": []}, latency_ms=3)


async def _sql_fail_exec(*, query: str, history: list[dict[str, Any]] | None = None) -> ToolResult:  # noqa: ANN001
    _ = (query, history)
    return ToolResult(
        success=False,
        data=None,
        error="sql exec failed",
        error_code="SQL_EXEC_TABLE_NOT_FOUND",
        error_stage="sql.execute",
        latency_ms=7,
    )


@dataclass(frozen=True)
class LatencyStats:
    n: int
    p50: float
    p95: float
    p99: float
    min: float
    max: float
    avg: float


def _percentile(sorted_ms: list[float], p: float) -> float:
    if not sorted_ms:
        return 0.0
    if p <= 0:
        return sorted_ms[0]
    if p >= 1:
        return sorted_ms[-1]
    k = int((len(sorted_ms) - 1) * p)
    return sorted_ms[k]


def _stats(ms: list[float]) -> LatencyStats:
    xs = sorted(ms)
    n = len(xs)
    avg = (sum(xs) / float(n)) if n else 0.0
    return LatencyStats(
        n=n,
        p50=_percentile(xs, 0.50),
        p95=_percentile(xs, 0.95),
        p99=_percentile(xs, 0.99),
        min=xs[0] if xs else 0.0,
        max=xs[-1] if xs else 0.0,
        avg=avg,
    )


def _extract_total_ms(events: list[dict[str, Any]]) -> int:
    for e in events:
        if e.get("type") != "latency":
            continue
        payload = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        v = payload.get("total_ms")
        try:
            return int(v)
        except Exception:  # noqa: BLE001
            continue
    return 0


def _extract_step_tool_ms(events: list[dict[str, Any]]) -> list[int]:
    ms: list[int] = []
    for e in events:
        if e.get("type") != "tool.call.end":
            continue
        payload = e.get("payload") if isinstance(e.get("payload"), dict) else {}
        v = payload.get("latency_ms")
        try:
            ms.append(int(v))
        except Exception:  # noqa: BLE001
            pass
    return ms


def main() -> None:
    # 说明：
    # - 这是“最小化 B2”基准：不依赖真实 RAG/Supabase/Text2SQL 后端，专注 agent.step 与 unified_chat E2E 的事件链路开销。
    # - 若要测真实 LLM intent：设置 CHATBI_V2_INTENT_LLM=true，并配置 SILICONFLOW_API_KEY / INTENT_LLM_MODEL。
    os.environ.setdefault("CHATBI_USE_AGENT", "true")
    os.environ.setdefault("CHATBI_V2_INTENT_LLM", "false")

    n = _env_int("CHATBI_V2_AGENT_BENCH_N", 50)
    queries = [
        "昨天销售额是多少",
        "什么是RAG",
        "翻译：Hello",
        "按月统计销售额",
        "为什么检索不准",
    ]

    index = _reload_api_index()
    import api.unified_chat as unified_chat

    class _DummyRegistry:
        def __init__(self, tools: list[Tool]) -> None:
            self._tools = tools

        def list_tools(self) -> list[Tool]:
            return self._tools

    # 两套工具：一套正常成功；一套模拟 SQL 失败触发 fallback，便于覆盖多步路径
    tools_ok = [
        _make_tool("text2sql_query", _ok_exec),
        _make_tool("rag_search", _ok_exec),
        _make_tool("direct_answer", _ok_exec),
    ]
    tools_fallback = [
        _make_tool("text2sql_query", _sql_fail_exec),
        _make_tool("rag_search", _ok_exec),
        _make_tool("direct_answer", _ok_exec),
    ]

    client = TestClient(index.app)
    e2e_ms: list[float] = []
    step_ms: list[float] = []

    for i in range(n):
        use_fallback = (i % 2) == 1
        unified_chat.get_tool_registry = (  # type: ignore[assignment]
            (lambda: _DummyRegistry(tools_fallback)) if use_fallback else (lambda: _DummyRegistry(tools_ok))
        )
        q = random.choice(queries)
        res = client.post(
            "/api/py/unified/chat",
            headers={"Authorization": "Bearer api-key-123"},
            json={"query": q},
        )
        if res.status_code != 200:
            continue
        data = res.json()
        events = data.get("events")
        if not isinstance(events, list):
            continue
        e2e_ms.append(float(_extract_total_ms(events)))
        step_ms.extend([float(x) for x in _extract_step_tool_ms(events)])

    st_e2e = _stats(e2e_ms)
    st_step = _stats(step_ms)

    print("Agent Latency Benchmark (stub tools, in-process)")
    print(f"- samples: e2e={st_e2e.n}, steps={st_step.n}")
    print(f"- E2E P50/P95/P99: {st_e2e.p50:.1f}/{st_e2e.p95:.1f}/{st_e2e.p99:.1f} ms (avg {st_e2e.avg:.1f})")
    print(f"- Step(tool.call.end) P50/P95/P99: {st_step.p50:.1f}/{st_step.p95:.1f}/{st_step.p99:.1f} ms (avg {st_step.avg:.1f})")


if __name__ == "__main__":
    main()
