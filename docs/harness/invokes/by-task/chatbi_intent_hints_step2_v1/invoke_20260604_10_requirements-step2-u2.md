# Invoke · 10 需求帽 · chatbi_intent_hints_step2_v1 · 2026-06-04

| 字段 | 值 |
| --- | --- |
| **hat_code** | 10 |
| **round** | R0（Epic U2 首派） |
| **task_slug** | `chatbi_intent_hints_step2_v1` |
| **git_branch** | `task/chatbi-intent-hints-step2-v1` |
| **Open Folder** | `ai-ink-brain-api-python` |
| **dispatched_by** | 人 · Step1/U1.5 merge 后开 U2 |
| **semi_auto** | true（10 完成后停 — 待 HG-TASK-DRAFT + 人择 A/B） |
| **Epic 单元** | U2 · Step 2 C-mid |

## §3 快照（10 开帽 Prompt 全文 · 可复制）

```text
你正在扮演工作区 Harness「需求与任务分析帽」，严格遵循：
- ai-ink-brain-api-python/docs/harness/prompts/hats/10-requirements.md
- ai-ink-brain-api-python/docs/harness/HARNESS_V2_PLAN.md §5
- ai-ink-brain-api-python/docs/spec/SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md

输入（占位符已全部替换）：

【目标与上下文】
Epic「ChatBI Intent Hints」之 **U2 · Step 2（C-mid）**：在 docs/tasks/active/ 新建 task_chatbi_intent_hints_step2_v1.md，使 30 帽可据 SPEC 实现 **同一份 intent_hints.yaml 驱动 V1 router 规则合并 + LLM/direct 可选仲裁**，补齐 Step1 **未覆盖**路径：Intent 超时→V1、LLM 高置信仍误判 direct、关 LLM 时 Portfolio 稳定度。

**前置已合 main**：Step1 #109（YAML + loader + Prompt 注入）· U1.5 #110（Intent LLM 重试 + 超时阶梯）。Step1 五问 **5/5 人验已通过**（不单独 reinspect 落盘）；RUNBOOK §4.1 **Q-INTENT** 已留：「聊聊你对刘新宁的看法，他在 AI coding 岗位有什么优势。」

实现分支：`task/chatbi-intent-hints-step2-v1`（开干前 `git fetch && git checkout -b task/chatbi-intent-hints-step2-v1 origin/main`）。6/9 投递 sprint **建议**合 main（非 Step1 硬门槛，但优先于 Step3）。

【已有材料路径或粘贴说明】
docs/spec/intent-hints/README.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Overview-v1_zh.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Analysis-v1_zh.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Schema-v1_zh.md（§4.5 arbitration · §4.3 rag_signals）
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step1-C-Lite-v1_zh.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step2-C-Mid-v1_zh.md
docs/spec/intent-hints/SPEC-ChatBI-Intent-Hints-Step3-C-Full-v1_zh.md（只读 · 非本 task 范围）
docs/tasks/done/task_chatbi_intent_hints_step1_v1.md（U1 关账 · Q-2 defer 至本 task）
docs/harness/guides/RUNBOOK_portfolio_rag_five_questions_v1_zh.md（§4 五问 + §4.1 Q-INTENT）
docs/chatbi/v1/intent_hints.yaml
api/intent_hints.py
api/intent_router.py
api/intent_agent.py
api/agent.py
tests/test_intent_hints_loader.py
tests/test_intent_router_backend_v1.py（若存在 · 扩展 Portfolio 用例）

【是否按任务审核文档回填】
无

【SDD 三轮状态】
轮0+1+2 已完成，清单有待确认项

【是否新建或重大修订 SPEC】
否

你必须完成：
0. **Invoke 快照（开帽起点）**：将本消息落盘 docs/harness/invokes/by-task/chatbi_intent_hints_step2_v1/invoke_20260604_10_requirements-step2-u2.md（元数据表 + §3 fenced code）。
1. **SDD 纪律（硬）**：
   - NEW_OR_MAJOR_SPEC = 否：不新建 L1 SPEC。
   - SDD 状态含「清单有待确认项」：下一棒 **只许推荐路径 A**，**禁止** 推荐路径 B。
   - task 须 **resolved** Overview §7 **Q-2**（Step2 仲裁默认开/关 · Step1 已 defer；建议默认 **仲裁开** + env `INTENT_HINTS_ARBITRATION` 可关）；Q-1/Q-3/Q-4 引用 Step1 决议勿重复争论。
2. 输出结构化块：背景 / 范围（S2-1～S2-6 对齐 Step2 SPEC §2.1）/ 非范围 / 依赖 / 验收标准 / failure_paths / 行为变更 Delta / 给执行帽必读列表。
3. test_strategy: required；test_strategy_note 须覆盖 router + 仲裁 mock 单测；audit_profile: post_close；experience_capture: required；freeze_id 沿用 `CHATBI-INTENT-HINTS@2026-06-09`；blocks: chatbi_intent_hints_step3_v1（若 Step3 仍独立）。
4. 验收须含（对齐 Step2 SPEC §5 + RUNBOOK）：
   - Step1 验收仍 pass（回归）
   - mock LLM 返回 direct + Q4 / Q-INTENT → 仲裁后 rag_search
   - CHATBI_V2_INTENT_LLM=false · Q4 → V1/启发式 rag
   - 负例「量子计算」不被误伤
   - pytest tests -m "not intent_eval and not intent_benchmark" 全绿
5. 禁止：api/graph/* · unified_chat_graph · Step3 全量 PROJECT_CONFIG · 批量改 60 条金标 · 写业务实现代码。
6. **写入 task 文件**：docs/tasks/active/task_chatbi_intent_hints_step2_v1.md（完整 Harness 元信息 + human_gate HG-TASK-DRAFT pending）。
7. 对话回复 — **下一棒须输出两条 Prompt（由人择一）**：
   - 推荐判定：仅推荐 **路径 A（22 R1）**（清单有待确认项 + test_strategy required + 涉 api/）。
   - 路径 A · 22 任务审核 R1：TEMPLATE-task-audit-invoke §3 全文，task_path=docs/tasks/active/task_chatbi_intent_hints_step2_v1.md，review 落盘 docs/harness/reviews/by-task/chatbi_intent_hints_step2_v1/ 或 docs/harness/reviews/task_chatbi_intent_hints_step2_v1_audit_R1_20260604.md（按 reviews/README）
   - 路径 B · 30 执行（跳过 22）：TEMPLATE-execute-invoke §3 全文（**不推荐**；须标注人承担闸 1）。
8. 回复末尾输出 HANDOFF_SEMI_AUTO §3.4 📋 Harness 状态栏（版本 B）。

Judgment（10）：
- spec_absorb: Q-2 是否在 task 中 resolved（仲裁默认 + env 关）
- hat_self: pass | pass-with-notes | blocked
```

## 10 帽交付摘要

- task：`docs/tasks/active/task_chatbi_intent_hints_step2_v1.md`
- Q-2 **resolved**：仲裁默认 **开** · `INTENT_HINTS_ARBITRATION=0/false` 关
- hat_self：**pass-with-notes**（Overview §7 SPEC 正文 checkbox 未同步勾选 · 由 U2 task 决议为准）
