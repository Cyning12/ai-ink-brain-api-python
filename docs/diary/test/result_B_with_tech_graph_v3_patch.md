# Prompt B V3 执行结果（Patch 版，以 `docs/_tech_graph/` 为索引，代码/SQL 核验）

> **说明**：本文件为 Prompt B V3 的重新执行结果，基于 subagent 对代码/SQL/CI 的逐项核验，覆盖 `result_B_with_tech_graph_v3.md` 并补充更精确的证据链。

---

## P1 易交接

### 1. 冷启动接手清单

1. 克隆仓库 `ai-ink-brain-api-python`，Python **3.11+**，执行 `pip install -r requirements.txt`。
2. 复制 `.env.example` 为 `.env.local`（或 `.env`），按 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §C 填写：
   - Supabase: `NEXT_PUBLIC_SUPABASE_URL` / `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` / `SUPABASE_SERVICE_KEY`
   - SiliconFlow: `SILICONFLOW_API_KEY` + `SILICONFLOW_BASE_URL` + `SILICONFLOW_CHAT_MODEL` + `SILICONFLOW_EMBEDDING_MODEL`
   - Auth: `NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET`（两者等价，见 `api/rag_env.py::admin_secret`）
   - Text2SQL（可选）: `TEXT2SQL_DATABASE_URL`
3. 打开 `docs/_tech_graph/00_main.md`（人类版）与 `00_main.ai.md`（AI 协议版，含 manifest 注入的 AUTO 端点块），建立「路由 → handler → 模块」心智模型。
4. 阅读 `docs/_tech_graph/99_spec.md`：了解 CI 门禁脚本（manifest check / drift check / contract check）及 env 拓扑意图。
5. 阅读 `docs/_tech_graph/01_struct.md`，再在 `supabase/sql/init.sql`、`hybrid_search.sql`、`code_chunks.sql` 中抽查表结构与 RPC。
6. 按主链路顺序浏览代码：
   - RAG: `10_flow_rag.md` → `api/index.py::chat` / `api/unified_chat.py`
   - FTS: `12_flow_fts.md` → `api/rag_recall_tools.py`
   - RPC: `13_flow_supabase_rpc.md` → `supabase/sql/*.sql`
   - Text2SQL: `11_flow_text2sql.md` → `api/text2sql_core.py` + `api/text2sql_api.py`
   - Code RAG: `api/code_retrieval.py`
   - Ingest: `api/ingest_pipeline.py` + `api/code_ingest.py`
7. SSE 契约：读 `docs/_tech_graph/_contract_manifest.json`（键名/枚举门禁），辅以 `14_runtime_observability.ai.md`；Python 产出点在 `api/unified_chat.py`（`_sse` / `_event`）。
8. 本地启动：`python -m uvicorn main:app --host 127.0.0.1 --port 8000`（根目录 `main.py` 转发 `api.index:app`）。
9. 冒烟：`curl -s http://127.0.0.1:8000/api/py/health`；带鉴权接口需在 Header 提供 `api/index.py::_require_auth` 认可的 token。
10. 变更端点/RPC/env/表名后：**必须**更新 `docs/_tech_graph/_manifest.json`，并运行 `python tools/tech_graph_manifest_check.py`；可选运行 `python tools/tech_graph_drift_check.py`。
11. 若涉及 Unified SSE 跨端契约：运行 `python tools/tech_graph_contract_check.py`（CI 中需检出前端仓库 `Cyning12/ai-ink-brain`，见 `.github/workflows/tech-graph-contract.yml`）。
12. 数据库侧：新项目执行 `supabase/sql/` 下脚本顺序以仓库注释为准；向量维度须与 `.env` 中 `EMBEDDING_DIM` / `SILICONFLOW_EMBEDDING_DIMENSIONS` / 表 `vector(N)` 一致（默认 1024）。
13. 排障：先看 `DEBUG_RAG`/`RAG_DEBUG`/`TEXT2SQL_DEBUG`/`DEBUG_INGEST`/`DEBUG_CODE_INGEST` 开关，再结合 `rag_conversation_logs` 与图谱 `14_runtime_observability` 的错误分支。

