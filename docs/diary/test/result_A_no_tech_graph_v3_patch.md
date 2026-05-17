<!-- Prompt 文件: docs/diary/test/prompt_A_no_tech_graph_v3.md -->
<!-- 执行日期: 2026-04-28 -->
<!-- git HEAD: 116ab0c -->

# Prompt A V3（禁用图谱）— 后端可交接梳理报告

## 1. 冷启动接手清单（10 步）

1. **读环境**：复制 `.env.example` 为 `.env.local`，填入 `SILICONFLOW_API_KEY`、`NEXT_PUBLIC_SUPABASE_URL`、`SUPABASE_SERVICE_ROLE_KEY`、`NEXT_PUBLIC_ADMIN_SECRET`。
2. **装依赖**：`pip install -r requirements.txt`（Python 3.11+）。
3. **起服务**：`python -m uvicorn main:app --host 127.0.0.1 --port 8000`；生产入口是 `api/index.py`（Vercel）。
4. **验健康**：`curl http://127.0.0.1:8000/api/py/health` 应返回 `{"ok":"true"}`。
5. **建数据库**：在 Supabase SQL Editor 按顺序执行 `supabase/sql/init.sql` → `hybrid_search.sql` → `create_rag_conversation_logs.sql`；若需 Code RAG 再执行 `code_chunks.sql`。
6. **核对维度**：确认 `.env` 中 `EMBEDDING_DIM`（默认 1024）与 SQL 中 `vector(1024)` 一致。
7. **跑测试**：`pytest tests/`；重点看 `test_unified_chat_backend_v1.py`、`test_unified_chat_streaming_sse.py`、`test_code_api_routes.py`。
8. **理解路由**：打开 `api/index.py`，从 `@app.post("/api/py/chat")` 开始，沿调用链看 `rewrite_query_with_history` → `augment_query_for_embedding` → `fuse_hits_rrf` → `token_stream`。
9. **理解 ingest**：打开 `api/ingest_pipeline.py`，看 `process_markdown_files`（先删后插）与 `sync_content_to_vector`（按 slug 删）。
10. **改前必读门禁**：任何 endpoint/RPC/表/env 变更，必须同步 `docs/_tech_graph/_manifest.json`，并本地执行 `python tools/tech_graph_manifest_check.py`；若涉及 SSE 事件键集变更，还要同步 `docs/_tech_graph/_contract_manifest.json` 并执行 `python tools/tech_graph_contract_check.py`。

---

## 2. 锚点索引表

