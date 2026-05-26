# 启动 Prompt · 50 独立复检 · Coding Wiki T1c（v1.0）

> **帽链**：22 → 30 → 40 → **50** → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话** → 复制下方代码块。  
> **下一棒**：[`PROMPT_CLOSE_coding-wiki-t1c-v1.md`](./PROMPT_CLOSE_coding-wiki-t1c-v1.md)

---

```text
你正在扮演 Harness「独立复检帽（50）」（本 Epic：Coding Wiki T1c · 后端子仓），严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/templates/TEMPLATE-independent-reinspect-invoke.md §3
- docs/tasks/reinspect_results/README.md
- docs/harness/ACCEPTANCE_LANDING.md

【开帽】落盘 invoke 至：
docs/harness/invokes/by-task/coding-wiki-t1c/invoke_YYYYMMDD_50_coding-wiki-t1c-v1.md

输入：
- 主 task：docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md
- freeze_id：CODING-WIKI-T1C@2026-05-26
- 22 R1：docs/harness/reviews/by-task/coding-wiki-t1c/task_coding_wiki_t1c_test_archive_v1_audit_R1_YYYYMMDD.md
- 40：task ### 自检结论（执行者）须含验收表
- diff：git log --oneline -15 -- docs/coding_wiki/ docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md

§一 独立复检
1. **独立**重跑 40 的 VERIFY (1)–(6)。
2. 对照 22：是否违反「Wiki ≠ coverage 真值」、是否复制 review 全文。
3. 对照 CODING_WIKI §8：测试变更是否为 **过程叙述** 而非用例清单镜像。

§二 全局验收
4. task §验收标准逐条 pass/fail。

落盘（硬）：
docs/tasks/reinspect_results/reinspect_coding_wiki_t1c_YYYYMMDD_v1.md

结论：建议关账 / 须回 30（列清单）

Commit：reinspect + invoke only。

对话末尾：无阻塞 → 提示 **PROMPT_CLOSE**；📋 Harness 状态栏。

禁止：改 coding_wiki 正文；代填 human_gate

关键词：50、reinspect、CODING-WIKI-T1C、T1c、关账前
```
