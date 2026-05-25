# Invoke · P0-A4 — harness README rsync 仅维护者

## 元信息（版本 C 摘要）

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task | `RECENT_TASK_SCHEDULE` §0.2 A4 |
| audit_profile | post_close |
| git_branch | `task/chore-diary-tmp-ignore-and-main-branch-policy` |
| human_gate | 无 |
| next | P0-B/C 或 P0-A PR |
| block | 无 |

---

## §3 可复制 Prompt 快照（P0-A 完成后 · 二选一）

```text
【路径 A · 推荐】开 PR 合入 P0-A 文档批（A1–A4）

分支：task/chore-diary-tmp-ignore-and-main-branch-policy
base：main
范围：TASK_TEMPLATE、HANDOFF 状态栏、10 A/B 推荐、harness README §4
合并后再在 main 上 rebase/拉取，继续 P0-B/C。

【路径 B】直接 P0-B/C 试点（task_05）

1. 在 docs/tasks/active/ 按 TASK_TEMPLATE 完善或新建 task_05（Harness 元信息齐全）
2. 分支 task/query-rewrite-obs（或与 slug 一致）
3. 10 帽 → 人择 22/30 → … → 首份新 reviews R1
见 RECENT_TASK_SCHEDULE §0.3
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：A4 完成；P0-A 收口 |
