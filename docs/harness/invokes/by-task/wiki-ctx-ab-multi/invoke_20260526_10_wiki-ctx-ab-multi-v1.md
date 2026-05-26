# Invoke 快照 · 10 需求帽（等效）· Wiki-CTX-AB Multi（v1）

| 字段 | 值 |
|------|-----|
| **hat_id** | 10（等效 · 由统筹 Agent 起草，未单独开 10 对话） |
| **task_slug** | `wiki-ctx-ab-multi` |
| **task_path** | `docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md` |
| **freeze_id** | `WIKI-CTX-AB-MULTI@2026-05-26` |
| **git_branch** | `task/wiki-ctx-ab-multi-slug-v1` |
| **落盘日期** | 2026-05-26 |

---

## 触发

人：T1c 已 PR；按 SPEC §5.1 起草 **多 slug AB** task，并生成 **22→关账** Prompt 链供新 Agent 执行。

## 10 帽交付摘要

- `docs/tasks/active/task_wiki_ctx_ab_multi_slug_v1.md`
- `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/`（README、questions 草案、scorecard 空表、H-lean 模板）
- `docs/harness/invokes/by-task/wiki-ctx-ab-multi/PROMPT_{22,30,40,50,CLOSE}_*.md`
- 人工闸初始 **pending**（须人批后再 22）

## 下一棒

**22 R1** · [`PROMPT_22_startup_wiki-ctx-ab-multi-v1.md`](./PROMPT_22_startup_wiki-ctx-ab-multi-v1.md)（新对话）
