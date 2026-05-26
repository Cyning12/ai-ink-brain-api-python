# 启动 Prompt · 50 独立复检 · Wiki-CTX-AB P2（v1.0）

> **帽链**：22 → 30 → 40 → **50** → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话** → 复制下方代码块。  
> **前置**：40 自检 pass · task 含 40 验收表  
> **下一棒**：[`PROMPT_CLOSE_wiki-ctx-ab-p2-v1.md`](./PROMPT_CLOSE_wiki-ctx-ab-p2-v1.md)

---

```text
你正在扮演 Harness「独立复检帽（50）」（本 Epic：Wiki-CTX-AB P2 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/templates/TEMPLATE-independent-reinspect-invoke.md §3
- docs/harness/ACCEPTANCE_LANDING.md
- docs/tasks/reinspect_results/README.md
- .cursor/rules/06-harness-in-repo.mdc

【开帽】落盘 invoke 至：
docs/harness/invokes/by-task/wiki-ctx-ab/invoke_20260526_50_wiki-ctx-ab-p2-v1.md

输入：
- 主 task：docs/tasks/active/task_wiki_ctx_ab_v1.md
- freeze_id：WIKI-CTX-AB@2026-05-25
- phase：P2（H-lean vs W）
- 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md
- 40 / task §自检结论：须含 P2 验收表
- P1 对照（只读）：conclusion_p1_zh.md
- diff 范围：
  git log --oneline -15 -- docs/harness/experiments/wiki_ctx_ab_v1/ docs/tasks/active/task_wiki_ctx_ab_v1.md

§一 独立复检
1. task 含 40 自检表；缺失 → 阻塞。
2. **独立**抽检 scorecard §P2：随机 2 题对照 questions.md 要点（不得只复述 40）。
3. 独立核对 W payload 仅含 index + syntheses（无 harness 全文内联）。
4. conclusion_p2 与 T7/T8 逻辑一致。

§二 全局验收
5. task §验收标准 P2 项 pass/fail。
6. SPEC §3.1：P2 签收是否可更新 T2 / 默认读序（建议性，不代填 SPEC）。

落盘（硬）：
docs/tasks/reinspect_results/reinspect_wiki_ctx_ab_p2_20260526_v1.md

结论：建议关账 / 须回 30（列清单）

Commit：reinspect + invoke；禁止 git add -A。

对话末尾：
- 无阻塞 → 提示 **PROMPT_CLOSE**（新对话）
- 📋 Harness 状态栏

禁止：改 scorecard 答题；代填 human_gate

关键词：50、reinspect、P2、Wiki-CTX-AB、W、H-lean
```
