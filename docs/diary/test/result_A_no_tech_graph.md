# Prompt A（禁用图谱）— 全量理解后端结果

> 生成时间：2026-04-27T22:28+08:00（约）
> 约束：未读取 `docs/_tech_graph/` 下任何文件；全部事实来自代码、SQL、配置、测试。

---

## 1. 摘要

`ai-ink-brain-api-python` 是 Ink-Brain 博客的 **RAG / Embedding / Chunking / Retrieval / ingest** 服务端（FastAPI）。核心能力：
- 对 Markdown 日记/文档做分块、SiliconFlow Embedding、写入 Supabase `documents`；
- 对 Python 代码做 AST 解析、分块、写入 `code_chunks`；
- 提供 **Hybrid 检索**（Vector Cosine + FTS Keyword + RRF 融合）与 **Text2SQL**（基于 DDL 样例的 SQL 生成与执行）；
- 支持 **Unified Chat**（RAG / Text2SQL / no_data 三模式路由）与 **SSE 流式事件链**；
- 全链路可观测：每轮请求写入 `rag_conversation_logs`，含 latency、命中数、rewrite 对比、keyword fallback 等元数据。

---

## 2. 入口与模块地图

### 2.1 FastAPI App 与路由注册

| 文件 | 职责 |
|------|------|
| `main.py` | 本地 `uvicorn main:app` 入口，仅转发 `api.index:app` |
| `api/index.py` | FastAPI `app` 创建、全部路由注册、RAG 主链路（`/api/py/chat` 流式）、admin ingest/sync |
| `api/unified_chat.py` | `handle_unified_chat` / `handle_unified_chat_stream`（JSON / SSE） |
| `api/chain_chat.py` | `handle_chain_chat`（v1 仅 Text2SQL events） |
| `api/text2sql_api.py` | `handle_text2sql_chat`（独立 Text2SQL 端点） |
| `api/code_retrieval.py` | `handle_code_query` / `handle_code_search`（代码 RAG） |

### 2.2 核心模块职责

| 文件 | 职责 |
|------|------|
| `api/rag_env.py` | `.env` 加载（`REPO_ROOT/.env.local` → `.env`）；Supabase/SiliconFlow 选择器；Embedding 参数封装 |
| `api/database_manager.py` | `SupabaseManager`：异步读写 `rag_conversation_logs`（`save_debug_log` / `get_chat_history` / `list_session_turns`） |
| `api/ingest_pipeline.py` | Markdown 分块（`chunk_text_by_chars`）、Embedding 批量调用、写入 `documents`；内存任务队列（`JOBS`） |
| `api/code_ingest.py` | 代码解析 → `IngestChunk` → Embedding → 写入 `code_chunks` |
| `api/code_parser.py` | Python AST 解析，产出 `ParsedChunk`（module_doc / function / class / method） |
| `api/hybrid_fusion.py` | RRF 融合：`fuse_hits_rrf(vector_hits, keyword_hits)`，常数 `RRF_K = 60` |
| `api/rag_recall_tools.py` | `rpc_execute_with_retry`（Supabase RPC 重试）、`structured_recall_by_date`（日期结构化召回）、i18n glossary 扩展、keyword query 构造 |
| `api/query_rewrite.py` | `rewrite_query_with_history`（基于 session 历史的查询改写，LLM 调用） |
| `api/keyword_fallback.py` | 当 rewrite 导致 keyword 命中不足时，用锚点 token / normalized query 回退检索 |
| `api/intent_router.py` | `decide_intent`：规则候选（rag / text2sql / no_data / tool）+ DDL/FTS 证据校验 |
| `api/text2sql_core.py` | Text2SQL 核心：`is_text2sql_intent`、`validate_sql_readonly`、`execute_select_sql`（psycopg）、`build_sql_prompt`、`llm_generate_sql`、`llm_summarize` |
| `api/text2sql_store.py` | `get_text2sql_store`：从 `docs/text2sql/v1/sql/supabase_init.sql` + samples 构建 Faiss/Fallback 检索库 |
| `api/rag_logging.py` | `build_rag_match_meta`、`build_retrieved_context_for_log`、`summarize_hits_brief` |

### 2.3 配置与 SQL

| 文件 | 职责 |
|------|------|
| `.env.example` | 环境变量模板（Embedding 厂商、Supabase、Admin Secret、阈值等） |
| `requirements.txt` | `fastapi uvicorn openai supabase python-dotenv pytest requests faiss-cpu numpy psycopg[binary]` |
| `supabase/sql/init.sql` | 建 `public.documents`（`vector(1024)`）、`match_documents` RPC、HNSW 索引、RLS |
| `supabase/sql/hybrid_search.sql` | 增 `fts_tokens` 列 + GIN 索引 + 触发器；`keyword_documents` RPC；`rag_fts_alias_text`（日期/版本/分隔符/CamelCase 别名）；`refresh_documents_fts_tokens_for_paths` |
| `supabase/sql/code_chunks.sql` | 建 `public.code_chunks`（`vector(1024)` + `fts_tokens`）；`match_code_chunks` / `keyword_code_chunks` / `refresh_code_chunks_fts_tokens_for_paths` |
| `supabase/sql/create_rag_conversation_logs.sql` | 建 `public.rag_conversation_logs`（uuid PK, session_id, query, rewritten_query, retrieved_context, response, metadata, created_at） |
| `supabase/sql/patch_match_documents_threshold.sql` | 旧版 `match_documents(vector, integer)` 升级为带 `match_threshold` 的三参数版本 |

