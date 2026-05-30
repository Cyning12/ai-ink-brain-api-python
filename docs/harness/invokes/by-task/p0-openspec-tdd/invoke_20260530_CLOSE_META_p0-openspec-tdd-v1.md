# Invoke · 关账 · META · p0-openspec-tdd

| 字段 | 值 |
|------|-----|
| **round** | META |
| **hat** | CLOSE |
| **task** | `docs/tasks/done/task_harness_p0_openspec_tdd_loop_v1.md` |
| **task_slug** | `p0-openspec-tdd` |
| **freeze_id** | `HARNESS-P0-OPENSPEC-TDD-LOOP@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
P0 OpenSpec×TDD Loop **META 关账**（R1–R3 均 done/），严格遵循：
- docs/tasks/skills/SKILL-harness-loop-batch.md §长 Loop 完成汇报
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md

【元信息】
- loop_slug: p0-openspec-tdd
- freeze_id: HARNESS-P0-OPENSPEC-TDD-LOOP@2026-05-30
- git_branch: task/harness-p0-openspec-tdd

步骤 · META：
1. 勾选母单 §验收 · 状态 done
2. git mv task_harness_p0_openspec_tdd_loop_v1.md → done/
3. 更新 docs/tasks/_views/done.md（母单 + R3 行）
4. 落盘 REPORT_completion_20260530_v1.md（§1–§5）
5. 本 CLOSE invoke + HANDOFF_CLOSE_TRACE
6. commit（REPORT 可紧随单独 commit）

硬约束：docs-only Loop · META 仅关账 · 单 PR pytest 绿
```

---

## 执行路线与 Commit 回溯

**一句结论**：P0 OpenSpec×TDD Loop R1–R3 全关账；validate + 22/40 帽补丁 + change_status JSON + Cursor commands 已交付。

| round | task_slug | 关键交付 |
|-------|-----------|----------|
| R1 | p0-task-validate | `harness_task_validate.py` + pytest + 50 reinspect |
| R2 | p0-audit-selfcheck | 22/40 帽 OpenSpec×TDD 补丁 |
| R3 | p0-status-cursor | `harness_change_status.py` + `.cursor/commands/` |
| META | p0-openspec-tdd | 母单 done + REPORT |

**Commit 详见** `REPORT_completion_20260530_v1.md` §4。
