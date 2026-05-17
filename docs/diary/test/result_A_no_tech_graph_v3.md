# ai-ink-brain-api-python · Result A（V3 · 禁用图谱）

本文档在未读取 `docs/_tech_graph/**` 前提下，仅凭代码、`supabase/sql/`、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`、`.env.example`、`requirements.txt`、`tests/` 梳理可交接信息。

---

#### P1 易交接（权重最高）

1. **冷启动接手清单**（10～15 步；每步一句可执行动作）

1. 克隆仓库后进入根目录，`pip install -r requirements.txt` 安装运行时依赖。
2. 对照 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 中「环境变量」表与 `.env.example`，在项目根目录准备 `.env` 或 `.env.local`（`api/rag_env.py` 以 `override=False` 加载二者）。
3. 在 Supabase SQL Editor 按需执行：`supabase/sql/init.sql`、`supabase/sql/hybrid_search.sql`；已有旧 `match_documents` 时可参考 `patch_match_documents_threshold.sql`。
4. 若使用 Code RAG，执行 `supabase/sql/code_chunks.sql` 创建 `public.code_chunks` 与相关 RPC。
5. 执行 `supabase/sql/create_rag_conversation_logs.sql`，确保存在 `public.rag_conversation_logs` 供会话日志与 history。
6. 本地启动：`python -m uvicorn main:app --host 127.0.0.1 --port 8000`（`main.py` 仅从 `api.index` 导出 `app`）。
7. `curl http://127.0.0.1:8000/api/py/health` 校验服务可达。
8. 带鉴权调用 `POST /api/py/chat`：Header 使用 `Authorization: Bearer <NEXT_PUBLIC_ADMIN_SECRET 或 CHAT_API_SECRET>` 或与 `API_KEY` 等长比对（见 `_require_auth`），Body 含 `messages`、`session_id`。
9. 打开 `tests/` 中与当前需求相关的文件，对照 `pytest` 用例理解契约；运行 `pytest`（需在环境中配置密钥或按需 mock）。
10. Markdown 入库：配置 `CONTENT_ROOT` 指向含 `.md`/`.mdx` 的根目录（见 `api/ingest_pipeline.py` 注释），调用 `POST /api/py/admin/ingest?type=markdown`。
11. 代码入库：`POST /api/py/admin/ingest?type=code` 并可传 `repo_path` 指向项目根。
12. Text2SQL 独立链路：设置 `TEXT2SQL_DATABASE_URL`（`text2sql_core.execute_select_sql`），再测 `POST /api/py/text2sql/chat`。

---

2. **锚点索引表**（路径/RPC/表/env → `文件路径` + `函数名或行区间` + 一句职责）

| 锚点 | 位置与职责 |
|------|------------|
| `GET /api/py/health` | `api/index.py` L434-L436 · `health()` · 存活探针 |
| `POST /api/py/chat` | `api/index.py` L591-L980 · `chat()` · 流式 RAG：rewrite → embedding → `match_documents` + `keyword_documents` → `fuse_hits_rrf` → 流式生成 + sources |
| `GET /api/py/chat/history` | `api/index.py` L439-L498 · `chat_history()` · 读 `rag_conversation_logs` 还原会话 |
| `POST /api/py/admin/ingest` | `api/index.py` L1026-L1052 · `py_admin_ingest()` · `markdown`→`process_markdown_files`，`code`→`process_code_files` |
| `POST /api/py/admin/sync` / `GET /api/py/admin/sync` | `api/index.py` L983-L1024 · 异步 ingest 任务，`ingest_pipeline` 内存 job |
| `POST /api/py/unified/chat` · `POST /api/py/unified/chat/stream` | `api/unified_chat.py` · intent + RAG/Text2SQL/无数据分支与 SSE |
| `POST /api/py/text2sql/chat` | `api/text2sql_api.py` · `handle_text2sql_chat` |
| `POST /api/py/chain/chat` | `api/chain_chat.py` · `handle_chain_chat` · 时间线事件 + Text2SQL |
| `POST /api/py/code/query` · `POST /api/py/code/search` | `api/code_retrieval.py` · code 向量/关键词混合检索 |
| RPC `match_documents` | `api/index.py` L703-L709；DDL `supabase/sql/init.sql`、`patch_match_documents_threshold.sql` |
| RPC `keyword_documents` | `api/index.py` `fetch_keyword_hits` L78-86；`hybrid_search.sql` |
| RPC `keyword_documents`（路由证据） | `api/intent_router.py` L123-L137 · `_fts_evidence` |
| RPC `refresh_documents_fts_tokens_for_paths` | `api/ingest_pipeline.py` L302 附近、`L369` 附近 · ingest 后刷新 FTS |
| RPC `match_code_chunks` · `keyword_code_chunks` | `api/code_retrieval.py` L339-L395；DDL `supabase/sql/code_chunks.sql` |
| RPC `refresh_code_chunks_fts_tokens_for_paths` | `api/code_ingest.py` L241-L244 |
| 表 `public.documents` | `supabase/sql/init.sql` · 主 RAG 文本块 |
| 表 `public.code_chunks` | `supabase/sql/code_chunks.sql` |
| 表 `public.rag_conversation_logs` | `supabase/sql/create_rag_conversation_logs.sql`；写 `database_manager.py` `save_debug_log` |
| `TEXT2SQL_DATABASE_URL` | `api/text2sql_core.py` L87-L90 · `execute_select_sql` 直连 Postgres |
| `RAG_MATCH_THRESHOLD` | `api/index.py` L100-L122、`unified_chat.py` L111-L125 · `match_documents` / `match_code_chunks` 阈值 |
| `SILICONFLOW_*` / Embedding 维度 | `api/index.py` L55-L60；`api/rag_env.py` · 与向量列维度一致 |

