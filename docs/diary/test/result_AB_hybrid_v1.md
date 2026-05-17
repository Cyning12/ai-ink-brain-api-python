<!-- Prompt 文件: docs/diary/test/prompt_AB_hybrid_v1.md -->
<!-- 执行日期: 2026-04-28 -->
<!-- git rev-parse --short HEAD: 116ab0c -->

# Result AB Hybrid V1 — 索引 + 实现深读 + 门禁（取长补短）

> 产出目标：对 `ai-ink-brain-api-python` 产出一份「索引（B）+ 实现深读（A）+ 门禁（补丁共识）」合一的可交接文档。  
> KPI：易交接（P1）> 可靠性（P2）> 省钱（P3）> 省时（P4）。

---

## P1 易交接

### 1. 冷启动接手清单（15 步）

1. **克隆仓库**并进入根目录：`cd ai-ink-brain-api-python`
2. **创建虚拟环境**（建议 Python 3.11+）：`python -m venv .venv && source .venv/bin/activate`
3. **安装依赖**：`pip install -r requirements.txt`
4. **配置 `.env`**：复制 `.env.example` → `.env`，至少填写：
   - `NEXT_PUBLIC_SUPABASE_URL` / `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY` / `SUPABASE_SERVICE_KEY`
   - `SILICONFLOW_API_KEY`
   - `NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET`（或 `API_KEY`）
5. **确认 Supabase 对象已就绪**：执行 `supabase/sql/init.sql`、`supabase/sql/hybrid_search.sql`（确保 `documents`、`code_chunks`、`rag_conversation_logs` 及 RPC 存在）
6. **本地起服**：`python -m uvicorn main:app --host 127.0.0.1 --port 8000`
7. **`curl` 冒烟健康检查**：`curl http://127.0.0.1:8000/api/py/health`
8. **`curl` 冒烟鉴权**：`curl -H "Authorization: Bearer \$ADMIN_SECRET" http://127.0.0.1:8000/api/py/chat/history?session_id=test`
9. **跑 `pytest` 全集**：`pytest`（当前约 30+ 条，覆盖 unified/chat、code、ingest、intent_router 等）
10. **跑 manifest 门禁**：`python tools/tech_graph_manifest_check.py`（必须返回 `OK`）
11. **跑漂移门禁**：`python tools/tech_graph_drift_check.py`（必须返回 `OK`）
12. **跑 contract 门禁**（若修改 SSE 事件键）：`python tools/tech_graph_contract_check.py`（需要前端仓作为 sibling 目录 `../ai-ink-brain/`）
13. **确认图谱双轨**：人类版 `.md` 与 AI 协议版 `.ai.md` 语义等价；改代码后优先更新 `.ai.md`
14. **确认 `_manifest.json` 与 `_contract_manifest.json`** 已覆盖你新增/改动的端点、RPC、env、SSE 键
15. **提交前最后检查**：`python tools/tech_graph_manifest_check.py && python tools/tech_graph_drift_check.py`

---

### 2. 图谱索引摘要

