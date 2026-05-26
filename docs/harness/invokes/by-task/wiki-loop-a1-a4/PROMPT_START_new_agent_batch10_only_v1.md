# 新 Agent 入口 · 仅生成 5 份 task 初稿（Batch-10 · 勿执行 Loop）

> **你的唯一任务**：运行 **Batch-10**，落盘 **5 个** `docs/tasks/active/task_*.md` + 1 个 invoke 快照，然后 **commit 并停**。  
> **禁止**：执行 A1 的 22、改 `docs/coding_wiki/` 正文、开 PR、跑 pytest。  
> **分支（硬）**：`task/wiki-loop-a1-a4-v1` · Open Folder **`ai-ink-brain-api-python/`**

| 项 | 值 |
|----|-----|
| **母 task** | `docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md` |
| **子 task ×4** | A1 ingest · A2 schema · A3 spec/对比表 · A4 排期 |
| **真值 Prompt** | 下文 §2 全文 = [`PROMPT_BATCH_10_four_tasks_v1.md`](./PROMPT_BATCH_10_four_tasks_v1.md) §3 |
| **验收人** | 用户将另开 Agent 做初稿验收；你只需交付文件 + 状态栏 |

**人工闸**：母 task 内 `HG-LOOP-BATCH` 保持 **`pending`**（勿代填 approved）。

**完成后输出**：5 个文件路径列表 + commit 短哈希 +「下一棒：人批 HG-LOOP-BATCH → `PROMPT_LOOP_22_to_CLOSE` round=A1」。

---

## 1. 执行前自检

```bash
git branch --show-current   # 须 task/wiki-loop-a1-a4-v1
test ! -f docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md || echo "若已存在则更新而非重复新建"
```

---

## 2. 可复制 Prompt（全文复制到**新对话**）

将 [`PROMPT_BATCH_10_four_tasks_v1.md`](./PROMPT_BATCH_10_four_tasks_v1.md) 中 **「## 3. 可复制 Prompt 正文」** 下 **整个** ` ```text ` 代码块原样粘贴为 **第一条 user 消息**。

若该文件 §3 与下框不一致，**以文件为准**；下框为便携副本（2026-05-26）。

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

## 3. 给验收 Agent 的指针（你不用做）

| 检查 | 路径 |
|------|------|
| 母闸 pending | `task_harness_wiki_loop_a1_a4_v1.md` |
| A2 占位 | `<!-- PLACEHOLDER:A1_OUTCOME -->` |
| Loop 入口 | `PROMPT_LOOP_22_to_CLOSE_v1.md` + `LOOP_MANIFEST.md` |
