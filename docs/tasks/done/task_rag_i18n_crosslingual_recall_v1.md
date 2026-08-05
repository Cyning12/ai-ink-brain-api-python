# Task：RAG i18n（跨语言检索）v1｜中文查询召回英文内容

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> **状态**：done（2026-04-24 验收通过）  
> **关联图谱**：`docs/_tech_graph/10_flow_rag.md`、`docs/_tech_graph/12_flow_fts.md`  
> **关联 Issue/PR**：无  
> **前端依赖**：无（接口不变；如需前端展示 debug 信息，另起前端任务）

---

## 背景与目标

当前存在“**中文提问无法召回英文文档**”的情况：用户用中文描述概念/功能点时，英文资料（如 docs/README/英文笔记）在 Keyword/FTS 路与 rewrite 后的检索中容易漏命中，导致 RAG sources 为空或相关性显著下降。

目标：在 **不更改对外 API 契约** 的前提下，让 `/api/py/chat`（以及 Unified Chat 的 RAG 分支）在用户中文查询时，能稳定召回英文内容（至少在 Keyword/FTS 路）并可观测、可回归。

---

## 范围

- [x] **Query-side i18n 扩展（v1）**：对 Keyword/FTS 查询文本做“跨语言候选”扩展（不改 `documents.content`、不要求重算 embedding）
  - [x] 输入中文 query 时，生成一组英文候选/同义短语，并以 `OR` 形式合并进 `keyword_documents(query_text)` 的 `query_text`
  - [x] 必须保留原始 query 与原始关键 token（文件名、版本号、标识符等），不得被“翻译”覆盖
  - [x] 需要可控：最多候选数、每个候选最大长度、总 query_text 长度上限
- [x] **可观测性（事件 + 日志）**：
  - [x] Unified Chat：在 `events[]` 增加 `rag.query_expand`（或等价事件）输出扩展前后 query 信息（脱敏/截断）
  - [x] /api/py/chat：在 `rag_conversation_logs.metadata.match` 增加 `i18n_expand` 字段（与 Task05 的 `query_compare` 结构兼容）
- [x] **回归用例与最小测试**（pytest）：
  - [x] 覆盖：中文 query → 英文候选生成；候选上限与截断；空/异常时优雅降级（只用原 query）

---

## 非范围

- 不做“通用机器翻译全文索引”/不改 `documents.content`
- 不新增中文分词扩展（仍使用 Supabase `to_tsvector('simple', ...)` 与 `websearch_to_tsquery('simple', ...)`）
- 不要求 embedding 模型跨语言对齐（v1 先提升 Keyword/FTS 稳定性；向量侧优化另起任务）
- 不做中英同义词库的长期运营体系（v1 只做最小可用与可观测）

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| FTS 方案 | `supabase/sql/hybrid_search.sql`（`keyword_documents` 基于 `websearch_to_tsquery('simple', query_text)`） |
| Keyword query 构造 | `api/rag_recall_tools.py::keyword_query_text()`（现有日期/版本号 OR 扩展） |
| Unified RAG 分支 | `api/unified_chat.py`（RAG 检索阶段调用 `keyword_documents`） |
| Legacy chat 检索 | `api/index.py`（`/api/py/chat` 检索阶段） |
| Rewrite 行为 | `api/query_rewrite.py`（已改为“保持原语言并保留英文 token”） |
| 图谱 | `docs/_tech_graph/12_flow_fts.md`（B2 query-side expand 节点）、`docs/_tech_graph/10_flow_rag.md` |

---

## 设计建议（v1：最小可用 + 可控）

### 1) i18n 候选来源（优先级）

1. **轻量术语表（可选，推荐）**：仓内维护一个小型 JSON/YAML 映射（例如 50~200 条高频术语）
   - 中文 → 英文（可含多候选）
   - 仅在命中术语表时扩展，稳定、可预测、低成本
