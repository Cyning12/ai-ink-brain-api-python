# Invoke · governance-tasks-done-hygiene

> **最终目的**：完成后端 `docs/tasks/` done 索引治理，同步 Coding Wiki 链路，50 复检落盘，开 PR 合 `main`（文档-only）。  
> **Task 真值**：[`docs/tasks/done/task_governance_tasks_done_index_hygiene_v1.md`](../../../../tasks/done/task_governance_tasks_done_index_hygiene_v1.md) · PR #160 · `GOV-TASKS-DONE-HYGIENE@2026-06-13`  
> **分支**：`task/governance-tasks-done-hygiene-v1`

---

## 帽序

```text
10-task → 22 R1 → 人签 → 30 → 40 → 50 → 人签 HG-REINSPECT → PR → CLOSE
```

---

## Prompt 索引

| 文件 | 用途 |
|------|------|
| [`PROMPT_kimi_agent_rethink_R1_R5.md`](./PROMPT_kimi_agent_rethink_R1_R5.md) | 10-task · R0–R5 |
| [`PROMPT_30_execute_docs_v1_zh.md`](./PROMPT_30_execute_docs_v1_zh.md) | 30 主交付（Hub + Wiki） |
| [`PROMPT_30_post_close_hygiene_v1_zh.md`](./PROMPT_30_post_close_hygiene_v1_zh.md) | 关账后卫生修复 Prompt |
| [`SUMMARY_post_close_hygiene_20260613.md`](./SUMMARY_post_close_hygiene_20260613.md) | **关账后卫生修复总结（G1–G7 pass · SKILL 已更新）** |
| [`SUMMARY_post_close_hygiene_TEMPLATE.md`](./SUMMARY_post_close_hygiene_TEMPLATE.md) | SUMMARY 骨架模板 |

---

## 关账后

- **2026-06-13**：关账后卫生修复已完成，G1–G7 全部 pass，详见 [`SUMMARY_post_close_hygiene_20260613.md`](./SUMMARY_post_close_hygiene_20260613.md)。
- **SKILL 更新**：`SKILL-docs-governance.md` H2 与 `SKILL-harness-task.md` 关账 checklist 第 3 项已对齐 Hub 纪律；两 SKILL 仍保持 `draft` 状态，待人工审阅后标 `active`。
- **遗留**：P1 子 task 将分批 `git mv` 138 篇 done task 到 `done/<domain>/`。

---

## 给 Cursor

`governance-tasks-done-hygiene`、`post-close`、`SKILL-docs-governance`、`Hub`、卫生修复
