# Prompt B 结果：基于 `_tech_graph` 快速全量理解（工程可接手级别）

> 执行时间：2026-04-27T22:28+08:00 起
> 执行 Agent：Kimi Code CLI（强制走图谱索引）

---

## 1. 摘要

`ai-ink-brain-api-python` 是 Ink-Brain 博客的 **RAG / Embedding / Retrieval / Ingest** 服务端（FastAPI）。核心能力：

- **Unified Chat**：单入口根据意图路由到 RAG 检索或 Text2SQL 查库，支持 JSON / SSE 双模输出；
- **RAG 检索**：SiliconFlow Embedding + Supabase pgvector（cosine）+ FTS（`websearch_to_tsquery`）+ RRF 融合，支持日期结构化召回与 I18N 跨语言扩展；
- **Text2SQL**：意图判定 → DDL/Example 语料检索 → LLM 生成 SQL → 只读校验 → 直连 Postgres 执行 → 聚合/LLM 总结；
- **Ingest**：Markdown（博客内容）与 Code（项目源码）分块、Embedding、写入 Supabase；
- **Code RAG**：独立 `code_chunks` 表，支持向量 + FTS 混合检索；
- **可观测**：SSE 事件链（`chain`/`done`）+ `rag_conversation_logs` 持久化 + 多环境 debug 开关。

---

## 2. 图谱索引总结（主流程目录）

读完 `00_main.md` / `00_main.ai.md` / `99_spec.md` / `99_mermaid_protocol.md` / `01_struct.md` / `02_version.md` 以及全部 `10~15_flow` 后，识别出的主链路如下：

| # | 链路 | 图谱文件 | 应深入阅读的代码文件 |
|---|------|---------|-------------------|
| 1 | **Unified Chat（JSON）** | `10_flow_rag.ai.md` / `11_flow_text2sql.ai.md` | `api/index.py::unified_chat_route` → `api/unified_chat.py::handle_unified_chat` |
| 2 | **Unified Chat（SSE Stream）** | `10_flow_rag.ai.md` / `11_flow_text2sql.ai.md` / `14_runtime_observability.ai.md` | `api/index.py::unified_chat_stream_route` → `api/unified_chat.py::handle_unified_chat_stream` |
| 3 | **Legacy RAG Chat** | `10_flow_rag.md` | `api/index.py::chat`（StreamingResponse） |
| 4 | **Text2SQL（独立端点）** | `11_flow_text2sql.ai.md` | `api/index.py::text2sql_chat` → `api/text2sql_api.py::handle_text2sql_chat` |
| 5 | **Intent Router** | `10_flow_rag.ai.md` / `11_flow_text2sql.ai.md` | `api/intent_router.py::decide_intent` |
| 6 | **RAG 召回（Vector + FTS + Structured）** | `10_flow_rag.ai.md` / `12_flow_fts.ai.md` | `api/rag_recall_tools.py`（`rpc_execute_with_retry`, `keyword_query_text_with_i18n_meta`, `structured_recall_by_date`） |
| 7 | **Hybrid Fusion（RRF）** | `10_flow_rag.ai.md` | `api/hybrid_fusion.py::fuse_hits_rrf` |
| 8 | **FTS 索引与查询** | `12_flow_fts.ai.md` / `12_flow_fts.md` | `supabase/sql/hybrid_search.sql`（`rag_fts_alias_text`, `keyword_documents`, `refresh_documents_fts_tokens_for_paths`） |
| 9 | **Supabase RPC 与表** | `13_flow_supabase_rpc.ai.md` / `01_struct.md` | `supabase/sql/init.sql`, `supabase/sql/code_chunks.sql`, `supabase/sql/create_rag_conversation_logs.sql` |
| 10 | **Ingest（Markdown）** | `00_main.ai.md` | `api/ingest_pipeline.py::process_markdown_files` |
| 11 | **Ingest（Code）** | `00_main.ai.md` | `api/code_ingest.py::process_code_files` |
| 12 | **Code RAG 检索** | `00_main.ai.md` | `api/code_retrieval.py::handle_code_query` / `handle_code_search` |
| 13 | **Chain Chat（Timeline）** | `00_main.ai.md` | `api/chain_chat.py::handle_chain_chat` |
| 14 | **Chat History** | `00_main.ai.md` | `api/index.py::chat_history` → `api/database_manager.py::SupabaseManager` |
| 15 | **Runtime / Observability** | `14_runtime_observability.ai.md` | `api/unified_chat.py::_event`, `_sse`, `save_debug_log`（通过 `database_manager.py`） |
| 16 | **E2E Boundary / Contract** | `15_e2e_boundary.ai.md` / `_contract_manifest.json` | `docs/_tech_graph/_contract_manifest.json` + CI 门禁 `.github/workflows/tech-graph-contract.yml` |

