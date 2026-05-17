# Prompt B V3 执行结果（以 `docs/_tech_graph/` 为索引，代码/SQL 核验）

## P1 易交接

### 1. 冷启动接手清单

1. 克隆仓库 `ai-ink-brain-api-python`，Python **3.11+**，在项目根执行 `pip install -r requirements.txt`。
2. 复制根目录 `.env.example` 为 `.env.local`（或 `.env`），按 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` §C 填写 Supabase URL、service_role、SiliconFlow、`NEXT_PUBLIC_ADMIN_SECRET` / `CHAT_API_SECRET` 等。
3. 打开 `docs/_tech_graph/00_main.md`（人类版）与 `00_main.ai.md`（manifest 注入端点锚点），对照 `_manifest.json` 建立「路由 → handler → 模块」心智模型。
4. 阅读 `docs/_tech_graph/99_spec.md`：了解 CI 门禁脚本名称（manifest check / drift check）及 env 真值图意图。
5. 阅读 `docs/_tech_graph/01_struct.md`，再在 `supabase/sql/init.sql`、`hybrid_search.sql`、`code_chunks.sql` 中抽查表结构与 RPC 是否与图谱一致。
6. 按主链路顺序浏览：`10_flow_rag.md` → `12_flow_fts.md` → `13_flow_supabase_rpc.md`；Unified/Text2SQL/Code/Ingest 分别对应 `api/unified_chat.py`、`api/text2sql_core.py`（及调用链）、`api/code_retrieval.py`、`api/ingest_pipeline.py`。
7. SSE 契约：读 `docs/_tech_graph/_contract_manifest.json`（键名/枚举门禁），辅以 `14_runtime_observability*.md`；Python 产出点在 `api/unified_chat.py`（`_sse` / `_event` 等）。
8. 本地启动：`python -m uvicorn main:app --host 127.0.0.1 --port 8000`（入口见根目录 `main.py` 转发 `api.index:app`）。
9. 冒烟：`curl -s http://127.0.0.1:8000/api/py/health`；带鉴权的接口需在 Header 中提供 `_require_auth` 认可的 token（见 `api/index.py::_require_auth`）。
10. 变更端点/RPC/env/表名后：**必须**更新 `docs/_tech_graph/_manifest.json`，并运行 `python tools/tech_graph_manifest_check.py`；可选运行 `python tools/tech_graph_drift_check.py`。
11. 若涉及 Unified SSE 跨端契约：运行 `python tools/tech_graph_contract_check.py`（CI 中需检出前端仓库 `ai-ink-brain`，见 `.github/workflows/tech-graph-contract.yml`）。
12. 数据库侧：新项目执行 `supabase/sql/` 下脚本顺序以仓库注释为准；向量维度须与 `.env` 中 `EMBEDDING_DIM` / 模型输出一致。
13. 排障：先看 `DEBUG_RAG`/`RAG_DEBUG`/`TEXT2SQL_DEBUG`/`DEBUG_INGEST` 开关（各模块读取点不同），再结合 `rag_conversation_logs` 与图谱 14 的错误分支。

### 2. 锚点索引表

