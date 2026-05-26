# 启动 Prompt · 关账 · Wiki-CTX-AB Multi（v1.0）

> **帽链终点**：22 → 30 → 40 → 50 → **本 Prompt**  
> **用法**：Open **`ai-ink-brain-api-python/`** → 新对话 → 50 无阻塞后复制下方代码块。  
> **task**：`docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md`

---

```text
你正在执行 Harness「关账」（HANDOFF_CLOSE_TRACE），本 Epic：Wiki-CTX-AB Multi · freeze_id WIKI-CTX-AB-MULTI@2026-05-26。

前置检查（缺一则停）：
- [ ] 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab-multi/task_wiki_ctx_ab_multi_slug_v1_audit_R1_YYYYMMDD.md
- [ ] 30/40 invoke 已落盘；task ### 自检结论含 40 pass
- [ ] 50：docs/tasks/reinspect_results/reinspect_wiki_ctx_ab_multi_*_v1.md 建议关账无阻塞
- [ ] conclusion_multi_slug_zh.md + scorecard §Multi 已 commit

你必须完成：

1. `git mv` task → docs/tasks/done/task_wiki_ctx_ab_multi_slug_v1.md；状态 `done（YYYY-MM-DD 验收通过 · WIKI-CTX-AB-MULTI@2026-05-26）`。

2. 勾选 §验收标准；文末 **HANDOFF_CLOSE_TRACE**（22/30/40/50 · invoke · commit）。

3. 更新 docs/tasks/_views/done.md；RECENT_TASK_SCHEDULE §6.6：
   · 新增行 **多 slug AB → done**
   · SPEC §5.1「多 slug AB」标 **done** 或链至本 task（勿与 T1c 混淆）

4. （可选 · 人审后）WIKI_REQUIREMENTS_COMPARISON #46 一行结论；SPEC §2 时间线 T1c 旁补「Multi slug AB done」。

5. 对话输出 **执行路线与 Commit 回溯**；**无下一棒 Prompt**。

6. Commit：message `docs(task): Wiki-CTX-AB Multi slug 关账 · WIKI-CTX-AB-MULTI@2026-05-26`

禁止：未 50 通过即标 done；改 harness prompts；覆盖 wiki_ctx_ab_v1 P2 冻结文件

关键词：关账、CLOSE_TRACE、WIKI-CTX-AB-MULTI、多 slug、§5.1
```