### 2. 锚点索引表

| 类型 | 名称 | 证据位置（路径 · 符号或职责） |
|------|------|------------------------------|
| HTTP | `GET /api/py/health` | `api/index.py` · `health`（L434 `@app.get` + L435 函数） |
| HTTP | `GET /api/py/chat/history` | `api/index.py` · `chat_history`（L439 `@app.get`） |
| HTTP | `POST /api/py/chat` | `api/index.py` · `chat`（L591 `@app.post`；遗留 RAG 流式） |
| HTTP | `POST /api/py/unified/chat` | `api/index.py` · `unified_chat_route`（L561）→ `api/unified_chat.py::handle_unified_chat` |
| HTTP | `POST /api/py/unified/chat/stream` | `api/index.py` · `unified_chat_stream_route`（L576）→ `handle_unified_chat_stream` |
| HTTP | `POST /api/py/text2sql/chat` | `api/index.py` · `text2sql_chat`（L531 `@app.post`） |
| HTTP | `POST /api/py/chain/chat` | `api/index.py` · `chain_chat_route`（L546）→ `api/chain_chat.py::handle_chain_chat` |
| HTTP | `POST /api/py/code/query` | `api/index.py` · `code_query`（L501）→ `api/code_retrieval.py::handle_code_query` |
| HTTP | `POST /api/py/code/search` | `api/index.py` · `code_search`（L516）→ `api/code_retrieval.py::handle_code_search` |
| HTTP | `POST /api/py/admin/sync` | `api/index.py` · `py_admin_sync_post`（L983）→ `api/ingest_pipeline.py::run_sync_job_sync` |
| HTTP | `GET /api/py/admin/sync` | `api/index.py` · `py_admin_sync_get`（L1009 `@app.get`） |
| HTTP | `POST /api/py/admin/ingest` | `api/index.py` · `py_admin_ingest`（L1026）→ `api/ingest_pipeline.py::process_markdown_files` / `api/code_ingest.py::process_code_files` |
| 鉴权 | `_require_auth` | `api/index.py` · L206 起；与 `api/rag_env.py::admin_secret`（L93）配合 |
| 鉴权 | `_require_unified_auth` | `api/unified_chat.py` · L35 起 |
| 鉴权 | `_require_code_api_auth` | `api/code_retrieval.py` · L38 起 |
| RPC | `match_documents` | `api/index.py` / `api/unified_chat.py` / `api/rag_recall_tools.py` · `.rpc("match_documents", ...)` |
| RPC | `keyword_documents` | `api/index.py::fetch_keyword_hits` / `api/rag_recall_tools.py::keyword_query_text_with_i18n_meta` |
| RPC | `match_code_chunks` | `api/code_retrieval.py` · `.rpc("match_code_chunks", ...)`（L338–395 区间） |
| RPC | `keyword_code_chunks` | `api/code_retrieval.py` · `.rpc("keyword_code_chunks", ...)` |
| RPC | `refresh_documents_fts_tokens_for_paths` | `api/ingest_pipeline.py` · `.rpc(...)`（L302 起） |
| RPC | `refresh_code_chunks_fts_tokens_for_paths` | `api/code_ingest.py` · `.rpc(...)`（L241 起） |
| RPC | `documents_fts_tokens_update` | `supabase/sql/hybrid_search.sql` · L134 `CREATE OR REPLACE FUNCTION` |
| RPC | `code_chunks_fts_tokens_update` | `supabase/sql/code_chunks.sql` · L34 `CREATE OR REPLACE FUNCTION` |
| RPC | `rag_fts_alias_text` | `supabase/sql/hybrid_search.sql` · L30 `CREATE OR REPLACE FUNCTION` |
| 表 | `documents` | `supabase/sql/init.sql` · L17 `CREATE TABLE IF NOT EXISTS public.documents` |
| 表 | `code_chunks` | `supabase/sql/code_chunks.sql` · L12 `CREATE TABLE IF NOT EXISTS public.code_chunks` |
| 表 | `rag_conversation_logs` | `supabase/sql/create_rag_conversation_logs.sql` · L6 `CREATE TABLE IF NOT EXISTS public.rag_conversation_logs` |
| Manifest | 端点/RPC/表/env/anchors 真值 | `docs/_tech_graph/_manifest.json`（196 行） |
| SSE 契约 | `chain`/`done` 事件与最小 payload 键 | `docs/_tech_graph/_contract_manifest.json`（62 行） |
| 渲染工具 | AUTO 端点块注入 | `tools/tech_graph_render_ai.py` → `00_main.ai.md` 的 `<!-- AUTO:ENDPOINTS_AND_ANCHORS BEGIN/END -->` |

