# 启动 Prompt · 关账 · Coding Wiki T1c（v1.0）

> **帽链终点**：22 → 30 → 40 → 50 → **本 Prompt**  
> **用法**：Open **`ai-ink-brain-api-python/`** → 新对话 → 50 无阻塞后复制下方代码块。  
> **task**：`docs/tasks/active/task_coding_wiki_t1c_test_archive_v1.md`

---

```text
你正在执行 Harness「关账」（HANDOFF_CLOSE_TRACE），本 Epic：Coding Wiki T1c · freeze_id CODING-WIKI-T1C@2026-05-26。

前置检查（缺一则停）：
- [ ] 22 R1：docs/harness/reviews/by-task/coding-wiki-t1c/task_coding_wiki_t1c_test_archive_v1_audit_R1_YYYYMMDD.md
- [ ] 30/40 invoke 已落盘；task ### 自检结论含 40 pass
- [ ] 50：docs/tasks/reinspect_results/reinspect_coding_wiki_t1c_*_v1.md 建议关账无阻塞
- [ ] T1c Wiki 交付已 commit（decisions + concept + 2 syntheses）

你必须完成：

1. `git mv` task → docs/tasks/done/task_coding_wiki_t1c_test_archive_v1.md；状态 `done（YYYY-MM-DD 验收通过 · CODING-WIKI-T1C@2026-05-26）`。

2. 勾选 §验收标准；文末 **HANDOFF_CLOSE_TRACE**（22/30/40/50 · invoke · commit）。

3. 更新 docs/tasks/_views/done.md；RECENT_TASK_SCHEDULE §6.6 行 **T1c → done**。

4. （可选）WIKI_REQUIREMENTS_COMPARISON §7 P1 T1c 行标 done。

5. 对话输出 **执行路线与 Commit 回溯**；**无下一棒 Prompt**。

6. Commit：message `docs(task): Coding Wiki T1c 关账 · CODING-WIKI-T1C@2026-05-26`

提醒：多 slug Wiki 对照实验 **非本 task**；若要做见 SPEC §5.1 另立 task。

关键词：关账、CLOSE_TRACE、T1c、CODING-WIKI-T1C、测试过程档案
```
