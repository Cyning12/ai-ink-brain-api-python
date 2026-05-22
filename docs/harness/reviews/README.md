# docs/harness/reviews（本后端仓 · 22 帽任务审核）

> **用途**：**仅**存放对本仓 **`docs/tasks/`** 绑定 task 的 **22 帽** 书面审查（`task_*_audit_R*_*.md`）。  
> **禁止**：把工作区总 Agent、前端仓或其他子项目的审查全文放在本目录（历史混放是删除旧 `reviews/` 的原因）。

---

## 落盘规则（硬）

| 项 | 约定 |
|----|------|
| **路径** | 本仓根相对：`docs/harness/reviews/<文件名>.md` |
| **命名** | `task_<slug>_audit_R<轮次>_YYYYMMDD.md`（例：`task_foo_v1_audit_R1_20260522.md`） |
| **绑定** | 元信息表须含 **`task_path`** → `docs/tasks/active|done/...` |
| **签收** | 终轮须有 **「签收 / 关闭」** 节，与 task 头部 `状态` 对齐 |

跨仓审查、工作区 Harness 任务：**不得**写入本目录；若需备忘，用工作区 `Projects/docs/harness/reviews/` 的 **pointer**（本仓不维护）。

---

## 与 20 / 50 分工

| 帽 | 目录 | 层级 |
|----|------|------|
| **20** | `docs/tasks/review_results/` | SPEC/task **短评**，可选 |
| **22** | **本目录** | task **合同**是否可执行（R1/R2…） |
| **50** | `docs/tasks/reinspect_results/` | 实现 vs 验收（三方，关账） |

---

## 人工择路（10 帽交接）

10 帽结束须给出 **两条** 下一棒 Prompt（见 [`../prompts/TEMPLATE-requirements-invoke.md`](../prompts/TEMPLATE-requirements-invoke.md) §3）：

- **路径 A**：`TEMPLATE-task-audit-invoke` → 本目录落盘 R1  
- **路径 B**：`TEMPLATE-execute-invoke` → 直进 30（**人**判定可跳过 22 时选用）

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v1：本仓专用 reviews；与工作区混放脱钩 |
