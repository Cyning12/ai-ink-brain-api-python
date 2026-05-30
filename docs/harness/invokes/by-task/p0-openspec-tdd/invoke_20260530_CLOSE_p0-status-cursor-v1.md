# Invoke · 关账 · R3 · p0-status-cursor

| 字段 | 值 |
|------|-----|
| **round** | R3 |
| **hat** | CLOSE |
| **task** | `docs/tasks/done/task_harness_p0_status_cursor_v1.md` |
| **task_slug** | `p0-status-cursor` |
| **freeze_id** | `HARNESS-P0-STATUS-CURSOR@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **next_task** | `docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md` (META) |

---

## §3 可复制 Prompt 正文

```text
P0 Loop R3 关账 → META

1. git mv task_harness_p0_status_cursor_v1.md → done/
2. 更新 _views/done.md
3. 续 META 母单关账 + REPORT_completion_*
commit: docs(task): P0 R3 关账 · HARNESS-P0-STATUS-CURSOR@2026-05-30
```

---

## 执行路线与 Commit 回溯

**一句结论**：O5 change_status JSON + O6 Cursor commands 已交付；R1–R3 全 done 后 META 关账。

**下一棒**：MANIFEST **META** · `p0-openspec-tdd`
