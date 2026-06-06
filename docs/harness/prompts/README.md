# docs/harness/prompts（10 / 20 / 22 / 30 / 40 / 50）

> **落盘**：[`../ACCEPTANCE_LANDING.md`](../ACCEPTANCE_LANDING.md) · **流程**：[`../SDD_HAT_FLOW.md`](../SDD_HAT_FLOW.md)

---

## 使用方式

1. **10 结束**：必须输出 **下一棒 A（22）** + **下一棒 B（30）** 两条 §3 Prompt，**人**择一。  
2. **22**：审查写入 **`docs/harness/reviews/`**（仅本仓 `docs/tasks/`，见 [`../reviews/README.md`](../reviews/README.md)）。  
3. **30→40→50**：50 须先落盘 `docs/tasks/reinspect_results/`。  
4. **半自动**：[`handoff/HANDOFF_SEMI_AUTO.md`](handoff/HANDOFF_SEMI_AUTO.md)。

---

## 文件列表

| 帽 | 文件 |
|----|------|
| 10 | `hats/10-requirements.md`、`templates/TEMPLATE-requirements-invoke.md` |
| 20 | `hats/20-review-spec-task.md`、`templates/TEMPLATE-review-spec-task-invoke.md` |
| **22** | **`hats/22-task-audit.md`**、**`templates/TEMPLATE-task-audit-invoke.md`** |
| 30 | `hats/30-execute-code.md`、`templates/TEMPLATE-execute-invoke.md` |
| 40 | `hats/40-self-check.md`、`templates/TEMPLATE-self-check-invoke.md` |
| 50 | `hats/50-independent-reinspect.md`、`templates/TEMPLATE-independent-reinspect-invoke.md`（+ 可选 full） |
| — | `handoff/HANDOFF_*` ×3 |
| **00 · Task 链试点** | [`PROMPT_cursor_task_chain_serial_v1.md`](PROMPT_cursor_task_chain_serial_v1.md) · T1 实例 [`PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md`](PROMPT_cursor_task_chain_serial_v1_T1_gov-docs-noise-p0_zh.md) |
| **Lead · Claude spawn 链** | [`PROMPT_claude_chain_serial_v1.md`](PROMPT_claude_chain_serial_v1.md)（§5.1 30 约束 · **§5.2 Git 仅 Lead**）· T0/T2b/T2c 实例 · [`.claude/agents/`](../../.claude/agents/README.md) · [`.claude/settings.json`](../../.claude/settings.json) |
| **P2 · T0/T2c** | [`PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md`](PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md) · [`PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md`](PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md) |
| **P2 · R1 改稿 handoff** | [`PROMPT_claude_P2_pre_exec_amendments_zh.md`](PROMPT_claude_P2_pre_exec_amendments_zh.md) · 审核 [`reviews/by-task/gov-docs-noise-p2/`](../reviews/by-task/gov-docs-noise-p2/) |
| **P1 · post-close** | [`PROMPT_claude_post_close_P1_full_zh.md`](PROMPT_claude_post_close_P1_full_zh.md) · [`PROMPT_claude_post_close_P1_v2_zh.md`](PROMPT_claude_post_close_P1_v2_zh.md) |
| **T3 · 母单关账** | [`PROMPT_claude_T3_gov-docs-noise-line-close_zh.md`](PROMPT_claude_T3_gov-docs-noise-line-close_zh.md) |

**工作区混放审查**（非本后端 task）：**不要**写入本仓 `docs/harness/reviews/`；见 archive。

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-06 | v8：T3 docs-noise 母单关账 PROMPT |
| 2026-06-06 | v7：P2 R1 改稿 handoff + post-close PROMPT 索引 |
| 2026-06-06 | v6：Claude spawn 链 PROMPT + `.claude/agents/` 指针 |
| 2026-06-06 | v5：增 Cursor Task 链 PROMPT 模板 + T1 gov-docs-noise 实例 |
| 2026-05-22 | v4：22 回本仓 reviews；10 双路径 |