### 3. 新人 FAQ

1. **入口路由都在哪定义？** 全部在 `api/index.py` 的 `@app.get` / `@app.post`。`_manifest.json` 的 `endpoints` 数组与之逐项对齐。**证据**：subagent grep 确认 12 个 handler 全部存在，方法/路径无误。
2. **Unified 与普通 `/chat` 有什么区别？** Unified 走 `api/unified_chat.py`，集成 intent 路由 + RAG + Text2SQL + SSE 结构化事件；遗留 `/chat` 在 `api/index.py::chat`，侧重 Hybrid RAG 流式。**证据**：两套路由与模块分离，各自独立 handler。
3. **图谱里的 RPC 名称与 SQL 完全一致吗？** `_manifest.json` 为权威真值；`13_flow_supabase_rpc.md` 人类图中有缩写（如 `refresh_documents_fts_tokens` 省略 `_for_paths`），以 SQL + Python 调用为准。**证据**：`hybrid_search.sql`/`code_chunks.sql` 与 `ingest_pipeline.py`/`code_ingest.py` 调用全名一致。
4. **`TEXT2SQL_DATABASE_URL` 何时必填？** Text2SQL 执行 SQL 分支需要；未配置会在执行阶段失败（`api/text2sql_core.py::execute_select_sql` L88 起），而非 import 阶段。**证据**：`api/text2sql_core.py` L88–90 读取 env。
5. **Admin ingest `type=code` 去哪扫代码？** `py_admin_ingest` 接收 `repo_path` query param；落到 `api/code_ingest.py::process_code_files`。**证据**：`api/index.py` L1027+ 分支逻辑。
6. **CI 如何保证文档不漂？** PR/push `main` 运行 `.github/workflows/tech-graph.yml` 中的 `python tools/tech_graph_manifest_check.py`；契约工作流见 `tech-graph-contract.yml`。**证据**：工作流 YAML 文件已读。
7. **为什么有两份 00_main（.md 与 .ai.md）？** `99_mermaid_protocol.md` 双轨说明：人类版与 AI 协议版语义等价；`.ai.md` 含 AUTO 块与 manifest 同步端点列表。**证据**：`99_mermaid_protocol.md` §双轨制。
8. **RAG 向量失败会怎样？** 代码路径会记录/降级 keyword（`fetch_keyword_hits`、`unified_chat` 内 tool 调用）；具体以 `api/index.py` L669 / `api/unified_chat.py` L527 分支为准。**证据**：subagent 确认 embedding fail → keyword-only 降级路径存在。
9. **env 里 `NEXT_PUBLIC_ADMIN_SECRET` 和 `CHAT_API_SECRET` 都要填吗？** 两者等价，`api/rag_env.py::admin_secret` 会按优先级读取（`CHAT_API_SECRET` > `NEXT_PUBLIC_ADMIN_SECRET`）。**证据**：`api/rag_env.py` L93–95。
10. **向量维度不一致会怎样？** `EMBEDDING_DIM` / `SILICONFLOW_EMBEDDING_DIMENSIONS` / 表 `vector(N)` 必须一致（默认 1024）。`api/rag_env.py::expected_embedding_dim` 提供统一值。**证据**：`api/rag_env.py` L36；`supabase/sql/init.sql` L17 `vector(1024)`。

