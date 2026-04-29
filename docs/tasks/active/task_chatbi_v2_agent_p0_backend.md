# Task：ChatBI V2 Agent（P0 后端）— 接入 `agent.*` 事件、ReAct 循环与记忆

状态：done（2026-04-29：P0 后端 Agent 全量落地并归档）  
范围：仅后端 `ai-ink-brain-api-python`  
关联：  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md`  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Intent.md`  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Tool-Design.md`  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-ReAct-Loop.md`  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Memory.md`  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Events.md`
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Gap-Checklist.md` — 缺口清单与优先级对照  

前端依赖策略（必须遵守）：
- 若本任务需要改动前端（例如展示新的 `agent.*` 时间线信息），则要求：**后端先验收通过后**，再由后端主导创建/编写对应的前端任务单；本任务单验收不以“前端展示效果”作为阻断项。

---

## 背景与目标

将 ChatBI 从 V1 规则路由升级为 V2 Agent 架构，使后端具备：
- LLM 意图识别（Intent Agent）选择工具：`rag_search / text2sql_query / direct_answer`
- ReAct 多步循环：每步输出 `agent.step.start → agent.think → agent.intent → tool.call.start/end → agent.step.end`，并最终输出 `agent.final`
- 记忆管理（最小可用记忆 + Supabase 持久化）：将 ReAct 步骤与工具结果写入 `rag_conversation_logs.agent_steps/tool_results`（JSONB）
- SSE 事件流兼容 V1：对外 mode 语义仍使用 `rag/text2sql/no_data`，新增事件 `agent.*` 满足“前端可忽略未知 type”

---

## 范围 / 非范围

### 范围

1. 新增/实现 V2 Agent 相关后端模块
   - `api/intent_agent.py`
   - `api/agent.py`
   - `api/tools.py`（Tool 抽象 + Registry + `error_code/error_stage` 规范化）
   - `api/agent_memory.py`

2. 接入 `api/unified_chat.py`
   - 增加后端开关（例如 `CHATBI_USE_AGENT=true/false`）
   - Agent 路径输出 `agent.*` 事件；对外最终 `mode` 与 V1 模式一致
   - 失败/降级：按失败类型 fallback（SQL / RAG / LLM timeout 等）

3. Supabase 记忆表字段（JSONB）
   - 更新 `supabase/sql/create_rag_conversation_logs.sql` 或新增迁移 SQL，使表包含：
     - `agent_steps JSONB`
     - `tool_results JSONB`

4. 契约验收门禁
   - 确保 `_contract_manifest.json` 与 `api/unified_chat.py` 输出事件 type/payload 最小键一致

### 非范围

- 不要求前端 UI 立刻展示 `agent.*`（前端可忽略未知 type）
- 不做业务逻辑大改（只在必要路径接入 Agent）

---

## 验收标准（必须可操作）

### 1) 契约/门禁（阻断项，P0）
- [ ] 运行 `python tools/tech_graph_contract_check.py`：通过
- [ ] 运行 `python tools/tech_graph_manifest_check.py`：通过（确保 env/endpoint/rpc/table/anchors 未漂移）
- [ ] SSE 新增事件类型包括并按 spec 输出：
  - `agent.step.start`
  - `agent.think`
  - `agent.intent`
  - `agent.step.end`
  - `agent.final`
- [ ] `agent.think.payload.thought` 仅包含用户级 1-2 句话摘要（不输出系统提示/策略细节）

### 2) 功能验收（阻断项，P0）
- [ ] Agent 能在单工具场景输出正确 `agent.final` 与对外 mode（`rag/text2sql/no_data`）
- [ ] Agent 至少支持 2 个工具串行调用（通过 ReAct loop 实现）
- [ ] SQL 失败按失败类型 fallback：
  - SQL 生成失败：重试 1 次；仍失败换 `rag_search`
  - SQL 执行失败（表不存在/权限）：换 `rag_search`
  - SQL 无数据：直接回答“未查到数据”，不换工具
- [ ] RAG 失败按失败类型 fallback：
  - `RAG_RETRIEVE_EMPTY` fallback 到 SQL 必须 **gated**（满足结构化聚合意图信号 A/B/C 任一才允许）
  - `RAG_GENERATE_UNCERTAIN` 换 `direct_answer` 或追问
- [ ] Intent Agent 满足：
  - 去关键词化（语义判断）
  - `min_confidence` 默认 0.6
  - 超时（3s）降级到 V1 规则路由

### 3) 记忆验收（阻断项，P0）
- [ ] Session Memory 最小可用：最近 5 轮 + 最近 3 次 tool 结果摘要（可按 spec 实现/压缩）
- [ ] Supabase 持久化：Agent 运行后能在 `rag_conversation_logs.agent_steps/tool_results` 中观察到写入内容（JSONB）
- [ ] 记忆加载用于下一轮 Intent/Agent 上下文（至少最近窗口生效）

### 4) 回归验收（阻断项，P0）
- [ ] `CHATBI_USE_AGENT=false` 时仍保持 V1 行为不变（事件类型与 payload 与旧版一致）
- [ ] V2 路径失败时有优雅降级（不要破坏 SSE 最终 `done`）

---

## 实现备忘（给开发者的最小指引）

1. 事件输出：
   - 建议在 Agent step 粒度 emit `agent.step.start/think/intent/tool.call.start/tool.call.end/agent.step.end`
   - 最终补 emit `agent.final`
   - 必须确保 payload 最小键集合与 `_contract_manifest.json` 完全一致

2. gating（关键约束）：
   - `RAG_RETRIEVE_EMPTY` 不允许无条件 fallback 到 SQL
   - 实现时需要产出并传入结构化信号 `structured_signals`（至少包含：
     - `llm_prefers_sql`
     - `has_aggregation_signals`
     - 复用 Intent 的 SQL 倾向结果）
   - 信号责任方（建议在实现上拆清楚）：
     - **产出方**：`api/intent_agent.py` 在做出 `IntentDecision` 时产出 `structured_signals`（并随 `IntentDecision` 返回/或放入其 `raw_response`，但必须让 Agent 能拿到）。
     - **消费方**：`api/agent.py` / `FailureTypeHandler` 在处理 `RAG_RETRIEVE_EMPTY` 的 fallback 决策时读取 `structured_signals`，执行 gating 判断。
   - gating 判定结果只用于“是否允许换工具”，不用于改变外部 `mode` 语义（仍按 V1：`rag/text2sql/no_data`）。

3. P0/P1 优先级边界（两阶段落地建议）
   - 本任务（P0）验收优先保证“事件类型齐全 + payload 最小键集合满足 contract_check/manifest_check”
   - 建议开发过程两步走：
     - Phase 1（先过门禁）：完成 `agent.*` type/payload 与 `_contract_manifest.json` 对齐，并确保 `python tools/tech_graph_contract_check.py` 通过
     - Phase 2（再过时序）：在代码实现后进行人工 review/抽样回放 SSE，确认 `agent.*` 事件时序符合 spec（尤其是 step 粒度 start→think→intent→step.end）

3. 存储与 schema：
   - 新增 SQL 字段/JSONB 需与 `tools/tech_graph_manifest_check.py` 使用的 truth 保持一致

---

## 依赖与引用

- 技术图谱契约真值：`docs/_tech_graph/_contract_manifest.json`
- 契约检查脚本：
  - `tools/tech_graph_contract_check.py`
  - `tools/tech_graph_manifest_check.py`

---

## 交付物（完成后应留痕）

- 后端新增/修改的核心模块文件
- `api/unified_chat.py` 支持 V2 路径与 `agent.*` SSE 事件
- Supabase SQL 表字段就绪（`rag_conversation_logs.agent_steps/tool_results`）
- 通过 `tools/tech_graph_contract_check.py` 与 `tools/tech_graph_manifest_check.py`

---

## 归档记录

- `docs/tasks/done/done_chatbi_v2_agent_p0_backend_full_2026-04-29.md`

