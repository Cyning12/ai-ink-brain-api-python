```mermaid
classDiagram
  %% DB Struct (from supabase/sql/*.sql + code usage)

  class documents {
    +bigserial id
    +text content
    +jsonb metadata
    +vector(1024) embedding
    +tsvector fts_tokens  %% vFTS (hybrid_search.sql)
    +timestamptz created_at
  }

  class code_chunks {
    +uuid id
    +text content
    +jsonb metadata
    +vector(1024) embedding
    +tsvector fts_tokens
    +timestamptz created_at
  }

  class rag_conversation_logs {
    +uuid id
    +varchar session_id
    +text query
    +text rewritten_query
    +jsonb retrieved_context
    +text response
    +jsonb metadata
    +timestamptz created_at
  }

  class FileMeta {
    +string category (req)
    +string slug (req)
    +string filename (req)
    +string relativePath (req)
    +int chunk_index (req)
    +string mtime (req)
    +string lastModified (req)
    +string date_norm (opt) %% B1 write-side（可从 slug/filename 抽取）
    +string slug_norm (opt) %% B1 write-side（可从 slug 抽取）
    +string original_link (opt)
    +string section_header (opt)
    +int page_number (opt)
    +string file_path (opt) %% code_chunks 扩展
    +int start_line (opt) %% code_chunks 扩展
    +int end_line (opt) %% code_chunks 扩展
    +string chunk_type (opt) %% code_chunks 扩展
    +string name (opt) %% code_chunks 扩展
    +string signature (opt) %% code_chunks 扩展
    +string module (opt) %% code_chunks 扩展
  }

  documents --> FileMeta : metadata
  code_chunks --> FileMeta : metadata
```