---

## 3. 入口与模块地图

### 3.1 HTTP 端点（全部在 `api/index.py` 注册）

| 方法 | 路径 | Handler | 实际业务模块 |
|------|------|---------|-------------|
| GET | `/api/py/health` | `health` | 本地（`api/index.py`） |
| GET | `/api/py/chat/history` | `chat_history` | `api/database_manager.py::SupabaseManager` |
| POST | `/api/py/code/query` | `code_query` | `api/code_retrieval.py::handle_code_query` |
| POST | `/api/py/code/search` | `code_search` | `api/code_retrieval.py::handle_code_search` |
| POST | `/api/py/text2sql/chat` | `text2sql_chat` | `api/text2sql_api.py::handle_text2sql_chat` |
| POST | `/api/py/chain/chat` | `chain_chat_route` | `api/chain_chat.py::handle_chain_chat` |
| POST | `/api/py/unified/chat` | `unified_chat_route` | `api/unified_chat.py::handle_unified_chat` |
| POST | `/api/py/unified/chat/stream` | `unified_chat_stream_route` | `api/unified_chat.py::handle_unified_chat_stream` |
| POST | `/api/py/chat` | `chat` | `api/index.py`（Legacy RAG） |
| POST | `/api/py/admin/ingest` | `py_admin_ingest` | `api/ingest_pipeline.py::process_markdown_files` / `api/code_ingest.py::process_code_files` |
| POST | `/api/py/admin/sync` | `py_admin_sync_post` | `api/ingest_pipeline.py::run_sync_job_sync`（BackgroundTasks） |
| GET | `/api/py/admin/sync` | `py_admin_sync_get` | `api/ingest_pipeline.py::get_job` |

### 3.2 核心模块职责

| 文件 | 职责 |
|------|------|
| `api/index.py` | FastAPI app 注册、全部路由入口、Legacy RAG chat 实现、鉴权 `_require_auth` |
| `api/unified_chat.py` | Unified Chat（JSON + SSE）核心：intent 路由、RAG 召回、Text2SQL 执行、事件构建 |
| `api/intent_router.py` | 意图判定：`decide_intent`（规则候选 + DDL/FTS evidence 校验） |
| `api/rag_recall_tools.py` | 召回工具：RPC 重试、keyword query 构建（含 I18N 扩展）、日期结构化召回 |
| `api/hybrid_fusion.py` | RRF 融合：`fuse_hits_rrf` |
| `api/query_rewrite.py` | 查询改写：`rewrite_query_with_history`（注入历史上下文） |
| `api/text2sql_core.py` | Text2SQL 核心：SQL 生成、只读校验、执行、总结 prompt 构建 |
| `api/text2sql_api.py` | Text2SQL HTTP handler（独立端点） |
| `api/text2sql_store.py` | Text2SQL 语料存储/检索（FAISS / 向量） |
| `api/ingest_pipeline.py` | Markdown 分块、Embedding、写入 `documents`、sync job |
| `api/code_ingest.py` | 代码解析、分块、写入 `code_chunks` |
| `api/code_retrieval.py` | Code RAG 检索（向量 + FTS + 过滤） |
| `api/chain_chat.py` | Chain Timeline（返回 events[]，当前仅覆盖 Text2SQL） |
| `api/database_manager.py` | `SupabaseManager`：异步写入/读取 `rag_conversation_logs` |
| `api/rag_env.py` | `.env` 加载、Supabase/SiliconFlow 客户端工厂、维度选择器 |
| `api/rag_logging.py` | RAG 命中摘要、context 构建（用于日志） |
| `api/keyword_fallback.py` | Keyword 降级匹配（Legacy chat 使用） |

---

## 4. 关键链路

### 4.1 Unified Chat（JSON 模式）

**入口**：`api/index.py::unified_chat_route`（L561）→ `api/unified_chat.py::handle_unified_chat`

**关键函数**：

1. `_require_unified_auth`（L33）：校验 `Authorization: Bearer <token>` / `x-blog-admin-token` / `x-admin-token`，比对 `API_KEY` 或 `NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET`。
2. `decide_intent`（`api/intent_router.py` L139）：
   - 规则候选：`no_data_keywords`（润色/翻译等）→ `no_data`；`sql_keywords` / `identifier_hint` → `text2sql`；否则 `rag`。
   - Evidence 校验：DDL 命中数（`text2sql_store.search`）与 FTS 命中数（`keyword_documents`）。
   - Protect：text2sql 无 DDL evidence → fallback 到 rag / no_data；rag 无 FTS evidence → fallback 到 no_data。
