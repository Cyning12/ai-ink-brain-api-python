# AI-Ink-Brain API（Python 后端）项目配置真值表（给总 Agent / 子 Agent）

> **最后校准**：2026-05-12（`GET /api/py/chatbi/access/verify` 探活；`GET /api/py/chat/history` 支持 **`X-ChatBI-Access-Token`** 与 `_require_rag_history_auth`；`resolve_chatbi_from_plain_token`）；此前 2026-05-11（V3 P0-2：`CHATBI_JSON_LOG` …）；再前见下文历史行

> 目标：把本仓库的**边界、入口、环境变量、目录地图、对外契约、安全注意事项**整理成“可复制粘贴的真值表”。  
> 说明：本文档只描述**本仓库实际读取/依赖**的内容；前端仓库的 `PY_API_URL`、Next BFF 等不在此展开（但会在边界里点名）。

---

## A. 仓库身份与边界

| 项 | 真值 / 说明 |
|---|---|
| 仓库名（示例） | `ai-ink-brain-api-python` |
| 远程默认分支 | `main`（以你本地 `git branch` / GitHub 默认分支为准） |
| 技术栈摘要 | FastAPI + Uvicorn；OpenAI SDK（指向 SiliconFlow 兼容接口）；`supabase-py`；Supabase（Postgres + pgvector + FTS） |
| 本仓负责的边界（Single Source of Truth） | **Embedding / Chunking / Retrieval / Hybrid Search / RAG 日志** 的权威实现以本仓库代码为准；**Cursor 规则载体**以 `.cursor/rules/*.mdc` 为主，根目录 `.cursorrules` 为兼容/历史参考 |
| 本仓不负责的边界 | **博客页面渲染、内容编辑 UX、Next.js BFF 转发** 在 `ai-ink-brain`；本仓只提供 HTTP API |
| 部署入口（概念） | 本地：`uvicorn main:app`；Vercel：README 说明生产入口为 `api/index.py`（以 Vercel Python Runtime 配置为准） |

---

## B. Cursor / Agent 规则（本仓）

| 文件 | 作用 | 是否必须存在 |
|---|---|---|
| `.cursor/rules/*.mdc` | 分路径规则（图谱、RAG、错误处理等）；**当前推荐的人类/Agent 真值入口** | **建议必须**（当前已存在多份 `.mdc`） |
| `.cursorrules` | 历史/兼容：全仓 AI 规则摘要（若与 `.mdc` 不一致，**以 `.mdc` + 本 `PROJECT_CONFIG` 为准**） | 可选（当前仓库内仍常保留） |
| `AGENTS.md` / `CLAUDE.md` | 额外 Agent 指引 | **本仓 `AGENTS.md` 存在**（`CLAUDE.md` 可选） |

