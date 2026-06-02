```mermaid
flowchart TD
  %% Runtime / Observability（人类友好版，最小同步）

  SSE[/SSE: /api/py/unified/chat/stream/] -->|chain| EV[events]
  SSE -->|done| DONE[done]

  EV -->|router.decision| R[route]
  EV -->|tool.call.start/end| T[tool calls]
  EV -->|rag.sources| S[sources]
  EV -->|sql.result| Q[sql result]
  EV -->|error| E[error]

  T --> LOG[(rag_conversation_logs)]

  LIVE[/api/py/live] --> LIVE_OK[health live]
  RDY[/api/py/ready] --> RDY_OK[readiness]
```

**运维 HTTP 入口（drift_check 字面量）**：`/api/py/live` · `/api/py/ready`

**Debug 开关字面量（drift_check）**：`DEBUG_RAG` `RAG_DEBUG` `NODE_ENV` `DEBUG_INGEST` `DEBUG_INTENT_CACHE` `DEBUG_AGENT_DB_LOG` `DEBUG_ROUTER_EVIDENCE` `DEBUG_ROUTER_EVIDENCE_DB` `DEBUG_ROUTER_TRACE_DB`