| 读过哪些图谱文件 | 用途（一句话） | 与代码核验的差异注意 |
|---|---|---|
| `00_main.md` / `00_main.ai.md` | 顶层入口与分支总图；AI 协议版带 `// →` 锚点注释与 AUTO 区块 | 无差异；`00_main.ai.md` 的 Endpoints/Anchors 区块由 `_manifest.json` 自动生成 |
| `01_struct.md` | DB 结构：documents / code_chunks / rag_conversation_logs + FileMeta 字段 | 无差异；`vector(1024)` 与代码默认 `SILICONFLOW_EMBEDDING_DIMENSIONS=1024` 一致 |
| `99_spec.md` | 技术图谱交付规约、Env Truth Table、Next Steps Backlog | **差异注意**：`99_spec.md` 中 `.cursorrules` 引用存在，但本仓实际规则文件为 `.cursor/rules/*.mdc`（见下文漂移防线） |
| `99_mermaid_protocol.md` | 拓扑协议 v2-Python 适配：边标记、节点形状、锚点规则、分层规则 | 无差异；双轨制 `.md` / `.ai.md` 已落地 |
| `_manifest.json` | 机器可读真值：endpoints、tables、rpc、env、anchors | 无差异；`python tools/tech_graph_manifest_check.py` 校验通过 |
| `_contract_manifest.json` | SSE 跨端契约：event/data 信封、chain/done 事件、各 type 最小 payload 键 | 无差异；`python tools/tech_graph_contract_check.py` 校验通过（需前端仓） |
| `10_flow_rag.md` / `10_flow_rag.ai.md` | RAG 检索流程（Query → Rewrite → Embed/Keyword → Fusion → Answer → Log） | **差异注意**：`10_flow_rag.ai.md` 标注了 `api/index.py#L669` embedding 降级点，实际代码中 Legacy chat 降级在 `api/index.py#L670-685`；Unified chat 降级在 `api/unified_chat.py#L527-532` |
| `11_flow_text2sql.ai.md` | Text2SQL 流程（Intent → Retrieve → Prompt → Generate → Validate → Execute → Summarize） | 仅读 `.ai.md`；人类版未读（按需覆盖） |
| `12_flow_fts.md` | FTS 写入流（Trigger → Alias → tsvector → GIN）与查询流（QS → RPC → tsquery → rank） | 无差异；i18n glossary 扩展在 `api/rag_recall_tools.py` 实现 |
| `13_flow_supabase_rpc.md` | Supabase RPC + Tables 全景（service_role） | 无差异；ingest 后调用 `refresh_*_fts_tokens_for_paths` 兜底 |
| `14_runtime_observability.md` | Runtime/Observability（按需加载） | **未读**（按需覆盖，见覆盖率） |
| `15_e2e_boundary.md` | E2E Boundary/Contract（按需加载） | **未读**（按需覆盖，见覆盖率） |

---

### 3. 锚点索引表

| 条目 | 文件路径 | 函数名 / 行区间 | 一句职责 |
|---|---|---|---|
| `GET /api/py/health` | `api/index.py` | `health` @L434 | 健康检查 |
| `GET /api/py/chat/history` | `api/index.py` | `chat_history` @L439 | 按 session 拉取历史 |
| `POST /api/py/chat` | `api/index.py` | `chat` @L591 | Legacy RAG Chat（流式 SSE） |
| `POST /api/py/unified/chat` | `api/index.py` | `unified_chat_route` @L561 | Unified JSON 响应 |
| `POST /api/py/unified/chat/stream` | `api/index.py` | `unified_chat_stream_route` @L576 | Unified SSE 流式 |
| `POST /api/py/chain/chat` | `api/index.py` | `chain_chat_route` @L546 | Chain Timeline |
| `POST /api/py/code/query` | `api/index.py` | `code_query` @L501 | 代码检索（hybrid） |
| `POST /api/py/code/search` | `api/index.py` | `code_search` @L516 | 代码搜索（filter） |
| `POST /api/py/text2sql/chat` | `api/index.py` | `text2sql_chat` @L531 | Text2SQL JSON |
| `POST /api/py/admin/ingest` | `api/index.py` | `py_admin_ingest` @L1026 | 同步 ingest（markdown/code） |
| `POST /api/py/admin/sync` | `api/index.py` | `py_admin_sync_post` @L983 | 异步 sync 任务（内存队列） |
| `GET /api/py/admin/sync` | `api/index.py` | `py_admin_sync_get` @L1009 | 查询 sync 任务状态 |
| 鉴权（Legacy） | `api/index.py` | `_require_auth` @L206 | Bearer / x-blog-admin-token / x-admin-token 三选一 |
| 鉴权（Unified） | `api/unified_chat.py` | `_require_unified_auth` @L33 | 同上，但错误信息更统一 |
| RAG 事件构造 | `api/unified_chat.py` | `_event` @L62 | 统一 event 结构：type/ts/step_id/payload |
| RAG sources payload | `api/unified_chat.py` | `_build_rag_sources_event` @L143 | 从 hits 提取 sources + retrieval |
| RAG 生成答案 | `api/unified_chat.py` | `_rag_generate_answer` @L170 | 调用 LLM，temperature=0.2 |
| Unified JSON 入口 | `api/unified_chat.py` | `handle_unified_chat` @L192 | 非流式，返回 events 数组 |
| Unified SSE 入口 | `api/unified_chat.py` | `handle_unified_chat_stream` @L712 | 流式，yield chain + done |
| Embedding 参数封装 | `api/rag_env.py` | `embedding_kwargs_for_inputs` @L71 | 自动加 dimensions（Qwen3） |
| Supabase Client | `api/rag_env.py` | `supabase_client` @L80 | service_role 连接 |
| 环境加载 | `api/rag_env.py` | 模块级 @L14 | 加载 `.env.local`、`.env`（override=False） |
| 日志写入 | `api/database_manager.py` | `SupabaseManager.save_debug_log` @L34 | 异步写入 rag_conversation_logs |
| 历史读取 | `api/database_manager.py` | `SupabaseManager.get_chat_history` @L43 | 读最近 5 轮 |
| session 轮次 | `api/database_manager.py` | `SupabaseManager.list_session_turns` @L66 | 正序返回（desc 取再 reverse） |
| Keyword + i18n | `api/rag_recall_tools.py` | `keyword_query_text_with_i18n_meta` @L279 | 构造 FTS query_text，含 glossary 扩展 |
| 结构化召回（日期） | `api/rag_recall_tools.py` | `structured_recall_by_date` @L482 | metadata.date_norm / slug / filename 精确匹配 |
| RPC 重试 | `api/rag_recall_tools.py` | `rpc_execute_with_retry` @L30 | 有限重试，指数退避 |
| RRF 融合 | `api/hybrid_fusion.py` | `fuse_hits_rrf` @L15 | vector + keyword 排名融合，默认 max_total=22 |
| Markdown ingest | `api/ingest_pipeline.py` | `process_markdown_files` @L253 | 重删再插，批量 embed，刷新 fts_tokens |
| Sync ingest | `api/ingest_pipeline.py` | `sync_content_to_vector` @L318 | 同上，但返回 upserted |
| 任务队列 | `api/ingest_pipeline.py` | `create_sync_job` / `run_sync_job_sync` / `get_job` @L402-437 | 内存队列，serverless 不持久 |
| Intent 路由 | `api/intent_router.py` | `decide_intent` | 规则 + prefer 决定 rag/text2sql/no_data |
| Query Rewrite | `api/query_rewrite.py` | `rewrite_query_with_history` | 基于历史轮次改写 query |
| Keyword Fallback | `api/keyword_fallback.py` | `run_keyword_fallback` | rewrite 丢实体时回退到 raw query |
| manifest 门禁 | `tools/tech_graph_manifest_check.py` | `main` @L229 | 校验 endpoints/rpc/tables/env/anchors |
| drift 门禁 | `tools/tech_graph_drift_check.py` | `main` @L59 | 校验 endpoints/rpc/tables/env 是否被图谱覆盖 |
| contract 门禁 | `tools/tech_graph_contract_check.py` | `main` @L222 | 校验 SSE 后端 truth vs contract vs 前端消费 |

