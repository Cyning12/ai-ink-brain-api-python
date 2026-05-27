# Invoke · 50 独立复检 · R1 · wiki-c2-r1-schedule-draft

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 50 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |
| **task_slug** | `wiki-c2-r1-schedule-draft` |
| **freeze_id** | `WIKI-C2-R1-SCHEDULE@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R1** · **50 独立复检帽**（上一帽 40 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R1
- task: docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md
- task_slug: wiki-c2-r1-schedule-draft
- freeze_id: WIKI-C2-R1-SCHEDULE@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1

【commit 硬纪律】复检报告落盘后 commit reinspect + 本 invoke → 再执行本 round 关账。

步骤 4 · 50 独立复检（须 **独立重跑** 40 VERIFY，禁止仅复读 40 表）：

VERIFY-1：
  rg 'Loop C2 Verify' docs/tasks/RECENT_TASK_SCHEDULE.md

VERIFY-2：
  确认 §6.6 行状态为 in_progress（非 done）

VERIFY-3 · invoke C2 抽检（本 round 已落盘 22/30/40/50）：
  wc -c docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_20260526_{22,30,40,50}_wiki-c2-r1-schedule-draft-v1.md
  目视各文件 §3 为可复制 Prompt（非 stub 摘要）

落盘：
  docs/tasks/reinspect_results/reinspect_wiki-c2-r1-schedule-draft_20260526_v1.md

结论二选一：
- **建议关账** — 全部 VERIFY pass · invoke C2 pass
- **须回 30** — 任一 FAIL

硬约束：50 证据独立于 40；不改 api/tests/prompts/CI
```
