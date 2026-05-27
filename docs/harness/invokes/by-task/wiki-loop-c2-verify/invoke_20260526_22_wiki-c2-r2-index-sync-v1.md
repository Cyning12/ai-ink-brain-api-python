# Invoke · 22 任务审核 · R2 · wiki-c2-r2-index-sync

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md` |
| **task_slug** | `wiki-c2-r2-index-sync` |
| **freeze_id** | `WIKI-C2-R2-INDEX@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R2** · **22 任务审核帽**（上一 round R1 已关账；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R2
- task: docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md
- task_slug: wiki-c2-r2-index-sync
- freeze_id: WIKI-C2-R2-INDEX@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1
- PREV_DONE_TASK: docs/tasks/done/task_governance_loop_c2_verify_r1_schedule_draft_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-c2-verify/

【commit 硬纪律】review + invoke 落盘 → commit → 再戴 30。

R2 22 开工前额外步骤（PROMPT_LOOP §2）：
1. 确认 R1 在 docs/tasks/done/ 且 RECENT §6.6 含 Loop C2 Verify 行（in_progress）
2. 读 R1 done task §实现备忘 / §自检 / R1 CLOSE invoke 回溯

步骤 1 · 22：
1. 审 task §范围/§非范围/§failure_paths（含 F2：R2 invoke **禁止 stub**）
2. 落盘 review：task_governance_loop_c2_verify_r2_index_sync_v1_audit_R1_20260526.md
3. 无阻塞 → 准许 30
4. commit（invoke C2 自检：§3 ≥15 行 · 元信息含 task_slug）

硬约束：单 PR · C2 全绿为本 Loop 主验收 · 不改 api/tests/prompts/CI
```
