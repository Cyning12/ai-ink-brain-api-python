# docs/harness/prompts（10 / 20 / 22 / 30 / 40 / 50）

> **落盘**：[`../ACCEPTANCE_LANDING.md`](../ACCEPTANCE_LANDING.md) · **流程**：[`../SDD_HAT_FLOW.md`](../SDD_HAT_FLOW.md)

---

## 使用方式

1. **10 结束**：必须输出 **下一棒 A（22）** + **下一棒 B（30）** 两条 §3 Prompt，**人**择一。  
2. **22**：审查写入 **`docs/harness/reviews/`**（仅本仓 `docs/tasks/`，见 [`../reviews/README.md`](../reviews/README.md)）。  
3. **30→40→50**：50 须先落盘 `docs/tasks/reinspect_results/`。  
4. **半自动**：[`HANDOFF_SEMI_AUTO.md`](HANDOFF_SEMI_AUTO.md)。

---

## 文件列表

| 帽 | 文件 |
|----|------|
| 10 | `10-requirements.md`、`TEMPLATE-requirements-invoke.md` |
| 20 | `20-review-spec-task.md`、`TEMPLATE-review-spec-task-invoke.md` |
| **22** | **`22-task-audit.md`**、**`TEMPLATE-task-audit-invoke.md`** |
| 30 | `30-execute-code.md`、`TEMPLATE-execute-invoke.md` |
| 40 | `40-self-check.md`、`TEMPLATE-self-check-invoke.md` |
| 50 | `50-independent-reinspect.md`、`TEMPLATE-independent-reinspect-invoke.md`（+ 可选 full） |
| — | `HANDOFF_*` ×3 |

**工作区混放审查**（非本后端 task）：**不要**写入本仓 `docs/harness/reviews/`；见 archive。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-22 | v4：22 回本仓 reviews；10 双路径 |
