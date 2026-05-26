# 启动 Prompt · 40 自检帽 · Wiki-CTX-AB Multi（v1.0）

> **帽链**：22 → 30 → **40** → 50 → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话** → 复制下方代码块。  
> **下一棒**：[`PROMPT_50_startup_wiki-ctx-ab-multi-v1.md`](./PROMPT_50_startup_wiki-ctx-ab-multi-v1.md)

---

```text
你正在扮演 Harness「自检帽（40）」（本 Epic：Wiki-CTX-AB Multi · 后端子仓），严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/templates/TEMPLATE-self-check-invoke.md §3

【开帽】落盘 invoke 至：
docs/harness/invokes/by-task/wiki-ctx-ab-multi/invoke_YYYYMMDD_40_wiki-ctx-ab-multi-v1.md

输入：
- 主 task：docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md
- freeze_id：WIKI-CTX-AB-MULTI@2026-05-26
- 30 invoke：docs/harness/invokes/by-task/wiki-ctx-ab-multi/invoke_*_30_wiki-ctx-ab-multi-v1.md

VERIFY（逐条 · 子仓根）：
(1) test -f docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/conclusion_multi_slug_zh.md
(2) 两 slug 各有 payloads/H-lean_<slug>.md 与 payloads/W_<slug>.md，且含 payload_char_count
(3) scorecard.md §Multi 已填（2 slug × 4 题 × 2 臂）
(4) git diff --name-only -- docs/harness/experiments/wiki_ctx_ab_v1/payloads/ | wc -l（预期 0，未误改 P2 冻结）
(5) git diff --name-only -- api/ docs/harness/prompts/ tests/ .github/ | wc -l（预期 0）
(6) 抽检 conclusion：引用 P2 结论不矛盾；未将「部分 slug 失败」写成「全盘否定 P2」除非证据支持

你必须完成：
1. 跑 VERIFY (1)–(6)，输出验收表。
2. 更新 task **### 自检结论（执行者）**（40 真值）。
3. Commit：task、invoke。
4. 📋 Harness 状态栏；下一棒 = 50。

关键词：40、VERIFY、WIKI-CTX-AB-MULTI、scorecard
```
