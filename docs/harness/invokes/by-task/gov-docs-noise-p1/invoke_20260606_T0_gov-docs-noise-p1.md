# Invoke · T0 · gov-docs-noise-p1

> **Round**：T0
> **Hat**：Lead / harness-10-requirements
> **Branch**：`task/gov-docs-noise-p1-v1`
> **Date**：2026-06-06

---

## 输入

- MANIFEST：`docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md`
- P0 样例：`docs/tasks/done/task_gov_docs_noise_p0_readme_v1.md`
- SPEC §8.2：`docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md`
- T2b PROMPT：`docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`

## 产出

- **Task 新建**：`docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md`
  - task_slug: `gov_docs_noise_p1_archived_v1`
  - test_strategy: `not_applicable`（纯 docs）
  - merge_policy: `docs_only_ci_green_merge` / close_action: `merge`
  - human_gate: HG-TASK-DRAFT (pending) / HG-GOV-P1-EXEC (pending)
  - failure_paths: F1–F5（含 P0 CI 教训 F5）
  - 验收：P1-1 archived / P1-2 flows/README
  - 链 MANIFEST + T2b PROMPT 路径

## Gate 状态

| gate_id | status | blocks |
|---------|--------|--------|
| HG-TASK-DRAFT | **pending** | 22-R1, 30 |
| HG-GOV-P1-EXEC | **pending** | explore, 22, 30, 40, CLOSE |

## 下一棒

**T2b** 执行链（explore → 22 → 30 → 40 → CLOSE，跳过 50），见：
`docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2b_gov-docs-noise-p1_zh.md`

---
*Lead 复核通过 · 待人签 HG-TASK-DRAFT*
