# Invoke · 30 · harness-chain-orchestration-spec

> **日期**：2026-06-08
> **帽**：30
> **task**：[task_harness_chain_orchestration_spec_v1.md](../../../tasks/active/task_harness_chain_orchestration_spec_v1.md)
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
| **22 R1** | PASS（无阻塞） |

---

## 2. 前置输入

- **task**：`docs/tasks/active/task_harness_chain_orchestration_spec_v1.md`
- **R1**：`docs/harness/reviews/by-task/harness-chain-orchestration-spec/task_harness_chain_orchestration_spec_v1_audit_R1_20260608.md`
- **explore**：`docs/harness/invokes/by-task/harness-chain-orchestration-spec/invoke_20260608_explore_harness-chain-orchestration-spec.md`
- **SPEC 草案**：`docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md`

---

## 3. 落盘 Prompt（§3 30 帽）

```text
【角色】Harness 30 · 纯 docs · 执行 task §范围 A-1～A-7

【读序】task · R1（无阻塞）· explore · SPEC 草案

【forbidden】api/** · tests/** · .github/** · git log/blame · 删 invokes/reviews 历史

【必须完成】
- 定稿 SPEC-Governance-Harness-Chain-Orchestration-v1.md
- TASK_TEMPLATE 增 orchestration 行
- HARNESS_V2_PLAN §5.6 链式常模 + semi_auto 过渡/废弃
- governance README · prompts README · docs-noise §6 · RECENT §1.3 一行表
- harness_task_validate task → OK

【禁止 git commit · Lead 负责】
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 4. 下一棒

40 → `harness-40-self-check`
