# Task · Ops Desk P2-5b · Langfuse Eval · Tier A Regression（后端）

> **状态**：`active` · **READY** · 2026-06-25  
> **协调**：[`task_ops_desk_p2_langfuse_eval_v1.md`](../../../../docs/harness/tasks/active/task_ops_desk_p2_langfuse_eval_v1.md)  
> **GUIDE**：[`GUIDE_ops_desk_langfuse_eval_v1_zh.md`](../../../../docs/harness/guides/GUIDE_ops_desk_langfuse_eval_v1_zh.md)  
> **题集真值**：[`ops_desk_eval_cases_v0.json`](../../../tests/fixtures/ops_desk_eval_cases_v0.json)

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `ops-desk-p2-langfuse-eval` |
| **test_strategy** | `required` |
| **freeze_id** | `OPS-DESK-KIMI-CODE-P2-LANGFUSE-EVAL` |
| **git_branch** | `task/ops-desk-p2-langfuse-eval` |
| **worktree_root** | `ai-ink-brain-api-python/` |
| **Open Folder** | `ai-ink-brain-api-python/` |
| **semi_auto** | `false` |

---

## 背景与目标

P2-5a 已交付 Tracing；本 task 交付 **Evaluation Phase B 后端回归**：Tier A（A1–A8）JSON 驱动 pytest，**不**改 D1–D4 Demo 产品语义。

### 完成态

- [ ] `tests/fixtures/ops_desk_eval_cases_v0.json` 与 Harness 题集同步
- [ ] `tests/ops_desk/test_eval_cases_v0.py` Tier A batch runner（mock LLM 默认 CI）
- [ ] Scorer 复用 `review_result` V1–V3 + fast 子串规则
- [ ] `pytest tests/ops_desk/test_eval_cases_v0.py -v` 绿
- [ ] PR merged → main

---

## 范围 / 非范围

| 范围 | 非范围 |
| --- | --- |
| `tests/ops_desk/test_eval_cases_v0.py` | 改 D1–D4 demo 语义 |
| `tests/fixtures/ops_desk_eval_cases_v0.json` | 扩 DemoClassifier 至 D5–D8 |
| mock LLM deep（默认 CI）· `OPS_DESK_EVAL_LIVE=1` 可选 | 生产默认开全量 trace |
| Langfuse Dataset 导入（staging · 可选） | P3 ReAct · Tier C |
| 子仓 task 骨架 | LLM-as-judge 全文评分 fast 题 |

---

## 行为变更（Delta）

### ADDED

- **Requirement**：Ops Desk eval regression v0
  - **Scenario**：`eval-tier-a-demo-cache` — GIVEN 清 cache WHEN 顺序 A1–A6 THEN fast/deep/cache 纪律成立
  - **Scenario**：`eval-d4-review` — GIVEN A4 WHEN deep THEN Review V1–V3 非 fail
- `tests/fixtures/ops_desk_eval_cases_v0.json`：Harness 题集副本（CI 可移植）
- `tests/ops_desk/test_eval_cases_v0.py`：JSON 驱动 Tier A 断言

### MODIFIED

- 无

### REMOVED

- 无

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| --- | --- | --- | --- | --- | --- |
| F1 | `fp-eval-no-llm-key` | A4 无 API Key · live 模式 | pytest skip 或 fail 并注明 | 配 key | — |
| F2 | `fp-eval-stale-cache` | 未清 cache 跑 A1/A4 | A5/A6 误 pass | 先清 cache | — |
| F3 | `fp-eval-gold-drift` | LLM 全文变化 | 仅结构/scorer 断言 · 不锁死全文 | 更新 baseline | — |
| F4 | `fp-eval-langfuse-down` | Cloud 不可用 | pytest 仍绿 · Langfuse 导入 skip | 稍后 | — |

---

## 依赖与引用

| 项 | 路径 |
| --- | --- |
| Eval cases v0 | `tests/fixtures/ops_desk_eval_cases_v0.json` |
| Harness 题集 | [`ops_desk_eval_cases_v0.json`](../../../../docs/harness/fixtures/ops_desk_eval_cases_v0.json) |
| P1 Demo 测试参考 | `tests/ops_desk/test_demo_cache_p1.py` |
| Review 规则 | `api/ops/orchestrator/core.py` · `review_result` |
| P2-5a tracing | [`task_ops_desk_p2_langfuse_tracing_v1.md`](../done/task_ops_desk_p2_langfuse_tracing_v1.md) |

---

## 给执行 Agent

- CHAIN：[`PROMPT_CHAIN_30_40_50_CLOSE_v1.md`](../../../../docs/harness/invokes/by-task/ops-desk-p2-langfuse-eval/PROMPT_CHAIN_30_40_50_CLOSE_v1.md)
- **先**读 JSON Tier A · **勿**臆造 D5–D8 为已实现 Demo

---

## 验收标准

- [ ] `pytest tests/ops_desk/test_eval_cases_v0.py -v` 绿（mock LLM 或 `OPS_DESK_EVAL_LIVE=1` 可选）
- [ ] `pytest tests/ops_desk/ -q` 绿（无回归）
- [ ] `python tools/harness_task_validate.py docs/tasks/active/task_ops_desk_p2_langfuse_eval_v1.md` OK
- [ ] Tier A JSON 与 runner 字段一致
- [ ] 维护者：清 cache 后 A1–A4 本地 pass · baseline 记录 run_id（可选）
- [ ] Langfuse Dataset 导入 ≥1 条（staging · 可选签收）

---

## 修订记录

| 日期 | 说明 |
| --- | --- |
| 2026-06-25 | v1 · eval_cases_v0 Tier A pytest runner |
