# Task：Chain Events（后端）— 统一事件模型输出（v1）

> **状态**：`pending`  
> **schedule_ref**：RECENT §1.1 #1  
> **关联**：`docs/UI/v1/UI-01-chain-chat-upgrade.md`

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` |
| **freeze_id** | — |
| **semi_auto** | `false` |
| **audit_profile** | `full` |
| **git_branch** | `task/ui-chain-events-backend` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | task 回填后人扫 |
| HG-AUDIT-R1 | pending | 30 | 22 R1 后人签 |

---

## 背景与目标

前端需要在一次对话中展示完整 chain（工具调用、SQL、图表等）。当前后端接口输出形态不统一（流式文本 vs JSON），缺少「事件级」结构化信息。

目标：

- 设计并实现最小可用的 `events[]` 事件模型
- 为 Text2SQL v1 与后续 Ticket Bot/Chat 统一铺路

---

## 范围

- 新增独立接口（建议）：
  - `POST /api/py/chain/chat`（返回 JSON，包含 `events[]`）
  - 或为现有接口新增 debug 模式：`?debug=events` 返回 JSON
- 事件模型（v1）至少覆盖：
  - `assistant.message`
  - `tool.call.start/end`
  - `sql.result`
  - `error`
  - `latency`

## 非范围

- 不要求链路图（Graph）结构（v1 用时间线即可）
- 不做企业级权限/审计（后续）

---

## 行为变更（Delta）

### ADDED

- **Requirement**：Chain Chat 最小事件流 API，响应含 `events[]` 时间线。  
  - **Scenario**：`chain-events-happy` — GIVEN 合法请求 WHEN `POST /api/py/chain/chat` THEN `ok: true` 且 `events[]` 含 `assistant.message` / 工具与 `sql.result` 等约定 type。  
- **Requirement**：错误路径仍返回结构化 `events[]`。  
  - **Scenario**：`chain-events-error` — GIVEN 内部失败 WHEN 请求处理 THEN `events[]` 含 `error` 事件且 `ok: false`（或等价字段）。

### MODIFIED

无（Previously: 无统一 chain 事件 JSON 面）

### REMOVED

无

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-chain-events-422` | 参数非法 | `422` + 结构化 `detail` | 否 | 字段级错误 |
| F2 | `fp-chain-events-tool-error` | Text2SQL / 工具内部错误 | `events[]` 含 `error` 事件，`ok: false` | 视错误 | 时间线错误节点 |
| F3 | `fp-chain-events-db-down` | 数据库不可用 | `500 DATABASE_DISCONNECT` 或等价 | 是 | 服务暂不可用 |

---

## 事件模型（建议 schema）

```json
{
  "ok": true,
  "run_id": "uuid",
  "events": [
    { "type": "assistant.message", "ts": 0, "step_id": "s1", "payload": { "role": "assistant", "content": "..." } },
    { "type": "tool.call.start", "ts": 1, "step_id": "t1", "payload": { "tool": "text2sql.generate_sql", "input": { "query": "..." } } },
    { "type": "tool.call.end", "ts": 2, "step_id": "t1", "payload": { "output": { "sql": "select ..." }, "error": null } },
    { "type": "sql.result", "ts": 3, "step_id": "q1", "payload": { "sql": "select ...", "columns": ["..."], "rows": [{ }], "truncated": true } }
  ]
}
```

---

## 验收标准

- [ ] 端到端返回 `events[]`，前端可直接按时间线渲染
- [ ] `events[]` 中包含 `sql.result`（rows/columns 截断）
- [ ] 错误路径也能返回 `events[]`（以 `error` 事件表达）
- [ ] 不影响现有 `/api/py/chat` 与 `/api/py/text2sql/chat`（可并存）
- [ ] PR 上 `pytest` workflow 全绿（本地等价：`pytest tests -m "not intent_eval and not intent_benchmark"`）

---

## 实现备忘

- v1 可先把 Text2SQL 的三个阶段「虚拟成 tool events」：
  - generate_sql / execute_sql / summarize
- 图表建议先输出 `chart.image`（url/base64）或 `chart.spec`（后续）