---

## 3. 关键链路

### 3.1 RAG 主链路（`POST /api/py/chat` → 流式）

入口：`api/index.py:chat()`

1. **鉴权**：`_require_auth()` — 检查 `Authorization: Bearer <token>` / `x-blog-admin-token` / `x-admin-token`，对比 `NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET` / `API_KEY`（`hmac.compare_digest`）。
2. **解析请求**：`messages[]` + `session_id`；取最后一条 user text 作为 `query`。
3. **读历史**：`SupabaseManager.get_chat_history(session_id, limit=5)` → 用于 rewrite。
4. **Query Rewrite**：`rewrite_query_with_history(oai, query, history, chat_model)`（`api/query_rewrite.py`）。失败则回退原 query。
5. **Embedding**：`oai.embeddings.create(model=SILICONFLOW_EMBEDDING_MODEL, input=[embed_input])`。Qwen3 模型带 `dimensions=1024`。
   - 失败降级：`vec = None`，后续走 keyword-only（`api/index.py:684`）。
6. **检索（Hybrid）**：
   - Vector 路：`sb.rpc("match_documents", {query_embedding, match_count=10, match_threshold})`（默认 threshold=0.3）。
   - Keyword 路：`sb.rpc("keyword_documents", {query_text, match_count=12})`。
   - 可观测：同时用 raw query 与 rewritten query 各跑一次 keyword，记录 `query_compare_meta`（`recall_raw_count` / `recall_rw_count` / `is_key_entity_lost` 等）。
   - Keyword Fallback：若 rewrite 后 keyword 命中不足，触发 `run_keyword_fallback()`（`api/keyword_fallback.py`），用锚点 token / normalized query 再检索。
   - 融合：`fuse_hits_rrf(vector_hits, keyword_hits, max_total=22)`。
7. **日期锚点注入**：若 query 含日期，调用 `fetch_date_anchor_hits()` 按 `metadata->>slug` / `content ilike 'Title: ...'` 精确匹配，优先插入结果头部（`merge_hits_anchors_first`）。
8. **构造 Prompt**：`build_system_prompt(context)` → 要求 LLM 优先依据 `[Document Context]` 片段作答，并识别 `Title: 某文件名.md` 为日期笔记。
9. **流式生成**：`oai.chat.completions.create(..., stream=True)`，逐 token yield。
   - 末尾追加 `---RAG_SOURCES_JSON---\n{json}`（`SOURCES_JSON_SEPARATOR`）。
   - 同时尝试写入 `x-sources` Header（percent-encoded JSON），超限（默认 6000 字符）则丢弃 Header，依赖流尾 JSON。
10. **后台写日志**：`background_tasks.add_task(save_log_after_stream)` → `SupabaseManager.save_debug_log()` 写入 `rag_conversation_logs`，含 latency（history/rewrite/embedding/retrieve/generate）、models、match meta、keyword fallback、query compare、i18n expand 等。

失败路径：
- 鉴权失败 → 401/500
- JSON 解析失败 → 400
- 缺少 `SILICONFLOW_API_KEY` → 500
- 缺少 Supabase 配置 → 500
- Embedding 失败 → 降级 keyword-only，不中断流程
- RPC 失败 → `try/except` 捕获，`hits=[]`，继续生成（可能上下文为空）
- 流生成失败 → yield `[错误] 对话生成失败: ...`
- 客户端断开 → `GeneratorExit` 被捕获，避免 `RuntimeError`

### 3.2 Unified Chat 链路（`POST /api/py/unified/chat` 与 `/stream`）

入口：`api/unified_chat.py`

1. **鉴权**：`_require_unified_auth()`（同 `_require_auth` 逻辑）。
2. **Intent 路由**：`decide_intent(query, prefer)`（`api/intent_router.py`）。
   - 规则候选：no_data（润色/翻译/写作等关键词）→ text2sql（查询/统计/多少等）→ rag（默认）。
   - 证据校验：DDL evidence（`text2sql_store.search`）与 FTS evidence（`keyword_documents`）。
   - 保护：text2sql 无 DDL evidence → fallback 到 rag / no_data；rag 无 FTS evidence → fallback 到 no_data / text2sql。
3. **三模式分支**：
   - `no_data`：直接调用 LLM 生成回答（无检索）。
   - `text2sql`：retrieve DDL/examples → `llm_generate_sql` → `validate_sql_readonly` → `execute_select_sql`（psycopg，只读 SELECT）→ `llm_summarize`。
   - `rag`：rewrite → embed → retrieve（vector + structured_recall_by_date + keyword raw + keyword rewrite，四层 RRF 融合）→ `llm_generate_answer`。
4. **事件输出**：
   - JSON 模式：返回 `{ok, run_id, session_id, mode, events[]}`，events 包含 `router.decision`、`tool.call.start/end`、`rag.sources`、`sql.result`、`assistant.message`、`latency`、`error` 等。
   - SSE 模式：每条 event 为 `event: chain\ndata: {...}\n\n`，最后一条 `event: done\ndata: {ok, mode, run_id, request_id, session_id}`。

