```mermaid
flowchart TD
  %% Entry: /api/py/chat | /api/py/unified/chat(.stream)

  IN[入口 Query] --> AUTH[鉴权<br/>API_KEY / admin_secret]
  AUTH --> HIS[可选: 历史轮次<br/>rag_conversation_logs]
  HIS --> RW[Query Rewrite<br/>query_rewrite.py]
  RW --> KQ[keyword_query_text()<br/>rag_recall_tools.py]
  RW --> EMB[Embedding(SiliconFlow/OpenAI)]

  %% recall branches
  IN -->|date-like| B1[Structured Recall(B1)<br/>metadata.date_norm eq ...]
  EMB --> VEC[Vector RPC<br/>match_documents]
  KQ --> FTS[Keyword RPC<br/>keyword_documents]

  %% reliability/observability
  VEC -. rpc retry .-> VEC
  FTS -. rpc retry .-> FTS

  %% fusion
  B1 --> FUSE[fuse_hits_rrf()<br/>hybrid_fusion.py]
  VEC --> FUSE
  FTS --> FUSE

  %% answer
  FUSE --> CTX[Context Build<br/>topK + strip prefix]
  CTX --> LLM[LLM Answer<br/>temperature=0.2]
  LLM --> SRC[sources payload<br/>build_sources_payload/_build_rag_sources_event]
  SRC --> OUT[返回 JSON / SSE events]

  %% logging
  OUT --> LOG[可选: save_debug_log()<br/>rag_conversation_logs]

  %% on-demand linking
  FTS --> FTS_DOC[加载子流程: 12_flow_fts.md]
  VEC --> RPC_DOC[加载子流程: 13_flow_supabase_rpc.md]
  LOG --> RPC_DOC
```

