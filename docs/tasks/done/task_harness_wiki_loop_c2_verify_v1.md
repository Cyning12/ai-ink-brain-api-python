# Task：Wiki Loop C2 Verify — 单 PR 编排母单（v3 试点）

> **状态**：done（2026-05-26 验收通过 · `WIKI-LOOP-C2-VERIFY@2026-05-26`）  
> **关联 SKILL**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../tasks/skills/SKILL-harness-loop-batch.md)（第三 Loop · **C2 Verify** · draft 未 accepted）  
> **前置（done）**：[`task_harness_wiki_loop_a1_a4_v1.md`](done/task_harness_wiki_loop_a1_a4_v1.md) · [`task_harness_wiki_loop_bq3_recheck_v1.md`](done/task_harness_wiki_loop_bq3_recheck_v1.md) · meta-reinspect [`reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md`](reinspect_results/reinspect_wiki-loop-bq3-recheck-meta_20260526_v1.md)（**C2 FAIL**）  
> **10 帽 Batch**：2026-05-26 · invoke [`docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_20260526_10_batch_c2_verify_v1.md`](../harness/invokes/by-task/wiki-loop-c2-verify/invoke_20260526_10_batch_c2_verify_v1.md)

> 落盘规则：两轮子 task 均 `done/` 后本单 META 关账；`git mv` → `docs/tasks/done/` 并更新 `_views/done.md`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 task 交付 docs 烟雾；母 task 不直接改业务正文。 |
| **freeze_id** | `WIKI-LOOP-C2-VERIFY@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths", "子 task 顺序", "B-Q3 Loop done"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |
| **task_slug** | `wiki-loop-c2-verify` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **approved** | 22-R1, 30, 40, 50 | **人批**后两子 task 方可启动 Loop（各子 task 写「继承母闸」） |

---

## 子 task 顺序（硬 · R1→R2→META）

| 序 | round | task 路径 | task_slug | freeze_id | 关账后回填 |
|----|-------|-----------|-----------|-----------|------------|
| 1 | **R1** | [`task_governance_loop_c2_verify_r1_schedule_draft_v1.md`](task_governance_loop_c2_verify_r1_schedule_draft_v1.md) | `wiki-c2-r1-schedule-draft` | `WIKI-C2-R1-SCHEDULE@2026-05-26` | — |
| 2 | **R2** | [`task_governance_loop_c2_verify_r2_index_sync_v1.md`](task_governance_loop_c2_verify_r2_index_sync_v1.md) | `wiki-c2-r2-index-sync` | `WIKI-C2-R2-INDEX@2026-05-26` | — |
| 3 | **META** | 本文件 | `wiki-loop-c2-verify` | `WIKI-LOOP-C2-VERIFY@2026-05-26` | 两轮均 `done/` 后关账 |

**Manifest 真值**：[`docs/harness/invokes/by-task/wiki-loop-c2-verify/LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-c2-verify/LOOP_MANIFEST.md)

**排期职责**：**R1** 负责 `RECENT_TASK_SCHEDULE.md` §6.6 **draft/in_progress** 行；**R2** 负责 RECENT 行标 **done** + `_views/done.md` + invoke README 验收说明。

---

## 帽子顺序（母单 · **跳过 10** · Loop 关账）

| 序 | 帽 | 说明 |
|----|-----|------|
| — | **10** | **本 Loop 已 Batch 起草**；子 task **禁止** 再开 10 |
| 1–2 | **R1–R2 各轮** | 每轮 **22 → 30 → 40 → 50 → 关账**；[`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-c2-verify/PROMPT_LOOP_22_to_CLOSE_v1.md) |
| 3 | **母关账** | 两轮子 task 均在 `done/` 后 META；输出 CLOSE_TRACE |

**执行纪律**：

- **单 PR**：两子 task 合入 **`task/wiki-loop-c2-verify-v1`**，最终 **一个 PR** 合 `main`。  
- **禁止**：改 `api/`、`tests/`、`docs/harness/prompts/`、CI workflow。  
- **主验收**：各 round **invoke C2 全绿**（§3 ≥15 行 · 非 stub · 元信息表含 `task_slug`）。  
- **META 注记**：第三 Loop 完成后，**人** 可审 SKILL `draft` → `accepted`（Agent **不得**代改 accepted）。

---

## 背景与目标

Loop A1–A4 与 B-Q3 Recheck 均已关账；meta-reinspect 对第二 Loop **条件通过** 但 **C2 FAIL**（R2/R3 的 30/40/50 invoke 为 stub）。第三批工程已在 PROMPT_LOOP / HANDOFF 写入 C2 自检句。

**母单完成态**：R1 增 RECENT §6.6 draft 行（+ 可选 SKILL 修订 smoke）；R2 同步 invoke README 验收说明 + `_views` + RECENT done；本单 META 关账；**全链 invoke 满足 C2 门禁** 作为第三 Loop 验收证据。

---

## 范围

- [x] `HG-LOOP-BATCH` 由 **人** 改 `approved` 后启动 R1 Loop。  
- [x] R1→R2 按上表顺序各走完整 22→30→40→50→关账链。  
- [x] 各 round invoke **C2 全绿**（非 stub）。  
- [x] 两轮子 task 均 `git mv` 至 `docs/tasks/done/` 并更新索引。  
- [x] 母 task META 关账：输出 `HANDOFF_CLOSE_TRACE`。

## 非范围

- 不重跑 B-Q3 实验或改 scorecard/conclusion。  
- 不改 Harness 帽子 prompts 正文。  
- 不代 SKILL 标 `accepted`。

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | 母 `HG-LOOP-BATCH` = `pending` | 22 **拒开工** | 人批后 |
| F2 | R2 开工时 R1 未 `done/` | 22 **阻塞** | R1 关账后 |
| F3 | 任一 round 30/40/50 invoke **stub**（C2 fail） | 50 fail · META meta-reinspect 标 C2 fail | 重写 invoke §3 |
| F4 | 子 task 越界改 `api/` | 50 fail · revert | 拆出 Loop |

---

## 验收标准

- [x] 两轮子 task 状态 `done` 且在 `docs/tasks/done/`。  
- [x] 各 round 22/30/40/50/CLOSE invoke **§3 ≥15 行**（C2 pass）。  
- [x] RECENT §6.6 含 Loop C2 Verify 行且关账时标 done。  
- [x] 本母单 META 关账；PR 单分支 `task/wiki-loop-c2-verify-v1`。

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | R1 RECENT §6.6 draft · R2 README/_views · invoke 链 `wiki-loop-c2-verify/` |
| 关账 commit | `task/wiki-loop-c2-verify-v1` · META 见 CLOSE invoke |

### 自检结论（执行者）

| 项 | 结果 |
|----|------|
| C2 invoke 链 | **pass** · R1/R2 各 22/30/40/50/CLOSE · §3 ≥15 行 · 非 stub |
| META CLOSE_TRACE | **pass** · 见 CLOSE invoke |

---

## 给 Cursor

`wiki-loop-c2-verify`、`HG-LOOP-BATCH`、`harness-loop-batch`、`invoke C2`、`PROMPT_LOOP`、`RECENT_TASK_SCHEDULE`
