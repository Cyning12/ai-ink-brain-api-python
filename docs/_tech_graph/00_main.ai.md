```mermaid
flowchart TD
  %% version: 2026-04-24 (main) — 拓扑协议 v2-Python 适配

  %% === 入口阶段 ===
  Q[[用户请求]] --"->"--> E{"@router.dispatch"}
  // → api/index.py#L434

  %% === Unified Chat 分支 ===
  E --"POST /api/py/unified/chat"--> U1[[Unified JSON]]
  // → api/index.py#L561 unified_chat_route → api/unified_chat.py::handle_unified_chat
  E --"POST /api/py/unified/chat/stream"--> U2[[Unified SSE]]
  // → api/index.py#L576 unified_chat_stream_route → api/unified_chat.py::handle_unified_chat_stream

  U1 --"::branches"--> RAG[[RAG 子流程]]
  U2 --"::branches"--> RAG
  U1 --"::branches"--> T2S[[Text2SQL 子流程]]
  U2 --"::branches"--> T2S

  RAG --"加载"--> RAG_DOC[>10_flow_rag.md]
  T2S --"加载"--> T2S_DOC[>11_flow_text2sql.md]

  %% === Legacy Chat 分支 ===
  E --"POST /api/py/chat"--> C1[[RAG Chat]]
  // → api/index.py#L591 chat
  C1 --"->"--> RAG

  %% === Health/History/Chain ===
  E --"GET /api/py/health"--> HL[[Health]]
  // → api/index.py#L434 health

  E --"GET /api/py/chat/history"--> H1[[Chat History]]
  // → api/index.py#L439 chat_history

  E --"POST /api/py/chain/chat"--> CH[[Chain Timeline]]
  // → api/index.py#L546 chain_chat_route → api/chain_chat.py::handle_chain_chat

  %% === Code RAG 分支 ===
  E --"POST /api/py/code/query"--> CR1[[Code Query]]
  // → api/index.py#L501 code_query → api/code_retrieval.py::handle_code_query
  E --"POST /api/py/code/search"--> CR2[[Code Search]]
  // → api/index.py#L516 code_search → api/code_retrieval.py::handle_code_search

  CR1 --"->"--> RPC[[Supabase RPC 子流程]]
  CR2 --"->"--> RPC
  RPC --"加载"--> RPC_DOC[>13_flow_supabase_rpc.md]

  %% === Runtime / Observability（按需加载）===
  E --"加载"--> OBS_DOC[>14_runtime_observability.md]

  %% === E2E Boundary / Contract（按需加载）===
  E --"加载"--> E2E_DOC[>15_e2e_boundary.md]

  %% === Admin Ingest 分支 ===
  E --"POST /api/py/admin/sync"--> A1[[Sync Ingest]]
  // → api/index.py#L983 admin_sync → api/ingest_pipeline.py::run_sync_job_sync
  E --"POST /api/py/admin/ingest"--> A2[[Ingest]]
  // → api/index.py#L1026 admin_ingest → api/ingest_pipeline.py::process_markdown_files

  A1 --"->"--> RPC
  A2 --"->"--> RPC

  %% === 共享基础设施 ===
  RAG --"->"--> FTS[[FTS 子流程]]
  FTS --"加载"--> FTS_DOC[>12_flow_fts.md]
  T2S --"->"--> RPC
  FTS --"->"--> RPC

  %% === 文档锚点 ===
  classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
  classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px;
  classDef milestone fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;

  class Q,E phase
  class RAG,T2S,RPC,FTS phase
  class RAG_DOC,T2S_DOC,RPC_DOC,FTS_DOC doc
  class RAG_DOC,T2S_DOC,RPC_DOC,FTS_DOC,OBS_DOC,E2E_DOC milestone
```

<!-- AUTO:ENDPOINTS_AND_ANCHORS BEGIN -->
<!-- This block is auto-generated from docs/_tech_graph/_manifest.json. Do not edit manually. -->

#### Endpoints（from manifest）
- `POST /api/py/admin/ingest` → `py_admin_ingest`  // → `api/index.py::py_admin_ingest`
- `GET /api/py/admin/sync` → `py_admin_sync_get`  // → `api/index.py::py_admin_sync_get`
- `POST /api/py/admin/sync` → `py_admin_sync_post`  // → `api/index.py::py_admin_sync_post`
- `POST /api/py/chain/chat` → `chain_chat_route`  // → `api/index.py::chain_chat_route`
- `POST /api/py/chat` → `chat`  // → `api/index.py::chat`
- `GET /api/py/chat/history` → `chat_history`  // → `api/index.py::chat_history`
- `POST /api/py/code/query` → `code_query`  // → `api/index.py::code_query`
- `POST /api/py/code/search` → `code_search`  // → `api/index.py::code_search`
- `GET /api/py/health` → `health`  // → `api/index.py::health`
- `POST /api/py/text2sql/chat` → `text2sql_chat`  // → `api/index.py::text2sql_chat`
- `POST /api/py/unified/chat` → `unified_chat_route`  // → `api/index.py::unified_chat_route`
- `POST /api/py/unified/chat/stream` → `unified_chat_stream_route`  // → `api/index.py::unified_chat_stream_route`

#### Anchors（from manifest）
- `api/database_manager.py::SupabaseManager`
- `api/index.py::_require_auth`
- `api/ingest_pipeline.py::process_markdown_files`
- `api/rag_env.py::admin_secret`
- `api/rag_env.py::pick_supabase_service_key`
- `api/rag_env.py::pick_supabase_url`
<!-- AUTO:ENDPOINTS_AND_ANCHORS END -->

- `Struct`：[`01_struct.md`](01_struct.md)
- `Version`：[`02_version.md`](02_version.md)
- `RAG Flow`：[`10_flow_rag.md`](10_flow_rag.md) ← [人类友好版](10_flow_rag.md)
- `Text2SQL Flow`：[`11_flow_text2sql.md`](11_flow_text2sql.md) ← [人类友好版](11_flow_text2sql.md)
- `FTS Flow`：[`12_flow_fts.md`](12_flow_fts.md) ← [人类友好版](12_flow_fts.md)
- `Supabase RPC`：[`13_flow_supabase_rpc.md`](13_flow_supabase_rpc.md) ← [人类友好版](13_flow_supabase_rpc.md)
- `Spec`：[`99_spec.md`](99_spec.md)
- `Mermaid Protocol`：[`99_mermaid_protocol.md`](99_mermaid_protocol.md) — 拓扑图绘制规范（Python/FastAPI 适配版）

> **双轨说明**：`.md` = 人类维护版（简洁易读），`.ai.md` = AI 协议版（结构化标记，降低幻觉）。两者语义等价，按需选用。