| 概念 | 文件路径 | 函数/行区间 | 一句职责 |
|------|----------|-------------|----------|
| **FastAPI app 注册** | `api/index.py` | L52 `app = FastAPI(...)` | 全局 app 实例，所有路由挂载点 |
| **健康检查** | `api/index.py` | L434–436 `health()` | `GET /api/py/health` |
| **Legacy RAG 流式聊天** | `api/index.py` | L591–980 `chat()` | `POST /api/py/chat`；hybrid 检索 + StreamingResponse |
| **聊天历史** | `api/index.py` | L439–498 `chat_history()` | `GET /api/py/chat/history`；读 `rag_conversation_logs` |
| **Unified 聊天（JSON events）** | `api/unified_chat.py` | L192–703 `handle_unified_chat()` | `POST /api/py/unified/chat`；intent router → RAG/Text2SQL/no_data |
| **Unified 聊天（SSE 流）** | `api/unified_chat.py` | L712–1080 `handle_unified_chat_stream()` | `POST /api/py/unified/chat/stream`；SSE event 输出 |
| **Chain Chat（Text2SQL events）** | `api/chain_chat.py` | L60–324 `handle_chain_chat()` | `POST /api/py/chain/chat`；仅 Text2SQL 链路 events |
| **Text2SQL 直连** | `api/text2sql_api.py` | L86–192 `handle_text2sql_chat()` | `POST /api/py/text2sql/chat`；非 event 格式，返回 sql/rows/answer |
| **Code Query（hybrid）** | `api/code_retrieval.py` | L223–453 `handle_code_query()` | `POST /api/py/code/query`；向量+FTS 检索代码块 |
| **Code Search（metadata）** | `api/code_retrieval.py` | L456–575 `handle_code_search()` | `POST /api/py/code/search`；按 name/file_path/chunk_type/module 精确过滤 |
| **Admin ingest** | `api/index.py` | L1026–1052 `py_admin_ingest()` | `POST /api/py/admin/ingest?type=markdown\|code` |
| **Admin sync（异步任务）** | `api/index.py` | L983–1023 `py_admin_sync_post/get()` | `POST /api/py/admin/sync` + `GET /api/py/admin/sync?jobId=` |
| **环境加载** | `api/rag_env.py` | L1–97 | 加载 `.env.local`/`.env`；封装 Supabase/SiliconFlow 选择器 |
| **Supabase 读写封装** | `api/database_manager.py` | L12–92 `SupabaseManager` | `save_debug_log` / `get_chat_history` / `list_session_turns` |
| **Markdown ingest** | `api/ingest_pipeline.py` | L253–315 `process_markdown_files()` | 扫描 markdown → chunk → embed → 写 `documents` |
| **Markdown sync（按 slug）** | `api/ingest_pipeline.py` | L318–382 `sync_content_to_vector()` | 按 slug 删除旧数据后全量插入 |
| **Code ingest** | `api/code_ingest.py` | L180–254 `process_code_files()` | AST 解析 Python → embed → 写 `code_chunks` |
| **Code 解析（AST）** | `api/code_parser.py` | L64–181 `parse_python_file()` | 提取 module_doc / function / class / method |
| **Hybrid 融合（RRF）** | `api/hybrid_fusion.py` | L15–55 `fuse_hits_rrf()` | 向量+keyword 排名融合，RRF_K=60 |
| **Query Rewrite** | `api/query_rewrite.py` | L23–63 `rewrite_query_with_history()` | 注入 session 历史，LLM 改写为独立检索 query |
| **Keyword Fallback** | `api/keyword_fallback.py` | L131–193 `run_keyword_fallback()` | rewrite 丢锚点时，用原 query 锚点 token 回退检索 |
| **Intent Router** | `api/intent_router.py` | L139–236 `decide_intent()` | 规则候选 + DDL/FTS evidence → final_mode |
| **RAG 召回工具** | `api/rag_recall_tools.py` | L30–541 | RPC 重试、日期结构化召回、keyword query 构造、i18n expand |
| **Text2SQL Core** | `api/text2sql_core.py` | L24–179 | 意图识别、SQL 校验（只读）、执行、prompt 构建 |
| **Text2SQL Store** | `api/text2sql_store.py` | L92–184 | 从 `docs/text2sql/v1/sql/supabase_init.sql` 构建 FAISS 检索库 |
| **RAG 日志构建** | `api/rag_logging.py` | L9–85 | 组装 `rag_conversation_logs` 的 metadata 字段 |
| **Vector RPC** | `supabase/sql/init.sql` | L50–76 | `match_documents(query_embedding, match_count, match_threshold)` |
| **Keyword RPC** | `supabase/sql/hybrid_search.sql` | L167–193 | `keyword_documents(query_text, match_count)` |
| **Code Vector RPC** | `supabase/sql/code_chunks.sql` | L59–85 | `match_code_chunks(...)` |
| **Code Keyword RPC** | `supabase/sql/code_chunks.sql` | L88–114 | `keyword_code_chunks(...)` |
| **日志表** | `supabase/sql/create_rag_conversation_logs.sql` | L6–15 | `public.rag_conversation_logs` |
| **Manifest 门禁脚本** | `tools/tech_graph_manifest_check.py` | L229–328 `main()` | 校验 endpoint/env/table/RPC 与 `_manifest.json` 一致 |
| **Contract 门禁脚本** | `tools/tech_graph_contract_check.py` | L222–436 `main()` | 校验 SSE 事件键集与 `_contract_manifest.json` 一致 |
| **CI manifest** | `.github/workflows/tech-graph.yml` | L1–23 | PR/push 时跑 `tech_graph_manifest_check.py` |
| **CI contract** | `.github/workflows/tech-graph-contract.yml` | L1–37 | PR/push 时 checkout 前后端，跑 `tech_graph_contract_check.py` |

---

## 3. 新人 FAQ（8 条）

