# SPEC-06：Unified Chat（RAG）检索可靠性修复（v1）

## 背景

回归测试中出现两类问题：

1) **网络不稳定**导致 Supabase RPC 失败（`Connection reset by peer`），直接造成 `vector_hits/keyword_hits/hits=0`，用户感知为 RAG“完全失效”。

2) 网络恢复后，RAG 仍可能出现 `hits=0`：

```json
{
  "output": { "vector_hits": 0, "keyword_hits": 0, "hits": 0 },
  "error": null,
  "latency_ms": 3894
}
```

需要明确：

- 这是“库中确实没有相关内容”还是“检索链路策略过弱/误改写/未做双路召回导致漏召回”。

## 目标（v1）

在不改动旧 `/api/py/chat` 的前提下，提升 Unified（`/api/py/unified/chat` 与 `/stream`）的 RAG 检索可靠性与可解释性：

- 增加 RPC 级别**重试兜底**（应对瞬时网络抖动）
- RAG 检索使用 **raw + rewrite 双路 Keyword** 召回，并与 Vector 融合
- 0 hits 时输出可解释事件（why：raw/rewrite 各自命中数、是否 embedding 失败等）

## 非目标

- v1 不引入复杂 rerank（cross-encoder）
- v1 不改 Supabase SQL schema/RPC

## 设计

### 1) raw + rewrite 双路召回

- Keyword：
  - `keyword_documents(raw_query)`
  - `keyword_documents(rewritten_query)`
- Vector：
  - v1 保持对 `rewritten_query` 做 embedding（省成本）；可选再补 raw embedding
- 融合：
  - 使用现有 RRF（`fuse_hits_rrf`）对 Vector + (Keyword raw + Keyword rewrite) 去重融合

### 2) RPC 重试兜底

对以下调用增加有限重试（默认 2 次）：

- `keyword_documents`
- `match_documents`

触发条件：

- 异常信息包含 `Connection reset by peer` / `ECONNRESET` / `timeout` 等

### 3) 可解释事件（events[]）

在 Timeline 中增加或增强以下事件 payload：

- `tool.call.end`（rag.retrieve）：
  - `vector_hits`
  - `keyword_hits_raw`
  - `keyword_hits_rewrite`
  - `hits`
  - `retry_count`
  - `embedding_error`（若有）

## 验收用例

1) **RAG 有命中**
- Q：`Task 04 来源引用怎么做？`
- 期望：`rag.sources` 非空

2) **RAG 无命中（正常）**
- Q：`2026-4-14 的日记记录了什么`
- 期望：`rag.sources` 为空，但 `rag.retrieve` 的统计字段齐全且无异常；assistant 明确“库中未检索到该日期日记”

3) **网络抖动兜底**
- 人工模拟短暂失败（或等待偶发）：
- 期望：重试后成功，或失败时在 `rag.retrieve` 中能看到 retry 次数与错误原因

## 输出

- 代码修改：`api/unified_chat.py`（RAG 分支）
- 测试：新增/更新单测覆盖 raw+rewrite 的召回统计字段

