---
schema: gate_ctx_c_dual_md_main_v1
arm: CTX_DUAL_MD
task_id: T001_embedding_dim_default
freeze_id: TECH_GRAPH_GATE_D_V2_TASKS_FREEZE_20260520_V1_0
---

<!-- gate_ctx_c dual_track role=ai path=docs/_tech_graph/10_flow_rag.ai.md -->
```mermaid
flowchart TD
  %% Entry: /api/py/chat | /api/py/unified/chat(.stream)
  %% 拓扑协议 v2-Python 适配

  %% === Query 阶段（软为主）===
  IN[[入口 Query]] --"->"--> AUTH[[鉴权]]
  // → api/index.py::_require_auth
  // → api/index.py::unified_chat_route Depends(require_chatbi_principal)

  AUTH --"[ok]"--> HIS[[历史轮次]]
  AUTH --"[err]"--> ERR_AUTH[>Auth Failed]
  // → api/index.py::_require_auth

  HIS --"可选"--> RW[[Query Rewrite]]
  // → api/query_rewrite.py::rewrite_query_with_history
  HIS --"无历史"--> RW

  %% === Work 阶段（硬为主）===
  RW --"::branches"--> KQ[[keyword_query_text()]]
  RW --"::branches"--> EMB[[async def embed]]
  // → api/rag_recall_tools.py::keyword_query_text_with_i18n_meta
  // → api/unified_chat.py::embedding_kwargs_for_inputs (via api/rag_env.py)

  KQ --"->"--> FTS[[FTS RPC]]
  EMB --"~>"--> VEC[[Vector RPC]]
  // → api/index.py::fetch_keyword_hits
  // → api/unified_chat.py::rpc_execute_with_retry

  EMB --"[err]"--> EMB_FAIL[>Embedding Failed]
  // → api/index.py#L669 (embedding failed -> keyword-only)
  // → api/unified_chat.py#L527 (vec=None)
  EMB_FAIL --"->"--> KEYWORD_ONLY[[keyword-only]]
  KEYWORD_ONLY --"::merges"--> FUSE

  %% === 结构化召回分支 ===
  IN --"date-like ?>"--> B1[[Structured Recall]]
  // → api/rag_recall_tools.py::structured_recall_by_date
  B1 --"[ok]"--> FUSE
  B1 --"[err]"--> FUSE

  %% === RPC 可靠性 ===
  VEC --"[retry=N]"--> VEC
  FTS --"[retry=N]"--> FTS
  // → api/rag_recall_tools.py::rpc_execute_with_retry
  // → api/unified_chat.py#L571 (N = int(os.getenv('RAG_RPC_RETRIES','2')))

  %% === Fusion 阶段 ===
  VEC --"::merges"--> FUSE[[fuse_hits_rrf()]]
  FTS --"::merges"--> FUSE
  // → api/hybrid_fusion.py

  FUSE --"?>"--> HIT0{hits == 0 ?}
  HIT0 --"[yes]"--> OUT_NO_DATA[[no_data / 不确定回答]]
  // → api/unified_chat.py#L664
  // → api/index.py#L664
  HIT0 --"[no]"--> CTX
  OUT_NO_DATA --"->"--> CTX

  %% === Answer 阶段 ===
  FUSE --"->"--> CTX[[Context Build]]
  // → api/unified_chat.py::build_context

  CTX --"->"--> LLM[[async def llm_answer]]
  // → api/unified_chat.py

  LLM --"::yields"--> SRC[[sources payload]]
  // → api/unified_chat.py::_build_rag_sources_event
  // → api/index.py::build_sources_payload

  %% tool.call.end payload（字段名，便于排障定位）
  TEND[[tool.call.end payload.keys]]
  TEND --"includes"--> TEND_KEYS["output.{vector_hits,structured_hits,keyword_hits_raw,keyword_hits_rewrite,hits,retry_count,embedding_error}<br/>error, latency_ms"]
  // → api/unified_chat.py::_event + tool.call.end payload
  // → api/index.py#L623 (save_debug_log payload.metadata.latency_ms / match.*)

  SRC --"->"--> OUT[[返回 JSON / SSE]]

  %% === 归档阶段 ===
  OUT --"::archives"--> LOG[[async def save_debug_log]]
  // → api/database_manager.py

  LOG --"~>"--> DB[(DB: rag_conversation_logs)]

  %% === 子流程链接 ===
  FTS --"加载"--> FTS_DOC[>12_flow_fts.md]
  VEC --"加载"--> RPC_DOC[>13_flow_supabase_rpc.md]
  LOG --"加载"--> RPC_DOC
  OUT --"加载"--> OBS_DOC[>14_runtime_observability.md]

  %% === 样式 ===
  classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
  classDef fn fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
  classDef data fill:#e8f5e9,stroke:#1b5e20,stroke-width:1px;
  classDef milestone fill:#fff8e1,stroke:#e65100,stroke-width:2px;
  classDef err fill:#ffebee,stroke:#b71c1c,stroke-width:1px;

  class IN,AUTH,HIS,RW,FUSE,CTX,LLM,SRC,OUT,LOG phase
  class KQ,EMB,FTS,VEC,B1,KEYWORD_ONLY,TEND fn
  class DB data
  class FTS_DOC,RPC_DOC,OBS_DOC milestone
  class ERR_AUTH err
  class EMB_FAIL,OUT_NO_DATA err
```

