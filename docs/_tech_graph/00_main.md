---
graph_id: 00_main
version: 2026-06-16
generated_at: 2026-06-22T07:47:58Z
source: docs/_tech_graph/00_main.graph.yaml
---

# 主路由图

API 入口分发与子流程路由

## Mermaid

```mermaid
flowchart TD
    Q[[用户请求]]
    E[["@router.dispatch"]]
    U1[Unified JSON]
    U2[Unified SSE]
    C1[RAG Chat]
    CH[Chain Timeline]
    CR1[Code Query]
    CR2[Code Search]
    CV[ChatBI Access Verify]
    H1[Chat History]
    HL[Health]
    SQ[Suggested Questions]
    A1[Sync Ingest]
    A2[Ingest]
    RAG[[RAG 子流程]]
    T2S[[Text2SQL 子流程]]
    RPC[[Supabase RPC 子流程]]
    FTS[[FTS 子流程]]
    AUTH[AUTH]
    EV_TYPES[EV_TYPES]
    RAG_DOC[>10_flow_rag.md]
    T2S_DOC[>11_flow_text2sql.md]
    FTS_DOC[>12_flow_fts.md]
    RPC_DOC[>13_flow_supabase_rpc.md]
    OBS_DOC[>14_runtime_observability.md]
    E2E_DOC[>15_e2e_boundary.md]
    OPS_CHAT[Ops Chat (P1)]
    OPS_CHAT_DOC[>16_flow_ops_chat.md]

    Q --> E
    // → api/index.py#L434
    E --"POST /api/py/unified/chat"--> U1
    E --"POST /api/py/unified/chat/stream"--> U2
    E --"POST /api/py/chat"--> C1
    E --"POST /api/py/chain/chat"--> CH
    E --"POST /api/py/code/query"--> CR1
    E --"POST /api/py/code/search"--> CR2
    E --"GET /api/py/chatbi/access/verify"--> CV
    E --"GET /api/py/chat/history"--> H1
    E --"GET /api/py/health"--> HL
    E --"GET /api/py/chat/suggested-questions"--> SQ
    E --"POST /api/py/admin/sync"--> A1
    E --"POST /api/py/admin/ingest"--> A2
    E --"加载"--> OBS_DOC
    E --"加载"--> E2E_DOC
    E --"POST /ops/chat/messages (P1)"--> OPS_CHAT
    E --"加载"--> OPS_CHAT_DOC
    OPS_CHAT --"加载"--> OPS_CHAT_DOC
    U1 --"::branches"--> RAG
    U1 --"::branches"--> T2S
    U1 --> U2
    U1 --> AUTH
    // → api/chatbi_principal.py::require_chatbi_principal
    U2 --"::branches"--> RAG
    U2 --"::branches"--> T2S
    U2 --> U1
    U2 --> AUTH
    // → api/chatbi_principal.py::require_chatbi_principal
    U2 --> EV_TYPES
    // → api/unified_chat.py::_event
    C1 --> RAG
    CR1 --> RPC
    CR2 --> RPC
    A1 --> RPC
    A2 --> RPC
    RAG --> FTS
    RAG --"加载"--> RAG_DOC
    T2S --> RPC
    T2S --"加载"--> T2S_DOC
    FTS --> RPC
    FTS --"加载"--> FTS_DOC
    RPC --"加载"--> RPC_DOC

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
    class Q,E,U1,U2,RAG,T2S,RPC,FTS phase
    class RAG_DOC,T2S_DOC,FTS_DOC,RPC_DOC,OBS_DOC,E2E_DOC,OPS_CHAT_DOC doc
    class AUTH,EV_TYPES infra
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| Q | 用户请求 |  |
| E | "@router.dispatch" |  |
| U1 | Unified JSON |  |
| U2 | Unified SSE |  |
| C1 | RAG Chat |  |
| CH | Chain Timeline |  |
| CR1 | Code Query |  |
| CR2 | Code Search |  |
| CV | ChatBI Access Verify |  |
| H1 | Chat History |  |
| HL | Health |  |
| SQ | Suggested Questions |  |
| A1 | Sync Ingest |  |
| A2 | Ingest |  |
| RAG | RAG 子流程 |  |
| T2S | Text2SQL 子流程 |  |
| RPC | Supabase RPC 子流程 |  |
| FTS | FTS 子流程 |  |
| AUTH | AUTH |  |
| EV_TYPES | EV_TYPES |  |
| RAG_DOC | >10_flow_rag.md |  |
| T2S_DOC | >11_flow_text2sql.md |  |
| FTS_DOC | >12_flow_fts.md |  |
| RPC_DOC | >13_flow_supabase_rpc.md |  |
| OBS_DOC | >14_runtime_observability.md |  |
| E2E_DOC | >15_e2e_boundary.md |  |
| OPS_CHAT | Ops Chat (P1) |  |
| OPS_CHAT_DOC | >16_flow_ops_chat.md |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| Q | E | -> | depends_on |  | 1 anchor(s) |
| E | U1 | -> | depends_on | POST /api/py/unified/chat |  |
| E | U2 | -> | depends_on | POST /api/py/unified/chat/stream |  |
| E | C1 | -> | depends_on | POST /api/py/chat |  |
| E | CH | -> | depends_on | POST /api/py/chain/chat |  |
| E | CR1 | -> | depends_on | POST /api/py/code/query |  |
| E | CR2 | -> | depends_on | POST /api/py/code/search |  |
| E | CV | -> | depends_on | GET /api/py/chatbi/access/verify |  |
| E | H1 | -> | depends_on | GET /api/py/chat/history |  |
| E | HL | -> | depends_on | GET /api/py/health |  |
| E | SQ | -> | depends_on | GET /api/py/chat/suggested-questions |  |
| E | A1 | -> | depends_on | POST /api/py/admin/sync |  |
| E | A2 | -> | depends_on | POST /api/py/admin/ingest |  |
| E | OBS_DOC | -> | depends_on | 加载 |  |
| E | E2E_DOC | -> | depends_on | 加载 |  |
| E | OPS_CHAT | -> | depends_on | POST /ops/chat/messages (P1) |  |
| E | OPS_CHAT_DOC | -> | depends_on | 加载 |  |
| OPS_CHAT | OPS_CHAT_DOC | -> | depends_on | 加载 |  |
| U1 | RAG | ::branches | branches |  |  |
| U1 | T2S | ::branches | branches |  |  |
| U1 | U2 | -> | depends_on |  |  |
| U1 | AUTH | -> | depends_on |  | 1 anchor(s) |
| U2 | RAG | ::branches | branches |  |  |
| U2 | T2S | ::branches | branches |  |  |
| U2 | U1 | -> | depends_on |  |  |
| U2 | AUTH | -> | depends_on |  | 1 anchor(s) |
| U2 | EV_TYPES | -> | depends_on |  | 1 anchor(s) |
| C1 | RAG | -> | depends_on |  |  |
| CR1 | RPC | -> | depends_on |  |  |
| CR2 | RPC | -> | depends_on |  |  |
| A1 | RPC | -> | depends_on |  |  |
| A2 | RPC | -> | depends_on |  |  |
| RAG | FTS | -> | depends_on |  |  |
| RAG | RAG_DOC | -> | depends_on | 加载 |  |
| T2S | RPC | -> | depends_on |  |  |
| T2S | T2S_DOC | -> | depends_on | 加载 |  |
| FTS | RPC | -> | depends_on |  |  |
| FTS | FTS_DOC | -> | depends_on | 加载 |  |
| RPC | RPC_DOC | -> | depends_on | 加载 |  |

## Sub-graph Links

- `Struct`: [`01_struct.md`](01_struct.md)（手写 · 无 `.graph.yaml`）
- `Version`: [`02_version.md`](02_version.md)（手写 · 无 `.graph.yaml`）
- `RAG Flow`: [`10_flow_rag.md`](10_flow_rag.md)（编辑源：[10_flow_rag.graph.yaml](10_flow_rag.graph.yaml)）
- `Text2SQL Flow`: [`11_flow_text2sql.md`](11_flow_text2sql.md)（编辑源：[11_flow_text2sql.graph.yaml](11_flow_text2sql.graph.yaml)）
- `FTS Flow`: [`12_flow_fts.md`](12_flow_fts.md)（编辑源：[12_flow_fts.graph.yaml](12_flow_fts.graph.yaml)）
- `Supabase RPC`: [`13_flow_supabase_rpc.md`](13_flow_supabase_rpc.md)（编辑源：[13_flow_supabase_rpc.graph.yaml](13_flow_supabase_rpc.graph.yaml)）
- `Runtime/Observability`: [`14_runtime_observability.md`](14_runtime_observability.md)（编辑源：[14_runtime_observability.graph.yaml](14_runtime_observability.graph.yaml)）
- `E2E Boundary/Contract`: [`15_e2e_boundary.md`](15_e2e_boundary.md)（编辑源：[15_e2e_boundary.graph.yaml](15_e2e_boundary.graph.yaml)）
- `Ops Desk Chat`: [`16_flow_ops_chat.md`](16_flow_ops_chat.md)（编辑源：[16_flow_ops_chat.graph.yaml](16_flow_ops_chat.graph.yaml) · P1 规划）
- `Spec`: [`99_spec.md`](99_spec.md)
- `Mermaid Protocol`: [`99_mermaid_protocol.md`](99_mermaid_protocol.md) — 拓扑图绘制规范（Python/FastAPI 适配版）

> **P0 决策备忘**：`00_main.md` 不嵌入 `AUTO:ENDPOINTS_AND_ANCHORS` 块（保持人类友好）；`_manifest.json` 仍由现有工具维护。

