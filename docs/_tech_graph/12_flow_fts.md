```mermaid
flowchart TD
  %% FTS is implemented by tsvector('simple', content + alias) + websearch_to_tsquery

  W[Write/Update content] --> TRG[trigger: documents_fts_tokens_update]
  TRG --> ALIAS[rag_fts_alias_text(content)<br/>B2 v1/v2]
  ALIAS --> TSV[fts_tokens := to_tsvector('simple', content + alias)]
  TSV --> IDX[GIN index: documents_fts_tokens_gin]

  Q[Query Text] --> QS[keyword_query_text()<br/>query-side normalize/expand]
  QS --> RPC[RPC keyword_documents(query_text)]
  RPC --> TSQ[websearch_to_tsquery('simple', query_text)]
  TSQ --> MATCH[fts_tokens @@ tsquery]
  MATCH --> RANK[ts_rank_cd score]
  RANK --> OUT[TopK hits]

  %% variant coverage
  subgraph B2_IndexSide["B2 (Index-side alias)"]
    ALIAS
  end
  subgraph B2_QuerySide["B2.1 (Query-side expand)"]
    QS
  end
```

