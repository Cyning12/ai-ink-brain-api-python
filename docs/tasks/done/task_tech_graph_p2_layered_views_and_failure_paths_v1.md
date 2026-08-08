# Task：Tech Graph P2 — 分层视角 + 失败路径/排障图（基于 manifest）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


> **状态**：done  
> **关联图谱**：`docs/_tech_graph/00_main.ai.md`、`docs/_tech_graph/10_flow_rag.ai.md`、`docs/_tech_graph/11_flow_text2sql.ai.md`、`docs/_tech_graph/12_flow_fts.ai.md`、`docs/_tech_graph/13_flow_supabase_rpc.ai.md`  
> **前端依赖**：无

---

## 背景与目标

P0/P1 已解决“可接手 + 可校验漂移”，但新 Agent 在排障时仍缺少两类关键视图：

- **运行层（Runtime View）**：SSE/events、错误分支、降级策略、重试、超时
- **失败路径（Failure Paths）**：0 hits / embedding fail / RPC fail / DB fail / auth fail 的最短定位链路

P2 目标：在不增加大段文本的前提下，为关键子流程补齐 **排障友好** 的分层视角图，且与 `docs/_tech_graph/_manifest.json` 保持一致。

---

## 范围

### 1) 在 `.ai.md` 中补齐“失败路径/排障分支”（优先）

- [x] `docs/_tech_graph/10_flow_rag.ai.md`
  - [x] 明确 `embedding failed -> keyword-only`（若存在该策略）或 `-> no_data`
  - [x] 明确 `keyword_documents 0 hit`、`match_documents 0 hit`、`structured recall 0 hit` 的合流与最终输出
  - [x] 明确 `rpc retry` 的次数来源（env）与 `[retry=N]` 语义
  - [x] 明确 `tool.call.end payload` 的关键字段（仅列字段名，不贴大 JSON）

- [x] `docs/_tech_graph/11_flow_text2sql.ai.md`
  - [x] 明确 `validate_sql_readonly [err]`、`execute_select_sql [err]` 的错误输出与事件落点
  - [x] 明确 `TEXT2SQL_DATABASE_URL missing` 的最短失败路径

- [x] `docs/_tech_graph/12_flow_fts.ai.md`
  - [x] 明确 `websearch_to_tsquery` 与 `rag_fts_alias_text` 的边界（index-side vs query-side）
  - [x] 明确 `fts_tokens is null / refresh RPC` 的兜底链路（若适用）

- [x] `docs/_tech_graph/13_flow_supabase_rpc.ai.md`
  - [x] 明确常见失败：`Unauthorized/401`、网络错误、RPC 不存在

### 2) 生成“运行层总览图”（新增 1 个小文件，按需加载）

- [x] 新增 `docs/_tech_graph/14_runtime_observability.ai.md`
  - [x] 覆盖：events 类型（router/tool/error/latency/rag.sources/sql.result）
  - [x] 覆盖：关键日志落点（`rag_conversation_logs`）与 Debug 开关（env）
  - [x] 与 `00_main.ai.md` 用“加载”节点连接（不放进主图）

> 说明：此文件只做运行/排障视角，不重复业务主链路。

### 3) 人类友好版同步策略（最小）

- [x] 对应 `.md` 文件仅做“最小同步”：新增 2~4 个节点/边即可（避免重绘）

---

## 非范围

- 不做 P3 端到端边界图（前端/内容仓）——另立任务
- 不引入新的业务功能改动（仅图谱补强）
- 不引入大段文字/长 JSON/DDL 粘贴

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| manifest 真值 | `docs/_tech_graph/_manifest.json` |
| manifest 校验 | `python tools/tech_graph_manifest_check.py` |
| Mermaid 协议 | `docs/_tech_graph/99_mermaid_protocol.md` |

---

## 验收标准

- [x] 新增 `14_runtime_observability.ai.md` 且从 `00_main.ai.md` 可按需加载访问
- [x] RAG/Text2SQL/FTS/RPC 的 `.ai.md` 至少各补齐 2 条失败路径分支（`[err]` / `?>` / `retry` 等）
- [x] 所有新增硬边都有 `// → path#Lx` 或 `// → path::symbol` 锚点
- [x] `python tools/tech_graph_manifest_check.py` 仍输出 `OK`（P2 不应引入漂移）

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/_tech_graph/00_main.ai.md`、`docs/_tech_graph/00_main.md`、`docs/_tech_graph/10_flow_rag.ai.md`、`docs/_tech_graph/10_flow_rag.md`、`docs/_tech_graph/11_flow_text2sql.ai.md`、`docs/_tech_graph/11_flow_text2sql.md`、`docs/_tech_graph/12_flow_fts.ai.md`、`docs/_tech_graph/12_flow_fts.md`、`docs/_tech_graph/13_flow_supabase_rpc.ai.md`、`docs/_tech_graph/13_flow_supabase_rpc.md`、`docs/_tech_graph/14_runtime_observability.ai.md`、`docs/_tech_graph/14_runtime_observability.md` |
| 关键 env | `RAG_RPC_RETRIES`、`RAG_MATCH_COUNT`、`DEBUG_RAG`、`RAG_DEBUG`、`NODE_ENV`、`DEBUG_INGEST`、`TEXT2SQL_DATABASE_URL` |
| 图谱变更点 | RAG：补齐 `embedding failed -> keyword-only`、`hits==0 -> no_data`、`rpc retry=N (env)`、tool.call.end payload 字段；Text2SQL：补齐 `validate_sql_readonly [err]`、`execute_select_sql [err]`、`TEXT2SQL_DATABASE_URL missing`；FTS：补齐 `fts_tokens is null -> refresh RPC`；RPC：补齐 `Unauthorized/401`、网络错误、RPC 不存在 |

