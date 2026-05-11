# ChatBI V3 — 结构化日志与 Trace

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2.1** P0-2  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §3.3.3 / §4.2（结构化日志、Trace ID）

---

## 1. 目标

为 Unified / Agent 路径提供 **可检索、可关联** 的日志与标识，支撑：V3 可观测（耗时归因）、安全审计（与 RBAC 落地后衔接）、运维排障。**不**在初版写死具体日志栈（如是否上 ELK），只约束 **字段契约与贯通关系**。

---

## 2. 标识贯通（逻辑真值）

| 标识 | 来源（现状或规划） | 约束 |
|------|-------------------|------|
| `request_id` | HTTP 层或中间件生成 | 单次 HTTP 请求唯一；**建议**进入 JSON 日志根字段 |
| `run_id` | SSE `meta` / `done` 已有语义（V2） | 单次 **Unified stream** 会话唯一；日志中须可与 SSE 帧对齐 |
| `session_id` | 业务会话 | 与 `rag_conversation_logs` 一致；落库失败分支仍建议打日志 |

**原则**：同一用户可见错误与后端排查路径，至少共享 **`request_id` + `run_id`** 之一可查。

---

## 3. JSON 日志形态（初版 — 实现 PR 填具体键名）

- **根级**：`timestamp`（ISO8601）、`level`、`message`、`request_id`、`run_id`（可选）、`session_id`（可选）、`service`（固定如 `chatbi-api`）。  
- **业务扩展**：`route`、`mode`（rag/text2sql/agent）、`tool`、`latency_ms`（整段或子阶段引用 P0-1 数据）、`error_code`（结构化错误时）。  
- **隐私**：默认 **不落** LLM delta 全文、不落完整 SQL 参数值（与 vNext **§8.6** 及运维约定一致）；调试开关见 `PROJECT_CONFIG`。

---

## 4. 与 Text2SQL 可观测的协同

P0-1 子阶段耗时 **写入** 日志时，须带同一 `run_id` / `step_id`（若 SSE 已发 `agent.step.*`），便于从 Timeline 跳到日志。

---

## 5. 非范围（初版）

- 前端 Console 镜像、客户端 log drain。  
- 跨服务分布式 trace（OpenTelemetry 全链路）—— **V3+** 可选增强，本规不强制。

---

## 6. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规 |
