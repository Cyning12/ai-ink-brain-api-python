# Invoke · governance-tasks-done-hygiene

> **最终目的**：完成后端 `docs/tasks/` done 索引治理，同步 Coding Wiki 链路，50 复检落盘，开 PR 合 `main`（文档-only）。  
> **Task 真值**：[`docs/tasks/active/task_governance_tasks_done_index_hygiene_v1.md`](../../active/task_governance_tasks_done_index_hygiene_v1.md)  
> **分支**：`task/governance-tasks-done-hygiene-v1`

---

## 帽序

```text
10-task（起草/ rethink） → 22 R1 审查 → 人签 HG-AUDIT-R1 → 30 执行 → 40 自检 → 50 复检 → 人签 HG-REINSPECT → PR → CLOSE
```

- `10`：由 Kimi Agent / Cursor Task 链承担 R0–R5 思考轮，产出 [`PROMPT_kimi_agent_rethink_R1_R5.md`](./PROMPT_kimi_agent_rethink_R1_R5.md)。
- `22`：审查 task，落盘 `docs/harness/reviews/by-task/governance-tasks-done-hygiene/task_governance_tasks_done_index_hygiene_audit_R1_*.md`。
- `30`：按 [`PROMPT_30_execute_docs_v1_zh.md`](./PROMPT_30_execute_docs_v1_zh.md) 执行文档索引治理，**禁止写 `api/**`。
- `40`：链接自检 + 验收标准回填。
- `50`：独立复检，落盘 `docs/tasks/reinspect_results/reinspect_governance_tasks_done_index_hygiene_*_v1.md`。
- **PR**：文档-only，body 含验收勾选 + 50 路径。

---

## 文件清单

| 文件 | 用途 |
|------|------|
| `PROMPT_kimi_agent_rethink_R1_R5.md` | 10-task / rethink 帽，R0–R5 框架 |
| `PROMPT_30_execute_docs_v1_zh.md` | 30 执行帽专用 Prompt |

---

## 给 Cursor

`governance-tasks-done-hygiene`、`_views/done.md`、`done/README.md`、`done_by_domain.md`、文档-only、链接自检
