# Invoke · 22 任务审核 · R2 · p0-audit-selfcheck

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md` |
| **task_slug** | `p0-audit-selfcheck` |
| **freeze_id** | `HARNESS-P0-AUDIT-SELFCHECK@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R2** · **22 任务审核帽**，严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md
- docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md §4.2–4.3

【元信息】
- round: R2
- task: docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md
- task_slug: p0-audit-selfcheck
- freeze_id: HARNESS-P0-AUDIT-SELFCHECK@2026-05-30
- git_branch: task/harness-p0-openspec-tdd
- 前置: R1 task_harness_p0_task_validate_v1.md 在 done/
- cross_round_semi_auto: true

步骤 1 · 22：
1. python tools/harness_human_gate_check.py --task docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md
2. 审 R2 task 范围（22/40 帽补丁 · 不改 tools/）
3. 落盘 R2 review：docs/harness/reviews/by-task/p0-audit-selfcheck/task_harness_p0_audit_selfcheck_v1_audit_R1_20260530.md
4. 落盘 R3 预审查（零阻塞）：.../task_harness_p0_status_cursor_v1_preflight_R1_20260530.md
5. 无阻塞 → 准许 30
6. commit review + invoke

硬约束：docs/harness/prompts/hats/ 仅本 round · 50 可选
```
