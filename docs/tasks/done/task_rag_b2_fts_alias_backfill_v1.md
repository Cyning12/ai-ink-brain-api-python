> **状态**：`done`  
> **归档说明**：2026-06-06 由 P2 消化；FTS 日期 alias（`public.rag_fts_alias_text`）与触发器已落地，见 `supabase/sql/hybrid_search.sql`。

# Task：B2 v1｜FTS alias（日期）+ 回填（Supabase）

## 背景与目标

对齐 `SPEC-09`：解决 FTS 对日期/分隔符写法敏感导致的漏召回（例如 `2026-4-14` vs `2026-04-14`）。

## 范围

- Supabase SQL：更新 `supabase/sql/hybrid_search.sql`
  - 新增 `public.rag_fts_alias_text(content)`：抽取日期并生成补零/不补零、分隔符变体 alias 文本
  - 触发器与刷新 RPC 统一用 `content + alias_text` 生成 `fts_tokens`
  - 提供可选“全量回填”SQL（离峰执行）

## 非范围

- 不改 `documents.content` / `documents.embedding`
- 不做中英同义（i18n 属于后续任务）

## 验收标准

- [ ] 在 Supabase 执行更新后的 `supabase/sql/hybrid_search.sql`
- [ ] 对同一篇 diary 文档：
  - `plainto_tsquery('simple','2026-4-14')` 与 `plainto_tsquery('simple','2026-04-14')` 至少一条能稳定命中（更理想是两条都命中）
  - 使用 `websearch_to_tsquery` 时两种写法都能命中
- [ ] 执行（可选）全量回填后，旧数据也能受益

