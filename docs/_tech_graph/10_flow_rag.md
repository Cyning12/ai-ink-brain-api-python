---
graph_id: 10_flow_rag
version: 2026-06-16
generated_at: 2026-06-16T10:34:43Z
source: docs/_tech_graph/10_flow_rag.graph.yaml
---

# RAG 子流程

RAG 召回、融合、回答与日志归档流程

## Mermaid

```mermaid
flowchart TD
    IN[入口 Query]
    HIS[历史轮次]
    RW[Query Rewrite]
    KQ[keyword_query_text()]
    EMB[async def embed]
    VEC[Vector RPC]
    B1[Structured Recall]
    FUSE[fuse_hits_rrf()]
    HIT0[hits == 0 ?]
    OUT_NO_DATA[no_data / 不确定回答]
    CTX[Context Build]
    LLM[async def llm_answer]
    SRC[sources payload]
    OUT[返回 JSON / SSE]
    LOG[async def save_debug_log]
    DB[DB: rag_conversation_logs]
    ERR_AUTH[>Auth Failed]
    EMB_FAIL[>Embedding Failed]
    KEYWORD_ONLY[keyword-only]
    TEND[tool.call.end payload.keys]
    TEND_KEYS[output.{vector_hits,structured_hits,keyword_hits_raw,keyword_hits_rewrite,hits,retry_count,embedding_error}<br/>error, latency_ms]

    IN --> AUTH
    // → api/index.py::_require_auth
    AUTH --"[ok]"--> HIS
    AUTH --"[err]"--> ERR_AUTH
    // → api/index.py::_require_auth
    HIS --"可选"--> RW
    // → api/query_rewrite.py::rewrite_query_with_history
    HIS --"无历史"--> RW
    RW --"::branches"--> KQ
    RW --"::branches"--> EMB
    // → api/rag_recall_tools.py::keyword_query_text_with_i18n_meta
    KQ --> FTS
    EMB --"~>"--> VEC
    // → api/index.py::fetch_keyword_hits
    // → api/unified_chat.py::rpc_execute_with_retry
    EMB --"[err]"--> EMB_FAIL
    EMB_FAIL --> KEYWORD_ONLY
    FTS --"[retry=N]"--> FTS
    // → api/rag_recall_tools.py::rpc_execute_with_retry
    VEC --"[retry=N]"--> VEC
    FTS --"::merges"--> FUSE
    // → api/hybrid_fusion.py
    VEC --"::merges"--> FUSE
    KEYWORD_ONLY --"::merges"--> FUSE
    B1 --"[ok]"--> FUSE
    B1 --"[err]"--> FUSE
    IN --"date-like ?"--> B1
    // → api/rag_recall_tools.py::structured_recall_by_date
    FUSE --"?>"--> HIT0
    HIT0 --"[yes]"--> OUT_NO_DATA
    // → api/unified_chat.py#L664
    // → api/index.py#L664
    HIT0 --"[no]"--> CTX
    OUT_NO_DATA --> CTX
    FUSE --> CTX
    // → api/unified_chat.py::build_context
    CTX --> LLM
    // → api/unified_chat.py
    LLM --"::yields"--> SRC
    // → api/unified_chat.py::_build_rag_sources_event
    // → api/index.py::build_sources_payload
    SRC --> OUT
    OUT --"::archives"--> LOG
    // → api/database_manager.py
    OUT --"加载"--> OBS_DOC
    LOG --"~>"--> DB
    LOG --"加载"--> RPC_DOC
    FTS --"加载"--> FTS_DOC
    VEC --"加载"--> RPC_DOC
    TEND --> TEND_KEYS

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| IN | 入口 Query |  |
| HIS | 历史轮次 |  |
| RW | Query Rewrite |  |
| KQ | keyword_query_text() |  |
| EMB | async def embed |  |
| VEC | Vector RPC |  |
| B1 | Structured Recall |  |
| FUSE | fuse_hits_rrf() |  |
| HIT0 | hits == 0 ? |  |
| OUT_NO_DATA | no_data / 不确定回答 |  |
| CTX | Context Build |  |
| LLM | async def llm_answer |  |
| SRC | sources payload |  |
| OUT | 返回 JSON / SSE |  |
| LOG | async def save_debug_log |  |
| DB | DB: rag_conversation_logs |  |
| ERR_AUTH | >Auth Failed |  |
| EMB_FAIL | >Embedding Failed |  |
| KEYWORD_ONLY | keyword-only |  |
| TEND | tool.call.end payload.keys |  |
| TEND_KEYS | output.{vector_hits,structured_hits,keyword_hits_raw,keyword_hits_rewrite,hits,retry_count,embedding_error}<br/>error, latency_ms |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| IN | AUTH | -> | depends_on |  | 1 anchor(s) |
| AUTH | HIS | [ok] | depends_on |  |  |
| AUTH | ERR_AUTH | [err] | depends_on |  | 1 anchor(s) |
| HIS | RW | -> | depends_on | 可选 | 1 anchor(s) |
| HIS | RW | -> | depends_on | 无历史 |  |
| RW | KQ | ::branches | branches |  |  |
| RW | EMB | ::branches | branches |  | 1 anchor(s) |
| KQ | FTS | -> | depends_on |  |  |
| EMB | VEC | ~> | async_calls |  | 2 anchor(s) |
| EMB | EMB_FAIL | [err] | depends_on |  |  |
| EMB_FAIL | KEYWORD_ONLY | -> | depends_on |  |  |
| FTS | FTS | [retry=N] | depends_on |  | 1 anchor(s) |
| VEC | VEC | [retry=N] | depends_on |  |  |
| FTS | FUSE | ::merges | merges |  | 1 anchor(s) |
| VEC | FUSE | ::merges | merges |  |  |
| KEYWORD_ONLY | FUSE | ::merges | merges |  |  |
| B1 | FUSE | [ok] | depends_on |  |  |
| B1 | FUSE | [err] | depends_on |  |  |
| IN | B1 | -> | condition | date-like ? | 1 anchor(s) |
| FUSE | HIT0 | ?> | condition |  |  |
| HIT0 | OUT_NO_DATA | [yes] | depends_on |  | 2 anchor(s) |
| HIT0 | CTX | [no] | depends_on |  |  |
| OUT_NO_DATA | CTX | -> | depends_on |  |  |
| FUSE | CTX | -> | depends_on |  | 1 anchor(s) |
| CTX | LLM | -> | depends_on |  | 1 anchor(s) |
| LLM | SRC | ::yields | yields |  | 2 anchor(s) |
| SRC | OUT | -> | depends_on |  |  |
| OUT | LOG | ::archives | archives |  | 1 anchor(s) |
| OUT | OBS_DOC | -> | depends_on | 加载 |  |
| LOG | DB | ~> | async_calls |  |  |
| LOG | RPC_DOC | -> | depends_on | 加载 |  |
| FTS | FTS_DOC | -> | depends_on | 加载 |  |
| VEC | RPC_DOC | -> | depends_on | 加载 |  |
| TEND | TEND_KEYS | -> | depends_on |  |  |
