-- =============================================================================
-- AI-Ink-Brain · Supabase 初始化（pgvector + documents + match_documents）
-- 用法：Supabase Dashboard → SQL Editor → 粘贴整段执行（新项目或空库）。
-- =============================================================================
-- 重要：vector(1024) 须与 Next 侧 EMBEDDING_DIM（及所选厂商模型）一致，如 BGE-M3、百炼 text-embedding-v3@1024。
--       若使用其他维度，请全文将 1024 改为 N，并删除旧表/索引/函数后重建，且全量重灌向量。
-- =============================================================================

-- -----------------------------------------------------------------------------
-- 1) 向量扩展（Supabase 默认装在 extensions schema，search_path 通常已包含）
-- -----------------------------------------------------------------------------
create extension if not exists vector;

-- -----------------------------------------------------------------------------
-- 2) 表：RAG 文档分块（Dense Vector + 可引用元数据）
-- -----------------------------------------------------------------------------
create table if not exists public.documents (
  id bigserial primary key,
  content text not null,
  -- 建议键：filename, original_link, page_number, section_header, chunk_index
  metadata jsonb not null default '{}'::jsonb,
  embedding vector(1024) not null,
  created_at timestamptz not null default now()
);

comment on table public.documents is 'RAG 文本分块：正文 + 元数据（引用）+ Embedding';
comment on column public.documents.metadata is 'JSON：filename, original_link, page_number, section_header, chunk_index 等';

-- 语义检索：余弦距离（与 <=> 及 vector_cosine_ops 一致）
-- 数据量较小时可暂缓；大量数据时强烈建议保留
create index if not exists documents_embedding_hnsw
  on public.documents
  using hnsw (embedding vector_cosine_ops);

-- 按文件名等过滤时可用（可选）
create index if not exists documents_metadata_filename
  on public.documents ((metadata ->> 'filename'));

-- -----------------------------------------------------------------------------
-- 3) RLS：不面向 anon 开放；Next.js 仅用 SUPABASE_SERVICE_ROLE_KEY 可绕过 RLS
-- -----------------------------------------------------------------------------
alter table public.documents enable row level security;

-- -----------------------------------------------------------------------------
-- 4) RPC：Cosine Distance Top-k（similarity ≈ 1 - cosine_distance）
--    match_threshold 为 null 时不做阈值过滤（兼容仅传 query_embedding + match_count 的调用）。
-- -----------------------------------------------------------------------------
drop function if exists public.match_documents(vector, integer);

create or replace function public.match_documents(
  query_embedding vector(1024),
  match_count integer default 5,
  match_threshold double precision default null
)
returns table (
  id bigint,
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
  from public.documents d
  where
    match_threshold is null
    or (1 - (d.embedding <=> query_embedding))::double precision > match_threshold
  order by d.embedding <=> query_embedding
  limit greatest(match_count, 1);
$$;

-- -----------------------------------------------------------------------------
-- 5) 权限：供服务端 service_role 写入与 RPC
-- -----------------------------------------------------------------------------
grant select, insert, update, delete on table public.documents to service_role;
grant usage, select on sequence public.documents_id_seq to service_role;
grant execute on function public.match_documents(vector, integer, double precision) to service_role;

-- -----------------------------------------------------------------------------
-- 附：若 HNSW 不可用（旧 pgvector），删除 documents_embedding_hnsw 后改用 ivfflat：
-- create index documents_embedding_ivfflat on public.documents
--   using ivfflat (embedding vector_cosine_ops) with (lists = 100);
-- （lists 与数据量相关；数据很少时可暂不建向量索引）
-- -----------------------------------------------------------------------------
