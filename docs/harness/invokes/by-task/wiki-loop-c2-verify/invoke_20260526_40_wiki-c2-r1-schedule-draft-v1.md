# Invoke · 40 自检 · R1 · wiki-c2-r1-schedule-draft

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |
| **task_slug** | `wiki-c2-r1-schedule-draft` |
| **freeze_id** | `WIKI-C2-R1-SCHEDULE@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R1** · **40 自检帽**（上一帽 30 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R1
- task: docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md
- task_slug: wiki-c2-r1-schedule-draft
- freeze_id: WIKI-C2-R1-SCHEDULE@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1

【commit 硬纪律】自检表填完后 commit task + 本 invoke → 再戴 50 帽。

步骤 3 · 40 自检 — 须独立重跑以下 VERIFY 项（禁止仅引用 30 对话摘要）：

VERIFY-1（task §验收）：
  rg 'Loop C2 Verify' docs/tasks/RECENT_TASK_SCHEDULE.md
  → 须命中 §6.6 表行

VERIFY-2（状态非 done）：
  目视 RECENT §6.6 本 Loop 行状态为 draft 或 in_progress（**非** done）

VERIFY-3（invoke C2 · 22/30 已落盘）：
  wc -c docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_20260526_{22,30}_wiki-c2-r1-schedule-draft-v1.md
  → 各文件 ≥800B 或 §3 ≥15 行

交付：
1. 填 task ### 自检结论（执行者）表（RECENT §6.6 · invoke C2 初检）
2. 落盘 invoke_20260526_40_wiki-c2-r1-schedule-draft-v1.md
3. commit 含 WIKI-C2-R1-SCHEDULE@2026-05-26
4. 下一棒 = **50 独立复检帽**

硬约束：不改 api/tests/prompts/CI
```
