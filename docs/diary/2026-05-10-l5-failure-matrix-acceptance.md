# L5 — `error_code` → 下一动作矩阵（验收归档 · 2026-05-10）

**口径**：`SPEC-ChatBI-V2-Agent-Overview.md` **§7.5.4** · **`api/agent.py`** → **`FailureTypeHandler.decide_next`**（至 **2026-05-10** 源码行 **238–282**）。  
**pytest 主文件**：`tests/test_unified_chat_backend_v2_agent.py`。  
**Runner**：`docs/tasks/active/task_chatbi_v2_acceptance_runner_v1.md` **§2.6** 标 **L5 通过** 时以本表 + 全量 **`pytest tests`（71 passed, 2 skipped）** 为据。

---

## 1. 矩阵表（`decide_next` 真值）

| `error_code` | 下一工具 `next_tool` | `stop_now` | 说明（与 §2.4 对齐） | pytest / 覆盖状态 |
|----------------|----------------------|------------|----------------------|-------------------|
| `SQL_GEN_EMPTY` | `rag_search` | false | SQL 生成仍失败 → 文档检索兜底 | 与 `SQL_GEN_SYNTAX` 同分支；**待补**独立 mock |
| `SQL_GEN_SYNTAX` | `rag_search` | false | 同上 | **待补**独立 mock |
| `SQL_EXEC_TABLE_NOT_FOUND` | `rag_search` | false | 表/权限类执行失败 → RAG | **`test_v2_json_multi_tool_sql_fail_then_rag`** |
| `SQL_EXEC_PERMISSION_DENIED` | `rag_search` | false | 同上（与 TABLE_NOT_FOUND 同列逻辑） | 与上行同 handler 分支；**待补**独立 `error_code` 字面 |
| `SQL_EXEC_NO_DATA` | `text2sql_query` | **true** | 不换工具，直接收束为「未查到数据」类结论 | **待补** mock |
| `RAG_RETRIEVE_EMPTY` | `text2sql_query` **或** `direct_answer` | false | **gating**（`_allow_sql_fallback`）开 → SQL；关 → `direct_answer` | **`test_v2_rag_empty_gated_fallback`** / **`test_v2_natural_diary_query_rag_empty_fallback_to_direct`** |
| `RAG_GENERATE_UNCERTAIN` | `direct_answer` | false | 检索答案不确定 → 直接答/追问 | **待补** mock |
| `LLM_API_TIMEOUT` | `rag_search` / `text2sql_query` / `direct_answer`（由 V1） | false | 超时降级 V1 规则路由 | **待补**工具层 `ToolResult` 触发；**`test_v2_intent_timeout_fallback_v1`** 覆盖 **Intent** 侧超时降级（非本表同一入口） |
| `UNKNOWN` / 其它 | `fallback_from_intent` | false | 回退到意图侧备用工具 | 多路径间接；**待补**显式 `UNKNOWN` 单测（可选） |

---

## 2. 验收结论

- **§7.5.4 硬门槛（`RAG_RETRIEVE_EMPTY` + gating）**：已在 CI 默认集合中由 **两则 canonical** 覆盖，**通过**。  
- **SQL → RAG 兜底**：**`SQL_EXEC_TABLE_NOT_FOUND`** 由 **`test_v2_json_multi_tool_sql_fail_then_rag`** 覆盖，**通过**。  
- **表中「待补」行**：不否掉本轮 **L5 通过** 结论；含义为「尚未为每个 `error_code` 字面建独立 pytest」，可在后续迭代按风险补 **专项 mock**（见 `L5-ChatBI-V2-FailureTypeHandler-pytest指南.md` §9）。

---

## 3. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-10 | 首版：自 `FailureTypeHandler.decide_next` 摘录矩阵，对齐 Runner §2.6 **L5 通过**。 |
