---
schema: gate_ctx_c_dual_md_main_v1
arm: CTX_DUAL_MD
task_id: T002_unified_sse_chain_contract
freeze_id: TECH_GRAPH_QUERY_COVERAGE_FREEZE_20260519_V1_0
---

<!-- gate_ctx_c dual_track role=ai path=docs/_tech_graph/15_e2e_boundary.ai.md -->
```mermaid
flowchart TD
  %% 15_e2e_boundary: Cross-repo boundary + contracts (AI protocol)
  %% version: 2026-04-27 (p3) — boundary/contract view

  %% === Domains (required 4) ===
  FE[[Frontend: UI SSE consumer]]
  CONTENT[[Content repo: content/ markdown]]
  BE[[Backend API: FastAPI (this repo)]]
  SB[[Supabase: Postgres + RPC]]

  %% === Frontend (SSE consumer / timeline renderer) ===
  FE_STREAM[fetch POST /api/py/unified/chat/stream]
  FE_PARSE[parseSSEBlocks + chainEventFromSse]
  // → ../ai-ink-brain/components/unified-chat/UnifiedChatPageClient.tsx#L286-L352

  FE --"->"--> FE_STREAM --"~>"--> FE_PARSE

  %% === Frontend BFF (Next route proxy) ===
  BFF[[Next BFF: /api/py/unified/chat/stream]]
  // → ../ai-ink-brain/app/api/py/unified/chat/stream/route.ts#L9-L47

  FE_STREAM --"->"--> BFF

  %% === Backend HTTP boundary (endpoints from manifest) ===
  PY_SSE[[POST /api/py/unified/chat/stream]]
  // → docs/_tech_graph/_manifest.json#endpoints[path="/api/py/unified/chat/stream"]
  // → api/index.py::unified_chat_stream_route

  BFF --"->"--> PY_SSE --"~>"--> BE

  %% === SSE contract: envelope + events ===
  SSE_ENV["SSE envelope keys: {event, data}"]
  SSE_EVENTS["SSE event: chain | done"]
  // → api/unified_chat.py::_sse

  PY_SSE --"::yields"--> SSE_EVENTS
  SSE_EVENTS --"->"--> SSE_ENV

  CHAIN_SHAPE["event: chain data keys: {type, ts, step_id, payload}"]
  // → api/unified_chat.py::_event

  DONE_SHAPE["event: done data keys: {ok, mode, run_id, session_id}"]
  // → api/unified_chat.py#L1062-L1065

  SSE_EVENTS --"->"--> CHAIN_SHAPE
  SSE_EVENTS --"->"--> DONE_SHAPE

  %% === Core event types (reference) ===
  EV_TYPES["chain.type set: router.decision | tool.call.start | tool.call.end | rag.query_expand | rag.sources | sql.result | assistant.message | latency | error"]
  // → docs/_tech_graph/14_runtime_observability.ai.md#L17-L27
  SSE_EVENTS --"->"--> EV_TYPES

  %% === Key payload keys (minimal, only list keys) ===
  RS_KEYS["rag.sources.payload.sources[*] keys: {id, content, filename, score, path, url}"]
  // → docs/_tech_graph/14_runtime_observability.ai.md#L34-L38
  SQL_KEYS["sql.result.payload keys: {sql, columns, rows[0..20], truncated}"]
  // → docs/_tech_graph/14_runtime_observability.ai.md#L39-L42

  EV_TYPES --"->"--> RS_KEYS
  EV_TYPES --"->"--> SQL_KEYS

  %% === Content ingest boundary (CONTENT_ROOT) ===
  CONTENT_ROOT[ENV: CONTENT_ROOT -> frontend content/]
  // → api/ingest_pipeline.py#L102-L116 get_all_markdown_chunks
  // → docs/_tech_graph/_manifest.json#env includes CONTENT_ROOT

  CONTENT --"->"--> CONTENT_ROOT --"->"--> BE

  %% === Backend ↔ Supabase boundary (tables/RPC as manifest truth) ===
  SB_TRUTH["Supabase truth: tables+rpc list (manifest)"]
  // → docs/_tech_graph/_manifest.json#supabase

  BE --"->"--> SB_TRUTH --"->"--> SB

  SB_MATCH_DOCS["RPC: public.match_documents(query_embedding, match_count, match_threshold)"]
  // → supabase/sql/init.sql#L50-L76

  SB_TRUTH --"->"--> SB_MATCH_DOCS

  classDef domain fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
  classDef api fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
  classDef payload fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
  classDef data fill:#fff8e1,stroke:#ff6f00,stroke-width:1px;

  class FE,CONTENT,BE,SB domain
  class BFF,PY_SSE,FE_STREAM,FE_PARSE api
  class SSE_ENV,SSE_EVENTS,CHAIN_SHAPE,DONE_SHAPE,EV_TYPES,RS_KEYS,SQL_KEYS payload
  class SB_TRUTH,SB_MATCH_DOCS,CONTENT_ROOT data
```

- 本图只表达“跨仓边界 + 契约锚点”，不展开前端组件树与后端业务子流程。
- 后端端点/表/RPC 以 `docs/_tech_graph/_manifest.json` 为真值；运行事件集合以 `14_runtime_observability.ai.md` 为真值。
- 跨仓 SSE 字段契约以 `docs/_tech_graph/_contract_manifest.json` 为真值；跨端门禁入口为 `python tools/tech_graph_contract_check.py`。
- 跨仓契约门禁已接入 CI：`.github/workflows/tech-graph-contract.yml`（PR / push main 自动执行）。

---
<!-- gate_ctx_c dual_track role=human path=docs/_tech_graph/15_e2e_boundary.md -->
```mermaid
flowchart TD
  %% 15_e2e_boundary: 人类友好版（≤12 节点）

  FE[Frontend UI<br/>SSE timeline renderer]
  BFF[Next BFF<br/>/api/py/unified/chat/stream<br/>ai-ink-brain/app/api/py/unified/chat/stream/route.ts]
  PY[Python FastAPI<br/>POST /api/py/unified/chat/stream<br/>api/index.py::unified_chat_stream_route]
  SSE[SSE events<br/>event: chain | done<br/>api/unified_chat.py::_sse]
  CONTRACT[契约最小键名<br/>chain:{type,ts,step_id,payload}<br/>done:{ok,mode,run_id,session_id}]

  CONTENT[Content repo<br/>content/]
  ROOT[CONTENT_ROOT 边界<br/>api/ingest_pipeline.py::get_all_markdown_chunks]

  DB[Supabase<br/>tables/RPC 以 manifest 为真值]
  RPC[example: match_documents<br/>supabase/sql/init.sql]

  FE --> BFF --> PY --> SSE --> CONTRACT
  CONTENT --> ROOT --> PY
  PY --> DB --> RPC
```

### 锚点与真值来源

- **后端端点/表/RPC 真值**：`docs/_tech_graph/_manifest.json`
- **SSE 事件集合 + 最小字段键**：`docs/_tech_graph/14_runtime_observability.ai.md`
- **前端 SSE 消费锚点**：`../ai-ink-brain/components/unified-chat/UnifiedChatPageClient.tsx`
- **前端 BFF 透传锚点**：`../ai-ink-brain/app/api/py/unified/chat/stream/route.ts`

