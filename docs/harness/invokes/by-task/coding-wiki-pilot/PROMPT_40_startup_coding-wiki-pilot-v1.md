# 启动 Prompt · 40 自检帽 · Coding Wiki 试点（v1.0）

> **帽链**：22 → **30** → **40** → 50 → 关账  
> **用法**：Open Folder **`ai-ink-brain-api-python/`** → **新对话**（与 30 分会话）→ 复制下方代码块。  
> **前置**：30 已交付 `docs/coding_wiki/` 并 commit（含 freeze_id）  
> **上一棒**：[`PROMPT_30_startup_coding-wiki-pilot-v1.md`](./PROMPT_30_startup_coding-wiki-pilot-v1.md)  
> **下一棒**：[`PROMPT_50_startup_coding-wiki-pilot-v1.md`](./PROMPT_50_startup_coding-wiki-pilot-v1.md)

---

```text
你正在扮演 Harness「自检帽（40）」（本 Epic：Coding Wiki 试点 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/templates/TEMPLATE-self-check-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5（test_strategy: not_applicable）
- .cursor/rules/06-harness-in-repo.mdc
- Harness 帽子链 ≠ Cursor Skills

【开帽】确认 30 已落盘 invoke 并 commit；将本消息落盘至：
docs/harness/invokes/by-task/coding-wiki-pilot/invoke_YYYYMMDD_40_coding-wiki-pilot-v1.md

输入：
- 主 task：docs/tasks/active/task_coding_wiki_pilot_v1.md
- worktree_root / cwd：.（子仓根）
- freeze_id：CODING-WIKI-PILOT@2026-05-25
- 22 R1 审查（须已存在）：
  docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md
- 30 invoke（填实际文件名）：
  docs/harness/invokes/by-task/coding-wiki-pilot/invoke_*_30_coding-wiki-pilot-v1.md

VERIFY（须在子仓根逐条执行 · 记录退出码）：
(1) test -f docs/coding_wiki/CODING_WIKI.md && test -f docs/coding_wiki/index.md && test -f docs/coding_wiki/log.md
(2) find docs/coding_wiki/syntheses docs/coding_wiki/concepts -name '*.md' 2>/dev/null | wc -l（预期 >=2）
(3) git diff --name-only -- docs/harness/prompts/ | wc -l（预期 0）
(4) rg -l 'coding_wiki' docs/README.md docs/tasks/README.md 2>/dev/null | head -1
(5) 抽检 2 张 Wiki 页：含相对链至 docs/tasks/done/、无绝对本机路径、非全文复制 SPEC

你必须完成：

1. 通读 task §验收标准、§非范围、30 帽 ### 自检结论（执行者）草稿。

2. 逐条跑 VERIFY (1)–(5)，输出 **验收表**（pass/fail + 证据）。

3. 更新 task **### 自检结论（执行者）**（含 40 复检表；与 30 草稿合并或覆盖为 40 真值）。

4. Commit：仅 docs/coding_wiki/、task、本 invoke、reviews（若补链）；message 含 freeze_id。

5. 对话末尾：📋 Harness 状态栏；**下一棒 = 50**（新对话 · PROMPT_50_startup）。

禁止：改 api/、改 docs/harness/prompts/、扩大 scope 重做 Wiki 架构

关键词：40、自检、CODING-WIKI-PILOT、VERIFY、not_applicable
```
