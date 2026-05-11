# P0 · 验收留档（阶段 A + 阶段 B）

> **用途**：存放 **阶段 A（P0-1 + P0-3）中间验收** 与 **阶段 B（P0-2 + 前后端 run_id 对齐留证）** 的人工留档（Timeline / 执行链路摘录），**不替代**任务单与 RUNBOOK 勾选；总门禁以 [`../../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`](../../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md) 及 [`../../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`](../../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md) 为准（**已归档 2026-05-11**）。

## 阶段 A

| 文件 | 说明 |
|------|------|
| [`阶段A-中间验收.md`](阶段A-中间验收.md) | 成功路径：子阶段 SSE、`text2sql_phases_ms`、无 error |
| [`阶段A-中间验收-超时.md`](阶段A-中间验收-超时.md) | 超时抽检：`LLM_API_TIMEOUT`、`llm_sql` 与 `retrieve` 等 |

## 阶段 B

| 文件 | 说明 |
|------|------|
| [`阶段B-验收.md`](阶段B-验收.md) | 基准留档（含历史双 `run_id` 样例时可对照） |
| [`阶段B-验收-1.md`](阶段B-验收-1.md) | **修订版**：前端于 **`meta`** 采用 **`payload.run_id`** 并回填后，**全链 `ChainEvent.run_id` 与 done / `CHATBI_JSON_LOG` 同源**（文首「修改后的表现」） |
| [`阶段B-留证-curl-stream-b-smoke-2026-05-11.md`](阶段B-留证-curl-stream-b-smoke-2026-05-11.md) | **curl SSE 原文落盘**（`b-smoke`、`prefer=text2sql`）；**stderr `text2sql_tool_call_end`** 对读见该文件 **§stderr 对齐** |

## 环境说明（阶段 A 读数）

Text2SQL **`retrieve`** 依赖 **Supabase / 向量检索及外网链路** 时，**更容易出现**阶段性墙时钟偏长或与 LLM 分阶段超时叠加后的「慢 + 超时」表象；**不宜单独解读为代码回归**。超时留档文首有详细说明，与成功路径 **对读**。

---

**给 Cursor**：`P0`、`阶段A`、`阶段B`、`中间验收`、`Supabase`、`text2sql_phases_ms`、`CHATBI_JSON_LOG`、`stage_b_done`、`tasks/done`
