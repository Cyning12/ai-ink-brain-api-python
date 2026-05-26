# 启动 Prompt · 关账 · Wiki-CTX-AB v1（P2 收口 · v1.0）

> **帽链终点**：22 → 30 → 40 → 50 → **本 Prompt**  
> **用法**：Open **`ai-ink-brain-api-python/`** → 新对话 → 50 建议关账无阻塞后复制下方代码块。  
> **task**：`docs/tasks/done/task_wiki_ctx_ab_v1.md`（已关账 · 2026-05-26）

---

```text
你正在执行 Harness「关账」（HANDOFF_CLOSE_TRACE），本 Epic：Wiki-CTX-AB v1 · freeze_id WIKI-CTX-AB@2026-05-25 · **P2 收口**（整 task 归档）。

前置检查（缺一则停）：
- [ ] 22 R1：docs/harness/reviews/by-task/wiki-ctx-ab/task_wiki_ctx_ab_v1_audit_R1_20260526.md
- [ ] 30/40 invoke 已落盘；task ### 自检结论含 40 pass（P2）
- [ ] 50：docs/tasks/reinspect_results/reinspect_wiki_ctx_ab_p2_*_v1.md 建议关账无阻塞
- [ ] scorecard §P2 + conclusion_p2_zh.md 已 commit
- [ ] P1 已 accepted（conclusion_p1_zh.md）

你必须完成：

1. ~~将 task `git mv` 至 done~~（**已完成**）；维护时仅核对状态与 §验收勾选。

2. 勾选 §验收标准 P1/P2；文末 **关闭回溯（HANDOFF_CLOSE_TRACE）**（22/30/40/50 · invoke · commit）。

3. 更新 docs/tasks/_views/done.md、RECENT_TASK_SCHEDULE §6.6（T2 done / Wiki 读序结论一行）。

4. （可选 · 人审后）SPEC §3.1 P2 签收行与「默认读序」建议 — 按 conclusion_p2 表述，勿与 conclusion 矛盾。

5. 对话输出 **执行路线与 Commit 回溯**；**无下一棒 Prompt**。

6. Commit：message `docs(task): Wiki-CTX-AB v1 关账 · WIKI-CTX-AB@2026-05-25`

禁止：未 50 通过即标 done；改 harness prompts

关键词：关账、CLOSE_TRACE、P2、T2、WIKI-CTX-AB、coding_wiki 读序
```
