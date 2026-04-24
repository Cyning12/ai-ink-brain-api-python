```mermaid
flowchart TD
  %% version: 2026-04-24 (main) — 拓扑协议 v2-Python 适配

  %% === 入口阶段 ===
  Q[[用户请求]] --"->"--> E{"@router.dispatch"}
  // → api/index.py#L1

  %% === Unified Chat 分支 ===
  E --"POST /api/py/unified/chat"--> U1[[Unified JSON]]
  E --"POST /api/py/unified/chat/stream"--> U2[[Unified SSE]]
  // → api/unified_chat.py

  U1 --"::branches"--> RAG[[RAG 子流程]]
  U2 --"::branches"--> RAG
  U1 --"::branches"--> T2S[[Text2SQL 子流程]]
  U2 --"::branches"--> T2S

  RAG --"加载"--> RAG_DOC[>10_flow_rag.md]
  T2S --"加载"--> T2S_DOC[>11_flow_text2sql.md]

  %% === Legacy Chat 分支 ===
  E --"POST /api/py/chat"--> C1[[RAG Chat]]
  // → api/index.py
  C1 --"->"--> RAG

  %% === Code RAG 分支 ===
  E --"POST /api/py/code/query"--> CR1[[Code Query]]
  E --"POST /api/py/code/search"--> CR2[[Code Search]]
  // → api/code_retrieval.py

  CR1 --"->"--> RPC[[Supabase RPC 子流程]]
  CR2 --"->"--> RPC
  RPC --"加载"--> RPC_DOC[>13_flow_supabase_rpc.md]

  %% === Admin Ingest 分支 ===
  E --"POST /api/py/admin/sync"--> A1[[Sync Ingest]]
  E --"POST /api/py/admin/ingest"--> A2[[Ingest]]
  // → api/ingest_pipeline.py

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
  class RAG_DOC,T2S_DOC,RPC_DOC,FTS_DOC milestone
```

- `Struct`：[`01_struct.md`](01_struct.md)
- `Version`：[`02_version.md`](02_version.md)
- `RAG Flow`：[`10_flow_rag.md`](10_flow_rag.md) ← [人类友好版](10_flow_rag.md)
- `Text2SQL Flow`：[`11_flow_text2sql.md`](11_flow_text2sql.md) ← [人类友好版](11_flow_text2sql.md)
- `FTS Flow`：[`12_flow_fts.md`](12_flow_fts.md) ← [人类友好版](12_flow_fts.md)
- `Supabase RPC`：[`13_flow_supabase_rpc.md`](13_flow_supabase_rpc.md) ← [人类友好版](13_flow_supabase_rpc.md)
- `Spec`：[`99_spec.md`](99_spec.md)
- `Mermaid Protocol`：[`99_mermaid_protocol.md`](99_mermaid_protocol.md) — 拓扑图绘制规范（Python/FastAPI 适配版）

> **双轨说明**：`.md` = 人类维护版（简洁易读），`.ai.md` = AI 协议版（结构化标记，降低幻觉）。两者语义等价，按需选用。
