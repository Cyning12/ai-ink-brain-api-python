# SPEC: ChatBI V2 —— Gap Checklist（缺口清单）

> 对齐对象：`docs/spec/v2-agent/SPEC-ChatBI-V2-*.md`  
> 维护说明：本文件用于记录「现有实现 vs V2 规格」的缺口、优先级与建议改动点，避免实现时遗漏关键契约/回退/记忆要求。  
> **读法**：下方 **「实现对齐快照」表为当前真值**；各 `## P0` 起章节保留**历史缺口原文**便于审计，**不得以旧 § 文字覆盖上表**。

---

## 实现对齐快照（2026-05-07 审计 · 全仓对照 · 与 `SPEC-ChatBI-V2-Agent-Overview.md` §7.4 一致）

以下条目在**下文各节**仍保留「原始缺口描述」便于读 spec；**本表仅标当前代码 / 部署 / 测试侧结论**；**深度回归操作**见 Overview **§7.5**。

| 原 § | 主题 | 当前结论 |
|------|------|----------|
| P0 §1 | `agent.*` 写入 `_contract_manifest.json` | **已落地**：`docs/_tech_graph/_contract_manifest.json` 含 `agent.step.start` / `agent.think` / `agent.intent` / `agent.step.end` / `agent.final` 及 `payload_min_keys_by_type`。 |
| P0 §2 | `rag_conversation_logs` 增加 `agent_steps` / `tool_results` | **已落地（SQL）**：`supabase/sql/create_rag_conversation_logs.sql` 已含对应 `jsonb` 列；**生产库是否已迁移**以实际 Supabase 为准（全量对照「运维」行）。 |
| P0 §3 | `intent_agent` / `agent` / `tools` / `agent_memory` 模块 | **已落地**：`api/intent_agent.py`、`api/agent.py`、`api/tools.py`、`api/agent_memory.py`；P1-D 已迭代 Intent Prompt。 |
| P0 §4 | `unified_chat` 接入 V2 + `CHATBI_USE_AGENT` | **已落地**：JSON + SSE 路径；前端 `ai-ink-brain` 已部分消费 `agent.*` 类型（见 Overview §7.4）。 |
| P1 §5 | ToolResult + `error_code` + fallback | **部分落地**：`FailureTypeHandler` + gating 已实现；**与 Overview §2.4 逐条等价**依赖 **§7.5 L5** 矩阵回归，非仅单元测存在即闭合。 |
| P1 §6–§7 | ReAct 事件时序、reasoning 分级 | **需持续对照**：以 `_contract_manifest.json` + **L4 实 SSE** 为准。 |
| P2 §8 | 多步 fallback / `agent.*` E2E 覆盖 | **部分**：`test_unified_chat_backend_v2_agent.py` 等存在；**Gap 原文所列「完全缺失」已不再成立**，仍缺 **L5/L6** 级全矩阵与跨仓报告。 |
| P2 §9 | env 默认值与 spec 一致 | **部分**：`PROJECT_CONFIG` / `.env.example` 已对齐 V2 开关；**纸面 P50/P95** 与线上延迟仍不一致（见 Overview §7.2）。 |

---

## P0（阻断项：必须先补齐，否则契约/验收无法通过）

### 1) SSE 契约真值缺失：`agent.*` 未写入 `_contract_manifest.json`

**缺口**  
当前 `docs/_tech_graph/_contract_manifest.json` 的 `sse.chain.type_values` 仅包含 V1 事件类型：`meta/router.decision/tool.call.start/tool.call.end/rag.query_expand/rag.sources/sql.result/assistant.message/latency/error`，未包含 V2 新增的：
- `agent.step.start`
- `agent.think`
- `agent.intent`
- `agent.step.end`
- `agent.final`

**建议改动点**  
- 修改 `docs/_tech_graph/_contract_manifest.json`：补齐 `type_values` 与对应的 `payload_min_keys_by_type`

**依据**  
V2 “策略 B”要求新增事件必须同步更新 `_contract_manifest.json`（否则 CI/门禁校验失败）。

---

### 2) 记忆存储缺字段：`rag_conversation_logs` 无 `agent_steps/tool_results`

**缺口**  
当前 `supabase/sql/create_rag_conversation_logs.sql`（以及表结构）未包含 V2 记忆管理需要的：
- `agent_steps JSONB`
- `tool_results JSONB`

**建议改动点**  
- 更新 Supabase SQL（或新增迁移）：对 `public.rag_conversation_logs` 增加 JSONB 字段。

**依据**  
V2 记忆管理设计要求最小可用记忆落在 `rag_conversation_logs.agent_steps/tool_results`。

---

### 3) V2 核心模块尚未落地：缺 `intent_agent/agent/tools/agent_memory`

