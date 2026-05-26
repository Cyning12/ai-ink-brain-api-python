# 启动 Prompt · 一次性 Batch-10 · Wiki Loop C2 Verify（v1）

> **只运行一次**。生成母 task + 两个子 task 初稿后，后续每轮 **仅** 使用 [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md)（见 [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md)）。  
> **分支**：`task/wiki-loop-c2-verify-v1` · Open **`ai-ink-brain-api-python/`**

---

```text
你正在扮演 Harness「需求与任务分析帽（10）· Batch 模式」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md（输出形状；本批 **禁止** 写业务代码）
- docs/tasks/templates/TASK_TEMPLATE.md
- docs/tasks/skills/SKILL-docs-governance.md（预填片段）
- docs/tasks/skills/SKILL-harness-loop-batch.md（Loop 字段 · v1.5 invoke C2 门禁）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、07-git-workflow.mdc

【背景】
Loop 实例 1（A1–A4）、实例 2（B-Q3 Recheck）均已 done；meta-reinspect 条件通过但 **C2 FAIL**（R2/R3 的 30/40/50 stub）。
第三批工程（PROMPT_LOOP C2 自检 + HANDOFF）已落盘。
本 Loop = **第三次 harness-loop-batch 试点**；主目标：**验证 invoke C2 全绿**（非重跑 B-Q3 业务）；**单 PR**、docs-only。

【loop-slug】wiki-loop-c2-verify
【git_branch】task/wiki-loop-c2-verify-v1
【freeze_id 母】WIKI-LOOP-C2-VERIFY@2026-05-26

【开帽 · Invoke 快照】将 **本 user 消息全文** 落盘至：
docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_YYYYMMDD_10_batch_c2_verify_v1.md

【SDD】不涉及新 SPEC · 状态 = 不涉及新 SPEC（§3 省略）

【你必须落盘以下 3 个 task 文件（相对子仓根）】

---

## 0. 母 task · task_harness_wiki_loop_c2_verify_v1.md

路径：docs/tasks/active/task_harness_wiki_loop_c2_verify_v1.md

| 字段 | 值 |
|------|-----|
| test_strategy | not_applicable |
| test_strategy_note | Loop 编排；子 task 交付 docs 烟雾；母 task 不直接改业务正文 |
| freeze_id | WIKI-LOOP-C2-VERIFY@2026-05-26 |
| semi_auto | true |
| audit_profile | post_close |
| git_branch | task/wiki-loop-c2-verify-v1 |
| task_slug | wiki-loop-c2-verify |

人工闸（仅母 task）：
| HG-LOOP-BATCH | pending | 22-R1,30,40,50 | 人批后子 task 写「继承母闸」 |

正文须含：
- 子 task 顺序 R1→R2→META
- 链 LOOP_MANIFEST / PROMPT_LOOP
- 单 PR、不改 api/tests/prompts/CI
- **R1 负责** RECENT §6.6 **draft** 行（Loop C2 Verify · in_progress）+ 可选 SKILL 修订记录 smoke 一行
- **R2 负责** invoke 目录 README 验收说明一行 + `_views/done.md` 同步 + RECENT 行关账时标 done
- META 关账：第三 Loop C2 Verify 完成 · **禁止** Agent 代 SKILL 标 `accepted`
- §验收：两轮子 task 均 done/ 后母关账；**C2 invoke 质量全绿**为 Loop 成功判据

---

## 1. 子 task R1 · task_governance_loop_c2_verify_r1_schedule_draft_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | WIKI-C2-R1-SCHEDULE@2026-05-26 |
| task_slug | wiki-c2-r1-schedule-draft |
| human_gate | 继承 HG-LOOP-BATCH |

**目标**（纯 docs 烟雾）：
1. 在 `RECENT_TASK_SCHEDULE.md` §6.6 表增 **Wiki Loop C2 Verify** 行（状态 **draft** 或 **in_progress**；链母 task active 路径）。
2. 可选：`SKILL-harness-loop-batch.md` 修订记录增一行「第三 Loop C2 Verify 试点 @2026-05-26」——**不**改 SKILL status。

**范围**：
- 改 RECENT §6.6 一行 + §8 修订记录一行（若惯例需要）
- 可选 SKILL 修订记录一行
- VERIFY：`rg 'Loop C2 Verify' docs/tasks/RECENT_TASK_SCHEDULE.md`

**非范围**：不改 api/tests/prompts/CI；不代 SKILL 标 accepted；RECENT 标 done（属 R2 关账）

**帽子顺序**：22→30→40→50→关账 · PROMPT_LOOP round=R1

---

## 2. 子 task R2 · task_governance_loop_c2_verify_r2_index_sync_v1.md

| 字段 | 值 |
|------|-----|
| freeze_id | WIKI-C2-R2-INDEX@2026-05-26 |
| task_slug | wiki-c2-r2-index-sync |
| human_gate | 继承 HG-LOOP-BATCH |

**目标**（依赖 R1 RECENT draft 行存在）：
1. 在 `docs/harness/invokes/by-task/wiki-loop-c2-verify/README.md` 增 **验收说明** 一行（C2 verify 主目标 · 链 meta-reinspect 结论）。
2. 关账时：更新 `docs/tasks/_views/done.md` 索引；将 RECENT §6.6 本 Loop 行 **draft/in_progress → done**。

**占位**：无 HTML 占位；22 前须确认 R1 已在 `done/` 且 RECENT 行存在。

**非范围**：改 api/tests/prompts；重跑 B-Q3 实验

**帽子顺序**：22→30→40→50→关账 · PROMPT_LOOP round=R2 · **本 round 负责** RECENT done + _views

---

【commit】
- 3 task + invoke batch + 本目录 README/MANIFEST/BATCH/START/LOOP
- message：`docs(task): Wiki Loop C2 Verify Batch-10 · WIKI-LOOP-C2-VERIFY@2026-05-26`

【停】
- **勿** 执行 22
- 下一棒：人批 `HG-LOOP-BATCH` → [`PROMPT_START_loop_c2_verify_full_chain_v1.md`](./PROMPT_START_loop_c2_verify_full_chain_v1.md) §3
```
