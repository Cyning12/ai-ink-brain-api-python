# SPEC-07：RAG Keyword（FTS）宽松化与日期查询归一化（v1）

## 背景

在 `public.documents` 已存在目标文档（如 `diary/2026-4-14.md`）的情况下，FTS/keyword 仍可能出现 “0 rows / 0 hits”，典型触发：

- 日期格式差异：`2026-04-14` 能命中，但 `2026-4-14` 可能 0 行（`'04' != '4'` 的 token 差异）
- `plainto_tsquery` 的 **AND** 语义：`2026-04-14 日记` 要求“日期 + 日记”同时出现，正文不含“日记”时直接 0 行

## 目标

1) Supabase 侧 keyword RPC 使用更贴近“搜索框”的 query 解析（`websearch_to_tsquery`）
2) Python 侧在调用 keyword RPC 前对**日期**做归一化与候选扩展（query-side），显著提升 diary/日志类检索稳定性

## 范围 / 非范围

- **范围**
  - Supabase SQL：`public.keyword_documents` 使用 `websearch_to_tsquery('simple', query_text)`
  - Python：`api/unified_chat.py` 的 RAG keyword 召回参数改为“日期候选 OR 表达式”
- **非范围**
  - 不做历史文档全量清洗/重写
  - 不改 embedding 模型与向量检索 RPC

## 设计

### 1) Supabase：keyword RPC（FTS）宽松化

- 将：
  - `ts_rank_cd(fts_tokens, plainto_tsquery('simple', query_text))`
  - `fts_tokens @@ plainto_tsquery('simple', query_text)`
- 替换为：
  - `websearch_to_tsquery('simple', query_text)`

备注：仓库内 `supabase/sql/hybrid_search.sql` 已采用 `websearch_to_tsquery`；若线上仍是 `plainto_tsquery`，需执行该迁移文件以对齐。

### 2) Python：查询侧日期归一化与候选扩展（Keyword Only）

当 query 检测到日期形态（支持 `YYYY-M-D` / `YYYY-MM-DD` 以及 `-` `/` `.`）：

- 生成候选（去重）：
  - `YYYY-MM-DD`（补零）
  - `YYYY-M-D`（去零）
  - 分隔符变体：`-` `/` `.` 与空格
- 将候选拼为 websearch 的 OR 表达式（带双引号）：
  - `"2026-04-14" OR "2026-4-14" OR "2026/04/14" ...`

仅用于 keyword RPC 的 `query_text`，不改变原始 query（用于展示/生成）。

## 验收标准

- [ ] Supabase `public.keyword_documents` 使用 `websearch_to_tsquery`
- [ ] 输入 `2026-4-14 的日记记录了什么` 时，keyword 召回不再因前导 0 造成 0 hits（至少命中 diary 文档）
- [ ] Unified Chat 的 `rag.retrieve` 事件中仍能看到 raw/rewrite 的命中统计（便于回归）

