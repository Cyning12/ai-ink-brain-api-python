# Loop Manifest · P0 OpenSpec×TDD（R1–R3 + META）

> **git_branch**：`task/harness-p0-openspec-tdd`  
> **母 task**：`docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md`  
> **全链启动**：[`PROMPT_START_p0_full_chain_v1.md`](./PROMPT_START_p0_full_chain_v1.md)  
> **Step 0**：O1–O3 模板已在分支首 commit（`TASK_TEMPLATE` Delta/Scenario/规划 artifact）

| round | task_path | task_slug | freeze_id | 前置 |
|-------|-----------|-----------|-----------|------|
| **R1** | `docs/tasks/active/task_harness_p0_task_validate_v1.md` | `p0-task-validate` | `HARNESS-P0-TASK-VALIDATE@2026-05-30` | `HG-LOOP-BATCH` approved |
| **R2** | `docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md` | `p0-audit-selfcheck` | `HARNESS-P0-AUDIT-SELFCHECK@2026-05-30` | R1 → `done/` |
| **R3** | `docs/tasks/active/task_harness_p0_status_cursor_v1.md` | `p0-status-cursor` | `HARNESS-P0-STATUS-CURSOR@2026-05-30` | R2 → `done/` |
| **META** | `docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md` | `p0-openspec-tdd` | `HARNESS-P0-OPENSPEC-TDD-LOOP@2026-05-30` | R1–R3 均 `done/` |

**顺序（硬）**：R1 validate → R2 22/40 → R3 status/cursor → META  
**成功判据**：单 PR · pytest Required 绿 · R1 `required` 须 50
