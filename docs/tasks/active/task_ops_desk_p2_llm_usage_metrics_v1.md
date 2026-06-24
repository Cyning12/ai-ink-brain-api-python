# Task · Ops Desk P2-5a-ext · LLM 用量 · 缓存指标（后端）

> **状态**：`active` · 2026-06-24  
> **SCOPE**：[`SCOPE_NOTE_langfuse_usage_metrics_addendum_v1_zh.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-langfuse-tracing/SCOPE_NOTE_langfuse_usage_metrics_addendum_v1_zh.md)  
> **协调**：[`task_ops_desk_p2_llm_usage_metrics_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_llm_usage_metrics_v1.md)  
> **前置**：P2-5a · main 含 #204

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-llm-usage-metrics` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-LLM-USAGE-METRICS` |
| **git_branch** | `task/ops-desk-p2-llm-usage-metrics` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |

---

## 背景与目标

P2-5a 已接 Langfuse trace。本 task 补齐 **项目内部** token / 缓存指标与 summary API；百炼 Provider stub。

### 完成态

- [ ] B1–B9（SCOPE addendum §5）
- [ ] V5–V9 验收
- [ ] PR merged → main

---

## 范围

见 SCOPE addendum §3–§5。

## 非范围

- 前端 · 百炼生产 · 流式 TTFT · P2-5b eval

---

## 失败路径

| Scenario ID | 条件 | 行为 |
| --- | --- | --- |
| F1 | API 无 usage | token=0 · event 标记 usage_missing |
| F2 | Langfuse 同步失败 | 内部 metrics 仍写 |
| F3 | provider=bailian 未实现 | 明确错误 |
| F4 | metrics API 无数据 | 200 零值 |

---

## 给执行 Agent

- CHAIN：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-llm-usage-metrics/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)

---

## 验收标准

- `pytest tests/ops_desk/test_llm_usage_metrics.py -v` 绿
- `pytest tests/ops_desk/ -q` 绿
- `pytest tests -m "not intent_eval and not intent_benchmark" -q` 绿
- SCOPE V5–V9 通过