---

3. **新人 FAQ**（6～10 条；每条含证据锚点）

1. **生产与本地入口为何不同？** 本地用 `main.py` → `uvicorn`；PROJECT_CONFIG §A 写明 Vercel 指向 `api/index.py`，本仓库两处导出同一 `app` 实例。证据：`main.py` L9、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` L17-L18。
2. **会话历史从哪读？上限多少轮？** `chat` 用 `SupabaseManager.get_chat_history(..., limit=5)`（`api/index.py` L637-L639）；`PROJECT_CONFIG.md` §B 提到当前实现为 5 轮。
3. **Embedding 失败会怎样？** 向量路跳过，`metadata.match.hybrid.mode` 会体现 keyword_only；融合仍走 `fuse_hits_rrf`（`api/index.py` L669-L685、L761）。
4. **鉴权密钥填哪个 env？** `admin_secret()` 读 `NEXT_PUBLIC_ADMIN_SECRET` 或 `CHAT_API_SECRET`；另支持 `API_KEY` 与时间序比对（`api/index.py` L206-L231）。
5. **`x-sources` 头有时没有？** 超长会省略，依赖流尾 `---RAG_SOURCES_JSON---`（`api/index.py` L68-L69、L879-L886、914-L918）。
6. **Unified 与普通 chat 的区别？** Unified 在 `api/unified_chat.py`：`decide_intent`（`intent_router.py`）+ Text2SQL 工具函数 + SSE 事件；Legacy 流式在 `chat()` 单文件闭环。
7. **Text2SQL 是否走 Supabase RPC？** 否；只读 SQL 通过 `psycopg` 连接 `TEXT2SQL_DATABASE_URL`（`api/text2sql_core.py` L87-L104）。
8. **`prefer=tool:*` 会怎样？** `intent_router.decide_intent` 对该前缀直接返回 `final_mode` 为该字符串，属预留行为（`api/intent_router.py` L142-L149）。

---

4. **改动配方卡**（三卡固定）

**卡片 A：新增 HTTP 端点**

| 必读文件 | `api/index.py`（路由注册与同文件 `_require_auth` 模式）；若需新领域逻辑则新建 `api/<module>.py` 并在 `index` 挂路由。 |
| 慎碰点 | 不要在未鉴权的路径暴露 `pick_supabase_service_key()`；流式接口注意 `StreamingResponse` 与 `BackgroundTasks` 生命周期。 |
| 推荐验证 | 本地启动后 `curl -i -X POST http://127.0.0.1:8000/api/py/<新路径>` 带 Bearer；或 `pytest` 新增路由测试类比 `tests/test_code_api_routes.py`。 |

**卡片 B：调整检索策略（向量/keyword/融合/threshold）**

| 必读文件 | `api/index.py`（`MATCH_COUNT`、`fetch_keyword_hits`、`fuse_hits_rrf`、`KEYWORD_*`/`run_keyword_fallback`）；`api/hybrid_fusion.py`（`RRF_K`、`fuse_hits_rrf`）；`api/keyword_fallback.py`、`api/query_rewrite.py`、`api/rag_recall_tools.py`（keyword 构造与国际化）；阈值 `RAG_MATCH_THRESHOLD`。Code 路额外读 `api/code_retrieval.py`。 |
| 慎碰点 | `match_documents`/`keyword_documents` 入参名称须与 RPC 签名一致（见 `supabase/sql`）；调高 `MATCH_COUNT` 易触达 `CONTEXT_MAX_CHARS`。 |
| 推荐验证 | 设 `DEBUG_RAG=1` 观察 stdout；比对 `pytest tests/` 中与 hybrid/RAG 相关用例；对 Supabase 直接 `rpc` 手工调用核对 threshold 语义。 |