`.cursor/rules` + `.cursorrules` 要点（执行层摘要，以代码为准）：
- RAG 日志必须写入 `rag_conversation_logs`
- pgvector 相似度使用 Cosine Distance（RPC `match_documents`）
- 每次请求必须处理 `session_id`，检索前读取最近 3-5 轮历史（当前实现为 5）
- **Legacy** `POST /api/py/chat` 的助手输出为 **`StreamingResponse`（text/plain）**；**Unified** 另提供 **`POST /api/py/unified/chat`**（JSON `events[]`）与 **`/stream`**（SSE），见 §F
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
| `SUPABASE_HTTP_RETRIES` | PostgREST 请求（`rag_conversation_logs` 等 insert/select）遇 **瞬时网络错误**（如 `Connection reset by peer` / 超时）时的最大尝试次数 | 可选 | `api/rag_env.py:_supabase_http_retry_params()`、`supabase_execute_with_retry`、`supabase_table_insert_with_retry`；`api/unified_chat.py`、`api/agent_memory.py`、`api/database_manager.py` | 默认 `4`；未设时可读别名 **`SUPABASE_INSERT_RETRIES`**；范围 clamp `1`～`12` | 与项目无关 |
| `SUPABASE_HTTP_RETRY_BASE_DELAY_S` | 上述重试的指数退避 **初始间隔**（秒） | 可选 | 同上 | 默认 `0.25`；别名 **`SUPABASE_INSERT_RETRY_BASE_DELAY_S`** | 与项目无关 |
| `SILICONFLOW_API_KEY` | SiliconFlow API Key | **必填** | `api/index.py`（chat）；`api/rag_env.py:must_siliconflow_api_key()`（ingest） | 留空：chat 直接 500；ingest 抛 `RuntimeError` | 与项目无关 |
| `SILICONFLOW_BASE_URL` | OpenAI 兼容 Base URL | 可选 | `api/index.py`（`SILICONFLOW_BASE`）；`api/rag_env.py:siliconflow_base()` | 默认 `https://api.siliconflow.cn/v1` | 与项目无关 |
| `SILICONFLOW_EMBEDDING_MODEL` | Embedding 模型名 | 可选 | `api/index.py`；`api/rag_env.py:siliconflow_embedding_model()` | **空字符串会被视为未设置**：回退默认 `Qwen/Qwen3-Embedding-0.6B`（避免 CI/环境变量显式空值导致上游 400） | 影响向量空间；需与入库一致 |
| `SILICONFLOW_EMBEDDING_DIMENSIONS` | Embedding 输出维度（Qwen3 需要） | 可选 | `api/index.py`；`api/rag_env.py:siliconflow_embedding_dimensions()` | 默认 `1024`；当模型名包含 `Qwen3-Embedding` 时传给 embeddings API | **必须与** `public.documents.embedding vector(N)` **一致**（默认 N=1024） |
| `SILICONFLOW_CHAT_MODEL` | Chat 模型 | 可选 | `api/index.py` | 默认 `deepseek-ai/DeepSeek-V3` | 与向量维度无关 |
| `NEXT_PUBLIC_ADMIN_SECRET` | Admin/Chat 鉴权 secret | **必填（二选一）** | `api/rag_env.py:admin_secret()` → `api/index.py:_require_auth()` | 留空：鉴权接口 500 | 与项目无关 |
| `CHAT_API_SECRET` | Admin secret 别名 | **可选（二选一）** | `api/rag_env.py:admin_secret()` | 留空则使用 `NEXT_PUBLIC_ADMIN_SECRET` | 与项目无关 |
| `CHATBI_USE_AGENT` | Unified Chat 是否走 V2 Agent（ReAct）路径 | 可选 | `api/unified_chat.py` | 默认 `false`；`1/true/yes/on` 开启 V2 | 与项目无关 |
| `CHATBI_SSE_INCREMENTAL` | Unified Agent 流式是否 **边执行边 emit**（vNext） | 可选 | `api/unified_chat.py`（规划） | 默认 **`true`**（vNext 落地后）；`false` 时 **强制** `await run` 后批量 replay，**忽略** `X-ChatBI-Sse-Contract: 2` 的增量语义（仍须安全）；组合真值见 `SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` **§9** | 与项目无关 |
| `CHATBI_SSE_EMIT_QUEUE_MAX` | G2 路径 `emit → asyncio.Queue` 的 **maxsize**（有界缓冲）；队列满时先发 **`agent.llm.truncated`**（`reason=backpressure`）再阻塞入队（vNext §4.3） | 可选 | `api/unified_chat.py` | 默认 **`512`**；合法范围 clamp 为 **`8`～`8192`**；单测可调低以验证背压 | 与项目无关 |
| `CHATBI_V2_DEBUG_LLM_PROMPTS` | V2 Unified：SSE/JSON 是否附带完整 LLM messages（`agent.debug.llm_prompts` 等） | 可选 | `api/unified_chat.py:_debug_llm_prompts_enabled()` | `1`/`true`/`yes`/`on` 开启；与请求体 **`debug_llm_prompts: true`** 任一满足即生效；含 system 指令，生产慎用 | 与项目无关 |
| `CHATBI_JSON_LOG` | V3 P0-2：是否输出 **单行 JSON** 结构化日志（`chatbi.obs`：`text2sql_phase_end` / `text2sql_tool_call_end`；根字段含 **`request_id`/`run_id`**，与 SSE `meta.run_id` 对齐；**`text2sql_phases_ms`** 与 `ToolResult.data` 同形） | 可选 | `api/chatbi_json_log.py`、`api/tools.py::text2sql_execute`、`api/agent.py`（`ChatBIAgent`） | 默认 **关闭**；`1`/`true`/`yes`/`on` 开启；见 `SPEC-ChatBI-V3-Logging-Trace.md` | 与项目无关 |
| `CHATBI_ACCESS_TOKEN_PEPPER` | 可选全局 pepper：参与 `SHA256(pepper_bytes + 明文 token)`，须与运维本地脚本 `docs/diary/local_chatbi_access_token_gen.py` 及 Supabase 插入的 `key_hash` **一致** | 可选 | `api/chatbi_access_hash.py`、`api/chatbi_principal.py`；本地脚本 `docs/diary/local_chatbi_access_token_gen.py` | 留空则 pepper 为空字节串；**勿**把 pepper 提交进 Git | 与项目无关 |
| `CHATBI_AGENT_DB_PERSIST_TIMEOUT_S` | V2 Agent 每轮结束写 `rag_conversation_logs` 的 **最大等待秒数**（在发出 SSE `done` 之前 `await`） | 可选 | `api/unified_chat.py:_await_persist_chatbi_v2_agent_log()` | 默认 `12`；范围 clamp 为 `1`～`120`；超时则 `done.persist.ok=false` 且先发 `error`（`stage=agent_db`） | 与项目无关 |
| `CHATBI_V2_INTENT_LLM` | V2 意图是否调用 SiliconFlow LLM | 可选 | `api/intent_agent.py`；`tests/test_intent_agent_accuracy.py`、`tests/benchmark_intent_latency.py` 等 | 默认 `true`；`false` 为纯启发式/V1 超时降级，**不创建上游 client（CI 零外呼）** | 与项目无关 |
| `INTENT_LLM_MODEL` | 意图识别所用 chat 模型名 | 可选 | `api/intent_agent.py` | 默认 `Qwen/Qwen2.5-7B-Instruct` | 与项目无关 |
| `CHATBI_V2_INTENT_EVAL` | 启用 60 条意图准确率 pytest（`@pytest.mark.intent_eval`） | 可选 | `tests/test_intent_agent_accuracy.py` | 不设为跳过；需密钥时配 `CHATBI_V2_INTENT_LLM=true` + `SILICONFLOW_API_KEY` | 与项目无关 |
| `CHATBI_V2_INTENT_EVAL_OUT` | 评测结果 JSONL/同 stem CSV 输出路径 | 可选 | `tests/test_intent_agent_accuracy.py` | 默认 `tests/_out/intent_accuracy.jsonl`。**相对路径**（推荐）：以 `ai-ink-brain-api-python` 仓库根为锚写 `tests/_out/foo.jsonl`；或以 `tests/` 为锚写 `_out/foo.jsonl`（与 pytest 启动目录无关） | 与项目无关 |
| `CHATBI_V2_INTENT_EVAL_PROGRESS` | 60 条评测是否逐条打印开始/结束行 | 可选 | `tests/test_intent_agent_accuracy.py` | 默认 `true`；CI 内 `test_stub_eval_end_to_end_writes_exports` 强制 `false` | 与项目无关 |
| `CHATBI_V2_INTENT_BENCH_N` | Intent 延迟基准采样次数 | 可选 | `tests/benchmark_intent_latency.py` | 默认 `100` | 与项目无关 |
| `CHATBI_V2_INTENT_BENCH_COLD_WARM` | Intent 延迟脚本是否输出「冷缓存 vs 热缓存」两轮 P50/P95 | 可选 | `tests/benchmark_intent_latency.py` | `1/true/...` 开启；需 `PYTHONPATH=.` 从仓库根运行脚本 | 与项目无关 |
| `DEBUG_INTENT_CACHE` | Intent 缓存诊断日志（仅 `key_hash` + `latency_ms`，不打印完整 query） | 可选 | `api/intent_agent.py` | `1/true/...` 开启 | 与项目无关 |
| `CHATBI_V2_INTENT_TIMEOUT_S` | Intent LLM 单次等待上限（秒），`asyncio.wait_for` 包住上游 `chat.completions`；超时后 `raw_response.used=v1_fallback`，走 V1 规则路由 | 可选 | `api/intent_agent.py`（`decide_intent_v2`）、`tests/benchmark_intent_latency.py` | 未设时沿用调用方默认 `3.0`；SiliconFlow 较慢时建议 `15`～`30`；**60 条 intent_eval 冻结验收**见 `docs/diary/2026-05-06-p1-intent-benchmark.md`（复跑五使用 `60`） | 与项目无关 |
| `INTENT_MIN_CONFIDENCE` | V2 Agent 传入 `decide_intent_v2` 的最低置信度；低于则填 `fallback`（映射见 `api/intent_agent.py:_fallback_tool_by_low_confidence`） | 可选 | `api/agent.py`（`ChatBIAgent`） | 默认 `0.6` | 与项目无关 |
| `CHATBI_V2_INTENT_BENCH_RUN` | 是否执行 pytest 中 B1 延迟基准（`intent_benchmark`） | 可选 | `tests/benchmark_intent_latency.py` | 默认不跑；`true` 时依赖外网与 `SILICONFLOW_API_KEY` | 与项目无关 |
| `RAG_MATCH_THRESHOLD` | `match_documents` 相似度阈值过滤 | 可选 | `api/rag_shared.py:parse_match_threshold()`；由 `api/index.py`（Legacy chat）、`api/unified_chat.py`、`api/code_retrieval.py`（注入）调用 | 默认 `0.3`；`none/null/off` 关闭阈值过滤；非法值或 `<0` 回退默认；`>1` 视为关闭过滤（`None`） | 与项目无关 |
| `DEBUG_RAG` / `RAG_DEBUG` | RAG 调试日志开关 | 可选 | `api/index.py` | `1/true/yes/on` 或 `NODE_ENV=development` | 与项目无关 |
| `NODE_ENV` | 影响 debug 判定 | 可选 | `api/index.py` | `development` 会打开部分 debug 行为 | 与项目无关 |
| `CONTENT_DEFAULT_YEAR` | 解析 `MM-DD` 日期时的默认年份 | 可选 | `api/index.py` | 默认 `2026` | 与项目无关 |
| `DEBUG_INGEST` | ingest 调试输出 | 可选 | `api/ingest_pipeline.py` | 默认关闭 | 与项目无关 |
| `CONTENT_ROOT` | Markdown 内容根目录（用于 ingest/sync） | 可选 | `api/ingest_pipeline.py:get_all_markdown_chunks()` | 留空：使用后端仓库内 `REPO_ROOT/content`；设置则扫描该目录（不存在则返回空） | 与项目无关 |
| `EMBEDDING_DIM` | 期望向量维度（入库校验） | 可选 | `api/rag_env.py:expected_embedding_dim()` | 默认 `1024` | **必须与** `vector(N)` **一致** |
| `SILICONFLOW_EMBEDDING_DIM` | `EMBEDDING_DIM` 兼容别名 | 可选 | `api/rag_env.py:expected_embedding_dim()` | 留空则看 `EMBEDDING_DIM` | **必须与** `vector(N)` **一致** |
| `TEXT2SQL_VALUE_HINTS_PATH` | Text2SQL 列值域 / 同义词 YAML 路径 | 可选 | `api/text2sql_value_hints.py:_resolve_hints_path()` | 留空则使用仓库内 `docs/text2sql/v1/value_hints.yaml`（存在则加载） | 与 Text2SQL 样例库枚举一致 |
| `TEXT2SQL_VALUE_HINTS_ENABLED` | 是否注入值域块 | 可选 | `api/text2sql_value_hints.py:_resolve_hints_path()` | `0`/`false`/`no`/`off` 关闭；未设时默认开启（仍受路径与文件是否存在约束） | 与项目无关 |
| `TEXT2SQL_DISTINCT_PROBE` | 是否对 allowlist 列执行 DISTINCT 并与 YAML `values` 并集 | 可选 | `api/text2sql_value_hints.py:_is_distinct_probe_enabled()` | `1`/`true` 开启；未设或 `0`/`false` 等为关闭 | 依赖 `TEXT2SQL_DATABASE_URL`；失败列降级为仅 YAML |
| `TEXT2SQL_DISTINCT_MAX` | 每条 DISTINCT 的 `LIMIT` 上限 | 可选 | `api/text2sql_value_hints.py:_distinct_row_limit()` | 默认 `64`； clamp 至 `1..500` | 与项目无关 |
| `TEXT2SQL_DISTINCT_COLUMNS` | allowlist：`schema.table.column`，英文逗号分隔 | 可选 | `api/text2sql_value_hints.py:parse_distinct_allowlist()` | 例：`public.agent_info.gender`；仅 `[A-Za-z0-9_]` 段接受 | 与样例库表一致 |
| `TEXT2SQL_DISTINCT_MAX_PROBES` | 单次请求最多执行的探针次数 | 可选 | `api/text2sql_value_hints.py:_distinct_max_probes()` | 默认 `8`； clamp `1..32` | 与项目无关 |
| `TEXT2SQL_DISTINCT_STMT_TIMEOUT_MS` | 单条探针 SQL 的 `statement_timeout`（毫秒） | 可选 | `api/text2sql_value_hints.py:_distinct_statement_timeout_ms()` | 留空则不设置；有值时经 `execute_select_sql(..., statement_timeout_ms=)` 注入 `SET LOCAL` | 与项目无关 |
| `CHATBI_TEXT2SQL_LLM_TIMEOUT_S` | Text2SQL **两段 LLM**（生成 SQL / 总结）共用的 **超时秒数**兜底 | 可选 | `api/tools.py::text2sql_execute`（`asyncio.wait_for`） | **未设**时代码默认 **`120.0`**；当 **`CHATBI_TEXT2SQL_LLM_SQL_TIMEOUT_S` / `CHATBI_TEXT2SQL_LLM_SUMMARY_TIMEOUT_S`** 已分别设置时，本变量仅作二者缺省时的回退 | 与项目无关 |
| `CHATBI_TEXT2SQL_LLM_SQL_TIMEOUT_S` | `llm_generate_sql` 阶段 **timeout**（秒） | 可选 | `api/tools.py::text2sql_execute` | 未设时回退 **`CHATBI_TEXT2SQL_LLM_TIMEOUT_S`** → 再未设则代码默认 **`120.0`** | 与项目无关 |
| `CHATBI_TEXT2SQL_LLM_SUMMARY_TIMEOUT_S` | `llm_summarize` 阶段 **timeout**（秒） | 可选 | `api/tools.py::text2sql_execute` | 未设时回退 **`CHATBI_TEXT2SQL_LLM_TIMEOUT_S`** → 再未设则代码默认 **`120.0`** | 与项目无关 |
| `CHATBI_TEXT2SQL_SUMMARY_LLM_MODEL` | Text2SQL **总结**阶段 chat 模型名（可选加速 / 降级） | 可选 | `api/tools.py::text2sql_execute` | **未设置或仅空白**时，与 **Intent** 默认一致（`INTENT_LLM_MODEL` 默认 `Qwen/Qwen2.5-7B-Instruct`，与 `api/intent_agent.py` 对齐） | 与项目无关 |
| `TEXT2SQL_DIALOGUE_CONTEXT_MAX_LEN` | 多轮 `history_to_rewrite_block` 注入 `build_sql_prompt` 前的 **最大字符数**（超出保留尾部） | 可选 | `api/tools.py::text2sql_execute` | 默认 **`8000`**；`<=0` 表示不截断 | 与项目无关 |

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
| `api/index.py` | FastAPI 路由注册、Legacy **`POST /api/py/chat`** 流式外壳、管理端 ingest/sync、Unified 路由投递至 `unified_chat` |
| `api/unified_chat.py` | Unified Chat：JSON / SSE 事件链、RAG + Text2SQL 路由；详见图谱 `docs/_tech_graph/00_main.md` |
| `api/rag_shared.py` | Legacy 与 Unified 共用的无状态 RAG 小工具（如阈值解析、snippet 去前缀） |
| `api/rag_env.py` | `.env` 加载、Supabase/SiliconFlow 选择器、Embedding 参数封装 |
| `api/database_manager.py` | Supabase 写入/读取 `rag_conversation_logs` |
| `api/ingest_pipeline.py` | Markdown ingest/sync、批量 embedding、写 `documents` |
| `supabase/sql/` | 数据库初始化/迁移脚本（`init.sql`、`hybrid_search.sql` 等） |
| `docs/tasks/` | 后端任务规格（Task03/Task04 等） |
| `docs/_tech_graph/` | 技术图谱与 `_manifest.json` / `_contract_manifest.json`（CI：`tech_graph_manifest_check` / `tech_graph_drift_check`） |
| `.github/workflows/` | **已存在**：`tech-graph.yml`（图谱/契约门禁）、`tech-graph-contract.yml`（契约相关校验）；真值以 YAML 内 jobs 为准 |