失败路径：
- 各阶段 `try/except` 捕获，生成 `error` event，不抛 500（除非鉴权/JSON 解析）。
- Text2SQL 生成空 SQL / 执行失败 → 返回 `error` event + `ok=False`。
- RAG retrieve 失败 → `hits=[]`，继续生成（可能回答“无资料”）。

### 3.3 Text2SQL 独立链路（`POST /api/py/text2sql/chat`）

入口：`api/text2sql_api.py:handle_text2sql_chat()`

1. 鉴权 → 解析 `query`。
2. `is_text2sql_intent(query)` 过滤：非查数类问题直接返回 `mode=non_text2sql`。
3. `get_text2sql_store().search(query, top_k=TEXT2SQL_RETRIEVE_TOPK)` 检索 DDL + examples（本地 Faiss/Fallback，基于 md5 哈希向量）。
4. `build_sql_prompt` → `llm_generate_sql` → `validate_sql_readonly`（禁止 INSERT/UPDATE/DELETE/ALTER/DROP 等，仅允许 SELECT/WITH）。
5. `execute_select_sql(sql, limit_rows=TEXT2SQL_MAX_ROWS)`：通过 `psycopg` 直连 `TEXT2SQL_DATABASE_URL`，强制加 LIMIT，超时 8s。
6. 聚合结果单行单列时，`_try_summarize_aggregate` 做确定性总结（避免 LLM 误判）。
7. `build_summary_prompt` → `llm_summarize`。
8. 返回 `{ok, mode, answer, sql, columns, rows, retrieved, errors, latency_ms}`。

失败路径：
- store 初始化失败 → 500
- SQL 生成失败 → `gen_err` 记录，sql 为空
- SQL 执行失败 → `exec_err` 记录，rows 为空
- summarize 失败 → 兜底回答（`未查到数据` 或 `查询返回 N 行结果`）

### 3.4 Ingest 链路（`POST /api/py/admin/ingest`）

入口：`api/index.py:py_admin_ingest()`

- `type=markdown`：
  1. `get_all_markdown_chunks()`（`api/ingest_pipeline.py`）扫描 `CONTENT_ROOT`（或 `REPO_ROOT/content`）下的 `.md`/`.mdx`。
  2. `chunk_text_by_chars(raw, chunk_size=512, overlap=50)` 按字符滑动窗口分块。
  3. `build_enhanced_chunk_text()` 包装为 `[Document Context]\nTitle: ...\nDate: ...\nCategory: ...\n---\nContent: ...`
  4. `delete_documents_by_relative_paths()` 先删后插（幂等）。
  5. `embed_texts_batch()` 批量 Embedding（batch=32）。
  6. `sb.table("documents").insert(slice)` 批量写入（batch=80）。
  7. `refresh_documents_fts_tokens_for_paths()` 兜底刷新 fts_tokens。
- `type=code`：
  1. `get_all_code_chunks()`（`api/code_ingest.py`）调用 `parse_project()`（`api/code_parser.py`）AST 解析 Python 文件。
  2. `build_enhanced_code_text()` 包装为 `[Code Context]\nFile: ...\nModule: ...\nLines: ...\nType: ...\nName: ...\nSignature: ...\n---\nContent: ...`
  3. 先删后插 `code_chunks`；兜底刷新 `refresh_code_chunks_fts_tokens_for_paths()`。

失败路径：
- 维度不匹配 → 400（`Unsupported` / `维度` 关键字）
- 其他异常 → 500，返回 `error` 字段

### 3.5 Code RAG 链路（`POST /api/py/code/query` 与 `/search`）

入口：`api/code_retrieval.py`

- `code_query`：
  1. 鉴权（优先 `API_KEY`，兼容 admin_secret）。
  2. `rewrite_query_with_history`（若带 `session_id`）。
  3. Embedding → `match_code_chunks`（vector）+ `keyword_code_chunks`（FTS）。
  4. keyword 兜底：`_identifier_only_query` → `_keyword_light_query` → 全表抽样（embedding 不可用时）。
  5. `fuse_hits_rrf` → `_passes_code_filters`（file_path / chunk_type / module）→ `_boost_by_query_name`（query 含符号名时加分）。
  6. 返回 `{ok, query, rewritten_query, chunks[], sources[], retrieval_meta}`。
- `code_search`：纯 metadata 过滤（`metadata->>name` / `file_path` / `chunk_type` / `module`），无向量/FTS，返回 `{ok, chunks[], sources[], retrieval_meta}`。

### 3.6 Admin Sync 链路（`POST /api/py/admin/sync`）

入口：`api/index.py:py_admin_sync_post()` / `py_admin_sync_get()`

- `POST`：创建内存 job（`JOBS` dict），`background_tasks` 异步执行 `run_sync_job_sync()`。
- `GET`：按 `jobId` 查询 job 状态（`queued` / `running` / `succeeded` / `failed`）。
- `run_sync_job_sync` 调用 `sync_content_to_vector()`（`api/ingest_pipeline.py`）：与 `process_markdown_files` 类似，但按 slug 删除（而非 relativePath），逐 chunk 单条 embedding（非 batch）。

---

## 4. 数据结构与存储

### 4.1 Supabase 表结构（以 SQL 为准）

#### `public.documents`

