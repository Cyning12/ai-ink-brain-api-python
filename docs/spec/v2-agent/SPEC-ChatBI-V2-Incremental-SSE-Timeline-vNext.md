# SPEC：ChatBI V2 —— 增量 SSE 与 Timeline 实时感知（下一版 / vNext）

> **状态**：draft（仅需求与架构约束，**未**绑定实现排期）  
> **日期**：2026-05-07  
> **依赖**：`SPEC-ChatBI-V2-Agent-Overview.md`、`SPEC-ChatBI-V2-Events.md`、前端 `ai-ink-brain` Unified Chat SSE 实现、后端 `api/unified_chat.py` + `api/agent.py`  
> **与当前 V2 关系**：在 **「V2 里程碑暂结」**（L0–L4 与 P1 主线）之上，**下一版**聚焦 **人机交互与可观测性**；不改变 Intent/Tool 业务语义，**改变事件下发时序与 LLM 输出粒度**。

---

## 1. 背景与问题

### 1.1 现状（代码真值）

`POST /api/py/unified/chat/stream` 在 **`CHATBI_USE_AGENT=true`** 时，对 **`ChatBIAgent.run(...)`** 采用 **`asyncio.create_task` + 等待完成** 后再 **批量 `yield`** `router.decision`、`agent.step.*`、`tool.*` 等 `chain` 事件（见 `api/unified_chat.py`：`agent_result = await _run_task` 之后才进入 `for step in agent_result.steps` 循环发 SSE）。

### 1.2 用户可感知问题

- 前端虽已使用 **SSE**，但在 **整段 `agent.run` 结束之前**，Timeline **几乎不增长**（除 `meta` 与 keepalive 注释外），用户误以为「卡住」或「未流式」。  
- **涉及 LLM 的子阶段**（Intent、RAG 生成、Text2SQL 生成/总结、Direct 生成）在 **当前契约** 下多为 **单次 `chain` 事件内的完整字段**，**无 token 级增量**（`event: token` 在 Agent 路径上**未系统性使用**）。

### 1.3 目标（产品一句话）

**每一步**（Intent 判定、单步 ReAct、工具执行边界、各 LLM 调用）在 **时间轴上可即时感知**；凡 **调用 LLM** 的环节，**均以 SSE 增量输出**；展示落点优先 **Timeline**，可选 **新增一栏** 专收「流式正文 / LLM delta」，**原 Timeline 保留不动** 以便 **对照**（A/B 或上下分栏）。

---

## 2. 范围 / 非范围

### 2.1 范围

| 域 | 内容 |
|----|------|
| **后端** | `unified_chat` Agent SSE：**在 `agent.run` 执行过程中**即下发 `chain`（及约定的 LLM delta 事件）；必要时重构 `ChatBIAgent.run` 为 **可增量汇报** 的接口（见 §4）。 |
| **契约** | 扩展或复用 SSE `event` / `chain.type`；更新 **`docs/_tech_graph/_contract_manifest.json`** 与 **`SPEC-ChatBI-V2-Events.md`**；CI `tech_graph_contract_check` 同步。 |
| **前端** | `UnifiedChatPageClient`（及 `ChainTimeline` / 相关组件）：**边收边渲染**；支持 **双栏/副栏** 方案；**未知事件类型** 仍须容错（策略 B）。 |
| **BFF** | `ai-ink-brain` 对 `/api/py/unified/chat/stream` **继续透传 body**，**禁止** `await upstream.text()` 吞流（与既有任务单一致）。 |

### 2.2 非范围（本 SPEC 不强制）

- 不改变 **V1 mode 对外语义**（`rag` / `text2sql` / `no_data`）。  
- 不替代 **L5–L7** 的后续验收（仅推迟）；本版 **不要求** 一次 PR 内完成 Gap 全闭合。  
- **不**承诺所有第三方 LLM 均支持 **OpenAI 式 `stream=True` chunk**；若某步仅支持同步 API，须定义 **服务端分片模拟**（如按句/按块切分）或 **显式标注为非流式降级**（仍发 `chain` 但无 delta）。

---

## 3. 体验与信息架构（UX）

### 3.1 方案 A（默认）：单 Timeline 增量

- **同一** `ChainTimeline`：**按到达顺序 append** `chain` 事件；**LLM delta** 以 **子事件** 或 **嵌套 payload** 形式挂在对应 `agent.think` / `tool.call.*` / 新增 **`agent.llm.*`** 下（具体见 §5）。  
- **优点**：实现路径短；与现有 mental model 一致。  
- **风险**：事件密度上升后 Timeline **可读性**下降，需折叠/聚合策略（后续迭代）。

### 3.2 方案 B（可选）：双栏 —「经典 Timeline」+「流式视图」

- **左（或上）**：**冻结为当前行为语义** 的 Timeline（或仅展示 **非 delta** 的 `chain`），用于 **与旧版对比 / 排障**。  
- **右（或下）**：**仅展示** LLM 流式输出（token / delta）及「当前子步骤标题」。  
- **优点**：对照清晰；便于灰度 **A/B**。  
- **成本**：前端状态机、布局、移动端适配。

**决策**：vNext **必须**支持 **方案 A**；**方案 B** 为 **feature flag**（如 `?stream_panel=1` 或用户设置），默认关闭。

---

## 4. 后端架构方向（约束级）

### 4.1 从「跑完再发」到「边跑边发」

**硬约束**：`StreamingResponse` 的 **生成器/async generator** 必须在 **`agent.run` 内部各阶段** 获得 **可 await 的增量**（或 **队列**），**禁止** 再在单点 `await agent.run` 后 **仅** 批量 replay（除非保留为 **兼容降级路径**）。

