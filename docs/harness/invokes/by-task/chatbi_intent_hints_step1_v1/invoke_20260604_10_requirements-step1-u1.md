# Invoke · 10 需求帽 · chatbi_intent_hints_step1_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 10 |
| **round** | R0（Epic U1 首派） |
| **task_slug** | `chatbi_intent_hints_step1_v1` |
| **git_branch** | `task/chatbi-intent-hints-step1-v1`（实现分支 · 10 落 task 后 30 开干前须 checkout） |
| **Open Folder** | `ai-ink-brain-api-python` |
| **dispatched_by** | 00 orchestrator · Epic `chatbi-intent-hints-epic` |
| **semi_auto** | true（10 完成后停 — 待 HG-TASK-DRAFT + 人择 A/B） |
| **Epic 单元** | U1 · Step 1 C-lite |

## §3 快照（10 开帽 Prompt 全文 · 可复制）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- ai-ink-brain-api-python/docs/harness/prompts/hats/10-requirements.md
- ai-ink-brain-api-python/docs/harness/HARNESS_V2_PLAN.md §5
- ai-ink-brain-api-python/docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md

输入（占位符已全部替换）：

【目标与上下文】
Epic「ChatBI Intent Hints」之 **U1 · Step 1（C-lite）**：在 docs/tasks/active/ 新建 task_chatbi_intent_hints_step1_v1.md，使 30 帽可据 SPEC 实现 intent_hints.yaml + loader + Prompt 注入，修复 Portfolio Q4 / 人名类 Intent 误路由。6/9 硬门槛。实现分支 task/chatbi-intent-hints-step1-v1（从 origin/main 拉）。

【已有材料路径或粘贴说明】
docs/spec/intent-hints/README.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Analysis-v1_zh.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md
docs/spec/governance/SPEC-Governance-Portfolio-RAG-Demo-v1_zh.md
docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md
api/text2sql_value_hints.py（参照 loader 模式）
docs/tasks/active/task_chatbi_v3_intent_classification_debt_v1.md（回链 · backlog）

【是否按任务审核文档回填】
无

【SDD 三轮状态】
轮0+1+2 已完成，清单有待确认项

【是否新建或重大修订 SPEC】
否

你必须完成：
0. **Invoke 快照（开帽起点）**：本消息即为 invoke 快照（已由 00 落盘 invoke_20260604_10_requirements-step1-u1.md）。
1. **SDD 纪律（硬）**：
   - NEW_OR_MAJOR_SPEC = 否：不新建 L1 SPEC。
   - SDD 状态含「清单有待确认项」：下一棒 **只许推荐路径 A**，**禁止** 推荐路径 B。
   - task 须显式处理 Overview §7 Q-1～Q-4（采纳 00 建议默认或写 defer 理由）。
2. 输出结构化块：背景 / 范围 / 非范围 / 依赖链接 / 验收列表 / failure_paths / 给执行帽的必读列表。
3. test_strategy: required；audit_profile: post_close；experience_capture: required。
4. 禁止：写业务实现代码；改 CI；api/graph/*；夹带 Step2/3 范围。
5. **写入 task 文件**：docs/tasks/active/task_chatbi_intent_hints_step1_v1.md（完整 Harness 元信息表 + human_gate HG-TASK-DRAFT pending）。
6. 对话回复 — **下一棒须输出两条 Prompt（由人择一）**：
   - 推荐判定：仅推荐 **路径 A（22 R1）**（清单有待确认项 + test_strategy required + 涉 api/）。
   - 路径 A · 22 任务审核 R1（推荐）：TEMPLATE-task-audit-invoke §3 全文，task_path=docs/tasks/active/task_chatbi_intent_hints_step1_v1.md，review 落盘 docs/harness/reviews/task_chatbi_intent_hints_step1_v1_audit_R1_20260604.md
   - 路径 B · 30 执行（跳过 22）：TEMPLATE-execute-invoke §3 全文（**不推荐**；须标注人承担闸 1）。
7. 回复末尾输出 HANDOFF_SEMI_AUTO §3.4 📋 Harness 状态栏（版本 B）。

Judgment（10）：
- spec_absorb: Q-1～Q-4 是否在 task 中 resolved/deferred
- hat_self: pass | pass-with-notes | blocked
```
