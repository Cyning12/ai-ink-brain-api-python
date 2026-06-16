---
graph_id: 13_flow_supabase_rpc
version: 2026-06-16
generated_at: 2026-06-16T12:08:13Z
source: docs/_tech_graph/13_flow_supabase_rpc.graph.yaml
---

# Supabase RPC 子流程

Supabase 客户端鉴权、连接池、documents/code_chunks 表与 RPC、rag_conversation_logs 归档流程

## Mermaid

```mermaid
flowchart LR
    C[(DB: public.code_chunks)]
    CHAT[RAG/Unified Chat]
    D[(DB: public.documents)]
    ERR_NET[>Network/Timeout]
    ERR_RPC_MISSING[>RPC 不存在/函数名错误]
    ING[Ingest Pipeline]
    KC[rpc keyword_code_chunks()]
    KD[rpc keyword_documents()]
    L[(DB: public.rag_conversation_logs)]
    MC[rpc match_code_chunks()]
    MD[rpc match_documents()]
    POOL[(连接池)]
    RC[rpc refresh_code_chunks_fts_tokens_for_paths()]
    RD[rpc refresh_documents_fts_tokens_for_paths()]
    SB[Supabase Client]

    AUTH --"[err]"--> ERR_AUTH
    // → api/index.py::_require_auth
    // → api/code_retrieval.py::_require_code_api_auth
    AUTH --"[ok]"--> POOL
    CHAT --> L
    // → api/database_manager.py
    CHAT --"::archives"--> L
    ING --"::triggers"--> C
    ING --"::triggers"--> D
    ING --"::triggers"--> RC
    // → api/ingest_pipeline.py
    ING --"::triggers"--> RD
    KC --"[err]"--> ERR_RPC_MISSING
    KD --"[err]"--> ERR_RPC_MISSING
    MC --"[err]"--> ERR_RPC_MISSING
    MD --"[err]"--> ERR_RPC_MISSING
    POOL --> C
    POOL --> D
    POOL --"[err]"--> ERR_NET
    // → api/rag_recall_tools.py::rpc_execute_with_retry
    POOL --"~>"--> KC
    // → supabase/sql/code_chunks.sql::keyword_code_chunks
    POOL --"~>"--> KD
    // → supabase/sql/hybrid_search.sql::keyword_documents
    POOL --> L
    // → supabase/sql/create_rag_conversation_logs.sql
    POOL --"~>"--> MC
    // → supabase/sql/code_chunks.sql::match_code_chunks
    POOL --"~>"--> MD
    // → supabase/sql/init.sql::match_documents
    POOL --"~>"--> RC
    // → supabase/sql/code_chunks.sql::refresh_code_chunks_fts_tokens_for_paths
    POOL --"~>"--> RD
    // → supabase/sql/hybrid_search.sql::refresh_documents_fts_tokens_for_paths
    RC --"[err]"--> ERR_RPC_MISSING
    RD --"[err]"--> ERR_RPC_MISSING
    SB --> AUTH
    // → api/rag_env.py::supabase_client

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| C | (DB: public.code_chunks) |  |
| CHAT | RAG/Unified Chat |  |
| D | (DB: public.documents) |  |
| ERR_NET | >Network/Timeout |  |
| ERR_RPC_MISSING | >RPC 不存在/函数名错误 |  |
| ING | Ingest Pipeline |  |
| KC | rpc keyword_code_chunks() |  |
| KD | rpc keyword_documents() |  |
| L | (DB: public.rag_conversation_logs) |  |
| MC | rpc match_code_chunks() |  |
| MD | rpc match_documents() |  |
| POOL | (连接池) |  |
| RC | rpc refresh_code_chunks_fts_tokens_for_paths() |  |
| RD | rpc refresh_documents_fts_tokens_for_paths() |  |
| SB | Supabase Client |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| AUTH | ERR_AUTH | [err] | depends_on |  | 2 anchor(s) |
| AUTH | POOL | [ok] | depends_on |  |  |
| CHAT | L | -> | depends_on |  | 1 anchor(s) |
| CHAT | L | ::archives | archives |  |  |
| ING | C | ::triggers | triggers |  |  |
| ING | D | ::triggers | triggers |  |  |
| ING | RC | ::triggers | triggers |  | 1 anchor(s) |
| ING | RD | ::triggers | triggers |  |  |
| KC | ERR_RPC_MISSING | [err] | depends_on |  |  |
| KD | ERR_RPC_MISSING | [err] | depends_on |  |  |
| MC | ERR_RPC_MISSING | [err] | depends_on |  |  |
| MD | ERR_RPC_MISSING | [err] | depends_on |  |  |
| POOL | C | -> | depends_on |  |  |
| POOL | D | -> | depends_on |  |  |
| POOL | ERR_NET | [err] | depends_on |  | 1 anchor(s) |
| POOL | KC | ~> | async_calls |  | 1 anchor(s) |
| POOL | KD | ~> | async_calls |  | 1 anchor(s) |
| POOL | L | -> | depends_on |  | 1 anchor(s) |
| POOL | MC | ~> | async_calls |  | 1 anchor(s) |
| POOL | MD | ~> | async_calls |  | 1 anchor(s) |
| POOL | RC | ~> | async_calls |  | 1 anchor(s) |
| POOL | RD | ~> | async_calls |  | 1 anchor(s) |
| RC | ERR_RPC_MISSING | [err] | depends_on |  |  |
| RD | ERR_RPC_MISSING | [err] | depends_on |  |  |
| SB | AUTH | -> | depends_on |  | 1 anchor(s) |

## Notes

### 客户端与鉴权

- `SB` 通过 `api/rag_env.py::supabase_client` 初始化，使用 `service_role` 密钥。
- `AUTH` 分支覆盖 `api/index.py::_require_auth`、`api/index.py::unified_chat_route`、`api/code_retrieval.py::_require_code_api_auth`。

### 关键 SQL 文件

- `supabase/sql/init.sql`：`match_documents`
- `supabase/sql/hybrid_search.sql`：`keyword_documents`、`refresh_documents_fts_tokens_for_paths`
- `supabase/sql/code_chunks.sql`：`match_code_chunks`、`keyword_code_chunks`、`refresh_code_chunks_fts_tokens_for_paths`
- `supabase/sql/create_rag_conversation_logs.sql`：`rag_conversation_logs`


