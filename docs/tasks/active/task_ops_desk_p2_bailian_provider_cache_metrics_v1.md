# Task · Ops Desk P2-5g · 百炼 Provider KV Cache 指标（后端子仓）

> **状态**：`active` · 泳道 A 实现中 · maintainer signoff 2026-06-25  
> **协调 task**：Projects [`task_ops_desk_p2_bailian_provider_cache_metrics_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_bailian_provider_cache_metrics_v1.md)  
> **前置**：P2-5e SiliconFlow KV #211 · P2-5c 百炼 #212

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-bailian-provider-cache-metrics` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-BAILIAN-PROVIDER-CACHE-METRICS` |
| **git_branch** | `task/ops-desk-p2-bailian-provider-cache-metrics` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |

---

## 背景与目标

P2-5e 已在 **SiliconFlow** 解析 Provider KV cache 并写入 `llm.provider_cache`。百炼 OpenAI 兼容响应 **无** SF 顶层 `prompt_cache_hit_tokens`，cache 指标在 `usage.prompt_tokens_details` 嵌套字段。本 task 补齐 **BailianProvider** 解析，复用 P2-5e metrics 聚合逻辑。

### 完成态

- [x] 字段映射 maintainer signoff（2026-06-25）
- [x] `openai_compatible._parse_completion_response` 百炼 nested 映射
- [x] pytest mock 百炼 usage · task_validate 绿
- [ ] D4 百炼 deep 人验 SQL / curl

---

## 字段映射（冻结）

| 上游（百炼） | LlmUsage |
| --- | --- |
| `usage.prompt_tokens_details.cached_tokens` | `prompt_cache_hit_tokens` + `cached_tokens` |
| `usage.prompt_tokens_details.cache_creation_input_tokens` | `prompt_cache_miss_tokens` |

SiliconFlow 顶层键解析 **不变**。

---

## 范围 / 非范围

| 范围 | 非范围 |
| --- | --- |
| `openai_compatible._parse_completion_response` bailian 分支 | 改 SiliconFlow 既有解析 |
| `tests/ops_desk/test_llm_usage_metrics.py` | `metrics_summary` 聚合逻辑 |
| `PROJECT_CONFIG` 百炼 cache 字段说明 | Demo `cache_hit_rate` |
| | P2-5f 模型链 fallback（另 PR） |

---

## 失败路径

| Scenario ID | 条件 | 行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- |
| F1 | `fp-bailian-no-cache-keys` · usage 无 cache 嵌套键 | 记 0 · 不标 `usage_missing` | — | Metrics 仍 0% 或「暂未采集」 |
| F2 | `fp-bailian-cache-demo-mix` · 误写入 Demo cache | **禁止** · CI / review 拒 | — | — |
| F3 | `fp-bailian-docs-unknown` · 字段名未文档确认 | task 阻塞 · 先 signoff 再实现 | 补文档 | — |

---

## 验收标准

- [x] `pytest tests/ops_desk/test_llm_usage_metrics.py -v` 绿（含 `test_bailian_parses_provider_cache_fields`）
- [x] `pytest tests/ops_desk/ -q` 绿
- [x] `python tools/harness_task_validate.py docs/tasks/active/task_ops_desk_p2_bailian_provider_cache_metrics_v1.md` OK
- [x] `ruff check api/ops tests/ops_desk` 绿
- [ ] Demo `cache_hit_rate` 与 P2-5d 签收一致 **不变**
- [ ] D4 百炼 deep · `provider_cache_hit_tokens` 与 UI 一致（维护者人验）

---

## 依赖与引用

- 对照实现：[`task_ops_desk_p2_provider_cache_metrics_v1.md`](../done/task_ops_desk_p2_provider_cache_metrics_v1.md)
- 工作区 task：[`task_ops_desk_p2_bailian_provider_cache_metrics_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_bailian_provider_cache_metrics_v1.md)

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-25 | v1 · 泳道 A · 百炼 nested cache 解析 + pytest |