### 4. 改动配方卡

#### 卡 A：新增 HTTP 端点

- **必读文件**：`api/index.py`（路由与鉴权）；`docs/_tech_graph/_manifest.json`（新增 `endpoints` 项）；若影响架构总览则更新 `docs/_tech_graph/00_main*.md`。
- **慎碰点**：与现有路径前缀 `/api/py/` 冲突；遗漏 manifest 会导致 `tech_graph_manifest_check.py` **失败**。
- **推荐验证**：本地起服务后 `curl` 新方法；运行 `python tools/tech_graph_manifest_check.py`。

#### 卡 B：调整检索策略（向量 / keyword / 融合 / threshold）

- **必读文件**：`api/index.py`（`_parse_match_threshold`、`fetch_keyword_hits`、`merge_hits_anchors_first`）；`api/rag_recall_tools.py`（`rpc_execute_with_retry`、`keyword_query_text_with_i18n_meta`、`structured_recall_by_date`）；`api/hybrid_fusion.py`（`fuse_hits_rrf`）；`api/unified_chat.py`（Unified 工具链）；环境变量 `RAG_MATCH_THRESHOLD`、`RAG_MATCH_COUNT`、`RAG_RPC_RETRIES`。
- **慎碰点**：`match_documents` 阈值为余弦相似度区间 (0,1]（`index.py` 注释）；改变 top_k 需与前端/契约对齐。
- **推荐验证**：单测或本地带 `DEBUG_RAG=1` 打日志；对比 `rag_conversation_logs` 中检索元数据。

#### 卡 C：调整 ingest（markdown / code）

- **必读文件**：`api/ingest_pipeline.py`（`process_markdown_files`、`CONTENT_ROOT`、`chunk_text_by_chars`）；`api/code_ingest.py`（`process_code_files`、代码解析与 `refresh_code_chunks_fts_tokens_for_paths`）；`supabase/sql/hybrid_search.sql` / `code_chunks.sql`（FTS 与刷新 RPC）。
- **慎碰点**：批量插入后需刷新 FTS 路径列表；向量维度与 `EMBEDDING_DIM` / 表 `vector(N)` 不一致会 400/500。
- **推荐验证**：`POST /api/py/admin/ingest?type=markdown` 或 `type=code&repo_path=`；检查 Supabase `documents`/`code_chunks` 行数与日志。

#### 卡 D：调整 SSE 事件契约

- **必读文件**：`docs/_tech_graph/_contract_manifest.json`（键名/枚举真值）；`api/unified_chat.py`（`_sse` / `_event` / `_build_rag_sources_event`）；`.github/workflows/tech-graph-contract.yml`。
- **慎碰点**：删改 `chain.data_keys` 或 `done.data_keys` 中的必需键会导致前端消费失败；CI 跨仓校验会失败。
- **推荐验证**：运行 `python tools/tech_graph_contract_check.py`；前端仓库需同步更新。

---

## P2 可靠性

### 5. 摘要（≤200 字）

FastAPI 后端：`api/index.py` 汇总 health、遗留 `/chat`、Unified（JSON/SSE）、Text2SQL、Chain、代码检索与 Admin ingest/sync；检索依赖 Supabase RPC 与 `documents`/`code_chunks`/`rag_conversation_logs`。以 `docs/_tech_graph/`（`00_main`、`01_struct`、flow10–15、`_manifest.json`、`_contract_manifest.json`）为索引；落地行为以源码与 `supabase/sql` 为准并对照图谱缩写。

### 6. 图谱索引摘要 + 模块地图与主链路

**图谱文件清单及目的（索引级，非替代核验）**