2. **LLM 生成候选（可选，开关控制）**：当术语表未命中且 query 为中文为主时，调用 LLM 生成 3~5 个英文检索短语
   - 必须启用严格约束：只产出“检索关键词短语”，不得生成长句
   - 必须缓存（按 query hash 缓存到内存/日志层即可，v1 不要求持久化）
3. **兜底：不扩展**：任何异常/超限均退回原 query（不得让 i18n 扩展成为可靠性风险）

> v1 推荐：先上 **术语表**（无需外部依赖），再加 LLM 开关；LLM 默认关闭。

### 2) query_text 合成规则（强制）

- 将候选与原 query 合成 `OR`：
  - 示例：`"langchain" OR "RunnableWithMessageHistory" OR "message history"`
- 候选必须经过清洗：
  - 去掉引号与控制字符
  - 仅允许字母数字、空格、`._-/`、下划线（必要时）
- 上限建议（可通过 env 调整）：
  - `I18N_EXPAND_MAX_CANDIDATES`：默认 5
  - `I18N_EXPAND_MAX_CANDIDATE_CHARS`：默认 48
  - `I18N_EXPAND_MAX_QUERY_TEXT_CHARS`：默认 240

### 3) 可观测输出（推荐字段）

- Unified Chat `events[]`：
  - `type="rag.query_expand"`
  - `payload`: `{ "raw": "...", "expanded": "...", "candidates": ["..."], "source": "glossary|llm|none", "truncated": true/false }`
- /api/py/chat 日志：
  - `metadata.match.i18n_expand`: 同上结构（raw/expanded/candidates/source/truncated）

---

## 验收标准

### A. 功能验收（最少 3 条）

- [x] **中文 → 英文召回**：当库中存在英文文档包含关键术语（例如 `RunnableWithMessageHistory` / `LangChain` / `vector store` 等）时：
  - [x] 用户用中文描述（不包含该英文词）也能在 Keyword/FTS 路出现命中（query-side glossary 扩展）
  - [x] Unified Chat 的 `events[]` 中出现 `rag.sources`，且 `rag.query_expand` 显示候选确实被 OR 合并
- [x] **不劣化既有路径**：英文原 query 不应被改坏（expanded 至少包含原 query；候选为空也可）
- [x] **可靠性兜底**：禁用 LLM 或任意异常时，检索仍可正常执行（只用原 query）

### B. 可观测性

- [x] Unified Chat：`events[]` 中存在 `rag.query_expand`（或等价），且字段被截断保护
- [x] /api/py/chat：`rag_conversation_logs.metadata.match.i18n_expand` 写入成功（字段结构稳定）

### C. 测试

- [x] `pytest` 全绿（`pytest -q tests`：32 passed）
- [x] 至少包含单测：
  - [x] 术语表命中生成候选 + OR 合成
  - [x] 上限/截断生效（候选数、字符数、总长）
  - [x] 异常兜底返回原 query

---

## 实现备忘（由后端 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `api/rag_recall_tools.py`、`api/unified_chat.py`、`api/index.py`、`tests/test_unified_chat_backend_v1.py`、`data/i18n_glossary.json`、`docs/_tech_graph/12_flow_fts.md` |
| 关键 env | `I18N_EXPAND_ENABLED`（默认 true）、`I18N_EXPAND_MODE=glossary|llm|off`（默认 glossary）、`I18N_EXPAND_MAX_CANDIDATES`（默认 5）、`I18N_EXPAND_MAX_CANDIDATE_CHARS`（默认 48）、`I18N_EXPAND_MAX_QUERY_TEXT_CHARS`（默认 240） |
| 数据文件 | `data/i18n_glossary.json`（v1 轻量术语表：中文短语 -> 英文候选短语列表，带 mtime 缓存与解析失败兜底） |
| 接口变更 | 无（仅 Keyword/FTS query_text 扩展 + Unified `rag.query_expand` events + `rag_conversation_logs.metadata.match.i18n_expand`） |
| 图谱变更点 | `docs/_tech_graph/12_flow_fts.md`：在 `keyword_query_text()` 的 Query-side expand（B2.1）补充 i18n 分支（glossary/错误兜底/OR 合成/上限） |

