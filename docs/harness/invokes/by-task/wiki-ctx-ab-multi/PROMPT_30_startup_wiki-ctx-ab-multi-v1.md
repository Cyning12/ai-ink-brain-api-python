# 启动 Prompt · 30 执行帽 · Wiki-CTX-AB Multi（v1.0）

> **帽链**：22 → **30** → 40 → 50 → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话**（22 无阻塞后）→ 复制下方代码块。  
> **前置**：22 R1 → `docs/harness/reviews/by-task/wiki-ctx-ab-multi/task_wiki_ctx_ab_multi_slug_v1_audit_R1_YYYYMMDD.md`  
> **下一棒**：[`PROMPT_40_startup_wiki-ctx-ab-multi-v1.md`](./PROMPT_40_startup_wiki-ctx-ab-multi-v1.md)

---

```text
你正在扮演 Harness「执行帽（30）」（本 Epic：Wiki-CTX-AB **多 slug** · 实验 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（无 api 代码）
- docs/harness/prompts/templates/TEMPLATE-execute-invoke.md §3
- docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md（方法论 · 只读）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、05-harness-semi-auto.mdc
- **禁止**改 docs/harness/prompts/ 帽子正文

【开帽】将本 user 消息全文落盘至：
docs/harness/invokes/by-task/wiki-ctx-ab-multi/invoke_YYYYMMDD_30_wiki-ctx-ab-multi-v1.md

输入：
- 主 task：docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md
- git_branch：task/wiki-ctx-ab-multi-slug-v1
- freeze_id：WIKI-CTX-AB-MULTI@2026-05-26
- 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab-multi/task_wiki_ctx_ab_multi_slug_v1_audit_R1_YYYYMMDD.md
- test_strategy：not_applicable

锁定 slug（HG-AB-MULTI-SLUGS）：
1. tech-graph-gate-d-v2-tasks
2. query-rewrite-observability

0b. HG-TASK-DRAFT、HG-AB-MULTI-SLUGS、HG-AB-P2-BASELINE 须 approved。

你必须完成（按序）：

1. 物化 payload（输出目录 **仅** docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/payloads/）：
   · W：对每个 slug 运行 `python tools/wiki_ctx_ab_materialize_w.py --slug <slug>`，将生成的 W_*.md **复制**到本实验 payloads/（**禁止覆盖** wiki_ctx_ab_v1/payloads/ 下既有文件）
   · H-lean：按 payloads/TEMPLATE-H-lean.md 为每 slug 生成 H-lean_<slug>.md（含 payload_char_count）

2. 按 questions.md 跑题：**每题 × 每臂 × 每 slug 独立会话**（或 semi_auto 连跑但须分臂隔离上下文）。W 臂 **禁止** 读 harness/done 全文。

3. 填写 scorecard.md §Multi（pass/fail、字符数、每 slug 降幅与 /4）。

4. 撰写 conclusion_multi_slug_zh.md：
   · 每 slug 是否满足「W 相对 H-lean 降幅 ≥30% 且正确性不降」
   · 汇总：是否支持「默认 coding_wiki 读序可外推至多域 slug」
   · 局限（参照 conclusion_p2 §4）

5. 更新 task §实现备忘；§自检结论写 30 草稿。

6. Commit：实验目录、task、invoke；message 含 WIKI-CTX-AB-MULTI@2026-05-26。

7. 对话末尾：📋 Harness 状态栏；**下一棒 = 40**（新对话）。

禁止：改 api/、tests/、CI；改 wiki_ctx_ab_v1 已 accepted 结论文；改 coding_wiki synthesis 正文（除非 22 阻塞项）

关键词：30、Multi slug、H-lean、W、scorecard、conclusion_multi_slug
```
