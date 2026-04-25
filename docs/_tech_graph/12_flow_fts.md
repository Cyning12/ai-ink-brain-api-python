```mermaid
flowchart TD
    %% FTS: tsvector('simple', content + alias) + websearch_to_tsquery

    %% 写入流
    W[写入/更新内容] --> TRG[Trigger 更新<br/>documents_fts_tokens_update]
    TRG --> ALIAS[别名生成<br/>rag_fts_alias_text()]
    ALIAS --> TSV[to_tsvector<br/>content + alias]
    TSV --> IDX[GIN 索引<br/>documents_fts_tokens_gin]

    %% 查询流
    Q[查询文本] --> QS[Query 预处理<br/>normalize / expand]
    QS --> RPC[RPC 调用<br/>keyword_documents()]
    RPC --> TSQ[websearch_to_tsquery]
    TSQ --> MATCH[fts_tokens @@ tsquery]
    MATCH -->|fts_tokens null| REF[refresh_documents_fts_tokens_for_paths]
    REF --> RPC
    MATCH --> RANK[ts_rank_cd 评分]
    RANK --> OUT[TopK 结果]

    %% B2 变体
    subgraph B2_Index["B2 索引侧别名"]
        ALIAS
    end

    subgraph B2_Query["B2.1 查询侧扩展"]
        QS
    end

    %% I18N 跨语言
    QS --> I18N{I18N_EXPAND_ENABLED?}
    I18N -->|glossary| GLOSS[i18n_glossary.json<br/>ZH → EN]
    I18N -->|off / error| NOX[降级回退<br/>raw query only]

    GLOSS --> CLEAN[候选清洗<br/>limit / chars]
    CLEAN --> ORQ[OR 组合<br/>raw OR en1 OR ...]
    ORQ --> RPC

    %% 样式
    classDef write fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef read fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    classDef i18n fill:#fff8e1,stroke:#ff6f00,stroke-width:1px

    class W,TRG,ALIAS,TSV,IDX write
    class Q,QS,RPC,TSQ,MATCH,RANK,OUT read
    class I18N,GLOSS,NOX,CLEAN,ORQ i18n
```
