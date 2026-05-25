# Invoke · P0-A1 — 扩展 TASK_TEMPLATE Harness 字段

## 元信息

| 字段 | 值 |
|------|-----|
| hat_id | 30（文档执行） |
| template | `RECENT_TASK_SCHEDULE` §0.2 A1 |
| git_branch | `task/chore-diary-tmp-ignore-and-main-branch-policy` |
| worktree_root | `ai-ink-brain-api-python` |
| task_paths | `docs/tasks/templates/TASK_TEMPLATE.md` |
| VERIFY | 模板含 §5 字段；链 `HARNESS_V2_PLAN` §5、`HANDOFF_SEMI_AUTO` |

---

## §3 可复制 Prompt 快照（下一棒 P0-A2）

```text
你正在执行 **RECENT_TASK_SCHEDULE P0-A2**：在 `docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md` 增补 **Harness 状态栏（版本 B）**（每棒结束须输出）。

## 输入

- 工作分支：`task/chore-diary-tmp-ignore-and-main-branch-policy`（勿切 main、勿新建 harness-improve 分支）
- 真值：`docs/diary/2026-05-22-harness-evaluation-improvement-response.md` §3.2（版本 B 为对话默认）
- 参照：`HANDOFF_CLOSE_TRACE.md`（状态栏 vs 关账回溯分工）

## 你必须完成

1. 在 `handoff/HANDOFF_SEMI_AUTO.md` 新增 §「每棒状态栏（版本 B）」：多行结构化字段（当前帽、audit_profile、human_gate 摘要、下一棒 A/B、分支名）。
2. 可选一句同步 `.cursor/rules/05-harness-semi-auto.mdc`（不扩写全文）。
3. 更新 `RECENT_TASK_SCHEDULE.md`：A2 标 **done** 并划掉。
4. 落盘 invoke + 按 `HANDOFF_AUTO_COMMIT.md` commit。

## 禁止

- 用推荐替代人择 A/B；代填 `human_gate: approved`
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：A1 完成，下一棒 A2 快照 |
