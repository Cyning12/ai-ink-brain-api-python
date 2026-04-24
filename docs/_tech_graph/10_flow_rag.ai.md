```mermaid
flowchart TD
  %% Entry: /api/py/chat | /api/py/unified/chat(.stream)
  %% 拓扑协议 v2-Python 适配

  %% === Query 阶段（软为主）===
  IN[[入口 Query]] --"->"--> AUTH[[鉴权]]
  // → api/index.py#L1

  AUTH --"[ok]"--> HIS[[历史轮次]]
  AUTH --"[err]"--> ERR_AUTH[>Auth Failed]
  // → api/index.py::verify_token

  HIS --"可选"--> RW[[Query Rewrite]]
  // → api/query_rewrite.py
  HIS --"无历史"--> RW

  %% === Work 阶段（硬为主）===
  RW --"::branches"--> KQ[[keyword_query_text()]]
  RW --"::branches"--> EMB[[async def embed]]
  // → api/rag_recall_tools.py

  KQ --"->"--> FTS[[FTS RPC]]
  EMB --"~>"--> VEC[[Vector RPC]]
  // → api/rag_recall_tools.py

  %% === 结构化召回分支 ===
  IN --"date-like ?>"--> B1[[Structured Recall]]
  // → api/rag_recall_tools.py::structured_recall
  B1 --"[ok]"--> FUSE
  B1 --"[err]"--> FUSE

  %% === RPC 可靠性 ===
  VEC --"[retry=3]"--> VEC
  FTS --"[retry=3]"--> FTS
  // → api/rag_env.py::supabase_client

  %% === Fusion 阶段 ===
  VEC --"::merges"--> FUSE[[fuse_hits_rrf()]]
  FTS --"::merges"--> FUSE
  // → api/hybrid_fusion.py

  %% === Answer 阶段 ===
  FUSE --"->"--> CTX[[Context Build]]
  // → api/unified_chat.py::build_context

  CTX --"->"--> LLM[[async def llm_answer]]
  // → api/unified_chat.py

  LLM --"::yields"--> SRC[[sources payload]]
  // → api/unified_chat.py::_build_rag_sources_event

  SRC --"->"--> OUT[[返回 JSON / SSE]]

  %% === 归档阶段 ===
  OUT --"::archives"--> LOG[[async def save_debug_log]]
  // → api/database_manager.py

  LOG --"~>"--> DB[(DB: rag_conversation_logs)]

  %% === 子流程链接 ===
  FTS --"加载"--> FTS_DOC[>12_flow_fts.md]
  VEC --"加载"--> RPC_DOC[>13_flow_supabase_rpc.md]
  LOG --"加载"--> RPC_DOC

  %% === 样式 ===
  classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
  classDef fn fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
  classDef data fill:#e8f5e9,stroke:#1b5e20,stroke-width:1px;
  classDef milestone fill:#fff8e1,stroke:#e65100,stroke-width:2px;
  classDef err fill:#ffebee,stroke:#b71c1c,stroke-width:1px;

  class IN,Auth,RW,FUSE,CTX,LLM,SRC,OUT,LOG phase
  class KQ,EMB,FTS,VEC,B1 fn
  class DB data
  class FTS_DOC,RPC_DOC milestone
  class ERR_AUTH err
```
