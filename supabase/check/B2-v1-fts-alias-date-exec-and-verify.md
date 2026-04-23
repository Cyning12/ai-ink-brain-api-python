# B2 v1｜FTS 日期 alias（fts_tokens）执行与验收记录

## 背景

FTS 对日期写法敏感（`2026-4-14` vs `2026-04-14`），导致在“文档内定位/关键词检索”场景出现漏召回，即使 B1 已能结构化锁定目标文档，仍可能在 chunk 级检索中 0 hits。

## 目标

仅增强 `fts_tokens`（不改 `documents.content` / `documents.embedding`），让日期不同写法更稳定 @@ 命中：

- 补零/不补零
- 分隔符变体（`-` `/` `.` 空格）

## 变更点（Supabase SQL）

对应文件：`supabase/sql/hybrid_search.sql`

- 新增函数：`public.rag_fts_alias_text(input_text text)`
  - 从 `content` 抽取所有 `YYYY[-/.]M[-/.]D`，生成多形态 alias 文本
- 更新触发器：`public.documents_fts_tokens_update()`
  - `new.fts_tokens := to_tsvector('simple', content || ' ' || rag_fts_alias_text(content))`
- 更新刷新 RPC：`public.refresh_documents_fts_tokens_for_paths(relative_paths text[])`
  - 同样使用 `content + alias_text` 重算 `fts_tokens`
- 回填：
  - 默认仅 `fts_tokens is null` 的行（增量安全）
  - 提供可选全量回填（离峰/分批）

## 执行步骤（生产/远程库）

1) Supabase SQL Editor 执行：
   - `supabase/sql/hybrid_search.sql`

2)（可选）全量回填（离峰执行；大表建议分批）：

```sql
update public.documents
set fts_tokens = to_tsvector(
  'simple',
  coalesce(content, '') || ' ' || coalesce(public.rag_fts_alias_text(content), '')
);
```

## 验收 SQL（v1）

对同一日期，以下两种写法应当都能稳定命中（或至少不再出现“一条命中另一条 0 行”的情况）：

```sql
select id
from public.documents, plainto_tsquery('simple', '2026-4-14') q
where fts_tokens @@ q
limit 20;
```

```sql
select id
from public.documents, plainto_tsquery('simple', '2026-04-14') q
where fts_tokens @@ q
limit 20;
```

## 关联记录

- 数据与现象记录：`supabase/check/2026-4-23.md`
- 现象分析：`supabase/check/ANALYSIS-2026-4-23-step3-fts.md`

