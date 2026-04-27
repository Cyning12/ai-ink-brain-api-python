```mermaid
flowchart TD
  %% FTS: tsvector('simple', content + alias) + websearch_to_tsquery
  %% 拓扑协议 v2-Python 适配

  %% === 写入/更新流 ===
  W[[Write/Update content]] --"::triggers"--> TRG[[trigger: documents_fts_tokens_update]]
  // → supabase/sql/hybrid_search.sql::documents_fts_tokens_update

  TRG --"->"--> ALIAS[[rag_fts_alias_text()]]
  // → supabase/sql/hybrid_search.sql::rag_fts_alias_text

  ALIAS --"->"--> TSV[[to_tsvector('simple', content + alias)]]
  TSV --"->"--> IDX[(GIN: documents_fts_tokens_gin)]
  // → supabase/sql/hybrid_search.sql#L16

  %% === 查询流 ===
  Q[[Query Text]] --"->"--> QS[[keyword_query_text()]]
  // → api/rag_recall_tools.py

  QS --"->"--> RPC[[RPC keyword_documents()]]
  // → api/rag_recall_tools.py::keyword_query_text_with_i18n_meta
  // → api/index.py::fetch_keyword_hits
  // → api/unified_chat.py::rpc_execute_with_retry

  RPC --"~>"--> TSQ[[websearch_to_tsquery('simple', query_text)]]
  // → supabase/sql/hybrid_search.sql::keyword_documents

  TSQ --"->"--> MATCH[[fts_tokens @@ tsquery]]
  MATCH --"->"--> RANK[[ts_rank_cd score]]
  RANK --"->"--> OUT[[TopK hits]]

  %% === B2 变体覆盖 ===
  subgraph B2_IndexSide["B2 (Index-side alias)"]
    ALIAS
  end

  subgraph B2_QuerySide["B2.1 (Query-side expand)"]
    QS
  end

  %% === 兜底：fts_tokens 为空/未迁移 ===
  MATCH --"fts_tokens is null ?>"--> FTS_NULL{fts_tokens is null?}
  FTS_NULL --"[yes]"--> REFRESH[[refresh_documents_fts_tokens_for_paths()]]
  // → supabase/sql/hybrid_search.sql::refresh_documents_fts_tokens_for_paths
  REFRESH --"->"--> RPC
  FTS_NULL --"[no]"--> RANK

  %% === I18N 跨语言召回 ===
  QS --"?>"--> I18N{I18N_EXPAND_ENABLED?}
  // → api/rag_recall_tools.py

  I18N --"[on & mode=glossary]"--> GLOSS[[data/i18n_glossary.json]]
  I18N --"[off / err]"--> NOX[[graceful fallback]]

  GLOSS --"->"--> CLEAN[[candidate clean & limits]]
  CLEAN --"->"--> ORQ[[OR compose]]
  ORQ --"->"--> RPC

  NOX --"->"--> RPC

  %% === 样式 ===
  classDef phase fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
  classDef fn fill:#f3e5f5,stroke:#4a148c,stroke-width:1px;
  classDef data fill:#e8f5e9,stroke:#1b5e20,stroke-width:1px;
  classDef fallback fill:#fff3e0,stroke:#ef6c00,stroke-width:1px;

  class W,Q,TRG,QS,RPC,TSQ,MATCH,RANK,OUT phase
  class ALIAS,ORQ,CLEAN,NOX fn
  class IDX data
  class GLOSS data
  class NOX fallback
```
