# Task：RAG Keyword（websearch）+ 日期查询归一化（v1）

## 背景与目标

对齐 `SPEC-07`：提升 diary/日期类查询在 FTS/keyword 路的稳定性，避免因 `04` vs `4` 或 AND 语义导致 0 hits。

## 范围

- Supabase：确认并应用 `public.keyword_documents` 的 `websearch_to_tsquery` 实现（若线上仍为 plainto）
- Python：在 `api/unified_chat.py` 的 keyword RPC 调用前加入日期候选 OR 归一化（raw + rewrite 两路）

## 非范围

- 不做历史文档全量清洗
- 不改向量 RPC

## 依赖与引用

- SQL：`supabase/sql/hybrid_search.sql`
- 代码：`api/unified_chat.py`
- 分析：`supabase/check/ANALYSIS-2026-4-23-step3-fts.md`

## 验收标准（可勾选）

- [ ] Supabase 执行 `supabase/sql/hybrid_search.sql` 后，`keyword_documents` 内部使用 `websearch_to_tsquery`
- [ ] 输入 `2026-4-14`/`2026-04-14` 两种格式，keyword 结果一致或接近（至少包含 diary 目标文档）
- [ ] `pytest` 全绿

## 实现备忘（回填）

- 涉及文件：
  - `api/unified_chat.py`
  - `supabase/sql/hybrid_search.sql`（如需再次执行/对齐）

