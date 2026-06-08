# Task · MANIFEST · semi_auto 退场 · 链式编排双轨（A+B）

> **状态**：`draft`  
> **Epic**：Harness 链式常模 · **全面废弃 `semi_auto`**（须 A+B 齐 CLOSE）  
> **规划 diary**：[`docs/diary/2026-06-08-harness-chain-next-task-planning_zh.md`](../diary/2026-06-08-harness-chain-next-task-planning_zh.md) §7  
> **P0 取向**：[`docs/diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md`](../diary/2026-06-06-gov-docs-noise-p0-task-chain-pilot_zh.md) §5「Task 链 = 改代码主力 · semi_auto 计划废弃」  
> **freeze_id**：`GOV-HARNESS-CHAIN-SEMI-AUTO-RETIRE@2026-06-08`

---

## Harness 元信息

| 字段 | 值 |
| --- | --- |
| **task_slug** | `harness_semi_auto_retirement_manifest_v1` |
| **orchestration** | **MANIFEST 仅** — 子批各自 Lead + `PROMPT_*_chain_serial_*` |
| **test_strategy** | `not_applicable`（母单无实现） |
| **git_branch** | `—`（子批各自分支） |

---

## 双轨与硬门禁

| 轨 | ID | task | 分支建议 | 执行器 | 证明 |
| --- | --- | --- | --- | --- | --- |
| **A · 治理** | G1 | [`task_harness_chain_orchestration_spec_v1.md`](task_harness_chain_orchestration_spec_v1.md) | `task/harness-chain-orchestration-spec-v1` | CC / Cursor | SPEC + TASK_TEMPLATE · `semi_auto` 过渡/废弃 |
| **B · api** | G2 | [`task_chatbi_intent_llm_retry_u1_5_v1.md`](task_chatbi_intent_llm_retry_u1_5_v1.md) | `task/chatbi-intent-llm-retry-u1.5-chain-v1` | **CC 首棒** | required + **50** · 链式关账 |

**对外宣称「semi_auto 全面废弃」**：G1 + G2 **均 done** 后。

---

## 已完成链式试点（非本 Epic 交付）

| 执行器 | 参考 |
| --- | --- |
| Cursor | docs-noise P0 · #121 |
| Claude Code | docs-noise P1–P3 · #123–#129 |
| Kimi Code | recentsync · #134 |

---

## Prompt 真值索引

| 子批 | PROMPT 实例 |
| --- | --- |
| A | [`PROMPT_claude_chain_serial_v1_T1_harness-chain-orchestration-spec_zh.md`](../harness/prompts/PROMPT_claude_chain_serial_v1_T1_harness-chain-orchestration-spec_zh.md) |
| B | [`PROMPT_claude_chain_serial_v1_T1_intent-retry-u1_5_zh.md`](../harness/prompts/PROMPT_claude_chain_serial_v1_T1_intent-retry-u1_5_zh.md) |

**通用**：[`PROMPT_claude_chain_serial_v1.md`](../harness/prompts/PROMPT_claude_chain_serial_v1.md) · [`COMPARISON_kimi_claude_chain_prompt_v1_zh.md`](../harness/prompts/COMPARISON_kimi_claude_chain_prompt_v1_zh.md)

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-08 | 初稿 · A+B 双轨 MANIFEST |
