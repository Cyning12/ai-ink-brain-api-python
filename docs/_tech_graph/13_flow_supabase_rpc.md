```mermaid
flowchart LR
  %% Supabase RPC + Tables (service_role)

  SB[Supabase Client<br/>service_role] --> D[table: public.documents]
  SB --> C[table: public.code_chunks]
  SB --> L[table: public.rag_conversation_logs]

  %% documents rpc
  SB --> MD[rpc: match_documents(query_embedding, match_count, match_threshold)]
  SB --> KD[rpc: keyword_documents(query_text, match_count)]
  SB --> RD[rpc: refresh_documents_fts_tokens_for_paths(relative_paths)]

  %% code_chunks rpc
  SB --> MC[rpc: match_code_chunks(query_embedding, match_count, match_threshold)]
  SB --> KC[rpc: keyword_code_chunks(query_text, match_count)]
  SB --> RC[rpc: refresh_code_chunks_fts_tokens_for_paths(relative_paths)]

  %% ingestion writes
  ING[Ingest Pipeline] -->|insert| D
  ING -->|insert| C
  ING -->|refresh fts| RD
  ING -->|refresh fts| RC

  %% debug logs
  CHAT[RAG/Unified Chat] -->|insert| L
  CHAT -->|select history| L
```

