```mermaid
flowchart TD
    %% version: 2026-04-24 (main)

    %% 入口
    Q[用户请求<br/>HTTP API] --> E{入口路由<br/>api/index.py#L434}

    %% 主业务分支
    E -->|Unified Chat| U1[JSON 响应<br/>/api/py/unified/chat<br/>api/index.py#L561 unified_chat_route<br/>api/unified_chat.py::handle_unified_chat]
    E -->|Unified Stream| U2[SSE 流式<br/>/api/py/unified/chat/stream<br/>api/index.py#L576 unified_chat_stream_route<br/>api/unified_chat.py::handle_unified_chat_stream]
    E -->|遗留 Chat| C1[RAG Chat<br/>/api/py/chat<br/>api/index.py#L591 chat]
    E -->|History| H1[Chat History<br/>/api/py/chat/history<br/>api/index.py#L439 chat_history]
    E -->|Health| HL[Health<br/>/api/py/health<br/>api/index.py#L434 health]
    E -->|Chain Chat| CH[Chain Timeline<br/>/api/py/chain/chat<br/>api/index.py#L546 chain_chat_route<br/>api/chain_chat.py::handle_chain_chat]

    %% 数据与代码分支
    E -->|Code Query| CR1[代码检索<br/>/api/py/code/query<br/>api/index.py#L501 code_query<br/>api/code_retrieval.py::handle_code_query]
    E -->|Code Search| CR2[代码搜索<br/>/api/py/code/search<br/>api/index.py#L516 code_search<br/>api/code_retrieval.py::handle_code_search]
    E -->|数据同步| A1[Sync Ingest<br/>/api/py/admin/sync<br/>api/index.py#L983 admin_sync<br/>api/ingest_pipeline.py::run_sync_job_sync]
    E -->|数据写入| A2[Ingest<br/>/api/py/admin/ingest<br/>api/index.py#L1026 admin_ingest<br/>api/ingest_pipeline.py::process_markdown_files]

    %% 核心子流程
    U1 --> RAG[RAG 检索流程]
    U2 --> RAG
    C1 --> RAG

    U1 --> T2S[Text2SQL 流程]
    U2 --> T2S

    CR1 --> RPC[Supabase RPC 调用]
    CR2 --> RPC
    A1 --> RPC
    A2 --> RPC

    %% 共享依赖
    RAG --> FTS[FTS 全文检索]
    FTS --> RPC
    T2S --> RPC

    %% 样式
    classDef start fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef main fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef infra fill:#fff8e1,stroke:#ff6f00,stroke-width:1px

    class Q,E start
    class U1,U2,C1,CR1,CR2,A1,A2 main
    class RAG,T2S,RPC,FTS infra
```

- `Struct`：[`01_struct.md`](01_struct.md)
- `Version`：[`02_version.md`](02_version.md)
- `RAG Flow`：[`10_flow_rag.md`](10_flow_rag.md)（[AI 协议版](10_flow_rag.ai.md)）
- `Text2SQL Flow`：[`11_flow_text2sql.md`](11_flow_text2sql.md)（[AI 协议版](11_flow_text2sql.ai.md)）
- `FTS Flow`：[`12_flow_fts.md`](12_flow_fts.md)（[AI 协议版](12_flow_fts.ai.md)）
- `Supabase RPC`：[`13_flow_supabase_rpc.md`](13_flow_supabase_rpc.md)（[AI 协议版](13_flow_supabase_rpc.ai.md)）
- `Spec`：[`99_spec.md`](99_spec.md)
- `Mermaid Protocol`：[`99_mermaid_protocol.md`](99_mermaid_protocol.md) — 拓扑图绘制规范（Python/FastAPI 适配版）
