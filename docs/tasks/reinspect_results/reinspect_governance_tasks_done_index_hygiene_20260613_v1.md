# 独立复检报告 · governance-tasks-done-hygiene

> **Task**：[`docs/tasks/done/task_governance_tasks_done_index_hygiene_v1.md`](../done/task_governance_tasks_done_index_hygiene_v1.md)  
> **复检日期**：2026-06-13  
> **复检人**：50 帽（独立）  
> **结论**：**pass / 无阻塞**

---

## 1. 复检范围

- `docs/tasks/done/README.md` — 域 Hub
- `docs/tasks/_views/done_by_domain.md` — 按域分组视图
- `docs/tasks/_views/done.md` — 薄指针
- `docs/tasks/README.md` — 归档流程更新
- `docs/coding_wiki/concepts/task-schedule-ink-backend.md` — Wiki 排期 hub 链路
- `docs/coding_wiki/index.md` — syntheses source_task 与 Hub 关系说明
- `docs/coding_wiki/CODING_WIKI.md` — ingest/query 纪律更新

---

## 2. 抽检清单与结果

| # | 检查项 | 方法 | 结果 |
|---|--------|------|------|
| 1 | `_views/done.md` ≤15 行 | `wc -l` | 10 行 ✅ |
| 2 | Hub 覆盖主域 | 目视 | harness / governance / chatbi / engineering / standards / epics 六域 ✅ |
| 3 | Hub 与 `done_by_domain.md` 域表一致 | 抽样对比 10 条 | 一致 ✅ |
| 4 | 所有索引链接有效 | Python 脚本扫描 7 个文件、356 个仓内相对链接 | zero BROKEN ✅ |
| 5 | 跨仓链接可解释 | 核对 `cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md` | 工作区中存在，作为域推断引用 ✅ |
| 6 | `docs/tasks/README.md` 归档流程更新 | 目视 | Hub / `done_by_domain` / 薄指针纪律已写入 ✅ |
| 7 | Coding Wiki 三文件已链 Hub | 目视 + 链接扫描 | task-schedule-ink-backend / index / CODING_WIKI 均含 Hub 指针 ✅ |
| 8 | 无 `api/` 或业务代码变更 | `git diff --name-only` | 仅 markdown 文件 ✅ |
| 9 | task 状态与范围勾选 | 目视 | A1–A6、B1–B4 已勾选；C、D、E 待关账 ✅ |

---

## 3. 域分布核对

| 域 | 文件数 | 抽样检查 |
|----|--------|----------|
| harness | 12 | ✅ 链接有效 |
| governance | 39 | ✅ 链接有效 |
| chatbi | 42 | ✅ 链接有效 |
| engineering | 29 | ✅ 链接有效 |
| standards | 6 | ✅ 链接有效 |
| epics | 11 | ✅ 链接有效 |
| **合计** | **139** | 注：含本 task 自身仍在 active，Hub 当前仅列 138 篇 done task |

---

## 4. 发现与说明

- **跨仓链接 3 处**：`docs/tasks/done/README.md`、`docs/tasks/README.md`、`docs/coding_wiki/CODING_WIKI.md` 均指向 `cyning-harness/harness/templates/FRAGMENT_task_domain_infer_v1_zh.md`。该文件在工作区 `Projects/cyning-harness/` 中存在，作为域推断规范引用，不视为 broken。
- **遗留未跟踪文件**：`docs/tasks/active/task_standards_backend_p3_p4_l3_ruff_v1.md` 在 `_views/done.md` 中已标 done（2026-06-09），但仍留在 `active/` 且为未跟踪。该问题已在 task §1 背景中记录，P0 不处理 bulk 迁移，留待后续治理子 task。
- **薄指针行数**：10 行，满足 ≤15 行要求。

---

## 5. 结论

`governance-tasks-done-hygiene` 文档索引治理满足验收标准前 6 项，无阻塞项。建议进入 PR 流程，并在 PR body 中注明：

- 文档-only，无 `api/` 行为变更；
- pytest 无回归；
- 50 复检报告路径：[`docs/tasks/reinspect_results/reinspect_governance_tasks_done_index_hygiene_20260613_v1.md`](./reinspect_governance_tasks_done_index_hygiene_20260613_v1.md)。

---

## 给 Cursor

`governance-tasks-done-hygiene`、reinspect、pass、文档-only、Hub、薄指针、跨仓链接
