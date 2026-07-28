# Done：ChatBI V2 Agent（P0 后端）— 全量落地归档（2026-04-29）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本文件无 Wiki 增量（2.19 lint-wiki-delta） |


> **状态**：done  
> **范围**：仅后端 `ai-ink-brain-api-python`  
> **关联任务**：`docs/tasks/active/task_chatbi_v2_agent_p0_backend.md`

---

## 完成内容（P0）

### 1) Agent 主链路（ReAct 多步 + 失败类型 fallback）

- [x] `api/agent.py`：实现 `ChatBIAgent`，支持多步工具串行调用（最小 ReAct loop）
- [x] 失败类型 fallback（P0）：
  - SQL 生成失败：重试 1 次；仍失败 → `rag_search`
  - SQL 执行失败（表不存在/权限）：→ `rag_search`
  - SQL 无数据：直接“未查到数据”，不换工具
  - RAG 空命中：按 gating A/B/C 才允许 fallback SQL，否则走 `direct_answer`
  - Intent/LLM 超时：降级到 V1 规则路由
- [x] `_has_aggregation_signals` 添加 TODO（P1：替换为轻量语义判定）

### 2) 统一入口接入（JSON + SSE）

- [x] `api/unified_chat.py`：在 `CHATBI_USE_AGENT=true` 时走 V2 Agent 路径
- [x] 事件流：
  - 保持 V1 对外 `mode` 语义（`rag/text2sql/no_data`）
  - 新增 `agent.*` 事件（前端可忽略未知 type）
  - JSON 与 SSE 两条路径均对齐同一组 `agent.*` 事件

### 3) Memory（P0 约束：一轮结束写一次）

- [x] `api/agent_memory.py`：加载历史（最近窗口）+ 内存 cache
- [x] 持久化写入由 `api/unified_chat.py` 统一完成：每轮结束写 `rag_conversation_logs.agent_steps/tool_results`

### 4) Supabase schema（JSONB 字段）

- [x] `supabase/sql/create_rag_conversation_logs.sql` 增加：
  - `agent_steps jsonb`
  - `tool_results jsonb`

### 5) 契约真值更新（阻断项）

- [x] `docs/_tech_graph/_contract_manifest.json`：
  - `type_values` 补齐 5 个 `agent.*`：
    - `agent.step.start`
    - `agent.think`
    - `agent.intent`
    - `agent.step.end`
    - `agent.final`
  - `payload_min_keys_by_type` 补齐上述 5 类的最小键集合

### 6) P0 测试补齐

- [x] `tests/test_unified_chat_backend_v2_agent.py`：补齐 3 个用例
  - `test_v2_rag_empty_gated_fallback`
  - `test_v2_intent_timeout_fallback_v1`
  - `test_v2_agent_disabled_regression`

---

## 验证记录（通过）

```bash
# 1) 手动检查（应命中 5 个 agent.*）
cat docs/_tech_graph/_contract_manifest.json | grep "agent\\."

# 2) 门禁脚本
python tools/tech_graph_contract_check.py
python tools/tech_graph_manifest_check.py

# 3) P0 测试
pytest -q tests/test_unified_chat_backend_v2_agent.py
```

期望结果：
- 门禁脚本：通过
- 测试：`6 passed`