**Q1：为什么本地 `uvicorn main:app` 能跑，但 Vercel 部署后行为不同？**
> `main.py` 仅做 `from api.index import app` 转发；Vercel 生产入口由 `vercel.json` 指向 `api/index.py`。两者业务逻辑一致，但 serverless 冷启动对内存任务队列（ingest job）不保证持久。证据：`main.py` L1–10，`vercel.json`（本任务未读取，但 AGENTS.md 已说明）。

**Q2：Embedding 服务挂了，聊天会 502 吗？**
> 不会。`api/index.py` L670–686 捕获 embedding 异常，降级为 `keyword_only`；`api/code_retrieval.py` L313–327 同理。日志字段 `metadata.match.hybrid.mode` 会记录 `"keyword_only"`。证据：`api/index.py` L670–686、L762。

**Q3：`/api/py/chat` 与 `/api/py/unified/chat` 有什么区别？**
> `/api/py/chat` 是 Legacy 流式 RAG（返回 `text/plain` StreamingResponse，末尾带 `---RAG_SOURCES_JSON---`）；`/api/py/unified/chat` 返回 JSON events 数组，支持 RAG / Text2SQL / no_data 三模式路由。证据：`api/index.py` L591、`api/unified_chat.py` L192。

**Q4：日期查询是怎么做到优先命中当天日记的？**
> 两路并行：
> 1. `augment_query_for_embedding`（`api/index.py` L279–284）在 embedding 输入中注入 `TitleAnchor: YYYY-MM-DD.md`；
> 2. `fetch_date_anchor_hits`（`api/index.py` L310–362）直接用 `metadata->>slug` / `content ilike` 查 `documents` 表；
> 3. Unified 版额外有 `structured_recall_by_date`（`api/rag_recall_tools.py` L482–541）支持中文数字日期。证据：`api/index.py` L795–804、`api/rag_recall_tools.py` L482–541。

**Q5：ingest 会重复插入吗？**
> `process_markdown_files` 按 `relativePath` 先删后插；`sync_content_to_vector` 按 `slug` 先删后插；`process_code_files` 按 `relativePath` 先删后插并额外清理 `docs/` 前缀脏数据。证据：`api/ingest_pipeline.py` L270–272、L336–338；`api/code_ingest.py` L199–202。

**Q6：为什么 keyword 检索有时 0 命中？**
> `websearch_to_tsquery('simple', query_text)` 对英文停用词/标点敏感。系统有三层兜底：
> 1. `keyword_query_text_with_i18n_meta`（`api/rag_recall_tools.py` L279）做日期/版本/i18n 扩展；
> 2. `run_keyword_fallback`（`api/keyword_fallback.py` L131）用锚点 token 回退；
> 3. Code RAG 还有 `_identifier_only_query` / `_keyword_light_query`（`api/code_retrieval.py` L166–220）。证据：`api/keyword_fallback.py` L131–193、`api/code_retrieval.py` L366–399。

**Q7：新增一个 HTTP 端点，除了写路由还要做什么？**
> 必须同步 `docs/_tech_graph/_manifest.json` 的 `endpoints` 数组，然后本地执行 `python tools/tech_graph_manifest_check.py`。若该端点产出 SSE 事件或修改 chain event 键集，还要同步 `docs/_tech_graph/_contract_manifest.json` 并执行 `python tools/tech_graph_contract_check.py`。CI 会在 PR 时再次校验。证据：`tools/tech_graph_manifest_check.py` L229–328、`.github/workflows/tech-graph.yml`。

**Q8：Text2SQL 的 DDL 和示例从哪来？**
> `api/text2sql_store.py` L169–172 读取 `docs/text2sql/v1/sql/supabase_init.sql` 解析 `create table` 块作为 DDL；同时读取 `docs/text2sql/v1/spec/SAMPLES-01-text2sql-mini.md` 作为示例。用 hash embedding + FAISS（或纯 Python fallback）做检索。证据：`api/text2sql_store.py` L52–89、L163–184。

---

## 4. 改动配方卡

### 卡 A：新增 HTTP 端点

- **必读文件**：`api/index.py`（路由注册）、`docs/_tech_graph/_manifest.json`（endpoint 列表）、`.github/workflows/tech-graph.yml`（CI 校验）
- **慎碰点**：
  - 不要改动 `api/index.py` 中已有端点的 `handler` 函数名，否则 manifest 校验会失败。
  - 若新端点需要鉴权，复用 `_require_auth`（或 `_require_unified_auth` / `_require_code_api_auth`），保持 token 来源一致。
