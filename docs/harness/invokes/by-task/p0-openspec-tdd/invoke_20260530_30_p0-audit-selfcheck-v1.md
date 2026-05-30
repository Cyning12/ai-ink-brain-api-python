# Invoke · 30 执行 · R2 · p0-audit-selfcheck

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md` |
| **task_slug** | `p0-audit-selfcheck` |
| **freeze_id** | `HARNESS-P0-AUDIT-SELFCHECK@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R2** · **30 执行帽**（上一帽 22 已结束），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md §4.2–4.3

【元信息】
- round: R2
- task: docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md
- task_slug: p0-audit-selfcheck
- freeze_id: HARNESS-P0-AUDIT-SELFCHECK@2026-05-30
- git_branch: task/harness-p0-openspec-tdd

步骤 2 · 30 交付清单：
1. 22-task-audit.md 增 OpenSpec×TDD 四勾选项 + validate CLI 链
2. 40-self-check.md 增 Completeness/Correctness/Coherence 三维表
3. reviews/README.md 增 harness_task_validate 指针
4. R3 预审查 md 已在 22 落盘
5. 回归：python tools/harness_task_validate.py docs/tasks/done/task_harness_p0_task_validate_v1.md
6. commit → 40 自检（50 可选跳过）

禁止：改 tools/ · api/ · TEMPLATE
```