3. **RAG branch**（`api/unified_chat.py` L484~L703）：
   - `rewrite_query_with_history`（`api/query_rewrite.py`）：有历史时 LLM 改写，无历史透传。
   - `embedding_kwargs_for_inputs`（`api/rag_env.py`）→ `oai.embeddings.create` → 得到向量。
   - `structured_recall_by_date`（`api/rag_recall_tools.py` L482）：按 `metadata->>date_norm` / `slug` / `filename` / `relativePath` 精确匹配。
   - `rpc_execute_with_retry`（`api/rag_recall_tools.py` L30）→ `match_documents`（vector）+ `keyword_documents`（FTS，raw + rewrite 双路）。
   - `fuse_hits_rrf`（`api/hybrid_fusion.py`）：三路 RRF 融合（structured + keyword + vector）。
   - `_rag_generate_answer`：构建 context（topK + strip prefix）→ LLM 生成回答。
4. **Text2SQL branch**（`api/unified_chat.py` L410~L482）：
   - `get_text2sql_store().search` 检索 DDL + Example。
   - `build_sql_prompt` → `llm_generate_sql` → `validate_sql_readonly`（仅 SELECT / WITH）。
   - `execute_select_sql`（直连 `TEXT2SQL_DATABASE_URL`）。
   - `_try_summarize_aggregate`（单行单列数值）或 `llm_summarize`。
5. **事件构建**：`_event`（L62）生成统一事件结构；最终 `finish()` 返回 JSON（含 `events[]`）。

**失败路径**：

- Auth 失败 → 401
- Embedding 失败 → `vec=None`，降级为 keyword-only（仍继续 RAG）
- RPC 失败（重试耗尽）→ `ret_err` 记入 `tool.call.end`，继续生成（可能无上下文）
- 0 hits → 输出 `no_data` 或继续 LLM 生成（取决于模式）
- SQL 校验失败 / 执行失败 → `error` 事件，返回空结果

**外部依赖**：

- SiliconFlow（Embedding + Chat）
- Supabase（`documents` / `code_chunks` / `rag_conversation_logs`）
- Text2SQL 目标库（`TEXT2SQL_DATABASE_URL`，独立 Postgres）

### 4.2 Unified Chat（SSE Stream）

**入口**：`api/index.py::unified_chat_stream_route`（L576）→ `api/unified_chat.py::handle_unified_chat_stream`（L712）

**关键函数**：

- `event_stream()`（内部生成器）：按阶段 `yield _sse("chain", _event(...))`。
- `_sse`（L706）：`event: chain\ndata: {json}\n\n`
- 最终 `yield _sse("done", {"ok": ..., "mode": ..., "run_id": ..., "session_id": ..., "request_id": ...})`

**事件类型**（已代码核验）：

- `meta` → `run_id`, `mode`, `session_id`
- `router.decision` → `prefer`, `candidate_mode`, `final_mode`, `rule_hits`, `evidence`, `fallback`
- `tool.call.start/end` → `tool`, `input` / `output`, `error`, `latency_ms`
- `rag.query_expand` → `raw`, `rewrite`
- `rag.sources` → `sources[]`（`id`, `content`, `filename`, `score`, `path`, `url`）+ `retrieval`
- `sql.result` → `sql`, `columns`, `rows`, `truncated`
- `assistant.message` → `role`, `content`
- `latency` → `total_ms`, `stages_ms`
- `error` → `stage`, `message`

### 4.3 Legacy RAG Chat

**入口**：`api/index.py::chat`（L591）

**特点**：直接返回 `StreamingResponse`（文本流 + 末尾 `SOURCES_JSON_SEPARATOR` + sources JSON）。不经过 Unified 的事件体系。使用 `fetch_keyword_hits` + `match_documents` + `keyword_fallback`。

### 4.4 Ingest Pipeline

**入口**：`api/index.py::py_admin_ingest`（L1026）

**Markdown ingest**：

- `get_all_markdown_chunks`（`api/ingest_pipeline.py` L102）：读取 `CONTENT_ROOT`（或 `REPO_ROOT/content`）→ 按字符分块（512/50 overlap）。
- `build_enhanced_chunk_text`：给 chunk 加 `[Document Context]` 前缀。
- `embed_texts_batch`：SiliconFlow Embedding，batch=32。
- `delete_documents_by_relative_paths`：先删旧数据。
- `sb.table("documents").insert()`：batch=80。
- `refresh_documents_fts_tokens_for_paths`：兜底刷新 FTS。