| 类型 | 名称 | 证据位置（路径 · 符号或职责） |
|------|------|------------------------------|
| HTTP | `GET /api/py/health` | `api/index.py` · `health`（约 L434 装饰器 + L435 函数） |
| HTTP | `GET /api/py/chat/history` | `api/index.py` · `chat_history` |
| HTTP | `POST /api/py/chat` | `api/index.py` · `chat`（流式 RAG） |
| HTTP | `POST /api/py/unified/chat` | `api/index.py` · `unified_chat_route` → `api/unified_chat.py::handle_unified_chat` |
| HTTP | `POST /api/py/unified/chat/stream` | `api/index.py` · `unified_chat_stream_route` → `handle_unified_chat_stream` |
| HTTP | `POST /api/py/text2sql/chat` | `api/index.py` · `text2sql_chat` |
| HTTP | `POST /api/py/chain/chat` | `api/index.py` · `chain_chat_route` → `api/chain_chat.py::handle_chain_chat` |
| HTTP | `POST /api/py/code/query` | `api/index.py` · `code_query` → `api/code_retrieval.py::handle_code_query` |
| HTTP | `POST /api/py/code/search` | `api/index.py` · `code_search` |
| HTTP | `POST /api/py/admin/sync` | `api/index.py` · `py_admin_sync_post` → `api/ingest_pipeline.py::run_sync_job_sync`（后台任务） |
| HTTP | `GET /api/py/admin/sync?jobId=` | `api/index.py` · `py_admin_sync_get` |
| HTTP | `POST /api/py/admin/ingest` | `api/index.py` · `py_admin_ingest` → `process_markdown_files` / `process_code_files` |
| 鉴权 | `_require_auth` | `api/index.py` · L206 起；与 `api/rag_env.py::admin_secret` 等配合 |
| RPC | `match_documents` | `api/index.py`、`api/unified_chat.py` 等 `.rpc("match_documents", ...)` |
| RPC | `keyword_documents` | `api/index.py::fetch_keyword_hits`、`api/rag_recall_tools.py`、`api/intent_router.py` 等 |
| RPC | `match_code_chunks` / `keyword_code_chunks` | `api/code_retrieval.py` · 约 L338–395 |
| RPC | `refresh_documents_fts_tokens_for_paths` | `api/ingest_pipeline.py` · 约 L302 起 |
| RPC | `refresh_code_chunks_fts_tokens_for_paths` | `api/code_ingest.py` · 约 L241 |
| 表 | `documents` / `code_chunks` / `rag_conversation_logs` | `supabase/sql/init.sql` 等；应用层 `sb.table(...)` 多处 |
| Manifest | 端点/RPC/表/env 真值 | `docs/_tech_graph/_manifest.json` |
| SSE 契约 | chain/done 事件与最小键 | `docs/_tech_graph/_contract_manifest.json` |

### 3. 新人 FAQ

1. **入口路由都在哪定义？** 主要在 `api/index.py` 的 `@app.get` / `@app.post`；与 `_manifest.json` 的 `endpoints` 数组逐项对齐。**证据**：grep `@app.` + manifest JSON。
2. **Unified 与普通 `/chat` 有什么区别？** Unified 走 `api/unified_chat.py`，集成路由/RAG/Text2SQL/SSE；遗留 `/chat` 仍在 `api/index.py::chat`，侧重 Hybrid RAG 流式。**证据**：两套路由与模块分离。
3. **图谱里的 RPC 名称与 SQL 完全一致吗？** `_manifest.json` 列为权威；`13_flow_supabase_rpc.md` 人类图中节点名有缩写（如「refresh_*」不带 `_for_paths`），以 SQL + Python 调用为准。**证据**：`hybrid_search.sql`/`code_chunks.sql`/`ingest_pipeline.py`。
4. **`TEXT2SQL_DATABASE_URL` 何时必填？** Text2SQL 执行 SQL 分支需要；详见 `PROJECT_CONFIG` 与 `api/text2sql_core.py`（执行路径）。未配置会在执行阶段失败而非 import 阶段。
5. **Admin ingest `type=code` 去哪扫代码？** `py_admin_ingest` 的 `repo_path` query；落到 `process_code_files`。**证据**：`api/index.py` L1027+。
6. **CI 如何保证文档不漂？** PR/push `main` 运行 `.github/workflows/tech-graph.yml` 中的 `python tools/tech_graph_manifest_check.py`；契约工作流见 `tech-graph-contract.yml`。**证据**：工作流 YAML 文件。
7. **为什么有两份 00_main（.md 与 .ai.md）？** `99_mermaid_protocol.md` 双轨说明：人类版与 AI 协议版语义等价；`.ai.md` 含 AUTO 块与 manifest 同步端点列表。
8. **RAG 向量失败会怎样？** 代码路径会记录/降级 keyword（如 `fetch_keyword_hits`、`unified_chat` 内 tool 调用）；具体以 `api/index.py` / `unified_chat.py` 分支为准。

### 4. 改动配方卡

#### 卡 A：新增 HTTP 端点