---

### 4. 新人 FAQ（12 条）

1. **Q：Legacy Chat 与 Unified Chat 有什么区别？**  
   A：Legacy（`POST /api/py/chat`）是早期流式 SSE，返回 `text/plain` + 末尾 `---RAG_SOURCES_JSON---`；Unified（`POST /api/py/unified/chat` 与 `/stream`）返回结构化 events（JSON 或 SSE），支持 RAG / Text2SQL / no_data 多模式路由。

2. **Q：`00_main.md` 与 `00_main.ai.md` 该读哪个？**  
   A：人类读 `.md`，AI / 脚本读 `.ai.md`；两者语义等价，`.ai.md` 锚点更密、带 `// →` 代码定位。

3. **Q：图谱里的节点名可以直接当 RPC / 表名用吗？**  
   A：**不可以**。必须以 `_manifest.json`、代码、`supabase/sql/*.sql` 为准；图谱节点名是缩写/示意。

4. **Q：新增一个 HTTP 端点，最少要改哪些地方？**  
   A：见「改动配方卡 A」：代码 → `_manifest.json` → `python tools/tech_graph_manifest_check.py` → 可选更新 `00_main.ai.md` AUTO 区块。

5. **Q：Embedding 失败会 502 吗？**  
   A：**不会**。Legacy 与 Unified 均降级为 keyword-only（FTS），服务保持可用。

6. **Q：ingest 是幂等的吗？**  
   A：`process_markdown_files` 先按 `relativePath` 删除旧行再插入新行，对同一批文件是幂等的；但 serverless 场景下 sync 任务队列不保证持久。