- **推荐验证**：
  1. 本地 `pytest tests/` 通过；
  2. `python tools/tech_graph_manifest_check.py` 输出 `OK`；
  3. 若涉及 SSE 契约：`python tools/tech_graph_contract_check.py` 输出 `OK`；
  4. `curl` 或 TestClient 验证新端点返回结构与文档一致。

### 卡 B：调整检索策略（向量 / keyword / 融合 / threshold）

- **必读文件**：`api/hybrid_fusion.py`（RRF 融合）、`api/rag_recall_tools.py`（keyword query 构造、结构化召回）、`api/index.py`（Legacy chat 检索逻辑）、`api/unified_chat.py`（Unified 检索逻辑）、`api/code_retrieval.py`（Code RAG 检索）
- **慎碰点**：
  - `RAG_MATCH_THRESHOLD` 默认 0.3，设为 `none` 会关闭 SQL 侧阈值过滤；`>1` 会被视为无效并回退 `None`（`api/index.py` L100–122）。
  - `RRF_K = 60` 是论文常用值，改动会全局影响融合排序。
  - `match_documents` 与 `keyword_documents` 的返回字段名不同（`similarity` vs `score`），上层已做兼容，但新增字段需检查 `build_sources_payload`。
- **推荐验证**：
  1. 设置 `DEBUG_RAG=1`，观察 console 输出的 `retrieve_summary` 与 `top_hits`；
  2. 跑 `test_unified_chat_backend_v1.py` 中的 RAG case；
  3. 对特定 query 对比 `vector_hits` / `keyword_hits` / `fused_scores` 变化。

### 卡 C：调整 ingest（markdown / code）

- **必读文件**：`api/ingest_pipeline.py`（markdown）、`api/code_ingest.py` + `api/code_parser.py`（code）、`supabase/sql/init.sql` + `code_chunks.sql`（表结构）
- **慎碰点**：
  - `CHUNK_SIZE = 512` / `CHUNK_OVERLAP = 50` 影响片段粒度与重复度；改后需全量重灌向量。
  - `EMBED_BATCH_SIZE = 32` / `INSERT_BATCH_SIZE = 80` 受 SiliconFlow RPM 与 Supabase 请求体大小限制，不要无脑调大。
  - `build_enhanced_chunk_text` 的文本格式（`[Document Context]` / `Title:` / `Content:`）被 `build_system_prompt` 和前端解析依赖，改动需同步前后端。
  - Code ingest 的 `parse_project` 排除 `.venv` / `__pycache__` / `docs/`；若新增排除目录，需在 `code_parser.py` 与 `code_ingest.py` 同步。
- **推荐验证**：
  1. 本地 `CONTENT_ROOT=xxx python -c "from api.ingest_pipeline import process_markdown_files; print(process_markdown_files())"`；
  2. `DEBUG_INGEST=1` 观察扫描文件列表与 embedding 进度；
  3. 灌库后抽查 `documents` / `code_chunks` 表的 `metadata->>relativePath` 与 `chunk_index`；
  4. 跑 `test_code_ingest_process.py`、`test_code_parser.py`。

---

## 5. 摘要

AI-Ink-Brain Python 后端是 FastAPI 服务，提供 RAG 聊天（Legacy 流式 + Unified events/SSE）、Text2SQL、Code RAG 与 Admin ingest/sync 四大能力。数据层依赖 Supabase（Postgres + pgvector + FTS），AI 层通过 OpenAI SDK 调用 SiliconFlow。核心设计：Hybrid 检索（向量+关键词+RRF 融合）、Embedding 失败降级 keyword-only、日期锚点优先召回、意图路由（rule + evidence）、ingest 先删后插幂等。门禁：`_manifest.json` + `_contract_manifest.json` + CI 校验。

---

## 6. 模块地图与主链路

### 6.1 Legacy RAG（`/api/py/chat`）

