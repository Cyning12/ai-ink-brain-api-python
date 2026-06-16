---
graph_id: 14_runtime_observability
version: 2026-06-16
generated_at: 2026-06-16T12:08:13Z
source: docs/_tech_graph/14_runtime_observability.graph.yaml
---

# Runtime/Observability 子流程

Unified Chat 运行时可观测性视角：SSE 事件包、工具调用、RAG/Text2SQL 证据、错误最短路径、调试开关

## Mermaid

```mermaid
flowchart TD
    AM[assistant.message]
    DONE[event: done]
    ENV[Debug env toggles]
    ENV_KEYS["DEBUG_RAG / RAG_DEBUG / NODE_ENV / DEBUG_INGEST / DEBUG_INTENT_CACHE / DEBUG_AGENT_DB_LOG / DEBUG_ROUTER_EVIDENCE / DEBUG_ROUTER_EVIDENCE_DB / DEBUG_ROUTER_TRACE_DB"]
    ERR[error]
    EV[event: chain]
    E_EMB[Embedding error -> keyword-only]
    E_EXECSQL[TEXT2SQL_DATABASE_URL missing / DB error]
    E_GENSQL[validate_sql_readonly [err]
    E_ROUTER[未实现工具路由 / 参数错误]
    E_RPC[RPC error / retries exhausted]
    JSON[JSON response]
    LAT[latency]
    QX[rag.query_expand]
    R1[router.decision]
    REQ[HTTP Request]
    RS[rag.sources]
    SQLR[sql.result]
    SQL_KEYS["{sql, columns, rows[0..20], truncated}"]
    SRC_KEYS["{id, content, filename, score, path, url}"]
    SSE[{SSE?]
    TCE[tool.call.end]
    TCE_KEYS["{output, error, latency_ms}"]
    TCS[tool.call.start]
    TCS_KEYS["{tool, input}"]

    AM --"::archives"--> LOG
    // → api/database_manager.py::save_debug_log
    ENV --> ENV_KEYS
    // → api/index.py::_rag_debug_enabled
    // → api/ingest_pipeline.py#L33
    ERR --"stage=rag.embed"--> E_EMB
    ERR --"stage=text2sql.execute_sql"--> E_EXECSQL
    // → api/unified_chat.py::handle_unified_chat(_stream)
    // → api/text2sql_core.py::execute_select_sql
    ERR --"stage=text2sql.generate_sql"--> E_GENSQL
    ERR --"stage=router"--> E_ROUTER
    ERR --"stage=rag.retrieve"--> E_RPC
    EV --"type=assistant.message"--> AM
    EV --"type=error"--> ERR
    // → api/unified_chat.py::_event
    EV --"type=latency"--> LAT
    EV --"type=rag.query_expand"--> QX
    EV --"type=router.decision"--> R1
    EV --"type=rag.sources"--> RS
    EV --"type=sql.result"--> SQLR
    EV --"type=tool.call.end"--> TCE
    EV --"type=tool.call.start"--> TCS
    LOG --> DB
    REQ --> SSE
    // → api/unified_chat.py::handle_unified_chat_stream
    RS --"payload.sources[*]"--> SRC_KEYS
    // → api/unified_chat.py::_build_rag_sources_event
    // → api/index.py::build_sources_payload
    SQLR --"payload"--> SQL_KEYS
    // → api/unified_chat.py#L425
    SSE --"[yes]"--> DONE
    // → api/unified_chat.py::_sse
    SSE --"[yes]"--> EV
    SSE --"[no]"--> JSON
    // → api/unified_chat.py::handle_unified_chat
    TCE --"payload"--> TCE_KEYS
    TCS --"payload"--> TCS_KEYS

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| AM | assistant.message |  |
| DONE | event: done |  |
| ENV | Debug env toggles |  |
| ENV_KEYS | "DEBUG_RAG / RAG_DEBUG / NODE_ENV / DEBUG_INGEST / DEBUG_INTENT_CACHE / DEBUG_AGENT_DB_LOG / DEBUG_ROUTER_EVIDENCE / DEBUG_ROUTER_EVIDENCE_DB / DEBUG_ROUTER_TRACE_DB" |  |
| ERR | error |  |
| EV | event: chain |  |
| E_EMB | Embedding error -> keyword-only |  |
| E_EXECSQL | TEXT2SQL_DATABASE_URL missing / DB error |  |
| E_GENSQL | validate_sql_readonly [err |  |
| E_ROUTER | 未实现工具路由 / 参数错误 |  |
| E_RPC | RPC error / retries exhausted |  |
| JSON | JSON response |  |
| LAT | latency |  |
| QX | rag.query_expand |  |
| R1 | router.decision |  |
| REQ | HTTP Request |  |
| RS | rag.sources |  |
| SQLR | sql.result |  |
| SQL_KEYS | "{sql, columns, rows[0..20], truncated}" |  |
| SRC_KEYS | "{id, content, filename, score, path, url}" |  |
| SSE | {SSE? |  |
| TCE | tool.call.end |  |
| TCE_KEYS | "{output, error, latency_ms}" |  |
| TCS | tool.call.start |  |
| TCS_KEYS | "{tool, input}" |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| AM | LOG | ::archives | archives |  | 1 anchor(s) |
| ENV | ENV_KEYS | -> | depends_on |  | 2 anchor(s) |
| ERR | E_EMB | -> | depends_on | stage=rag.embed |  |
| ERR | E_EXECSQL | -> | depends_on | stage=text2sql.execute_sql | 2 anchor(s) |
| ERR | E_GENSQL | -> | depends_on | stage=text2sql.generate_sql |  |
| ERR | E_ROUTER | -> | depends_on | stage=router |  |
| ERR | E_RPC | -> | depends_on | stage=rag.retrieve |  |
| EV | AM | -> | depends_on | type=assistant.message |  |
| EV | ERR | -> | depends_on | type=error | 1 anchor(s) |
| EV | LAT | -> | depends_on | type=latency |  |
| EV | QX | -> | depends_on | type=rag.query_expand |  |
| EV | R1 | -> | depends_on | type=router.decision |  |
| EV | RS | -> | depends_on | type=rag.sources |  |
| EV | SQLR | -> | depends_on | type=sql.result |  |
| EV | TCE | -> | depends_on | type=tool.call.end |  |
| EV | TCS | -> | depends_on | type=tool.call.start |  |
| LOG | DB | -> | depends_on |  |  |
| REQ | SSE | -> | depends_on |  | 1 anchor(s) |
| RS | SRC_KEYS | -> | depends_on | payload.sources[*] | 2 anchor(s) |
| SQLR | SQL_KEYS | -> | depends_on | payload | 1 anchor(s) |
| SSE | DONE | [yes] | depends_on |  | 1 anchor(s) |
| SSE | EV | [yes] | depends_on |  |  |
| SSE | JSON | [no] | depends_on |  | 1 anchor(s) |
| TCE | TCE_KEYS | -> | depends_on | payload |  |
| TCS | TCS_KEYS | -> | depends_on | payload |  |

## Notes

### 运维 HTTP 入口

- `/api/py/live` — health live
- `/api/py/ready` — readiness

### Debug 开关

`DEBUG_RAG`、`RAG_DEBUG`、`NODE_ENV`、`DEBUG_INGEST`、`DEBUG_INTENT_CACHE`、`DEBUG_AGENT_DB_LOG`、`DEBUG_ROUTER_EVIDENCE`、`DEBUG_ROUTER_EVIDENCE_DB`、`DEBUG_ROUTER_TRACE_DB`

### 说明

本图为运行/排障视角，不重复 RAG/Text2SQL/FTS 业务主链路；详细事件契约见 `_contract_manifest.json`。


