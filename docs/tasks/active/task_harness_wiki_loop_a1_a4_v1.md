# Task：Wiki Loop A1–A4 — 单 PR 编排母单（v1）

> **状态**：`draft`  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.1（Multi 部分外推后续）  
> **证据**：[`docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md`](../harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md) §4  
> **前置（done）**：[`task_wiki_ctx_ab_multi_slug_v1.md`](../done/task_wiki_ctx_ab_multi_slug_v1.md) · [`task_coding_wiki_t1c_test_archive_v1.md`](../done/task_coding_wiki_t1c_test_archive_v1.md)  
> **10 帽 Batch**：2026-05-26 · invoke [`docs/harness/invokes/by-task/wiki-loop-a1-a4/invoke_20260526_10_batch_four_tasks_v1.md`](../harness/invokes/by-task/wiki-loop-a1-a4/invoke_20260526_10_batch_four_tasks_v1.md)

> 落盘规则：四轮子 task 均 `done/` 后本单关账；`git mv` → `docs/tasks/done/` 并更新 `_views/done.md`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 task 交付 docs；母 task 不直接改 synthesis / SPEC 正文。 |
| **freeze_id** | `WIKI-LOOP-A1-A4@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths", "子 task 顺序"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **task_slug** | `wiki-loop-a1-a4` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **pending** | 22-R1, 30, 40, 50 | **人批**后四子 task 方可启动 Loop（各子 task 写「继承母闸」） |

---

## 子 task 顺序（硬 · A1→A4→母关账）

| 序 | round | task 路径 | task_slug | freeze_id | 关账后回填 |
|----|-------|-----------|-----------|-----------|------------|
| 1 | **A1** | [`task_coding_wiki_ingest_test_strategy_v1.md`](task_coding_wiki_ingest_test_strategy_v1.md) | `wiki-a1-ingest-test-strategy` | `CODING-WIKI-A1-TEST-STRATEGY@2026-05-26` | A2 `PLACEHOLDER:A1_OUTCOME` |
| 2 | **A2** | [`task_coding_wiki_schema_test_strategy_rule_v1.md`](task_coding_wiki_schema_test_strategy_rule_v1.md) | `wiki-a2-schema-test-strategy` | `CODING-WIKI-A2-SCHEMA-RULE@2026-05-26` | — |
| 3 | **A3** | [`task_governance_wiki_spec_comparison_sync_v1.md`](task_governance_wiki_spec_comparison_sync_v1.md) | `wiki-a3-spec-comparison` | `GOV-WIKI-A3-SPEC-SYNC@2026-05-26` | — |
| 4 | **A4** | [`task_governance_recent_schedule_wiki_sync_v1.md`](task_governance_recent_schedule_wiki_sync_v1.md) | `wiki-a4-recent-schedule` | `GOV-WIKI-A4-SCHEDULE@2026-05-26` | — |
| 5 | **META** | 本文件 | `wiki-loop-a1-a4` | `WIKI-LOOP-A1-A4@2026-05-26` | 四轮均 `done/` 后关账 |

**Manifest 真值**：[`docs/harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md)

---

## 帽子顺序（母单 · **跳过 10** · Loop 关账）

| 序 | 帽 | 说明 |
|----|-----|------|
| — | **10** | **本 Loop 已 Batch 起草**；子 task **禁止** 再开 10 |
| 1–4 | **A1–A4 各轮** | 每轮 **22 → 30 → 40 → 50 → 关账**；启动 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md) + `LOOP_MANIFEST` 替换 `round` |
| 5 | **母关账** | 四轮子 task 均在 `done/` 后，META round 关账本文件 |

**执行纪律**：

- **单 PR**：四子 task 变更合入 **`task/wiki-loop-a1-a4-v1`** 同一分支，最终 **一个 PR** 合 `main`。  
- **禁止**：改 `api/`、`tests/`、`docs/harness/prompts/`、CI workflow（`.github/workflows/`）。  
- **分支**：禁止在 `main` 上连续提交；每帽新对话 + Open **`ai-ink-brain-api-python/`**。

---

## 背景与目标

