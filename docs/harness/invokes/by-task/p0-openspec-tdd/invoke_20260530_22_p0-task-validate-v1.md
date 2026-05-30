# Invoke · 22 任务审核 · R1 · p0-task-validate

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_harness_p0_task_validate_v1.md` |
| **task_slug** | `p0-task-validate` |
| **freeze_id** | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R1** · **22 任务审核帽**（上一帽 START 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）
- docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md §4.1

【元信息】
- round: R1
- task: docs/tasks/active/task_harness_p0_task_validate_v1.md
- task_slug: p0-task-validate
- freeze_id: HARNESS-P0-TASK-VALIDATE@2026-05-30
- git_branch: task/harness-p0-openspec-tdd
- 母 task: docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md
- invoke 目录: docs/harness/invokes/by-task/p0-openspec-tdd/
- cross_round_semi_auto: true

【commit 硬纪律】每帽结束 before 下一帽：git add → commit → 回复 `已提交：@ <short-hash>`。

步骤 0 · Gate：
  python tools/harness_human_gate_check.py --task docs/tasks/active/task_harness_p0_task_validate_v1.md
  → exit 0（母单 HG-LOOP-BATCH approved）

步骤 1 · 22 任务审核：
1. 审 task §范围 / §非范围 / §failure_paths / §行为变更 Delta / §验收 / Harness 元信息表。
2. 对照 SPEC §4.1 规则清单；test_strategy=required 且交付 tools/+tests/ 合理。
3. 落盘 review：docs/harness/reviews/by-task/p0-task-validate/task_harness_p0_task_validate_v1_audit_R1_20260530.md
4. 审查结论须含：已核对项表、阻塞/非阻塞、是否准许 30、签收/关闭、下一棒可复制 Prompt。
5. 无阻塞 → 准许 **30** 执行帽开工。
6. commit review + 本 invoke（invoke 未过 C2 不得 commit）。

硬约束：单 PR · 不改 api/ 业务 · R1 须 50 required
```
