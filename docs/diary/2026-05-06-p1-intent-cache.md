# ChatBI V2 P1-C：IntentCache（LRU+TTL）与可观测性 — 跑批记录

日期：2026-05-06  
范围：仅 `ai-ink-brain-api-python`（`api/intent_agent.py`、基准脚本、单元测试）。

## 复跑命令

```bash
cd ai-ink-brain-api-python
# 单元测试（不触网）
PYTHONPATH=. python -m pytest tests/test_intent_cache.py -q --tb=short

# 冷/热两轮延迟对比（须 PYTHONPATH=.；启发式路径示例）
PYTHONPATH=. CHATBI_V2_INTENT_LLM=false CHATBI_V2_INTENT_BENCH_COLD_WARM=1 CHATBI_V2_INTENT_BENCH_N=30 \
  python tests/benchmark_intent_latency.py

# 真实上游时：将 CHATBI_V2_INTENT_LLM=true 并配置 SILICONFLOW_API_KEY；可选 CHATBI_V2_INTENT_TIMEOUT_S=15~30
```

## 本次本地样例（启发式 / 无外呼）

环境：`CHATBI_V2_INTENT_LLM=false`（无 SiliconFlow intent 调用），`CHATBI_V2_INTENT_BENCH_N=30`，`CHATBI_V2_INTENT_BENCH_COLD_WARM=1`，`PYTHONPATH=.`，分位数口径与脚本 `_stats` 一致。

| 指标 | 冷相（清空缓存后首轮） | 暖相（同序列第二轮） |
|------|------------------------|----------------------|
| P50 | 0.013 ms | 0.008 ms |
| P95 | 0.027 ms | 0.010 ms |

- **hit/miss 条数**（两相合计）：hit=30，miss=30（冷相全 miss、暖相全 hit；脚本用 `bench_turn:{i}` 区分 history，保证首轮键唯一）。  
- **Intent 评测 JSONL**：`decide_intent_v2` 的 `raw_response` 已含 `cache` / `cache_key_hash` / `latency_ms`，`test_intent_agent_accuracy` 导出会一并写入 `raw_response` 字段。

## 可选调试

- `DEBUG_INTENT_CACHE=1`：服务端 logger 输出 `[intent-cache] hit|miss key_hash=... latency_ms=...`（不记录完整 query）。

## 说明

- 第二次同 key 命中路径 **<10ms** 已在 `tests/test_intent_cache.py::test_cache_hit_latency_under_10ms` 用 mock LLM 校验（wall-clock 与 `raw_response.latency_ms`）。  
- 真实 LLM 下冷相 P50/P95 由上游主导；暖相仍以内存缓存命中为主，可复用上述命令对比。

## Git 说明

本文件位于 `docs/diary/`，当前仓库 `.gitignore` 中 `docs/*` 会忽略该路径；若需提交请使用 `git add -f docs/diary/2026-05-06-p1-intent-cache.md`（或调整 ignore 白名单）。