- **必读文件**：`api/index.py`（路由与鉴权）；`docs/_tech_graph/_manifest.json`（新增 `endpoints` 项）；若影响架构总览则更新 `docs/_tech_graph/00_main*.md`。
- **慎碰点**：与现有路径前缀 `/api/py/` 冲突；遗漏 manifest 会导致 `tech_graph_manifest_check.py` **失败**。
- **推荐验证**：本地起服务后 `curl` 新方法；运行 `python tools/tech_graph_manifest_check.py`。

#### 卡 B：调整检索策略（向量 / keyword / 融合 / threshold）

- **必读文件**：`api/index.py`（`_parse_match_threshold`、`fetch_keyword_hits`、`merge_hits_anchors_first` 等）；`api/rag_recall_tools.py`；`api/hybrid_fusion.py`（若动 RRF）；`api/unified_chat.py`（Unified 工具链）；环境变量 `RAG_MATCH_THRESHOLD`、`RAG_MATCH_COUNT` / `RAG_RPC_RETRIES`（见 `api/rag_env.py` 与 `PROJECT_CONFIG`）。
- **慎碰点**：`match_documents` 阈值为余弦相似度区间 (0,1]（`index.py` 注释）；改变 top_k 需与前端/契约对齐。
- **推荐验证**：单测或本地带 `DEBUG_RAG=1` 打日志；对比 `rag_conversation_logs` 中检索元数据。

#### 卡 C：调整 ingest（markdown / code）

- **必读文件**：`api/ingest_pipeline.py`（`process_markdown_files`、`CONTENT_ROOT`）；`api/code_ingest.py`（代码块与 `refresh_code_chunks_fts_tokens_for_paths`）；`supabase/sql/hybrid_search.sql` / `code_chunks.sql`（FTS 与刷新 RPC）。
- **慎碰点**：批量插入后需刷新 FTS 路径列表；向量维度与 `EMBEDDING_DIM` / 表 `vector(N)` 不一致会 400/500。
- **推荐验证**：`POST /api/py/admin/ingest?type=markdown` 或 `type=code&repo_path=`；检查 Supabase `documents`/`code_chunks` 行数与日志。

---

## P2 可靠性

### 5. 摘要（≤200 字）

FastAPI 后端：`api/index.py` 汇总 health、遗留 `/chat`、Unified（JSON/SSE）、Text2SQL、Chain、代码检索与 Admin ingest/sync；检索依赖 Supabase RPC 与 `documents`/`code_chunks`/`rag_conversation_logs`。以 `docs/_tech_graph/`（`00_main`、`01_struct`、flow10–15、`_manifest.json`、`_contract_manifest.json`）为索引；落地行为必须以源码与 `supabase/sql` 为准并对照图谱缩写。

### 6. 图谱索引摘要 + 模块地图与主链路

**图谱索引摘要（读图目的，非替代核验）**

| 图谱文件 | 用途（索引级） |
|----------|----------------|
| `00_main.md` / `00_main.ai.md` | 全仓 HTTP 分支总览；`.ai.md` 含 `_manifest.json` 注入的端点/handlers 列表 |
| `01_struct.md` | 表与 `metadata` 字段意图（class 图） |
| `99_spec.md` | 事实来源约束、env 拓扑示意、`tools/` 漂移/manifest 门禁说明 |
| `99_mermaid_protocol.md` | 双轨与边标记约定 |
| `10_flow_rag.md` | RAG：鉴权→改写→keyword/向量→融合→LLM→日志 |
| `11_flow_text2sql.md` | Text2SQL：意图→检索→生成→校验→执行→总结 |
| `12_flow_fts.md` | FTS：触发器、`keyword_documents`、可选 i18n 扩展 |
| `13_flow_supabase_rpc.md` | Client→表与 RPC（注意图中 RPC **缩写**） |
| `14_runtime_observability*.md` | SSE 事件类型与排障锚点 |
| `15_e2e_boundary.md` | 前端/BFF/Python/内容仓边界 |
| `_manifest.json` | 机器可读端点、表、RPC、env、anchors 列表 |
| `_contract_manifest.json` | Unified SSE：`chain`/`done` 及 `type` 枚举与最小 payload 键 |

