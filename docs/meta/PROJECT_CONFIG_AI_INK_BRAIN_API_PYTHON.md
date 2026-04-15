# AI-Ink-Brain API（Python 后端）项目配置真值表（给总 Agent / 子 Agent）

> 目标：把本仓库的**边界、入口、环境变量、目录地图、对外契约、安全注意事项**整理成“可复制粘贴的真值表”。  
> 说明：本文档只描述**本仓库实际读取/依赖**的内容；前端仓库的 `PY_API_URL`、Next BFF 等不在此展开（但会在边界里点名）。

---

## A. 仓库身份与边界

| 项 | 真值 / 说明 |
|---|---|
| 仓库名（示例） | `ai-ink-brain-api-python` |
| 远程默认分支 | `main`（以你本地 `git branch` / GitHub 默认分支为准） |
| 技术栈摘要 | FastAPI + Uvicorn；OpenAI SDK（指向 SiliconFlow 兼容接口）；`supabase-py`；Supabase（Postgres + pgvector + FTS） |
| 本仓负责的边界（Single Source of Truth） | **Embedding / Chunking / Retrieval / Hybrid Search / RAG 日志** 的权威实现应在本仓库（与 `.cursorrules` 一致） |
| 本仓不负责的边界 | **博客页面渲染、内容编辑 UX、Next.js BFF 转发** 在 `ai-ink-brain`；本仓只提供 HTTP API |
| 部署入口（概念） | 本地：`uvicorn main:app`；Vercel：README 说明生产入口为 `api/index.py`（以 Vercel Python Runtime 配置为准） |

---

## B. Cursor / Agent 规则（本仓）

| 文件 | 作用 | 是否必须存在 |
|---|---|---|
| `.cursorrules` | 全仓 AI 规则（RAG 标准、Supabase 日志、Hybrid、Streaming 等） | **建议必须**（当前存在） |
| `AGENTS.md` / `CLAUDE.md` | 额外 Agent 指引 | **本仓当前未发现**（可选） |
| `.cursor/rules/*.mdc` | 分路径规则 | **本仓当前未发现**（可选） |

`.cursorrules` 要点（执行层摘要）：
- RAG 日志必须写入 `rag_conversation_logs`
- pgvector 相似度使用 Cosine Distance（RPC `match_documents`）
- 每次请求必须处理 `session_id`，检索前读取最近 3-5 轮历史（当前实现为 5）
- LLM 输出使用 `StreamingResponse`
- Hybrid：Vector + FTS，并融合排序

---

## C. 环境变量（与代码读取点对齐）

> 读取规则：本仓库通过 `api/rag_env.py` 在 import 时加载仓库根目录 `.env.local`、`.env`（`override=False`）。  
> 下表“谁读取”以**实际 grep 命中**为准。