**卡片 C：调整 ingest（markdown/code）**

| 必读文件 | `api/ingest_pipeline.py`（markdown 分块、批量 embedding、`documents` 写入、`refresh_documents_fts_tokens_for_paths`）；`api/code_ingest.py` + `api/code_parser.py`（代码分块、`code_chunks` 插入、`refresh_code_chunks_fts_tokens_for_paths`）；`api/rag_env.py`（embedding 维度与密钥）。 |
| 慎碰点 | `CONTENT_ROOT` 未设时用仓库内 `REPO_ROOT/content`（`ingest_pipeline` L106-L111）；embedding 失败时 code ingest 用零向量占位（`code_ingest.py` L210-L217），可能影响向量质量；维度与 SQL `vector(N)` 不一致会 400/500（`index.py` L1048-L1051）。 |
| 推荐验证 | `POST /api/py/admin/ingest?type=markdown|code` 看返回 JSON 统计；小样本 pytest：`tests/test_code_ingest_process.py`、`tests/test_admin_ingest_route.py`。 |

---

#### P2 可靠性

5. **摘要**（≤200 字）

FastAPI 应用集中在 `api/index.py`，复用 SiliconFlow embeddings + Chat、Supabase 上 `documents`/`code_chunks` 与 FTS RPC，RRF 融合向量与关键词路；会话与调试日志写入 `rag_conversation_logs`。并提供 Unified/Chain/Text2SQL/Code 检索等扩展端点及 admin ingest/sync。环境与维度以 `rag_env`、`init.sql`、`code_chunks.sql` 对齐为准。

6. **模块地图与主链路**

**Legacy RAG（`POST /api/py/chat`）**  
入口 `chat()`：`query_rewrite.rewrite_query_with_history` → OpenAI-compatible embeddings → `match_documents` + `keyword_documents` → `fuse_hits_rrf` → 可选日期锚点合并 → 组装 system prompt → 流式 chat → tail JSON sources + BackgroundTasks 写 `rag_conversation_logs`。

**Unified**  
`unified_chat.handle_unified_chat` / `handle_unified_chat_stream`：鉴权 `_require_unified_auth` → `intent_router.decide_intent`（规则 + DDL store + `keyword_documents` 证据）→ 分支：`structured_recall_by_date`、`rag` 混合检索、Text2SQL（`execute_select_sql`）、`no_data` 直答；流式分支输出 SSE 事件。

**Text2SQL**  
`text2sql_api.handle_text2sql_chat` / unified 内部：`is_text2sql_intent`、`llm_generate_sql`、`validate_sql_readonly`、`execute_select_sql(TEXT2SQL_DATABASE_URL)`；DDL/示例出自 `text2sql_store`。

**Ingest**  
`process_markdown_files`：`documents` 表 + `refresh_documents_fts_tokens_for_paths`。`process_code_files`：`code_chunks` + `refresh_code_chunks_fts_tokens_for_paths`。`/admin/sync` 为内存异步任务队列。

**Code RAG**  
`code_retrieval`：`match_code_chunks`、`keyword_code_chunks`、`fuse_hits_rrf`；兜底可能扫 `code_chunks` 表 limited rows。

---

7. **事实断言清单**

