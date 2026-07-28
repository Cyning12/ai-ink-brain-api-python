# Task · Ops Desk P2-5g · 百炼 Provider KV Cache 指标（后端子仓）

> **状态**：`done` · **human CLOSE pass** · 2026-06-25  
> **协调 task**：Projects [`task_ops_desk_p2_bailian_provider_cache_metrics_v1.md`](../../../../docs/harness/tasks/done/task_ops_desk_p2_bailian_provider_cache_metrics_v1.md)  
> **PR**：#215 → main · merge `07e2a853`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-bailian-provider-cache-metrics` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-BAILIAN-PROVIDER-CACHE-METRICS` |
| **git_branch** | `task/ops-desk-p2-bailian-provider-cache-metrics` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

---

## 完成态

- [x] 字段映射 maintainer signoff（2026-06-25）
- [x] `openai_compatible._parse_completion_response` 百炼 nested 映射
- [x] pytest mock 百炼 usage · task_validate · CI 绿 · PR #215 merged
- [x] maintainer 验收 pass

---

## 字段映射（冻结）

| 上游（百炼） | LlmUsage |
| --- | --- |
| `usage.prompt_tokens_details.cached_tokens` | `prompt_cache_hit_tokens` + `cached_tokens` |
| `usage.prompt_tokens_details.cache_creation_input_tokens` | `prompt_cache_miss_tokens` |

SiliconFlow 顶层键解析 **不变**。

---

## 失败路径

| Scenario ID | 条件 | 行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- |
| F1 | `fp-bailian-no-cache-keys` · usage 无 cache 嵌套键 | 记 0 · 不标 `usage_missing` | — | Metrics 仍 0% 或「暂未采集」 |
| F2 | `fp-bailian-cache-demo-mix` · 误写入 Demo cache | **禁止** · CI / review 拒 | — | — |
| F3 | `fp-bailian-docs-unknown` · 字段名未文档确认 | task 阻塞 · 先 signoff 再实现 | 补文档 | — |

---

## 验收标准

- [x] `pytest tests/ops_desk/test_llm_usage_metrics.py -v` 绿
- [x] `pytest tests/ops_desk/ -q` 绿
- [x] `python tools/harness_task_validate.py docs/tasks/done/task_ops_desk_p2_bailian_provider_cache_metrics_v1.md` OK
- [x] Demo `cache_hit_rate` 不变
- [x] maintainer 验收 pass · 2026-06-25

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-25 | v1 · 泳道 A · 百炼 nested cache 解析 + pytest |
| 2026-06-25 | CLOSE · PR #215 merge · human pass |
