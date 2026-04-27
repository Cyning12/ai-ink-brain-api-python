## Task 03：Supabase 混合检索（Hybrid Search）可验收任务

### 任务目标
- 将单一向量检索升级为 **“向量（Vector）+ 全文检索（FTS Keyword）”双路并行召回**。
- 使用 **RRF（Reciprocal Rank Fusion）** 做结果融合与统一排序。
- **接口对前端透明**：`POST /api/py/chat` 入参/出参保持不变（仍为流式文本）。
- 保持可观测性：每轮对话将 `retrieved_context`、`latency`、融合信息写入 `rag_conversation_logs`。

### 范围与约束
- **数据库**：Supabase（PostgreSQL + pgvector），向量检索仍使用 `match_documents`（Cosine Distance）。
- **FTS**：为 `public.documents` 增加 `fts_tokens tsvector` + GIN 索引，并保证写入/更新时自动维护。
- **融合**：RRF 公式固定为 `1 / (60 + rank)`，rank 从 1 开始。
- **元数据**：融合后的命中结果必须保留 `metadata`（至少 `filename / original_link / page_number / section_header / chunk_index` 等既有字段）。

---

## 1) 数据库层任务（Supabase SQL）

### 1.1 需要执行的 SQL
在 Supabase Dashboard → SQL Editor 执行：
- `supabase/sql/hybrid_search.sql`

该脚本应完成：
- `ALTER TABLE public.documents ADD COLUMN fts_tokens tsvector`
- 创建 `GIN(fts_tokens)` 索引
- 创建触发器：在 `content` insert/update 时自动维护 `fts_tokens`
- 回填历史数据：将空的 `fts_tokens` 填充为 `to_tsvector(...)`
- 创建 RPC：
  - `keyword_documents(query_text, match_count)`：Keyword 路召回
  - `refresh_documents_fts_tokens_for_paths(relative_paths[])`：按 ingest 的 relativePath 刷新 fts_tokens（兜底）

> 说明：FTS 配置建议使用 `simple`（更通用，适配中英文混合）；若后续引入中文分词扩展，可再迭代配置与查询函数。

### 1.2 验收（数据库）
满足以下任一方式即可验收：
- **结构验收**：
  - `public.documents` 存在 `fts_tokens` 列
  - 存在 GIN 索引（例如 `documents_fts_tokens_gin`）
  - 存在触发器（insert/update content 时会更新 `fts_tokens`）
- **功能验收**：
  - 执行 `select public.keyword_documents('test', 5);` 能返回结构为 `id/content/metadata/score` 的结果（有命中时）。

### 1.3 回滚（数据库）
若需要回滚 Hybrid Search（不建议频繁做），按需执行：
- `drop trigger if exists trg_documents_fts_tokens_update on public.documents;`
- `drop function if exists public.documents_fts_tokens_update();`
- `drop function if exists public.keyword_documents(text, integer);`
- `drop function if exists public.refresh_documents_fts_tokens_for_paths(text[]);`
- `drop index if exists public.documents_fts_tokens_gin;`
- `alter table public.documents drop column if exists fts_tokens;`

---

## 2) 后端开发任务（api/）

### 2.1 Ingest 入库阶段（`api/ingest_pipeline.py`）
要求：
- 当 chunk 写入 `public.documents` 后，**确保 `fts_tokens` 已被填充**。
- 验收策略：
  - 优先依赖 SQL 触发器自动维护；
  - 同时允许在 ingest 后调用 Supabase RPC 进行兜底刷新（避免库未迁移或历史数据出现空值）。

### 2.2 Chat 检索阶段（`api/index.py`）
要求实现双路召回与融合：
- **路 A（Vector）**：保持现有 `match_documents(query_embedding, match_count, match_threshold)`。
- **路 B（Keyword）**：使用 FTS（通过 RPC `keyword_documents(query_text, match_count)` 或 SQL 等价逻辑 `fts_tokens @@ plainto_tsquery/websearch_to_tsquery`）。
- **融合（RRF）**：
  - 对两路结果分别按 rank 计算 `1/(60+rank)`；
  - 同一 `id` 的结果累加得分得到 `fused_score`；
  - 按 `fused_score` 降序取 TopN（建议 22 左右，需与 Context Window 控制一致）。
- **透明接口**：
  - `/api/py/chat` 不新增必填字段，不破坏现有前端调用。

### 2.3 可观测性与日志（必须）
每轮对话写入 `public.rag_conversation_logs`：
- `retrieved_context`：应包含融合后命中片段（含 `metadata`、截断后的 `content`），并能看到融合相关字段（如 `fused_score` / `rrf`）。
- `metadata.latency_ms`：至少包含 history / rewrite / embedding / retrieve / generate 的毫秒耗时。

---

## 3) 端到端验收用例（E2E）

### 3.1 前置条件
- Supabase 已执行 `hybrid_search.sql`
- `documents` 表内存在内容（可通过 ingest 或已有数据）
- 服务端环境变量正确（Supabase/SiliconFlow/Admin Secret）

### 3.2 验收用例（建议最少跑 3 条）
1) **关键字强匹配用例（验证 Keyword 路有效）**
- 输入：包含明确关键词（例如某篇标题/文件名内的特征词）
- 预期：
  - `rag_conversation_logs.retrieved_context` 中能看到 keyword 命中的记录（至少 `rrf.keyword_rank` 或 keyword 相关字段存在）
  - 最终回答引用/围绕关键词相关片段

2) **语义近似用例（验证 Vector 路仍有效）**
- 输入：同义改写/不含原词的提问
- 预期：
  - `retrieved_context` 中存在 vector 命中（`rrf.vector_rank` 或 similarity 字段存在）

3) **混合优势用例（验证 RRF 融合）**
- 输入：同时包含“关键词 + 语义描述”的问题
- 预期：
  - `retrieved_context` 中存在 `fused_score`，并且排序前列能体现两路共同贡献（同时带 vector_rank 与 keyword_rank 的项，其 fused_score 应更高）

### 3.3 通过标准（Pass/Fail）
- **Pass**：三条用例均能在 `rag_conversation_logs` 中观察到融合痕迹（`fused_score/rrf`）且回答质量明显不低于纯向量版本。
- **Fail**：Keyword 路完全无命中/无融合字段、或接口行为发生破坏（非流式、报 4xx/5xx、前端无法消费）。

---

## 4) 对前端的交付物
- 对接文档输出到前端仓库：`content/tasks/task_03_hybrid_search_backend_frontend_contract.md`
- 文档需包含：接口不变说明、需要执行的 SQL 清单、RRF 融合解释、排障方式（查 `rag_conversation_logs`）。