```
POST /api/py/chat
  → _require_auth
  → rewrite_query_with_history(oai, query, history[5])
  → augment_query_for_embedding (日期 TitleAnchor 注入)
  → SiliconFlow Embedding
  → Supabase RPC:
      match_documents(vector, match_count=10, threshold)
      keyword_documents(FTS, match_count=12)
  → keyword_fallback (锚点回退)
  → fuse_hits_rrf(vector, keyword, max_total=22)
  → fetch_date_anchor_hits (slug/Title 精确匹配) → merge_hits_anchors_first
  → build_system_prompt + build_sources_payload
  → OpenAI chat.completions.create(stream=True) → StreamingResponse
  → background_tasks: save_debug_log → rag_conversation_logs
```

### 6.2 Unified Chat（`/api/py/unified/chat` & `/stream`）

```
POST /api/py/unified/chat
  → decide_intent(query, prefer) → mode ∈ {auto, rag, text2sql, no_data, tool:*}
  → no_data: 直接 LLM 生成
  → text2sql:
      get_text2sql_store.search → build_sql_prompt → llm_generate_sql
      → validate_sql_readonly → execute_select_sql → llm_summarize
  → rag:
      rewrite → embed → structured_recall_by_date
      → match_documents + keyword_documents(raw+rewrite)
      → fuse_hits_rrf 多层融合 → _rag_generate_answer
  → 返回 events[]（非流）或 SSE event 流（stream）
```

### 6.3 Text2SQL（独立端点 `/api/py/text2sql/chat` & Chain Chat）

- `text2sql_api.py`：非 event 格式，直接返回 `sql/columns/rows/answer`。
- `chain_chat.py`：仅 Text2SQL 链路，返回 events 数组（供前端时间线）。
- 两者共用 `text2sql_core.py`（生成/执行/总结）与 `text2sql_store.py`（DDL 检索）。

### 6.4 Ingest（Markdown + Code）

- Markdown：`ingest_pipeline.py` → `get_all_markdown_chunks` → `chunk_text_by_chars(512,50)` → `build_enhanced_chunk_text` → embed → `documents`
- Code：`code_parser.py` AST 解析 → `code_ingest.py` → `build_enhanced_code_text` → embed → `code_chunks`
- 均先删后插，均调用 `refresh_*_fts_tokens_for_paths` 兜底刷新 FTS。

### 6.5 Code RAG（`/api/py/code/query` & `/search`）

- `code/query`：hybrid（`match_code_chunks` + `keyword_code_chunks`）→ filter → boost_by_query_name → 返回 chunks + sources。
- `code/search`：纯 metadata 过滤（`name` / `file_path` / `chunk_type` / `module`），无向量/FTS。

---

## 7. 事实断言清单

| 断言 | 证据 | 核验方式 | 置信度 |
|------|------|----------|--------|
| `POST /api/py/chat` 返回 `text/plain` StreamingResponse | `api/index.py` L975–980 | 代码阅读 / TestClient | 高 |
| 流末尾带 `---RAG_SOURCES_JSON---` + JSON | `api/index.py` L916–919 | 代码阅读 | 高 |
| `x-sources` Header 有 6000 字符上限 | `api/index.py` L69、L880 | 代码阅读 | 高 |
| Embedding 失败降级 keyword-only，不 502 | `api/index.py` L670–686、L762 | 代码阅读 / `test_unified_chat_backend_v1.py` | 高 |
| `match_documents` 使用 Cosine Distance（`1 - <=>`） | `supabase/sql/init.sql` L65–69 | SQL 阅读 | 高 |
| `keyword_documents` 使用 `websearch_to_tsquery('simple', ...)` | `supabase/sql/hybrid_search.sql` L185 | SQL 阅读 | 高 |
| `RAG_MATCH_THRESHOLD` 默认 0.3；`none` 关闭过滤 | `api/index.py` L100–122 | 代码阅读 | 高 |
| Unified Chat 支持 `prefer=auto/rag/text2sql/no_data` | `api/unified_chat.py` L98–108 | 代码阅读 / `test_intent_router_backend_v1.py` | 高 |
| Intent Router 用 rule + DDL/FTS evidence 决策 | `api/intent_router.py` L139–236 | 代码阅读 / `test_intent_router_backend_v1.py` | 高 |
| `rag_conversation_logs` 表结构含 `session_id/query/response/metadata` | `supabase/sql/create_rag_conversation_logs.sql` L6–15 | SQL 阅读 | 高 |
| Code RAG 表为 `code_chunks`，独立 RPC `match_code_chunks`/`keyword_code_chunks` | `supabase/sql/code_chunks.sql` L12–114 | SQL 阅读 | 高 |
| ingest 后调用 `refresh_documents_fts_tokens_for_paths` 兜底 | `api/ingest_pipeline.py` L301–308、L368–375 | 代码阅读 | 高 |
| Manifest 校验脚本检查 endpoint/env/table/RPC/anchors | `tools/tech_graph_manifest_check.py` L229–328 | 代码阅读 / 本地执行 | 高 |
| Contract 校验脚本检查 SSE event/chain.type/payload keys | `tools/tech_graph_contract_check.py` L222–436 | 代码阅读 / 本地执行 | 高 |
| CI 在 PR/push 时自动跑 manifest + contract 校验 | `.github/workflows/tech-graph.yml`、`.github/workflows/tech-graph-contract.yml` | 文件阅读 | 高 |
| `TEXT2SQL_DATABASE_URL` 用于直连 Postgres 执行 SQL | `api/text2sql_core.py` L88 | 代码阅读 | 高 |
| Text2SQL store 从 `docs/text2sql/v1/sql/supabase_init.sql` 解析 DDL | `api/text2sql_store.py` L169–172 | 代码阅读 | 高 |
| `api/index.py` 通过 `bind_index_symbols` 向 `code_retrieval` 注入共享函数 | `api/index.py` L234–243、`api/code_retrieval.py` L578–600 | 代码阅读 | 高 |