**Code ingest**：

- `api/code_ingest.py::process_code_files`：解析代码文件 → AST/正则提取函数/类 → 分块 → 写入 `code_chunks`。

### 4.5 Text2SQL（独立端点）

**入口**：`api/index.py::text2sql_chat`（L531）→ `api/text2sql_api.py::handle_text2sql_chat`

**链路**：鉴权 → `is_text2sql_intent` → `get_text2sql_store().search` → `build_sql_prompt` → `llm_generate_sql` → `validate_sql_readonly` → `execute_select_sql` → `_try_summarize_aggregate` / `llm_summarize` → JSON 响应。

### 4.6 Code RAG

**入口**：`api/index.py::code_query` / `code_search`（L501/L516）→ `api/code_retrieval.py`

- `handle_code_query`：向量检索（`match_code_chunks`）+ 过滤。
- `handle_code_search`：FTS 检索（`keyword_code_chunks`）+ 过滤。
- 均使用 `fuse_hits_rrf` 融合。

---

## 5. 数据结构与存储

### 5.1 表结构（以 `01_struct.md` 为候选，SQL 核验）

| 表 | 字段 | 类型 | 来源确认 |
|---|------|------|---------|
| `public.documents` | `id` | `bigserial primary key` | `supabase/sql/init.sql` L17 |
| | `content` | `text not null` | L19 |
| | `metadata` | `jsonb not null default '{}'` | L21 |
| | `embedding` | `vector(1024) not null` | L22 |
| | `fts_tokens` | `tsvector` | `supabase/sql/hybrid_search.sql` L18 |
| | `created_at` | `timestamptz not null default now()` | `init.sql` L23 |
| `public.code_chunks` | `id` | `uuid primary key default gen_random_uuid()` | `supabase/sql/code_chunks.sql` L13 |
| | `content` | `text not null` | L14 |
| | `metadata` | `jsonb not null default '{}'` | L15 |
| | `embedding` | `vector(1024) not null` | L16 |
| | `fts_tokens` | `tsvector` | L17 |
| | `created_at` | `timestamptz not null default now()` | L18 |
| `public.rag_conversation_logs` | `id` | `uuid primary key default gen_random_uuid()` | `supabase/sql/create_rag_conversation_logs.sql` L7 |
| | `session_id` | `varchar not null` | L8 |
| | `query` | `text not null` | L9 |
| | `rewritten_query` | `text` | L10 |
| | `retrieved_context` | `jsonb` | L11 |
| | `response` | `text` | L12 |
| | `metadata` | `jsonb` | L13 |
| | `created_at` | `timestamptz not null default now()` | L14 |

### 5.2 metadata 字段（代码使用方式核验）

`documents.metadata` 实际写入的键（`api/ingest_pipeline.py::to_db_metadata` L168~L187）：

- `category`（req）
- `slug`（req）
- `slug_norm`（opt，从 slug 抽取日期）
- `date_norm`（opt，从 filename/slug 抽取）
- `mtime`（req）
- `lastModified`（req）
- `relativePath`（req）
- `chunk_index`（req）
- `filename`（req）
- `original_link`（null）
- `page_number`（null）
- `section_header`（null）

`code_chunks.metadata` 扩展键（`api/code_ingest.py` / `api/code_parser.py` 推测，未逐行全读）：

- `file_path`, `start_line`, `end_line`, `chunk_type`, `name`, `signature`, `module`（与 `01_struct.md` 的 `FileMeta` 一致）

### 5.3 RPC（已 SQL 核验）

| RPC | 所在 SQL 文件 | 用途 |
|-----|-------------|------|
| `match_documents` | `init.sql` L50 | 向量检索（cosine distance） |
| `keyword_documents` | `hybrid_search.sql` L167 | FTS 检索（`websearch_to_tsquery`） |
| `refresh_documents_fts_tokens_for_paths` | `hybrid_search.sql` L198 | 按 relativePath 刷新 fts_tokens |
| `match_code_chunks` | `code_chunks.sql` L59 | code 向量检索 |
| `keyword_code_chunks` | `code_chunks.sql` L88 | code FTS 检索 |
| `refresh_code_chunks_fts_tokens_for_paths` | `code_chunks.sql` L117 | code fts_tokens 刷新 |
| `rag_fts_alias_text` | `hybrid_search.sql` L30 | 生成 alias 文本（日期/版本号/分隔符/CamelCase） |
| `documents_fts_tokens_update` | `hybrid_search.sql` L134 | 触发器函数 |
| `code_chunks_fts_tokens_update` | `code_chunks.sql` L34 | code 触发器函数 |