| 图谱文件 | 用途 |
|----------|------|
| `00_main.md` / `00_main.ai.md` | 全仓 HTTP 分支总览；`.ai.md` 含 `_manifest.json` 注入的端点/handlers 列表 |
| `01_struct.md` | 表与 `metadata` 字段意图（class 图） |
| `02_version.md` | Git 迭代时间线（Mermaid timeline） |
| `99_spec.md` | 事实来源约束、env 拓扑示意、`tools/` 漂移/manifest 门禁说明 |
| `99_mermaid_protocol.md` | 双轨与边标记约定（Python/FastAPI 适配版） |
| `10_flow_rag.md` / `.ai.md` | RAG：鉴权→改写→keyword/向量→融合→LLM→日志 |
| `11_flow_text2sql.md` / `.ai.md` | Text2SQL：意图→检索→生成→校验→执行→总结 |
| `12_flow_fts.md` / `.ai.md` | FTS：触发器、`keyword_documents`、可选 i18n 扩展 |
| `13_flow_supabase_rpc.md` / `.ai.md` | Client→表与 RPC（注意图中 RPC **缩写**） |
| `14_runtime_observability.md` / `.ai.md` | SSE 事件类型与排障锚点 |
| `15_e2e_boundary.md` / `.ai.md` | 前端/BFF/Python/内容仓边界 |
| `_manifest.json` | 机器可读端点、表、RPC、env、anchors 列表 |
| `_contract_manifest.json` | Unified SSE：`chain`/`done` 及 `type` 枚举与最小 payload 键 |

**代码核验后的模块地图与主链路**

1. **Legacy RAG**：`POST /api/py/chat` → `api/index.py::chat`（L591）；Hybrid：`match_documents` + `keyword_documents` + 日期锚点合并等；流式 `StreamingResponse`，`x-sources` 与文末 marker。
2. **Unified Chat**：`POST /api/py/unified/chat` 与 `/stream` → `api/unified_chat.py::handle_unified_chat` / `handle_unified_chat_stream`；流式 SSE 事件类型以 `_contract_manifest.json` 为准；RAG/Text2SQL 子路径仍调上述 RPC 与 Text2SQL 执行器。
3. **Text2SQL**：`POST /api/py/text2sql/chat` → `api/text2sql_api.py` / `api/text2sql_core.py`；`TEXT2SQL_*` env；`11_flow` 图中引用 `docs/text2sql/v1/sql/supabase_init.sql` **在本仓库存在**（`supabase/sql/` 同级路径外另有 `docs/text2sql/v1/sql/supabase_init.sql`）。
4. **Ingest / Sync**：`admin/ingest`、`admin/sync` → `api/ingest_pipeline.py` / `api/code_ingest.py`；刷新 `refresh_*_fts_tokens_for_paths`。
5. **Code RAG**：`code/query`、`code/search` → `api/code_retrieval.py`；RPC `match_code_chunks`、`keyword_code_chunks`。
6. **Chain Chat**：`POST /api/py/chain/chat` → `api/chain_chat.py::handle_chain_chat`；固定 pipeline：intent → rewrite → retrieval → LLM，非流式 JSON。

### 7. 事实断言清单

