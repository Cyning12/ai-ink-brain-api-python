# Text2SQL v1（极简版）— 后端任务单（MVP）

## 状态
- 草稿（总设初稿，供后端 Agent 执行与回填）

## 背景与目标
需要在 `ai-ink-brain-api-python` 后端新增 Text2SQL 基础能力，实现“自然语言 → SQL → 数据 → 自然语言”的最小闭环，用于 ChatBI 场景的查数问答。

本版本严格遵循 SDD 极简范围：只做 **意图识别 → 表结构检索 → SQL 生成 → 只读校验 → 执行 → 结果总结**，暂不做权限/审计/敏感字段等企业增强。

## 范围
- **包含**
  - Text2SQL 的端到端流程（见引用 SDD）
  - Text2SQL 专用 RAG 检索（FAISS）：表结构 DDL + 示例 SQL（3–5 条）
  - LLM 生成 SQL（仅 SELECT）
  - 数据库执行与结果集返回
  - LLM 结果总结（自然语言）
- **不包含（v1 不做）**
  - 权限控制、审计日志、敏感字段过滤
  - 自动从真实业务库拉 DDL 的增量同步（后续版本）
  - 异常重试、SQL 自动优化等增强

## 依赖与引用
- 极简流程 SDD：`docs/text2sql/v1/spec/ChatBI 系统 Text2SQL 模块（极简版）详细流程规范（SDD）.md`
- 前置任务（数据 SQL 落 Supabase）：`docs/text2sql/v1/spec/开始TextSQL之前的任务.md`
- 数据 SQL 来源（仅关注此处）：`docs/text2sql/v1/sql/`

## 接口与 I/O（v1 建议）

> 这里先给一个建议接口形态，具体路径/字段可由后端 Agent 在实现时回填并保持与前端对齐。

- **POST** `/api/py/text2sql/chat`
  - input：`{ session_id: string, query: string }`
  - output（建议 JSON）：`{ ok: true, answer: string, sql: string, rows: any[], columns?: string[] }`

说明：
- v1 可以先不做流式输出（SDD 没强制），但建议保留后续切换 Streaming 的空间。
- SQL 与 rows 返回主要用于调试与验收；未来可隐藏或加 debug 开关。
- 之后会融合到 /api/py/chat中，只是chat的一个functioncall能力分支，需要考虑后续融合的便携

## 实现步骤（后端 Agent 执行清单）

### 1) 完成前置：Supabase 数据表与样例数据

- 按 `docs/text2sql/v1/spec/开始TextSQL之前的任务.md` 完成：
  - 将 `docs/text2sql/v1/sql/` 的 MySQL 导出脚本改成 Supabase/Postgres 可执行版本
  - 在 Supabase SQL Editor 执行成功并产出可查询数据
  - 准备 3–5 条示例问答 + SQL（只 SELECT）

### 2) Text2SQL 专用“表结构/示例”语料准备（FAISS）

- 目标：让 “表结构 DDL + 示例 SQL” 可被检索到，进入 SQL 生成 prompt
- 最小方案（v1 允许手工）：
  - 将每张表的 DDL（或字段清单）整理成可向量化的文本片段
  - 将 3–5 条示例问答 + SQL 作为另一类片段
  - 用 FAISS 建一个 text2sql 专用 index（与现有 RAG index 隔离）

### 3) 意图识别（极简）

- v1：只做“是否结构化查数”的简单判断
- 建议策略：
  - 若 query 明显是查数（例如包含：查询/统计/多少/金额/人数/按月/按部门/TopN 等），进入 Text2SQL
  - 否则返回“非结构化查询”提示（或交给现有 RAG chat）

### 4) Prompt 组装与 SQL 生成（LLM）

按 SDD 组装 prompt：用户 query +（检索到的）DDL + 示例 SQL → 生成 SQL

强约束（必须写进 prompt）：
- 只允许 SELECT
- 只允许使用提供的表/字段
- 必须可在目标数据库执行（Postgres/Supabase）

### 5) SQL 基础校验（只读）

v1 只做硬约束：
- 禁止 UPDATE/DELETE/ALTER/DROP/INSERT/TRUNCATE 等
- 允许的关键字白名单（建议）：SELECT / FROM / WHERE / GROUP BY / ORDER BY / LIMIT / JOIN / WITH 等

### 6) 执行查询并拿到结果集

- 用连接信息连接目标数据库（本版暂只要求“能跑通”）
- 捕获基础异常（连接失败、SQL 执行错误、超时）
- 返回结构化结果（rows）

### 7) 结果总结（LLM）

把 rows（可截断）交给 LLM 总结成自然语言回答，贴合用户意图。

## 验收标准（v1）

- [ ] 能对 3–5 条示例问题生成正确 SQL（可在 Supabase/Postgres 执行）
- [ ] 执行结果集正确，且最终自然语言总结与结果一致
- [ ] SQL 校验能拦截明显写操作或危险语句
- [ ] Text2SQL 的“表结构/示例”检索可解释：能看到检索到的 DDL/示例片段

## 由后端 Agent 回填

- 涉及文件列表（新增/修改）
- API 路径与请求/响应 schema（最终版）
- 环境变量（数据库连接/LLM 配置）与默认行为
- 最小集成测试方式（如何复现/如何验收）

