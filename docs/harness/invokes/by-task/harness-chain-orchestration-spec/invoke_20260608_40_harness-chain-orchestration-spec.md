# Invoke · 40 · harness-chain-orchestration-spec

> **日期**：2026-06-08
> **帽**：40
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
| **30** | A-1~A-7 完成 |

---

## 2. 前置输入

- **task**：`docs/tasks/active/task_harness_chain_orchestration_spec_v1.md`
- **30 产出**：6 文件变更（SPEC / HARNESS_V2_PLAN / RECENT / docs-noise / governance README / prompts README）

---

## 3. 落盘 Prompt（§3 40 帽）

```text
【角色】Harness 40 · docs-only 自检

【验证】
- rg orchestration docs/tasks/templates/TASK_TEMPLATE.md
- test -f docs/spec/governance/SPEC-Governance-Harness-Chain-Orchestration-v1.md
- python tools/harness_task_validate.py docs/tasks/active/task_harness_chain_orchestration_spec_v1.md

【跳过】pytest · 50（not_applicable · task 明示）

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 4. 下一棒

CLOSE → PR → CI → merge（task 授权）
