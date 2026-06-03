# SPEC — 调研：自研链式编排 vs LangChain（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft`（调研 · 无 task 绑定） |
| **日期** | 2026-06-03 |
| **范围** | 本仓 Chat / Unified Chat / Agent 编排层 |
| **非范围** | 引入 LangChain 库的具体 PR、依赖升级、前端改动 |
| **关联真值** | `docs/spec/v2-agent/SPEC-ChatBI-V2-Agent-Overview.md` · `docs/_tech_graph/00_main.ai.md` · `docs/_tech_graph/10_flow_rag.ai.md` |
| **配对调研** | [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) |

---

## 0. 结论摘要（TL;DR）

1. **整体思路与 LangChain 同类**：均为「分步编排 LLM 应用」——RAG、Tool、Router、Memory、Streaming 等概念一一对应。
2. **本仓未依赖 LangChain 库**：使用 FastAPI handler + `openai` SDK + 自研 `events[]` / SSE 契约 + `ToolRegistry` / `ChatBIAgent`。
3. **最大差异**：你们是 **产品导向的自研链**（ChatBI 契约、SQL Gate、plan token、contract CI）；LangChain 是 **框架导向的通用链**（Runnable/LCEL、标准 Retriever/Tool 抽象、LangSmith 生态）。
4. **务实建议**：短期不必为「对齐 LangChain」而换库；若需 Agent 图化与断点续跑，优先参考 LangGraph 思想（见配对 SPEC），工具层与 RAG 召回可继续自研。

---

## 1. 背景

### 1.1 本仓「链式」指什么

本仓 **没有** 安装 `langchain` / `langchain-core`。所谓「链式调用」指：

- HTTP handler 内 **顺序执行** 多阶段逻辑（rewrite → embed → retrieve → generate 等）；
- 每步 **手动** 组装 prompt、调用 LLM/DB、记录 latency；
- 通过 **`events[]` / SSE** 对外暴露步骤（`tool.call.*`、`agent.*`、`router.decision`）；
- V2 路径下 `ChatBIAgent.run` 为 **手写 ReAct 式循环**（`CHATBI_USE_AGENT` 开关）。

主要代码锚点：

| 链路 | 入口 | 说明 |
| --- | --- | --- |
| Legacy RAG Chat | `api/index.py::chat` | 博客 RAG 流式问答 |
| Unified Chat V1 | `api/unified_chat.py::handle_unified_chat*` | 规则路由 + RAG/Text2SQL 分支 |
| Chain Timeline | `api/chain_chat.py::handle_chain_chat` | Text2SQL 分步 events |
| V2 Agent | `api/agent.py::ChatBIAgent.run` | Intent + 多步 Tool + fallback |
| Tool 层 | `api/tools.py` | `ToolRegistry`、`ToolResult` |

### 1.2 LangChain 在本对比中的含义

指 **LangChain 生态的通用抽象与编排模型**（LCEL、`Runnable`、Retriever、Tool、Agent、Callback），**不限于**是否引入 Python 包。LangGraph 作为 Agent/图编排扩展，在配对 SPEC 中单列。

---

## 2. 概念对齐：自研 ↔ LangChain

| LangChain 常见概念 | 本仓自研对应 | 代码锚点 |
| --- | --- | --- |
| **Chain / LCEL 流水线** | handler 内顺序阶段 + early return | `chain_chat.py`、`index.py::chat` |
| **RAG Chain** | rewrite → embed → hybrid recall → context → LLM | `tools.py::rag_search_execute`、`index.py::chat` |
| **Router / 意图分流** | V1 规则 + V2 LLM Intent | `intent_router.py`、`intent_agent.py` |
| **Tool / Agent** | `ToolRegistry` + `ChatBIAgent` ReAct 循环 | `tools.py`、`agent.py` |
| **Memory** | `AgentMemoryStore` + `rag_conversation_logs` | `agent_memory.py` |
| **Prompt Template** | 各类 `build_*_prompt` / `build_rewrite_llm_messages` | `text2sql_core.py`、`query_rewrite.py` |
| **Retriever** | Text2SQL store search；Supabase vector/FTS RPC | `text2sql_store.py`、`rag_recall_tools.py` |
| **Output Parser / 校验** | `validate_sql_readonly`、`chatbi_sql_gate` | `text2sql_core.py`、`chatbi_sql_gate.py` |
| **Callbacks / Tracing** | 自研 `events[]`、SSE、`rag_conversation_logs` | `unified_chat.py`、`agent.py` |
| **Streaming** | SSE + `_emit_simulated_llm` 伪流式 | `unified_chat.py`、`agent.py` |

**判定**：在 **概念层**，本仓已实现 LangChain 文档中 RAG / Agent 应用的主干模式；差异在 **编排载体** 与 **领域闸口**，不在「有没有 RAG」。

---

## 3. 编排方式对比

### 3.1 自研：命令式（Imperative）

