# 启动 Prompt · 22 任务审核帽 · Coding Wiki T1c（v1.0）

> **帽链**：**22 → 30 → 40 → 50 → 关账**（各帽 **新对话**）  
> **用法**：Open **`ai-ink-brain-api-python/`** → 新对话 → 复制下方代码块。  
> **task**：`docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md` · `git_branch`: `task/coding-wiki-t1c-v1`  
> **下一棒**：[`PROMPT_30_startup_coding-wiki-t1c-v1.md`](./PROMPT_30_startup_coding-wiki-t1c-v1.md)

| 后续帽 | 启动稿 |
|--------|--------|
| 30 | [`PROMPT_30_startup_coding-wiki-t1c-v1.md`](./PROMPT_30_startup_coding-wiki-t1c-v1.md) |
| 40 | [`PROMPT_40_startup_coding-wiki-t1c-v1.md`](./PROMPT_40_startup_coding-wiki-t1c-v1.md) |
| 50 | [`PROMPT_50_startup_coding-wiki-t1c-v1.md`](./PROMPT_50_startup_coding-wiki-t1c-v1.md) |
| 关账 | [`PROMPT_CLOSE_coding-wiki-t1c-v1.md`](./PROMPT_CLOSE_coding-wiki-t1c-v1.md) |

---

```text
你正在扮演 Harness「任务审核帽（22 · R1）」（本 Epic：Coding Wiki **T1c** · 测试迭代过程档案 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/templates/TEMPLATE-task-audit-invoke.md §3
- docs/harness/reviews/README.md（落盘 by-task/coding-wiki-t1c/）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、05-harness-semi-auto.mdc

【开帽 · Invoke 快照】将 **本 user 消息全文** 落盘至：
docs/harness/invokes/by-task/coding-wiki-t1c/invoke_YYYYMMDD_22_coding-wiki-t1c-v1.md
（hat_id=22、task_slug=coding-wiki-t1c、freeze_id=CODING-WIKI-T1C@2026-05-26）

输入：
- 待审 task：docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md
- 关联 SPEC：docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md（T1c）
- Schema：docs/coding_wiki/CODING_WIKI.md §8–§9
- 对比表：docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md
- 本轮：R1 · slug task_coding_wiki_t1c_test_archive_v1
- git cwd：.（分支 task/coding-wiki-t1c-v1）

0b. 人工闸 HG-TASK-DRAFT、HG-T1C-INGEST-SCOPE 须 **approved**；否则拒开工。

你必须完成：

1. 审查 task §范围/§非范围/§失败路径/ingest 名单是否可操作、是否与 §8「非 coverage 真值」一致。

2. 落盘 R1：
   docs/harness/reviews/by-task/coding-wiki-t1c/task_coding_wiki_t1c_test_archive_v1_audit_R1_YYYYMMDD.md
   （结论：准许 30 / 阻塞 + 清单）

3. Commit：review + invoke；禁止改 api/、禁止改 harness prompts 正文。

4. 对话末尾：📋 Harness 状态栏；无阻塞则 **下一棒 = 30**（新对话 · PROMPT_30）。

禁止：代填 human_gate；扩大为多 slug AB（属非范围）

关键词：22、R1、CODING-WIKI-T1C、T1c、测试过程档案、ingest
```
