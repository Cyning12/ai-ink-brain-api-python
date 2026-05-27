# Invoke · 30 执行 · R1 · wiki-c2-r1-schedule-draft

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |
| **task_slug** | `wiki-c2-r1-schedule-draft` |
| **freeze_id** | `WIKI-C2-R1-SCHEDULE@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R1** · **30 执行帽**（上一帽 22 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R1
- task: docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md
- task_slug: wiki-c2-r1-schedule-draft
- freeze_id: WIKI-C2-R1-SCHEDULE@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1
- 22 review: docs/harness/reviews/by-task/wiki-loop-c2-verify/task_governance_loop_c2_verify_r1_schedule_draft_v1_audit_R1_20260526.md

【commit 硬纪律】交付完成后 git add 本轮路径 → commit message 须含 WIKI-C2-R1-SCHEDULE@2026-05-26 → 再戴 40 帽。

步骤 2 · 30 执行交付清单：
1. `docs/tasks/RECENT_TASK_SCHEDULE.md` §6.6 表增一行 **Wiki Loop C2 Verify**（状态 **draft** 或 **in_progress**，链至母 task active 路径）
2. §8 修订记录增一行（R1 RECENT draft 注记 · 含 freeze_id）
3. 可选：`docs/tasks/skills/SKILL-harness-loop-batch.md` 修订记录「第三 Loop C2 Verify 试点 @2026-05-26」——**禁止** Agent 改 SKILL status 字段
4. 回填 task §实现备忘（涉及文件、RECENT 行摘要）
5. 落盘本 invoke：`invoke_20260526_30_wiki-c2-r1-schedule-draft-v1.md`（§3 ≥15 行 · 非交付摘要 stub）
6. commit 后下一棒 = **40 自检帽**

硬约束：不改 api/、tests/、docs/harness/prompts/、CI workflow · 单 PR `task/wiki-loop-c2-verify-v1`
```
