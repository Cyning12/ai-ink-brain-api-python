# 标准样本 · ChatBI V3 低置信 RAG 预览 + plan_execution_token（§5-3）

> **用途**：联调 / PR / FE-5 烟测留证；**非**实现真值（真值见 `docs/tasks/done/task_chatbi_v3_lowconf_rag_preview_v1.md`、SPEC、pytest）。
> **采集**：2026-05-31 · 后端 `b297c94` · Ink FE `72f8f0c` · **浏览器 真机**（2026-06-01 补截图与 E2E Timeline）
> **freeze_id**：`CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31`

## 环境要点（路线 A · 5-3）

| 项 | 值 |
|----|-----|
| 问句（成功预览） | `2026-04-28日记的大致内容` |
| session_id | `791291bd-92f8-4936-b698-28e8fb4025e9` |
| round1 run_id | `085082ae-6386-4f43-a60f-f11b4fffcd65`（14 条 SSE） |
| round2 run_id | `df8593fb-1dc1-4154-9349-6c68bd6e7b08`（浏览器全链 34 条；JSON 内为关键路径摘录） |
| 开关 | `CHATBI_USE_AGENT=1` · `CHATBI_V2_INTENT_LLM=1` · `CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` · `CHATBI_V3_PLAN_PREVIEW_CONFIRM=1` · **`INTENT_MIN_CONFIDENCE=1.0`（仅联调）** |

联调通过后请将 `INTENT_MIN_CONFIDENCE` 改回 **0.6** 并重启 uvicorn。

## 截图

| 文件 | 说明 |
|------|------|
| [`screenshots/ui-confirm-rag-preview-card.png`](screenshots/ui-confirm-rag-preview-card.png) | 确认卡「按预览执行」+ `rewrite_query` |
| [`screenshots/timeline-round1-14-events-preview.png`](screenshots/timeline-round1-14-events-preview.png) | 首轮 ~14 条：`plan.preview` + `clarify` |
| [`screenshots/timeline-rag-preview-clarify-execution-path.png`](screenshots/timeline-rag-preview-clarify-execution-path.png) | 执行链含 preview / clarify 片段 |

## 两轮 Timeline（真机）

| 轮次 | 文件 | 关键观测 |
|------|------|----------|
| 1 预览+澄清 | [`round1_preview_clarify_timeline.json`](round1_preview_clarify_timeline.json) | 14 条 · `tool=rag_search` · `rewrite_query` · `plan_execution_token` · `agent.clarify` · **无** `tool.call` |
| 2 令牌放行 | [`round2_token_bypass_execute_timeline.json`](round2_token_bypass_execute_timeline.json) | token 校验 · **无** `clarify` · `rag_search` · `RAG_GENERATE_UNCERTAIN` · fallback `direct_answer` · **无** `rag.sources` |

**路线 B 对照**（未开 `INTENT_MIN_CONFIDENCE=1.0` 或未重启）：~31–34 条、直接 `tool.call.*`，无确认卡 — 非本目录样本目标。

## 已知问题（答案质量）

见 [`NOTES-future-diary-llm-date.md`](NOTES-future-diary-llm-date.md)：**未来日记**误判 — 估计 RAG/直接回答 **未给 LLM 当前日期与 KB 边界提示词**，非 §5-3 闸门缺陷。

## 再生（TestClient stub · 可选）

```bash
cd ai-ink-brain-api-python
python scripts/export_lowconf_rag_diary_sample.py
```

> 脚本导出为 pytest 同形 stub；**本目录主 JSON 已为浏览器 E2E**（round1 全量 14 条；round2 关键路径 + `event_count_full_capture: 34`）。若你本地仍保留浏览器导出的完整 34 条 JSON，可覆盖 `round2_token_bypass_execute_timeline.json` 的 `timeline` 数组。

## 关联

- `docs/tasks/done/task_chatbi_v3_lowconf_rag_preview_v1.md`
- `docs/tasks/reinspect_results/reinspect_chatbi-v3-lowconf-rag-preview_20260531_v1.md`
- 对照 5-2：[`../chatbi-v3-lowconf-sql-preview/`](../chatbi-v3-lowconf-sql-preview/)
- Ink FE：`ai-ink-brain` · `72f8f0c`
