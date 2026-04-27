```mermaid
flowchart TD
  %% Entry: /api/py/chat | /api/py/unified/chat(.stream)
  %% 拓扑协议 v2-Python 适配

  %% === Query 阶段（软为主）===
  IN[[入口 Query]] --"->"--> AUTH[[鉴权]]
  // → api/index.py::_require_auth
  // → api/unified_chat.py::_require_unified_auth

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
