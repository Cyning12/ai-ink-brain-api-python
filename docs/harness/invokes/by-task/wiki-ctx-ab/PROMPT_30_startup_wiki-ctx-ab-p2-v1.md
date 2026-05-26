# 启动 Prompt · 30 执行帽 · Wiki-CTX-AB P2（v1.0）

> **帽链**：22 → **30** → 40 → 50 → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话**（22 无阻塞后）→ 复制下方代码块。  
> **前置（硬）**：22 R1 已落盘且无阻塞 → `docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md`  
> **下一棒**：[`PROMPT_40_startup_wiki-ctx-ab-p2-v1.md`](./PROMPT_40_startup_wiki-ctx-ab-p2-v1.md)

---

```text
你正在扮演 Harness「执行帽（30）」（本 Epic：Wiki-CTX-AB **P2** · 纯文档实验 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（文档 Epic：无 api 代码）
- docs/harness/prompts/templates/TEMPLATE-execute-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc
- **禁止**改 docs/harness/prompts/ 帽子正文

【开帽】将本 user 消息全文落盘至：
docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_30_wiki-ctx-ab-p2-v1.md

输入：
- 主 task：docs/tasks/active/task_wiki_ctx_ab_v1.md
- git_branch：task/wiki-ctx-ab-p2-v1
- freeze_id：WIKI-CTX-AB@2026-05-25
- 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md
- 实验真值：
  docs/harness/experiments/wiki_ctx_ab_v1/questions.md
  docs/harness/experiments/wiki_ctx_ab_v1/PROMPT_third_party_agent_wiki_ctx_ab_p2.md
- gold slug：harness-p1-docs-consolidation
- test_strategy：not_applicable

0b. 人工闸 HG-AB-SLUG、HG-AB-P1-DONE 须 approved。

你必须完成（P2 执行 · 按序）：

1. **物化 W 臂**（若 22 指出缺失或 char_count 空）：
   python tools/wiki_ctx_ab_materialize_w.py --slug harness-p1-docs-consolidation
   确认：docs/harness/experiments/wiki_ctx_ab_v1/payloads/W_harness-p1-docs-consolidation.md
   对照 payloads/TEMPLATE-W.md

2. **跑 P2 对照**（H-lean vs W · 同 questions.md Q1–Q4）：
   - 严格按 PROMPT_third_party_agent_wiki_ctx_ab_p2.md §0–§3
   - 每臂每题 **独立会话**（或独立 thread）
   - 载荷仅允许：
     · H-lean：payloads/H-lean_harness-p1-docs-consolidation.md（P1 已物化 · **勿改**）
     · W：payloads/W_harness-p1-docs-consolidation.md
   - **禁止**读盘载荷外文件

3. **填表**：docs/harness/experiments/wiki_ctx_ab_v1/scorecard.md **§P2**（8 行 + 汇总 + 逐题原文可选）

4. **结论文**：docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md
   - 须回答：W 相对 H-lean 是否再省 token（建议阈值 ≥30%）且正确性不降（SPEC §3.1）
   - 明确：是否推荐 Agent **默认先读** `docs/coding_wiki/index` + 相关 syntheses

5. 更新 task：§范围 P2 勾选；实现备忘（模型名、日期、payload_char_count）；**勿**关账（属 CLOSE）。

6. **Commit**（禁止 git add -A）：
   docs/harness/experiments/wiki_ctx_ab_v1/
   tools/wiki_ctx_ab_materialize_w.py
   docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_30_*.md
   docs/tasks/active/task_wiki_ctx_ab_v1.md

7. 对话末尾：📋 Harness 状态栏；**下一棒 = 40**（新对话 · PROMPT_40）。

禁止：改 api/、改 docs/harness/prompts/、重跑 P1 改 H-full/H-lean 源文件

关键词：30、P2、H-lean、W、scorecard、conclusion_p2、Wiki-CTX-AB
```
