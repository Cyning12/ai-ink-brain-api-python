# SPEC — 计划：LangChain/LangGraph 思想借鉴 · 自研编排改进路线图（v1）

| 项 | 内容 |
| --- | --- |
| **状态** | `draft`（需求计划 · **无 task 绑定**） |
| **日期** | 2026-06-03 |
| **文档性质** | **后续需求 / 排期输入**；非对比调研正文 |
| **前置决策** | [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §4.3（D-1～D-5 已冻结） |
| **关联调研** | [`SPEC-Research-SelfChain-vs-LangChain-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangChain-v1_zh.md) · [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) |
| **非范围** | 引入 LangChain/LangGraph 库；修改现有 `unified_chat.py` 行为；生产访客暴露 Graph 入口（见 D-4） |
| **配对前端** | `ai-ink-brain` ChatBI / Unified Chat Timeline（**本计划以标注列说明是否需改**） |

### 前端标注图例（全文通用）

| 标记 | 含义 |
| --- | --- |
| **否** | 纯后端；现有前端/BFF **无需**改动即可继续用旧 Unified 路径 |
| **契约** | 后端 SSE/HTTP 契约有增量；前端须遵守 **未知 type 忽略**（V2 总规已有）；Timeline **不强制**改 UI |
| **可选** | 接 Graph 或新 `graph.*` 事件可增强 Timeline；**不接也能跑通** |
| **联调** | local/dev 验证 Graph 时，前端/BFF **须**改请求 URL 或加 dev 开关（D-4） |
| **必须** | 生产对访客开放 Graph 入口或 HITL 新交互时，前端 **必改**（MVP 验收后） |

---

## 0. 结论摘要（TL;DR）

1. **借思想、不借依赖**（D-1）：用自研 `StateGraph`、统一节点 IO、边表驱动 fallback，不引入 `langchain-core` / `langgraph`。
2. **P0 打共享层地基**（events / State / Runnable 式 IO），**P1 在 Graph 新路由落地 MVP**，旧 Unified 仅逐步 import 共享模块。
3. **领域层保留自研**：SQL Gate、Prompt Guard、hybrid RRF、contract CI — LangChain 不提供，不得为「对齐框架」而删。
4. **低优先 / 不建议**：VectorStore 包装、默认 AgentExecutor、Legacy `/api/py/chat` 整链 LCEL 化、Graph 路径接入 V1 规则路由。
5. **`agent.py` 瘦身**：P0 抽模块（行为不变）→ Graph 接棒 → parity 后 `run()` 变壳；**MVP 前不重写** `ChatBIAgent.run` 语义（D-2）。
6. **P0 = 单 Loop 单 task**：合并原 Task-A + Task-A′；**由 00（轮 0 意图卡 · 10 需求帽）把控** 后再开 `active` task 与 30 实现。

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
| **D-4 前端控入口** | 后端 Graph 常开；MVP 前仅 local/dev 联调 → 前端 **联调** 可选、生产 **必须** 后置 |
| **D-5 SSE superset** | P0 Callback 层预留 `graph.*` 新 type + contract 登记 → 前端 **契约** / 新 type **可选** |

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

| 优先级 | LangChain/LangGraph 概念 | 本项目改进点 | 范围 | 前端 | 建议阶段 |
| :---: | --- | --- | --- | :---: | :---: |
| **P0** | LangGraph **State + 条件边** | 显式 `ChatBIState`、边表驱动 fallback | 共享层 + Graph 新路由 | **否** | MVP 前 |
| **P0** | **Callback** 与业务解耦 | 抽 `chatbi_events.py`；节点只改 state | 全路径（Graph 先用） | **否** | MVP 前 |
| **P0** | **Runnable** 统一 IO | `(state) → partial_state` + `error_code` | `tools.py` + Graph 节点 | **否** | MVP 前 |
| **P0** | **`agent.py` 抽模块瘦身** | events / models / failure 迁出；`run()` 暂留 | `api/agent.py` → 共享层 | **否** | MVP 前 |
| **P1** | **Structured Output / Parser** | Intent、SQL 强类型解析 → `error_code` | `intent_agent` · `text2sql_core` | **否** | Graph MVP |
| **P1** | **RunnableConfig** 上下文传播 | `run_id` / `session_id` / `principal` 进 State | 共享 State | **否** | Graph MVP |
| **P1** | **Router** 单一决策点 | 一个 route 节点 + 条件边 | **仅 Graph** | **契约** | Graph MVP |
| **P1** | **Tool schema**（bind_tools 思想） | `Tool.parameters` → Intent prompt 自动生成 | `tools` + `intent_agent` | **否** | Graph MVP |
| **P1** | **Graph 新路由 + SSE** | `/unified/chat/graph*` · parity + `graph.*` | Graph handler | **联调** · **可选** | Graph MVP |
| **P2** | **Interrupt / HITL** | plan preview、clarify 图暂停 + resume | **仅 Graph** | **必须** | MVP 后 |
| **P2** | **Checkpointer + thread_id** | 运行态断点；与 DB 历史分工（Q-4） | **仅 Graph** | **可选** | MVP 后 |
| **P2** | **Subgraph** | Text2SQL 内 retrieve→…→summary | Graph 内 `tool_text2sql` | **否** | 可选 |
| **P2** | **RunnableWithFallbacks** 式降级 | FailureTypeHandler **边表化** | Graph → 可选回灌 Agent | **否** | MVP 后 |
| **P3** | **Prompt Template** 组合 | `build_*_prompt` 可组合片段 | 全 LLM 点 | **否** | 按需 |
| **P3** | **Retriever** 接口 | `search(query)→hits` 抽象 | `rag_recall_tools` | **否** | 换后端时 |
| **P3** | **LCEL 并行** | Intent 阶段并行 evidence | Graph intent | **否** | 性能优化 |
| **P3** | **Document** 模型 | hit → context 字段统一 | RAG context | **契约** | 低 |
| **—** | VectorStore、AgentExecutor、LangSmith | **不建议** | — | **否** | — |

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
| **前端** | **否** |

### 4.2 Callback 与业务解耦

| 项 | 内容 |
| --- | --- |
| **借鉴** | LangChain CallbackHandler：观测与业务分离 |
| **改进** | 抽 `api/chatbi_events.py`（`_event` / `_agent_chain` / 未来 `graph.*`） |
| **范围** | Graph 节点通过 `on_node_start/end` 发 SSE；旧路径 **逐步 import**，不一次性改 |
| **验收** | Graph 节点函数内 **无** 直接 `events.append` |
| **前端** | **否**（Graph 未接前）；登记 `graph.*` 后 **契约** |

### 4.3 Runnable 统一 IO（不引库）

| 项 | 内容 |
| --- | --- |
| **借鉴** | Runnable `invoke` 输入输出契约 |
| **改进** | `run_tool_node(state) → partial_state`；Tool 外层包装，保留 `ToolResult` |
| **范围** | `tools.py` 三 Tool + Graph 节点；旧 `ChatBIAgent` 仍调原 `Tool.execute` |
| **验收** | 每个节点可 mock State 单测 |
| **前端** | **否** |

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

#### 4.4.7 前端

| 阶段 | 前端 |
| --- | --- |
| P0 抽取 | **否** — 旧 Unified Timeline 不变 |
| P1 Graph MVP | **联调** — local/dev 改 BFF URL 测 Graph；**可选** — 渲染 `graph.*` |
| P2 `run()` 变壳 | **否** — 若仍走旧 endpoint；切 Graph 默认时同 P1 **联调** |

---

## 4A. P0 单 Loop 任务（合并 · 由 00 把控）

> **结论**：P0 **可以且推荐** 在一个 Harness Loop / 一个 PR / 一条后端 task 内完成；**不**拆 Task-A 与 Task-A′ 为两个 Loop。  
> **管控**：本 Loop 的 scope、Done、非范围 **由 00 收口**（见下表）；00 未清零待确认项前 **禁止** 开 30 实现帽。

### 4A.1 00 把控含义（Harness · SDD）

对齐 [`SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md`](../SPEC-SDD-Drafting-Intent-Rounds-v1_zh.md) **轮 0 · 意图卡** 与 **10 需求帽**：

| 项 | 约定 |
| --- | --- |
| **00 产出** | 意图卡（完成态一句话 · 非范围 · 依赖 · 验收 `- [ ]`）→ 写入 **`docs/tasks/active/task_<slug>.md` 背景节** 或短附页；引用本计划 §4A + 冻结 SPEC §4.3 |
| **00 必冻结** | P0 Done 清单（§4A.3）、建议 `task_slug`、Q-8 path 暂定（可随 00 拍板） |
| **00 停止条件** | 待确认决策 **≤5 条且清零** 或人明示「方向对」；**然后** 才进入 22（若需要）→ **30 单 Loop 实现** |
| **30 Loop 范围** | §4A.2 五步；**禁止**夹带 P1（完整 intent→tool parity） |
| **前端** | **否** — 00/30 均不涉及 `ai-ink-brain` 改动 |

### 4A.2 单 Loop 内执行顺序（30 帽）

```text
① agent 抽模块     chatbi_events · chatbi_agent_models · chatbi_failure → agent.py 改 import
② State + 边表草案  ChatBIState · failure_edges_legacy / failure_edges_graph（Graph 侧 D-3 A）
③ 最小 runner       api/graph/runner.py（stub 节点，非完整 ReAct）
④ 骨架路由          unified_chat_graph.py + index 注册 + _manifest
⑤ 单测              边表参数化 + runner smoke；pytest 必绿集全绿
```

### 4A.3 P0 单 Loop Done 清单（关账勾选）

- [ ] `agent.py` 行数明显下降；`FailureTypeHandler` 等已迁出；**旧 Unified 行为无回归**
- [ ] `chatbi_events` / models / failure 可被 Graph 与 Agent **共用**
- [ ] `ChatBIState` + 边表草案；Graph 侧 Intent 超时走 **方案 A**（legacy 边保留 v1 fallback）
- [ ] Graph 路由 **已注册、可调用**（stub 响应即可）；**不要求** 与旧 Agent parity
- [ ] `_manifest` 登记新端点；`_contract_manifest` / `tech_graph_contract_check` **仍绿**
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [ ] **未** 修改 `unified_chat.py` 行为；**未** 做 P1 clarify/plan 上图

### 4A.4 单 Loop 明确不做（留给 P1 Task-B）

完整 intent→tool→fallback 环 · Graph SSE parity · `unified_chat` 大规模改 import · 前端 BFF · HITL interrupt。

### 4A.5 建议 task 元信息（00 轮填入 active task）

| 字段 | 建议值 |
| --- | --- |
| **task_slug** | `chatbi_graph_p0_foundation_v1`（00 可微调） |
| **semi_auto** | `true`（00 确认后） |
| **test_strategy** | `required`（涉 `api/` + 新路由） |
| **图谱** | 增量 `00_main.ai.md` / 待建 `10_flow_agent_graph.ai.md` 指针 |
| **前置 SPEC** | 本文件 §4A + [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §4.3 |

---

## 5. P1 — Graph MVP 核心（与 D-2 新路由同期 · Task-B）

> **依赖**：**Task-P0 done** 后方可开本阶段 Loop。

### 5.1 Structured Output / Output Parser

- Intent、SQL JSON 块 → Pydantic/dataclass；失败映射 `INTENT_PARSE_FAIL` / `SQL_GEN_SYNTAX`。
- **范围**：Graph 路径先上；parity 后可回灌 `intent_agent.py`。
- **旧 Unified**：可选，非 MVP 阻塞项。
- **前端**：**否**。

### 5.2 RunnableConfig 式上下文

- State 显式携带 `run_id`、`session_id`、`principal`；减少 `chatbi_request_ctx` 隐式依赖。
- **范围**：Graph 全链 + persist 节点。
- **前端**：**否**（请求体字段与旧 Unified 一致）。

### 5.3 Router 单一决策点

- Graph 内：`intent_decide → clarify_gate | tool_* | plan_preview | tool_direct`（D-3 方案 A）。
- **范围**：**仅 Graph**；handler 不再嵌套大段 if。
- **前端**：**契约** — 现有 `router.decision` / `agent.*` parity；无新 UI 要求。

### 5.4 Tool schema

- `ToolRegistry` 生成 Intent system 工具说明；参数 JSON Schema 与 registry 同源。
- **范围**：Graph + 旧 Agent **共用** registry。
- **前端**：**否**。

### 5.5 P1 交付物清单

| 交付物 | 说明 | 前端 |
| --- | --- | :---: |
| 新路由 | `POST /api/py/unified/chat/graph` · `.../graph/stream`（Q-8 定名 + manifest） | **联调** |
| StateGraph MVP | intent → tool 环 + Failure 边表 | **否** |
| SSE | 现有 type parity + 可选 `graph.*`（D-5） | **契约** · **可选** |
| Intent 超时 | 方案 A 单测 + contract 快照 | **契约** |
| 共享模块 | `chatbi_events` · `chatbi_state` · 边表 | **否** |
| BFF 转发 | `ai-ink-brain` `/api/py/unified/chat/graph*` 代理（若 local 直连则跳过） | **联调** |

---

## 6. P2 — MVP 后（LangGraph 相对链式最大增量）

### 6.1 Interrupt / Human-in-the-loop

- plan preview、clarify → 图 `interrupt` + resume；与 `plan_execution_token` 并存过渡期（Q-5）。
- **范围**：**仅 Graph**。
- **前端**：**必须** — 澄清/plan 确认 UI 与 resume 请求（可与现有 `agent.clarify` / `agent.plan.preview` 复用或扩展）。

### 6.2 Checkpointer

- `thread_id = session_id`；内存实现即可 MVP+；与 `rag_conversation_logs` 分工见 Q-4。
- **范围**：**仅 Graph**。
- **前端**：**可选** — 断点续跑/刷新恢复若产品需要则改；默认 **否**。

### 6.3 Subgraph（Text2SQL）

- `tool_text2sql` 内子图：retrieve → sql → gate → execute → summary。
- **范围**：Graph 内；**不改** `chain_chat.py` 对外 API。
- **前端**：**否**。

### 6.4 边表化 Fallback

- 配置表驱动：`RAG_RETRIEVE_EMPTY + gating → text2sql | direct`（§2.4.1）。
- **范围**：Graph 先行；验证后可回灌 `FailureTypeHandler`。
- **前端**：**否**（Timeline 仍消费既有 `agent.*` / `tool.*`）。

---

## 7. P3 — 按需 / 低优先

| 项 | 触发条件 | 范围 | 前端 |
| --- | --- | --- | :---: |
| Prompt Template 组合 | 多语言 / A/B / prompt 膨胀 | 全 LLM 点 | **否** |
| Retriever 抽象 | 换向量后端或多 Retriever 组合 | `rag_recall_tools` | **否** |
| LCEL 并行 evidence | Intent P95 超标 | Graph intent | **否** |
| Document 模型 | sources 契约大改 | RAG context build | **契约** |

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

### 9.1 后端模块

```text
                    │ 共享层          │ Graph 新路由      │ agent.py        │ 旧 Unified      │ Legacy /chat
────────────────────┼─────────────────┼───────────────────┼─────────────────┼─────────────────┼──────────────
P0 State/Events/IO  │ ✅ 必做         │ ✅ 消费           │ ✅ 抽模块瘦身   │ 🔶 import 共享  │ ❌ 暂不
P1 Parser/Router    │ ✅ tools/intent │ ✅ 主战场         │ 🔶 停止膨胀     │ 🔶 仍调 Agent   │ ❌ 暂不
P2 interrupt/子图   │ 🔶 接口预留     │ ✅ 主战场         │ ✅ run() 变壳   │ ❌              │ ❌
P3 Retriever/Prompt │ 🔶 按需         │ 🔶 按需           │ —               │ ❌              │ ❌
```

### 9.2 前端（`ai-ink-brain` · 摘要）

| 阶段 | 前端工作 | 标记 | 说明 |
| --- | --- | :---: | --- |
| **P0** | 无 | **否** | 继续 `/api/py/unified/chat(.stream)` |
| **P1 Graph MVP** | BFF 增 Graph 代理；dev 入口切 URL | **联调** | D-4：生产访客 **不** 暴露 |
| **P1 Graph MVP** | Timeline 消费 `graph.*` | **可选** | 未知 type 忽略即可 |
| **P1 Graph MVP** | `done` / `mode` / 核心 agent 帧 parity | **契约** | 须与旧路径一致 |
| **P2 HITL** | clarify / plan resume 交互 | **必须** | interrupt 替代 token 时 |
| **P2 Checkpointer** | 刷新/续跑 UX | **可选** | 产品未要求则不做 |
| **P3 生产开放** | 默认 Chat 走 Graph endpoint | **必须** | MVP 验收 **之后**（D-4） |

图例（后端）：✅ 必做 · 🔶 可选/渐进 · ❌ 本阶段不做

---

## 10. 建议 Task 拆分（开 task 时引用）

### 10.1 P0 · 单 Loop（00 把控 → 一条 active task）

| Task ID | 优先级 | 主题 | 依赖 | 前端 | Harness |
| --- | --- | --- | --- | :---: | --- |
| **Task-P0** | P0 | **单 Loop 地基**：§4A.2 五步（抽模块 + State/边表 + stub runner + 骨架路由 + 测） | D-1～D-5 · 本计划 §4A | **否** | **00** 意图卡 → **30** 实现 → 50（`required`） |

> 原 Task-A + Task-A′ **合并为 Task-P0**；不可拆成两个 Loop 除非 00 重开范围。

### 10.2 P1 及以后

| Task ID | 优先级 | 主题 | 依赖 | 前端 | Harness |
| --- | --- | --- | --- | :---: | --- |
| **Task-B** | P1 | Graph MVP：intent→tool 环 + SSE superset + Intent 超时 A | **Task-P0 done** | **联调** · **契约** | 00′ 可仅 delta · 30 |
| **Task-B-FE** | P1 | （`ai-ink-brain`）BFF Graph 路由 + local/dev 入口 | Task-B 后端可测 | **联调** | 前端仓 task |
| **Task-C** | P2 | interrupt + checkpointer；`run()` 变壳评估 | Task-B | **必须** | 30 |
| **Task-D** | P3 | Parser 回灌、Prompt 组合、Retriever 抽象 | 按需 | **否** | 按需 |
| **Task-E** | P3 | （`ai-ink-brain`）生产默认走 Graph | Task-B/C | **必须** | 前端仓 task |

> Task-P0/B 开单时须同步：`_manifest`、`_contract_manifest`（若有新 type）、`_tech_graph`。  
> **Task-B-FE / Task-E** 不阻塞 Task-P0。

---

## 11. 开放问题（继承 LangGraph 调研 SPEC）

| ID | 问题 | 影响阶段 |
| --- | --- | --- |
| Q-7 | Intent 超时方案 A 的 `ok`：`true` 降级答 vs `false` 硬失败 | Task-B · contract |
| Q-8 | Graph 新路由最终 path 命名 | **Task-P0 · 00 轮冻结** · manifest |
| Q-4 | Checkpointer vs `rag_conversation_logs` 双写 | Task-C |
| Q-5 | `plan_execution_token` 与 interrupt 并存期 | Task-C · **前端必须** |

完整列表见 [`SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md`](./SPEC-Research-SelfChain-vs-LangGraph-v1_zh.md) §15。

---

## 12. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-06-03 | 初版 draft：P0～P3 优先级、范围矩阵、Task 拆分建议 |
| 2026-06-03 | §4.4 `agent.py` 瘦身；Task-A′；范围矩阵增 agent 列 |
| 2026-06-03 | 全文增 **前端** 标注图例、§9.2、Task-B-FE / Task-E |
| 2026-06-03 | **§4A P0 单 Loop**；Task-P0 合并；**00 把控** Harness 映射 |