---

## 8. 不确定性与验证步骤

| 不确定性 | 说明 | 建议验证 |
|----------|------|----------|
| `docs/text2sql/v1/sql/supabase_init.sql` 与 `docs/text2sql/v1/spec/SAMPLES-01-text2sql-mini.md` 的具体内容 | 本任务未读取这两个文件；Text2SQL store 的 DDL/示例质量依赖它们 | 打开 `docs/text2sql/v1/sql/supabase_init.sql` 确认表定义是否与实际业务库一致 |
| `vercel.json` 的精确配置 | AGENTS.md 提到 Vercel 入口指向 `api/index.py`，但未读取该文件 | 打开 `vercel.json` 确认 `builds`/`routes` 配置 |
| 前端消费 SSE 的具体实现 | `_contract_manifest.json` 提到前端文件路径 `../ai-ink-brain/...`，但本任务未读取前端仓库 | 如需修改 SSE 键集，必须 checkout 前端仓库并运行 `tech_graph_contract_check.py` |
| `.cursorrules` 的完整内容 | AGENTS.md 与 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 均引用 `.cursorrules`，但本任务未读取 | 如需遵循 RAG 工程约束，应打开 `.cursorrules` 全文 |
| `data/i18n_glossary.json` 的词条覆盖度 | `api/rag_recall_tools.py` 读取该文件做 i18n expand，但本任务未读取 | 检查该文件是否存在及关键术语是否覆盖 |
| 生产环境是否启用 `API_KEY` 鉴权 | `api/index.py` 中 `_require_auth` 同时检查 `admin_secret` 和 `API_KEY`，但 `.env.example` 未列出 `API_KEY` | 检查生产环境变量或 `.env.local` 是否配置了 `API_KEY` |
| `docs/tasks/` 中的任务规格 | AGENTS.md 提到任务驱动，但本任务未读取 `docs/tasks/*.md` | 如需实现新功能，应先读取对应任务文件 |

---

## 9. 消耗明细

### 时间估算