| # | 断言 | 证据 | 核验方式 | 置信度 |
|---|------|------|----------|--------|
| 1 | `GET /api/py/health` 存在 | `api/index.py` L434–435 | subagent grep + 行号 | 高 |
| 2 | `POST /api/py/unified/chat/stream` 存在 | `api/index.py` L576+ | subagent grep + 行号 | 高 |
| 3 | `_manifest.json` 列出 12 条 endpoint 记录 | `docs/_tech_graph/_manifest.json` endpoints 数组 | JSON 字段计数 | 高 |
| 4 | 12 个 endpoint handler 全部存在于 `api/index.py` | subagent 逐一手动确认 | 代码遍历 | 高 |
| 5 | 6 个 anchor 全部存在于对应文件 | subagent 逐一手动确认 | 代码遍历 | 高 |
| 6 | 3 个表全部存在于 SQL 文件 | `init.sql` / `code_chunks.sql` / `create_rag_conversation_logs.sql` | subagent 读 SQL | 高 |
| 7 | 9 个 RPC 全部存在于 SQL 文件 | `hybrid_search.sql` / `code_chunks.sql` | subagent 读 SQL CREATE | 高 |
| 8 | 30 个 env var 全部在 `api/*.py` 中有引用 | subagent 逐变量 grep | 代码遍历 | 高 |
| 9 | Python 调用 `refresh_documents_fts_tokens_for_paths` | `api/ingest_pipeline.py` L302+ | subagent grep `.rpc(` | 高 |
| 10 | Python 调用 `refresh_code_chunks_fts_tokens_for_paths` | `api/code_ingest.py` L241+ | subagent grep `.rpc(` | 高 |
| 11 | `tech-graph.yml` 运行 `manifest_check.py` | `.github/workflows/tech-graph.yml` L22–23 | 读 YAML | 高 |
| 12 | `tech-graph-contract.yml` 检出前端并运行 `contract_check.py` | `.github/workflows/tech-graph-contract.yml` | 读 YAML | 高 |
| 13 | `documents` 表含 `embedding vector(1024)` | `supabase/sql/init.sql` L17 | 读 SQL | 高 |
| 14 | `code_chunks` 表含 `embedding vector(1024)` | `supabase/sql/code_chunks.sql` L12 | 读 SQL | 高 |
| 15 | `rag_conversation_logs` 含 `rewritten_query` 字段 | `supabase/sql/create_rag_conversation_logs.sql` L6+ | 读 SQL | 高 |
| 16 | `match_documents` 在 `init.sql` 和 `patch_match_documents_threshold.sql` 中均有定义 | 两个 SQL 文件 | subagent 读 SQL | 高（patch 为升级路径） |
| 17 | `api/rag_env.py::expected_embedding_dim` 默认 1024 | `api/rag_env.py` L36 | subagent 读代码 | 高 |
| 18 | `api/rag_env.py::admin_secret` 读取 `CHAT_API_SECRET` > `NEXT_PUBLIC_ADMIN_SECRET` | `api/rag_env.py` L93–95 | subagent 读代码 | 高 |
| 19 | `13_flow_supabase_rpc.md` 图中节点名为 `refresh_documents_fts_tokens`（无 `_for_paths`） | `docs/_tech_graph/13_flow_supabase_rpc.md` 原文 | 与 SQL/Python 对照 | 中（文档缩写，已标注） |
| 20 | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 写「本仓当前未发现 workflows」 | `PROJECT_CONFIG` L92–93 | 列目录 `.github/workflows/` | 低（与仓库现状不符，CI 已存在） |

### 8. 不确定性与验证步骤

| 不确定性 | 建议验证步骤 |
|----------|--------------|
| `11_flow_text2sql.md` 指向 `docs/text2sql/v1/sql/supabase_init.sql` 是否与本仓 Text2SQL 实际 DDL 一致 | 对比 `docs/text2sql/v1/sql/supabase_init.sql` 与 `api/text2sql_core.py` 中引用的表结构；确认 agent_info 等表是否已部署 |
| `15_e2e_boundary.md` 写 SSE 契约锚点为 `14_runtime_observability.ai.md` | 以 `_contract_manifest.json` + `tech_graph_contract_check.py` 为门禁真值；14 图为辅助 |
| Hybrid RRF 与各路由优先级细节 | 对照 `api/hybrid_fusion.py`、`api/intent_router.py` 单测或日志 |
| Admin sync 任务队列在 serverless 下的持久性 | 读 `ingest_pipeline.py` 中 job 实现；压测重启 |
| `match_documents` patch 文件 `patch_match_documents_threshold.sql` 是否已在生产执行 | 检查生产 Supabase 迁移历史 |
| `tools/tech_graph_render_ai.py` 的渲染脚本行为细节 | 若修改 AUTO 块流程可再读；当前仅知它注入端点/anchors 到 `00_main.ai.md` |

### 9. 漂移防线

本仓库**实际读到**：