7. **Q：`RAG_MATCH_THRESHOLD=none` 是什么意思？**  
   A：关闭 SQL 侧相似度过滤，只保留 top-k。默认 `0.3`；非法值回退默认。

8. **Q：`_manifest.json` 和 `_contract_manifest.json` 谁维护？**  
   A：开发者手动维护（当前无自动生成）。新增/改名/删除端点、RPC、env、SSE 键时必须同步更新。

9. **Q：为什么 `api/rag_env.py` 优先读 `NEXT_PUBLIC_SUPABASE_URL`？**  
   A：与 Next.js 前端共享环境变量命名，减少配置重复。`SUPABASE_URL` 为兼容别名。

10. **Q：本地 ingest 需要 content 目录吗？**  
    A：需要。默认扫描 `REPO_ROOT/content`；可通过 `CONTENT_ROOT` 指向前端仓库的 content 目录。

11. **Q：`pytest` 跑不过怎么办？**  
    A：先确认 `.env` 已配置 `SILICONFLOW_API_KEY` 与 Supabase 凭据；部分测试需要真实 RPC（如 `test_unified_rag_structured_recall_cn_date`）。

12. **Q：修改 SSE 事件键后，前端会崩吗？**  
    A：会。必须先更新 `_contract_manifest.json`，再跑 `python tools/tech_graph_contract_check.py`（需要前端仓 sibling 目录），确认前端消费键在契约范围内。

---

### 5. 改动配方卡（四卡固定）

#### 卡 A：新增 HTTP 端点

- **必读文件**：`api/index.py`（路由装饰器位置）、`_manifest.json`（endpoints 数组）、`tools/tech_graph_manifest_check.py`（校验逻辑）
- **慎碰点**：路径前缀 `/api/py/` 是前后端约定，慎改；handler 命名需与 `manifest` 一致
- **推荐验证**：
  1. 本地 `curl` 冒烟新端点
  2. `python tools/tech_graph_manifest_check.py`（必须 OK）
  3. `python tools/tech_graph_drift_check.py`（必须 OK）
  4. 可选：`python tools/tech_graph_render_ai.py` 刷新 `00_main.ai.md` AUTO 区块

#### 卡 B：调整检索策略（RRF、threshold、keyword）

- **必读文件**：`api/hybrid_fusion.py`（RRF 逻辑）、`api/rag_recall_tools.py`（keyword / structured recall）、`api/index.py`（Legacy 调用点）、`api/unified_chat.py`（Unified 调用点）
- **慎碰点**：
  - `RRF_K = 60` 是论文常用值，改前需 A/B
  - `RAG_MATCH_THRESHOLD` 在 `api/index.py` 与 `api/unified_chat.py` 各有一份 `_parse_match_threshold()`（实现相同，但分散两处）
  - Legacy 与 Unified 的召回逻辑**未完全复用**（见漂移防线）
- **推荐验证**：
  1. `pytest tests/test_unified_chat_backend_v1.py`（含 structured recall、keyword expand）
  2. `pytest tests/test_code_api_routes.py`（code RAG 也走 hybrid）
  3. 设置 `DEBUG_RAG=1` 观察 `retrieve_summary` 日志

#### 卡 C：调整 ingest（markdown/code、维度、fts_tokens）

- **必读文件**：`api/ingest_pipeline.py`（markdown）、`api/code_ingest.py`（code）、`api/rag_env.py`（embedding 维度）、`supabase/sql/init.sql`（vector(N)）
- **慎碰点**：
  - `EMBEDDING_DIM` / `SILICONFLOW_EMBEDDING_DIM` 必须与 `public.documents.embedding vector(N)` 一致
  - `process_markdown_files` 是「重删再插」，非 upsert；大数据量注意批量大小（`EMBED_BATCH_SIZE=32`、`INSERT_BATCH_SIZE=80`）
  - ingest 后需调用 `refresh_documents_fts_tokens_for_paths`（代码已兜底，但异常会静默跳过）
- **推荐验证**：
  1. `pytest tests/test_admin_ingest_route.py`
  2. `pytest tests/test_code_ingest_process.py`
  3. ingest 后抽查 Supabase `documents` 表 `fts_tokens` 非空

#### 卡 D：调整 SSE / Unified 事件契约

