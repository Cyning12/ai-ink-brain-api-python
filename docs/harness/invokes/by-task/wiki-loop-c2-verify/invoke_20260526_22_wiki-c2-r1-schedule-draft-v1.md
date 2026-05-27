# Invoke · 22 任务审核 · R1 · wiki-c2-r1-schedule-draft

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |
| **task_slug** | `wiki-c2-r1-schedule-draft` |
| **freeze_id** | `WIKI-C2-R1-SCHEDULE@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R1** · **22 任务审核帽**（上一帽已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R1
- task: docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md
- task_slug: wiki-c2-r1-schedule-draft
- freeze_id: WIKI-C2-R1-SCHEDULE@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1
- 母 task: docs/tasks/active/task_harness_wiki_loop_c2_verify_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-c2-verify/
- cross_round_semi_auto: true

【授权】semi_auto 跨 round：R1 关账后按 LOOP_MANIFEST 续 R2→META。每帽 invoke §3 全文落盘 + commit。

【commit 硬纪律】每帽结束 before 下一帽：git add → commit → 回复 `已提交：@ <short-hash>`。

步骤 0 跳过（R1 · PLACEHOLDER_ID = 无）。

步骤 1 · 22 任务审核：
1. 确认母 task `HG-LOOP-BATCH` = **approved**（禁止 Agent 代填 pending）。
2. 审 task §范围 / §非范围 / §failure_paths / §验收标准 / Harness 元信息表。
3. 子 task 写「继承母闸」；本 round 职责 = RECENT §6.6 **draft/in_progress** 行（**不**标 done）。
4. 落盘 review：docs/harness/reviews/by-task/wiki-loop-c2-verify/task_governance_loop_c2_verify_r1_schedule_draft_v1_audit_R1_20260526.md
5. 审查结论须含：已核对项表、阻塞/非阻塞、是否准许 30、签收/关闭、下一棒可复制 Prompt。
6. 无阻塞 → 准许 **30** 执行帽开工。
7. commit review + 本 invoke（invoke 未过 C2 不得 commit）。

硬约束：单 PR · 不改 api/tests/prompts/CI · **C2 invoke 质量全绿**为本 Loop 主验收
```