**缺口**  
当前代码库仍以 V1 路由（`api/intent_router.py` + `api/unified_chat.py` 固定分支）为主，缺少 V2 规定的新增模块/抽象：
- `api/intent_agent.py`
- `api/agent.py`
- `api/tools.py`
- `api/agent_memory.py`

**建议改动点**  
- 新增模块并按 V2 总规组织职责（Intent Agent：工具选择 + 置信度；Agent：ReAct 循环；Tool：统一接口与 error_code；Memory：持久化与压缩策略）。

---

### 4) `unified_chat.py` 未接入 V2 Agent 路径与 `agent.*` 事件

**缺口**  
当前 `api/unified_chat.py` 输出的 SSE 事件仍停留在 V1 类型（`router.decision/tool.call.start/sql.result/rag.sources/assistant.message/latency/error`），没有 `agent.*` 事件流，也没有 `CHATBI_USE_AGENT`（或同等）分流。

**建议改动点**  
- 在 `api/unified_chat.py`/`unified_chat_stream_route` 增加 V2 主路径与 fallback 到 V1 规则路由。
- Agent 完成时 emit 事件：`agent.step.start/think/intent/step.end/final`
- 对外仍输出 V1 mode 语义：`rag/text2sql/no_data`

---

## P1（行为正确性：fallback / gating / 错误恢复必须按 error_code 实现）

### 5) Tool 失败类型分类与 fallback 策略未实现

**缺口**  
V2 要求 ToolResult 必须携带：
- `success`
- `error_code`
- `error_stage`

并由 Agent 按失败类型映射进行重试/换工具/降级。

**建议改动点**  
- 在 `api/tools.py` 实现统一 ToolResult 与错误码集合。
- 在 `api/agent.py` 或 `api/intent_agent.py` 实现 `FailureTypeHandler`：
  - SQL 生成失败：重试 1 次 → 仍失败换 `rag_search`
  - SQL 执行失败：换 `rag_search`
  - SQL 无数据：直接回答“未查到数据”，不换工具
  - RAG 无命中：`gated` 决策后才允许换 `text2sql_query`
  - RAG 不确定：换 `direct_answer` 或追问
  - LLM 超时：降级到 V1 规则路由

**关键约束（必须有）**  
`RAG_RETRIEVE_EMPTY` → fallback 到 SQL 必须满足结构化聚合意图 gating，否则不得盲目查库。

---

### 6) ReAct Loop 事件时序缺失/不符合 spec

**缺口**  
V2 事件时序规定每步需要输出至少：
`agent.step.start → agent.think → agent.intent → tool.call.start/end → agent.step.end`  
并最终 `agent.final`。

**建议改动点**  
- 在 `api/agent.py` 实现严格的 step 编号与 payload 结构，确保与 `_contract_manifest.json` 一致。

---

### 7) reasoning 输出分级缺失

**缺口**  
V2 要求用户级只输出 `agent.think.payload.thought`（1-2 句摘要）；完整 reasoning 进日志/管理员 debug 接口。

**建议改动点**  
- 事件 payload 中仅放摘要
- 内部级 reasoning 走日志，不进入 SSE。

---

## P2（工程化：测试、可观测性、env/默认值一致性）

### 8) V2 测试覆盖缺失

**缺口**  
当前测试主要覆盖 V1（`test_unified_chat_backend_v1.py` 等）。缺少 V2：
- `agent.*` 事件出现与 payload 最小键校验
- 多步 fallback / gating 行为用例

**建议改动点**  
- 新增 `tests/test_chatbi_v2_*`：
  - SSE contract 校验（按 `_contract_manifest.json`）
  - 失败类型 fallback 单元/集成测试

---

### 9) env 默认值与 spec 不一致风险

**缺口**  
spec 中如 `INTENT_MIN_CONFIDENCE=0.6`、Intent 超时 3s、`AGENT_MAX_STEPS` 等有默认与推导目标；当前实现与 spec 未统一来源。

**建议改动点**  
- 统一默认值从同一 env 读取，并与 spec 保持一致。

---

## 建议下一步（相对当前快照）

1. **发布前**：执行 Overview **§7.5** 中 **L0 + L3**；若对外承诺 Intent 质量则加 **L1**。
2. **宣称与 §2.4 完全等价前**：执行 **L5**（`error_code` 矩阵）并归档用例 / 日志。
3. **宣称延迟 SLA 前**：执行 **L2**，并在 Overview §7.2 或发布说明中写明与纸面目标的差距及缓解（超时、`v1_fallback`、模型选型）。
4. **生产 DB**：确认迁移与代码版本一致后，再在 §7.4 将「记忆 / 落库」标为已对齐。
5. **L4–L7 操作细则**：见 Overview **§7.5.3–§7.5.6**（SSE、`curl`、跨仓、运维核对）；**L0–L3 验收归档**见 `docs/diary/2026-05-07-l0-l3-regression-acceptance.md`（`git add -f`）。

