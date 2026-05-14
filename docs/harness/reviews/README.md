# docs/harness/reviews（本后端仓 · 任务审核产出）

> **用途**：存放 **任务审核帽**（工作区 [`docs/harness/prompts/22-task-audit.md`](../../../../docs/harness/prompts/22-task-audit.md)）对本仓 **`docs/tasks/`** 相关 task 的**书面审查结果**（每轮必产出）。  
> **真值**：与本仓 `docs/tasks/active|done` 强绑定的 task，其 **签收 / 关闭** 以 **本目录** 下对应 `task_*_audit_*.md` 为准，并与 task 头部 `状态` 一致；**不得以聊天结论替代落盘**。  
> **工作区索引**：[`docs/harness/reviews/README.md`](../../../../docs/harness/reviews/README.md)（多子仓总说明；后端 task 全文以 **本目录** 为归档真值）。  
> **Invoke 快照**（新帽节 §3 正文锚点）：[`../invokes/README.md`](../invokes/README.md)（与本仓 `docs/tasks` 强绑定时，快照归 **本目录旁 `invokes/`**；总规见工作区链入文件）。

---

## 命名建议

与工作区一致：

| 场景 | 建议文件名 |
|------|------------|
| 首轮审查 | `task_<slug>_audit_R1_YYYYMMDD.md` |
| 复审 | 递增 `R2`、`R3`…；文首「元信息」链回上一轮文件 |

路径均相对 **本仓库根**：`docs/harness/reviews/<文件名>.md`。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-14 | v1：后端仓独立落盘任务审核；与根 `docs/harness/reviews` 分工 |
| 2026-05-14 | v1.1：链 **Invoke 快照** [`../invokes/README.md`](../invokes/README.md) |

---

## 给 Cursor

`Harness`、`reviews`、`任务审核`、`audit`、`R1`、`签收`、`闭环`、`docs/tasks`