| 断言 | 证据 | 核验方式 | 置信度 |
|------|------|----------|--------|
| HTTP 路由含 `/api/py/health`、`chat`、`chat/history`、`unified/chat`、`unified/chat/stream`、`text2sql/chat`、`chain/chat`、`code/query`、`code/search`、`admin/ingest`、`admin/sync` | `api/index.py` 装饰器 L434-L1026（grep `@app.`） | 打开文件或本地 `openapi.json`/`curl` | 高 |
| Markdown RPC：`match_documents`、`keyword_documents` | `api/index.py` L78、L703-709 | grep `sb.rpc(` | 高 |
| Code RPC：`match_code_chunks`、`keyword_code_chunks` | `api/code_retrieval.py` L339-395 | 同上 | 高 |
| 表：`documents`、`code_chunks`、`rag_conversation_logs` | `supabase/sql/*.sql`、`database_manager.py` | SQL 文件与 `.table(` 调用 | 高 |
| 融合常数 `RRF_K = 60` | `api/hybrid_fusion.py` L6-7 | 读源码 | 高 |
| Ingest FTS 刷新 RPC 名：`refresh_documents_fts_tokens_for_paths`、`refresh_code_chunks_fts_tokens_for_paths` | `ingest_pipeline.py`、`code_ingest.py` | grep `refresh_` | 高 |
| 生产部署仍以 `api/index` 导出 `app` 为业务真值（`README`/`PROJECT_CONFIG` 口述） | `main.py`、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` A 节边界说明 | `vercel.json` 仅为 schema shell，须在 Vercel 项目 Settings 中对「入口」逐项核对 | 中 |

---

8. **不确定性与验证步骤**

| 不确定项 | 验证步骤 |
|----------|----------|
| Serverless「根路由 → 哪一个 Python 模块」是否仍指向 `api.index:app` | 读 Dashboard Build/Runtime；仓库内 `vercel.json` 无业务路由字段（已见仅 `$schema`） |
| `INTENT_*` / `KEYWORD_*` / `TEXT2SQL_*` 等大量可选 tuning env 默认值对线上行为的影响 | grep 模块内 `getenv`，在 staging 打 A/B 日志 |
| `text2sql_store`（Faiss/本地路径）在具体部署下的数据目录是否存在 | 查 `TEXT2SQL_STORE` 相关代码与运行时路径（需读 `text2sql_store.py` 全文） |
| Unified 分支内是否还有未被上述概括的边角（如 prefer 特例） | 通读 `unified_chat.py` 800+ 行并跑 `pytest tests/test_unified_chat*` |

---

#### P3/P4

9. **消耗明细**（时间 + token，分项累计 + 估算公式）

**时间（估算）**

| 分项 | 值 | 依据 |
|------|-----|------|
| t_scan | ~4 min | Glob 枚举仓库、`grep` 路由与 `rpc`、`wc` 行数 |
| t_read | ~28 min | 精读 `PROJECT_CONFIG`、入口与六条主链若干文件、两份 SQL DDL、测试目录列表 |
| t_synthesis | ~18 min | 整理锚点表、断言表、配方卡与 FAQ |
| t_total | ~50 min | 三项之和 |

**Token（估算）**

- 公式：代码/SQL ~12 tokens/行；Markdown ~10 tokens/行；中文正文 ~4 字符 ≈ 1 token。

| 分项 | 行数或规模 | Tokens（约） |
|------|-------------|---------------|
| 已读的 `api/*.py` 总行数（抽样覆盖主链） | 5858 行 | ~70 300 |
| `supabase/sql/*.sql` 合计 | 515 行 | ~6 200 |
| `PROJECT_CONFIG*.md` + `.env.example` + `requirements.txt` | ~200 行 eq | ~2 000 |
| grep/命令输出折算 | ~80 行 | ~640 |
| **读入合计（约）** | — | **~79 000** |
| 本文件中文+表格输出 | ~220 行 md + ~4.5k 汉字 | ~10 000 + ~1 100 ≈ **11 000** |

---

10. **覆盖率**（读过哪些文件；若抽样请注明读到 approximately 哪些行段）

**通读或完整阅读**

- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（全文）
- `.env.example`、`requirements.txt`
- `main.py`
- `vercel.json`（已读：仅 `$schema`，无自定义 routes）
- `api/rag_env.py`（全文）
- `api/hybrid_fusion.py`（全文）
- `api/database_manager.py`（全文）
- `supabase/sql/init.sql`（前 ~90 行）、`hybrid_search.sql`（前 ~100 行）、`create_rag_conversation_logs.sql`、`patch_match_documents_threshold.sql`（全文）、`code_chunks.sql`（前 ~80 行）
- `api/text2sql_core.py`（前 ~120 行）

**抽样 / 主链区间（approximately）**

- `api/index.py`：L1-L240、L279-L365、L434-L1054（覆盖全部路由与 `chat` 主逻辑）
- `api/unified_chat.py`：L1-L200 + import 与 `_parse_match_threshold` 段
- `api/text2sql_api.py`：L1-L120
- `api/ingest_pipeline.py`：L1-L120
- `api/code_retrieval.py`：L300-L420
- `api/code_ingest.py`：L200-L250
- `api/intent_router.py`：L1-L210
- `api/chain_chat.py`：L1-L80
- `api/rag_recall_tools.py`：行首工具函数与 `structured_recall_by_date` 片段（约 L1-L120、L482-L537）

**未读但已用 glob/测试清单约束**

- `api/unified_chat.py` 后半（流式与全部分支细节）
- `api/text2sql_store.py`、`api/code_parser.py` 全文
- `tests/*.py` 各文件内部：仅列举文件名作回归入口，未逐行精读

**显式排除**

- `docs/_tech_graph/**`（按任务约束未读取）