典型模式（Text2SQL chain）：

```text
retrieve → events.append(start) → try generate_sql → events.append(end)
  → if error: return
  → execute_sql → summarize → return JSONResponse(events=...)
```

特征：

- 控制流写在 Python 函数体内（`if/else`、early `return`）；
- 状态分散在局部变量与 `events` 列表；
- 改一步需阅读整段 handler；
- 可观测与业务逻辑 **耦合**（每步手动 `_event(...)`）。

### 3.2 LangChain：组合式（Declarative）

- **LCEL**：`prompt | llm | output_parser` 管道声明组合；
- **Runnable**：统一 `invoke` / `stream` / `batch` 接口；
- **Agent**：Tool 绑定 + LLM 决策环（或 LangGraph 图）；
- **Callback**：与业务链解耦的可观测钩子。

### 3.3 对照表

| 维度 | 自研链 | LangChain |
| --- | --- | --- |
| 控制流位置 | 散落在各 handler / agent 方法 | 链/图对象本身 |
| 复用方式 | 抽函数、复制事件模板 | `Runnable` 管道复用 |
| 单步测试 | mock handler 或 tool 函数 | mock Runnable / node |
| 可视化 | `docs/_tech_graph/` Mermaid | LangSmith / Studio（若接入） |
| 学习成本 | 读 Python 即可 | 需熟悉 Runnable / 版本迁移 |

---

## 4. 抽象层对比

### 4.1 自研：薄框架 + 深领域

| 层 | 实现 |
| --- | --- |
| LLM | 直接 `openai.OpenAI(base_url=siliconflow_base())` |
| Embedding | SiliconFlow + 维度 env；熔断 `llm_execute_with_circuit_breaker` |
| 向量检索 | 自研 hybrid RRF（`hybrid_fusion.py`）+ Supabase RPC |
| Tool 契约 | `ToolResult` + `error_code` / `error_stage` 驱动 Agent fallback |
| 对外语义 | V1 `mode`（rag / text2sql / no_data）与 SSE 事件类型 |

### 4.2 LangChain：厚抽象 + 可插拔集成

| 层 | 典型抽象 |
| --- | --- |
| LLM | `ChatOpenAI`、`BaseChatModel` |
| Embedding | `Embeddings` 接口 |
| 向量检索 | `VectorStore`、`Retriever`、`Document` |
| Tool | `@tool`、`StructuredTool`、`bind_tools` |
| 可观测 | CallbackHandler、LangSmith |

### 4.3 差异本质

- **换后端成本**：LangChain 低（换 Retriever/LLM 实现）；本仓低层与 Supabase/SiliconFlow **硬绑定**，换栈需改代码。
- **领域能力**：本仓 **SQL AST Gate、Prompt Guard、plan_execution_token、contract CI** 等不在 LangChain 默认栈内，换库 **不能删除** 这些逻辑，只能 **搬迁**。

---

## 5. Agent 层对比

### 5.1 自研 `ChatBIAgent`

| 能力 | 实现 |
| --- | --- |
| 决策 | `decide_intent_v2`（LLM）或 `prefer` 强制 |
| 循环 | `for step in range(max_steps)` 手写 |
| 失败路由 | `FailureTypeHandler` 按 `ToolResult.error_code` + gating（如 RAG 空命中 → 有条件才 SQL） |
| 人机协同 | `plan_execution_token`、低置信 `agent.clarify` |
| 对外兼容 | 内部 tool 名 → 外部 V1 `mode`（策略 B，见 V2 总规 §2.2） |

### 5.2 LangChain Agent 栈

| 能力 | 典型实现 |
| --- | --- |
| 决策 | ReAct / tool-calling prompt |
| 循环 | `AgentExecutor` 或 LangGraph `StateGraph` |
| 失败路由 | 默认较简；复杂 gating 需自定义 |
| 人机协同 | LangGraph `interrupt` + checkpointer |
| 对外兼容 | 需自建适配层 |

**判定**：V2 Agent **语义接近** LangChain ReAct Agent + 自定义 Router；**未**采用 LangGraph 式显式 State / checkpoint。

---

## 6. 可观测与契约

### 6.1 自研：SSE 契约为第一公民

- 事件类型与 payload 最小字段：**`_contract_manifest.json`** 真值；
- CI：`tools/tech_graph_contract_check.py`；
- 前端 Timeline 依赖固定 `type`（`agent.step.start`、`tool.call.end` 等）；
- 每步 **显式** `events.append` / `emit(...)`。

### 6.2 LangChain：Callback / Tracer 为主

- 默认面向开发者调试与 LangSmith；
- 事件结构随版本变化；
- 对接本仓 Timeline 需 **映射层**（LangGraph `astream_events` → 现有 SSE 类型）。

**判定**：这是与 LangChain **最大的工程差异**——你们为 ChatBI **产品化了** 可观测契约；LangChain 默认可观测 **不等价** 于你们的 contract CI。

---