**代码核验后的模块地图与主链路**

1. **Legacy RAG**：`POST /api/py/chat` → `api/index.py::chat`；Hybrid：`match_documents` + `keyword_documents` + 日期锚点合并等；流式 `StreamingResponse`，`x-sources` 与文末 marker（见 `PROJECT_CONFIG` F.1）。
2. **Unified**：`POST /api/py/unified/chat` 与 `/stream` → `api/unified_chat.py`；流式 SSE 事件类型以 `_contract_manifest.json` 为准；RAG/Text2SQL 子路径仍调上述 RPC 与 Text2SQL 执行器。
3. **Text2SQL**：`POST /api/py/text2sql/chat`；`TEXT2SQL_*` env；`11_flow` 图中引用 `docs/text2sql/...` **在本仓库未找到同名路径**（见 §8）。
4. **Ingest / Sync**：`admin/ingest`、`admin/sync` → `ingest_pipeline` / 代码 ingest；刷新 `refresh_*_fts_tokens_for_paths`。
5. **Code RAG**：`code/query`、`code/search` → `code_retrieval.py`；RPC `match_code_chunks`、`keyword_code_chunks`。

### 7. 事实断言清单

| 断言 | 证据 | 核验方式 | 置信度 |
|------|------|----------|--------|
| `GET /api/py/health` 存在 | `api/index.py` L434–435 | grep / 本地 curl | 高 |
| `POST /api/py/unified/chat/stream` 存在 | `api/index.py` L576+ | grep | 高 |
| `_manifest.json` 列出 12 条 endpoint 记录 | `docs/_tech_graph/_manifest.json` | JSON 字段计数 | 高 |
| Python 调用 `refresh_documents_fts_tokens_for_paths` | `api/ingest_pipeline.py` | grep `.rpc(` | 高 |
| `tech-graph.yml` 运行 `manifest_check.py` | `.github/workflows/tech-graph.yml` L22–23 | 读 YAML | 高 |
| `tech-graph-contract.yml` 检出前端并运行 `tech_graph_contract_check.py` | `.github/workflows/tech-graph-contract.yml` | 读 YAML | 高 |
| `documents` 表含 `embedding vector(1024)` | `supabase/sql/init.sql` | 读 SQL | 高 |
| `13_flow_supabase_rpc.md` 图中节点名为 `refresh_documents_fts_tokens`（无 `_for_paths`） | `docs/_tech_graph/13_flow_supabase_rpc.md` | 与 SQL/Python 对照 | 低（图与实现不一致，属文档缩写） |
| `docs/meta/PROJECT_CONFIG_*` 写「本仓当前未发现 workflows」 | `PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` L92–93 | 列目录 `.github/workflows/` | 低（与仓库现状不符） |

### 8. 不确定性与验证步骤

| 不确定性 | 建议验证步骤 |
|----------|----------------|
| `11_flow_text2sql.md` 指向 `docs/text2sql/v1/sql/supabase_init.sql` | 在仓库内 `glob`/搜索；若不存在则修正图谱或补充文档 |
| `15_e2e_boundary.md` 写 SSE 契约锚点为 `14_runtime_observability.ai.md` | 以 `_contract_manifest.json` + `tech_graph_contract_check.py` 为门禁真值；14 图为辅助 |
| Hybrid RRF 与各路由优先级细节 | 对照 `api/hybrid_fusion.py`、`api/intent_router.py` 单测或日志 |
| Admin sync 任务队列在 serverless 下的持久性 | 读 `ingest_pipeline` 中 job 实现；压测重启 |

### 9. 漂移防线（可选小节）

本仓库**实际读到**：

| 路径 | 用途 |
|------|------|
| `tools/tech_graph_manifest_check.py` | manifest 与 `api/index.py`、SQL、`api/*.py` env 等交叉校验（见脚本与 `99_spec.md`） |
| `tools/tech_graph_drift_check.py` | 端点/RPC/env/表名是否在 `docs/_tech_graph/*.md` 覆盖 |
| `tools/tech_graph_contract_check.py` | `_contract_manifest.json` 与 `api/unified_chat.py` SSE 结构 |
| `.github/workflows/tech-graph.yml` | PR/push 运行 manifest check |
| `.github/workflows/tech-graph-contract.yml` | 跨仓契约 check（需检出 `Cyning12/ai-ink-brain` production） |

