# 启动 Prompt · 22 任务审核帽 · Wiki-CTX-AB Multi（v1.0）

> **帽链**：**22 → 30 → 40 → 50 → 关账**（各帽 **新对话**）  
> **用法**：Open **`ai-ink-brain-api-python/`** → 新对话 → 复制下方代码块。  
> **task**：`docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md` · `git_branch`: `task/wiki-ctx-ab-multi-slug-v1`  
> **下一棒**：[`PROMPT_30_startup_wiki-ctx-ab-multi-v1.md`](./PROMPT_30_startup_wiki-ctx-ab-multi-v1.md)

| 后续帽 | 启动稿 |
|--------|--------|
| 30 | [`PROMPT_30_startup_wiki-ctx-ab-multi-v1.md`](./PROMPT_30_startup_wiki-ctx-ab-multi-v1.md) |
| 40 | [`PROMPT_40_startup_wiki-ctx-ab-multi-v1.md`](./PROMPT_40_startup_wiki-ctx-ab-multi-v1.md) |
| 50 | [`PROMPT_50_startup_wiki-ctx-ab-multi-v1.md`](./PROMPT_50_startup_wiki-ctx-ab-multi-v1.md) |
| 关账 | [`PROMPT_CLOSE_wiki-ctx-ab-multi-v1.md`](./PROMPT_CLOSE_wiki-ctx-ab-multi-v1.md) |

---

```text
你正在扮演 Harness「任务审核帽（22 · R1）」（本 Epic：Wiki-CTX-AB **多 slug** · H-lean vs W 扩域 · 后端子仓），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/templates/TEMPLATE-task-audit-invoke.md §3
- docs/harness/reviews/README.md（落盘 by-task/wiki-ctx-ab-multi/）
- docs/harness/HARNESS_V2_PLAN.md §5
- .cursor/rules/06-harness-in-repo.mdc、05-harness-semi-auto.mdc

【开帽 · Invoke 快照】将 **本 user 消息全文** 落盘至：
docs/harness/invokes/by-task/wiki-ctx-ab-multi/invoke_YYYYMMDD_22_wiki-ctx-ab-multi-v1.md
（hat_id=22、task_slug=wiki-ctx-ab-multi、freeze_id=WIKI-CTX-AB-MULTI@2026-05-26）

输入：
- 待审 task：docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md
- 关联 SPEC：docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md §5.1（多 slug AB）
- 实验目录：docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/
- 题集草案：docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/questions.md
- P2 基线（只读）：docs/harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md
- 锁定 slug（须 test -f synthesis）：
  · docs/coding_wiki/syntheses/tech-graph-gate-d-v2-tasks.md
  · docs/coding_wiki/syntheses/query-rewrite-observability.md
- git cwd：.（分支 task/wiki-ctx-ab-multi-slug-v1）

0b. 人工闸 HG-TASK-DRAFT、HG-AB-MULTI-SLUGS、HG-AB-P2-BASELINE 须 **approved**；否则拒准 30。

你必须完成：

1. 审查 task §范围/§非范围/§失败路径；确认 **不** 覆盖 wiki_ctx_ab_v1 已冻结 P1/P2 文件。

2. 审查 questions.md：每 slug 4 题、要点可自 done task + synthesis 验证；陷阱题（A-Q4、B-Q4）边界清晰。

3. 检查实验工件：README、scorecard 空表、TEMPLATE-H-lean；W 物化路径说明可执行。

4. 落盘 R1：
   docs/harness/reviews/by-task/wiki-ctx-ab-multi/task_wiki_ctx_ab_multi_slug_v1_audit_R1_YYYYMMDD.md
   （结论：准许 30 / 阻塞 + 清单）

5. Commit：review + invoke；禁止改 api/、禁止改 harness prompts 正文。

6. 对话末尾：📋 Harness 状态栏；无阻塞则 **下一棒 = 30**（新对话 · PROMPT_30）。

禁止：代填 human_gate；执行跑题/填 scorecard（属 30）；擅自增第三 slug

关键词：22、R1、WIKI-CTX-AB-MULTI、多 slug、H-lean、W、对照实验二
```
