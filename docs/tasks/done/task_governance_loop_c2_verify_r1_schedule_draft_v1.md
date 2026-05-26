# Task：治理 — RECENT §6.6 Loop C2 Verify draft 行（R1 · 烟雾）

> **状态**：draft  
> **母 Loop**：[`task_harness_wiki_loop_c2_verify_v1.md`](task_harness_wiki_loop_c2_verify_v1.md) · round **R1**

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；**本 round 负责** `RECENT_TASK_SCHEDULE.md` §6.6 **draft/in_progress** 行（**不**标 done）。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 排期表 draft 行 + 可选 SKILL 修订 smoke；纯 docs。 |
| **freeze_id** | `WIKI-C2-R1-SCHEDULE@2026-05-26` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |
| **task_slug** | `wiki-c2-r1-schedule-draft` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 继承 [`HG-LOOP-BATCH`](task_harness_wiki_loop_c2_verify_v1.md) |

---

## 帽子顺序（**跳过 10** · Loop R1）

| 序 | 帽 | 启动 |
|----|-----|------|
| 1–5 | **22→50→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-c2-verify/PROMPT_LOOP_22_to_CLOSE_v1.md) · **round=R1** |

---

## 背景与目标

第三 Loop 主目标为 **invoke C2 质量全绿**；本 round 以最小 docs 交付验证 Loop 流水线。在 RECENT §6.6 增 **Wiki Loop C2 Verify** 行（draft/in_progress），链至母 task active 路径。

**完成态**：

- [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §6.6 表增一行（状态 **draft** 或 **in_progress**）。  
- 可选：[`SKILL-harness-loop-batch.md`](../tasks/skills/SKILL-harness-loop-batch.md) 修订记录一行「第三 Loop C2 Verify 试点 @2026-05-26」；**禁止** Agent 改 SKILL status。

---

## 范围

- [ ] 更新 RECENT §6.6 + §8 修订记录（若惯例需要）。  
- [ ] 可选 SKILL 修订记录一行。  
- [ ] 22/30/40/50 invoke **C2 全绿**（§3 ≥15 行 · 非 stub）。  
- [ ] 关账时更新 `_views/done.md` 本 task 一行。

## 非范围

- RECENT 行标 **done**（属 R2）。  
- api / tests / Harness prompts / CI。  
- 重跑 B-Q3 实验。

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | 母闸 pending | 22 拒开工 |
| F2 | RECENT 行误标 done | 50 fail · 回 30 |
| F3 | invoke 30/40/50 为 stub | C2 fail · 50 fail |

---

## 验收标准

- [ ] `rg 'Loop C2 Verify' docs/tasks/RECENT_TASK_SCHEDULE.md` 命中 §6.6 行。  
- [ ] RECENT 行状态为 draft/in_progress（非 done）。  
- [ ] 本 round invoke 链 C2 pass。

**VERIFY**：

```bash
rg 'Loop C2 Verify' docs/tasks/RECENT_TASK_SCHEDULE.md
```

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `RECENT_TASK_SCHEDULE.md` §6.6/§8 · `SKILL-harness-loop-batch.md` 修订记录 |
| RECENT §6.6 | 增 **Wiki Loop C2 Verify** 行 · 状态 **in_progress** · 链母 task active |
| §8 修订 | 2026-05-26 R1 draft 行注记 |
| SKILL | 修订记录「第三 Loop C2 Verify 试点 @2026-05-26」（status 未改） |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| RECENT §6.6 | **pass** | `rg 'Loop C2 Verify'` 命中 §6.6 行 · 状态 **in_progress**（非 done） |
| invoke C2 | **pass（初检）** | 22/30 invoke 已落盘 · §3 ≥15 行 · 元信息含 task_slug；50 独立复检 |

---

## 给 Cursor

`wiki-c2-r1-schedule-draft`、`PROMPT_LOOP`、`round=R1`、`RECENT_TASK_SCHEDULE`