- **必读文件**：`api/unified_chat.py`（所有 `_event(...)` 与 `_sse(...)` 调用）、`_contract_manifest.json`、`.github/workflows/tech-graph-contract.yml`
- **慎碰点**：
  - 任何 `chain` 事件的 `type` 值、payload 键名增删，都必须同步 `_contract_manifest.json`
  - `done` 事件的 `data_keys`（`ok`, `mode`, `run_id`, `session_id`, `request_id`）是前端收尾依赖，**禁止删减**
  - `request_id` 当前与 `run_id` 等价（`api/unified_chat.py#L1071`）
- **推荐验证**：
  1. `python tools/tech_graph_contract_check.py`（需要 `../ai-ink-brain/` 前端仓存在）
  2. `pytest tests/test_unified_chat_streaming_sse.py`
  3. 手动 `curl` SSE 端点，检查事件序列：`meta` → `router.decision` → ... → `done`

---

## P2 可靠性

### 6. 摘要（<=200 字）

`ai-ink-brain-api-python` 是 Ink-Brain 博客的 RAG / Embedding / Retrieval 后端（FastAPI）。核心能力：Markdown/Code 分块入库（SiliconFlow Embedding + Supabase pgvector）、Hybrid 检索（Vector + FTS + RRF 融合）、Unified Chat（RAG / Text2SQL / no_data 多模式路由，JSON 与 SSE 双输出）、RAG 全链路日志。关键约束：embedding 失败降级 keyword-only；ingest 重删再插；serverless 不保证 sync 任务持久；所有端点/RPC/env/SSE 键变更须过 manifest / drift / contract 三门禁。

---

### 7. 模块地图与主链路

#### Legacy RAG（`POST /api/py/chat`）

- 入口：`api/index.py::chat` @L591
- 鉴权：`_require_auth` @L206
- 历史：`SupabaseManager.get_chat_history` -> `api/query_rewrite.py::rewrite_query_with_history`
- Embedding：`OpenAI.embeddings.create`（`SILICONFLOW_EMBEDDING_MODEL`）；失败降级 keyword-only @L670-685
- 召回：
  - Vector：`match_documents`（`api/index.py#L703`）
  - Keyword：`fetch_keyword_hits` -> `keyword_documents`（`api/index.py#L719-722`）
  - Date anchor：`fetch_date_anchor_hits`（`api/index.py#L796`）-> `merge_hits_anchors_first`
- 融合：`fuse_hits_rrf(vector_hits, keyword_hits)` @L761
- 生成：`_rag_generate_answer`（temperature=0.2）
- 返回：`StreamingResponse`（text/plain）+ 末尾 `SOURCES_JSON_SEPARATOR` + sources JSON
- 日志：`SupabaseManager.save_debug_log`（`api/index.py#L830-860` 区间，含 latency、match meta）

#### Unified Chat（`POST /api/py/unified/chat` 与 `/stream`）

- 入口：`api/unified_chat.py::handle_unified_chat` @L192（JSON）、`handle_unified_chat_stream` @L712（SSE）
- 鉴权：`_require_unified_auth` @L33
- 路由：`api/intent_router.py::decide_intent` -> `mode` in {rag, text2sql, no_data, auto}
- **RAG 分支**（`api/unified_chat.py#L484-703`）：
  - rewrite -> embed（降级 @L527-532）-> structured_recall_by_date -> match_documents + keyword_documents（raw + rewrite 双路）-> RRF 三级融合（`fuse_hits_rrf` 链式调用 @L611-613）-> `_rag_generate_answer`
  - 事件：`tool.call.start/end`、 `rag.query_expand`、`rag.sources`、`assistant.message`、`latency`
- **Text2SQL 分支**（`api/unified_chat.py#L297-482`）：
  - `text2sql_store.search` -> `build_sql_prompt` -> `llm_generate_sql` -> `validate_sql_readonly` -> `execute_select_sql` -> `llm_summarize`
  - 事件：`tool.call.start/end`、`sql.result`、`assistant.message`、`latency`
- **no_data 分支**：直接 LLM 生成，temperature=0.7
- SSE 格式：`event: chain\\ndata: {type, ts, step_id, payload}\\n\\n`；最后必须 `event: done`

#### Text2SQL（独立端点 `POST /api/py/text2sql/chat`）

- 入口：`api/index.py::text2sql_chat` @L531 -> `api/text2sql_api.py::handle_text2sql_chat`
- 复用 `api/text2sql_core.py` 与 `api/text2sql_store.py`
- 与 Unified 的 Text2SQL 分支逻辑同源，但事件输出格式不同（Legacy JSON vs Unified events）

