# 启动 Prompt · 关账 · Coding Wiki 试点（v1.0）

> **帽链终点**：22 → 30 → 40 → 50 → **本 Prompt**  
> **用法**：Open **`ai-ink-brain-api-python/`** → 新对话 → 50 无阻塞后复制下方代码块。  
> **task**：`docs/tasks/active/task_coding_wiki_pilot_v1.md`

---

```text
你正在执行 Harness「关账」（HANDOFF_CLOSE_TRACE），本 Epic：Coding Wiki 试点 · freeze_id CODING-WIKI-PILOT@2026-05-25。

前置检查（缺一则停）：
- [ ] 22 R1：docs/harness/reviews/by-task/coding-wiki-pilot/task_coding_wiki_pilot_v1_audit_R1_20260526.md
- [ ] 30/40 invoke 已落盘；task ### 自检结论（执行者）含 40 pass
- [ ] 50：docs/tasks/reinspect_results/reinspect_coding_wiki_pilot_*_v1.md 建议关账无阻塞
- [ ] docs/coding_wiki/ 已 commit

你必须完成：

1. 将 task `git mv` 至 docs/tasks/done/task_coding_wiki_pilot_v1.md；状态改为 done（YYYY-MM-DD）。

2. 在本 task 文末写入 **关闭回溯（HANDOFF_CLOSE_TRACE）**：执行路线表（22/30/40/50 · invoke 路径 · commit short-hash）。

3. 更新（若存在）docs/tasks/_views/ 或 RECENT_TASK_SCHEDULE §6.6 一行（T1b done · 可选）。

4. 对话输出 **执行路线与 Commit 回溯**（分仓仅 api-python）；**无下一棒 Prompt**。

5. Commit：task done 路径 + 关账段落 + _views；message：docs(task): Coding Wiki pilot 关账 · CODING-WIKI-PILOT@2026-05-25

提醒：关账后可启动 Wiki-CTX-AB **P2**（task_wiki_ctx_ab_v1 · 依赖本 pilot 同 slug ingest）。

关键词：关账、done、CLOSE_TRACE、T1b、CODING-WIKI-PILOT
```