| 路径 | 用途 |
|------|------|
| `tools/tech_graph_manifest_check.py`（329 行） | manifest 与 `api/index.py`、SQL、`api/*.py` env 等交叉校验 |
| `tools/tech_graph_drift_check.py`（108 行） | 端点/RPC/env/表名是否在 `docs/_tech_graph/*.md` 覆盖 |
| `tools/tech_graph_contract_check.py`（438 行） | `_contract_manifest.json` 与 `api/unified_chat.py` SSE 结构跨仓校验 |
| `tools/tech_graph_render_ai.py`（125 行） | 读取 `_manifest.json` 并注入 AUTO 端点/anchors 块到 `00_main.ai.md` |
| `.github/workflows/tech-graph.yml`（23 行） | PR/push 运行 manifest check |
| `.github/workflows/tech-graph-contract.yml`（37 行） | 跨仓契约 check（需检出 `Cyning12/ai-ink-brain` production 分支） |

未单独通读：`tech_graph_render_ai.py` 的完整渲染逻辑细节——若修改 AUTO 块流程可再读。

---

## P3/P4

### 10. 消耗明细

**Token 估算（按 Prompt B V3 公式）**

| 类别 | 行数 | tokens/行 | 估算 tokens |
|------|------|-----------|-------------|
| 图谱文件（`.md` + `.ai.md` + `_manifest.json` + `_contract_manifest.json`） | ~1,450 | 10 | ~14,500 |
| 代码/SQL（核心文件抽样核验） | ~3,500 | 12 | ~42,000 |
| 命令/grep 输出（subagent 返回） | ~800 | 8 | ~6,400 |
| 本结果正文 | ~450 行 ≈ 18,000 字符 | 4 字符/token | ~4,500 |
| **合计（阅读+合成）** | — | — | **~67,400** |

**时间估算**

| 阶段 | 时长 |
|------|------|
| `t_graph`（读图谱双轨 + manifest + contract） | ~25 min |
| `t_read`（subagent 核验 endpoint/RPC/表/env/CI/tools） | ~20 min |
| `t_synthesis`（综合输出） | ~15 min |
| `t_total` | **~60 min** |

### 11. 覆盖率

**图谱文件阅读覆盖率**

| 文件 | 是否完整阅读 | 目的 |
|------|-------------|------|
| `00_main.md` | ✅ 是 | 主干路由与人类版 Mermaid |
| `00_main.ai.md` | ✅ 是 | 拓扑协议版 + AUTO 端点块 |
| `01_struct.md` | ✅ 是 | 表与 metadata 意图 |
| `02_version.md` | ✅ 是 | Git 迭代时间线 |
| `99_spec.md` | ✅ 是 | CI/env/backlog |
| `99_mermaid_protocol.md` | ✅ 是 | 双轨与边语义 |
| `10_flow_rag.md` | ✅ 是 | RAG 子流程（人类版） |
| `10_flow_rag.ai.md` | ✅ 是 | RAG 子流程（AI 协议版） |
| `11_flow_text2sql.md` | ✅ 是 | Text2SQL 子流程（人类版） |
| `11_flow_text2sql.ai.md` | ✅ 是 | Text2SQL 子流程（AI 协议版） |
| `12_flow_fts.md` | ✅ 是 | FTS 与触发器链路（人类版） |
| `12_flow_fts.ai.md` | ✅ 是 | FTS 与触发器链路（AI 协议版） |
| `13_flow_supabase_rpc.md` | ✅ 是 | RPC 视图（人类版，注意缩写） |
| `13_flow_supabase_rpc.ai.md` | ✅ 是 | RPC 视图（AI 协议版） |
| `14_runtime_observability.md` | ✅ 是 | SSE 简图 |
| `14_runtime_observability.ai.md` | ✅ 是 | SSE 详细事件与错误分支 |
| `15_e2e_boundary.md` | ✅ 是 | 端到端边界（人类版） |
| `15_e2e_boundary.ai.md` | ✅ 是 | 端到端边界（AI 协议版） |
| `_manifest.json` | ✅ 是 | 机器真值 |
| `_contract_manifest.json` | ✅ 是 | SSE 契约门禁 |

