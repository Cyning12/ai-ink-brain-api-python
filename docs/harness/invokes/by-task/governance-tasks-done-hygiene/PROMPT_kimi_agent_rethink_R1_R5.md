# PROMPT · Kimi Agent rethink R1–R5（governance-tasks-done-hygiene）

> **阶段**：10-task / rethink  
> **目标**：在 22 R1 审查前，完成 task `task_governance_tasks_done_index_hygiene_v1.md` 的 R0–R5 思考轮回填，确保索引治理方案可行、链接不漂移、50 有落盘路径。  
> **约束**：不写 `api/**`；不改业务代码；只补全 task 文档与 invoke。

---

## 1. 必读（按顺序）

1. [`docs/tasks/active/task_governance_tasks_done_index_hygiene_v1.md`](../../active/task_governance_tasks_done_index_hygiene_v1.md)
2. [`docs/tasks/README.md`](../../../tasks/README.md)
3. [`docs/tasks/_views/done.md`](../../../tasks/_views/done.md)
4. [`docs/tasks/RECENT_TASK_SCHEDULE.md`](../../../tasks/RECENT_TASK_SCHEDULE.md) §6.1 / §6.6
5. [`docs/coding_wiki/CODING_WIKI.md`](../../../coding_wiki/CODING_WIKI.md)
6. [`docs/coding_wiki/concepts/task-schedule-ink-backend.md`](../../../coding_wiki/concepts/task-schedule-ink-backend.md)
7. [`cyning-harness/harness/templates/TASK_done_README.md`](../../../../../../cyning-harness/harness/templates/TASK_done_README.md)
8. [`cyning-harness/harness/templates/VIEW_done_by_domain.md`](../../../../../../cyning-harness/harness/templates/VIEW_done_by_domain.md)
9. [`cyning-harness/harness/templates/VIEW_done_thin_pointer.md`](../../../../../../cyning-harness/harness/templates/VIEW_done_thin_pointer.md)
10. [`cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md`](../../../../../../cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md)

---

## 2. 思考轮问题（必须逐条回答）

### R0 · 读 task / SPEC / 非范围

- `done/` 当前到底有多少篇 `.md`？列出最近 20 篇文件名前缀分布。
- 哪些域最拥挤？哪些域最稀疏？
- 现有 `_views/done.md` 多少行？是否已超过「薄指针」阈值？
- 本 task 明确排除的 bulk `git mv` 会带来什么风险？

### R1 · 代码/文档事实

- `docs/tasks/README.md` 当前归档流程是否提到域子目录？若否，需在哪里插入 Hub 纪律？
- `docs/coding_wiki/index.md` 与 `task-schedule-ink-backend.md` 当前是否链到 `done/README.md`？若否，最佳插入点在哪里？
- 现有 syntheses 的 `source_task` 是否都指向扁平 `done/task_*.md`？是否需要因本 task 而改动？
- `done/` 中是否有 `legacy/` 或命名不规范文件需要特殊处理？

### R2 · 方案对比

- 方案 α：P0 只做 Hub + 薄指针，不改物理路径。
- 方案 β：P0 同步 bulk `git mv` 到域子目录。
- 本 task 为何选 α？代价是什么？P1 子 task 应如何描述？
- `_views/done_by_domain.md` 与 Hub 的维护关系：双向同步还是 Hub 单向真值？

### R3 · 边界 / 测试 / failure_paths

- 如何确保 Hub 中链接不 404？自检命令是什么？
- 如何防止 Agent 只读旧 `_views/done.md` 而忽略 Hub？
- 50 复检应抽检哪些域/链接？
- 若 `done/README.md` 与 `_views/done_by_domain.md` 不一致，失败路径 F2 如何触发？

### R4 · 链接自检 / PR 策略

- 推荐用什么工具/命令做相对链接自检？（可手工 `rg` / Python / markdown-link-check）
- PR body 应包含哪些验收勾选？
- 文档-only PR 的 CI 如何处理？（无 pytest 回归，但可能有 ruff / markdown lint）

### R5 · 图谱/契约增量 + 关账判断

- 本 task 是否改 `docs/_tech_graph/`？（否）
- 本 task 是否改 `api/` 契约？（否）
- 关账时必须生成的 `freeze_id` 建议格式？
- 是否存在必须回填到 `RECENT_TASK_SCHEDULE.md` 的条目？

---

## 3. 输出格式

在 task 文件 `docs/tasks/active/task_governance_tasks_done_index_hygiene_v1.md` 的 **§5 思考轮次** 中逐条回填：

```markdown
### R0 · 读 task / SPEC / 非范围

- 回答 1
- 回答 2
...
```

并更新 **思考轮控制表**：

```markdown
| 字段 | 值 |
|------|-----|
| **actual_last_round** | `R5` |
| **early_stop** | `no` |
| **early_stop_reason** | — |
| **residual_risks** | `none` 或逐条 |
```

---

## 4. 禁止

- 不写 `api/**`。
- 不改 `packages/**`。
- 不新建 `docs/spec/` 行为变更。
- 不批量 `git mv` `done/` 文件。
- 不修改 `HG-*` 闸的 `status`（仅人可改）。

---

## 5. 交接物

完成 R0–R5 后，输出：

1. 已更新的 task 文件路径。
2. 是否建议进入 22 R1（yes/no + 理由）。
3. 若有阻塞，列出清单并建议退回 10 补全。

---

## 给 Kimi

`governance-tasks-done-hygiene`、R0–R5、Hub、薄指针、域子目录、链接自检、文档-only
