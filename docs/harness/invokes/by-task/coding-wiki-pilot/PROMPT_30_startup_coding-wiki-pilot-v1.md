# 启动 Prompt · 30 执行帽 · Coding Wiki 试点（v1.1）

> **帽链**：22 → **30** → 40 → 50 → 关账  
> **用法**：Open Folder **`ai-ink-brain-api-python/`** → **新对话**（22 完成后）→ 复制下方代码块。  
> **task**：`docs/tasks/active/task_coding_wiki_pilot_v1.md` · `git_branch`: `task/coding-wiki-pilot-v1`  
> **前置（硬）**：22 R1 已落盘且无阻塞 → `docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md`（日期以实际为准）  
> **下一棒**：[`PROMPT_40_startup_coding-wiki-pilot-v1.md`](./PROMPT_40_startup_coding-wiki-pilot-v1.md)

---

```text
你正在扮演 Harness「执行编码帽」（本 Epic：纯文档 · L2 Coding Wiki · 后端子仓），严格遵循：
- .cursor/rules/06-harness-in-repo.mdc、05-harness-semi-auto.mdc
- docs/harness/prompts/hats/30-execute-code.md、40-self-check.md
- docs/harness/HARNESS_V2_PLAN.md §5
- 工作区指导意见（只读）：Projects/docs/harness/guides/GUIDANCE_coding_wiki_llm_wiki_insert_v1_zh.md §7 骨架

【开帽】将本用户消息全文落盘至：
docs/harness/invokes/by-task/coding-wiki-pilot/invoke_YYYYMMDD_30_coding-wiki-pilot-v1.md
（同会话追问不新建 invoke）

输入：
- 主 task（相对子仓根）：
  docs/tasks/active/task_coding_wiki_pilot_v1.md
- 逻辑子仓 / worktree_root / git cwd：
  .（ai-ink-brain-api-python 子仓根）
- freeze_id：CODING-WIKI-PILOT@2026-05-25
- test_strategy：not_applicable（文档验收，见 VERIFY）
- 任务审核（22 R1 · 须已准许开工）：
  docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md
- 关联 SPEC：
  docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md（T1b）
- 首期 ingest（已锁定 · 各写 1 张 syntheses/ 或 concepts/ 页）：
  docs/tasks/done/task_harness_p1_docs_consolidation_v1.md
  docs/tasks/done/task_engineering_tech_graph_gate_d_v2_tasks_v1.md
  docs/tasks/done/task_docs_tasks_reorg_move_v1.md

0b. 人工闸 HG-TASK-DRAFT、HG-WIKI-INGEST-SCOPE 须 approved；否则拒开工。

VERIFY（文档验收 · 非 pytest · 在子仓根执行）：
(1) test -f docs/coding_wiki/CODING_WIKI.md && test -f docs/coding_wiki/index.md && test -f docs/coding_wiki/log.md
(2) find docs/coding_wiki/syntheses docs/coding_wiki/concepts -name '*.md' 2>/dev/null | wc -l | awk '$1>=2'
(3) git diff --name-only -- docs/harness/prompts/ | wc -l | awk '$1==0'
(4) rg -l 'coding_wiki' docs/README.md docs/tasks/README.md 2>/dev/null | head -1

你必须完成（按序）：

1. 通读 task §范围 / §非范围 / §failure_paths / §帽子顺序。

2. 新建 docs/coding_wiki/ 骨架（见 GUIDANCE §7）：
   - CODING_WIKI.md（L0/L1/L2、ingest/query/lint、frontmatter、[[wikilink]]）
   - index.md、log.md（含 2026-05-26 试点启动条目）
   - syntheses/ 或 concepts/ 下 ≥2 页（来自上表 3 个 done task 中的至少 2 个；建议 3 页各 1 张）
   - 每页：摘要 + freeze_id/关账日 + 相对链至 task/review；**禁止**复制 SPEC/review 全文

3. docs/tasks/README.md 或 docs/README.md 增加一行链至 coding_wiki/。

4. 自检：跑 VERIFY (1)–(4)；回填 task ### 自检结论（执行者）。

5. Commit（仅本子仓 · 禁止 git add -A）：
   git add docs/coding_wiki/ docs/tasks/README.md docs/README.md docs/tasks/active/task_coding_wiki_pilot_v1.md
   message 含 freeze_id CODING-WIKI-PILOT@2026-05-25

6. 对话末尾：📋 Harness 状态栏（版本 B）；**下一棒 = 40**（新对话 · PROMPT_40_startup）；帽链余下 **50 → PROMPT_CLOSE**。

硬约束：
- Open Folder 必须是本子仓（交付物在 docs/coding_wiki/）
- 禁止改 docs/harness/prompts/、api/、CI
- 禁止 ingest active task 入 syntheses/
- Harness 流程 ≠ Cursor Skills（skills 仅 Wiki stub 链）

关键词：Coding Wiki、ingest、index.md、CODING_WIKI、T1b、done task only
```