未单独通读：`tech_graph_render_ai.md` 的渲染脚本行为细节——若修改 AUTO 块流程可再读。

---

## P3/P4

### 10. 消耗明细

- **Token 估算公式（与 Prompt 一致）**：代码/SQL ≈ 12 tokens/行；Markdown（含图谱）≈ 10 tokens/行；命令输出 ≈ 8 tokens/行；本结果正文 ≈ 4 字符 ≈ 1 token。
- **粗算（量级）**：图谱与 manifest 约 2000+ 行×10 ≈ 20k tokens 级阅读；`api/index.py` 等核心代码约千行×12；合成输出约数千 tokens 级。
- **时间（经验估计）**：`t_graph` 30–45 min；`t_read` 核验 25–40 min；`t_synthesis` 20–30 min；`t_total` 约 1.5–2 h（若单人深度读完 flow 双轨）。

### 11. 覆盖率（含「图谱文件清单及目的」）

**图谱文件清单及目的**

| 文件 | 阅读目的 |
|------|----------|
| `00_main.md` | 主干路由与人类版 Mermaid |
| `00_main.ai.md` | 拓扑协议版 + AUTO 端点块 |
| `01_struct.md` | 表与 metadata 意图 |
| `99_spec.md` | CI/env/backlog |
| `99_mermaid_protocol.md` | 双轨与边语义 |
| `10_flow_rag.md` | RAG 子流程 |
| `11_flow_text2sql.md` | Text2SQL 子流程 |
| `12_flow_fts.md` | FTS 与触发器链路 |
| `13_flow_supabase_rpc.md` | RPC 视图（需与 manifest/SQL 校正） |
| `14_runtime_observability.md` | SSE 简图 |
| `14_runtime_observability.ai.md` | SSE 详细事件与错误分支 |
| `15_e2e_boundary.md` | 端到端边界 |
| `_manifest.json` | 机器真值 |
| `_contract_manifest.json` | SSE 契约门禁 |

**代码/SQL（抽样核验，非全仓库逐行）**

- `api/index.py`：路由 grep + L206 `_require_auth`、L434–591、L983–1053 admin、Unified 段落。
- `api/unified_chat.py`、`api/ingest_pipeline.py`、`api/code_retrieval.py`、`api/code_ingest.py`：grep `.rpc(` 与关键调用。
- `supabase/sql/init.sql`、`hybrid_search.sql`、`code_chunks.sql`：RPC/表名抽查。
- `.github/workflows/*.yml`、`tools/tech_graph_*.py`：首部与用途。
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`：§C env。

---

```text
📊 Execution Report
├── Duration: （单次会话合成；约等价 90–120 min 人工工作量）
├── Thinking Steps:
│ 1. 以 `docs/_tech_graph/` 为索引建立章节骨架，再用 grep/read 核验 endpoint/RPC/manifest/CI，避免把图谱缩写当作事实。
│ 2. 将 `13_flow` 与 `_manifest`/SQL 的差异记入断言置信度与不确定性，不把过时 PROJECT_CONFIG 句当作真值。
│ 3. 输出严格遵循 Prompt A/B V3 同级标题顺序，便于与 `result_A_no_tech_graph_v3.md` 横向对比。
├── Files Modified:
│ - ai-ink-brain-api-python/docs/diary/test/result_B_with_tech_graph_v3.md
├── Risk Level: Low
└── Notes: `11_flow_text2sql` 外链路径在本仓库未检出；若以图谱为准部署 Text2SQL DDL 需人工确认实际规格路径。
• Cost Awareness:
• 图谱优先策略减少迷路成本；核验脚本路径已写入漂移防线小节。
• Loop Guard: 不适用（单次落盘）。
• Scope Confirmation: 仅新增约定结果文件，未改业务代码。
```