| 列 | 类型 | 说明 |
|----|------|------|
| `id` | `bigserial primary key` | 自增 |
| `content` | `text not null` | 分块正文（含 `[Document Context]` 前缀） |
| `metadata` | `jsonb not null default '{}'` | 含 `category`, `slug`, `slug_norm`, `date_norm`, `mtime`, `lastModified`, `relativePath`, `chunk_index`, `filename`, `original_link`, `page_number`, `section_header` |
| `embedding` | `vector(1024) not null` | SiliconFlow Embedding（默认 1024 维） |
| `fts_tokens` | `tsvector` | 由触发器自动维护（`hybrid_search.sql`） |
| `created_at` | `timestamptz not null default now()` | — |

索引：`documents_embedding_hnsw`（HNSW, `vector_cosine_ops`）、`documents_metadata_filename`（expression index）、`documents_fts_tokens_gin`（GIN）。

#### `public.code_chunks`

| 列 | 类型 | 说明 |
|----|------|------|
| `id` | `uuid primary key default gen_random_uuid()` | — |
| `content` | `text not null` | 代码分块正文（含 `[Code Context]` 前缀） |
| `metadata` | `jsonb not null default '{}'` | 含 `category`, `slug`, `relativePath`, `chunk_index`, `filename`, `file_path`, `start_line`, `end_line`, `chunk_type`, `name`, `signature`, `module` 等 |
| `embedding` | `vector(1024) not null` | — |
| `fts_tokens` | `tsvector` | 触发器维护 |
| `created_at` | `timestamptz not null default now()` | — |

索引：`code_chunks_embedding_hnsw`、`code_chunks_metadata_filename`、`code_chunks_fts_tokens_gin`。

#### `public.rag_conversation_logs`

| 列 | 类型 | 说明 |
|----|------|------|
| `id` | `uuid primary key default gen_random_uuid()` | — |
| `session_id` | `varchar not null` | 会话标识 |
| `query` | `text not null` | 原始用户问题 |
| `rewritten_query` | `text` | 改写后查询 |
| `retrieved_context` | `jsonb` | 命中片段摘要（`build_retrieved_context_for_log`） |
| `response` | `text` | 最终回答 |
| `metadata` | `jsonb` | latency、models、match、keyword fallback、query compare、i18n expand 等 |
| `created_at` | `timestamptz not null default now()` | — |

索引：`rag_conversation_logs_session_id_idx`、`rag_conversation_logs_created_at_idx`。

### 4.2 核心 Python 数据结构（dataclass）

| 类 | 文件 | 字段 |
|----|------|------|
| `IngestMeta` | `api/ingest_pipeline.py` | `category, slug, last_modified, relative_path, chunk_index` |
| `IngestChunk` | `api/ingest_pipeline.py` | `content, metadata: IngestMeta` |
| `CodeIngestMeta` | `api/code_ingest.py` | `file_path, start_line, end_line, chunk_type, name, signature, module`（动态挂载到 `IngestMeta`） |
| `ParsedChunk` | `api/code_parser.py` | `name, chunk_type, signature, docstring, body, file_path, relative_path, module, start_line, end_line` |
| `KeywordFallbackConfig` | `api/keyword_fallback.py` | `enabled, min_hits, match_count, max_tokens` |
| `KeywordFallbackResult` | `api/keyword_fallback.py` | `triggered, reason, query_used, query_text, anchor_tokens, latency_ms, initial_hits, final_hits` |
| `RouterDecision` | `api/intent_router.py` | `prefer, candidate_mode, final_mode, rule_hits, evidence, fallback` |
| `I18nExpandResult` | `api/rag_recall_tools.py` | `raw, expanded, candidates, source, truncated, enabled, mode` |
| `StructuredRecallResult` | `api/rag_recall_tools.py` | `hits, date_norms` |
| `Text2SqlResult` | `api/text2sql_core.py` | `sql, columns, rows, answer, retrieved` |
| `StoreDoc` | `api/text2sql_store.py` | `doc_type, title, content` |
| `SupabaseManager` | `api/database_manager.py` | `url, service_key` |

### 4.3 环境变量（必填/可选）

