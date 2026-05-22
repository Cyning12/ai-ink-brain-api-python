# docs/harness（本后端仓 · 22 + 50 + 执行链）

> **目标**：日常只读本目录 + `docs/tasks/`；含 **三方 Agent（50 帽）** 可查收落盘。  
> **历史**：22/reviews、旧 invoke 见 [`../diary/harness-archive/`](../diary/harness-archive/README.md)。

---

## 1. 日常读什么

| 场景 | 路径 |
|------|------|
| 写 task / **下一棒双 Prompt** | `TEMPLATE-requirements`（**A:22** + **B:30**，人择一） |
| 任务审核 22 | [`reviews/README.md`](reviews/README.md) → `TEMPLATE-task-audit` |
| 执行 + 自检 | `TEMPLATE-execute` → `TEMPLATE-self-check` |
| **三方复检** | `TEMPLATE-independent-reinspect` → [`../tasks/reinspect_results/`](../tasks/reinspect_results/README.md) |
| 半自动 / 人工闸 | `HANDOFF_SEMI_AUTO` |
| commit / 关账 | `HANDOFF_AUTO_COMMIT`、`HANDOFF_CLOSE_TRACE` |
| task 字段 | `HARNESS_V2_PLAN.md` §5 |
| 流程 | `SDD_HAT_FLOW.md` |
| 新 invoke | `invokes/` |
| **Harness 裁决共识（已接受）** | [`../diary/2026-05-22-harness-evaluation-improvement-response.md`](../diary/2026-05-22-harness-evaluation-improvement-response.md) **§九** |

**Cursor**：`.cursor/rules/05-harness-semi-auto.mdc`、`.cursor/rules/06-harness-in-repo.mdc`。

---

## 2. 目录结构

```text
docs/harness/
  README.md
  ACCEPTANCE_LANDING.md     # 人类可读落盘 + 50 硬规则
  HARNESS_V2_PLAN.md
  SDD_HAT_FLOW.md
  prompts/                  # 10/20/22/30/40/50 + TEMPLATE + HANDOFF_*
  reviews/README.md         # 22 帽 · 仅本仓 task
  invokes/README.md
```

---

## 3. 关账最低要求（摘要）

1. （若人择 **路径 A**）`docs/harness/reviews/task_*_audit_*.md`（22）无阻塞  
2. task **`### 自检结论（执行者）`**（40）  
3. **`docs/tasks/reinspect_results/reinspect_*.md`**（50）  
4. **`human_gate`** → `approved`（人改）  
5. CI 绿

---

## 4. 上游同步（维护者）

```bash
rsync -a ../docs/harness/prompts/50-independent-reinspect.md docs/harness/prompts/
rsync -a ../docs/harness/prompts/TEMPLATE-independent-reinspect-invoke.md docs/harness/prompts/
# 合并后保留本仓 ACCEPTANCE_LANDING、ACCEPTANCE 落盘约定，勿覆盖删 50
```

---

## 5. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v2 最小集 |
| 2026-05-22 | v3：**恢复 50** + `ACCEPTANCE_LANDING` + `reinspect_results` 关账 |
| 2026-05-22 | v4：链 diary **§九 生效共识**；`reviews/` 历史样例召回见 `reviews/README.md` |
