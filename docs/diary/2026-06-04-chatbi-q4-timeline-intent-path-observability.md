# ChatBI Q4 Timeline 复盘 · Intent 路径可观测性

> **日期**：2026-06-04  
> **关联**：RUNBOOK Q4 · Step1 Prompt · Step2 仲裁/V1 合并 · U1.5 Intent 重试  
> **task**：`chatbi_intent_hints_step2_v1`

---

## 1. 背景

Portfolio 五问 **Q4 逐字**（`11 年经历里 AI Coding 相关成果？`）在 Unified Chat Timeline 上出现两种形态，易误判为「重试三次才成功」或「只有降级路径才出 rag」。

---

## 2. 两次实测对比

| 维度 | Run A（慢 · ~89s） | Run B（快 · ~17s） |
| --- | --- | --- |
| Intent 阶段相对耗时 | ~70s 后才有首条 agent 事件 | ~5s |
| `router.decision` reasoning | Portfolio 语义（LLM 成功） | 同左 |
| `agent.think.thought` | **「Agent 超时，降级到 V1 规则路由。」** | 与 Intent reasoning **一致** |
| 最终工具 | `rag_search` + `cv-online.md` 来源 | 同左 |
| `agent.final.fallback_used` | false | false |

### 2.1 Run A 解读

1. **Intent LLM 已成功**：`router.decision.evidence.agent_reasoning` 为 Portfolio 文案，**不是** Intent `v1_fallback` 固定句「意图识别超时，降级到 V1…」。
2. **`agent.think` 误导**：文案来自 **Agent 软超时**（`AGENT_MAX_LATENCY_MS` 默认 15s），Intent 外呼拖太久（~70s），进工具循环前触发 `agent_soft_timeout_v1`，仅 **覆盖 thought**，工具仍可能为 rag。
3. **U1.5 三次重试**：在 `decide_intent_v2` 内部完成，**旧版 Timeline 无逐次事件**。

### 2.2 Run B 解读

- Intent ~5s 内完成（首轮 LLM 或 **Intent 缓存 hit**）。
- 未触发 Agent 软超时 → `agent.think` 与 `router.decision` 一致。
- **Happy path**：Step1 Prompt 即足够，未依赖 Step2 仲裁/V1 合并。

---

## 3. 三层机制（勿混）

| 层 | 触发 | Timeline 旧表现 | 典型文案 |
| --- | --- | --- | --- |
| **U1.5 Intent 重试** | 单次外呼超时/429/5xx | 不可见 | — |
| **Intent v1_fallback** | 重试耗尽 | 仅 reasoning 变固定句 | 「**意图**识别超时…」 |
| **Agent 软超时** | Intent 总耗时 > `AGENT_MAX_LATENCY_MS` 且未执行工具 | `agent.think` 变固定句 | 「**Agent** 超时…」 |

`agent.llm.* (intent)` 的 `simulated_stream: true` = Intent 结束后 **回放** reasoning，**不是**实时 token 流，也 **不代表**重试次数。

---

## 4. 新增 Timeline 字段（2026-06-04 代码）

实现：`api/intent_agent.py::build_intent_path_obs` · `api/unified_chat.py::_router_agent_evidence`

### 4.1 `agent.intent` / `router.decision.evidence` / `agent.think`（step 1）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `intent_path` | string \| null | `llm` · `llm_retry` · `v1_fallback` · `heuristic` · `prefer_override` |
| `intent_attempt` | int \| null | U1.5 外呼序号（1～3） |
| `hints_arbitration` | object \| null | Step2：`{ applied: true, reason }` 或 null |

### 4.2 仅 `agent.think`

| 字段 | 说明 |
| --- | --- |
| `agent_step_routing` | `intent`（默认）· `agent_soft_timeout_v1` |

### 4.3 已有字段调整

- `cache`（hit/miss）：**始终**从 Intent raw_response 透出（不再仅 debug_router）

---

## 5. 前端读法（Q4）

- `intent_path=llm` + `intent_attempt=1` → 首轮成功（Run B）
- `intent_path=llm_retry` → U1.5 重试过
- `intent_path=v1_fallback` → Intent 层降级
- `agent_step_routing=agent_soft_timeout_v1` → 勿只看 thought 文案
- `hints_arbitration.applied=true` → Step2 仲裁生效

---

## 6. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-04 | Q4 双 run 复盘 + 可观测字段落盘 |

---

## 7. Intent 重试日志（2026-06-04 补充）

- **不**依赖 `DEBUG_INTENT_CACHE`；进程日志级别 ≥ INFO 即输出 `[intent-retry]`。
- 失败将重试：`attempt=N/M failed … will_retry`（WARNING）
- 重试后成功：`success attempt=N/M`（INFO）
- 耗尽：`exhausted … → v1_fallback`（WARNING）
- `DEBUG_INTENT_CACHE` **仍仅**控制 `[intent-cache]` 行。
