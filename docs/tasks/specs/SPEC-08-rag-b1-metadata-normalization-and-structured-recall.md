# SPEC-08（B1）：RAG 元数据归一化 + 结构化召回（v1）

## 背景

当前 diary/日期类查询在 FTS/向量检索上存在天然不确定性：

- FTS 会受分词、前导 0、AND/OR 语义影响
- 向量检索对“精确定位某一天”并非最优

但 diary 的目标对象往往是**确定文件**（`metadata.filename/relativePath/slug`），更适合走“结构化召回”。

## 目标

在不改变 `documents.content` 与 `documents.embedding` 的前提下：

1) 为新写入文档补齐 `metadata` 中可用于结构化检索的规范字段（如 `date_norm`）
2) 对 diary/日期查询增加结构化召回路径（优先命中并提升排序），使查询对日期格式更鲁棒

## 范围 / 非范围

- **范围**
  - Python ingest：写入 `public.documents` 时写入/补齐 `metadata.date_norm`、`metadata.slug_norm`（可选）
  - Python retrieve：当 query 命中日期模式时，先尝试结构化召回（按 metadata 精确匹配）并合并到 hits
  - Supabase：不改表结构（仅写 metadata）
- **非范围**
  - 不重算 embedding，不全量重灌
  - 不改现有 `match_documents/keyword_documents` RPC 的输入输出

## 设计

### 1) metadata 规范字段（写入时生成）

对 `metadata` 中已存在的：

- `filename`（如 `2026-4-14.md`）
- `relativePath`（如 `diary/2026-4-14.md`）
- `slug`（如 `2026-4-14`）

提取日期并归一化：

- `date_norm`: `YYYY-MM-DD`
- `slug_norm`（可选）：`YYYY-MM-DD`（仅对纯日期 slug）

### 2) 结构化召回（读取时使用）

当 query 抽取到日期：

- 构造候选：
  - `date_norm = YYYY-MM-DD`
  - `filename = YYYY-M-D.md` / `YYYY-MM-DD.md`（两种）
  - `relativePath = diary/YYYY-?.md`（两种）
  - `slug = YYYY-M-D` / `YYYY-MM-DD`

召回方式：

- 直接通过 Supabase `from('documents').select(...)` 按 `metadata->>'date_norm'` 或 `metadata->>'relativePath'` 等过滤
- 将命中结果作为 “structured hits” 与 vector/keyword hits 一起做融合（可直接设置更高 fused_score 或在 RRF 前插入）

### 3) 旧数据兼容

不要求立即回填全库 `metadata.date_norm`。

- v1 可在结构化召回时同时尝试匹配旧字段（filename/relativePath/slug）保证旧数据可命中
- 后续可提供一次性回填脚本（可选，不作为 v1 必需）

## 验收标准

- [ ] 新写入 diary 文档会写入 `metadata.date_norm`
- [ ] `2026-4-14 的日记记录了什么` 能稳定命中对应 diary 文档（即便 FTS 失败）
- [ ] 不改 `documents.embedding`，无需重灌向量

