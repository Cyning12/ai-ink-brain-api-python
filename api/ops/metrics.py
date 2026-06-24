"""Ops Desk metrics 路由（含 LLM usage summary）。"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Query

from api.ops.constants import DEFAULT_DAYS
from api.ops.deps import get_supabase_client, require_ops_secret
from api.ops.queries import OpsQueries

router = APIRouter(prefix="/ops/metrics", tags=["ops-metrics"])


def ops_queries() -> OpsQueries:
    return OpsQueries(get_supabase_client())


@router.get("/cycle-time")
def cycle_time(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    return queries.cycle_time_metric(days)


@router.get("/review-time")
def review_time(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    return queries.review_time_metric(days)


@router.get("/issue-throughput")
def issue_throughput(
    days: Annotated[int, Query(ge=1, le=365)] = DEFAULT_DAYS,
    queries: OpsQueries = Depends(ops_queries),
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    return queries.issue_throughput_metric(days)


@router.get("/summary")
def metrics_summary(
    days: Annotated[int, Query(ge=1, le=365)] = 7,
    _: None = Depends(require_ops_secret),
) -> dict[str, Any]:
    """返回最近 N 日 token 消耗与缓存命中率汇总。

    基于 ops_runs.metrics_json 聚合；无数据时返回零值（F4）。
    """
    client = get_supabase_client()
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).isoformat()

    # 1. 基础聚合：total_runs / total_tokens / total_llm_calls / cache_hits / cache_misses
    def _aggregate_once() -> dict[str, Any]:
        # 使用 Supabase RPC 或直接查询；这里用 PostgREST 的 select + 过滤
        # metrics_json->'llm'->>'total_tokens' 等 JSON 路径在 PostgREST 中可用
        # 但聚合函数（sum/count）需要后端计算，我们拉取行后在 Python 聚合
        res = (
            client.table("ops_runs")
            .select("metrics_json, created_at")
            .gte("created_at", cutoff)
            .execute()
        )
        rows = res.data if isinstance(res.data, list) else []

        total_runs = len(rows)
        total_tokens = 0
        total_llm_calls = 0
        cache_hits = 0
        cache_misses = 0
        provider_cache_hit_tokens = 0
        provider_cache_miss_tokens = 0
        by_route: dict[str, dict[str, Any]] = {}

        for row in rows:
            m = row.get("metrics_json") or {}
            if not isinstance(m, dict):
                continue

            # LLM 聚合
            llm = m.get("llm") or {}
            if isinstance(llm, dict):
                total_tokens += int(llm.get("total_tokens") or 0)
                total_llm_calls += int(llm.get("calls") or 0)
                provider_cache = llm.get("provider_cache") or {}
                if isinstance(provider_cache, dict):
                    provider_cache_hit_tokens += int(provider_cache.get("hit_tokens") or 0)
                    provider_cache_miss_tokens += int(provider_cache.get("miss_tokens") or 0)

            # Cache 聚合
            cache = m.get("cache") or {}
            if isinstance(cache, dict) and cache.get("hit") is True:
                cache_hits += 1
            else:
                cache_misses += 1

            # Route 聚合
            route = str(m.get("route") or "unknown")
            if route not in by_route:
                by_route[route] = {
                    "runs": 0,
                    "tokens": 0,
                    "llm_calls": 0,
                    "cache_hits": 0,
                }
            by_route[route]["runs"] += 1
            by_route[route]["tokens"] += int(llm.get("total_tokens") or 0)
            by_route[route]["llm_calls"] += int(llm.get("calls") or 0)
            if isinstance(cache, dict) and cache.get("hit") is True:
                by_route[route]["cache_hits"] += 1

        total_cacheable = cache_hits + cache_misses
        cache_hit_rate = round(cache_hits / total_cacheable, 4) if total_cacheable > 0 else 0.0

        total_provider_cacheable = provider_cache_hit_tokens + provider_cache_miss_tokens
        provider_cache_hit_rate = (
            round(provider_cache_hit_tokens / total_provider_cacheable, 4)
            if total_provider_cacheable > 0
            else 0.0
        )

        result: dict[str, Any] = {
            "window_days": days,
            "total_runs": total_runs,
            "total_tokens": total_tokens,
            "total_llm_calls": total_llm_calls,
            "cache_hits": cache_hits,
            "cache_misses": cache_misses,
            "cache_hit_rate": cache_hit_rate,
            "provider_cache_hit_tokens": provider_cache_hit_tokens,
            "provider_cache_miss_tokens": provider_cache_miss_tokens,
            "by_route": by_route,
        }
        if total_provider_cacheable > 0:
            result["provider_cache_hit_rate"] = provider_cache_hit_rate
        return result

    from api.rag_env import supabase_execute_with_retry
    return supabase_execute_with_retry(_aggregate_once)