| 名称 | 用途 | 必填/可选 | 谁读取（文件/模块） | 典型值 / 留空行为 | 与 Supabase 维度一致性 |
|---|---|---|---|---|---|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase Project URL | **必填（二选一）** | `api/rag_env.py:pick_supabase_url()`；`api/index.py` 间接使用 | 形如 `https://xxx.supabase.co` | 与项目无关 |
| `SUPABASE_URL` | Supabase URL 别名 | **可选（二选一）** | `api/rag_env.py:pick_supabase_url()` | 留空则使用 `NEXT_PUBLIC_SUPABASE_URL` | 与项目无关 |
| `SUPABASE_SERVICE_ROLE_KEY` | service_role key（服务端写库） | **必填（二选一）** | `api/rag_env.py:pick_supabase_service_key()` | 留空会导致无法创建 Supabase client | 与项目无关 |
| `SUPABASE_SERVICE_KEY` | service key 别名 | **可选（二选一）** | `api/rag_env.py:pick_supabase_service_key()` | 留空则使用 `SUPABASE_SERVICE_ROLE_KEY` | 与项目无关 |
| `SILICONFLOW_API_KEY` | SiliconFlow API Key | **必填** | `api/index.py`（chat）；`api/rag_env.py:must_siliconflow_api_key()`（ingest） | 留空：chat 直接 500；ingest 抛 `RuntimeError` | 与项目无关 |
| `SILICONFLOW_BASE_URL` | OpenAI 兼容 Base URL | 可选 | `api/index.py`（`SILICONFLOW_BASE`）；`api/rag_env.py:siliconflow_base()` | 默认 `https://api.siliconflow.cn/v1` | 与项目无关 |
| `SILICONFLOW_EMBEDDING_MODEL` | Embedding 模型名 | 可选 | `api/index.py`；`api/rag_env.py:siliconflow_embedding_model()` | **空字符串会被视为未设置**：回退默认 `Qwen/Qwen3-Embedding-0.6B`（避免 CI/环境变量显式空值导致上游 400） | 影响向量空间；需与入库一致 |
| `SILICONFLOW_EMBEDDING_DIMENSIONS` | Embedding 输出维度（Qwen3 需要） | 可选 | `api/index.py`；`api/rag_env.py:siliconflow_embedding_dimensions()` | 默认 `1024`；当模型名包含 `Qwen3-Embedding` 时传给 embeddings API | **必须与** `public.documents.embedding vector(N)` **一致**（默认 N=1024） |
| `SILICONFLOW_CHAT_MODEL` | Chat 模型 | 可选 | `api/index.py` | 默认 `deepseek-ai/DeepSeek-V3` | 与向量维度无关 |
| `NEXT_PUBLIC_ADMIN_SECRET` | Admin/Chat 鉴权 secret | **必填（二选一）** | `api/rag_env.py:admin_secret()` → `api/index.py:_require_auth()` | 留空：鉴权接口 500 | 与项目无关 |
| `CHAT_API_SECRET` | Admin secret 别名 | **可选（二选一）** | `api/rag_env.py:admin_secret()` | 留空则使用 `NEXT_PUBLIC_ADMIN_SECRET` | 与项目无关 |
| `RAG_MATCH_THRESHOLD` | `match_documents` 相似度阈值过滤 | 可选 | `api/index.py:_parse_match_threshold()` | 默认 `0.3`；`none/null/off` 关闭阈值过滤；非法值回退默认 | 与项目无关 |
| `DEBUG_RAG` / `RAG_DEBUG` | RAG 调试日志开关 | 可选 | `api/index.py` | `1/true/yes/on` 或 `NODE_ENV=development` | 与项目无关 |
| `NODE_ENV` | 影响 debug 判定 | 可选 | `api/index.py` | `development` 会打开部分 debug 行为 | 与项目无关 |
| `CONTENT_DEFAULT_YEAR` | 解析 `MM-DD` 日期时的默认年份 | 可选 | `api/index.py` | 默认 `2026` | 与项目无关 |
| `DEBUG_INGEST` | ingest 调试输出 | 可选 | `api/ingest_pipeline.py` | 默认关闭 | 与项目无关 |
| `CONTENT_ROOT` | Markdown 内容根目录（用于 ingest/sync） | 可选 | `api/ingest_pipeline.py:get_all_markdown_chunks()` | 留空：使用后端仓库内 `REPO_ROOT/content`；设置则扫描该目录（不存在则返回空） | 与项目无关 |
| `EMBEDDING_DIM` | 期望向量维度（入库校验） | 可选 | `api/rag_env.py:expected_embedding_dim()` | 默认 `1024` | **必须与** `vector(N)` **一致** |
| `SILICONFLOW_EMBEDDING_DIM` | `EMBEDDING_DIM` 兼容别名 | 可选 | `api/rag_env.py:expected_embedding_dim()` | 留空则看 `EMBEDDING_DIM` | **必须与** `vector(N)` **一致** |

补充：`.cursorrules` 文本里提到 `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY`，但代码实际优先读取 `NEXT_PUBLIC_SUPABASE_URL` 与 `SUPABASE_SERVICE_ROLE_KEY`（并支持别名）。**以代码为准**。

---

## D. 运行与脚本

