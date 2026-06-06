> **状态**：`done`  
> **归档说明**：2026-06-06 由 P2 消化；FTS alias v2（分隔符/版本号/标识符）已合入 `public.rag_fts_alias_text()`，见 `supabase/sql/hybrid_search.sql`。

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **task_slug** | `task_rag_b2_v2_fts_alias_symbols_versions_identifiers` |
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | legacy 归档消化；正文为历史交付记录，P2 仅补状态与元信息表 |
| **semi_auto** | `false` |
| **git_branch** | `task/gov-docs-noise-p2-v1` |

## 失败路径

| # | Scenario ID | 触发 | 系统行为 | 可重试 | 用户可见 | 测试 |
|---|-------------|------|----------|--------|----------|------|
| F1 | `fp-legacy-archive` | legacy 文件被误要求重新激活开发 | 保持 `done` 归档状态；若需迭代应新建 task | 否 | — | — |

# Task：B2 v2｜FTS alias 扩展（分隔符/版本号/标识符）+ 分批回填

## 背景与目标

在 B2 v1（日期 alias）基础上，继续解决“同一实体多种写法”导致的 FTS 漏命中，覆盖：

- 分隔符变体：`_` `-` `.` `/` `\` 与空格互换
- 版本号变体：`v0.1.0` / `0.1.0` / `0-1-0` / `0_1_0`
- 标识符变体：驼峰/下划线/点号的拆分与 lower 形态（例：`RunnableWithMessageHistory`、`match_threshold`、`matchDocuments`）

仍然只改 `fts_tokens`，不改 `documents.content` / `documents.embedding`。

## 范围

- Supabase SQL：扩展 `public.rag_fts_alias_text()`（或拆分为多个 helper）
  - 追加版本号/标识符/分隔符 alias 生成
  - 保持输出可控（长度上限、去重）
- Supabase：提供分批回填模板（按 `id` 范围或按 `metadata.relativePath`）
- 增加回归 SQL 用例（至少 6 条），纳入 `supabase/check/`

## 非范围

- 不做中英同义（i18n 不在本任务）
- 不重算 embedding

## 设计建议（v2）

### 1) 分隔符归一（低风险高收益）

目标：让 `a_b`、`a-b`、`a.b`、`a/b`、`a b` 互相可命中。

实现思路（alias 文本追加）：

- 从 content 中抽取包含分隔符的 token（长度限制，例如 3–64）
- 生成归一化形态：把 `[_./\\-]+` 全替换为空格（或统一为 `-`）

### 2) 版本号 alias（中风险，需限制规则）

识别 `v?\d+\.\d+(\.\d+)?`：

- 追加 `0.1.0` 与 `v0.1.0`
- 追加分隔符替换版本：`0-1-0`、`0_1_0`

### 3) 标识符 alias（中风险，需限制规则）

识别常见形态：

- `CamelCase`：拆分为 `camel case`、`camelcase`
- `snake_case`：拆分为 `snake case`、`snakecase`
- 同时追加 lower 形态（FTS 的 `simple` 配置对大小写影响有限，但对用户 query 更友好）

> 规则必须“只对疑似标识符的 token 作用”，避免对普通英文句子膨胀。

## 分批回填模板（建议离峰执行）

### A) 按 id range

```sql
update public.documents
set fts_tokens = to_tsvector(
  'simple',
  coalesce(content, '') || ' ' || coalesce(public.rag_fts_alias_text(content), '')
)
where id >= :id_start and id < :id_end;
```

### B) 按路径（仅刷新某一批文件）

```sql
select public.refresh_documents_fts_tokens_for_paths(array[
  'diary/2026-4-14.md',
  'learning/2026-04-12/docs.langchain.com__oss_python_langchain_philosophy__8cb075f0ca.md'
]);
```

## 验收标准

- [ ] `v0.1.0` 与 `0.1.0`、`0-1-0`、`0_1_0` 互相可命中（同一篇 learning 文档范围内）
- [ ] `RunnableWithMessageHistory`（驼峰）用 `runnable with message history` 或 `runnablewithmessagehistory` 也能命中（若语料存在）
- [ ] 不显著增加误召回（抽样检查 top 20 结果相关性）
- [ ] 回填可分批执行，不阻塞线上

