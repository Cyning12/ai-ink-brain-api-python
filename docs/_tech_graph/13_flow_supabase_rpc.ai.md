```mermaid
flowchart LR
  %% Supabase RPC + Tables (service_role)
  %% 拓扑协议 v2-Python 适配

  %% === 客户端 ===
  SB[[Supabase Client]] --"service_role"--> AUTH{鉴权?}
  // → api/rag_env.py::supabase_client

  AUTH --"[ok]"--> POOL[(连接池)]
  AUTH --"[err]"--> ERR_AUTH[>Unauthorized/401]
  // → api/index.py::_require_auth
  // → api/index.py::unified_chat_route Depends(require_chatbi_principal)
  // → api/code_retrieval.py::_require_code_api_auth

  POOL --"[err]"--> ERR_NET[>Network/Timeout]
  // → api/rag_recall_tools.py::rpc_execute_with_retry

  %% === documents 表与 RPC ===
  POOL --"->"--> D[(DB: public.documents)]
  POOL --"~>"--> MD[[rpc match_documents()]]
  // → supabase/sql/init.sql::match_documents
  POOL --"~>"--> KD[[rpc keyword_documents()]]
  // → supabase/sql/hybrid_search.sql::keyword_documents
  POOL --"~>"--> RD[[rpc refresh_documents_fts_tokens_for_paths()]]
  // → supabase/sql/hybrid_search.sql::refresh_documents_fts_tokens_for_paths

  MD --"[err]"--> ERR_RPC_MISSING[>RPC 不存在/函数名错误]
  KD --"[err]"--> ERR_RPC_MISSING
  RD --"[err]"--> ERR_RPC_MISSING

  %% === code_chunks 表与 RPC ===
  POOL --"->"--> C[(DB: public.code_chunks)]
  POOL --"~>"--> MC[[rpc match_code_chunks()]]
  // → supabase/sql/code_chunks.sql::match_code_chunks
  POOL --"~>"--> KC[[rpc keyword_code_chunks()]]
  // → supabase/sql/code_chunks.sql::keyword_code_chunks
  POOL --"~>"--> RC[[rpc refresh_code_chunks_fts_tokens_for_paths()]]
  // → supabase/sql/code_chunks.sql::refresh_code_chunks_fts_tokens_for_paths

  MC --"[err]"--> ERR_RPC_MISSING
  KC --"[err]"--> ERR_RPC_MISSING
  RC --"[err]"--> ERR_RPC_MISSING

  %% === logs 表 ===
  POOL --"->"--> L[(DB: public.rag_conversation_logs)]
  // → supabase/sql/create_rag_conversation_logs.sql

  %% === Ingest 写入流 ===
  ING[[Ingest Pipeline]] --"::triggers"--> D
  ING --"::triggers"--> C
  ING --"::triggers"--> RD
  ING --"::triggers"--> RC
  // → api/ingest_pipeline.py

  %% === Chat 读写流 ===
  CHAT[[RAG/Unified Chat]] --"::archives"--> L
  CHAT --"select"--> L
  // → api/database_manager.py

  %% === 样式 ===
  classDef client fill:#e3f2fd,stroke:#1565c0,stroke-width:2px;
  classDef rpc fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
  classDef table fill:#e8f5e9,stroke:#1b5e20,stroke-width:2px;
  classDef pipeline fill:#fff3e0,stroke:#ef6c00,stroke-width:1px;
  classDef err fill:#ffebee,stroke:#b71c1c,stroke-width:1px;

  class SB,POOL client
  class MD,KD,RD,MC,KC,RC rpc
  class D,C,L table
  class ING,CHAT pipeline
  class ERR_AUTH,ERR_NET,ERR_RPC_MISSING err
```
