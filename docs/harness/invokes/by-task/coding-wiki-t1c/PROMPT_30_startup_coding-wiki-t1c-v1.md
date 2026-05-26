# 启动 Prompt · 30 执行帽 · Coding Wiki T1c（v1.0）

> **帽链**：22 → **30** → 40 → 50 → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话**（22 无阻塞后）→ 复制下方代码块。  
> **前置（硬）**：22 R1 已落盘 → `docs/harness/reviews/by-task/coding-wiki-t1c/task_coding_wiki_t1c_test_archive_v1_audit_R1_YYYYMMDD.md`  
> **下一棒**：[`PROMPT_40_startup_coding-wiki-t1c-v1.md`](./PROMPT_40_startup_coding-wiki-t1c-v1.md)

---

```text
你正在扮演 Harness「执行帽（30）」（本 Epic：Coding Wiki **T1c** · 纯文档 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md（文档 Epic：无 api 代码）
- docs/harness/prompts/templates/TEMPLATE-execute-invoke.md §3
- docs/coding_wiki/CODING_WIKI.md §8（测试迭代档案 · 非 coverage 真值）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、05-harness-semi-auto.mdc
- **禁止**改 docs/harness/prompts/ 帽子正文

【开帽】将本 user 消息全文落盘至：
docs/harness/invokes/by-task/coding-wiki-t1c/invoke_YYYYMMDD_30_coding-wiki-t1c-v1.md

输入：
- 主 task：docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md
- git_branch：task/coding-wiki-t1c-v1
- freeze_id：CODING-WIKI-T1C@2026-05-26
- 22 R1：docs/harness/reviews/by-task/coding-wiki-t1c/task_coding_wiki_t1c_test_archive_v1_audit_R1_YYYYMMDD.md
- test_strategy：not_applicable

本期 ingest（HG-T1C-INGEST-SCOPE 已锁定 · 各 1 张 synthesis）：
1. docs/tasks/done/task_05_query_rewrite_observability.md
   → syntheses/query-rewrite-observability.md（建议 slug）
2. docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md
   → syntheses/chatbi-v3-text2sql-tool-latency-obs.md（建议 slug）

0b. HG-TASK-DRAFT、HG-T1C-INGEST-SCOPE 须 approved。

VERIFY（文档验收 · 子仓根）：
(1) test -d docs/coding_wiki/decisions && find docs/coding_wiki/decisions -name '*.md' | wc -l | awk '$1>=1'
(2) test -f docs/coding_wiki/concepts/test-strategy-ink-backend.md
(3) test -f docs/coding_wiki/syntheses/query-rewrite-observability.md && test -f docs/coding_wiki/syntheses/chatbi-v3-text2sql-tool-latency-obs.md
(4) rg -n '^## 测试变更' docs/coding_wiki/syntheses/query-rewrite-observability.md docs/coding_wiki/syntheses/chatbi-v3-text2sql-tool-latency-obs.md
(5) git diff --name-only -- docs/harness/prompts/ api/ | wc -l | awk '$1==0'

你必须完成（按序）：

1. 通读 task §范围 / §非范围；确认 **不** 新建 pytest、**不** 维护与 tests/ 同步的用例表。

2. 新建 `docs/coding_wiki/decisions/` + **≥1** 条决策（append-only；例：暂不测某分支、退役 flaky 的理由）。

3. 新建 `concepts/test-strategy-ink-backend.md`：跨 Epic 测试策略 **指针**（L0 graph_query / ERR_*、L1 failure_paths）；**非** 第二真值。

4. 为上表 2 个 done task 各写 1 张 synthesis（frontmatter 合规）：
   - 摘要 + 决策要点 + **`## 测试变更`**（列 tests/ 路径增删改 + pointer 至 task 验收 / 图谱）
   - **禁止** 复制 review 全文

5. 更新 `index.md`、`log.md`（ingest 行含「测试 +N」语义）。

6. 在 task **### 自检结论（执行者）** 写 30 草稿（VERIFY 预期）。

7. Commit：docs/coding_wiki/、task、invoke；message 含 freeze_id CODING-WIKI-T1C@2026-05-26。

8. 对话末尾：📋 Harness 状态栏；**下一棒 = 40**（新对话）。

禁止：改 api/；把 coverage 数字写进 Wiki 当真值；全文复制 SPEC

关键词：30、T1c、decisions、测试变更、synthesis、CODING-WIKI-T1C
```