**候选实现**（实现阶段再选其一，本 SPEC 不拍板唯一方案）：

| 方案 | 思路 | 备注 |
|------|------|------|
| **G1** | `ChatBIAgent.run` 改为 **`AsyncIterator[AgentStreamChunk]`**，由 `unified_chat` 转 SSE | 侵入性高，契约清晰 |
| **G2** | `agent.run` 接收 **`emit: Callable[[dict], Awaitable[None]]]`**（或 `asyncio.Queue`），每步调用 | 与现有 `AgentRunView` 组装方式需协调 |
| **G3** | 拆分为 **`run_intent_stream` + `run_step_stream`**，由 `unified_chat` 编排 | 中间状态落库需再评估 |

### 4.2 LLM 子步「均为 SSE」

对每个 **会调用上游 chat/completions** 的子过程，定义以下之一：

1. **原生流式**：上游 `stream=True`，服务端 **边读 chunk 边** `yield` **`event: token`** 或 **`chain` + 新 `type`**（见 §5）；  
2. **伪流式**：上游仅同步整段返回时，服务端 **切分**（按标点/长度）后 **节流** 发出 delta（**须在 UI 标明**「模拟流式」或在 metadata 标记 `simulated_stream: true`）。

### 4.3 保活与背压

- 保留 **`SSE_KEEPALIVE_INTERVAL_S`** 语义；在 **长 LLM chunk 间隔** 间仍须 **注释行保活**。  
- **背压**：若客户端消费慢，服务端 **不得** 无界缓冲 delta；需 **上限**（队列长度 / 丢弃策略）并在 **`error`** 或 **`meta`** 中可观测。

---

## 5. 契约与事件设计（草案）

> **说明**：以下为 **vNext 提案**；落地前须走 **`_contract_manifest.json` + drift_check**。

### 5.1 复用 `event: token`（优先评估）

- **现状**：前端已对 `token` **容错**（可忽略）。  
- **扩展**：`data` 内增加 **`scope`**（如 `intent` | `rag_generate` | `text2sql_sql` | `text2sql_summary` | `direct`）、**`step_id`**、**`run_id`**，避免与旧版「最终答案 token」混淆。  
- **优点**：少增顶层 `event` 类型。  
- **风险**：与 **Legacy RAG 页** 的 `token` 语义需 **严格区分**（仅靠 `scope` + 路由区分）。

### 5.2 或新增 `chain` 子类型（备选）

- 例如 **`agent.llm.delta`**：`payload` 含 `text`、`part_index`、`encoding`。  
- **优点**：Timeline 类型系统更干净。  
- **成本**：manifest + 前端 `ChainEventCard` 分支增加。

### 5.3 `chain` 事件时序（目标）

在 **单步内** 建议顺序（可微调，须写入 Events 子规）：

`agent.step.start` →（`agent.intent` 若本步适用）→ **`agent.llm.start`（可选）** → **delta 序列** → **`agent.llm.end`（可选）** → `agent.think`（最终摘要或合并）→ `tool.call.start` → …

**Intent 单独一步**：若 Intent 走 LLM，**须在 Intent 完成前** 下发 **delta** 或至少 **`agent.intent` 的「进行中」占位**（避免长时间无 `chain`）。

---

## 6. 前端约束

| 项 | 要求 |
|----|------|
| **解析** | 维持 **`\n\n` 分帧**；**单帧 JSON 损坏** 时跳过并计数，不白屏。 |
| **Timeline** | **增量 append**；可选 **按 `step_id` 聚合** delta。 |
| **双栏** | flag 关闭时 **零 UI 回归**；开启时 **不阻塞** `done` 解锁输入。 |
| **性能** | 高频 `token` 下 **React 渲染** 须节流（`requestAnimationFrame` / batch）。 |

---

## 7. 验收标准（vNext）

- [ ] **T+0s**：在 `meta` 之后 **≤1s**（或一次网络 RTT）内出现 **下一帧有意义 `chain`**（Intent 或 step 开始），**非** 长期仅 keepalive。  
- [ ] **Intent LLM**：若开启真实 LLM，用户可在 Timeline（或流式栏）看到 **delta 或明确进行中状态**。  
- [ ] **RAG / Text2SQL / Direct**：至少 **一条路径** 在 E2E 中验证 **LLM 段有增量 SSE**。  
- [ ] **契约**：`_contract_manifest.json` 与 **前端类型** 同步；`tech_graph_contract_check` **通过**。  
- [ ] **兼容**：关闭 flag 时，行为与 **当前 V2「完成后批量发事件」** 相比 **用户可见差异** 仅体现在「更实时」，**不**改变最终 `assistant.message` 与 `done` 语义。

---

## 8. 风险与依赖

| 风险 | 缓解 |
|------|------|
| 重构 `ChatBIAgent` 影响 P1 单测 | 保留 **同步 `run` + 批量 emit** 为 **降级路径**（env 或 flag） |
| 事件顺序与前端排序 | `ts` **单调**；文档规定 **以服务端到达顺序为准** |
| 多 LLM 厂商流式差异 | `simulated_stream` 降级 + 单测 mock |

---

## 9. 关联与任务落点建议

| 仓库 | 建议任务单路径 |
|------|----------------|
| `ai-ink-brain-api-python` | `docs/tasks/active/task_chatbi_v2_incremental_sse_backend_v1.md`（待建） |
| `ai-ink-brain` | 沿用 / 扩展 `content/tasks/task_frontend_unified_chat_streaming_sse_v1.md` 或新建 **v2 incremental** 任务单 |

---

## 10. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-07 | 初稿：冻结 L5–L7 背景下，定义增量 SSE + Timeline/双栏 UX 与契约方向 |
