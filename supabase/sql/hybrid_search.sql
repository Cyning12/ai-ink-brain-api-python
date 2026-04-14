-- =============================================================================
-- AI-Ink-Brain · Hybrid Search（FTS + Vector）增量迁移
-- 用法：Supabase Dashboard → SQL Editor → 执行本文件
--
-- 目标：
-- - 为 public.documents 增加 fts_tokens tsvector + GIN 索引
-- - 用触发器保证 content 写入/更新时自动维护 fts_tokens
-- - 提供 keyword 检索 RPC：keyword_documents
-- - 提供 ingest 后刷新 RPC：refresh_documents_fts_tokens_for_paths
--
-- 说明：
-- - 默认使用 to_tsvector('simple', content)（更通用，适配中英文混合）。
--   若你已安装中文分词扩展（如 zhparser），可自行替换配置。
-- =============================================================================

-- 1) 增加 tsvector 列
alter table public.documents
  add column if not exists fts_tokens tsvector;

-- 2) GIN 索引（提升 @@ 查询性能）
create index if not exists documents_fts_tokens_gin
  on public.documents using gin (fts_tokens);

-- 3) 触发器：自动维护 fts_tokens
create or replace function public.documents_fts_tokens_update()
returns trigger
language plpgsql
as $$
begin
  new.fts_tokens := to_tsvector('simple', coalesce(new.content, ''));
  return new;
end;
$$;

drop trigger if exists trg_documents_fts_tokens_update on public.documents;
create trigger trg_documents_fts_tokens_update
before insert or update of content
on public.documents
for each row
execute function public.documents_fts_tokens_update();

-- 4) 回填历史数据（只更新空值，避免无意义全表写）
update public.documents
set fts_tokens = to_tsvector('simple', coalesce(content, ''))
where fts_tokens is null;

-- 5) RPC：Keyword 路（全文检索）
-- - query_text 为空时返回空集合
-- - 返回字段结构尽量对齐 match_documents，便于后端合并
create or replace function public.keyword_documents(
  query_text text,
  match_count integer default 10
)
returns table (
  id bigint,
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
  from public.documents d
  where
    query_text is not null
    and btrim(query_text) <> ''
    and d.fts_tokens @@ websearch_to_tsquery('simple', query_text)
  order by score desc, d.id asc
  limit greatest(match_count, 1);
$$;

grant execute on function public.keyword_documents(text, integer) to service_role;

-- 6) RPC：按 relativePath 刷新 fts_tokens（供 ingest 兜底调用）
create or replace function public.refresh_documents_fts_tokens_for_paths(
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

  update public.documents d
  set fts_tokens = to_tsvector('simple', coalesce(d.content, ''))
  where (d.metadata ->> 'relativePath') = any(relative_paths);

  get diagnostics updated_count = row_count;
  return updated_count;
end;
$$;

grant execute on function public.refresh_documents_fts_tokens_for_paths(text[]) to service_role;

