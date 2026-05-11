# V3 待办：Text2SQL 工具链延迟与可观测性（多轮场景）

## 元信息

- **状态**：backlog（V3 开工时纳入迭代）
- **与 SPEC §2.1 批次对应**：本单承载 **P0-1** + **P0-2** + **P0-3**（见 **§拍板**）；允许 **分阶段 commit**（先 **P0-1+3** 中间验收，再 **P0-2**），**总规 P0 最终验收** 须在 **§验收勾选** 四项一并满足后再对外宣称完成。
- **V3 总规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md`（**§2.1 P0**、**§3** 任务归拢）  
- **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Observability-Text2SQL.md`；日志协同见 `SPEC-ChatBI-V3-Logging-Trace.md`
- **是否建议单独关单**：**禁止**在缺少 P0-2 时宣称 **总规 P0 已验收**；允许先合 **仅 1+3** 做 **中间验收**，见 **§拍板 #2**。
- **背景会话**：多轮追问下 `text2sql_query` 的 `tool.call.start` → `tool.call.end` 间隔可达百秒级，期间无 SSE，体感「卡在 step5→step6」
- **关联代码**：`api/agent.py`（工具事件边界）、`api/tools.py::text2sql_execute`、`api/text2sql_core.py`、`api/text2sql_api.py`（聚合快路径参考）
- **图谱**：`_tech_graph/11_flow_text2sql.md`（确定性总结分支与 Agent 路径对齐）
- **执行计划 · Checklist · 验收流程**（过程文档，随迭代同步更新）：[`task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`](task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md)
- **前端对接**（Timeline / SSE 消费 `text2sql.phase.*` 与 `tool.call.end` 内 `text2sql_phases_ms`）：Ink-Brain 仓 `content/tasks/active/task_chatbi_v3_text2sql_phase_sse_timeline_frontend_v1.md`（**v1 关单 / 数据源策略** 已拍板；后端 L1 摘要：`SPEC-ChatBI-V3-Observability-Text2SQL.md` §5.1）

## 拍板（2026-05-11 · 产品 / 架构）

以下取代前文「二选一 / PR 未定」的开放问题，作为本单实现与验收真值。

| # | 主题 | 决议 |
|---|------|------|
| 1 | **首包是否含 SSE** | **含**。交付形态须含 **SSE 子阶段事件** + **`ToolResult.data`（或等价）结构化分段 ms**；契约变更走 `X-ChatBI-Sse-Contract`、`_contract_manifest.json`、`tech_graph_contract_check`，与 **引入该契约的代码变更同批次合并**（可与 **§拍板 #2 阶段 A** 对齐，不必与 P0-2 同一 commit）。 |
| 2 | **P0-2 与 P0-1/3 的 commit / 验收节奏** | **允许阶段 commit**。**阶段 A**：**P0-1 + P0-3**（SSE + `text2sql_phases_ms` + LLM 分阶段 timeout）可先合并，并用于 **中间验收**（pytest / SSE+ToolResult 手工或自动化验证）。**阶段 B**：**P0-2**（JSON 日志 + `request_id`/`run_id` 贯通）。**最终**：阶段 A 与 B 均上主线后，**一并勾选** 下文 **§验收标准** 与总规 **P0 验收标志**。**禁止**在缺少 P0-2 时宣称总规 P0 已最终验收。 |
| 3 | **分段耗时键名与单位** | 结构化字段与日志共用 **`text2sql_phases_ms`**：`{ retrieve, llm_sql, validate, db, llm_summary }` → 非负 **整数 ms**；未经历的阶段可省略或 `0`（实现 PR 选一种并写死）。 |
| 4 | **「P95 可归因」验收层级** | P0 **不要求**现网 metrics 管道。**阶段 A**：**pytest** + SSE / `ToolResult` 上 `text2sql_phases_ms` 即可支撑中间验收。**最终**：**pytest** + **单次请求** JSON 日志中 `text2sql_phases_ms` + `run_id` **人工归因**；指标管道为后续增强。 |
| 5 | **LLM 超时 T 与错误码** | **分设**：`CHATBI_TEXT2SQL_LLM_SQL_TIMEOUT_S`、`CHATBI_TEXT2SQL_LLM_SUMMARY_TIMEOUT_S`（秒）；各自未设时回退 **`CHATBI_TEXT2SQL_LLM_TIMEOUT_S`**；再未设则代码默认 **120.0**（实现 PR 可微调并回填 `PROJECT_CONFIG`）。两阶段超时对用户可见错误沿用既有 **`LLM_API_TIMEOUT`** 语义；若已有 `stage` / `detail.phase` 字段，填 `llm_sql` / `llm_summary` 以区分。 |
| 6 | **`step_id` 与 `agent.step.*`** | 子阶段 SSE / 日志使用稳定 **`text2sql.phase.<phase_id>`**（`phase_id` 同 L1：`retrieve` \| `llm_sql` \| …），**不与**现有 Agent step 序号强行一一合并；排障以 `run_id` + `text2sql.phase.*` 为主键。 |
| 7 | **（改进点 5）总结用模型 env** | 新增 **`CHATBI_TEXT2SQL_SUMMARY_LLM_MODEL`**（可选）：**未设置或仅空白**时，总结阶段 chat 模型名与 **Intent 生效模型一致**（即 `INTENT_LLM_MODEL` 经 `api/intent_agent.py` 解析后的同一套默认/读取逻辑，实现时抽复用或同值读取，避免漂移）。 |

> **关于「P0-2 与 P0-1/3」**：总规 **P0 最终验收** 仍要求 **可观测（含 SSE + phases_ms）+ 日志 Trace + timeout** 全齐。「阶段策略」：**可先 1+3 合并并做中间验收，再 2，最后总验收**；与「四条必须最终都成立」不矛盾——矛盾的是 **未做 2 就宣称 P0 已验收**。

