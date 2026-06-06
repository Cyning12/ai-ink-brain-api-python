> **状态**：`done`  
> **归档说明**：2026-06-06 由 P2 消化；`metadata.date_norm` 归一化与结构化召回已落地，见 `api/ingest_pipeline.py`、`api/unified_chat.py`。

# Task：B1｜metadata 归一化 + 结构化召回（v1）

## 背景与目标

对齐 `SPEC-08`。当前 RAG 已能召回 `2026-04-14` 形式，但像「四月十四号那天写了什么」这类不含标准日期 token 的问法仍容易 0 hits。

本任务目标是在不重算 embedding、不改 content 的前提下，增强“按日期/文件”定位能力：

- 写入侧：补齐 `metadata.date_norm`（`YYYY-MM-DD`）
- 检索侧：当 query 命中日期信息时，先做结构化召回（metadata 精确匹配），确保稳定命中 diary 文档

## 范围

- Python ingest：写入 `public.documents` 时补齐 `metadata.date_norm`（必要时 `slug_norm`）
- Unified RAG：日期类 query 增加结构化召回路径，并与 vector/keyword hits 融合

## 非范围

- 不重算 embedding
- 不全量清洗历史 content

## 依赖与引用

- `docs/tasks/specs/SPEC-08-rag-b1-metadata-normalization-and-structured-recall.md`
- 入口：`api/ingest_pipeline.py`、`api/unified_chat.py`

## 验收标准

- [ ] ingest 新写入的 diary 文档 metadata 含 `date_norm=YYYY-MM-DD`
- [ ] 查询 `四月十四号那天写了什么` 能命中 `diary/2026-4-14.md`（至少 sources 出现该文档）
- [ ] `pytest` 全绿

