-- =============================================================================
-- AI-Ink-Brain · Code RAG（code_chunks + Hybrid Search）
-- 用法：Supabase Dashboard → SQL Editor → 粘贴整段执行（增量迁移）
-- =============================================================================
-- 说明：
-- - 与 Markdown documents 分离：独立表 public.code_chunks
-- - embedding 维度默认 1024，须与 EMBEDDING_DIM / SiliconFlow 模型输出一致
-- =============================================================================

create extension if not exists vector;

create table if not exists public.code_chunks (
  id uuid primary key default gen_random_uuid(),
  content text not null,
  metadata jsonb not null default '{}'::jsonb,
  embedding vector(1024) not null,
  fts_tokens tsvector,
  created_at timestamptz not null default now()
);

comment on table public.code_chunks is '代码语义检索分块：正文 + 元数据 + Embedding';

create index if not exists code_chunks_embedding_hnsw
  on public.code_chunks
  using hnsw (embedding vector_cosine_ops);

create index if not exists code_chunks_metadata_filename
  on public.code_chunks ((metadata ->> 'filename'));

create index if not exists code_chunks_fts_tokens_gin
  on public.code_chunks using gin (fts_tokens);

-- FTS 触发器：自动维护 fts_tokens
create or replace function public.code_chunks_fts_tokens_update()
returns trigger
language plpgsql
as $$
begin
  new.fts_tokens := to_tsvector('simple', coalesce(new.content, ''));
  return new;
end;
$$;

drop trigger if exists trg_code_chunks_fts_tokens_update on public.code_chunks;
create trigger trg_code_chunks_fts_tokens_update
before insert or update of content
on public.code_chunks
for each row
execute function public.code_chunks_fts_tokens_update();

-- 回填历史数据（仅更新空值）
update public.code_chunks
set fts_tokens = to_tsvector('simple', coalesce(content, ''))
where fts_tokens is null;

-- Vector RPC：Cosine Distance Top-k（similarity ≈ 1 - cosine_distance）
drop function if exists public.match_code_chunks(vector, integer, double precision);

create or replace function public.match_code_chunks(
  query_embedding vector(1024),
  match_count integer default 10,
  match_threshold double precision default null
)
returns table (
  id uuid,
  content text,
  metadata jsonb,
  similarity double precision
)
language sql
stable
parallel safe
as $$
  select
    d.id,
    d.content,
    d.metadata,
    (1 - (d.embedding <=> query_embedding))::double precision as similarity
  from public.code_chunks d
  where
    match_threshold is null
    or (1 - (d.embedding <=> query_embedding))::double precision > match_threshold
  order by d.embedding <=> query_embedding
  limit greatest(match_count, 1);
$$;

-- Keyword RPC：FTS
create or replace function public.keyword_code_chunks(
  query_text text,
  match_count integer default 10
)
returns table (
  id uuid,
  content text,
  metadata jsonb,
  score double precision
)
language sql
stable
parallel safe
as $$
  select
    d.id,
    d.content,
    d.metadata,
    ts_rank_cd(d.fts_tokens, websearch_to_tsquery('simple', query_text))::double precision as score
  from public.code_chunks d
  where
    query_text is not null
    and btrim(query_text) <> ''
    and d.fts_tokens @@ websearch_to_tsquery('simple', query_text)
  order by score desc, d.id asc
  limit greatest(match_count, 1);
$$;

-- ingest 后刷新 fts_tokens（兜底）
create or replace function public.refresh_code_chunks_fts_tokens_for_paths(
  relative_paths text[]
)
returns integer
language plpgsql
as $$
declare
  updated_count integer := 0;
begin
  if relative_paths is null or array_length(relative_paths, 1) is null then
    return 0;
  end if;

  update public.code_chunks d
  set fts_tokens = to_tsvector('simple', coalesce(d.content, ''))
  where (d.metadata ->> 'relativePath') = any(relative_paths);

  get diagnostics updated_count = row_count;
  return updated_count;
end;
$$;

-- 权限：service_role
grant select, insert, update, delete on table public.code_chunks to service_role;
grant execute on function public.match_code_chunks(vector, integer, double precision) to service_role;
grant execute on function public.keyword_code_chunks(text, integer) to service_role;
grant execute on function public.refresh_code_chunks_fts_tokens_for_paths(text[]) to service_role;
