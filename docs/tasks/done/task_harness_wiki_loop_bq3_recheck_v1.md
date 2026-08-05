# Task：Wiki Loop B-Q3 Recheck — 单 PR 编排母单（v2 试点）

> **状态**：`done（2026-05-26 验收通过 · WIKI-LOOP-BQ3-RECHECK@2026-05-26 · 第二 harness-loop-batch Loop）`  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md) §5.1  
> **SKILL 验证**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../tasks/skills/SKILL-harness-loop-batch.md)（第二 Loop · draft 未 accepted）  
> **前置（done）**：[`task_harness_wiki_loop_a1_a4_v1.md`](done/task_harness_wiki_loop_a1_a4_v1.md) · [`task_wiki_ctx_ab_multi_slug_v1.md`](done/task_wiki_ctx_ab_multi_slug_v1.md)  
> **10 帽 Batch**：2026-05-26 · invoke [`docs/harness/invokes/by-task/wiki-loop-bq3-recheck/invoke_20260526_10_batch_bq3_recheck_v1.md`](../harness/invokes/by-task/wiki-loop-bq3-recheck/invoke_20260526_10_batch_bq3_recheck_v1.md)

> 落盘规则：三轮子 task 均 `done/` 后本单 META 关账；`git mv` → `docs/tasks/done/` 并更新 `_views/done.md`。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 task 交付实验/治理 docs；母 task 不直接改 synthesis。 |
| **freeze_id** | `WIKI-LOOP-BQ3-RECHECK@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths", "子 task 顺序", "A1–A4 done"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-bq3-recheck-v1` |
| **task_slug** | `wiki-loop-bq3-recheck` |
| **wiki_delta** | `docs/coding_wiki` |
| **wiki_delta_note** | 存量迁移 · 本 task 触及 docs/coding_wiki（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | **approved** | 22-R1, 30, 40, 50 | **人批**后三子 task 方可启动 Loop（各子 task 写「继承母闸」） |

---

## 子 task 顺序（硬 · R1→R3→META）

| 序 | round | task 路径 | task_slug | freeze_id | 关账后回填 |
|----|-------|-----------|-----------|-----------|------------|
| 1 | **R1** | [`task_wiki_ctx_ab_multi_bq3_recheck_v1.md`](task_wiki_ctx_ab_multi_bq3_recheck_v1.md) | `wiki-bq3-r1-payload-scorecard` | `WIKI-BQ3-R1-PAYLOAD@2026-05-26` | R2 `PLACEHOLDER:R1_OUTCOME` |
| 2 | **R2** | [`task_wiki_ctx_ab_multi_conclusion_bq3_sync_v1.md`](task_wiki_ctx_ab_multi_conclusion_bq3_sync_v1.md) | `wiki-bq3-r2-conclusion` | `WIKI-BQ3-R2-CONCLUSION@2026-05-26` | — |
| 3 | **R3** | [`task_governance_wiki_bq3_spec_schedule_sync_v1.md`](task_governance_wiki_bq3_spec_schedule_sync_v1.md) | `wiki-bq3-r3-gov-sync` | `GOV-WIKI-BQ3-SYNC@2026-05-26` | — |
| 4 | **META** | 本文件 | `wiki-loop-bq3-recheck` | `WIKI-LOOP-BQ3-RECHECK@2026-05-26` | 三轮均 `done/` 后关账 |

**Manifest 真值**：[`docs/harness/invokes/by-task/wiki-loop-bq3-recheck/LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-bq3-recheck/LOOP_MANIFEST.md)

**排期职责**：**R3** 负责 `RECENT_TASK_SCHEDULE.md` §6.6 与本 Loop 行 + SPEC §5.1 脚注；**#46 / conclusion** 属 **R2**。

---

## 帽子顺序（母单 · **跳过 10** · Loop 关账）

| 序 | 帽 | 说明 |
|----|-----|------|
| — | **10** | **本 Loop 已 Batch 起草**；子 task **禁止** 再开 10 |
| 1–3 | **R1–R3 各轮** | 每轮 **22 → 30 → 40 → 50 → 关账**；[`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-bq3-recheck/PROMPT_LOOP_22_to_CLOSE_v1.md) |
| 4 | **母关账** | 三轮子 task 均在 `done/` 后 META；输出 CLOSE_TRACE |