| 阶段 | 时长 | 依据 |
|------|------|------|
| `t_scan`（文件枚举、glob、快速浏览） | ~3 min | 19 个 api/*.py + 6 个 SQL + 9 个 tests + meta + manifest + tools + workflows |
| `t_read`（逐行精读核心文件） | ~18 min | 核心文件约 5000 行，按 250 行/min 估算 |
| `t_synthesis`（整理、写报告、交叉核对） | ~12 min | 锚点表、FAQ、配方卡、断言清单 |
| **t_total** | **~33 min** | 估算 |

### Token 估算

| 类别 | 行数 | 系数 | 估算 tokens |
|------|------|------|-------------|
| Python 代码（api/*.py + tests/*.py + tools/*.py） | ~6800 | 12 | ~81,600 |
| SQL 文件 | ~515 | 12 | ~6,180 |
| Markdown 文档（meta + 本报告输入 prompt） | ~213 | 10 | ~2,130 |
| manifest/contract JSON | ~258 | 10 | ~2,580 |
| 命令/grep 输出 | ~50 | 8 | ~400 |
| **输入合计** | — | — | **~92,890** |
| 本报告输出（中文为主） | ~550 行 × 约 30 字 | 4 字/token | **~4,125** |

> 公式：中文正文 ≈ 4 字符 / 1 token；代码/SQL ≈ 12 tokens/行；Markdown ≈ 10 tokens/行。

---

## 10. 覆盖率

### 已完整读取的文件（逐行或接近逐行）

- `api/index.py`（1053 行，全读）
- `api/unified_chat.py`（1080 行，全读）
- `api/ingest_pipeline.py`（438 行，全读）
- `api/rag_recall_tools.py`（541 行，全读）
- `api/text2sql_api.py`（193 行，全读）
- `api/database_manager.py`（92 行，全读）
- `api/rag_env.py`（97 行，全读）
- `api/chain_chat.py`（325 行，全读）
- `api/intent_router.py`（237 行，全读）
- `api/hybrid_fusion.py`（55 行，全读）
- `api/keyword_fallback.py`（194 行，全读）
- `api/query_rewrite.py`（64 行，全读）
- `api/rag_logging.py`（85 行，全读）
- `api/code_ingest.py`（255 行，全读）
- `api/code_parser.py`（183 行，全读）
- `api/code_retrieval.py`（600 行，全读）
- `api/text2sql_core.py`（179 行，全读）
- `api/text2sql_store.py`（185 行，全读）
- `supabase/sql/init.sql`（90 行，全读）
- `supabase/sql/hybrid_search.sql`（224 行，全读）
- `supabase/sql/create_rag_conversation_logs.sql`（22 行，全读）
- `supabase/sql/code_chunks.sql`（143 行，全读）
- `supabase/sql/patch_match_documents_threshold.sql`（34 行，全读）
- `supabase/sql/match_documents.sql`（2 行，仅注释，已确认合并到 init.sql）
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（150 行，全读）
- `docs/_tech_graph/_manifest.json`（196 行，全读）
- `docs/_tech_graph/_contract_manifest.json`（62 行，全读）
- `tools/tech_graph_manifest_check.py`（329 行，全读）
- `tools/tech_graph_contract_check.py`（438 行，全读）
- `.github/workflows/tech-graph.yml`（23 行，全读）
- `.github/workflows/tech-graph-contract.yml`（37 行，全读）
- `tests/test_unified_chat_backend_v1.py`（357 行，全读）
- `tests/test_unified_chat_streaming_sse.py`（142 行，全读）
- `tests/test_intent_router_backend_v1.py`（178 行，全读）
- `tests/test_code_api_routes.py`（384 行，全读）
- `.env.example`（40 行，全读）
- `requirements.txt`（10 行，全读）
- `main.py`（10 行，全读）

### 未读取的文件（抽样或跳过）

- `tests/test_admin_ingest_route.py`、`test_chain_chat_events.py`、`test_code_ingest_process.py`、`test_code_ingest_text.py`、`test_code_parser.py`：已通过其他测试文件和源码推断其覆盖范围，未逐行阅读。
- `tools/tech_graph_contract_demo.py`、`tech_graph_drift_check.py`、`tech_graph_render_ai.py`：未阅读；但已知 `manifest_check.py` 会提示运行 `render_ai.py`。
- `docs/_tech_graph/*.md`、`*.ai.md`：**按 Prompt 强制约束禁止读取**。
- `docs/tasks/*.md`：未读取；AGENTS.md 建议任务驱动时阅读。
- `docs/text2sql/v1/sql/supabase_init.sql`、`docs/text2sql/v1/spec/SAMPLES-01-text2sql-mini.md`：未读取；被 `text2sql_store.py` 引用。
- `data/i18n_glossary.json`：未读取；被 `rag_recall_tools.py` 引用。
- `web/assistant_ticket_bot-3.py`：未读取；不在核心链路。
- `scripts/validate_mermaid.py`：未读取。