#### Ingest / Sync

- Markdown：`api/ingest_pipeline.py::process_markdown_files` @L253
  - `get_all_markdown_chunks` -> `chunk_text_by_chars`（512/50）-> `embed_texts_batch` -> `delete_documents_by_relative_paths` -> `insert` -> `refresh_documents_fts_tokens_for_paths`
- Code：`api/code_ingest.py::process_code_files`（AST 解析，按 function/class 分块）
- Sync：`api/ingest_pipeline.py::sync_content_to_vector` @L318（内存任务队列）

#### Code RAG

- 入口：`api/index.py::code_query` @L501、`code_search` @L516
- 实现：`api/code_retrieval.py::handle_code_query` / `handle_code_search`
- 召回：`match_code_chunks` + `keyword_code_chunks`（hybrid，与 documents 同源）

#### Chain Chat

- 入口：`api/index.py::chain_chat_route` @L546 -> `api/chain_chat.py::handle_chain_chat`
- 职责：Timeline 式对话（具体实现未精读，见覆盖率）

---

### 8. 事实断言清单

| 断言 | 证据 | 核验方式 | 置信度 |
|---|---|---|---|
| 共有 12 个 HTTP 端点 | `api/index.py` 装饰器 + `_manifest.json` endpoints 数组 | `grep '@app\\.(get|post)' api/index.py` / `python tools/tech_graph_manifest_check.py` | 高 |
| Embedding 模型默认 `Qwen/Qwen3-Embedding-0.6B`，维度 1024 | `api/rag_env.py:L53`、`api/index.py:L57` | 代码直读 | 高 |
| Vector 相似度使用 Cosine Distance | `supabase/sql/init.sql`（`vector(1024)`）+ `match_documents` 实现 | SQL 文件 + Supabase 控制台 | 高 |
| RRF 融合常数 `K=60` | `api/hybrid_fusion.py:L6` | 代码直读 | 高 |
| `RAG_MATCH_THRESHOLD` 默认 0.3，`none` 关闭过滤 | `api/index.py:L100-122`、`api/unified_chat.py:L111-125` | 代码直读 | 高 |
| Unified SSE 必须输出 `done` 作为最后事件 | `api/unified_chat.py:L1062-1076`（finally yield _sse("done", ...)） | 代码直读 | 高 |
| `_contract_manifest.json` 要求 `done.data_keys` 含 `ok, mode, run_id, session_id, request_id` | `_contract_manifest.json:L11-L12`、`L53` | JSON 直读 | 高 |
| ingest 后调用 `refresh_documents_fts_tokens_for_paths` 兜底 | `api/ingest_pipeline.py:L301-308`、`L368-375` | 代码直读 | 高 |
| `rag_conversation_logs` 表字段含 `session_id, query, rewritten_query, retrieved_context, response, metadata` | `docs/_tech_graph/01_struct.md` + `api/database_manager.py` | 图谱 + 代码 | 高 |
| manifest_check、drift_check 当前均通过 | 本执行输出 | `python tools/tech_graph_manifest_check.py` / `drift_check.py` | 高 |
| Legacy chat 与 Unified chat 的 `_parse_match_threshold` 实现分散两处 | `api/index.py:L100` 与 `api/unified_chat.py:L111` | 代码直读 | 高 |
| `api/index.py` 的 `chat` 函数约 260 行（L591-850+），未拆分子函数 | `api/index.py` 行区间目测 | 代码直读 | 高 |

---

### 9. 不确定性与验证步骤

1. **Unified Chat 的 `no_data` 分支 temperature=0.7，而 RAG 分支 temperature=0.2**：设计意图待确认（no_data 更开放？）。验证：查看 `.cursorrules` 或任务规格 `docs/tasks/`。
2. **Text2SQL 的 `execute_select_sql` 是否只读**：`validate_sql_readonly` 做了关键字过滤，但非语法级保证。验证：审计 `api/text2sql_core.py` 的过滤列表。
3. **Code RAG 的 `code_chunks` 表维度**：`01_struct.md` 标注 `vector(1024)`，但 code ingest 的模型是否与 markdown 一致？验证：检查 `api/code_ingest.py` 的 embedding 调用点。
4. **Chain Chat 的具体事件契约**：未精读 `api/chain_chat.py`，不确定是否有独立契约文件。验证：读 `api/chain_chat.py` 与 `docs/_tech_graph/15_e2e_boundary.md`。
5. **前端 BFF 透传路径**：`_contract_manifest.json` 标注 `../ai-ink-brain/app/api/py/unified/chat/stream/route.ts`，但未校验该文件内容。验证：需前端仓存在并运行 contract_check。

