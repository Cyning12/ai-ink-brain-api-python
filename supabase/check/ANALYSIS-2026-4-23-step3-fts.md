# 分析：`supabase/check/2026-4-23.md` 第三步（FTS/keyword）为何“改 query 结果大变”

## 结论摘要

你在第 3 步观察到的现象是**正常且可解释的**：当前 `keyword_documents`（以及你手工用 `plainto_tsquery('simple', ...)` 模拟的查询）依赖 Postgres 的 **Full-Text Search（FTS）分词/归一化规则**。日期字符串在 FTS 中会被拆成多个 token，并且**前导 0 是否存在会直接影响 token 是否匹配**，导致：

- `plainto_tsquery('simple','2026-04-14')` 能命中
- `plainto_tsquery('simple','2026-4-14')` 反而**完全命不中**
- `plainto_tsquery('simple','2026-04-14 日记')` 可能命不中，是因为 `日记` 并不一定在文档内容里出现（FTS 默认是 AND 语义）

因此，“改 query 会影响结果”并不必然说明向量相似度（`match_documents`）很差；它首先说明 **keyword/FTS 对日期这类结构化字符串非常敏感**，需要做 query 归一化或改检索策略。

## 你当前数据状态（来自 2026-4-23.md）

- `public.documents` 总量：1513
- `embedding_null=0`、`fts_tokens_null=0`
- 存在 `metadata.filename='2026-4-14.md'` 的文档（`id=4414`）
- `keyword_documents`/`match_documents` 两个 RPC 都存在
- `documents.id` 为 `bigint`（这对 RRF 去重是 OK 的）

## 现象复盘与根因

### A. 为什么 `2026-04-14 日记` 返回 0 行？

你执行的是：

```sql
plainto_tsquery('simple', '2026-04-14 日记')
```

关键点：

1) **`plainto_tsquery` 默认是 AND 语义**
- query 会被拆成多个 lexeme，然后组合成 `lexeme1 & lexeme2 & ...`
- 只要其中一个 lexeme 在 `fts_tokens` 中不存在，就会 0 行

2) `日记` 很可能不在 `content` 内
- 你命中的那条 diary 文档标题是 `2026-4-14.md`，正文包含 `Day14 2026-04-14 ...`
- 但正文不一定出现“日记”这个词（或写成 diary / 日志 / diary 等）

结论：这条 query 等价于“必须同时包含 2026、04、14、日记”的文档；只要缺“日记”就 0 行。

### B. 为什么 `2026-04-14` 有结果、但 `2026-4-14` 无结果？

你验证到：

- `plainto_tsquery('simple','2026-04-14')` → 命中 `id=4414`
- `plainto_tsquery('simple','2026-4-14')` → 0 行

根因：FTS 对数字/符号的拆分与 token 形态会保留“04”与“4”的差异。

典型情况下（`to_tsvector('simple', content)`）：

- 文本中的 `2026-04-14` 会产生 lexeme：`'2026'`, `'04'`, `'14'`
- query `2026-4-14` 会产生 lexeme：`'2026'`, `'4'`, `'14'`

因为 `'04' != '4'`，所以 AND 组合无法满足，最终 0 行。

这解释了为什么“只是改了 query 的写法（是否补 0）”，结果从 1 条变 0 条。

## 为什么这会被误判为“相似度检索不理想”

第 3 步用的是 FTS（keyword）模拟，它衡量的是**词项匹配**，不是向量相似度：

- `keyword_documents` 对应 FTS/词频排名（你用 `ts_rank_cd` 也印证了）
- `match_documents` 才是向量检索（embedding + pgvector distance）

因此，如果你看到 “keyword_hits=0”，它更可能意味着：

- query 没有做归一化（日期格式、全半角、大小写等）
- query 里带了“强约束词”（如 `日记`）导致 AND 失败
- `keyword_documents` 的实现选择了 `plainto_tsquery`（AND）而不是更宽松的 OR/search query

## 建议的改进方向（优先级从高到低）

### 1) 对日期 query 做归一化（最关键）

目标：把用户输入的 `2026-4-14` 统一改写为 `2026-04-14`，同时生成“多形态候选”用于 keyword 召回：

- `2026-04-14`
- `2026/04/14`
- `2026.04.14`
- `2026 04 14`

你已经在后端实现了 **raw + rewrite 双路 keyword** 召回（`api/unified_chat.py`），下一步只要确保 rewrite 能把日期补 0，即可显著提升该类查询的 keyword 命中率。

### 2) keyword 查询从 AND 改为更宽松的 query 组合

如果 RPC 内部用的是 `plainto_tsquery`（AND），建议改为：

- `websearch_to_tsquery('simple', query_text)`（更贴近“搜索框”语义，支持更宽松的组合）
- 或将 token 用 OR 连接（对日期/短 query 更友好）

> 该项需要改 Supabase 侧 RPC（SQL function），不是 Python 侧即可完成。

### 3) 对“日记/diary/日志”做同义词/降权处理

对于 `2026-04-14 日记` 这类 query：

- 如果“日记”并不在正文出现，就会 0 行
- 可以在 rewrite 时把“日记”降级为可选词（OR），或者把其替换为 metadata 过滤（见下一条）

### 4) 用 metadata 做结构化过滤（对 diary 最稳）

你实际要找的很可能是：

- `metadata.relativePath = 'diary/2026-4-14.md'`
- 或 `metadata.filename = '2026-4-14.md'`
- 或 `metadata.slug = '2026-4-14'`

建议在检索链路增加一条“结构化召回”：

- 当 query 命中日期模式时，先尝试匹配 `metadata->>'filename'` / `metadata->>'slug'` / `metadata->>'relativePath'`
- 命中则直接提升排序或直接作为强候选

该策略不依赖 FTS 分词，也不依赖 embedding，相当于“确定性召回”。

## 建议的验证 SQL（用来量化问题）

### A) 看看 `fts_tokens` 实际把日期拆成什么（直观定位 04 vs 4）
```sql
select id, ts_debug('simple', content)
from public.documents
where id = 4414;
```

### B) 验证 AND 导致 0 行（去掉“日记”马上命中）
```sql
select id
from public.documents, plainto_tsquery('simple', '2026-04-14 日记') q
where fts_tokens @@ q;

select id
from public.documents, plainto_tsquery('simple', '2026-04-14') q
where fts_tokens @@ q;
```

### C) 验证前导 0 的关键性
```sql
select id
from public.documents, plainto_tsquery('simple', '2026-4-14') q
where fts_tokens @@ q;

select id
from public.documents, plainto_tsquery('simple', '2026-04-14') q
where fts_tokens @@ q;
```