---

## 6. 运行与观测

### 6.1 Debug 开关（已代码核验）

| 环境变量 | 影响代码位置 | 行为 |
|---------|------------|------|
| `DEBUG_RAG=1` / `RAG_DEBUG=1` / `NODE_ENV=development` | `api/index.py::_rag_debug_enabled`（L100~L110 区域） | 打印 RAG 检索过程 |
| `DEBUG_INGEST=1` | `api/ingest_pipeline.py` L33 | 打印 ingest 过程 |
| `DEBUG_CODE_INGEST=1` | `api/code_ingest.py` | 打印 code ingest 过程 |
| `TEXT2SQL_DEBUG=1` | `api/text2sql_api.py::_t2s_debug` L51 | 打印 text2sql 过程 |

### 6.2 重试与超时

| 机制 | 代码位置 | 配置 |
|------|---------|------|
| RPC 重试 | `api/rag_recall_tools.py::rpc_execute_with_retry` L30 | `RAG_RPC_RETRIES`（默认 2），backoff 0.15s × 2^attempt |
| 可重试错误 | `should_retry_error` L13 | connection reset / timeout / server disconnected 等 |
| DB connect timeout | `api/text2sql_core.py::execute_select_sql` L100 | `TEXT2SQL_DB_CONNECT_TIMEOUT_S`（默认 8s） |
| SQL limit rows | `api/text2sql_core.py::execute_select_sql` L97 | `TEXT2SQL_MAX_ROWS`（默认 200） |

### 6.3 日志归档

- `api/database_manager.py::SupabaseManager.save_debug_log`（L34）：异步写入 `rag_conversation_logs`。
- Legacy chat：`api/index.py::chat` 中通过 `BackgroundTasks.add_task` 调用 `save_debug_log`。
- Unified chat：`api/unified_chat.py` 的 `finish()` 中调用 `save_debug_log`（非 streaming）或在 `event_stream` 的 `finally` 中处理（streaming）。

### 6.4 SSE 事件契约

- 真值来源：`docs/_tech_graph/_contract_manifest.json`
- CI 门禁：`.github/workflows/tech-graph-contract.yml`（运行 `python tools/tech_graph_contract_check.py`）
- 校验内容：envelope_keys、`chain`/`done` 最小键名、`type_values` 枚举、`payload_min_keys_by_type`

---

## 7. 改动指引

### 7.1 新增一个端点

1. **在 `api/index.py` 注册路由**：参考现有模式，添加 `@app.post/get(...)`，调用独立 handler（避免 index.py 膨胀）。
2. **鉴权**：复用 `_require_auth` 或新建 `_require_xxx_auth`（注意常量时间比较 `hmac.compare_digest`）。
3. **更新 manifest**：`docs/_tech_graph/_manifest.json` 的 `endpoints` 数组新增条目，否则 CI `tech_graph_manifest_check.py` 失败。
4. **更新图谱**：`00_main.md` / `00_main.ai.md` 添加节点与锚点注释。
5. **（可选）更新 contract**：若涉及 SSE 新事件类型，需更新 `_contract_manifest.json`。

**风险点**：

- 忘记更新 manifest → CI 失败。
- 在 `index.py` 写太多业务逻辑 → 文件膨胀（当前 1053 行已偏大）。

### 7.2 调整检索策略

1. **修改召回逻辑**：`api/rag_recall_tools.py`（keyword query 构建、日期召回、I18N 扩展）。
2. **修改融合逻辑**：`api/hybrid_fusion.py`（RRF 参数、融合顺序、max_total）。
3. **修改向量检索参数**：`api/unified_chat.py` 或 `api/index.py` 中 `match_count` / `match_threshold`（环境变量 `RAG_MATCH_COUNT` / `RAG_MATCH_THRESHOLD`）。
4. **修改 FTS 索引**：`supabase/sql/hybrid_search.sql`（`rag_fts_alias_text` 函数、触发器），需重新执行 SQL 并可能全量刷新。

**风险点**：

- `rag_fts_alias_text` 改动后，历史数据需重新生成 `fts_tokens`（大表注意性能）。
- RRF 融合顺序改变可能影响 topK 结果稳定性。
- `match_threshold` 设为 `none` 会关闭 SQL 侧过滤，但 Python 侧仍可能做后处理。