| 项 | 真值 / 说明 |
|---|---|
| Python 版本建议 | `3.11+`（与前端 CI ingest workflow 对齐） |
| 依赖安装 | `pip install -r requirements.txt` |
| 本地启动 | `python -m uvicorn main:app --host 127.0.0.1 --port 8000` |
| 本仓是否包含 Node | **否**（纯 Python） |
| 包管理器 | **无**（不使用 pnpm/npm） |

---

## E. 目录地图（“去哪改”）

| 目录/文件 | 入口/职责 |
|---|---|
| `main.py` | 本地 `uvicorn` 入口：转发 `api.index:app` |
| `api/index.py` | FastAPI 路由与 RAG 主链路（chat/history/admin） |
| `api/rag_env.py` | `.env` 加载、Supabase/SiliconFlow 选择器、Embedding 参数封装 |
| `api/database_manager.py` | Supabase 写入/读取 `rag_conversation_logs` |
| `api/ingest_pipeline.py` | Markdown ingest/sync、批量 embedding、写 `documents` |
| `supabase/sql/` | 数据库初始化/迁移脚本（`init.sql`、`hybrid_search.sql` 等） |
| `docs/tasks/` | 后端任务规格（Task03/Task04 等） |
| `.github/workflows/` | **本仓当前未发现**（CI 可在前端仓库触发 ingest） |

---

## F. 对外契约（易忘项）

| 契约 | 路径/说明 |
|---|---|
| `GET /api/py/health` | 健康检查 |
| `POST /api/py/chat` | **流式** `text/plain`；检索 hybrid；失败降级策略见下 |
| `GET /api/py/chat/history` | 按 `session_id` 拉取 `rag_conversation_logs` |
| `POST /api/py/admin/ingest` | 同步扫描内容并写入 `documents`（重删再插策略） |
| `POST /api/py/admin/sync` + `GET /api/py/admin/sync?jobId=` | 异步任务（内存队列，serverless 不保证持久） |

### F.1 流式回答 + 证据链（Task04）

| 机制 | 说明 |
|---|---|
| `x-sources` response header | JSON（**percent-encoded**），前端优先解析 |
| 流末尾 marker | `---RAG_SOURCES_JSON---` + JSON（兼容代理丢 header） |

### F.2 检索降级（Embedding 失败）

| 行为 | 说明 |
|---|---|
| Embedding 失败 | **不再 502**；跳过 vector，走 `keyword_documents`（FTS） |
| 日志字段 | `metadata.match.hybrid.mode`：`hybrid` / `keyword_only`；`embedding_error` |

---

## G. 安全与密钥

| 项 | 规则 |
|---|---|
| 绝不能提交进 Git | `.env`、`.env.local`、任何 service role key、SiliconFlow key |
| GitHub Actions（若在本仓跑） | 使用 Secrets 注入；不要写进 workflow 明文 |
| 最小权限原则 | service role key 仅用于服务端；不要暴露给浏览器 |

---

## H. 任务驱动流程（与本仓协作约定）

| 约定 | 说明 |
|---|---|
| 任务入口 | 前端仓库 `content/tasks/*.md` + 本仓库 `docs/tasks/*.md`（后端实现/验收） |
| 子 Agent 交付物（建议） | 本文件：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（持续更新） |
| 变更回填 | 任务完成后应回填：涉及文件、关键 env、SQL 执行顺序、验收 SQL/接口 |

---

## 附：Supabase 必备对象清单（与本仓代码强绑定）

| 对象 | 说明 |
|---|---|
| `public.documents` | 向量列默认 `vector(1024)`（见 `supabase/sql/init.sql`） |
| `public.match_documents(...)` | Vector Top-k + threshold |
| `public.keyword_documents(...)` | FTS keyword 路（见 `supabase/sql/hybrid_search.sql`） |
| `public.refresh_documents_fts_tokens_for_paths(...)` | ingest 后刷新 `fts_tokens`（兜底） |
| `public.rag_conversation_logs` | RAG 全链路日志表 |
