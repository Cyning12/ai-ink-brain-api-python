# 任务：Text2SQL 无权限终态与禁止 RAG 后再启 Text2SQL

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |


## 元信息

- **状态**：**done**（2026-05-12；本单已归档至 **`docs/tasks/done/`**；验收真值见下）
- **关联 spec（归档）**：`docs/spec/v3-agent/text2sql/archive/3-无权限用户-非预期.md`（修复前快照）、`docs/spec/v3-agent/text2sql/archive/4-无权限用户-预期-终版.md`（**验收真值**）
- **图谱**：按需更新 `docs/_tech_graph/` 中 Agent 失败回落说明

## 背景与目标

无权限 / 表级策略拦截时，旧链路会 RAG → 再 Text2SQL 循环。**完成态**：

1. 策略类预取失败与 DB 权限/RLS 使用稳定 `error_code` 与用户可读中文（`api/tools.py`）。
2. Agent 对 **`SQL_EXEC_PERMISSION_DENIED` / `CHATBI_SQL_DENIED` / `CHATBI_SQL_WRITE_DENIED`**：**不再调用 `rag_search`**，直接 **`stop_now`**，终态 `assistant.message` 为工具返回的 `error`（无权限说明）。
3. 不再依赖 `suppress_sql_fallback` / `RAG_RETRIEVE_EMPTY` 特判防二次 Text2SQL（因已无「先 RAG」一步）。

## 范围 / 非范围

- **范围**：`api/agent.py`（`FailureTypeHandler`、终态模拟 LLM 流）、`api/tools.py`、`tests/test_unified_chat_backend_v2_agent.py::test_v2_text2sql_write_denied_stops_without_rag`。
- **非范围**：库侧 `GRANT`/RLS SQL；`CHATBI_USE_AGENT=false` 的 unified 直链路径。

## 依赖与引用

- `CHATBI_SQL_WRITE_DENIED`：`schema_prefetch_source=error_policy` 时由 `text2sql_execute` 返回。
- `FailureTypeHandler.TEXT2SQL_DENY_FINAL_ANSWER_CODES`：与上述三码集合一致。

## 验收标准

- [x] 无权限场景：`tools_used` 仅含 **`text2sql_query`**，**不出现** `rag_search`。
- [x] `assistant.message` 含无权限说明，**不出现**「问题太复杂」掩盖。
- [x] `pytest tests/test_unified_chat_backend_v2_agent.py::test_v2_text2sql_write_denied_stops_without_rag` 通过。

## 实现备忘

| 项 | 说明 |
|----|------|
| Agent | 拒绝码分支 `next_tool=direct_answer`，`stop_now=True`；已移除 `suppress_sql_fallback` / `last_text2sql_denial_message`；无权限终态仍发射与 `assistant.message` 一致的模拟 `text2sql_summary` 流。 |
| 测试 | `test_v2_text2sql_write_denied_stops_without_rag`：`rag_search` 若被调用则 `AssertionError`。 |

## 给 Cursor

验收、`TEXT2SQL_DENY_FINAL_ANSWER_CODES`、`CHATBI_SQL_WRITE_DENIED`、无 RAG、`text2sql/archive`。
