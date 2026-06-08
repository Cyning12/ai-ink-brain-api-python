# Invoke · explore · harness-chain-orchestration-spec

> **日期**：2026-06-08
> **帽**：explore
> **task**：[`task_harness_chain_orchestration_spec_v1.md`](../../../tasks/active/task_harness_chain_orchestration_spec_v1.md)
> **Round**：T1
> **执行器**：Claude Code · Harness Lead

---

## 1. 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `harness-chain-orchestration-spec` |
| **git_branch** | `task/harness-chain-orchestration-next-v1` |
| **merge_policy** | `docs_only_ci_green_merge` |
| **test_strategy** | `not_applicable` |
| **human_gate** | HG-TASK-DRAFT approved · HG-CHAIN-A-EXEC approved |

---

## 2. 落盘 Prompt（§3 explore 帽）

```text
【角色】Harness explore · A 轨 · 只读差分

【canonical 读序】
1. docs/tasks/active/task_harness_chain_orchestration_spec_v1.md
2. docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md（草案）
3. docs/tasks/templates/TASK_TEMPLATE.md
4. docs/harness/HARNESS_V2_PLAN.md §5.6
5. docs/diary/2026-06-08-harness-chain-next-task-planning_zh.md §7

【forbidden】api/** · tests/** · .github/** · 改业务交付文件

【交付】A-1～A-7 缺口表 · TASK_TEMPLATE 是否缺 orchestration · §5.6 semi_auto 表述对照
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 3. 下一棒

22 R1 → `docs/harness/reviews/by-task/harness-chain-orchestration-spec/`
