from __future__ import annotations

"""Intent 延迟基准（B1）。

测量边界：自 `decide_intent_v2` 入口起至返回止的 wall-clock（含内部 `asyncio.to_thread` 调 LLM）。
`CHATBI_V2_INTENT_LLM=false` 时为启发式路径，用于对照网络型延迟。

P1-C：支持「冷启动 vs 热缓存」两轮对比（同一进程内先 `clear_intent_cache()` 再全量 miss，
第二轮不清缓存以观察命中路径 P50/P95）。分位数口径与 `_stats` 一致。

用法示例：
  CHATBI_V2_INTENT_LLM=true CHATBI_V2_INTENT_BENCH_N=100 python tests/benchmark_intent_latency.py
  CHATBI_V2_INTENT_BENCH_COLD_WARM=1 CHATBI_V2_INTENT_BENCH_N=50 python tests/benchmark_intent_latency.py
"""

import asyncio
import os
import random
import time
from dataclasses import dataclass
from typing import Any

import pytest

from api.intent_agent import clear_intent_cache, decide_intent_v2
from api.tools import Tool


def _env_flag(name: str) -> bool:
    raw = (os.getenv(name, "") or "").strip().lower()
    return raw in ("1", "true", "yes", "on")


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


def _bench_case_at(i: int, queries: list[str]) -> tuple[str, list[dict[str, Any]]]:
    """用稳定但互不相同的 history 区分条目，便于冷相全 miss、暖相全 hit。"""
    q = queries[i % len(queries)]
    hist = [{"role": "user", "content": f"bench_turn:{i}"}]
    return q, hist


async def benchmark_intent_cold_warm(*, n: int, timeout_s: float = 3.0) -> tuple[LatencyStats, LatencyStats, dict[str, int]]:
    """同一组 (query,history) 序列：冷相清空缓存；暖相重复同一序列以观察命中延迟。"""
    tools = _make_tools()
    queries = [
        "昨天销售额是多少",
        "什么是RAG",
        "翻译：Hello",
        "按月统计销售额",
        "怎么优化向量检索",
    ]
    clear_intent_cache()
    cold: list[float] = []
    hits = 0
    misses = 0
    for i in range(n):
        q, hist = _bench_case_at(i, queries)
        t0 = time.perf_counter()
        d = await decide_intent_v2(query=q, history=hist, tools=tools, timeout=timeout_s)
        cold.append((time.perf_counter() - t0) * 1000.0)
        if d.raw_response.get("cache") == "hit":
            hits += 1
        elif d.raw_response.get("cache") == "miss":
            misses += 1

    warm: list[float] = []
    for i in range(n):
        q, hist = _bench_case_at(i, queries)
        t0 = time.perf_counter()
        d = await decide_intent_v2(query=q, history=hist, tools=tools, timeout=timeout_s)
        warm.append((time.perf_counter() - t0) * 1000.0)
        if d.raw_response.get("cache") == "hit":
            hits += 1
        elif d.raw_response.get("cache") == "miss":
            misses += 1

    counts = {"hit": hits, "miss": misses}
    return _stats(cold), _stats(warm), counts


def main() -> None:
    n = _env_int("CHATBI_V2_INTENT_BENCH_N", 100)
    timeout_s = float(os.getenv("CHATBI_V2_INTENT_TIMEOUT_S", "3.0"))
    if _env_flag("CHATBI_V2_INTENT_BENCH_COLD_WARM"):
        cold, warm, counts = asyncio.run(benchmark_intent_cold_warm(n=n, timeout_s=timeout_s))
        print("Intent Latency Benchmark (cold vs warm cache)")
        print(f"- n per phase={cold.n}")
        print(f"- cold P50: {cold.p50:.3f}ms  P95: {cold.p95:.3f}ms  min={cold.min:.3f}ms  max={cold.max:.3f}ms")
        print(f"- warm P50: {warm.p50:.3f}ms  P95: {warm.p95:.3f}ms  min={warm.min:.3f}ms  max={warm.max:.3f}ms")
        print(f"- cache hit/miss (both phases): hit={counts['hit']} miss={counts['miss']}")
        print(f"- cold P99: {cold.p99:.3f}ms  warm P99: {warm.p99:.3f}ms")
        return

    st = asyncio.run(benchmark_intent(n=n, timeout_s=timeout_s))
    print("Intent Latency Benchmark")
    print(f"- n={st.n}")
    print(f"- P50: {st.p50:.1f}ms")
    print(f"- P95: {st.p95:.1f}ms")
    print(f"- P99: {st.p99:.1f}ms")
    print(f"- Avg: {st.avg:.1f}ms")
    print(f"- Min: {st.min:.1f}ms")
    print(f"- Max: {st.max:.1f}ms")


@pytest.mark.intent_benchmark
@pytest.mark.skipif(
    (os.getenv("CHATBI_V2_INTENT_BENCH_RUN", "") or "").strip().lower() not in ("1", "true", "yes", "on"),
    reason="默认不进 CI；设置 CHATBI_V2_INTENT_BENCH_RUN=true 且配置 SILICONFLOW 后执行。",
)
def test_intent_latency_benchmark_pytest() -> None:
    """与 `main()` 同源逻辑，便于 `pytest -m intent_benchmark` 统一入口。"""
    main()


if __name__ == "__main__":
    # 用法：
    # CHATBI_V2_INTENT_LLM=true CHATBI_V2_INTENT_BENCH_N=100 python tests/benchmark_intent_latency.py
    main()