**执行纪律**：

- **单 PR**：三子 task 合入 **`task/wiki-loop-bq3-recheck-v1`**，最终 **一个 PR** 合 `main`。  
- **禁止**：改 `api/`、`tests/`、`docs/harness/prompts/`、CI workflow。  
- **META 注记**：第二 Loop 完成后，**人** 可审 [`SKILL-harness-loop-batch.md`](../tasks/skills/SKILL-harness-loop-batch.md) `draft` → `accepted`（Agent **不得**代改 accepted）。

---

## 背景与目标

Loop A1–A4 已在 synthesis 补全 `test_strategy`，但 Multi 实验 **W 载荷与 scorecard** 仍反映 A1 前状态（slug B W 臂 B-Q3 **fail**，3/4）。对比表 **#46** 仍为「部分外推」。

**母单完成态**：R1 物化新 W 载荷并 scorecard §Recheck；R2 更新 conclusion 脚注与对比表；R3 同步 SPEC/RECENT；本单 META 关账，作为 **harness-loop-batch SKILL 第二 Loop** 验收证据。

---

## 范围

- [x] `HG-LOOP-BATCH` 由 **人** 改 `approved` 后启动 R1 Loop。  
- [x] R1→R2→R3 按上表顺序各走完整 22→30→40→50→关账链。  
- [x] R1 关账后回填 R2 内 `PLACEHOLDER:R1_OUTCOME`。  
- [x] 三轮子 task 均 `git mv` 至 `docs/tasks/done/` 并更新索引。  
- [x] 母 task META 关账：输出 `HANDOFF_CLOSE_TRACE`。

## 非范围

- 不改 Harness 帽子 prompts 正文。  
- 不代 SKILL 标 `accepted`。  
- 不重跑 slug A 或 P2 单 slug 实验。

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | 母 `HG-LOOP-BATCH` = `pending` | 22 **拒开工** | 人批后 |
| F2 | R2 开工时 R1 未 `done/` 或占位未回填 | 22 **阻塞** | R1 关账后 |
| F3 | R1 B-Q3 仍 fail | R2 仍须记录证据；#46 保持「部分」或附条件 | 回 A1 查 synthesis |
| F4 | 子 task 越界改 `api/` | 50 fail · revert | 拆出 Loop |

---

## 验收标准

- [x] 三轮子 task 状态 `done` 且在 `docs/tasks/done/`。  
- [x] W payload 含 `test_strategy`；scorecard 有 §Recheck addendum。  
- [x] conclusion / 对比表 / SPEC / RECENT 与 R1 跑分一致。  
- [x] 本母单 META 关账；PR 单分支 `task/wiki-loop-bq3-recheck-v1`。

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | R1 `payloads/W_*.md` + scorecard §Recheck · R2 conclusion §5 + 对比表 #46 · R3 SPEC/RECENT · invoke 链 `wiki-loop-bq3-recheck/` |
| 关账 commit | `task/wiki-loop-bq3-recheck-v1` · META 见 CLOSE invoke |
| R1 结论 | B-Q3 **pass** · slug B W **4/4** |
| SKILL 注记 | 第二 Loop 完成 · **人**可审 `harness-loop-batch` draft→accepted |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| 三子 task done/ | **pass** | R1/R2/R3 |
| invoke 链 C2 | **pass** | 22/30/40/50/CLOSE ×3 + META |
| cross_round_semi_auto | **pass** | R1·22 invoke |
| diff 无 api/tests/prompts | **pass** | docs-only |

---

## 给 Cursor

`wiki-loop-bq3-recheck`、`HG-LOOP-BATCH`、`SKILL-harness-loop-batch`、B-Q3、§Recheck、单 PR
