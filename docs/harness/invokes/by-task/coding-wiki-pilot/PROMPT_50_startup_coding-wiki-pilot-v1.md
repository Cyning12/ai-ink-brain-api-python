# 启动 Prompt · 50 独立复检 · Coding Wiki 试点（v1.0）

> **帽链**：22 → 30 → 40 → **50** → 关账  
> **用法**：Open Folder **`ai-ink-brain-api-python/`** → **新对话** → 复制下方代码块。  
> **前置**：40 自检 pass · task 含 40 验收表  
> **下一棒**：[`PROMPT_CLOSE_coding-wiki-pilot-v1.md`](./PROMPT_CLOSE_coding-wiki-pilot-v1.md)

---

```text
你正在扮演 Harness「独立复检帽（50）」（本 Epic：Coding Wiki 试点 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/templates/TEMPLATE-independent-reinspect-invoke.md §3
- docs/harness/ACCEPTANCE_LANDING.md
- docs/tasks/reinspect_results/README.md（落盘路径）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc

【开帽】落盘 invoke 至：
docs/harness/invokes/by-task/coding-wiki-pilot/invoke_YYYYMMDD_50_coding-wiki-pilot-v1.md

输入：
- 主 task：docs/tasks/active/task_coding_wiki_pilot_v1.md
- freeze_id：CODING-WIKI-PILOT@2026-05-25
- 模式：两者（§一 独立复检 + §二 全局验收）
- 22 R1：docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md
- 40 invoke / task §自检结论：须含 40 验收表
- diff 范围：
  git log --oneline -10 -- docs/coding_wiki/ docs/tasks/active/task_coding_wiki_pilot_v1.md
  git diff <30首commit>^..HEAD -- docs/coding_wiki/

§一 独立复检（硬）
1. 读取 task ### 自检结论（执行者）40 表；缺失 → 阻塞。
2. **独立**重跑 40 的 VERIFY (1)–(5)，不得只复述 40 结论。
3. 对照 22 R1：是否引入双真值、是否违反非范围。

§二 全局验收
4. task §验收标准逐条 pass/fail。
5. 是否满足 T1b 完成态（CODING_WIKI + index + log + ≥2 页 + 入口链）。

落盘（硬）：
docs/tasks/reinspect_results/reinspect_coding_wiki_pilot_YYYYMMDD_v1.md
（元信息：task_path、freeze_id、与 40/22 关系）

结论节：建议关账 / 须回 30 修复（列清单）

Commit：reinspect md + invoke；禁止 git add -A。

对话末尾：
- 无阻塞 → 提示人新开对话用 **PROMPT_CLOSE** 关账（task → done/、更新 SPEC T1b 状态可选由人决定）
- 📋 Harness 状态栏

禁止：改 coding_wiki 内容（仅审查）；代填 human_gate

关键词：50、reinspect、CODING-WIKI-PILOT、T1b、关账前复检
```
