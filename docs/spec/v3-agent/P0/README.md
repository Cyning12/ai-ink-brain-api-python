# P0 · 阶段 A 中间验收留档

> **用途**：存放 **阶段 A（P0-1 + P0-3）中间验收** 的人工留档（Timeline / 执行链路摘录），**不替代**任务单与 RUNBOOK 勾选；总门禁仍以 [`../../../tasks/active/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`](../../../tasks/active/task_chatbi_v3_text2sql_tool_latency_obs_v1.md) 及 [`../../../tasks/active/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`](../../../tasks/active/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md) 为准。

## 文件

| 文件 | 说明 |
|------|------|
| [`阶段A-中间验收.md`](阶段A-中间验收.md) | 成功路径：子阶段 SSE、`text2sql_phases_ms`、无 error |
| [`阶段A-中间验收-超时.md`](阶段A-中间验收-超时.md) | 超时抽检：`LLM_API_TIMEOUT`、`llm_sql` 与 `retrieve` 等 |

## 环境说明（读数时必读）

Text2SQL **`retrieve`** 依赖 **Supabase / 向量检索及外网链路** 时，**更容易出现**阶段性墙时钟偏长或与 LLM 分阶段超时叠加后的「慢 + 超时」表象；**不宜单独解读为代码回归**。超时留档文首有详细说明，与成功路径 **对读**。

---

**给 Cursor**：`P0`、`阶段A`、`中间验收`、`Supabase`、`text2sql_phases_ms`、`stage_a_done`