| 名称 | 必填 | 读取位置 | 默认值/留空行为 |
|------|------|----------|----------------|
| `NEXT_PUBLIC_SUPABASE_URL` / `SUPABASE_URL` | 必填（二选一） | `api/rag_env.py:pick_supabase_url()` | — |
| `SUPABASE_SERVICE_ROLE_KEY` / `SUPABASE_SERVICE_KEY` | 必填（二选一） | `api/rag_env.py:pick_supabase_service_key()` | — |
| `SILICONFLOW_API_KEY` | 必填 | `api/rag_env.py:must_siliconflow_api_key()` | chat 500 / ingest RuntimeError |
| `NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET` / `API_KEY` | 必填（至少一个） | `api/rag_env.py:admin_secret()` + 各模块 `_require_*_auth` | 鉴权 500 |
| `SILICONFLOW_BASE_URL` | 可选 | `api/rag_env.py:siliconflow_base()` | `https://api.siliconflow.cn/v1` |
| `SILICONFLOW_EMBEDDING_MODEL` | 可选 | `api/rag_env.py:siliconflow_embedding_model()` | `Qwen/Qwen3-Embedding-0.6B` |
| `SILICONFLOW_EMBEDDING_DIMENSIONS` | 可选 | `api/rag_env.py:siliconflow_embedding_dimensions()` | `1024` |
| `SILICONFLOW_CHAT_MODEL` | 可选 | `api/index.py` 等 | `deepseek-ai/DeepSeek-V3` |
| `RAG_MATCH_THRESHOLD` | 可选 | `api/index.py:_parse_match_threshold()` | `0.3`；`none` 关闭过滤 |
| `EMBEDDING_DIM` / `SILICONFLOW_EMBEDDING_DIM` | 可选 | `api/rag_env.py:expected_embedding_dim()` | `1024` |
| `CONTENT_ROOT` | 可选 | `api/ingest_pipeline.py:get_all_markdown_chunks()` | `REPO_ROOT/content` |
| `CONTENT_DEFAULT_YEAR` | 可选 | `api/index.py` | `2026` |
| `TEXT2SQL_DATABASE_URL` | **Text2SQL 必填** | `api/text2sql_core.py:execute_select_sql()` | 缺失则 RuntimeError |
| `TEXT2SQL_FAISS_DIM` | 可选 | `api/text2sql_store.py` | `256` |
| `DEBUG_RAG` / `RAG_DEBUG` | 可选 | `api/index.py:_rag_debug_enabled()` | `1/true/yes/on` 或 `NODE_ENV=development` 开启 |
| `DEBUG_INGEST` | 可选 | `api/ingest_pipeline.py` | — |
| `DEBUG_CODE_INGEST` | 可选 | `api/code_ingest.py` | — |
| `TEXT2SQL_DEBUG` | 可选 | `api/text2sql_api.py` | — |
| `I18N_EXPAND_ENABLED` | 可选 | `api/rag_recall_tools.py` | `True` |
| `I18N_EXPAND_MODE` | 可选 | `api/rag_recall_tools.py` | `glossary` |
| `KEYWORD_FALLBACK_ENABLED` | 可选 | `api/keyword_fallback.py` | `True` |
| `RAG_RPC_RETRIES` | 可选 | `api/unified_chat.py` | `2` |
| `RAG_MATCH_COUNT` | 可选 | `api/unified_chat.py` | `10` |
| `TEXT2SQL_RETRIEVE_TOPK` | 可选 | `api/text2sql_api.py` 等 | `6` |
| `TEXT2SQL_MAX_ROWS` | 可选 | `api/text2sql_core.py` 等 | `200` |
| `MAX_X_SOURCES_HEADER_CHARS` | 可选 | `api/index.py` | `6000` |

---

## 5. 运行与观测

### 5.1 Debug 开关

| 开关 | 生效范围 | 行为 |
|------|----------|------|
| `DEBUG_RAG=1` / `RAG_DEBUG=1` / `NODE_ENV=development` | RAG 主链路 | `_rag_log()` 输出 `[rag-debug] ...` 到 stdout；包含 query、rewrite、embedding、retrieve、fallback、hits 摘要等 |
| `DEBUG_INGEST=1` | Markdown ingest | 打印扫描文件列表、embedding 进度、fts refresh 跳过原因 |
| `DEBUG_CODE_INGEST=1` | Code ingest | 打印文件数、chunk 数、embedding 进度、失败降级信息 |
| `TEXT2SQL_DEBUG=1` | Text2SQL | `_t2s_debug()` 输出 `[text2sql] ...` 到 stdout |

### 5.2 日志点（关键）

- `api/index.py`：`[rag]` 前缀 print（非 debug 也输出）：hybrid 融合结果统计、date anchor 注入信息、match_documents error。
- `api/index.py`：`[rag-debug]` 前缀（条件输出）：rewrite 结果、embedding 失败、retrieve summary、query compare、keyword fallback detail、top hits、x-sources header 超限、save_debug_log 失败。
- `api/unified_chat.py`：无 stdout 日志，全部通过 `events[]` 返回给调用方。
- `api/text2sql_api.py`：`[text2sql]` 前缀（条件输出）：store 初始化、检索结果数。
- `api/code_retrieval.py`：`_rag_log()` 输出 supabase_url 与 key_len（调试用）。

### 5.3 重试与超时

| 场景 | 策略 | 代码位置 |
|------|------|----------|
| Supabase RPC（connection reset / timeout / broken pipe 等） | 最多 `RAG_RPC_RETRIES` 次（默认 2），指数退避（base 0.15s） | `api/rag_recall_tools.py:rpc_execute_with_retry()` |
| Text2SQL DB 连接 | `connect_timeout=TEXT2SQL_DB_CONNECT_TIMEOUT_S`（默认 8s） | `api/text2sql_core.py:execute_select_sql()` |
| Embedding 失败 | 不重试，直接降级 keyword-only | `api/index.py:chat()` |
| Query Rewrite 失败 | 不重试，回退原 query | `api/index.py:chat()` / `api/unified_chat.py` |

### 5.4 降级策略

- **Embedding 不可用**（ SiliconFlow 故障 / Key 失效）：跳过 vector，仅 keyword（FTS），日志标记 `mode=keyword_only`。
- **Keyword 命中不足**（rewrite 导致锚点丢失）：触发 `keyword_fallback`，用原始 query 的锚点 token / normalized query 再检索。
- **Text2SQL store 无 faiss**：降级为 `Text2SqlFallbackStore`（纯 Python 点积排序）。
- **Code ingest embedding 失败**：用零向量占位，保证入库继续，后续 query 自动降级 keyword-only。

