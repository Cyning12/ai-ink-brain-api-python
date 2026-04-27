# Task 05：Rewrite 可观测性增强（raw vs rewrite 召回对比 + 关键实体丢失判定）

状态：pending  
范围：仅后端 `ai-ink-brain-api-python`  

## 背景与目标

当前排查 “rewrite 导致检索变差/丢关键 token（如 task_04/文件名/日期）” 时，需要频繁去 Supabase 查询 `documents` 或翻 `rag_conversation_logs`，成本高且不直观。

目标：

- 在每次 `/api/py/chat` 请求中，记录 **raw query** 与 **rewrite query** 的对比指标，回答：
  - rewrite 是否降低了召回？
  - 是否丢失关键实体（日期/数字/文件名/任务编号/专有名词等可配置规则）？
- 将对比指标写入 `public.rag_conversation_logs.metadata`，并在 `DEBUG_RAG=1` 时输出可读摘要（减少查库频次）。

> 说明：本任务不改变对外 API 契约；仅增加日志字段与 debug 输出。召回策略的升级（方案 1：双查询并行融合）另起任务。

## 范围 / 非范围

### 范围
- `POST /api/py/chat`：新增 query 对比日志（raw vs rewrite）与关键实体丢失判定
- `DEBUG_RAG` 模式下：输出一条聚合摘要（console）

### 非范围
- 不修改 Supabase SQL（不新增表/函数）
- 不改变 RRF 融合逻辑（仍以现有检索链路为准）
- 不新增前端 UI（前端 debug 展示由前端任务处理）

## 设计（日志字段与含义）

新增字段建议落在：

- `rag_conversation_logs.metadata.match.query_compare`

字段（简易版对齐需求）：

- `query_raw`: 原始问题（同 `payload.query`，此处冗余存储便于单点读取）
- `query_rewrite`: 改写后问题（同 `payload.rewritten_query`）
- `recall_raw_count`: 原始 query 的召回数量（**Keyword/FTS 路**为主）
- `recall_rw_count`: 改写 query 的召回数量（Keyword/FTS 路）
- `recall_raw_top1_score`: 原始 query 的 Top1 分数（Keyword 路 `score`）
- `recall_rw_top1_score`: 改写 query 的 Top1 分数（Keyword 路 `score`）
- `is_key_entity_lost`: 是否丢失关键实体（raw 中存在但 rewrite 中缺失）

扩展字段（推荐，便于调试与后续做方案 2/1）：

- `key_entities.tokens_raw`: 规则提取到的 raw token 列表（去重保序）
- `key_entities.tokens_rewrite`: rewrite token 列表
- `key_entities.missing`: raw - rewrite 的缺失 token
- `key_entities.lost_types`: 可选（按规则分类：date/file/task/number/...）
- `score_type`: `"fts_score"`（显式说明 top1_score 的含义，避免与 vector similarity 混淆）

> 注：如需记录 Vector 路的 Top1 similarity，可另加 `vector_top1_similarity`，但不与上述 `top1_score` 混用。

## 关键实体（token）规则

规则集中管理，便于增删改：

- 文件名/后缀：`*.md/mdx/pdf/txt/...`
- task 编号：`task_04 / task-04 / Task 04`
- 日期：`YYYY-MM-DD`（含 `2026-4-14.md`）
- （可选）数字串、路径片段、代码符号等

## 验收标准

- [ ] `POST /api/py/chat` 的 `rag_conversation_logs.metadata.match.query_compare` 中包含上述字段
- [ ] 对于输入包含 `task_04` / 文件名 / 日期 的问题：
  - [ ] 若 rewrite 丢失 token，`is_key_entity_lost=true` 且 `missing` 包含对应 token
- [ ] `DEBUG_RAG=1` 时，终端输出包含一行 query_compare 摘要（raw/rewrite counts、top1 分数、是否丢失 token）
- [ ] 不影响现有流式输出与 sources 机制

## 实现备忘

建议实现步骤：

1. 抽取/复用 token 规则（可复用 `api/keyword_fallback.py` 的锚点 token 规则并扩展）
2. 在检索阶段，对 Keyword 路分别执行：
   - `keyword_documents(query_raw, ...)`
   - `keyword_documents(query_rewrite, ...)`
   记录 count 与 top1 score（此处仅用于日志，不改变最终召回策略）
3. 在写库 payload 时写入 `metadata.match.query_compare`

