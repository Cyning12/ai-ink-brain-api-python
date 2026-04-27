# SPEC-09（B2）：FTS（fts_tokens）增强 + 旧数据回填（v1）

## 背景

即便 keyword RPC 已采用 `websearch_to_tsquery`，日期类查询仍可能因内容内日期格式不一致导致漏召回：

- 文档中出现 `2026-04-14`，用户输入 `2026-4-14`
- FTS token 可能是 `'04'` 而 query token 是 `'4'`，导致 `@@` 失败

查询侧候选扩展可以缓解，但在更多“结构化字符串”（版本号、编号、日期）场景下，写入侧增强能进一步降低漏召回概率。

## 目标

在不重算 embedding 的前提下：

1) 让 `fts_tokens` 同时包含“原文本 token”与“规范化别名 token”
2) 通过一次性回填/刷新，使旧数据也获得增强后的 `fts_tokens`

## 范围 / 非范围

- **范围**
  - Supabase：增强 `documents_fts_tokens_update` 触发器的生成逻辑
  - Supabase：提供回填方式刷新历史 `fts_tokens`
- **非范围**
  - 不修改 `documents.content` 与 `documents.embedding`
  - 不更换中文分词扩展（仍使用 `'simple'`）

## 设计

### 1) 生成“别名文本”（alias_text）

在触发器中对 `new.content` 派生一个 `alias_text`（仅用于 FTS，不落 content）：

- 从内容中抽取日期形态 `YYYY-M-D` / `YYYY-MM-DD`
- 生成规范化 `YYYY-MM-DD` 并追加到 alias_text
- 可扩展：对分隔符变体（`/` `.` 空格）生成别名

最终：

- `new.fts_tokens := to_tsvector('simple', coalesce(new.content,'') || ' ' || coalesce(alias_text,''));`

### 2) 旧数据回填

提供两种方式：

- **全表回填**（一次性）：
  - `update public.documents set fts_tokens = to_tsvector(...)`
- **按路径回填**（增量）：
  - 扩展/复用 `refresh_documents_fts_tokens_for_paths(relative_paths text[])`

## 风险与约束

- 对大表执行全表回填会产生写放大；建议离峰执行，并分批（可按 id range）
- alias 生成要避免过度膨胀（只对明确日期模式生成；设置上限）

## 验收标准

- [ ] 用户输入 `2026-4-14` 与 `2026-04-14` 的 keyword 命中接近（不再因前导 0 造成 0 hits）
- [ ] 不改 `documents.embedding`，无需重灌向量
- [ ] 回填后旧数据同样受益（随机抽样验证）