---

## 6. 改动指引

### 6.1 新增一个端点

1. **在 `api/index.py` 注册路由**：`@app.post("/api/py/xxx")`，调用新 handler。
2. **鉴权**：复用 `_require_auth()` 或新建 `_require_xxx_auth()`（建议统一使用 `admin_secret()` + `API_KEY` + `hmac.compare_digest`）。
3. **若需 Supabase**：`pick_supabase_url()` + `pick_supabase_service_key()` → `create_client()` 或 `SupabaseManager.from_env()`。
4. **若需 LLM**：`openai_siliconflow_client()` 或手动 `OpenAI(api_key=..., base_url=...)`。
5. **日志**：如需写入 `rag_conversation_logs`，复用 `SupabaseManager.save_debug_log()`。
6. **测试**：在 `tests/` 新增 `test_xxx.py`，用 `pytest` 运行。

风险点：
- 循环 import：`api/code_retrieval.py` 通过 `bind_index_symbols()` 运行时注入避免循环 import；新增模块若需共享符号，建议同样采用运行时注入或把常量/函数放到 `api/rag_env.py`。
- Serverless 状态：内存队列（`JOBS`）不持久；若新增需要持久状态的功能，应写入 Supabase 表而非内存。

### 6.2 调整检索策略

| 目标 | 改动文件 | 说明 |
|------|----------|------|
| 修改 Vector top-k | `api/index.py`（`MATCH_COUNT`）/ `api/unified_chat.py`（`RAG_MATCH_COUNT` env） | 默认 10 |
| 修改相似度阈值 | `api/index.py:_parse_match_threshold()` / `api/unified_chat.py:_parse_match_threshold()` | 默认 0.3；`none` 关闭 |
| 修改 RRF 常数 | `api/hybrid_fusion.py:RRF_K` | 默认 60 |
| 修改 Keyword match_count | `api/index.py:fetch_keyword_hits()` / `api/unified_chat.py` RPC 参数 | 默认 12 |
| 修改日期召回 limit | `api/rag_recall_tools.py:structured_recall_by_date()` | 默认 6 |
| 新增 i18n 术语 | `data/i18n_glossary.json` | 无需改代码，glossary 按 mtime 缓存 |
| 修改 keyword fallback 策略 | `api/keyword_fallback.py` | `KeywordFallbackConfig.from_env()` 读取环境变量 |
| 修改 query rewrite prompt | `api/query_rewrite.py:_sync_rewrite()` | 直接改 prompt 文本 |

风险点：
- `match_documents` RPC 的 `match_threshold` 为余弦相似度（0~1），>1 会被视为无效并回退为 `None`（关闭过滤）。
- `keyword_documents` 使用 `websearch_to_tsquery('simple', query_text)`，query_text 过长或含特殊字符可能语法错误；当前已做清洗与截断（`rag_recall_tools.py`）。

### 6.3 调整 ingest

| 目标 | 改动文件 | 说明 |
|------|----------|------|
| 修改分块大小/重叠 | `api/ingest_pipeline.py:CHUNK_SIZE / CHUNK_OVERLAP` | 默认 512 / 50 |
| 修改 Embedding batch | `api/ingest_pipeline.py:EMBED_BATCH_SIZE` | 默认 32 |
| 修改写入 batch | `api/ingest_pipeline.py:INSERT_BATCH_SIZE` | 默认 80 |
| 修改内容根目录 | 环境变量 `CONTENT_ROOT` | 默认 `REPO_ROOT/content` |
| 新增文件类型支持 | `api/ingest_pipeline.py:_is_md()` / `_walk_markdown()` | 当前仅 `.md` / `.mdx` |
| 修改代码解析范围 | `api/code_parser.py:parse_project()` | 当前仅 `.py`；排除 `.venv` / `__pycache__` / `.git` / `node_modules` / `docs` |
| 修改代码元数据字段 | `api/code_ingest.py:to_db_metadata_code()` / `CodeIngestMeta` | 新增字段需同步 SQL 侧注释/索引（可选） |

风险点：
- 向量维度必须与 `supabase/sql/init.sql` 中 `vector(N)` 一致；当前默认 1024。若改模型维度，需全量重灌。
- `process_markdown_files` 与 `sync_content_to_vector` 删除策略不同：前者按 `relativePath` 删，后者按 `slug` 删；混用可能导致数据残留。
- ingest 后必须调用 `refresh_documents_fts_tokens_for_paths` 或依赖触发器自动维护；大批量写入时触发器可能延迟。

---

## 7. 不确定性与验证步骤