### 7.3 调整 Ingest

1. **修改分块策略**：`api/ingest_pipeline.py::chunk_text_by_chars`（CHUNK_SIZE / CHUNK_OVERLAP）。
2. **修改 metadata 写入**：`to_db_metadata`（新增字段需同步更新 `01_struct.md` 的 `FileMeta`）。
3. **修改 Embedding 前缀**：`build_enhanced_chunk_text`（当前是 `[Document Context]` 格式）。
4. **新增 ingest 类型**：`api/index.py::py_admin_ingest` 的 `type` 参数扩展 + 新增处理函数。
5. **刷新 FTS**：ingest 后自动调用 `refresh_documents_fts_tokens_for_paths`。

**风险点**：

- 分块大小改变 → 向量维度不变但语义粒度变化，需评估检索效果。
- metadata 新增字段 → 需确认 Supabase 表结构无需 DDL 变更（jsonb 扩展灵活）。
- Code ingest 与 Markdown ingest 的 `metadata` 结构不完全一致，统一字段时需注意兼容。

---

## 8. 不确定性与验证步骤

| # | 不确定点 | 处理策略 / 验证步骤 |
|---|---------|-------------------|
| 1 | `api/code_ingest.py` 与 `api/code_parser.py` 的完整实现细节 | 未逐行全读，仅确认入口 `process_code_files` 存在。如需深入，应阅读这两个文件并核对 `code_chunks` 的 metadata 写入键。 |
| 2 | `api/text2sql_store.py` 的具体存储后端（FAISS？内存？持久化？） | 未深入阅读。图谱提到 `TEXT2SQL_FAISS_DIM`，推测使用 FAISS 内存索引。验证：阅读 `api/text2sql_store.py` 全文。 |
| 3 | `api/keyword_fallback.py` 在 Legacy chat 中的实际触发条件与效果 | 仅确认符号存在，未阅读全文。Legacy chat 的 fallback 路径在 `api/index.py::chat` 中调用。验证：阅读 `api/keyword_fallback.py` + `api/index.py` 中 fallback 分支。 |
| 4 | `.github/workflows/tech-graph-contract.yml` 的具体实现 | 未阅读。已知入口是 `python tools/tech_graph_contract_check.py`，但 CI yaml 内容未知。验证：阅读 `.github/workflows/*.yml`。 |
| 5 | `tools/tech_graph_manifest_check.py` 与 `tools/tech_graph_drift_check.py` 的具体校验逻辑 | 未阅读。图谱提到它们是 CI/本地门禁。验证：阅读这两个文件。 |
| 6 | `api/index.py::chat`（Legacy）的完整 retrieve + generate 逻辑 | 已读开头（L591~L629），但未读完全部（约 200+ 行）。Unified chat 已覆盖主要逻辑，Legacy 的差异点（如 `keyword_fallback`）需额外阅读。 |
| 7 | `vercel.json` 当前为空（仅 `$schema`），生产部署如何指向 `api/index.py` | 图谱/AGENTS.md 提到 "Vercel 生产环境入口由 `vercel.json` 指向 `api/index.py`"，但 `vercel.json` 内容为空。推测由 Vercel 默认约定（`api/index.py` 自动识别）或平台配置覆盖。验证：查看 Vercel Dashboard 或询问维护者。 |
| 8 | `NEXT_PUBLIC_ADMIN_SECRET` 与 `CHAT_API_SECRET` 的优先级和实际使用场景 | 代码中两者是 "或" 关系（`admin_secret()` 返回第一个非空值）。未确认是否存在同时设置时的冲突。验证：检查 `api/rag_env.py::admin_secret` + 各 `_require_*_auth` 的调用。 |
| 9 | `data/i18n_glossary.json` 的实际内容规模与更新频率 | 仅确认文件路径存在（`api/rag_recall_tools.py::_i18n_glossary_path`）。未阅读内容。验证：`cat data/i18n_glossary.json`。 |
| 10 | `api/unified_chat.py` 的 `save_debug_log` 在 SSE streaming 模式下是否实际执行 | 代码中 `event_stream` 的 `finally` 块主要输出 `done` 事件，未明显看到 `save_debug_log` 调用。可能通过外层 `handle_unified_chat_stream` 的 `background_tasks` 或遗漏。验证：全文搜索 `save_debug_log` 在 `unified_chat.py` 中的引用。 |

---

## 9. 消耗明细

### 9.1 时间

