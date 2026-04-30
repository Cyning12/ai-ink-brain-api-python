from __future__ import annotations

import asyncio
import os
import random
import time
from dataclasses import dataclass
from typing import Any

from api.intent_agent import decide_intent_v2
from api.tools import Tool


def _env_int(name: str, default: int) -> int:
    raw = (os.getenv(name) or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except Exception:  # noqa: BLE001
        return default


def _percentile(sorted_ms: list[float], p: float) -> float:
    if not sorted_ms:
        return 0.0
    if p <= 0:
        return sorted_ms[0]
    if p >= 1:
        return sorted_ms[-1]
    k = int((len(sorted_ms) - 1) * p)
    return sorted_ms[k]


async def _dummy_execute(*, query: str, history: list[dict[str, Any]] | None = None) -> Any:  # noqa: ANN401
    _ = (query, history)
    return {"ok": True}


def _make_tools() -> list[Tool]:
    async def _exec(query: str, *, history: list[dict[str, Any]] | None = None) -> Any:  # noqa: ANN401
        return await _dummy_execute(query=query, history=history)

    return [
        Tool(name="text2sql_query", description="结构化查数/统计/聚合，返回具体结果。", parameters={}, execute=_exec),
        Tool(name="rag_search", description="检索项目内资料/文档来回答。", parameters={}, execute=_exec),
        Tool(name="direct_answer", description="无需检索/查库，直接回答或生成内容。", parameters={}, execute=_exec),
    ]


@dataclass(frozen=True)
class LatencyStats:
    n: int
    p50: float
    p95: float
    p99: float
    min: float
    max: float
    avg: float


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


async def benchmark_intent(*, n: int, timeout_s: float = 3.0) -> LatencyStats:
    tools = _make_tools()
    queries = [
        "昨天销售额是多少",
        "什么是RAG",
        "翻译：Hello",
        "按月统计销售额",
        "怎么优化向量检索",
    ]
    ms: list[float] = []
    for _ in range(n):
        q = random.choice(queries)
        t0 = time.perf_counter()
        _ = await decide_intent_v2(query=q, history=[], tools=tools, timeout=timeout_s)
        ms.append((time.perf_counter() - t0) * 1000.0)
    return _stats(ms)


def main() -> None:
    n = _env_int("CHATBI_V2_INTENT_BENCH_N", 100)
    timeout_s = float(os.getenv("CHATBI_V2_INTENT_TIMEOUT_S", "3.0"))
    st = asyncio.run(benchmark_intent(n=n, timeout_s=timeout_s))
    print("Intent Latency Benchmark")
    print(f"- n={st.n}")
    print(f"- P50: {st.p50:.1f}ms")
    print(f"- P95: {st.p95:.1f}ms")
    print(f"- P99: {st.p99:.1f}ms")
    print(f"- Avg: {st.avg:.1f}ms")
    print(f"- Min: {st.min:.1f}ms")
    print(f"- Max: {st.max:.1f}ms")


if __name__ == "__main__":
    # 用法：
    # CHATBI_V2_INTENT_LLM=true CHATBI_V2_INTENT_BENCH_N=100 python tests/benchmark_intent_latency.py
    main()
