# PROMPT · Claude T0 · gov-docs-noise P2（改稿确认 / task 复核）

> **Round**：T0  
> **MANIFEST**：[task_governance_docs_noise_line_manifest_v1.md](../../tasks/active/task_governance_docs_noise_line_manifest_v1.md)  
> **git_branch**：`task/gov-docs-noise-p2-v1`  
> **slug**：`gov-docs-noise-p2`  
> **task**：[docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md](../../tasks/active/task_gov_docs_noise_p2_readorder_v1.md)（已存在；本 Round 复核/改稿）

---

## 0. 开跑前

| 项 | 说明 |
| --- | --- |
| **档期** | 读 RECENT §1.2 + MANIFEST · 确认 P2 为当前棒 |
| **gate** | T0 **不**执行 30；task 改稿后 gate 仍为 `pending` → **人签** 再开 T2c |

---

## 1. §3 Lead 正文（可复制）

```text
你 = Harness Lead（Claude Code · Round T0 · P2 task 复核/改稿）。遵循：
- docs/harness/prompts/PROMPT_claude_chain_serial_v1.md
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md（本文件）
- docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md
- docs/spec/governance/docs-noise-inventory/README.md
- docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §8.3
- docs/harness/prompts/PROMPT_claude_P2_pre_exec_amendments_zh.md（R1 改稿真值）

开跑 SCHEDULE_SCAN：RECENT §1.2 → MANIFEST 确认 P2/T0。

Round T0 帽链：
  A. Lead 直接改稿/复核
  B. spawn harness-10-requirements → 复核 task → Lead 确认

交付：
- task 改稿后须 `python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md` → OK
- 新建 T0/T2c PROMPT 实例（若尚未创建）
- 更新 MANIFEST + docs-noise-inventory README §6
- invoke：docs/harness/invokes/by-task/gov-docs-noise-p2/invoke_*_T0_*.md
- commit 脚手架

task 必含（复核）：
- Harness 元信息（orchestration: Claude Code · git_branch · test_strategy: not_applicable + note）
- failure_paths 表含 F# + Scenario ID
- merge_policy: docs_only_ci_green_merge · close_action: merge
- human_gate: HG-TASK-DRAFT / HG-GOV-P2-EXEC（status: pending）
- 验收：P2-1 PROJECT_CONFIG · P2-2 AGENTS↔docs/README 互链子集 · P2-3 根 README pointer · P2-4 legacy 消化 + C4/C5 寄存器更新
- 链 MANIFEST + T2c PROMPT 路径

禁止：代签 gate · 改 P2 范围外文件 · 执行 SPEC §8.3 实现（留 T2c）

完成后：向人报告须签 gate_id + 路径；给出 T2c 下一棒指针（不 spawn T2c）
```

---

## 2. §3 harness-10-requirements spawn 正文（若用 B）

```text
【角色】Harness 10 需求帽 · P2 task 复核/改稿 · 禁止改业务交付文件

【canonical 读序】
1. docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md
2. docs/harness/prompts/PROMPT_claude_P2_pre_exec_amendments_zh.md
3. docs/spec/governance/docs-noise-inventory/SPEC-Governance-Docs-Noise-Inventory-v1_zh.md §8.3
4. docs/tasks/active/task_governance_docs_noise_line_manifest_v1.md

【forbidden】
docs/diary/** glob · docs/harness/invokes/** glob · api/** · tests/**
本 Round 禁止打开 PROJECT_CONFIG/AGENTS/README 全文（task 仅引用路径）

【交付物】
- docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md（改稿后）
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T0_gov-docs-noise-p2_zh.md（本文件已存在则复核）
- docs/harness/prompts/PROMPT_claude_chain_serial_v1_T2c_gov-docs-noise-p2_zh.md

【必须】
- 改稿后 `python tools/harness_task_validate.py docs/tasks/active/task_gov_docs_noise_p2_readorder_v1.md` → OK
- 不执行 P2-1~P2-4 实现

【回报】Status / Deliverables / Blockers / Judgment（各≤10行）
```

---

## 3. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-06 | T0 实例 · P2 task 改稿确认 + PROMPT 脚手架 |