---
<!-- gate_ctx_c dual_track role=human path=docs/_tech_graph/10_flow_rag.md -->
```mermaid
flowchart TD
    %% Entry: /api/py/chat | /api/py/unified/chat(.stream)

    %% Query 阶段
    IN[入口 Query] --> AUTH[鉴权<br/>API_KEY / admin_secret]
    AUTH --> HIS[历史轮次<br/>rag_conversation_logs]
    HIS --> RW[Query Rewrite<br/>query_rewrite.py]

    %% 召回分支
    RW --> KQ[Keyword 查询<br/>rag_recall_tools.py]
    RW --> EMB[Embedding<br/>SiliconFlow / OpenAI]
    EMB -->|fail| FBO[降级<br/>keyword-only]

    IN -->|date-like| B1[结构化召回<br/>metadata.date_norm]

    KQ --> FTS[Keyword RPC<br/>keyword_documents]
    EMB --> VEC[Vector RPC<br/>match_documents]

    %% 可靠性
    VEC -. rpc retry .-> VEC
    FTS -. rpc retry .-> FTS
    VEC -->|0 hits| NH[0 hits]
    FTS -->|0 hits| NH
    NH --> OUT[返回 JSON / SSE]

    %% Fusion
    B1 --> FUSE[RRF 融合<br/>hybrid_fusion.py]
    VEC --> FUSE
    FTS --> FUSE

    %% Answer
    FUSE --> CTX[Context 构建<br/>topK + strip prefix]
    CTX --> LLM[LLM 回答<br/>temperature=0.2]
    LLM --> SRC[Sources 载荷<br/>build_sources_payload]
    SRC --> OUT[返回 JSON / SSE]

    %% 日志
    OUT --> LOG[Debug 日志<br/>rag_conversation_logs]

    %% 子流程链接
    FTS --> FTS_DOC[> 12_flow_fts.md]
    VEC --> RPC_DOC[> 13_flow_supabase_rpc.md]
    LOG --> RPC_DOC

    %% 样式
    classDef query fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef recall fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef answer fill:#fff8e1,stroke:#ff6f00,stroke-width:2px
    classDef infra fill:#f3e5f5,stroke:#4a148c,stroke-width:1px

    class IN,Auth,HIS,RW query
    class KQ,EMB,B1,FTS,VEC,FUSE recall
    class CTX,LLM,SRC,OUT answer
    class LOG,FTS_DOC,RPC_DOC infra
```

