-- 已有旧版 match_documents(vector, integer) 时，在 SQL Editor 单独执行本段以升级（无需重建整张表）。
-- 新项目请直接用 init.sql 全文。

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

grant execute on function public.match_documents(vector, integer, double precision) to service_role;
