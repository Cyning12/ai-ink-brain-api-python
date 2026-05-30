# Invoke · 22 任务审核 · R3 · p0-status-cursor

| 字段 | 值 |
|------|-----|
| **round** | R3 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_harness_p0_status_cursor_v1.md` |
| **task_slug** | `p0-status-cursor` |
| **freeze_id** | `HARNESS-P0-STATUS-CURSOR@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R3** · **22 任务审核帽**，严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md
- docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md §5

【元信息】
- round: R3
- task: docs/tasks/active/task_harness_p0_status_cursor_v1.md
- task_slug: p0-status-cursor
- freeze_id: HARNESS-P0-STATUS-CURSOR@2026-05-30
- git_branch: task/harness-p0-openspec-tdd
- 前置: R2 task_harness_p0_audit_selfcheck_v1.md 在 done/
- R2 预审查: docs/harness/reviews/by-task/p0-audit-selfcheck/task_harness_p0_status_cursor_v1_preflight_R1_20260530.md
- cross_round_semi_auto: true

步骤 1 · 22：
1. python tools/harness_human_gate_check.py --task docs/tasks/active/task_harness_p0_status_cursor_v1.md
2. 审 O5 change_status --json + O6 Cursor commands + tests
3. 落盘 review：docs/harness/reviews/by-task/p0-status-cursor/task_harness_p0_status_cursor_v1_audit_R1_20260530.md
4. 无阻塞 → 准许 30
5. commit review + invoke

硬约束：不改 api/ · 复用 R1 validate 解析
```
