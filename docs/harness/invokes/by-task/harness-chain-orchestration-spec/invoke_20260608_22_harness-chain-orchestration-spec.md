# Invoke · 22 R1 · harness-chain-orchestration-spec

> **日期**：2026-06-08
> **帽**：22
> **task**：[task_harness_chain_orchestration_spec_v1.md](../../../tasks/active/task_harness_chain_orchestration_spec_v1.md)
> **Round**：T1 · R1
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

## 2. 前置输入

- **explore 报告**：`docs/harness/invokes/by-task/harness-chain-orchestration-spec/invoke_20260608_explore_harness-chain-orchestration-spec.md`
- **gap 摘要**：A-2/A-4/A-5 已就绪；A-1/A-3/A-6/A-7 为 30 必须修改项

---

## 3. 落盘 Prompt（§3 22 帽）

```text
【角色】Harness 22 · R1 审查

【读序】task · explore 报告 · SPEC 草案 · MANIFEST

【审查】A-1～A-7 范围 · failure_paths F1–F3 · orchestration/semi_auto 关系是否清晰
【禁止】改 api/ · 代签 gate
【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 4. 下一棒

30 → `harness-30-docs`（A-1/A-3/A-6/A-7 执行 + A-1 定稿）
