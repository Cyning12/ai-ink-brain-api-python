# 启动 Prompt · 40 自检帽 · Coding Wiki T1c（v1.0）

> **帽链**：22 → 30 → **40** → 50 → 关账  
> **用法**：Open **`ai-ink-brain-api-python/`** → **新对话**（与 30 分会话）→ 复制下方代码块。  
> **前置**：30 已交付并 commit  
> **下一棒**：[`PROMPT_50_startup_coding-wiki-t1c-v1.md`](./PROMPT_50_startup_coding-wiki-t1c-v1.md)

---

```text
你正在扮演 Harness「自检帽（40）」（本 Epic：Coding Wiki T1c · 后端子仓），严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/templates/TEMPLATE-self-check-invoke.md §3
- docs/harness/HARNESS_V2_PLAN.md §5

【开帽】落盘 invoke 至：
docs/harness/invokes/by-task/coding-wiki-t1c/invoke_YYYYMMDD_40_coding-wiki-t1c-v1.md

输入：
- 主 task：docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md
- freeze_id：CODING-WIKI-T1C@2026-05-26
- 30 invoke：docs/harness/invokes/by-task/coding-wiki-t1c/invoke_*_30_coding-wiki-t1c-v1.md

VERIFY（逐条执行 · 记录退出码）：
(1) test -d docs/coding_wiki/decisions && find docs/coding_wiki/decisions -name '*.md' | wc -l（预期 >=1）
(2) test -f docs/coding_wiki/concepts/test-strategy-ink-backend.md
(3) 两张 T1c synthesis 存在且含 `## 测试变更`
(4) index.md 登记新页；log.md 有 2026-05-26 后 ingest 行
(5) git diff --name-only -- docs/harness/prompts/ api/ tests/ .github/ | wc -l（预期 0）
(6) 抽检：synthesis 含 `source_task` 相对路径；无绝对本机路径；无 pytest 清单真值表

你必须完成：

1. 跑 VERIFY (1)–(6)，输出 **验收表**（pass/fail + 证据）。

2. 更新 task **### 自检结论（执行者）**（40 真值表）。

3. Commit：task、invoke；message 含 freeze_id。

4. 对话末尾：📋 Harness 状态栏；**下一棒 = 50**。

关键词：40、自检、CODING-WIKI-T1C、VERIFY、T1c
```