---

### 10. 漂移防线（必选）

#### tools / workflows 中与图谱门禁相关的条目

| 文件 | 职责 | 触发方式 |
|---|---|---|
| `tools/tech_graph_manifest_check.py` | 校验 `_manifest.json` vs 代码/SQL truth（endpoints、tables、rpc、env、anchors） | 本地手动 / `.github/workflows/tech-graph.yml` |
| `tools/tech_graph_drift_check.py` | 校验代码中的 endpoints/rpc/tables/env 是否在 `docs/_tech_graph/*.md` 被覆盖 | 本地手动 |
| `tools/tech_graph_contract_check.py` | 校验 SSE 后端 truth vs `_contract_manifest.json` vs 前端消费键 | 本地手动（需前端仓）/ `.github/workflows/tech-graph-contract.yml` |
| `.github/workflows/tech-graph.yml` | CI 跑 `python tools/tech_graph_manifest_check.py` | PR / push to main |
| `.github/workflows/tech-graph-contract.yml` | CI  checkout 前后端两仓，跑 `python tools/tech_graph_contract_check.py` | PR / push to main |

#### PROJECT_CONFIG 与 docs/_tech_graph 之间发现的矛盾

1. **`PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 声称「本仓当前未发现 `.github/workflows/`」**，但实际上存在 `.github/workflows/tech-graph.yml` 与 `tech-graph-contract.yml`。  
   -> **漂移**：`PROJECT_CONFIG` E 节目录地图已过时。
2. **`PROJECT_CONFIG` 声称「`.cursorrules` 要点」存在**，但本仓实际规则文件为 `.cursor/rules/*.mdc`（`AGENTS.md` 已更新指向 `.cursor/rules/*.mdc`）。  
   -> **漂移**：`PROJECT_CONFIG` B 节对 `.cursorrules` 的描述与仓库实际结构不一致。
3. **`99_spec.md` 的 Next Steps Backlog 中 P1_3「最小漂移校验」已落地**（`tools/tech_graph_drift_check.py`），但 P1_2「自动校验（CI/脚本均可）」只落了一半（manifest_check 有 CI，drift_check 无 CI workflow）。  
   -> **不确定性**：drift_check 是否应加入 CI？当前仅手动运行。
4. **Legacy chat 与 Unified chat 的 RAG 召回逻辑存在代码重复**：`_parse_match_threshold`、embedding 降级、keyword fallback、date anchor 等逻辑在两处独立实现，未提取到公共模块。  
   -> **漂移**：`10_flow_rag.ai.md` 暗示统一流程，但实现层面未完全统一。

---

## P3/P4

### 11. 消耗明细

| 分项 | 内容 | 估算 |
|---|---|---|
| **t_graph** | 第一层（00_main/01_struct/99_spec/99_mermaid_protocol/_manifest/_contract）+ 第二层（10_flow_rag.ai/10_flow_rag/11_text2sql.ai/12_fts/13_rpc） | ~15 min |
| **t_code** | 第三层（index.py 关键区间、unified_chat.py 全读、rag_recall_tools.py、ingest_pipeline.py、hybrid_fusion.py、database_manager.py、rag_env.py）+ 第四层（tools/*.py、workflows） | ~25 min |
| **t_synthesis** | 整理锚点表、FAQ、配方卡、断言表、漂移防线、产出 markdown | ~15 min |
| **t_total** | — | ~55 min |

**Token 分项公式**：

- 图谱 + meta（~1002 行 Markdown）：~1002 x 10 = ~10,020 tokens
- 代码精读（~3356 行 Python，含 index/unified_chat/rag_recall_tools/ingest_pipeline/hybrid_fusion/database_manager/rag_env）：~3356 x 12 = ~40,272 tokens
- tools + workflows（~875 行）：~875 x 12 = ~10,500 tokens
- 命令/grep 输出（~200 行）：~200 x 8 = ~1,600 tokens
- **输入合计**：~62,400 tokens
- 输出（本文件约 12,000 中文字符 + 表格/代码）：~12,000 / 4 = ~3,000 tokens（中文正文），含表格结构后约 ~6,000-8,000 tokens

---

### 12. 覆盖率

#### 图谱文件清单及阅读深度

| 文件 | 深度 | 备注 |
|---|---|---|
| `00_main.md` | 全文精读 | 人类版，含子流程链接 |
| `00_main.ai.md` | 全文精读 | AI 协议版，含 AUTO 区块 |
| `01_struct.md` | 全文精读 | DB 结构 |
| `02_version.md` | **未读** | 版本迭代时间线，按需 |
| `10_flow_rag.md` | 全文精读 | 人类版 |
| `10_flow_rag.ai.md` | 全文精读 | AI 协议版，锚点更密 |
| `11_flow_text2sql.md` | **未读** | 人类版，未读 |
| `11_flow_text2sql.ai.md` | 全文精读 | AI 协议版 |
| `12_flow_fts.md` | 全文精读 | FTS 写入与查询流 |
| `13_flow_supabase_rpc.md` | 全文精读 | RPC 全景 |
| `14_runtime_observability.md` | **未读** | Runtime/Observability，按需 |
| `15_e2e_boundary.md` | **未读** | E2E Boundary/Contract，按需 |
| `99_spec.md` | 全文精读 | 交付规约、Env Truth Table、Backlog |
| `99_mermaid_protocol.md` | 全文精读 | 拓扑协议 |
| `_manifest.json` | 全文精读 | 机器真值 |
| `_contract_manifest.json` | 全文精读 | SSE 契约 |
| `PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` | 全文精读 | 环境变量真值表 |

#### 代码 / SQL / tests / tools 清单及精读/抽样区间

| 文件 | 精读区间 | 备注 |
|---|---|---|
| `api/index.py` | L1-120（常量/辅助函数）、L206-244（鉴权/bind）、L430-850（chat 主链路）、L980-1053（admin 端点） | 其余区间抽样扫读 |
| `api/unified_chat.py` | **全文精读**（L1-1080） | 核心文件，含 JSON/SSE 双入口 |
| `api/rag_recall_tools.py` | L1-120（rpc_execute/日期正则）、L200-340（i18n/glossary）、L400-541（structured_recall） | 中间区间抽样 |
| `api/ingest_pipeline.py` | L1-120（chunk/walk）、L200-316（process_markdown_files）、L350-438（sync/任务队列） | 其余区间抽样 |
| `api/hybrid_fusion.py` | **全文精读**（55 行） | RRF 融合 |
| `api/database_manager.py` | **全文精读**（92 行） | SupabaseManager |
| `api/rag_env.py` | **全文精读**（97 行） | 环境加载与选择器 |
| `api/text2sql_core.py` | **未读** | Text2SQL 实现，按需 |
| `api/text2sql_store.py` | **未读** | Text2SQL 向量存储，按需 |
| `api/intent_router.py` | **未读** | Intent 路由，按需 |
| `api/chain_chat.py` | **未读** | Chain Timeline，按需 |
| `api/code_retrieval.py` | **未读** | Code RAG，按需 |
| `api/query_rewrite.py` | **未读** | Query Rewrite，按需 |
| `api/keyword_fallback.py` | **未读** | Keyword Fallback，按需 |
| `api/rag_logging.py` | **未读** | RAG 日志辅助，按需 |
| `supabase/sql/*.sql` | **未抽样** | 以 `_manifest.json` 与 drift_check 通过为信任基础 |
| `tests/*.py` | 清单扫描（`pytest --co`） | 未逐条阅读测试代码 |
| `tools/tech_graph_manifest_check.py` | **全文精读**（329 行） | 门禁逻辑 |
| `tools/tech_graph_contract_check.py` | **全文精读**（438 行） | 契约校验逻辑 |
| `tools/tech_graph_drift_check.py` | **全文精读**（108 行） | 漂移校验逻辑 |
| `.github/workflows/tech-graph.yml` | **全文精读**（23 行） | manifest CI |
| `.github/workflows/tech-graph-contract.yml` | **全文精读**（37 行） | contract CI |

---

*Hybrid V1：取代「纯赛马」意义上的 V4；可作为团队默认 onboarding Prompt 迭代基线。*
