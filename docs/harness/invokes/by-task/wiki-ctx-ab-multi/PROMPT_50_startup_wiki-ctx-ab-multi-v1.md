# 启动 Prompt · 50 独立复检 · Wiki-CTX-AB Multi（v1.0）

> **帽链**：22 → 30 → 40 → **50** → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话** → 复制下方代码块。  
> **下一棒**：[`PROMPT_CLOSE_wiki-ctx-ab-multi-v1.md`](./PROMPT_CLOSE_wiki-ctx-ab-multi-v1.md)

---

```text
你正在扮演 Harness「独立复检帽（50）」（本 Epic：Wiki-CTX-AB Multi · 后端子仓），严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/templates/TEMPLATE-independent-reinspect-invoke.md §3
- docs/tasks/reinspect_results/README.md
- docs/harness/ACCEPTANCE_LANDING.md

【开帽】落盘 invoke 至：
docs/harness/invokes/by-task/wiki-ctx-ab-multi/invoke_YYYYMMDD_50_wiki-ctx-ab-multi-v1.md

输入：
- 主 task：docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md
- freeze_id：WIKI-CTX-AB-MULTI@2026-05-26
- 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab-multi/task_wiki_ctx_ab_multi_slug_v1_audit_R1_YYYYMMDD.md
- 40：task ### 自检结论（执行者）
- 实验：docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/

§一 独立复检
1. **独立**重跑 40 的 VERIFY (1)–(6)。
2. 对照 22：slug 名单、题集、非范围。
3. 抽检 scorecard 与 questions.md 要点一致性（各抽 2 题）。

§二 全局验收
4. task §验收标准逐条 pass/fail。

落盘（硬）：
docs/tasks/reinspect_results/reinspect_wiki_ctx_ab_multi_YYYYMMDD_v1.md

结论：建议关账 / 须回 30（列清单）

Commit：reinspect + invoke only。

对话末尾：无阻塞 → 提示 PROMPT_CLOSE；📋 Harness 状态栏。

禁止：改 scorecard/conclusion 正文；代填 human_gate

关键词：50、reinspect、WIKI-CTX-AB-MULTI、多 slug
```
