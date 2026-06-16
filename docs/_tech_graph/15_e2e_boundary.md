---
graph_id: 15_e2e_boundary
version: 2026-06-16
generated_at: 2026-06-16T12:10:04Z
source: docs/_tech_graph/15_e2e_boundary.graph.yaml
---

# E2E Boundary/Contract 子流程

跨仓边界与契约视图：前端 ↔ BFF ↔ Python FastAPI ↔ Supabase，以及 SSE 事件包最小键名

## Mermaid

```mermaid
flowchart TD
    BE[BE]
    BFF[BFF]
    CHAIN_SHAPE[CHAIN_SHAPE]
    CONTENT[CONTENT]
    CONTENT_ROOT[CONTENT_ROOT]
    DONE_SHAPE[DONE_SHAPE]
    FE[FE]
    FE_PARSE[FE_PARSE]
    FE_STREAM[FE_STREAM]
    PY_SSE[PY_SSE]
    RS_KEYS[RS_KEYS]
    SB_MATCH_DOCS[>SB_MATCH_DOCS]
    SB_TRUTH[SB_TRUTH]
    SSE_ENV[SSE_ENV]
    SSE_EVENTS[SSE_EVENTS]

    BE --> SB_TRUTH
    BFF --> PY_SSE
    CONTENT --> CONTENT_ROOT
    CONTENT_ROOT --> BE
    EV_TYPES --> RS_KEYS
    EV_TYPES --> SQL_KEYS
    FE --> FE_STREAM
    FE_STREAM --> BFF
    // → api/index.py::unified_chat_stream_route
    FE_STREAM --"~>"--> FE_PARSE
    PY_SSE --"~>"--> BE
    // → api/unified_chat.py::_sse
    PY_SSE --"::yields"--> SSE_EVENTS
    SB_TRUTH --> SB
    SB_TRUTH --> SB_MATCH_DOCS
    SSE_EVENTS --> CHAIN_SHAPE
    SSE_EVENTS --> DONE_SHAPE
    SSE_EVENTS --> EV_TYPES
    SSE_EVENTS --> SSE_ENV
    // → api/unified_chat.py::_event

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    class SB_MATCH_DOCS doc
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| BE | BE |  |
| BFF | BFF |  |
| CHAIN_SHAPE | CHAIN_SHAPE |  |
| CONTENT | CONTENT |  |
| CONTENT_ROOT | CONTENT_ROOT |  |
| DONE_SHAPE | DONE_SHAPE |  |
| FE | FE |  |
| FE_PARSE | FE_PARSE |  |
| FE_STREAM | FE_STREAM |  |
| PY_SSE | PY_SSE |  |
| RS_KEYS | RS_KEYS |  |
| SB_MATCH_DOCS | SB_MATCH_DOCS |  |
| SB_TRUTH | SB_TRUTH |  |
| SSE_ENV | SSE_ENV |  |
| SSE_EVENTS | SSE_EVENTS |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| BE | SB_TRUTH | -> | depends_on |  |  |
| BFF | PY_SSE | -> | depends_on |  |  |
| CONTENT | CONTENT_ROOT | -> | depends_on |  |  |
| CONTENT_ROOT | BE | -> | depends_on |  |  |
| EV_TYPES | RS_KEYS | -> | depends_on |  |  |
| EV_TYPES | SQL_KEYS | -> | depends_on |  |  |
| FE | FE_STREAM | -> | depends_on |  |  |
| FE_STREAM | BFF | -> | depends_on |  | 1 anchor(s) |
| FE_STREAM | FE_PARSE | ~> | async_calls |  |  |
| PY_SSE | BE | ~> | async_calls |  | 1 anchor(s) |
| PY_SSE | SSE_EVENTS | ::yields | yields |  |  |
| SB_TRUTH | SB | -> | depends_on |  |  |
| SB_TRUTH | SB_MATCH_DOCS | -> | depends_on |  |  |
| SSE_EVENTS | CHAIN_SHAPE | -> | depends_on |  |  |
| SSE_EVENTS | DONE_SHAPE | -> | depends_on |  |  |
| SSE_EVENTS | EV_TYPES | -> | depends_on |  |  |
| SSE_EVENTS | SSE_ENV | -> | depends_on |  | 1 anchor(s) |

## Notes

### 锚点与真值来源

- **后端端点/表/RPC 真值**：`docs/_tech_graph/_manifest.json`
- **SSE 事件集合 + 最小字段键**：`docs/_tech_graph/14_runtime_observability.md`
- **前端 SSE 消费锚点**：`../ai-ink-brain/components/unified-chat/UnifiedChatPageClient.tsx`
- **前端 BFF 透传锚点**：`../ai-ink-brain/app/api/py/unified/chat/stream/route.ts`

### 说明

本图只表达“跨仓边界 + 契约锚点”，不展开前端组件树与后端业务子流程。跨仓契约门禁入口为 `python tools/tech_graph_contract_check.py`，已接入 CI `.github/workflows/tech-graph-contract.yml`。


