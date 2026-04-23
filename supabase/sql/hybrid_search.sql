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

-- 2.1) B2 v2：生成 alias 文本（仅用于 FTS，不改 content/embedding）
-- 目标：
-- - 日期：'2026-4-14' 与 '2026-04-14' 等不同写法都能 @@ 命中
-- - 版本号：v0.1.0 / 0.1.0 / 0-1-0 / 0_1_0
-- - 分隔符：_ - . / \ 归一
-- - 标识符：CamelCase / snake_case 拆分（轻量、受限）
create or replace function public.rag_fts_alias_text(input_text text)
returns text
language plpgsql
immutable
as $$
declare
  s text := coalesce(input_text, '');
  token text;
  m text[];
  y int;
  mo int;
  d int;
  mo2 text;
  d2 text;
  mo1 text;
  d1 text;
  out text := '';
  added int := 0;
  max_added int := 60;
begin
  -- 安全阈值：避免超长文本导致 alias 膨胀
  if length(s) > 200000 then
    s := left(s, 200000);
  end if;

  -- 提取所有日期：YYYY[-/.]M[-/.]D
  for m in
    select regexp_matches(s, '(\d{4})[./-](\d{1,2})[./-](\d{1,2})', 'g')
  loop
    y := m[1]::int;
    mo := greatest(1, least(12, m[2]::int));
    d := greatest(1, least(31, m[3]::int));
    mo2 := lpad(mo::text, 2, '0');
    d2 := lpad(d::text, 2, '0');
    mo1 := mo::text;
    d1 := d::text;

    -- 同时写入补零/不补零 + 分隔符变体 + 空格变体
    out := out
      || ' ' || y::text || '-' || mo2 || '-' || d2
      || ' ' || y::text || '-' || mo1 || '-' || d1
      || ' ' || y::text || '/' || mo2 || '/' || d2
      || ' ' || y::text || '/' || mo1 || '/' || d1
      || ' ' || y::text || '.' || mo2 || '.' || d2
      || ' ' || y::text || '.' || mo1 || '.' || d1
      || ' ' || y::text || ' ' || mo2 || ' ' || d2
      || ' ' || y::text || ' ' || mo1 || ' ' || d1;
    added := added + 8;
    if added >= max_added then
      return btrim(out);
    end if;
  end loop;

  -- 版本号 alias：v0.1.0 / 0.1.0 / 0-1-0 / 0_1_0
  for m in
    select regexp_matches(s, '\bv?(\d+)\.(\d+)(?:\.(\d+))?\b', 'g')
  loop
    out := out
      || ' ' || 'v' || m[1] || '.' || m[2] || '.' || coalesce(m[3], '0')
      || ' ' || m[1] || '.' || m[2] || '.' || coalesce(m[3], '0')
      || ' ' || m[1] || '-' || m[2] || '-' || coalesce(m[3], '0')
      || ' ' || m[1] || '_' || m[2] || '_' || coalesce(m[3], '0');
    added := added + 4;
    if added >= max_added then
      return btrim(out);
    end if;
  end loop;

  -- 分隔符归一：只抽取“看起来像标识符/路径”的 token，避免把整句膨胀
  for token in
    select distinct t from regexp_split_to_table(s, '\s+') as t
    where length(t) between 3 and 64
      and t ~ '[_./\\-]'
      and t ~ '[A-Za-z0-9]'
    limit 40
  loop
    out := out || ' ' || regexp_replace(token, '[_./\\-]+', ' ', 'g');
    added := added + 1;
    if added >= max_added then
      return btrim(out);
    end if;
  end loop;

  -- CamelCase 拆分（轻量）：RunnableWithMessageHistory -> Runnable With Message History
  for token in
    select distinct t from regexp_split_to_table(s, '\s+') as t
    where length(t) between 6 and 64
      and t ~ '^[A-Za-z][A-Za-z0-9]+$'
      and t ~ '[a-z]'
      and t ~ '[A-Z]'
    limit 40
  loop
    out := out || ' ' || regexp_replace(token, '([a-z0-9])([A-Z])', '\1 \2', 'g');
    added := added + 1;
    if added >= max_added then
      return btrim(out);
    end if;
  end loop;

  return btrim(out);
end;
$$;

-- 3) 触发器：自动维护 fts_tokens
create or replace function public.documents_fts_tokens_update()
returns trigger
language plpgsql
as $$
begin
  new.fts_tokens := to_tsvector(
    'simple',
    coalesce(new.content, '') || ' ' || coalesce(public.rag_fts_alias_text(new.content), '')
  );
  return new;
end;
$$;

drop trigger if exists trg_documents_fts_tokens_update on public.documents;
create trigger trg_documents_fts_tokens_update
before insert or update of content
on public.documents
for each row
execute function public.documents_fts_tokens_update();

-- 4) 回填历史数据
-- 4.1 仅更新空值（避免无意义全表写）
update public.documents
set fts_tokens = to_tsvector('simple', coalesce(content, '') || ' ' || coalesce(public.rag_fts_alias_text(content), ''))
where fts_tokens is null;

-- 4.2 （可选）全量回填：使旧数据立刻享受 alias token（大表建议离峰/分批）
-- update public.documents
-- set fts_tokens = to_tsvector('simple', coalesce(content, '') || ' ' || coalesce(public.rag_fts_alias_text(content), ''));

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
  set fts_tokens = to_tsvector(
    'simple',
    coalesce(d.content, '') || ' ' || coalesce(public.rag_fts_alias_text(d.content), '')
  )
  where (d.metadata ->> 'relativePath') = any(relative_paths);

  get diagnostics updated_count = row_count;
  return updated_count;
end;
$$;

grant execute on function public.refresh_documents_fts_tokens_for_paths(text[]) to service_role;