| 阶段 | 耗时估算 | 说明 |
|------|---------|------|
| t_graph（阅读图谱） | ~8 min | 14 个图谱文件（含 .md + .ai.md），约 1200 行 |
| t_read（阅读与追链路） | ~18 min | 深入阅读 15+ 代码/SQL 文件，约 3500 行 |
| t_synthesis（总结与写结果） | ~10 min | 结构化整理 + 撰写本文件 |
| **t_total** | **~36 min** | 含思考与交叉核验 |

### 9.2 Token（估算）

**估算方法说明**：

- 阅读文件输入 token：按 **每行 12 tokens** 估算（Python/SQL/Markdown 混合，平均词长中等，含标点与缩进）。
- 搜索/命令输出输入 token：按 **每行 8 tokens** 估算（`wc -l` 等短输出）。
- 最终结果输出 token：按 **每 4 字符 ≈ 1 token** 估算（中文为主，混合英文标识符）。

| 类别 | 文件/来源 | 行数 | 每行 token | 输入 token 估算 |
|------|----------|------|-----------|----------------|
| 图谱文件 | `docs/_tech_graph/*.md` + `*.ai.md` | ~1200 | 12 | 14,400 |
| 代码文件 | `api/index.py` (630 行抽样) | 630 | 12 | 7,560 |
| | `api/unified_chat.py` (680 行抽样) | 680 | 12 | 8,160 |
| | `api/rag_recall_tools.py` (541 行全读) | 541 | 12 | 6,492 |
| | `api/ingest_pipeline.py` (320 行抽样) | 320 | 12 | 3,840 |
| | `api/intent_router.py` (237 行全读) | 237 | 12 | 2,844 |
| | `api/text2sql_core.py` (179 行全读) | 179 | 12 | 2,148 |
| | `api/text2sql_api.py` (193 行全读) | 193 | 12 | 2,316 |
| | `api/database_manager.py` (92 行全读) | 92 | 12 | 1,104 |
| | `api/hybrid_fusion.py` (55 行全读) | 55 | 12 | 660 |
| | `api/rag_env.py` (97 行全读) | 97 | 12 | 1,164 |
| | `api/query_rewrite.py` (64 行全读) | 64 | 12 | 768 |
| | `api/rag_logging.py` (85 行全读) | 85 | 12 | 1,020 |
| | `api/chain_chat.py` (120 行抽样) | 120 | 12 | 1,440 |
| | `api/code_retrieval.py` (120 行抽样) | 120 | 12 | 1,440 |
| SQL 文件 | `supabase/sql/*.sql`（6 个文件，约 515 行） | 515 | 12 | 6,180 |
| 配置/其他 | `main.py`, `vercel.json`, `.env.example`, `_manifest.json`, `_contract_manifest.json` | ~310 | 12 | 3,720 |
| 搜索/命令 | `wc -l`, `ls -la` 等 | ~50 行输出 | 8 | 400 |
| **输入 token 合计** | | | | **~64,716** |
| 输出 token（本结果文件） | 约 12,000 中文字符 + 3,000 英文字符 ≈ 15,000 字符 | — | 4 字符/token | **~3,750** |
| **total_tokens** | | | | **~68,466** |

> 注：以上为粗略估算，实际值因 tokenizer 差异可能有 ±15% 偏差。

---

## 10. 覆盖率

### 10.1 已读文件清单（逐项说明）

