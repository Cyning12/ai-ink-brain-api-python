# Invoke · 40 自检 · R1 · p0-task-validate

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_harness_p0_task_validate_v1.md` |
| **task_slug** | `p0-task-validate` |
| **freeze_id** | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R1** · **40 自检帽**（上一帽 30 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R1
- task: docs/tasks/active/task_harness_p0_task_validate_v1.md
- task_slug: p0-task-validate
- freeze_id: HARNESS-P0-TASK-VALIDATE@2026-05-30
- git_branch: task/harness-p0-openspec-tdd

【commit 硬纪律】自检表填完后 commit task + 本 invoke → 再戴 50 帽。

步骤 3 · 40 自检 — 须独立重跑以下 VERIFY 项（禁止仅引用 30 对话摘要）：

VERIFY-1（单测）：
  pytest tests/test_harness_task_validate.py -v
  → 6 passed

VERIFY-2（CLI 本 task）：
  python tools/harness_task_validate.py docs/tasks/active/task_harness_p0_task_validate_v1.md
  → exit 0 · 输出 OK

VERIFY-3（全量 Required）：
  pytest tests -m "not intent_eval and not intent_benchmark"
  → 全绿

VERIFY-4（invoke C2 · 22/30 已落盘）：
  wc -c docs/harness/invokes/by-task/p0-openspec-tdd/invoke_20260530_{22,30}_p0-task-validate-v1.md
  → 各文件 ≥800B

交付：
1. 填 task ### 自检结论（执行者）表
2. 落盘 invoke_20260530_40_p0-task-validate-v1.md
3. commit 含 HARNESS-P0-TASK-VALIDATE@2026-05-30
4. 下一棒 = **50 独立复检帽**（required）

硬约束：不改 api/ 业务
```