**代码/SQL 核验覆盖率（抽样，非全仓库逐行）**

- `api/index.py`：路由 grep + L206 `_require_auth`、L434–591 chat/Unified、L983–1053 admin、Unified 段落 → ✅
- `api/unified_chat.py`：grep `.rpc(` + `handle_unified_chat` / `handle_unified_chat_stream` → ✅
- `api/ingest_pipeline.py`：`process_markdown_files`、`run_sync_job_sync`、`.rpc(` 调用 → ✅
- `api/code_ingest.py`：`process_code_files`、`.rpc(` 调用 → ✅
- `api/code_retrieval.py`：`handle_code_query`、`handle_code_search`、`.rpc(` 调用 → ✅
- `api/rag_env.py`：`pick_supabase_url`、`pick_supabase_service_key`、`admin_secret`、`expected_embedding_dim` → ✅
- `api/rag_recall_tools.py`：`rpc_execute_with_retry`、`keyword_query_text_with_i18n_meta`、`structured_recall_by_date` → ✅
- `api/hybrid_fusion.py`：`fuse_hits_rrf` → ✅
- `api/intent_router.py`：`decide_intent` → ✅
- `api/text2sql_core.py`：`execute_select_sql`、`validate_sql_readonly` → ✅
- `api/chain_chat.py`：`handle_chain_chat` → ✅
- `supabase/sql/init.sql`：表 + `match_documents` → ✅
- `supabase/sql/hybrid_search.sql`：`keyword_documents`、`rag_fts_alias_text`、`documents_fts_tokens_update`、`refresh_documents_fts_tokens_for_paths` → ✅
- `supabase/sql/code_chunks.sql`：表 + `match_code_chunks`、`keyword_code_chunks`、`code_chunks_fts_tokens_update`、`refresh_code_chunks_fts_tokens_for_paths` → ✅
- `supabase/sql/create_rag_conversation_logs.sql`：`rag_conversation_logs` → ✅
- `supabase/sql/patch_match_documents_threshold.sql`：`match_documents` patch → ✅
- `.github/workflows/*.yml`：首部与用途 → ✅
- `tools/tech_graph_*.py`：首部与用途 → ✅
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`：§C env → ✅

---

```text
📊 Execution Report (Patch)
├── Duration: ~60 min 等效人工工作量
├── Thinking Steps:
│ 1. 以 `docs/_tech_graph/` 为索引建立章节骨架，再用 subagent 逐项核验 endpoint/RPC/manifest/CI，避免把图谱缩写当作事实。
│ 2. 将 `13_flow` 与 `_manifest`/SQL 的差异记入断言置信度与不确定性，不把过时 PROJECT_CONFIG 句当作真值。
│ 3. 输出严格遵循 Prompt B V3 同级标题顺序，便于与 `result_A_no_tech_graph_v3.md` / `result_B_with_tech_graph_v3.md` 横向对比。
│ 4. Patch 版补充：更精确的 subagent 核验结果（12 endpoint + 6 anchor + 3 table + 9 RPC + 30 env + CI/tools）、新增 FAQ（env 等价性、向量维度）、新增改动配方卡 D（SSE 契约）。
├── Files Created:
│ - ai-ink-brain-api-python/docs/diary/test/result_B_with_tech_graph_v3_patch.md
├── Risk Level: Low
└── Notes:
    - `11_flow_text2sql` 外链 `docs/text2sql/v1/sql/supabase_init.sql` 已确认存在于本仓库。
    - `PROJECT_CONFIG` 中「未发现 workflows」表述与仓库现状不符，已记入低置信断言。
• Cost Awareness:
• 图谱优先策略减少迷路成本；核验脚本路径已写入漂移防线小节。
• Loop Guard: 不适用（单次落盘）。
• Scope Confirmation: 仅新增约定结果文件，未改业务代码。
```
