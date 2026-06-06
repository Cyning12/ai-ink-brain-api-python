# PROMPT · Claude T0 · gov-docs-noise P1（写 task 单）

> **Round**：T0  
> **MANIFEST**：[`task_governance_docs_noise_line_manifest_v1.md`](../../tasks/active/task_governance_docs_noise_line_manifest_v1.md)  
> **git_branch**：`task/gov-docs-noise-p1-v1`  
> **slug**：`gov-docs-noise-p1`  
> **交付 task**：`docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md`（本 Round 创建）

---

## 0. 开跑前

| 项 | 说明 |
| --- | --- |
| **档期** | 读 RECENT §1.2 + MANIFEST · 确认 P1 为当前棒 |
| **gate** | T0 **不**执行 30；产出 task 后 gate 为 `pending` → **人签** 再开 T2b |

---

## 1. §3 Lead 正文（可复制）

```text
你 = Harness Lead（Claude Code · Round T0 · 写 P1 task）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p1_zh.md（本文件）
- docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md
- docs/spec/governance/docs-noise-inventory/README.md
- docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §8.2
- docs/tasks/done/task_gov_docs_noise_p0_readme_v1.md（字段样例）

开跑 SCHEDULE_SCAN：RECENT §1.2 → MANIFEST 确认 P1/T0。

Round T0 帽链（二选一，推荐 B）：
  A. Lead 直接写 task
  B. spawn harness-10-requirements → 落盘 task → Lead 复核

交付：
- 新建 docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md
- invoke：docs/harness/invokes/by-task/gov-docs-noise-p1/invoke_*_T0_*.md
- commit 脚手架

task 必含：
- Harness 元信息（orchestration: Claude Code · git_branch · test_strategy: not_applicable + note）
- failure_paths 表含 F# + Scenario ID（见 P0 CI 教训）
- merge_policy: docs_only_ci_green_merge · close_action: merge
- human_gate: HG-TASK-DRAFT / HG-GOV-P1-EXEC（status: pending）
- 验收：P1-1 delivery archived · P1-2 flows/README
- 链 MANIFEST + T2b PROMPT 路径

禁止：代签 gate · 改 P1 范围外文件 · 执行 SPEC §8.2 实现（留 T2b）

完成后：向人报告须签 gate_id + 路径；给出 T2b 下一棒指针（不 spawn T2b）
```

---

## 2. §3 harness-10-requirements spawn 正文

```text
【角色】Harness 10 需求帽 · 仅写 P1 task 草案 · 禁止改 delivery/flows 正文

【canonical 读序】
1. docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md（边界）
2. docs/spec/governance/docs-noise-inventory/README.md
3. SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §8.2
4. docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md
5. docs/tasks/done/task_gov_docs_noise_p0_readme_v1.md

【forbidden】
docs/diary/** glob · docs/harness/invokes/** glob · api/** · tests/**
本 Round 禁止打开 docs/delivery/** docs/flows/** 全文（task 仅引用路径）

【交付物】
docs/tasks/active/task_gov_docs_noise_p1_archived_v1.md

【必须字段】
task_slug: gov_docs_noise_p1_archived_v1
git_branch: task/gov-docs-noise-p1-v1
orchestration: Claude Code
audit_profile: post_close
kpi_rubric: KPI_RUBRIC_v1_2
merge_policy / close_action / failure_paths(F#+Scenario ID) / human_gate 表

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 3. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T0 实例 · Claude 写 P1 task |
