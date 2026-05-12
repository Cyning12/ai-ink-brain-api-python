# ChatBI V3 — 可观测性：Text2SQL 工具链

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2** 支柱一、**§2.1** P0-1 / P0-3  
> **任务单**：`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`（验收勾选以任务单为准；**done**）

---

## 1. 问题陈述

Agent 路径下 `text2sql_execute` 被 **`tool.call.start` / `tool.call.end`** 整段包裹，墙时钟可达百秒级；内含 **DDL 检索 → SQL 生成 → 校验/执行 → 总结** 等串行阶段，用户侧易误判「挂死」。V3 本规约束：**可观测、可预算、可超时退出**。

---

## 2. 范围 / 非范围

| 类型 | 内容 |
|------|------|
| **范围** | `api/tools.py::text2sql_execute`、`api/text2sql_core.py`、`api/agent.py` 工具事件边界；**首包须并存**：**SSE 子阶段事件** + **`ToolResult.data.text2sql_phases_ms`**（与任务单 **§拍板** 一致）；契约走 **`X-ChatBI-Sse-Contract`** + manifest + `tech_graph_contract_check`；`llm_generate_sql` / `llm_summarize` 的 **分阶段 timeout**（env 见 `PROJECT_CONFIG` 与任务单 §拍板 #5）与既有 **`LLM_API_TIMEOUT`** 对齐；复用 `text2sql_api.py` 确定性总结（`_try_summarize_aggregate` 等）；`dialogue_context` / `_text2sql_retrieve_query` **预算复核** |
| **非范围** | 替换 SiliconFlow、重写 Text2SQL 算法；非 Agent 聚合 API 的 UX 改版 |

---

## 3. 子阶段模型（逻辑真值 — 实现可命名微调）

建议在实现中至少区分以下 **逻辑阶段**（与任务单 §改进点一致）：

| 阶段 ID（建议） | 含义 | 计时归属 |
|-----------------|------|----------|
| `retrieve` | DDL / 向量检索合并串 | I/O + 嵌入 |
| `llm_sql` | 生成 SQL 的 LLM 调用 | 上游 LLM |
| `validate` | SQL 校验（语法/策略） | 本地 CPU |
| `db` | 执行查询 | DB RTT |
| `llm_summary` | 自然语言总结 LLM | 上游 LLM |

**产出形态（首包强制并存）**：

1. **结构化耗时**：`ToolResult.data`（或任务单回填的最终路径）内 **`text2sql_phases_ms`**：`{ retrieve, llm_sql, validate, db, llm_summary }` → 非负整数 **ms**（未经历阶段省略或 `0`，与实现 PR 一致）。  
2. **SSE 子阶段事件**：进行中 emit，使前端无需等 `tool.call.end` 才拆分；新 `chain.type` / 事件名须同步 **`SPEC-ChatBI-V2-Events.md`**、**`_contract_manifest.json`**，且与 **`tools/tech_graph_contract_check.py`** 在 **引入该契约的合并批次** 内绿（可与任务单 **阶段 A（P0-1+3）** 对齐，**不必**与 P0-2 日志同一 commit）。子阶段 **`step_id` / `subphase_id` 建议** `text2sql.phase.<phase_id>`（见 Logging-Trace L1）。

---

## 4. 与 V2 契约的边界

- **不**使用顶层 `event: token` 传递 Text2SQL 子步（与 vNext **chain-only** 叙事一致）。  
- 若仅扩展 **`tool.call.end` 的 payload** 而不新增 `chain.type`，须评估前端 **`ChainEventCard`** 是否需展示折叠子耗时。  
- **版本协商**：若必须新 SSE 语义，优先走 **`X-ChatBI-Sse-Contract`** 递增与 vNext SPEC 对齐，**禁止**静默改旧客户端解析假设。

---

## 5. 验收方向（数值进任务单 / pytest）

- 多轮场景 **进行中** 可区分「等模型」与「查库」（**SSE**）；`tool.call.end` 仍带 **`text2sql_phases_ms`**。  
- **P95 可归因**（P0）：以 **pytest** + **单次请求 JSON 日志**可人工拆解各阶段 ms 为足；不要求现网 metrics 管道。  
- 典型「COUNT / 单值」路径：**不**无谓触发第二次 LLM（与任务单验收一致）。  
- LLM 调用在超时后返回 **结构化错误**（`LLM_API_TIMEOUT` + 可区分 phase），连接不无限挂起。  
- `_tech_graph/11_flow_text2sql.md`（及 `.ai.md`）与实现一致。

### 5.1 前端消费真值（跨仓协同 · 摘要）

> **详述与 UI 默认真值**（v1 关单定义、进行中 vs 终态数据源、`X-ChatBI-Sse-Contract`）：**Ink-Brain** 仓 `content/tasks/active/task_chatbi_v3_text2sql_phase_sse_timeline_frontend_v1.md`（§V1 交付与排期、§数据源与 UI 策略、§ChainEvent / Reducer）。**本 L1 不复制**前端验收勾选，避免双处漂移。

- **进行中**：`text2sql.phase.start` / `text2sql.phase.end`，用 `phase_kind` 区分 **llm** 与 **db/io**；单段展示用 `phase.end.latency_ms`。  
- **终态**：`tool.call.end` 的 **`output.text2sql_phases_ms`** 为 **唯一**「分段 ms」汇总真值（与后端 `ToolResult.data` 一致透出）。  
- **契约头**：前后端 v1 对齐 **`X-ChatBI-Sse-Contract: 2`**；升 `3` 须另任务 + vNext 矩阵。

---

## 6. 关联

- `docs/spec/v2-agent/SPEC-ChatBI-V2-Tool-Design.md`  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Events.md`  
- `docs/_tech_graph/11_flow_text2sql.md`

---

## 7. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 从总规拆出子规初版 |
| 2026-05-11 | 首包改为 **SSE + `text2sql_phases_ms` 并存**；P0 验收与 timeout / step_id 与任务单 **§拍板** 对齐 |
| 2026-05-11 | 契约/manifest 与 **引入语义的合并批次** 对齐；允许 **先 1+3 再 2**（见任务单 §拍板 #2） |
| 2026-05-11 | **§5.1** 前端消费真值摘要 + Ink-Brain 任务单链接（避免与前端任务重复维护） |
