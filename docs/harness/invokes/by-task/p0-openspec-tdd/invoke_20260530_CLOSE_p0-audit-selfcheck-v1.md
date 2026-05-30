# Invoke · 关账 · R2 · p0-audit-selfcheck

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | CLOSE |
| **task** | `docs/tasks/done/task_harness_p0_audit_selfcheck_v1.md` |
| **task_slug** | `p0-audit-selfcheck` |
| **freeze_id** | `HARNESS-P0-AUDIT-SELFCHECK@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **next_task** | `docs/tasks/active/task_harness_p0_status_cursor_v1.md` |

---

## §3 可复制 Prompt 正文

```text
P0 Loop R2 关账

1. git mv task_harness_p0_audit_selfcheck_v1.md → done/
2. 更新 _views/done.md
3. cross_round 续 R3 p0-status-cursor
commit: docs(task): P0 R2 关账 · HARNESS-P0-AUDIT-SELFCHECK@2026-05-30
```

---

## 执行路线与 Commit 回溯

**一句结论**：R2 22/40 帽 OpenSpec×TDD 补丁已落盘；R3 预审查零阻塞；50 跳过（not_applicable）。

**下一棒**：MANIFEST **R3** · `p0-status-cursor`
