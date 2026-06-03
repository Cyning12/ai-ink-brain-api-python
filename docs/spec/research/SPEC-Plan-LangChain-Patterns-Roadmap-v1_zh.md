# SPEC — 计划：LangChain/LangGraph 思想借鉴 · 自研编排改进路线图（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft`（需求计划 · **无 task 绑定**） |
| **日期** | 2026-06-03 |
| **文档性质** | **后续需求 / 排期输入**；非对比调研正文 |
| **前置决策** | [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §4.3（D-1～D-5 已冻结） |
| **关联调研** | [`SPEC-Research-SelfChain-vs-LangChain-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangChain-v1_zh.md) · [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) |
| **非范围** | 引入 LangChain/LangGraph 库；修改现有 `unified_chat.py` 行为；生产访客暴露 Graph 入口（见 D-4） |

---

## 0. 结论摘要（TL;DR）

1. **借思想、不借依赖**（D-1）：用自研 `StateGraph`、统一节点 IO、边表驱动 fallback，不引入 `langchain-core` / `langgraph`。
2. **P0 打共享层地基**（events / State / Runnable 式 IO），**P1 在 Graph 新路由落地 MVP**，旧 Unified 仅逐步 import 共享模块。
3. **领域层保留自研**：SQL Gate、Prompt Guard、hybrid RRF、contract CI — LangChain 不提供，不得为「对齐框架」而删。
4. **低优先 / 不建议**：VectorStore 包装、默认 AgentExecutor、Legacy `/api/py/chat` 整链 LCEL 化、Graph 路径接入 V1 规则路由。
5. **`agent.py` 瘦身**：P0 抽模块（行为不变）→ Graph 接棒 → parity 后 `run()` 变壳；**MVP 前不重写** `ChatBIAgent.run` 语义（D-2）。

---

## 1. 背景与定位

### 1.1 本文档用途

- 从 LangChain / LangGraph **生态实践**中筛选 **值得自研吸收** 的模式；
- 给出 **优先级（P0～P3）** 与 **改动范围**（共享层 / Graph 新路由 / 旧 Unified / Legacy）；
- 作为 **开 task、排 RECENT、拆 PR** 时的输入，**不**替代对比调研 SPEC 正文。

### 1.2 与冻结决策的对齐

| 决策 | 对本计划的约束 |
| --- | --- |
| **D-1 自研** | 下文全部为自研实现，无新增 LangChain 依赖 |
| **D-2 并行 Graph** | P0～P2 主战场 = 新 `/api/py/unified/chat/graph*`；旧 Unified **不改行为** |
| **D-3 方案 A** | Intent 超时 → `direct_answer` + error/think；边表须覆盖 |
| **D-4 前端控入口** | 后端 Graph 常开；MVP 前仅 local/dev 联调 |
| **D-5 SSE superset** | P0 Callback 层预留 `graph.*` 新 type + contract 登记 |

---

## 2. 总原则

| 原则 | 说明 |
| --- | --- |
| **借思想，不借依赖** | 学 State/边/Callback/Structured Output，不引库 |
| **领域层不动** | ChatBI 闸口与 RRF 召回保持自研 |
| **先共享层，再 Graph** | P0 抽模块；Graph 消费；旧路径渐进 import |
| **RAG 召回低优先** | LangChain `Retriever` 抽象对 hybrid RRF **收益小** |

---

## 3. 优先级总表

| 优先级 | LangChain/LangGraph 概念 | 本项目改进点 | 范围 | 建议阶段 |
| :---: | --- | --- | --- | :---: |
| **P0** | LangGraph **State + 条件边** | 显式 `ChatBIState`、边表驱动 fallback | 共享层 + Graph 新路由 | MVP 前 |
| **P0** | **Callback** 与业务解耦 | 抽 `chatbi_events.py`；节点只改 state | 全路径（Graph 先用） | MVP 前 |
| **P0** | **Runnable** 统一 IO | `(state) → partial_state` + `error_code` | `tools.py` + Graph 节点 | MVP 前 |
| **P0** | **`agent.py` 抽模块瘦身** | events / models / failure 迁出；`run()` 暂留 | `api/agent.py` → 共享层 | MVP 前 |
| **P1** | **Structured Output / Parser** | Intent、SQL 强类型解析 → `error_code` | `intent_agent` · `text2sql_core` | Graph MVP |
| **P1** | **RunnableConfig** 上下文传播 | `run_id` / `session_id` / `principal` 进 State | 共享 State | Graph MVP |
| **P1** | **Router** 单一决策点 | 一个 route 节点 + 条件边 | **仅 Graph** | Graph MVP |
| **P1** | **Tool schema**（bind_tools 思想） | `Tool.parameters` → Intent prompt 自动生成 | `tools` + `intent_agent` | Graph MVP |
| **P2** | **Interrupt / HITL** | plan preview、clarify 图暂停 + resume | **仅 Graph** | MVP 后 |
| **P2** | **Checkpointer + thread_id** | 运行态断点；与 DB 历史分工（Q-4） | **仅 Graph** | MVP 后 |
| **P2** | **Subgraph** | Text2SQL 内 retrieve→…→summary | Graph 内 `tool_text2sql` | 可选 |
| **P2** | **RunnableWithFallbacks** 式降级 | FailureTypeHandler **边表化** | Graph → 可选回灌 Agent | MVP 后 |
| **P3** | **Prompt Template** 组合 | `build_*_prompt` 可组合片段 | 全 LLM 点 | 按需 |
| **P3** | **Retriever** 接口 | `search(query)→hits` 抽象 | `rag_recall_tools` | 换后端时 |
| **P3** | **LCEL 并行** | Intent 阶段并行 evidence | Graph intent | 性能优化 |
| **P3** | **Document** 模型 | hit → context 字段统一 | RAG context | 低 |
| **—** | VectorStore、AgentExecutor、LangSmith | **不建议** | — | — |

---

## 4. P0 — MVP 前必做（Graph 地基 + 共享层）

### 4.1 State + 条件边（最高 ROI）

| 项 | 内容 |
| --- | --- |
| **借鉴** | LangGraph 显式 State、条件边、可单测控制流 |
| **改进** | `ChatBIState` + `EDGE_TABLE[error_code] → next_node`；`FailureTypeHandler` 逻辑数据化 |
| **范围** | 新建 `api/chatbi_state.py`（或 `api/graph/state.py`）、边表 YAML/模块；**Graph 新路由消费** |
| **不做** | 改写 `unified_chat.py`；RAG hybrid 内部图化 |
| **验收** | 边表单测覆盖 V2 总规 §2.4 主要 `error_code` |

### 4.2 Callback 与业务解耦

| 项 | 内容 |
| --- | --- |
| **借鉴** | LangChain CallbackHandler：观测与业务分离 |
| **改进** | 抽 `api/chatbi_events.py`（`_event` / `_agent_chain` / 未来 `graph.*`） |
| **范围** | Graph 节点通过 `on_node_start/end` 发 SSE；旧路径 **逐步 import**，不一次性改 |
| **验收** | Graph 节点函数内 **无** 直接 `events.append` |

### 4.3 Runnable 统一 IO（不引库）

| 项 | 内容 |
| --- | --- |
| **借鉴** | Runnable `invoke` 输入输出契约 |
| **改进** | `run_tool_node(state) → partial_state`；Tool 外层包装，保留 `ToolResult` |
| **范围** | `tools.py` 三 Tool + Graph 节点；旧 `ChatBIAgent` 仍调原 `Tool.execute` |
| **验收** | 每个节点可 mock State 单测 |

### 4.4 `agent.py` 瘦身（P0 抽取 · P1 Graph 接棒 · P2 变壳）

> 锚点：`api/agent.py`（当前 ~1342 行）。LangChain 里编排、Callback、Router、Fallback 分属不同模块；本仓五类职责堆在同一文件。

#### 4.4.1 现状职责块

| 块 | 内容 | 约行数 | 迁出目标 |
| --- | --- | ---: | --- |
| SSE / 事件 | `_agent_chain`、`_emit_simulated_llm`、contract 锚点 | ~130 | `api/chatbi_events.py` |
| 视图模型 | `AgentStepView` / `AgentRunView` / `AgentFinalView` | ~50 | `api/chatbi_agent_models.py` |
| 失败路由 | `FailureTypeHandler` | ~115 | `api/chatbi_failure.py`（后改边表） |
| 辅助 | `_has_aggregation_signals`、failure digest、env helper | ~80 | gating 模块 / 边表 |
| **`ChatBIAgent.run`** | intent + clarify/plan + 循环 + 大量 emit | **~900+** | `api/graph/*` 编排；`run()` 最终变壳 |

#### 4.4.2 阶段策略（对齐 D-2）

| 阶段 | 对 `agent.py` 的操作 | 文件体量目标 | 行为 |
| --- | --- | --- | --- |
| **P0 抽取** | 迁 events / models / failure；`agent.py` 改 import | ~900 行（`run()` 仍大） | **不变** |
| **P1 Graph MVP** | 新 `StateGraph` 参考 `run()` 语义；Graph 为薄编排 | 新模块薄；agent 停止膨胀 | 旧 Unified 仍调 `ChatBIAgent` |
| **P2 parity 后** | `run()` → 调 `run_agent_graph()` 或 legacy 分支 | **~150–250 行** 壳 | Graph parity 通过后可选切换 |
| **禁止** | MVP 前重写 / 删 `run()` 逻辑 | — | 违反 D-2 |

#### 4.4.3 P0 目标文件布局

```text
api/chatbi_events.py          ← _agent_chain, _emit_simulated_llm, contract anchors
api/chatbi_agent_models.py    ← AgentStepView, AgentRunView, AgentFinalView
api/chatbi_failure.py         ← FailureTypeHandler（暂保留 class）
api/agent.py                  ← ChatBIAgent + run()（import 上述模块）
```

#### 4.4.4 P1 目标文件布局（Graph 接棒）

```text
api/graph/state.py            ← ChatBIState
api/graph/nodes/*.py          ← intent, tool_*, clarify, finalize
api/graph/runner.py           ← StateGraph.invoke / astream
api/unified_chat_graph.py     ← 薄 HTTP handler
```

#### 4.4.5 Legacy vs Graph 失败边（D-3）

| 路径 | `LLM_API_TIMEOUT` 行为 |
| --- | --- |
| **旧 `agent.py` / Unified** | 保留 V2 总规：降级 `decide_intent_v1`（`FailureTypeHandler` 内） |
| **Graph 边表** | **方案 A**：`direct_answer` + error/think（D-3） |

抽取 `chatbi_failure.py` 时建议 **分表** 或分函数：`failure_edges_legacy()` / `failure_edges_graph()`，避免一套边表两种语义。

#### 4.4.6 验收

| 项 | 标准 |
| --- | --- |
| P0 抽取 PR | `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿；`agent.py` 行数下降 |
| 契约锚点 | `_CONTRACT_ANCHOR_*` 仍可被 `tech_graph_contract_check` 扫描（迁出后更新扫描路径或保留 re-export） |
| Graph MVP | 新路由 parity 测 vs 旧 Agent 关键路径 diff 文档 |

---

## 5. P1 — Graph MVP 核心（与 D-2 新路由同期）

### 5.1 Structured Output / Output Parser

- Intent、SQL JSON 块 → Pydantic/dataclass；失败映射 `INTENT_PARSE_FAIL` / `SQL_GEN_SYNTAX`。
- **范围**：Graph 路径先上；parity 后可回灌 `intent_agent.py`。
- **旧 Unified**：可选，非 MVP 阻塞项。

### 5.2 RunnableConfig 式上下文

- State 显式携带 `run_id`、`session_id`、`principal`；减少 `chatbi_request_ctx` 隐式依赖。
- **范围**：Graph 全链 + persist 节点。

### 5.3 Router 单一决策点

- Graph 内：`intent_decide → clarify_gate | tool_* | plan_preview | tool_direct`（D-3 方案 A）。
- **范围**：**仅 Graph**；handler 不再嵌套大段 if。

### 5.4 Tool schema

- `ToolRegistry` 生成 Intent system 工具说明；参数 JSON Schema 与 registry 同源。
- **范围**：Graph + 旧 Agent **共用** registry。

### 5.5 P1 交付物清单

| 交付物 | 说明 |
| --- | --- |
| 新路由 | `POST /api/py/unified/chat/graph` · `.../graph/stream`（Q-8 定名 + manifest） |
| StateGraph MVP | intent → tool 环 + Failure 边表 |
| SSE | 现有 type parity + 可选 `graph.*`（D-5） |
| Intent 超时 | 方案 A 单测 + contract 快照 |
| 共享模块 | `chatbi_events` · `chatbi_state` · 边表 |

---

## 6. P2 — MVP 后（LangGraph 相对链式最大增量）

### 6.1 Interrupt / Human-in-the-loop

- plan preview、clarify → 图 `interrupt` + resume；与 `plan_execution_token` 并存过渡期（Q-5）。
- **范围**：**仅 Graph**。

### 6.2 Checkpointer

- `thread_id = session_id`；内存实现即可 MVP+；与 `rag_conversation_logs` 分工见 Q-4。
- **范围**：**仅 Graph**。

### 6.3 Subgraph（Text2SQL）

- `tool_text2sql` 内子图：retrieve → sql → gate → execute → summary。
- **范围**：Graph 内；**不改** `chain_chat.py` 对外 API。

### 6.4 边表化 Fallback

- 配置表驱动：`RAG_RETRIEVE_EMPTY + gating → text2sql | direct`（§2.4.1）。
- **范围**：Graph 先行；验证后可回灌 `FailureTypeHandler`。

---

## 7. P3 — 按需 / 低优先

| 项 | 触发条件 | 范围 |
| --- | --- | --- |
| Prompt Template 组合 | 多语言 / A/B / prompt 膨胀 | 全 LLM 调用点 |
| Retriever 抽象 | 换向量后端或多 Retriever 组合 | `rag_recall_tools` |
| LCEL 并行 evidence | Intent P95 超标 | Graph intent 节点 |
| Document 模型 | sources 契约大改 | RAG context build |

---

## 8. 不建议吸取（明确排除）

| 项 | 理由 |
| --- | --- |
| VectorStore / 标准 Retriever 栈 | hybrid RRF + structured date 已深度定制 |
| 默认 AgentExecutor / create_react_agent | 无 SQL gating、plan preview、contract SSE |
| ChatOpenAI 替换 OpenAI SDK | SiliconFlow + 熔断已稳定 |
| LangSmith 默认追踪 | 已有 `_contract_manifest` + Timeline |
| Legacy `/api/py/chat` 整链 LCEL 化 | 风险大、Portfolio 依赖稳定 |
| Graph 路径 V1 规则路由 | D-3 已冻结不接入 |
| 后端 env 关停 Graph | D-4 已冻结后端常开 |

---

## 9. 范围矩阵

```text
                    │ 共享层          │ Graph 新路由      │ agent.py        │ 旧 Unified      │ Legacy /chat
────────────────────┼─────────────────┼───────────────────┼─────────────────┼─────────────────┼──────────────
P0 State/Events/IO  │ ✅ 必做         │ ✅ 消费           │ ✅ 抽模块瘦身   │ 🔶 import 共享  │ ❌ 暂不
P1 Parser/Router    │ ✅ tools/intent │ ✅ 主战场         │ 🔶 停止膨胀     │ 🔶 仍调 Agent   │ ❌ 暂不
P2 interrupt/子图   │ 🔶 接口预留     │ ✅ 主战场         │ ✅ run() 变壳   │ ❌              │ ❌
P3 Retriever/Prompt │ 🔶 按需         │ 🔶 按需           │ —               │ ❌              │ ❌
```

图例：✅ 必做 · 🔶 可选/渐进 · ❌ 本阶段不做

---

## 10. 建议 Task 拆分（开 task 时引用）

| Task ID | 优先级 | 主题 | 依赖 |
| --- | --- | --- | --- |
| **Task-A** | P0 | `chatbi_events` + `ChatBIState` + 边表草案 + Graph 骨架路由 | D-1～D-5 |
| **Task-A′** | P0 | **`agent.py` 抽模块瘦身**（events / models / failure 迁出；行为不变） | 可与 Task-A 同 PR 或紧接 |
| **Task-B** | P1 | Graph MVP：intent→tool 环 + SSE superset + Intent 超时 A | Task-A |
| **Task-C** | P2 | interrupt（plan/clarify）+ 内存 checkpointer；`run()` 变壳评估 | Task-B |
| **Task-D** | P3 | Parser 回灌、Prompt 组合、Retriever 抽象 | 按需 |

> Task-A/A′/B 开单时须同步：`_manifest` 新端点、`_contract_manifest` 新 type（若有）、`_tech_graph` Agent 分支。

---

## 11. 开放问题（继承 LangGraph 调研 SPEC）

| ID | 问题 | 影响阶段 |
| --- | --- | --- |
| Q-7 | Intent 超时方案 A 的 `ok`：`true` 降级答 vs `false` 硬失败 | Task-B · contract |
| Q-8 | Graph 新路由最终 path 命名 | Task-A/B · manifest |
| Q-4 | Checkpointer vs `rag_conversation_logs` 双写 | Task-C |
| Q-5 | `plan_execution_token` 与 interrupt 并存期 | Task-C |

完整列表见 [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §15。

---

## 12. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-03 | 初版 draft：P0～P3 优先级、范围矩阵、Task 拆分建议 |
| 2026-06-03 | §4.4 `agent.py` 瘦身；Task-A′；范围矩阵增 agent 列 |