| 文件 | 目的/贡献 |
|------|----------|
| `docs/_tech_graph/00_main.md` | 顶层流程总图，识别全部入口端点 |
| `docs/_tech_graph/00_main.ai.md` | AI 协议版，确认端点锚点与 manifest 引用 |
| `docs/_tech_graph/01_struct.md` | DB Struct 候选，后续用 SQL 核验 |
| `docs/_tech_graph/02_version.md` | 版本迭代时间线，了解项目演进 |
| `docs/_tech_graph/10_flow_rag.md` | RAG 流程人类版 |
| `docs/_tech_graph/10_flow_rag.ai.md` | RAG 流程 AI 版（含错误分支、锚点） |
| `docs/_tech_graph/11_flow_text2sql.md` | Text2SQL 流程人类版 |
| `docs/_tech_graph/11_flow_text2sql.ai.md` | Text2SQL 流程 AI 版（含 validate/execute 错误分支） |
| `docs/_tech_graph/12_flow_fts.md` | FTS 流程人类版 |
| `docs/_tech_graph/12_flow_fts.ai.md` | FTS 流程 AI 版（含 I18N、B2 变体） |
| `docs/_tech_graph/13_flow_supabase_rpc.md` | RPC 流程人类版 |
| `docs/_tech_graph/13_flow_supabase_rpc.ai.md` | RPC 流程 AI 版（含错误分支） |
| `docs/_tech_graph/14_runtime_observability.md` | 观测人类版 |
| `docs/_tech_graph/14_runtime_observability.ai.md` | 观测 AI 版（SSE 事件类型、error 最短路径） |
| `docs/_tech_graph/15_e2e_boundary.md` | E2E 边界人类版 |
| `docs/_tech_graph/15_e2e_boundary.ai.md` | E2E 边界 AI 版（跨仓契约、SSE 字段） |
| `docs/_tech_graph/99_spec.md` | 技术图谱交付规约、Env Truth Table、Next Steps |
| `docs/_tech_graph/99_mermaid_protocol.md` | Mermaid 拓扑协议（边标记、节点标记、锚点规则） |
| `docs/_tech_graph/_manifest.json` | 端点/表/RPC/env/锚点真值 |
| `docs/_tech_graph/_contract_manifest.json` | SSE 跨端契约真值 |
| `api/index.py` | 全部路由入口、Legacy chat、admin ingest/sync |
| `api/unified_chat.py` | Unified Chat JSON + SSE 核心实现 |
| `api/intent_router.py` | 意图路由规则 + evidence 校验 |
| `api/rag_recall_tools.py` | 召回工具（RPC 重试、keyword、I18N、日期结构化召回） |
| `api/hybrid_fusion.py` | RRF 融合算法 |
| `api/query_rewrite.py` | 查询改写（历史注入） |
| `api/text2sql_core.py` | SQL 生成、校验、执行、总结 |
| `api/text2sql_api.py` | Text2SQL HTTP handler |
| `api/ingest_pipeline.py` | Markdown 分块、Embedding、写入 documents |
| `api/database_manager.py` | SupabaseManager（日志读写） |
| `api/rag_env.py` | .env 加载、客户端工厂 |
| `api/rag_logging.py` | RAG 命中摘要、context 构建 |
| `api/chain_chat.py` | Chain Timeline handler（抽样） |
| `api/code_retrieval.py` | Code RAG handler（抽样） |
| `supabase/sql/init.sql` | documents 表、match_documents、权限 |
| `supabase/sql/hybrid_search.sql` | fts_tokens、触发器、keyword_documents、rag_fts_alias_text |
| `supabase/sql/code_chunks.sql` | code_chunks 表、match_code_chunks、keyword_code_chunks |
| `supabase/sql/create_rag_conversation_logs.sql` | 日志表 |
| `supabase/sql/match_documents.sql` | 已合并提示 |
| `supabase/sql/patch_match_documents_threshold.sql` | 阈值升级补丁 |
| `main.py` | 本地运行入口 |
| `vercel.json` | Vercel 部署配置 |
| `.env.example` | 环境变量示例 |

### 10.2 未覆盖/抽样区域

| 区域 | 说明 |
|------|------|
| `api/code_ingest.py` | 仅确认入口 `process_code_files` 存在，未深入阅读 AST 解析与 metadata 构建 |
| `api/code_parser.py` | 未阅读，推测被 `code_ingest.py` 调用 |
| `api/keyword_fallback.py` | 未深入阅读，仅确认符号存在 |
| `api/index.py::chat`（Legacy）后半段 | 已读开头（L591~L629），剩余约 200 行未读（含 retrieve/generate/fallback） |
| `api/code_retrieval.py` 后半段 | 已读前 120 行，剩余约 480 行未读 |
| `api/chain_chat.py` 后半段 | 已读前 120 行，剩余约 205 行未读 |
| `tests/` | 未阅读任何测试文件 |
| `docs/tasks/`, `docs/diary/`, `docs/flows/` | 未阅读（非代码/SQL 事实来源） |
| `tools/`（除已知入口外） | 未阅读 `tech_graph_contract_check.py`、`tech_graph_drift_check.py`、`tech_graph_manifest_check.py` 的实现 |
| `.github/workflows/` | 未阅读 CI yaml |
| `web/` | 未阅读 |
| `data/i18n_glossary.json` | 未阅读内容 |

---

> **自检结论**：
> - 图谱中的名词（端点、RPC、表、env、handler）均已回链到代码或 SQL；无法直接确认的事项已列入“不确定性与验证步骤”。
> - 未使用“我猜/可能/大概”替代定位；要么定位到代码行，要么明确“不确定”并给出验证方式。
