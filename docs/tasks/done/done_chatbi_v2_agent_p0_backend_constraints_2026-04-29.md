# ChatBI V2 Agent（P0 后端）— 11 点约束确认与落地计划（问答回溯）

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本文件无 Wiki 增量（2.19 lint-wiki-delta） |


> **状态**：done（2026-04-29）  
> **归档路径**：`docs/tasks/done/done_chatbi_v2_agent_p0_backend_constraints_2026-04-29.md`  
> **关联任务**：`docs/tasks/active/task_chatbi_v2_agent_p0_backend.md`  
> **目的**：把用户在对话中明确的实现约束固化，作为后续落地/代码审查/测试验收的唯一依据。

---

## 0. 总体原则（本问答的强约束）

- 必须实现 **多步 ReAct 循环**，并且至少支持 **2 个工具串行调用**。
- `CHATBI_USE_AGENT=false` 时必须保持 **V1 行为不变**（事件类型/ payload/ mode 语义一致）。
- `agent.*` 事件类型与 `payload 最小键集合` 必须满足 `_contract_manifest.json` 的静态契约门禁。
- fallback / gating / memory 落库规则必须与用户给定的语义一致。

---

## 1. ReAct 最大步数与偏好设置（问题 1）

**确认值**

- `AGENT_MAX_STEPS = 5`（固定；不支持单步 Agent）
- `AGENT_MAX_LATENCY_MS = 15000`（整体超时预算 15s）
- `INTENT_MIN_CONFIDENCE = 0.6`
- `CHATBI_V2_INTENT_LLM = true`（默认开启 LLM 意图识别；_heuristic_decide 仅用于超时/异常降级）
- `CHATBI_USE_AGENT = false`（默认全局开关；true 才走 V2）

**实现落地点**

- `api/agent.py` 必须以 `AGENT_MAX_STEPS=5` 控制 `for step in range(max_steps)` 的上界。
- 当 LLM 意图或工具执行失败时，不能“停在单步”；必须进入后续 ReAct 步（直到 final 或达到 max_steps）。

---

## 2. 单步 vs 多步 Agent（问题 2）

**确认点**

- 必须支持多步 ReAct。
- “单步 Agent”被视为不满足验收：它只是 LLM 选工具的 V1，不等同于 Agent。

**示例约束（来自问答原文）**

- `销售额下降原因`
  - Step 1: `text2sql_query → 查到数据`
  - Step 2: `rag_search → 分析原因`
  - Step 3: `综合分析 → 最终回答`

---

## 3. LLM 意图识别开关（问题 3）

**确认点**

- 生产/验收：`CHATBI_V2_INTENT_LLM=true`
- 本地调试允许临时 false，但测试用例必须覆盖 true
- 默认开启 LLM 意图识别；`_heuristic_decide` 仅作为超时/异常降级路径

**实现落地点**

- `api/intent_agent.py` 的默认行为必须是：未显式关闭时走 LLM，再由超时/异常降级到启发式。

---

## 4. `AGENT_MAX_STEPS = 5`（问题 4）

**确认点**

- 即使 `SPEC-ChatBI-V2-ReAct-Loop.md` 曾写 10，总规修订为 5。

**实现落地点**

- 代码默认值必须从 `10` 修正到 `5`（或完全以 env 读取并保证 env 默认就是 5）。

---

## 5. `router.decision` 保留（问题 5）

**确认点**

- V2 中保留 `router.decision`，但语义替换为 “Agent 初始决策”。
- 时序要求：
  - `chain: router.decision   # Agent 初始决策（替代规则决策）`
  - 后接 `agent.step.start → agent.think → ...`
- payload 结构与 V1 一致：
  - `final_mode` 必填
  - `rule_hits` 可以为空或用 `agent_reasoning` 替代

---

## 6. 事件时序：`agent.intent` 只在 Step 1 出现（问题 6）

**确认表述**

- Step 1：`agent.step.start → agent.intent（Intent Agent 决策）→ agent.think → tool.call.start`
- Step 2+：`agent.step.start → agent.think（无 intent）→ tool.call.start`

---

## 7. `fallback_used` 计算逻辑（问题 7）

**确认规则**

- `agent.final.payload.fallback_used = True` 当且仅当：
  - 低置信度时使用了预设 fallback；或
  - tool 失败后根据 `error_code` 换了工具；
  - 否路顺利未换工具：为 `false`

**实现落地点**

- `api/agent.py` 必须保存 “Intent 原始选择工具” 与 “实际执行工具列表”，做对比得出 fallback_used。

---

## 8. Memory save 复用 V1 写入逻辑（问题 8）

**确认规则**

- 不要每步 insert。
- 一轮对话结束后 upsert，复用 `unified_chat.py` 的写入逻辑，只多写两个 JSONB 字段：

```json
{
  "session_id": "<session_id>",
  "query": "<query>",
  "response": "<answer>",
  "mode": "<mode>",
  "agent_steps": {...},
  "tool_results": {...}
}
```

---

## 9. 意图缓存 P0 预留接口（问题 9）

**确认点**

- P0 阶段可以不做缓存实现，但代码中必须预留 `_intent_cache: LRUCache = ...` 这样的结构。

---

## 10. 模型分级（问题 10）

**确认规则**

- Intent：Qwen-Turbo（`INTENT_LLM_MODEL`）
- Agent 决策：DeepSeek-V3（`AGENT_LLM_MODEL`）
- Tool 执行：复用 V1（`SILICONFLOW_CHAT_MODEL`）
- `INTENT_LLM_MODEL = os.getenv("INTENT_LLM_MODEL", "Qwen/Qwen2.5-7B-Instruct")`

**实现落地点**

- `api/intent_agent.py` LLM 调用必须使用 `INTENT_LLM_MODEL`。

---

## 11. P0 最小测试集（问题 11）

**确认清单**

- 事件流测试：3 场景
  - 单工具
  - 多工具
  - Fallback
- 回归测试：V1 全量
  - 覆盖 `CHATBI_USE_AGENT=false`
- 意图测试：10 条核心用例（后续扩展到 60 条）

---

## 下一步优先级（你给出的实现顺序）

1. `api/agent.py` — ReAct + FailureTypeHandler + 事件回调（严格时序/字段/ fallback_used）
2. `api/unified_chat.py` — V2 路径接入 + `CHATBI_USE_AGENT` 开关
3. Supabase SQL 字段 + `_contract_manifest.json`
4. 跑通 `contract_check + manifest_check`
5. P0 最小测试（3 场景事件流 + 回归）

