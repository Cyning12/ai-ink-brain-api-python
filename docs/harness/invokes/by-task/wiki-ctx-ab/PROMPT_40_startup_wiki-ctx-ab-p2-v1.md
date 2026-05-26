# 启动 Prompt · 40 自检帽 · Wiki-CTX-AB P2（v1.0）

> **帽链**：22 → 30 → **40** → 50 → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话** → 复制下方代码块。  
> **前置**：30 已填 scorecard §P2 + `conclusion_p2_zh.md` 并 commit  
> **下一棒**：[`PROMPT_50_startup_wiki-ctx-ab-p2-v1.md`](./PROMPT_50_startup_wiki-ctx-ab-p2-v1.md)

---

```text
你正在扮演 Harness「自检帽（40）」（本 Epic：Wiki-CTX-AB P2 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/templates/TEMPLATE-self-check-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc

【开帽】落盘 invoke 至：
docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_40_wiki-ctx-ab-p2-v1.md

输入：
- 主 task：docs/tasks/active/task_wiki_ctx_ab_v1.md
- freeze_id：WIKI-CTX-AB@2026-05-25
- 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md
- 30 invoke：docs/harness/invokes/by-task/wiki-ctx-ab/invoke_*_30_wiki-ctx-ab-p2-v1.md

VERIFY（子仓根 · 记录退出码）：
(1) test -f docs/harness/experiments/wiki_ctx_ab_v1/payloads/TEMPLATE-W.md
(2) test -f docs/harness/experiments/wiki_ctx_ab_v1/payloads/W_harness-p1-docs-consolidation.md
(3) test -f docs/coding_wiki/syntheses/harness-p1-docs-consolidation.md
(4) rg -n '^## P2' docs/harness/experiments/wiki_ctx_ab_v1/scorecard.md && rg 'pass|fail' scorecard.md §P2 区域（人工读表：8 行已填）
(5) test -f docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md
(6) git diff --name-only -- docs/harness/prompts/ | wc -l（预期 0）
(7) python tools/wiki_ctx_ab_materialize_w.py --slug harness-p1-docs-consolidation（可选：确认 W 可再生）

你必须完成：

1. 通读 30 产出、task §验收标准（P2）、conclusion_p2 是否回答「默认读序」。

2. 逐条 VERIFY (1)–(6)，输出 **验收表**。

3. 更新 task **### 自检结论（执行者）**（40 · P2 专节或合并表）。

4. Commit：实验目录、task、invoke；message 含 WIKI-CTX-AB · P2 · 40。

5. 对话末尾：📋 Harness 状态栏；**下一棒 = 50**（新对话）。

禁止：改 scorecard 答题原文（除非 30 明显错误且注明）；改 harness prompts

关键词：40、P2、VERIFY、scorecard、conclusion_p2
```