| 序号 | 不确定性描述 | 处理方式 | 验证步骤 |
|------|-------------|----------|----------|
| 1 | `docs/text2sql/v1/sql/supabase_init.sql` 是否存在？代码中 `text2sql_store.py` 依赖该文件构建 Text2SQL store；但当前目录扫描未列出 `docs/text2sql/`。 | 未下结论，标记为不确定 | `ls docs/text2sql/v1/sql/` 确认文件存在性；若缺失，`get_text2sql_store()` 会抛 `RuntimeError` |
| 2 | `API_KEY` 是否在生产环境实际使用？代码中多处读取，但 `.env.example` 未列出。 | 代码中存在，但配置模板未显式说明 | 检查生产环境 `.env` 或 Vercel Secrets 是否注入 `API_KEY`；对比 `NEXT_PUBLIC_ADMIN_SECRET` 优先级 |
| 3 | `TEXT2SQL_DATABASE_URL` 的 Supabase 项目是否与 `NEXT_PUBLIC_SUPABASE_URL` 为同一项目？ | 无法从代码确认 | 检查 `.env` 中两者是否指向同一 Postgres 实例；若为不同库，需确认权限与网络白名单 |
| 4 | `match_code_chunks` 与 `keyword_code_chunks` RPC 的 `match_threshold` 参数是否与 `match_documents` 一致？ | `code_chunks.sql` 中 `match_code_chunks` 签名与 `init.sql` 一致（三参数），但 `code_retrieval.py` 调用时传了 `match_threshold`，需确认 SQL 侧已部署 | 在 Supabase SQL Editor 执行 `\df public.match_code_chunks` 确认函数签名 |
| 5 | `refresh_documents_fts_tokens_for_paths` 与 `refresh_code_chunks_fts_tokens_for_paths` 是否已在生产库创建？ | 代码中调用，但 SQL 文件需手动执行 | 在 Supabase SQL Editor 执行 `\df public.refresh_*` 确认存在性 |
| 6 | `hybrid_search.sql` 中的 `rag_fts_alias_text` 函数是否在生产库执行过？ | 该函数是 B2 v2 增量迁移的一部分 | 检查 `docs/tasks/legacy/task_rag_b2_fts_alias_backfill_v1.md` 等任务文档，或在 SQL Editor 执行 `\df public.rag_fts_alias_text` |
| 7 | `intent_router.py` 中 `_ddl_evidence` 与 `_fts_evidence` 的异常捕获是否会导致路由延迟显著增加？ | 代码中 `try/except` 包裹，但无超时控制 | 通过 `rag_conversation_logs.metadata.evidence` 观察实际延迟；若频繁超时，考虑加缓存或异步预计算 |
| 8 | `unified_chat.py` 的 RAG branch 中 `structured_recall_by_date` 与 vector/keyword 的融合顺序是否最优？ | 当前顺序：structured → keyword raw/rewrite → vector；代码注释未说明理由 | 通过 A/B 实验或观察 `rag_conversation_logs.metadata.match` 中各层命中数，评估顺序对最终答案的影响 |
| 9 | `code_retrieval.py` 中 `_boost_by_query_name` 的 `+100.0` 加分是否会导致 RRF 分数失真？ | 当前实现直接修改 `fused_score`，非 RRF 原生逻辑 | 观察 code query 结果中同名 chunk 是否过度前置；若失真，改为在 RRF 前过滤或调整权重 |
| 10 | `ingest_pipeline.py` 中 `sync_content_to_vector` 与 `process_markdown_files` 的删除策略差异是否会导致数据残留？ | `process` 按 relativePath 删，`sync` 按 slug 删；若同一文件改名，slug 不变则 `sync` 不会清理旧 relativePath | 检查生产库中 `documents` 表是否有 `relativePath` 与 `slug` 不一致的脏数据；必要时统一删除策略 |

---

## 8. 消耗明细

### 8.1 时间

