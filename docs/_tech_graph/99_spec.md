```mermaid
flowchart TD
  %% 技术图谱交付规约（本项目落盘版）

  ROOT[docs/_tech_graph/00_main.md<br/>唯一常驻上下文] --> S1[01_struct.md<br/>DB Struct]
  ROOT --> V1[02_version.md<br/>Git 迭代]
  ROOT --> F1[10_flow_rag.md]
  ROOT --> F2[11_flow_text2sql.md]
  ROOT --> F3[12_flow_fts.md]
  ROOT --> F4[13_flow_supabase_rpc.md]
  ROOT --> ENV[Env Truth Table<br/>见下图]
  ROOT --> TODO[Next Steps Backlog<br/>见下图]

  subgraph TruthSource["事实来源（禁止编造）"]
    TS1[api/*.py 真实代码]
    TS2[supabase/sql/*.sql 真实SQL]
    TS3[git log 真实提交历史]
  end

  subgraph Constraints["AI 行为约束（低幻觉）"]
    C1[禁止: 不存在的表/字段/RPC/端点]
    C2[禁止: 在图中粘贴完整 DDL/长 JSON]
    C3[要求: Struct 表达 DB 结构]
    C4[要求: 流程必须用连线对接<br/>不依赖上下文文字]
    C5[要求: 子流程按需加载<br/>00_main 只保留入口/分支]
    C6[要求: 所有 Mermaid 图遵循<br/>99_mermaid_protocol.md 拓扑协议]
  end

  TS1 --> ROOT
  TS2 --> ROOT
  TS3 --> ROOT

  Constraints --> ROOT
```

```mermaid
flowchart TD
  %% Env Truth Table（变量 -> 影响节点）

  subgraph Supabase["Supabase"]
    SURL[NEXT_PUBLIC_SUPABASE_URL / SUPABASE_URL] --> SB[supabase_client()<br/>api/rag_env.py]
    SKEY[SUPABASE_SERVICE_ROLE_KEY / SUPABASE_SERVICE_KEY] --> SB
  end

  subgraph Auth["Auth"]
    AK[API_KEY] --> AUTHU[unified/text2sql/chat auth]
    AS[NEXT_PUBLIC_ADMIN_SECRET / CHAT_API_SECRET] --> AUTHU
  end

  subgraph RAG["RAG"]
    EMBM[SILICONFLOW_EMBEDDING_MODEL] --> EMB[Embedding]
    EMBD[SILICONFLOW_EMBEDDING_DIMENSIONS] --> EMB
    TH[RAG_MATCH_THRESHOLD (0~1 或 none)] --> VEC[match_documents threshold]
    DBG[DEBUG_RAG / RAG_DEBUG / NODE_ENV] --> LOG[rag debug print]
  end

  subgraph LLM["LLM"]
    CK[SILICONFLOW_API_KEY] --> OAI[openai_siliconflow_client / OpenAI]
    CM[SILICONFLOW_CHAT_MODEL] --> OAI
    BASE[SILICONFLOW_BASE_URL] --> OAI
  end

  subgraph Text2SQL["Text2SQL"]
    TDB[TEXT2SQL_DATABASE_URL] --> EX[execute_select_sql]
    TTOPK[TEXT2SQL_RETRIEVE_TOPK] --> RET[text2sql_store.search]
    TROW[TEXT2SQL_MAX_ROWS] --> EX
  end
```

```mermaid
flowchart TD
  %% Next Steps Backlog（优先级 + 验收点 + 影响文件）

  START[接手下一步] --> P0[P0: RAG 召回可靠性回归验证]
  P0 --> A0[验收: 典型问法<br/>date/cn-date/version/identifier<br/>tool.call.end payload 含 hits]
  P0 --> F0[影响: api/unified_chat.py<br/>api/rag_recall_tools.py<br/>supabase/sql/hybrid_search.sql]

  A0 --> P1[P1: Text2SQL flexible match / 路由修正]
  P1 --> A1[验收: 明确表名/字段名/统计词<br/>auto mode 走 text2sql 且 SQL 只读]
  P1 --> F1[影响: api/intent_router.py<br/>api/text2sql_core.py<br/>api/text2sql_store.py]

  A1 --> P2[P2: auto mode 优化（减少误判）]
  P2 --> A2[验收: no_data 不幻觉<br/>RAG/SQL 互不抢占]
  P2 --> F2[影响: api/intent_router.py<br/>api/unified_chat.py]
```

