```mermaid
flowchart TD
  %% version: 2026-04-23 (main)

  Q[用户请求<br/>HTTP API] --> E{入口路由<br/>api/index.py}

  %% unified
  E -->|POST /api/py/unified/chat| U1[Unified JSON<br/>api/unified_chat.py]
  E -->|POST /api/py/unified/chat/stream| U2[Unified SSE<br/>api/unified_chat.py]
  U1 --> RAG[加载子流程: 10_flow_rag.md]
  U2 --> RAG
  U1 --> T2S[加载子流程: 11_flow_text2sql.md]
  U2 --> T2S

  %% legacy chat
  E -->|POST /api/py/chat| C1[RAG Chat<br/>api/index.py]
  C1 --> RAG

  %% code rag
  E -->|POST /api/py/code/query| CR1[Code Query<br/>api/code_retrieval.py]
  E -->|POST /api/py/code/search| CR2[Code Search<br/>api/code_retrieval.py]
  CR1 --> RPC[加载子流程: 13_flow_supabase_rpc.md]
  CR2 --> RPC

  %% admin ingest
  E -->|POST /api/py/admin/sync| A1[Sync ingest<br/>api/ingest_pipeline.py]
  E -->|POST /api/py/admin/ingest| A2[Ingest<br/>api/ingest_pipeline.py]
  A1 --> RPC
  A2 --> RPC

  %% shared infra
  RAG --> FTS[加载子流程: 12_flow_fts.md]
  T2S --> RPC
  FTS --> RPC

  %% docs links (human clickable)
  classDef link fill:#fff,stroke:#bbb,stroke-width:1px;
```

- `Struct`：[`01_struct.md`](01_struct.md)
- `Version`：[`02_version.md`](02_version.md)
- `RAG Flow`：[`10_flow_rag.md`](10_flow_rag.md)
- `Text2SQL Flow`：[`11_flow_text2sql.md`](11_flow_text2sql.md)
- `FTS Flow`：[`12_flow_fts.md`](12_flow_fts.md)
- `Supabase RPC`：[`13_flow_supabase_rpc.md`](13_flow_supabase_rpc.md)
- `Spec`：[`99_spec.md`](99_spec.md)
- `Mermaid Protocol`：[`99_mermaid_protocol.md`](99_mermaid_protocol.md) — 拓扑图绘制规范（Python/FastAPI 适配版）

