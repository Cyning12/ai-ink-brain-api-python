# B2 v2｜FTS alias（分隔符/版本号/标识符）执行与验收（模板）

## 目标

在 B2 v1（日期 alias）基础上，扩展 `fts_tokens` 的 alias 能力，提升以下写法变化的 @@ 命中稳定性：

- 分隔符：`_` `-` `.` `/` `\` 与空格互换
- 版本号：`v0.1.0` / `0.1.0` / `0-1-0` / `0_1_0`
- 标识符：CamelCase 拆分（例：`RunnableWithMessageHistory` → `Runnable With Message History`）

## 执行

1) Supabase SQL Editor 执行：
   - `supabase/sql/hybrid_search.sql`

2)（建议）对指定路径增量刷新（避免全表回填）：

```sql
select public.refresh_documents_fts_tokens_for_paths(array[
  'diary/2026-4-14.md',
  'learning/2026-04-12/docs.langchain.com__oss_python_langchain_philosophy__8cb075f0ca.md'
]);
```

3)（可选）离峰分批回填（按 id range）：

```sql
update public.documents
set fts_tokens = to_tsvector(
  'simple',
  coalesce(content, '') || ' ' || coalesce(public.rag_fts_alias_text(content), '')
)
where id >= :id_start and id < :id_end;
```

## 验收 SQL

### A) 版本号写法变体

```sql
select id
from public.documents, plainto_tsquery('simple', 'langchain v0.1.0') q
where fts_tokens @@ q
limit 20;
```

```sql
select id
from public.documents, plainto_tsquery('simple', 'langchain 0.1.0') q
where fts_tokens @@ q
limit 20;
```

```sql
select id
from public.documents, plainto_tsquery('simple', 'langchain 0_1_0') q
where fts_tokens @@ q
limit 20;
```

### B) CamelCase 拆分写法

> 前提：语料中确实存在该标识符。

```sql
select id
from public.documents, plainto_tsquery('simple', 'RunnableWithMessageHistory') q
where fts_tokens @@ q
limit 20;
```

```sql
select id
from public.documents, plainto_tsquery('simple', 'Runnable With Message History') q
where fts_tokens @@ q
limit 20;
```

## 注意事项（约束）

- alias 生成有上限（避免 token 膨胀）；如遇极端长文，仅取前 200k 字符参与 alias
- 本阶段不做中英同义（i18n），仅做“格式 alias”