---

## F. 对外契约（易忘项）

| 契约 | 路径/说明 |
|---|---|
| `GET /api/py/health` | 健康检查 |
| `POST /api/py/chat` | **流式** `text/plain`；检索 hybrid；失败降级策略见下 |
| `GET /api/py/chat/history` | 按 `session_id` 拉取 `rag_conversation_logs`；**鉴权**：Ink admin（`_require_auth`）**或**请求头 **`X-ChatBI-Access-Token`**（DB 明文，与 Next BFF 对齐；实现见 `api/index.py::_require_rag_history_auth`） |
| `GET /api/py/chatbi/access/verify` | ChatBI 明文 token **探活**（JSON：`ok` / `access_level` / `principal_kind` / `token_id`）；**鉴权**：与 Unified 相同，**仅** `Authorization: Bearer <明文>` → `require_chatbi_principal` |
| `POST /api/py/admin/ingest` | 同步扫描内容并写入 `documents`（重删再插策略） |
| `POST /api/py/admin/sync` + `GET /api/py/admin/sync?jobId=` | 异步任务（内存队列，serverless 不保证持久） |
| `POST /api/py/unified/chat` | Unified 非流式：`events[]` JSON；字段与锚点以 **`docs/_tech_graph/_contract_manifest.json`** 为准；**鉴权**：仅 **`Authorization: Bearer`** + `public.chatbi_access_tokens`（见 `api/chatbi_principal.py`），**不再**接受与 Legacy 相同的 `API_KEY` 明文并行校验 |
| `POST /api/py/unified/chat/stream` | Unified SSE：链式事件流；契约同上；**鉴权**同上 |

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
| `public.chatbi_access_tokens` | ChatBI V3：`key_hash` + `access_level` + `subject_user_id`（L2 必填）；Unified `Depends(require_chatbi_principal)` 查询 |
| `public.chatbi_sql_table_policy` | Text2SQL 表级 `min_*_level`；NULL=该操作类型关闭 |
| `public.chatbi_user_portrait` | L2 肖像/长久 Prompt；写路径列白名单见任务单 |
| `public.documents` | 向量列默认 `vector(1024)`（见 `supabase/sql/init.sql`） |
| `public.match_documents(...)` | Vector Top-k + threshold |
| `public.keyword_documents(...)` | FTS keyword 路（见 `supabase/sql/hybrid_search.sql`） |
| `public.refresh_documents_fts_tokens_for_paths(...)` | ingest 后刷新 `fts_tokens`（兜底） |
| `public.rag_conversation_logs` | RAG 全链路日志表 |
