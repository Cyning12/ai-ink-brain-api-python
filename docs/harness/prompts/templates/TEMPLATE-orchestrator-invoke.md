# 总调度（00）· 对话调用模板

> **用途**：本仓 **链式常模**入口；Lead 按 [`PROMPT_claude_chain_serial_v1.md`](../PROMPT_claude_chain_serial_v1.md) 或 Cursor 等价 [`PROMPT_cursor_task_chain_serial_v1.md`](../../../../docs/harness/prompts/PROMPT_cursor_task_chain_serial_v1.md) spawn / Task。  
> **真值**：[`SPEC-Governance-Harness-Chain-Orchestration-v1.md`](../../../spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md)、[`../guides/KPI_RUBRIC_v1_2.md`](../../guides/KPI_RUBRIC_v1_2.md)（若有）。

---

## 1. 占位符

| 占位符 | 含义 |
|--------|------|
| `{{TASK_PATH}}` | 主 task（相对本仓根） |
| `{{TASK_SLUG}}` | invoke 目录 slug |
| `{{PLANNED_HATS}}` | 如 `22,30,40,50,CLOSE` |
| `{{GIT_BRANCH}}` | `task/<slug>` |
| `{{CHAIN_PROMPT}}` | 如 `docs/harness/prompts/PROMPT_claude_chain_serial_v1_T1_*.md` |
| `{{RESUME_INVOKE}}` | 续跑 invoke；全新=`无` |

---

## 2. 可复制 Prompt 正文（§3）

```text
你 = Harness Lead（链式串行 · 00 职责）。严格遵循：
- {{CHAIN_PROMPT}}（实例 · 占位符已替换）
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md（或 task 指定的 chain 模板）
- docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/HARNESS_V2_PLAN.md §5.6（orchestration；semi_auto deprecated）

输入：
- task：{{TASK_PATH}}
- slug：{{TASK_SLUG}}
- planned_hats：{{PLANNED_HATS}}
- git_branch：{{GIT_BRANCH}}
- 续跑 invoke：{{RESUME_INVOKE}}

你必须完成：
1. GATE_SCAN：读 human_gate + orchestration；pending → 只报 gate_id。
2. 每帽：invoke → Lead commit → spawn/Task → 收 ≤10 行（Git 仅 Lead）。
3. 关账：HANDOFF_CLOSE_TRACE + task README 归档。

禁止：代签 approved；subagent commit；main 链式提交；semi_auto: true 作总闸。
```

---

## 3. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-31 | v1：KPI v1.2 同批 |
| 2026-06-08 | v2：链式常模；绑 PROMPT_*_chain_serial_*；移除 semi_auto |
