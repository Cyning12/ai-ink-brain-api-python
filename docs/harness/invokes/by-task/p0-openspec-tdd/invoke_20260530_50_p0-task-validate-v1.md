# Invoke · 50 独立复检 · R1 · p0-task-validate

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 50 |
| **task** | `docs/tasks/active/task_harness_p0_task_validate_v1.md` |
| **task_slug** | `p0-task-validate` |
| **freeze_id** | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R1** · **50 独立复检帽**（上一帽 40 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R1
- task: docs/tasks/active/task_harness_p0_task_validate_v1.md
- task_slug: p0-task-validate
- freeze_id: HARNESS-P0-TASK-VALIDATE@2026-05-30
- git_branch: task/harness-p0-openspec-tdd

【commit 硬纪律】复检报告落盘后 commit reinspect + 本 invoke → 再执行本 round 关账。

步骤 4 · 50 独立复检（须 **独立重跑** 40 VERIFY，禁止仅复读 40 表）：

VERIFY-1：
  pytest tests/test_harness_task_validate.py -q

VERIFY-2：
  python tools/harness_task_validate.py docs/tasks/active/task_harness_p0_task_validate_v1.md; echo exit=$?

VERIFY-3：
  pytest tests -m "not intent_eval and not intent_benchmark" -q

VERIFY-4 · human_gate diff：
  母单 HG-LOOP-BATCH approved · 子单继承 · 无 Agent 代填

VERIFY-5 · invoke C2 抽检：
  ls docs/harness/invokes/by-task/p0-openspec-tdd/invoke_20260530_{22,30,40,50}_p0-task-validate-v1.md

落盘：
  docs/tasks/reinspect_results/reinspect_p0-task-validate_20260530_v1.md

结论：test_strategy required → 建议关账（全部 VERIFY pass）

硬约束：50 证据独立于 40；不改 api/ 业务
```
