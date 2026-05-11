# Text2SQL 可观测（V3）— 执行计划 · Checklist · 验收流程

> **关联任务（真值：拍板 / 改进点 / 主验收勾选）**：[`task_chatbi_v3_text2sql_tool_latency_obs_v1.md`](task_chatbi_v3_text2sql_tool_latency_obs_v1.md)  
> **维护约定**：本文件为 **过程文档**；实现推进中 **随 PR / 会议结论同步改**（执行步骤打勾、环境键名、事件名、pytest 路径等）。**架构拍板** 仍以任务单 **§拍板** 为准；若与本 runbook 冲突，**以任务单为准**并修正本文件。  
> **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Observability-Text2SQL.md`、`SPEC-ChatBI-V3-Logging-Trace.md`  
> **状态占位**（执行中回填）：`planning` → `in_progress` → `stage_a_done` → `stage_b_done` → `ready_for_close`

---

## 1. 执行计划（分阶段）

### 阶段 A — P0-1 + P0-3（可先合并、中间验收）

| 序号 | 步骤 | 说明 | 状态 |
|------|------|------|------|
| A1 | 契约与设计冻结 | 读 `SPEC-ChatBI-V2-Events.md`、`_contract_manifest.json`、`SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md`；定子阶段 **事件名 / `chain.type` / payload**、`X-ChatBI-Sse-Contract` 递增；与 `tools/tech_graph_contract_check.py` 同 PR 绿 | [ ] |
| A2 | 分段计时 + `text2sql_phases_ms` | `text2sql_execute` 链路上对 `retrieve` / `llm_sql` / `validate` / `db` / `llm_summary` 打点；写入 **`ToolResult.data.text2sql_phases_ms`**（非负整数 ms；未经历阶段 **省略或 0** 二选一，PR 内写死） | [ ] |
| A3 | SSE 子阶段 emit | 进行中 emit（非顶层 `token`）；`subphase_id` / 对齐字段采用 **`text2sql.phase.<phase_id>`** | [ ] |
| A4 | LLM 分阶段 timeout | `CHATBI_TEXT2SQL_LLM_SQL_TIMEOUT_S`、`CHATBI_TEXT2SQL_LLM_SUMMARY_TIMEOUT_S` → 回退 `CHATBI_TEXT2SQL_LLM_TIMEOUT_S` → 默认 `120.0`；超时 **`LLM_API_TIMEOUT`** + `llm_sql` / `llm_summary` 可区分 | [ ] |
| A5 | 改进点 2 / 3 / 5（与 A 同批或紧随） | 确定性总结 `_try_summarize_aggregate`；`dialogue_context` / retrieve 预算复核；可选 **`CHATBI_TEXT2SQL_SUMMARY_LLM_MODEL`**（空白 = Intent 生效模型） | [ ] |
| A6 | 测试与回填 | pytest（含超时 / 多轮或长路径）；`PROJECT_CONFIG`、`.env.example`；必要时先增量 `_tech_graph/11_flow_text2sql.md` | [ ] |

### 阶段 B — P0-2（最终验收前完成）

| 序号 | 步骤 | 说明 | 状态 |
|------|------|------|------|
| B1 | JSON 日志根字段 | `request_id`、`run_id` 贯通（及 L1 Logging 根级约定） | [ ] |
| B2 | Text2SQL 扩展字段 | 日志中带 **`text2sql_phases_ms`**（与 `ToolResult.data` 同结构）；子阶段行可带 **`subphase_id`** | [ ] |
| B3 | 对齐验证 | 单次请求：日志中 `run_id` + `text2sql_phases_ms` 与 SSE / 会话 **人工可对齐** | [ ] |

### 阶段 C — 关单前

| 序号 | 步骤 | 说明 | 状态 |
|------|------|------|------|
| C1 | 图谱 | `_tech_graph/11_flow_text2sql.md` + `.ai.md` 与实现一致 | [ ] |
| C2 | 主任务勾选 | 任务单 **§验收标准** 全部勾选；**禁止**在缺 B 时宣称总规 P0 最终验收 | [ ] |

---

## 2. Checklist（与主任务对齐）

> **对外宣称**：以任务单 [`task_chatbi_v3_text2sql_tool_latency_obs_v1.md`](task_chatbi_v3_text2sql_tool_latency_obs_v1.md) **§验收标准** 勾选为准。下表用于 **过程分解**；完成后 **回抄** 到主任务单对应 `- [ ]`。

### 2.1 阶段 A（中间验收）

- [ ] SSE 子阶段事件 + `ToolResult` 上 **`text2sql_phases_ms`**；**进行中** 可区分等模型 / 查库
- [ ] 分阶段 timeout（§拍板 #5）+ **`LLM_API_TIMEOUT`** + phase 可区分（`detail.phase` 等）
- [ ] 契约：`X-ChatBI-Sse-Contract`、`_contract_manifest.json`、`tech_graph_contract_check` 与语义变更 **同合并批次**

### 2.2 阶段 B（P0-2）

- [ ] JSON 日志 **`request_id` + `run_id`** 贯通
- [ ] 日志含 **`text2sql_phases_ms`**，与 **同一 `run_id`** 的 SSE 可对齐；可选 **`subphase_id` = `text2sql.phase.<phase_id>`**

### 2.3 最终（A+B 后）

- [ ] **`text2sql_execute`** 聚合路径 **确定性总结**（典型 COUNT/单值用例）
- [ ] **`_tech_graph/11_flow_text2sql.md`** / **`.ai.md`** 已更新
- [ ] 新增 env 已写入 **`PROJECT_CONFIG`** + **`.env.example`**

---

## 3. 验收流程指引

### 3.1 总则

| 项 | 约定 |
|----|------|
| **验收真值** | 任务单 **§拍板** + **§验收标准**；L1：`Observability-Text2SQL`、`Logging-Trace` |
| **阶段门禁** | **阶段 A** 可单独 **中间验收**（合并主线或发布候选均可，由团队定）；**总规 P0 / 本单最终完成** 须在 **A + B + 最终项** 全部满足后 |
| **禁止** | 缺 **P0-2（日志贯通）** 即宣称 **总规 P0 已最终验收**（见任务单元信息、§拍板 #2） |

### 3.2 参与角色与职责（可按团队裁剪）

| 角色 | 职责 |
|------|------|
| **实现** | 代码、manifest、contract_check、pytest、图谱、配置表回填 |
| **契约 / 前端** | Timeline / `text2sql.phase.*` 与 `text2sql_phases_ms` 展示见 **Ink-Brain** `content/tasks/active/task_chatbi_v3_text2sql_phase_sse_timeline_frontend_v1.md`；`X-ChatBI-Sse-Contract` 变更须与 vNext 矩阵一致，避免静默破坏旧客户端 |
| **验收执行** | 按 §3.3–§3.5 跑通并留证（日志片段、pytest 输出、必要时录屏） |

**与 Ink-Brain 任务对齐的摘要（避免双文档各写一套）**：进行中 UI 靠 **`text2sql.phase.*`**；**终态分段 ms 以 `tool.call.end.output.text2sql_phases_ms` 为准**；**v1 维持 Contract `2`**；前端 v1 **须满足其任务单全部验收项** 方可宣称该前端任务 done —— 详见该文件 **§V1 交付与排期**、**§数据源与 UI 策略**。L1 总规摘要见 `SPEC-ChatBI-V3-Observability-Text2SQL.md` **§5.1**。

### 3.3 阶段 A — 中间验收流程

1. **环境**：检出含阶段 A 的 commit；`.env` / `PROJECT_CONFIG` 中 **timeout 与可选模型** 与 PR 说明一致。  
2. **自动化**：`pytest`（本单相关用例全绿）；记录命令与摘要到 **§4 进度日志**。  
3. **SSE / ToolResult**：多轮或长查询场景下确认：**`tool.call.end` 前** 已收到子阶段事件；结束帧或 Tool 结果中含 **`text2sql_phases_ms`**，且能区分 **`llm_*` vs `db`/`retrieve`**。  
4. **超时（可选抽检）**：将 SQL / Summary timeout 调至极小，确认 **T 秒内** 返回 **`LLM_API_TIMEOUT`** 且 **phase 可区分**（见 §拍板 #5）。  
5. **门禁**：§2.1 与上表 **A1–A6** 完成 → 可在 runbook / 团队看板标记 **stage_a_done**；主任务单仅勾选 **（A）** 两项（若策略为「中间也勾主单」）。

### 3.4 阶段 B — P0-2 验收流程

1. **日志格式**：确认结构化日志为 **JSON**，根级含 **`request_id`、`run_id`**。  
2. **归因**：同一次 Agent Text2SQL 请求，从 SSE **`meta`/`done`** 或客户端记录取得 **`run_id`**，在日志中 grep **同 `run_id`**，确认存在带 **`text2sql_phases_ms`** 的行（及可选 **`subphase_id`**）。  
3. **门禁**：§2.2 完成 → **stage_b_done**；主任务单勾选 **（B）** 项。

### 3.5 最终验收与关单

1. **合并条件**：主线（或发布分支）上 **阶段 A + B** 均已合入。  
2. **最终项**：§2.3（确定性总结、图谱、配置）全部满足。  
3. **主任务**：在任务单 **§验收标准** 中 **A+B+最终** 全部 `- [x]`。  
4. **对外表述**：总规 P0 本单可与 Overview **§2.1 P0 验收标志** 对齐宣称（仍遵守简历/对外不夸大「规划中」能力）。

### 3.6 产物建议（留档）

- pytest 命令与通过摘要  
- 一段脱敏 JSON 日志（含 `run_id` + `text2sql_phases_ms`）  
- 契约版本号与 PR 链接（可选）

---

## 4. 进度与变更日志（执行中回填）

| 日期 | 变更摘要 | PR / 备注 |
|------|----------|-----------|
| 2026-05-11 | 初版：执行计划、checklist、验收流程落盘 | — |
| 2026-05-11 | 阶段 A 实现：`text2sql_phases_ms`、`text2sql.phase.*` SSE、分阶段 timeout、确定性总结迁入 `text2sql_core`；manifest + contract_check 纳入 `tools.py` | 本 PR |

---

## 5. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版 |

---

**给 Cursor**：`RUNBOOK`、`text2sql_phases_ms`、`text2sql.phase`、`stage_a`、`stage_b`、`LLM_API_TIMEOUT`、`task_chatbi_v3_text2sql_tool_latency_obs_v1`