## 背景与目标

当前 V2 Agent 路径下，`tool.call.start/end` 包住 **整段** `text2sql_execute`（DDL 检索 → 生成 SQL → 执行 → 总结），`ToolResult.latency_ms` 为整段墙时；**同一工具内串行两次** `chat.completions.create`（`llm_generate_sql` + `llm_summarize`），多轮时 prompt 随 `history_to_rewrite_block` 变长，上游排队时延迟叠加。V3 目标：**可观测、可预算、低冗余调用**，避免用户误以为挂死。

## 范围 / 非范围

- **范围**：Agent 路径 Text2SQL 工具、SSE 契约扩展（若需新版本头，与 `SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` 对齐）、可选配置项。
- **非范围**：替换 SiliconFlow、重写 Text2SQL 算法；本单仅列改进点与验收方向。

## 改进点（V3 实施清单）

1. **子阶段 SSE + 结构化耗时（首包并存）**
   - 在 `text2sql_execute` 内分段计时（retrieve / llm_sql / validate / db / llm_summary），写入 **`ToolResult.data.text2sql_phases_ms`**（或任务回填的最终挂载点），并 **emit SSE 子阶段事件**（进行中可区分「等模型」vs「查库」）；契约版本 **`X-ChatBI-Sse-Contract`**、manifest、contract_check 同 PR。
   - **验收**：多轮场景下前端 **进行中** 可区分等模型 / 查库；**P95** 按 **§拍板 #4**（pytest + 单次日志人工归因）验收。

2. **Agent 路径复用确定性总结（跳第二次 LLM）**
   - `text2sql_api.py` 已有 `_try_summarize_aggregate`；`tools.text2sql_execute` 在「单行/单值数值」等条件下应走同一逻辑，避免简单 COUNT 仍调 `llm_summarize`。
   - **验收**：典型「多少条 / 几个」类查询仅 **一次** 生成 SQL 的 LLM 调用（或明确文档例外）。

3. **多轮上下文预算**
   - 对注入 `build_sql_prompt` 的 `dialogue_context`、`_text2sql_retrieve_query` 合并串设硬上限或摘要（已有 `TEXT2SQL_RETRIEVE_QUERY_MAX_LEN`，可复核 grounding 行膨胀）。
   - **验收**：第 N 轮 prompt token 有上界或监控指标，延迟不随轮次线性失控。

4. **LLM 调用超时与降级**
   - `OpenAI` 客户端为 `llm_generate_sql` / `llm_summarize` 配置合理 `timeout`；超时返回结构化 `error_code`（与现有 `LLM_API_TIMEOUT` 语义一致），避免无限挂起。
   - **验收**：下游慢时用户在 T 秒内收到失败/降级事件，而非仅长等待。

5. **（可选）模型分级**
   - 总结阶段模型由 **`CHATBI_TEXT2SQL_SUMMARY_LLM_MODEL`** 控制；**未设或空白 = 与 Intent 生效模型相同**（见 **§拍板 #7**）。若需「更小模型」显式写入该 env。
   - **验收**：配置项写入 `PROJECT_CONFIG` + `.env.example`；默认与 V2 行为一致（未设 env 时不改变现网模型选择）。

## 依赖与引用

- `docs/spec/v2-agent/SPEC-ChatBI-V2-Events.md` — 事件枚举扩展时同步
- `docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §4.2 V3 — 可与结构化日志 / Trace ID 一并落地

## 验收标准（V3 开工时勾选）

> **节奏**：**阶段 A（P0-1+3）** 可先勾选下列 **A** 项做中间验收；**阶段 B（P0-2）** 完成后勾选 **B** 项；**最终** 须 **A+B** 全勾满再宣称总规 P0 本单验收完成。  
> **验收流程细则**（角色、门禁顺序、阶段入口/出口、留档建议）：见 [`task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`](task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md) **§3**。

- [x] **（A · 中间）** 多轮 Text2SQL 具备 **SSE 子阶段事件** + **`ToolResult`（或等价）上 `text2sql_phases_ms`**，进行中可区分等模型 / 查库
- [x] **（A · 中间）** LLM 调用具备 **分阶段 timeout**（env 见 **§拍板 #5**）与 **`LLM_API_TIMEOUT`**（及可区分 `detail.phase` 若已有）
- [x] **（B · 最终）** JSON 日志贯通 **`request_id` + `run_id`**；含 **`text2sql_phases_ms`** 的日志行与 **同一 `run_id`** 的 SSE/会话可对齐；子阶段日志可带 **`subphase_id` = `text2sql.phase.<phase_id>`**（见 L1 Logging-Trace；开关 **`CHATBI_JSON_LOG`**，`api/chatbi_json_log.py`）
- [ ] **（最终）** `text2sql_execute` 对可判定聚合结果走 **确定性总结**，减少无谓 `llm_summarize`
- [ ] **（最终）** `_tech_graph/11_flow_text2sql.md` / `.ai.md` 与实现一致

## 实现备忘（回填）

- 由 V3 负责 Agent 回填：涉及文件列表、SSE manifest、环境变量表（`PROJECT_CONFIG`）
- P0-2 日志：`api/chatbi_json_log.py`；`api/tools.py::text2sql_execute`（`json_log_ctx` + `text2sql_phase_end`）；`api/agent.py`（`text2sql_tool_call_end`）；`tests/test_chatbi_json_log.py`

---

**给 Cursor**：关键词：`V3`、`backlog`、`text2sql_execute`、`tool.call`、`latency`、`_try_summarize_aggregate`、`_tech_graph`
