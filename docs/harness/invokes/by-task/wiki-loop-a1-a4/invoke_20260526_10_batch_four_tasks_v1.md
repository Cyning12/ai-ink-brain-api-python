# Invoke · 10 帽 Batch · Wiki Loop A1–A4 五份 task 初稿（v1）

| 字段 | 值 |
|------|-----|
| **hat_id** | 10 · 需求与任务分析（Batch 模式） |
| **task_slug** | `wiki-loop-a1-a4` |
| **freeze_id** | `WIKI-LOOP-A1-A4@2026-05-26` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **audit_profile** | `post_close` |
| **semi_auto** | true（本 invoke 仅起草；**不**链 22/30） |
| **human_gate** | `HG-LOOP-BATCH` **pending**（仅母 task） |
| **date** | 2026-05-26 |

---

## 1. 交付物

| # | 路径 |
|---|------|
| 0 | `docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md` |
| 1 | `docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md` |
| 2 | `docs/tasks/active/task_coding_wiki_schema_test_strategy_rule_v1.md` |
| 3 | `docs/tasks/active/task_governance_wiki_spec_comparison_sync_v1.md` |
| 4 | `docs/tasks/active/task_governance_recent_schedule_wiki_sync_v1.md` |

**Prompt 真值**：[`PROMPT_BATCH_10_four_tasks_v1.md`](./PROMPT_BATCH_10_four_tasks_v1.md) · [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md)

---

## 2. §3 调用体快照（user 消息全文）

```text
你正在扮演 Harness「需求与任务分析帽（10）· Batch 模式」，严格遵循：
- docs/harness/prompts/hats/10-requirements.md
- docs/tasks/templates/TASK_TEMPLATE.md
- docs/tasks/skills/SKILL-docs-governance.md
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、07-git-workflow.mdc

【背景】Wiki Multi slug 部分外推 · synthesis 缺 test_strategy · 单 PR loop 试点。
本批只生成 5 份 task 初稿；执行阶段不再开 10。

【开帽】落盘 invoke：docs/harness/invokes/by-task/wiki-loop-a1-a4/invoke_YYYYMMDD_10_batch_four_tasks_v1.md

【须落盘 5 文件】
0. docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md（HG-LOOP-BATCH pending；子单顺序 A1→A4→母关账）
1. docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md（A1 · synthesis test_strategy · freeze CODING-WIKI-A1-TEST-STRATEGY@2026-05-26）
2. docs/tasks/active/task_coding_wiki_schema_test_strategy_rule_v1.md（A2 · CODING_WIKI §8 · 含 PLACEHOLDER:A1_OUTCOME）
3. docs/tasks/active/task_governance_wiki_spec_comparison_sync_v1.md（A3 · SPEC §2 + 对比表）
4. docs/tasks/active/task_governance_recent_schedule_wiki_sync_v1.md（A4 · RECENT §1/§6.6）

每份含：Harness 元信息、范围/非范围、验收 - [ ]、failure_paths、帽子顺序（跳过10·链 PROMPT_LOOP+MANIFEST）、自检结论空表。

【commit】五 task + invoke · message 含 WIKI-LOOP-A1-A4@2026-05-26

【停】勿执行 22/30。末尾 📋 Harness 状态栏。
```

---

## 3. 10 帽结论摘要

| 项 | 结论 |
|----|------|
| SDD | 不涉及新 SPEC |
| 子 task 顺序 | A1 → A2 → A3 → A4 → 母 META 关账 |
| 下一棒 | 人批 `HG-LOOP-BATCH` → [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) · `LOOP_MANIFEST` **round=A1** |
| 禁止 | 本 invoke 会话内执行 22/30 或改 `docs/coding_wiki/` 正文 |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-26 | Batch-10 落盘五 task + 本 invoke |
