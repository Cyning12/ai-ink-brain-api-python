# Task：Unified Chat（后端）— Router Trace 记录 Text2SQL SQL 与结果摘要（v1）

> **状态**：done（2026-04-30 验收通过）  
> **关联图谱**：无（仅补齐可追溯日志字段，不改业务流程）  
> **关联 Issue/PR**：无  
> **前端依赖**：无（仅落库；前端展示/查询另起任务）  
>
> 落盘规则：新任务一律新建在 `docs/tasks/active/`；验收通过后改状态为 `done（YYYY-MM-DD 验收通过）` 并 `git mv` 到 `docs/tasks/done/`，同时更新 `docs/tasks/_views/done.md` 索引。

---

## 背景与目标

目前已落库：
- `rag_conversation_logs.metadata.router_debug.router_trace_v1`（过程摘要：decision/ddl_search/fts_search/timing_ms/events_digest/errors）
- `rag_conversation_logs.metadata.router_debug.router_evidence_details`（候选摘要）

但当路由进入 Text2SQL 时，仍缺少对 **LLM 生成 SQL 是否正确** 的可追溯信息：无法直接从落库中判断“SQL 写错了 / 执行错了 / 结果为空但其实应有数据 / 总结错了”等问题。

目标：在不引入新表、不阻塞响应、严格控制体积与敏感信息的前提下，把 **Text2SQL 的 SQL 及结果摘要** 落库到 `router_trace_v1` 中，支撑事后复盘与对比。

---

## 范围

- [x] **新增落库字段**：写入 `public.rag_conversation_logs.metadata.router_debug.router_trace_v1.text2sql_exec`
- [x] **触发条件**：仅当最终 `mode == "text2sql"` 且实际执行了 SQL 时写入
- [x] **数据约束**：必须截断/限量/脱敏，禁止落库完整结果集与大字段
- [x] **体积约束**：与 `router_trace_v1` 的 8KB shrink 策略兼容；超限时优先丢弃 `rows_preview`
- [x] **测试**：新增最小 pytest 覆盖（mock SQL 执行结果），验证字段存在与截断策略生效

---

## 非范围

- 不把该信息塞进 `ddl_search`（`ddl_search` 语义仅为 DDL evidence 检索）
- 不新增 SSE 事件类型（仅落库字段；事件/契约变更另起任务）
- 不新增 DB 表/索引

---

## 落库位置（真值）

- **表**：`public.rag_conversation_logs`
- **列**：`metadata`（JSONB）
- **路径**：`metadata.router_debug.router_trace_v1.text2sql_exec`

---

## 数据结构：`router_trace_v1.text2sql_exec`（建议）

```json
{
  "text2sql_exec": {
    "sql": "SELECT ...",                 // 截断：<= 2000 chars
    "sql_raw": "```sql ...```",          // 可选，截断：<= 2000 chars
    "ok": true,
    "error": null,                       // 失败时 string，截断：<= 300 chars
    "latency_ms": 123,                   // 执行 SQL 的耗时（不含总结）
    "rows_len": 200,                     // 总行数（数字）
    "columns": ["id", "name"],           // 最多 30 个
    "rows_preview": [                    // 最多 10 行；每行最多 20 列；cell <= 80 chars
      {"id": "1", "name": "张三"}
    ],
    "truncated": true                    // preview/字段截断导致的不完整标记
  }
}
```

### 截断与脱敏（必须）

- `sql/sql_raw`：严格截断（建议 2000 字符），并对明显 secret 做 mask（复用 `_safe_text_for_event` 的 `***` 替换逻辑）
- `rows_preview`：
  - 行数：最多 10
  - 每行列数：最多 20
  - 每个 cell：转成字符串后截断到 80
  - 字段名白名单/黑名单（二选一，推荐黑名单）：
    - 黑名单示例：`phone`/`mobile`/`id_card`/`身份证`/`邮箱`/`address` 等，命中则该列不写入 preview（只保留 `rows_len/columns`）
- 严禁写入完整结果集（只允许 preview + rows_len）

---

## 与 8KB shrink 的兼容策略（必须）

当 `router_trace_v1` 超过 8KB：
1. 优先丢弃 `router_trace_v1.events_digest`
2. 丢弃 `ddl_search/fts_search.candidates`
3. **新增规则**：丢弃 `text2sql_exec.rows_preview`（保留 `sql/ok/error/rows_len/columns`）
4. 最后兜底缩短 `query_text`（既有逻辑）

---

## 验收标准

### 门禁与真值同步
- [ ] 无需新增事件 type；仅确保 `router_trace_v1` 落库逻辑仍通过现有 pytest

### 行为验收（阻断项）
- [ ] `mode != "text2sql"` 时：`router_trace_v1.text2sql_exec` 不存在/为空
- [ ] `mode == "text2sql"` 且执行成功：落库包含 `sql/ok/rows_len/columns/rows_preview/truncated`
- [ ] `mode == "text2sql"` 且执行失败：落库包含 `sql/ok=false/error`，且不写入大字段
- [ ] `rows_preview` 满足行/列/cell 截断与敏感字段过滤
- [ ] `router_trace_v1` 仍满足 8KB 约束（超限时能自动 shrink，且优先丢 `rows_preview`）

### 测试验收（阻断项）
- [ ] pytest 至少 1 条用例：mock 一次 text2sql 执行，断言 `text2sql_exec` 字段存在且截断生效

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `api/unified_chat.py`（text2sql 分支落库点；router_trace_v1 shrink 扩展） |
| 关键 env | 无新增（复用 `DEBUG_ROUTER_TRACE_DB` 的落库开关） |
| 数据库表 | `public.rag_conversation_logs`（无需迁移） |
| 图谱变更点 | 无（如新增 env 才需要更新 `_manifest.json`） |

