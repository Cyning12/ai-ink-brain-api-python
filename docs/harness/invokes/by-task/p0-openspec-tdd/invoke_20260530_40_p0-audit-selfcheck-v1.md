# Invoke · 40 自检 · R2 · p0-audit-selfcheck

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md` |
| **task_slug** | `p0-audit-selfcheck` |
| **freeze_id** | `HARNESS-P0-AUDIT-SELFCHECK@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R2** · **40 自检帽**（上一帽 30 已结束），严格遵循：
- docs/harness/prompts/hats/40-self-check.md（含 T3 三维表）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md

【元信息】
- round: R2
- task_slug: p0-audit-selfcheck
- freeze_id: HARNESS-P0-AUDIT-SELFCHECK@2026-05-30

步骤 3 · 40 自检 VERIFY：
VERIFY-1：rg 'OpenSpec × TDD' docs/harness/prompts/hats/22-task-audit.md
VERIFY-2：rg 'Completeness' docs/harness/prompts/hats/40-self-check.md
VERIFY-3：python tools/harness_task_validate.py docs/tasks/done/task_harness_p0_task_validate_v1.md
VERIFY-4：三维自检摘要写入 task §自检结论

50 可选（not_applicable）→ 跳过，直接 CLOSE 关账
commit 含 HARNESS-P0-AUDIT-SELFCHECK@2026-05-30
```
