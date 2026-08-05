# Task · Ops Desk P2-5e · Provider KV Cache 指标（后端子仓）

> **状态**：`done` · script CLOSE 2026-06-24 · 人验 pending  
> **协调 task**：Projects [`task_ops_desk_p2_provider_cache_metrics_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_provider_cache_metrics_v1.md)  
> **invoke**：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-provider-cache-metrics/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)  
> **PR**：#211 → main · commit `64448d67`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-provider-cache-metrics` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-PROVIDER-CACHE-METRICS` |
| **git_branch** | `task/ops-desk-p2-provider-cache-metrics` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 背景与目标

采集 SiliconFlow LLM 响应中的 **Provider KV / prompt cache** token 字段，写入内部 metrics（与 Demo `cache_hit_rate` **分离**）。

### 完成态

- [x] `LlmUsage` + SiliconFlow 解析 + event 写入
- [x] `_build_metrics_json` 汇总 `llm.provider_cache`
- [x] `metrics_summary` 增 `provider_cache_*`
- [x] pytest 绿 · reinspect R1 pass
- [ ] D4 deep 人验 SQL

---

## 范围 / 非范围

| 范围 | 非范围 |
| --- | --- |
| SiliconFlow Provider KV cache | BailianProvider（P2-5c） |
| metrics_json + events + summary | 前端 Ink 页面 |
| pytest | Langfuse provider cache 镜像 |

---

## 失败路径

| Scenario ID | 条件 | 行为 |
| --- | --- | --- |
| F1 | usage 无 cache 键 | 记 0 · 不标 `usage_missing` |
| F2 | 非 siliconflow provider | provider_cache 全 0 或省略 |
| F3 | summary 历史 run 无 provider_cache | 聚合为 0 |

---

## 验收标准

- [x] `pytest tests/ops_desk/test_llm_usage_metrics.py -v` 绿
- [x] `pytest tests/ops_desk/ -q` 绿
- [x] `pytest tests -m "not intent_eval and not intent_benchmark" -q` 绿
- [x] mock SiliconFlow usage 含 cache 字段时 · event + metrics_json 正确
- [x] `GET /ops/metrics/summary` 返回新字段 · 旧 `cache_hit_rate` 不变
- [ ] SQL：`payload->>'prompt_cache_hit_tokens'` 可查（维护者人验）

---

## 给执行 Agent

- CHAIN：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-provider-cache-metrics/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-24 | script CLOSE · reinspect R1 pass · PR #211 pending merge |
