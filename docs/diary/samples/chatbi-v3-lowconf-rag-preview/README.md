# 标准样本 · ChatBI V3 低置信 RAG 预览 + plan_execution_token（§5-3）

> **用途**：联调 / PR / FE-5 烟测留证索引；**非**实现真值（真值见 `docs/tasks/done/task_chatbi_v3_lowconf_rag_preview_v1.md`、SPEC、pytest）。
> **采集**：2026-05-31 · 后端 `task/chatbi-v3-lowconf-rag-preview` @ `b297c94` · Ink FE `72f8f0c`
> **freeze_id**：`CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31`

## 环境要点

| 项 | 值 |
|----|-----|
| 开关 | `CHATBI_USE_AGENT=1` · `CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` · `CHATBI_V3_PLAN_PREVIEW_CONFIRM=1` |
| 意图 | 低置信 **`rag_search`**（`prefer=auto`） |
| 契约 C1 | `rewrite_query` · `planned_top_k` · `preview_headlines`（可选） |

## 两轮预期（后端 pytest 钉住）

| 轮次 | 观测 | 测例 |
|------|------|------|
| 1 预览+澄清 | `agent.plan.preview`（`tool=rag_search`）→ `agent.clarify`；`router.decision.final_mode=rag` | `test_v3_rag_plan_preview_json_includes_rewrite_query` |
| 2 令牌放行 | body 含 `plan_execution_token`；无 `agent.clarify`；含 `rag.sources` | `test_v3_rag_plan_execution_token_json_bypasses_clarify` |

SSE parity：`test_v3_rag_plan_preview_sse_parity`

## Ink 全栈留证

- 前端 task：`ai-ink-brain/content/tasks/active/task_chatbi_v3_lowconf_rag_preview_frontend_v1.md`
- 前端 50：`content/tasks/reinspect_results/reinspect_chatbi-v3-lowconf-rag-preview-frontend_20260531_v1.md`
- 对照 5-2 SQL 样本：[`../chatbi-v3-lowconf-sql-preview/`](../chatbi-v3-lowconf-sql-preview/)

## 关联

- `docs/tasks/done/task_chatbi_v3_lowconf_rag_preview_v1.md`
- `docs/tasks/reinspect_results/reinspect_chatbi-v3-lowconf-rag-preview_20260531_v1.md`

> **补录**：浏览器导出的 `round*_timeline.json` 与 `screenshots/` 可在联调后追加至本目录（不阻塞后端关账）。
