# Task · Ops Desk P2-5e · Provider KV Cache 指标（后端子仓）

> **状态**：`done` · script CLOSE 2026-06-24 · 人验 pending  
> **协调 task**：Projects [`task_ops_desk_p2_provider_cache_metrics_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_provider_cache_metrics_v1.md)  
> **invoke**：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-provider-cache-metrics/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)

---

## 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-provider-cache-metrics` |
| **test_strategy** | `required` |
| **分支** | `task/ops-desk-p2-provider-cache-metrics` |

---

## 交付清单

- [x] `api/ops/llm/types.py` — `LlmUsage` 增 `prompt_cache_hit_tokens` · `prompt_cache_miss_tokens` · `cached_tokens`
- [x] `api/ops/llm/providers/siliconflow.py` — 从 `usage` / `prompt_tokens_details` 解析
- [x] `api/ops/llm/__init__.py` — `_write_usage_event` payload 含新字段
- [x] `api/ops/orchestrator/core.py` — `_build_metrics_json` 汇总 `llm.provider_cache`
- [x] `api/ops/metrics.py` — `metrics_summary` 增 `provider_cache_hit_tokens` · `provider_cache_miss_tokens`
- [x] `tests/ops_desk/test_llm_usage_metrics.py` — mock 含/不含 cache 字段
- [x] `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` — Provider KV vs Demo cache 说明

---

## 自检（§40 pass · 2026-06-24）

```bash
OPS_DESK_SECRET= pytest tests/ops_desk/test_llm_usage_metrics.py -v   # 23 passed
OPS_DESK_SECRET= pytest tests/ops_desk/ -q                            # 150 passed
OPS_DESK_SECRET= pytest tests -m "not intent_eval and not intent_benchmark" -q  # 573 passed
ruff check api/ops tests/ops_desk                                     # pass
```
