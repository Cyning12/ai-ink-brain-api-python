# docs/harness/invokes（新快照落盘）

> **用途**：本仓 `docs/tasks/` 任务在 **每顶帽子新开局** 时，将已替换占位符的 `TEMPLATE-*` **§3 全文** 存一份于此。  
> **历史快照**（2026-05 图谱/闸口等 ~50 份）已迁至 [`../../diary/harness-archive/invokes/`](../../diary/harness-archive/invokes/)，**非必读**。

---

## 命名

`invoke_YYYYMMDD_<帽号>_<slug>.md`（例：`invoke_20260525_30_chatbi-v3-p2-1a-health.md`）

## 目录 taxonomy（规划 · 与 [`../README.md`](../README.md) §2.1 一致）

| 阶段 | 路径 |
|------|------|
| **现状** | 扁平在 `invokes/` 根下 |
| **目标** | `invokes/by-task/<task_slug>/invoke_*.md`（`<task_slug>` 与 task 文件名主干一致，如 `chatbi-v3-p2-1a-health`） |

**规则**：新 invoke **建议**直接落 `by-task/`；历史根目录文件迁移前仍有效。按 **task** 归类，**不**按 `chatbi` / `tech-graph` 域分目录。

## 规则（摘要）

1. **同一帽**多轮追问 **不** 重复落盘；换帽才新建文件。  
2. 与 task 同 **`git_branch`** 提交；并行任务用独立 worktree（见 [`../README.md`](../README.md) §3）。  
3. 审查结论：用 **`docs/tasks/review_results/`**（20 帽）或 task 正文，**不**使用已移除的 `harness/reviews/`。

## 模板来源

[`../prompts/README.md`](../prompts/README.md)
