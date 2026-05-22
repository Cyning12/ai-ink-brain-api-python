# Invoke · P0-A3 — 10 帽 A/B 推荐

## 元信息（版本 C 摘要）

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task | `RECENT_TASK_SCHEDULE` §0.2 A3 |
| audit_profile | post_close |
| git_branch | `task/chore-diary-tmp-ignore-and-main-branch-policy` |
| human_gate | 无 |
| next | P0-A4 |
| block | 无 |

---

## §3 可复制 Prompt 快照（下一棒 P0-A4）

```text
你正在执行 **RECENT_TASK_SCHEDULE P0-A4**：在 `docs/harness/README.md` §4 标明 `rsync` **仅维护者**、非 Agent 日常路径。

## 输入

- 工作分支：`task/chore-diary-tmp-ignore-and-main-branch-policy`
- 文件：`docs/harness/README.md`（及若存在的 `README.workspace-upstream.md` 交叉链）
- 真值：Harness 评价回复 §2（rsync 偶发同步，非 Agent 必读）

## 你必须完成

1. §4（或等价节）明确：rsync 面向维护者；Agent 只读本仓 `docs/harness/prompts/`。
2. `RECENT_TASK_SCHEDULE.md`：A4 标 **done** 并划掉；invoke + commit。
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：A3 完成，下一棒 A4 快照 |