| 阶段 | 耗时估算 | 说明 |
|------|----------|------|
| t_scan（目录/索引扫描） | ~2 min | `find` / `ls` 扫描 api/、supabase/sql/、tests/、docs/meta/；并行读取 requirements.txt、.env.example、vercel.json、pytest.ini |
| t_read（阅读与追链路） | ~18 min | 逐文件阅读 api/*.py（19 个文件，~5500 行）、SQL（5 个文件，~525 行）、测试（9 个文件，~1443 行）、docs/meta（1 个文件，150 行）；交叉 grep 追调用链、env 读取点、RPC 名称 |
| t_synthesis（结构化总结与写结果） | ~8 min | 整理模块地图、链路、数据结构、改动指引、不确定性清单；计算 token 与覆盖率 |
| **t_total** | **~28 min** | 估算值，含并行阅读与反复验证 |

### 8.2 Token（估算）

**估算方法说明**：
- 代码/SQL/配置：按 **每行 12 tokens** 估算（Python 平均词密度约 8-15 tokens/行，取中值）。
- 文档（markdown）：按 **每行 10 tokens** 估算（自然语言密度略低）。
- 搜索/命令输出：按 **每行 8 tokens** 估算（多为路径或简短结果）。
- 最终结果输出：按 **每 4 字符 1 token** 估算（中文混合文本约 3-5 字符/token，取保守值）。

| 项目 | 行数 | 每行 tokens | 输入 tokens |
|------|------|-------------|-------------|
| api/*.py（19 文件） | ~5,500 | 12 | 66,000 |
| supabase/sql/*.sql（5 文件） | ~525 | 12 | 6,300 |
| tests/*.py（9 文件） | ~1,443 | 12 | 17,316 |
| docs/meta/*.md（1 文件） | 150 | 10 | 1,500 |
| 其他配置（requirements, .env.example, vercel.json, pytest.ini, main.py） | ~60 | 10 | 600 |
| Shell grep 输出（约 15 次命令，平均 30 行/次） | ~450 | 8 | 3,600 |
| **input_tokens_code** | — | — | **~66,000** |
| **input_tokens_docs** | — | — | **~1,500** |
| **input_tokens_shell_or_search** | — | — | **~3,600** |
| **input_tokens_total** | — | — | **~71,400** |

**输出 tokens**：
- 本结果文件约 12,000 字符（中文为主，含表格、代码块）。
- 按 4 字符/token 估算：`12,000 / 4 = 3,000` tokens。
- 保守加 20% 格式开销：`3,000 * 1.2 ≈ 3,600` tokens。

| 项目 | tokens |
|------|--------|
| output_tokens_result | ~3,600 |
| **total_tokens** | **~75,000** |

---

## 9. 覆盖率

### 9.1 读过的关键文件清单（>20 个）

| # | 文件路径 | 目的/贡献 |
|---|----------|-----------|
| 1 | `main.py` | 本地 uvicorn 入口确认 |
| 2 | `api/index.py` | FastAPI 路由注册、RAG 主链路、鉴权、admin ingest/sync、流式响应 |
| 3 | `api/unified_chat.py` | Unified Chat（JSON + SSE）、Intent 路由调用、RAG/Text2SQL/no_data 三模式实现 |
| 4 | `api/chain_chat.py` | Chain Chat v1（仅 Text2SQL events） |
| 5 | `api/text2sql_api.py` | 独立 Text2SQL 端点、聚合结果兜底 |
| 6 | `api/text2sql_core.py` | SQL 意图识别、只读校验、psycopg 执行、prompt 构建、LLM 调用 |
| 7 | `api/text2sql_store.py` | Faiss/Fallback 检索库、DDL/examples 解析、惰性加载 |
| 8 | `api/intent_router.py` | 规则路由 + DDL/FTS 证据校验、fallback 逻辑 |
| 9 | `api/rag_env.py` | .env 加载、Supabase/SiliconFlow 选择器、Embedding 参数封装 |
| 10 | `api/database_manager.py` | SupabaseManager：rag_conversation_logs 读写、历史查询 |
| 11 | `api/ingest_pipeline.py` | Markdown 分块、Embedding、写入 documents、内存任务队列 |
| 12 | `api/code_ingest.py` | 代码分块、Embedding、写入 code_chunks、元数据扩展 |
| 13 | `api/code_parser.py` | Python AST 解析、ParsedChunk 生成 |
| 14 | `api/code_retrieval.py` | 代码 Query/Search、Hybrid 检索、过滤、boost、兜底策略 |
| 15 | `api/hybrid_fusion.py` | RRF 融合算法 |
| 16 | `api/rag_recall_tools.py` | RPC 重试、日期结构化召回、i18n glossary、keyword query 构造 |
| 17 | `api/query_rewrite.py` | 基于历史的查询改写 |
| 18 | `api/keyword_fallback.py` | 锚点 token 提取、keyword fallback 策略 |
| 19 | `api/rag_logging.py` | 日志元数据构建、命中摘要 |
| 20 | `supabase/sql/init.sql` | documents 表、match_documents RPC、HNSW 索引 |
| 21 | `supabase/sql/hybrid_search.sql` | fts_tokens、keyword_documents RPC、alias 函数、触发器 |
| 22 | `supabase/sql/code_chunks.sql` | code_chunks 表、match_code_chunks / keyword_code_chunks RPC |
| 23 | `supabase/sql/create_rag_conversation_logs.sql` | 日志表结构 |
| 24 | `supabase/sql/patch_match_documents_threshold.sql` | 阈值参数升级补丁 |
| 25 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | 环境变量真值表、目录地图、对外契约 |
| 26 | `requirements.txt` | 依赖清单 |
| 27 | `.env.example` | 环境变量模板 |
| 28 | `vercel.json` | 部署配置（极简 schema） |
| 29 | `pytest.ini` | 测试配置 |

### 9.2 未覆盖但可能重要的区域

| 区域 | 说明 |
|------|------|
| `tests/*.py`（9 个文件） | 已抽样浏览文件名与大致内容，但未逐行精读；测试覆盖了 intent router、unified chat、chain chat、code API、code ingest/parser、admin ingest route 等，可作为行为契约的辅助验证源 |
| `docs/tasks/`（~20 个任务文件） | 未阅读；包含 Task 规格与验收标准，可能补充设计决策背景（如 B2 FTS alias、i18n crosslingual recall 等） |
| `docs/diary/` | 未阅读；为日记/知识总结素材，与代码理解无关 |
| `docs/flows/` / `docs/delivery/` / `docs/UI/` | 未阅读；可能包含流程图与交付物，但任务要求禁用 `docs/_tech_graph/`，其他 docs 子目录未强制要求 |
| `tools/*.py`（5 个文件） | 未阅读；为技术图谱相关工具（contract check、drift check、manifest check、render），与运行时代码无关 |
| `web/` | 未阅读；仅一个文件 `assistant_ticket_bot-3.py`，职责不明 |
| `data/i18n_glossary.json` | 未阅读内容；仅确认文件存在，用于 i18n expand |
| `.cursor/rules/*.mdc` | 未阅读；可能包含 RAG 工程约束 |
| `.github/workflows/` | 未阅读；CI 配置可能包含 ingest 触发逻辑 |
| `supabase/check/` | 未阅读；为 SQL 执行验证记录，非代码 |

---

*本文件由 Agent 在完全不读取 `docs/_tech_graph/` 的前提下，基于真实代码、SQL、配置文件独立完成。*