## 7. 路由层：本仓特有三层决策

| 层级 | 机制 | 文件 |
| --- | --- | --- |
| L1 | V1 规则路由（关键词 + DDL/FTS 证据） | `intent_router.py` |
| L2 | V2 LLM Intent | `intent_agent.py` |
| L3 | Agent 内工具失败二次路由 | `agent.py`（`FailureTypeHandler`） |

LangChain 常见做法为 **单一 RouterChain 或 LangGraph 条件边**。本仓因 **历史兼容**（`prefer`、`CHATBI_USE_AGENT`、V1 mode）路由路径更多，但也更贴合现有前端与日志统计。

---

## 8. 本仓有、LangChain 不自带的能力

| 能力 | 说明 | 锚点 |
| --- | --- | --- |
| ChatBI SQL AST Gate | 租户/表白名单、变更 SQL 拦截 | `chatbi_sql_gate.py` |
| Prompt Guard | 任何上游 LLM 前的 query 扫描短路 | `unified_chat.py` |
| Plan Preview + Token | Text2SQL/RAG 执行前用户确认 | `chatbi_plan_token.py`、`agent.py` |
| Hybrid RRF + structured date recall | 博客 RAG 特化召回 | `hybrid_fusion.py`、`rag_recall_tools.py` |
| Grounding prefix | 多轮 intent 上下文 | `text2sql_grounding.py` |
| Circuit breaker | SiliconFlow 熔断 | `rag_env.py` 等 |
| 图谱 + contract CI | 架构与 SSE 契约门禁 | `docs/_tech_graph/`、`tools/tech_graph_*` |

引入 LangChain **不会自动获得** 上表能力；迁移时须 **原样保留或封装为自定义 Runnable/Tool**。

---

## 9. 依赖与运维

| 项 | 自研链 | LangChain |
| --- | --- | --- |
| 核心依赖 | `fastapi`、`openai`、Supabase 客户端 | `langchain-core` + integration 包 |
| 升级面 | 较小（OpenAI SDK、自研模块） | 大版本 API 变动需跟进 |
| 团队技能 | Python + 本仓契约 | Runnable / Agent / LangGraph 模型 |
| 调试 | 断点 handler / tool | callback / graph state |
| 镜像体积 | 无 LangChain 树 | 依赖树更大 |

---

## 10. 细粒度概念映射（便于讨论是否引库）

| 自研 | LangChain 近似 | 备注 |
| --- | --- | --- |
| `_event` / `_agent_chain` | Custom Event / `dispatch_custom_event` | 须映射到 contract 字段 |
| `ToolResult` | `ToolMessage` + 自定义 error 字段 | `error_code` 为 fallback 真值 |
| `ToolRegistry` | Tool 列表 + `bind_tools` | 参数 schema 在 `Tool.parameters` |
| `AgentMemoryStore.load` | `ChatMessageHistory` / checkpointer | DB 真值在 Supabase |
| `decide_intent_v1` | RouterChain / 规则链 | 关键词 + 证据 |
| `decide_intent_v2` | LLM Router | JSON tool 决策 |
| `FailureTypeHandler` | 自定义 conditional edge | gating 表在 V2 总规 §2.4 |
| `handle_unified_chat_stream` | `astream` + SSE 适配 | 非 token 级时伪流式 |
| `rag_search_execute` | RAG chain / Retriever + LLM | 内部多步未暴露为独立 Runnable |

---

## 11. 若将来引入 LangChain 的适配工作（预览 · 非承诺）

> 本节仅供选型讨论；**无 task、无排期**。

1. **Tool 层**：`Tool.execute` → LangChain Tool / LangGraph node；保留 `error_code` 语义。
2. **SSE 映射**：LangGraph `astream_events` → 现有 `_contract_manifest` 事件类型。
3. **Fallback 逻辑**：搬迁 `FailureTypeHandler` + §2.4.1 gating，不可依赖默认 Agent。
4. **RAG 召回**：评估 Retriever 抽象收益；hybrid RRF 可能 **保留自研**。
5. **双路径迁移**：V1 unified + V2 agent + legacy chat 渐进；Feature flag 灰度。
6. **文档/CI**：更新 `_tech_graph`、contract manifest、pytest 快照。

更完整 **LangGraph 向** 工作清单见配对 SPEC §3–§10。

---

## 12. 开放问题（待后续 task 冻结）

| ID | 问题 |
| --- | --- |
| Q-1 | 是否引入 `langchain-core` 仅作 Runnable 包装，还是零依赖继续自研？ |
| Q-2 | Agent 路径是否优先 LangGraph，而 RAG/Text2SQL 保持函数调用？ |
| Q-3 | SSE contract 是否允许新增 graph 级事件，还是严格映射到现有 type？ |
| Q-4 | Checkpointer 与 `rag_conversation_logs` 双写还是单一真值？ |

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-03 | 初版 draft：概念对齐、差异维度、映射表、开放问题 |
