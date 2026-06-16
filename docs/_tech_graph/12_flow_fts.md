---
graph_id: 12_flow_fts
version: 2026-06-16
generated_at: 2026-06-16T12:08:13Z
source: docs/_tech_graph/12_flow_fts.graph.yaml
---

# FTS 子流程

全文检索写入/更新触发、tsvector 生成、GIN 索引、查询召回与 I18N 扩展流程

## Mermaid

```mermaid
flowchart TD
    ALIAS[rag_fts_alias_text()]
    CLEAN[candidate clean & limits]
    FTS_NULL[fts_tokens is null?]
    GLOSS[data/i18n_glossary.json]
    I18N[I18N_EXPAND_ENABLED?]
    IDX[(GIN: documents_fts_tokens_gin)]
    MATCH[fts_tokens @@ tsquery]
    NOX[graceful fallback]
    ORQ[OR compose]
    QS[keyword_query_text()]
    RANK[ts_rank_cd score]
    REFRESH[refresh_documents_fts_tokens_for_paths()]
    TRG[trigger: documents_fts_tokens_update]
    TSQ[websearch_to_tsquery('simple', query_text)]
    TSV[to_tsvector('simple', content + alias)]
    W[Write/Update content]

    ALIAS --> TSV
    CLEAN --> ORQ
    FTS_NULL --"[no]"--> RANK
    FTS_NULL --"[yes]"--> REFRESH
    // → supabase/sql/hybrid_search.sql::refresh_documents_fts_tokens_for_paths
    GLOSS --> CLEAN
    I18N --"[on & mode=glossary]"--> GLOSS
    I18N --"[off / err]"--> NOX
    MATCH --"fts_tokens is null ?>"--> FTS_NULL
    MATCH --> RANK
    NOX --> RPC
    ORQ --> RPC
    Q --> QS
    // → api/rag_recall_tools.py
    QS --"?>"--> I18N
    // → api/rag_recall_tools.py
    QS --> RPC
    // → api/rag_recall_tools.py::keyword_query_text_with_i18n_meta
    // → api/index.py::fetch_keyword_hits
    // → api/unified_chat.py::rpc_execute_with_retry
    RANK --> OUT
    REFRESH --> RPC
    RPC --"~>"--> TSQ
    // → supabase/sql/hybrid_search.sql::keyword_documents
    TRG --> ALIAS
    // → supabase/sql/hybrid_search.sql::rag_fts_alias_text
    TSQ --> MATCH
    TSV --> IDX
    // → supabase/sql/hybrid_search.sql#L16
    W --"::triggers"--> TRG
    // → supabase/sql/hybrid_search.sql::documents_fts_tokens_update

    classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef doc fill:#fff8e1,stroke:#ff6f00,stroke-width:1px
    classDef infra fill:#e8f5e9,stroke:#2e7d32,stroke-width:1px
```

## Structured Data

### Nodes

| ID | Label | Kind |
|----|-------|------|
| ALIAS | rag_fts_alias_text() |  |
| CLEAN | candidate clean & limits |  |
| FTS_NULL | fts_tokens is null? |  |
| GLOSS | data/i18n_glossary.json |  |
| I18N | I18N_EXPAND_ENABLED? |  |
| IDX | (GIN: documents_fts_tokens_gin) |  |
| MATCH | fts_tokens @@ tsquery |  |
| NOX | graceful fallback |  |
| ORQ | OR compose |  |
| QS | keyword_query_text() |  |
| RANK | ts_rank_cd score |  |
| REFRESH | refresh_documents_fts_tokens_for_paths() |  |
| TRG | trigger: documents_fts_tokens_update |  |
| TSQ | websearch_to_tsquery('simple', query_text) |  |
| TSV | to_tsvector('simple', content + alias) |  |
| W | Write/Update content |  |

### Edges

| From | To | Mark | Type | Label | Anchors |
|------|----|------|------|-------|---------|
| ALIAS | TSV | -> | depends_on |  |  |
| CLEAN | ORQ | -> | depends_on |  |  |
| FTS_NULL | RANK | [no] | depends_on |  |  |
| FTS_NULL | REFRESH | [yes] | depends_on |  | 1 anchor(s) |
| GLOSS | CLEAN | -> | depends_on |  |  |
| I18N | GLOSS | [on & mode=glossary] | depends_on |  |  |
| I18N | NOX | [off / err] | depends_on |  |  |
| MATCH | FTS_NULL | -> | condition | fts_tokens is null ?> |  |
| MATCH | RANK | -> | depends_on |  |  |
| NOX | RPC | -> | depends_on |  |  |
| ORQ | RPC | -> | depends_on |  |  |
| Q | QS | -> | depends_on |  | 1 anchor(s) |
| QS | I18N | ?> | condition |  | 1 anchor(s) |
| QS | RPC | -> | depends_on |  | 3 anchor(s) |
| RANK | OUT | -> | depends_on |  |  |
| REFRESH | RPC | -> | depends_on |  |  |
| RPC | TSQ | ~> | async_calls |  | 1 anchor(s) |
| TRG | ALIAS | -> | depends_on |  | 1 anchor(s) |
| TSQ | MATCH | -> | depends_on |  |  |
| TSV | IDX | -> | depends_on |  | 1 anchor(s) |
| W | TRG | ::triggers | triggers |  | 1 anchor(s) |

## Notes

### B2 变体覆盖

- **B2 索引侧别名**：`ALIAS` 节点在写入流通过 `rag_fts_alias_text()` 生成索引别名。
- **B2.1 查询侧扩展**：`QS` 节点在查询流根据配置做 keyword expand / i18n 扩展。

### 关键文件

- SQL 定义：`supabase/sql/hybrid_search.sql`（trigger / tsvector / GIN / `keyword_documents` RPC）
- Python 入口：`api/rag_recall_tools.py::keyword_query_text_with_i18n_meta`