Wiki-CTX-AB **Multi slug** 已签收 **部分外推**：slug B（`query-rewrite-observability`）W 臂 B-Q3 因 synthesis **缺 `test_strategy` 枚举** 失分（3/4）。结论建议 ingest 规范补洞，**不**否定 P2 与 slug A 结论。

**母单完成态**：A1–A4 四子 task 均验收关账（`done/`）；治理文档（SPEC §2、对比表、排期表）与 Coding Wiki ingest 纪律一致；本单 META 关账。

---

## 范围

- [ ] `HG-LOOP-BATCH` 由 **人** 改 `approved` 后启动 A1 Loop。  
- [ ] A1→A2→A3→A4 按上表顺序各走完整 22→30→40→50→关账链。  
- [ ] A1 关账后回填 A2 内 `PLACEHOLDER:A1_OUTCOME`。  
- [ ] 四轮子 task 均 `git mv` 至 `docs/tasks/done/` 并更新索引。  
- [ ] 母 task META 关账：输出 `HANDOFF_CLOSE_TRACE`；本文件 `done/`。

## 非范围

- 重跑 Wiki-CTX-AB Multi slug 实验或改 `wiki_ctx_ab_multi_slug_v1/` 已冻结 scorecard。  
- 新增 slug ingest、改 `api/` / pytest / Harness 帽子 Prompt。  
- 在本母单内执行子 task 的 30 实现（由各子 task 的 Loop 轮次承担）。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| Multi 结论 | `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md` |
| Loop Prompt | `docs/harness/invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md` |
| Loop Manifest | `docs/harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md` |
| 目标 synthesis | `docs/coding_wiki/syntheses/query-rewrite-observability.md` |
| L1 真值 | `docs/tasks/done/task_05_query_rewrite_observability.md`（`test_strategy: recommended`） |
| 排期 | `docs/tasks/RECENT_TASK_SCHEDULE.md` §1、§6.6 |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | `HG-LOOP-BATCH` 仍为 `pending` | Agent **拒执行** 任一子 task 的 22/30 | 是 | 须改母 task 人工闸 |
| F2 | 子 task 跳过顺序（如 A3 先于 A1 done） | 排期/占位不一致；22 应 **阻塞** 并列出依赖 | 是 | 按 MANIFEST 顺序重开 |
| F3 | 子 task 关账未回填 `PLACEHOLDER:A1_OUTCOME` | A2 的 22 **拒开工**（见 A2 task） | 是 | 先完成 A1 关账回填 |
| F4 | 误改 `api/` / `tests/` / prompts / CI | 违反 Loop 纪律；50 应 **fail** | 否 | revert 或单列 hotfix task |

---

## 验收标准

- [ ] 四子 task 文件均在 `docs/tasks/done/`，且 `_views/done.md` 已更新。  
- [ ] A1：`query-rewrite-observability` synthesis 含可检索 `test_strategy`（与 L1 `recommended` 一致）。  
- [ ] A2：`CODING_WIKI.md` §8 含 api/ 类 Epic ingest 的 `test_strategy` 纪律。  
- [ ] A3：SPEC §2 T1c / Multi slug 标 **done**；对比表 #12、#46 与 Multi 结论一致。  
- [ ] A4：`RECENT_TASK_SCHEDULE.md` §1 快照与 §6.6 Wiki 行反映 Loop **done**。  
- [ ] 单 PR 合 `main`；`pytest` Required 仍绿（本 Loop **无** `api/` 变更）。

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`（本母单无代码变更，作回归基线）。

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | 见四子 task「实现备忘」汇总 |
| 子 task commits | A1–A4 各轮 CLOSE_TRACE |
| 图谱变更点 | 无（纯 docs / Wiki L2） |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | — |
| 结论 | — |
| 要点 | META 关账轮由 40 填写 |

---

## 给 Cursor

`wiki-loop-a1-a4`、`HG-LOOP-BATCH`、`WIKI-LOOP-A1-A4@2026-05-26`、`PROMPT_LOOP_22_to_CLOSE`、`LOOP_MANIFEST`、`单 PR`、`test_strategy`、`semi_auto`、`post_close`
