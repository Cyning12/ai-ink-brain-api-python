# Task：ChatBI V2 Agent（P0 后端）— 模块骨架落盘

> **状态**：done（2026-04-29：完成 tools/intent_agent/agent_memory 骨架落地；尚未接入 unified_chat 与 ReAct loop）
> **归档路径**：`docs/tasks/done/done_chatbi_v2_agent_p0_backend_modules_intent_tools_memory.md`
> **范围**：仅后端 `ai-ink-brain-api-python`
> **关联任务**：`docs/tasks/active/task_chatbi_v2_agent_p0_backend.md`

---

## 目标

为 ChatBI V2 Agent P0 建立“可执行的最小模块骨架”，使后续接入 `unified_chat.py` 与 ReAct loop 时可以直接复用：

- `api/tools.py`：Tool 抽象 + 三类工具封装（`rag_search / text2sql_query / direct_answer`）+ 统一 `error_code/error_stage`
- `api/intent_agent.py`：IntentDecision 数据结构 + 意图判定（LLM 可选，默认启发式）+ 结构化 gating 信号
- `api/agent_memory.py`：Supabase 持久化的最小 Session Memory（读 `agent_steps/tool_results` 相关字段；写入当前回合）

---

## 已完成（实现情况）

### 1) `api/tools.py`（Tool 抽象 + 三工具封装）

- [x] 定义 `ToolResult`：包含 `success/data/error/error_code/error_stage/latency_ms`
- [x] 定义 `ToolRegistry`：注册/获取工具
- [x] 内置并注册 3 个工具（函数级封装，复用 V1 逻辑）：
  - `rag_search_execute`
    - 复用 query rewrite + embedding + Supabase RPC + RRF 融合 + 一次性生成
    - 失败码：
      - `RAG_RETRIEVE_EMPTY`（检索无命中）
      - `RAG_GENERATE_UNCERTAIN`（生成不确定/为空）
      - `LLM_API_TIMEOUT`（超时）
  - `text2sql_execute`
    - 复用 text2sql retrieve（DDL/examples）+ 生成 SQL + `validate_sql_readonly` + 执行 + 总结
    - 失败码：
      - `SQL_GEN_EMPTY` / `SQL_GEN_SYNTAX`
      - `SQL_EXEC_TABLE_NOT_FOUND` / `SQL_EXEC_PERMISSION_DENIED`
      - `SQL_EXEC_NO_DATA`
      - `LLM_API_TIMEOUT`
  - `direct_answer_execute`
    - 仅调用 LLM 生成
    - 失败码：`LLM_API_TIMEOUT` / `UNKNOWN`

- [x] `tool_mode_map()`：内部 tool 名到 V1 mode 的映射（用于 unified_chat 对外兼容）

**落点文件**
- `api/tools.py`

---

### 2) `api/intent_agent.py`（IntentDecision + gating 结构化信号）

- [x] 定义 `IntentDecision` 与 `StructuredSignals`：
  - gating 依赖字段：
    - `structured_signals.llm_prefers_sql`（复用 `is_text2sql_intent`）
    - `structured_signals.has_aggregation_signals`（基于聚合语义关键词的启发式）
- [x] 提供 `decide_intent_v2()`：
  - timeout（3s）在超时时降级到 V1 `intent_router.decide_intent`
  - 默认保证可用性：启发式决策兜底
  - 置信度低于 `min_confidence` 时给出 fallback tool（与 spec 的 rag → text2sql → direct 路径一致）

**落点文件**
- `api/intent_agent.py`

---

### 3) `api/agent_memory.py`（最小 Session Memory）

- [x] `load(session_id)`：
  - 从 `public.rag_conversation_logs` 拉取 `query/response/created_at/agent_steps/tool_results`
  - 将最近记录还原为 LLM 友好 `history`（user/assistant message 列表）
- [x] `save(session_id, payload)`：
  - 插入一条新日志到 `rag_conversation_logs`：
    - `query/response`
    - `metadata.mode`
    - `agent_steps/tool_results`（JSONB）
  - 更新内存 cache

**落点文件**
- `api/agent_memory.py`

---

## 未完成（当前 P0 缺口）

以下项仍需在下一轮任务中落地（与你当前的“下一步偏好”无关，属于必做 P0）：

- [ ] 新增 `api/agent.py`（ReAct loop 编排 + tool 调用 + 失败类型 fallback + gating：`RAG_RETRIEVE_EMPTY` 受 structured_signals 控制）
- [ ] 修改 `api/unified_chat.py`：
  - 增加 `CHATBI_USE_AGENT` 分流（默认 V1 行为不变）
  - 在 V2 路径 emit `agent.step.start / agent.think / agent.intent / agent.step.end / agent.final`（并保留对外 V1 mode 语义）
  - SSE 最终 `done` 不破坏现有 payload 键集合
- [ ] 更新契约真值：`docs/_tech_graph/_contract_manifest.json` 补齐 `agent.*` 的 `type_values` 与 `payload_min_keys_by_type`
- [ ] 更新 Supabase SQL：`supabase/sql/create_rag_conversation_logs.sql` 增加 `agent_steps JSONB` 与 `tool_results JSONB`
- [ ]（建议）补最小测试：断言 V2 模式下出现 `agent.*` 事件且 payload 满足契约最小键集合

---

## 验证要点（用于你后续回放/抽检）

- 事件契约静态校验脚本：`python tools/tech_graph_contract_check.py`
  - 目前仍会失败（因为 `unified_chat.py` 尚未 emit `agent.*`）
- manifest 静态校验脚本：`python tools/tech_graph_manifest_check.py`
  - 目前仍会失败（因为 `_manifest.json`/`_contract_manifest.json` 与 SQL 字段尚未更新）

