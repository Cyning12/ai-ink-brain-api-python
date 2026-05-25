# Invoke · P0-A2 — HANDOFF 状态栏（版本 B）

## 元信息（版本 C 摘要）

| 字段 | 值 |
|------|-----|
| hat_id | 30 |
| task | `RECENT_TASK_SCHEDULE` §0.2 A2 |
| audit_profile | post_close |
| git_branch | `task/chore-diary-tmp-ignore-and-main-branch-policy` |
| human_gate | 无 |
| next | P0-A3 |
| block | 无 |

---

## §3 可复制 Prompt 快照（下一棒 P0-A3）

```text
你正在执行 **RECENT_TASK_SCHEDULE P0-A3**：在 10 帽模板中增补 **双 Prompt A/B**、标题 **`（推荐）`** 与一行推荐理由。

## 输入

- 工作分支：`task/chore-diary-tmp-ignore-and-main-branch-policy`
- 文件：`docs/harness/prompts/hats/10-requirements.md`、`docs/harness/prompts/templates/TEMPLATE-requirements-invoke.md`
- 真值：Harness 评价回复 §3.3；`handoff/HANDOFF_SEMI_AUTO.md` §3.4（状态栏，本棒已 done）
- 硬规则：仍输出 A、B **全文**；推荐 **不得** 替代人择或自动执行下一帽

## 你必须完成

1. 10 结束须给下一棒 **A（22）+ B（30）** 两条 Prompt，其中一路标题加 `（推荐）` + 理由表（audit_profile / test_strategy 启发式，task 显式声明优先）。
2. 同步 `TEMPLATE-requirements-invoke.md` §3 示例与禁止项。
3. `RECENT_TASK_SCHEDULE.md`：A3 标 **done** 并划掉；落盘 invoke + commit。

## 禁止

- Agent 因推荐自动走路径；代填 human_gate approved
```

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：A2 完成，下一棒 A3 快照 |
