# UI-04：Unified Chat 意图路由（v1）— auto 选择 RAG / Text2SQL / No-Data / Tools

## 背景

当前 Unified Chat（v1）只做极简二分：

- `text2sql`（查库类） vs `rag`（其它）

问题：

- 很多 query 不需要 rag/sql（例如写作、润色、头脑风暴），强行检索会引入噪声、增加成本
- 未来还会接入更多工具（code-rag、ticket-bot 等），需要统一路由框架

## 目标（v1）

在 **不引入数据库配置表** 的前提下，提供可维护、可观测的意图路由：

- `mode ∈ { rag, text2sql, no_data, tool:<name> }`
- 路由由两段构成：
  1) **规则快速判别**（keyword/regex）
  2) **轻量证据校验**（小 topk 检索/ddl 命中），防止误入 sql/rag
- 将路由决策写入 `events[]`，前端可在 Timeline/Debug 面板展示 why

> v1 不做“在线可运营配置表”，原因：变更频繁、维护成本高、需要权限/审计；先用代码内配置（可 json/yaml）+ env 即可版本化。

## 路由模式定义（v1）

1) **text2sql**
- 目标：结构化查库
- 输出：`sql.result` + tool events

2) **rag**
- 目标：基于文档库回答
- 输出：`rag.sources` + tool events

3) **no_data**
- 目标：无需 rag/sql 的普通问答/写作/润色
- 输出：仅 LLM 回答 + tool events（可不含 sources）

4) **tool:<name>**（v1 可先预留）
- 例如 `tool:code_rag`、`tool:ticket_bot`

## 路由输入（建议）

`POST /api/py/unified/chat` / `/stream`：

```json
{ "session_id":"...", "query":"...", "prefer":"auto|rag|text2sql|no_data|tool:xxx" }
```

> v1 允许仅支持 `auto|rag|text2sql`，但建议开始支持 `no_data` 与 `tool:*` 预留。

## 路由策略（v1 推荐）

### Step 0：prefer 强制

若 `prefer != auto`：

- `rag` → 直接 rag
- `text2sql` → 直接 text2sql（但仍做只读校验）
- `no_data` → 直接 no_data
- `tool:*` → 直接进入对应 tool（若未实现则返回 error 事件）

### Step 1：规则快速判别（fast rules）

- **SQL 倾向**：
  - 中文：查询/统计/多少/金额/人数/数量/Top/排行/按月/按部门/分组/汇总
  - 英文：count/sum/avg/group by/top
- **No-Data 倾向**：
  - 写作/润色/翻译/改写/总结/生成/头脑风暴/提纲/邮件/周报
  - 且不包含明显“查库/查文档”信号
- **Tool 倾向（预留）**：
  - code-rag：提到函数名/文件名/路径/报错栈等
  - ticket-bot：门票/订单/SKU/销量/渠道/周数 等

输出一个初判 `candidate_mode` 与 `rule_hits[]`（用于 why）。

### Step 2：轻量证据校验（evidence check）

目的：降低误路由。

#### 2.1 Text2SQL evidence（DDL 命中）

- 用 Text2SQL store 检索 DDL（topk=3）：
  - 若命中 DDL >= 1（score>阈值，阈值可 env），则允许进入 text2sql
  - 否则回退到 rag 或 no_data（按规则）

#### 2.2 RAG evidence（FTS 试探）

- 用 Supabase `keyword_documents(query, match_count=3)` 试探：
  - 若命中 >= 1，进入 rag
  - 否则更倾向 no_data（避免空检索噪声）

> v1 仅做小 topk，不改变主检索策略；只是用于路由判断。

### Step 3：最终 mode 决策

优先级建议：

1. tool:*（若命中强规则）
2. text2sql（规则命中 + ddl evidence）
3. rag（规则命中或默认 + fts evidence）
4. no_data（规则命中，或 rag evidence 不足）

## 可观测性（必须）

在 `events[]` 中新增一条（或复用 meta）：

- `type: "router.decision"`
- payload：
  - `prefer`
  - `candidate_mode`
  - `final_mode`
  - `rule_hits`: string[]
  - `evidence`: { ddl_hits, ddl_top_score, fts_hits, ... }
  - `fallback`: string | null

## 验收用例（v1）

1) **Text2SQL**
- Q：`统计 agent_info 表里有多少条数据`
- 期望：`final_mode=text2sql`，且包含 `sql.result`

2) **RAG**
- Q：`Task 04 来源引用怎么做？`
- 期望：`final_mode=rag`，包含 `rag.sources`

3) **No-Data**
- Q：`帮我把这段话润色成更正式的中文`
- 期望：`final_mode=no_data`，不做 sources/检索（可有 empty sources）

4) **误路由保护**
- Q：`统计一下我最近学了什么`（无 ddl/无 docs 命中）
- 期望：不进入 text2sql；更倾向 no_data 或 rag（按 evidence）

