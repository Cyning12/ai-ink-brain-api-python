# SPEC：ChatBI V2 —— 增量 SSE 与 Timeline 实时感知（下一版 / vNext）

> **状态**：**终稿**（需求与契约已定，与 §5 及澄清简报 §9 一致；**实现代码与排期未绑定**；`type_values` 枚举须与代码 **同 PR** 落地，见 manifest `_note`）  
> **日期**：2026-05-07（文首状态对齐：**2026-05-08**）  
> **依赖**：`SPEC-ChatBI-V2-Agent-Overview.md`、`SPEC-ChatBI-V2-Events.md`、前端 `ai-ink-brain` Unified Chat SSE 实现、后端 `api/unified_chat.py` + `api/agent.py`  
> **与当前 V2 关系**：在 **「V2 里程碑暂结」**（L0–L4 与 P1 主线）之上，**下一版**聚焦 **人机交互与可观测性**；不改变 Intent/Tool 业务语义，**改变事件下发时序与 LLM 输出粒度**。

---

## 0. 修订目标与执行顺序（任务 Agent）

1. **锁契约（唯一真值链）**：以本文 **§5** + `SPEC-ChatBI-V2-Events.md` **§8** 为语义真值；**实现合并日**将 `chain.type` / `payload_min_keys_by_type` 写入 `docs/_tech_graph/_contract_manifest.json`（与 `unified_chat.py` **同一 PR**，见 manifest `_note`）。**禁止**长期「token 或 chain 二选一」并行表述。  
2. **锁验收口径**：**§7** — CI 用 **顺序 / tick** 断言；产品级「≤1s」为 **staging 手测非阻断**；「有意义」以 **Events §8.3 白名单** 为准。  
3. **锁降级矩阵**：**§9** — `CHATBI_USE_AGENT` × `CHATBI_SSE_INCREMENTAL` × `X-ChatBI-Sse-Contract` 组合。  
4. **同步任务单填空**：后端任务写死 **G2 推荐**、契约头、矩阵、mock/LLM；前端任务写死 **query + localStorage**、**不做** step 聚合 v1、坏帧策略、**开工门槛**。

---

## 1. 背景与问题

### 1.1 现状（代码真值）

`POST /api/py/unified/chat/stream` 在 **`CHATBI_USE_AGENT=true`** 时，对 **`ChatBIAgent.run(...)`** 采用 **`asyncio.create_task` + 等待完成** 后再 **批量 `yield`** `router.decision`、`agent.step.*`、`tool.*` 等 `chain` 事件（见 `api/unified_chat.py`：`agent_result = await _run_task` 之后才进入 `for step in agent_result.steps` 循环发 SSE）。

### 1.2 用户可感知问题

- 前端虽已使用 **SSE**，但在 **整段 `agent.run` 结束之前**，Timeline **几乎不增长**（除 `meta` 与 keepalive 注释外），用户误以为「卡住」或「未流式」。  
- **涉及 LLM 的子阶段**（Intent、RAG 生成、Text2SQL 生成/总结、Direct 生成）在 **当前契约** 下多为 **单次 `chain` 事件内的完整字段**，**无 token 级增量**（`event: token` 在 Agent 路径上**未系统性使用**）。

### 1.3 目标（产品一句话）

**每一步**（Intent 判定、单步 ReAct、工具执行边界、各 LLM 调用）在 **时间轴上可即时感知**；凡 **调用 LLM** 的环节，**均以 SSE 增量输出**；**默认布局为左右双栏**（见 **§3.2 方案 B**）：**左侧** 为 **Timeline**（`ChainTimeline`，链路 / `chain` 语义与当前对齐，便于对照），**右侧** 为 **执行链路**（按 phase 分段的 LLM 正文 + router / intent / think / tool 等一行摘要，**不**与左侧重复 Timeline）；**本版不考虑移动端专适**（桌面优先验收）。

---

## 2. 范围 / 非范围

### 2.1 范围

| 域 | 内容 |
|----|------|
| **后端** | `unified_chat` Agent SSE：**在 `agent.run` 执行过程中**即下发 `chain`（及约定的 LLM delta 事件）；必要时重构 `ChatBIAgent.run` 为 **可增量汇报** 的接口（见 §4）。 |
| **契约** | 扩展或复用 SSE `event` / `chain.type`；更新 **`docs/_tech_graph/_contract_manifest.json`** 与 **`SPEC-ChatBI-V2-Events.md`**；CI `tech_graph_contract_check` 同步。 |
| **前端** | `UnifiedChatPageClient`（及 `ChainTimeline` / 相关组件）：**边收边渲染**；**默认左右双栏**（左 Timeline、右 **执行链路**）；**未知事件类型** 仍须容错（策略 B）。 |
| **BFF** | `ai-ink-brain` 对 `/api/py/unified/chat/stream` **继续透传 body**，**禁止** `await upstream.text()` 吞流（与既有任务单一致）。 |

### 2.2 非范围（本 SPEC 不强制）

- 不改变 **V1 mode 对外语义**（`rag` / `text2sql` / `no_data`）。  
- 不替代 **L5–L7** 的后续验收（仅推迟）；本版 **不要求** 一次 PR 内完成 Gap 全闭合。  
- **不**承诺所有第三方 LLM 均支持 **OpenAI 式 `stream=True` chunk**；若某步仅支持同步 API，须定义 **服务端分片模拟**（如按句/按块切分）或 **显式标注为非流式降级**（仍发 `chain` 但无 delta）。  
- **移动端** 响应式与触控专适（§3.2）：**本版不纳入范围**。

---

## 3. 体验与信息架构（UX）

### 3.1 方案 A（内核 / 非默认 UI）：单 Timeline 增量

- **同一** `ChainTimeline`：**按到达顺序 append** `chain`；**LLM delta** 亦可挂在对应 `agent.think` / **`agent.llm.*`** 下（见 §5）。  
- **用途**：作为 **数据与状态机内核**；当用户 **显式关闭双栏**（非默认）时，页面 **回退为单栏** 仅展示本 Timeline（流式区可折叠、合并或隐藏，实现阶段定稿）。  
- **风险**：单栏模式下事件密度高时 **可读性** 下降，可后续加折叠/聚合。

### 3.2 方案 B（默认布局）：左右双栏 —「Timeline」+「执行链路」

- **左侧**：**Timeline**（`ChainTimeline`，`chain` 按 SSE **到达序** 全量展示，用于 **对照 / 排障**）。  
- **右侧**：**执行链路**（可读摘要，**非**第二份 Timeline）：**Query** + 按 SSE 顺序的 **`step-1` / `step-2` / …** 叙事块；每段 **`agent.llm.start` … `agent.llm.delta*` … `agent.llm.end`** **仅在该 phase 内**拼接正文（**禁止**跨 phase 把所有 `agent.llm.delta` 混成一段）；并穿插 **`router.decision` / `agent.intent` / `agent.think` / `tool.call.*` / `error` / `agent.llm.truncated`** 等一行摘要。**不在右栏重复** `ChainTimeline`（避免与左侧重复）。  
- **布局**：**仅采用左右分栏**（不采用上下分栏作为默认或等价替代）。  
- **移动端**：**本版不在验收范围内**（不要求小屏断点、触控专适；实现可固定最小宽度或保留横向滚动，但不强制「可用性达标」）。

**决策**：vNext **默认开启** 左右双栏（方案 B）。**可选**（**非默认**）：`?single_panel=1`、用户设置或等价开关，折叠为 **§3.1 单栏** 以便排障或与旧版对比。  
**与当前前端真值**：`ai-ink-brain` Unified Chat **首版落地**对「可选单栏」的接线见 **§6.1**（固定双栏与 §6 表格「布局开关」行存在**有文档登记**的差异）。

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

1. **原生流式**：上游 `stream=True`，服务端 **边读 chunk 边** `yield` **`chain`** 且 `type` 为 **`agent.llm.delta`** 序列（见 §5）；**禁止**在 Unified Chat Agent 路径用顶层 **`event: token`** 承载子步 LLM 增量。  
2. **伪流式**：上游仅同步整段返回时，服务端 **切分**（按标点/长度）后 **节流** 发出 delta（**须在 UI 标明**「模拟流式」或在 metadata 标记 `simulated_stream: true`）。

### 4.3 保活与背压

- 保留 **`SSE_KEEPALIVE_INTERVAL_S`** 语义；在 **长 LLM chunk 间隔** 间仍须 **注释行保活**。  
- **背压**：若客户端消费慢，服务端 **不得** 无界缓冲 delta；需 **上限**（队列长度 / 丢弃策略）。触顶时 **必须** 发出可观测 `chain`：`type: agent.llm.truncated`，`payload` 至少含 **`dropped_chars`**（number）、**`reason`**（string，如 `backpressure`）（见 §8.5）。可选同步 `error` / `done` 仍须到达（见 §8.3）。

---

## 5. 契约与事件设计（终稿 — vNext）

> **唯一真值**：`SPEC-ChatBI-V2-Events.md` **§8**（语义、顺序、坏例、Legacy）与本节；**机器枚举**以合并日 `docs/_tech_graph/_contract_manifest.json` 为准（与代码同 PR）。

### 5.1 已锁定：LLM 子步增量 **仅** 走 `event: chain`

| 项 | 规则 |
|----|------|
| **载体** | 每条增量为一条 **`event: chain`**，`data.type` ∈ `{ agent.llm.start, agent.llm.delta, agent.llm.end, agent.llm.truncated }`。 |
| **兄弟事件** | **`agent.llm.delta` 为多条独立 `chain`**，**不**嵌套在 `agent.think.payload` 内；嵌套深度 **1**（与现有 `ChainEventCard` 一一对应）。 |
| **`agent.think` 语义** | **仅用户级摘要**（1–2 句），在 **`agent.llm.end` 之后**发出（允许与 `assistant.message` 紧相邻）；**全文真相源**见 §8.4。 |
| **`event: token`** | **Unified Chat + `CHATBI_USE_AGENT=true` + 增量路径** 下 **禁止** 用顶层 `token` 传子步 LLM 增量（避免与 Legacy RAG 页 `token` 混义）。Legacy 仍限于 **非 Unified** 端点，靠 **URL 路径** 区分。 |
| **弃用** | 历史草案中「`token` + scope」方案 **不采用**；manifest / TS **不得**再并列两套路由。 |

### 5.2 `payload` 最小字段（实现写入 manifest 时对齐）

| `type` | `payload` 最小键 | 说明 |
|--------|------------------|------|
| `agent.llm.start` | `phase`, `step_id` | `phase`：如 `intent` \| `rag_generate` \| `text2sql_sql` \| `text2sql_summary` \| `direct`（与 Events §8.4 枚举一致）。 |
| `agent.llm.delta` | `text`, `part_index` | `part_index` 从 **0** 递增；`encoding` 可选，默认 `utf-8`。 |
| `agent.llm.end` | `ok`, `phase`, `step_id` | `ok: false` 表示本段 LLM 失败；可选 `simulated_stream`（bool）。 |
| `agent.llm.truncated` | `dropped_chars`, `reason` | 背压或截断；见 §4.3。 |

### 5.3 单步内 `chain` 顺序（冻结）

`agent.step.start` →（`agent.intent` 若适用）→ **`agent.llm.start`** → **若干 `agent.llm.delta`** → **`agent.llm.end`** → **`agent.think`** → `tool.call.start` → …  

Intent 若单独走 LLM：**在 Intent 完成前** 须出现 **`agent.llm.start`** 或 **`agent.intent`**（含进行中语义），避免长时间无 `chain`。

### 5.4 最小 JSON 示例（SSE 帧体 — 节选）

**好例（单步骨架，仅 `data` 内对象）** — 顺序意义大于数值：

```json
{"type":"agent.step.start","ts":1,"step_id":"s1","payload":{"step_number":1,"max_steps":5}}
{"type":"agent.llm.start","ts":2,"step_id":"s1","payload":{"phase":"intent","step_id":"s1"}}
{"type":"agent.llm.delta","ts":3,"step_id":"s1","payload":{"text":"分","part_index":0}}
{"type":"agent.llm.delta","ts":4,"step_id":"s1","payload":{"text":"析","part_index":1}}
{"type":"agent.llm.end","ts":5,"step_id":"s1","payload":{"ok":true,"phase":"intent","step_id":"s1"}}
{"type":"agent.think","ts":6,"step_id":"s1_think","payload":{"step_number":1,"thought":"意图简述…","selected_tool":"rag_search","mode":"rag","confidence":0.9}}
```

**坏例（delta 缺 `text`）** — 前端 **策略 B**：**跳过该帧**，内部 **`parse_error_count += 1`**；**不对用户默认展示计数**（可 `console.debug`；若 `meta` 带 `debug: true` 可镜像到 `meta.debug.sse_parse_errors` **可选**，非 v1 强制）。

---

## 6. 前端约束

| 项 | 要求 |
|----|------|
| **解析** | 维持 **`\n\n` 分帧**；**单帧 JSON 损坏** 时跳过并计数，不白屏（见 §5.4 坏例）。 |
| **Timeline** | **增量 append**；**v1 不要求** 按 `step_id` **聚合** delta（留 v2）。 |
| **执行链路（右栏）** | 由 `events` **派生**（`useMemo` 等）：按 §3.2 规则生成 **Query + step 叙事**；**不**复制左侧 `ChainTimeline`；高频更新可 **`requestAnimationFrame`** 合并 `setState`（与 §6「性能」行一致）。 |
| **双栏** | **默认**左右分栏；**单栏**为可选降级（非默认）。任一排版下 **不阻塞** `done` 解锁输入。 |
| **布局开关（无 NEXT_PUBLIC_）— 产品目标** | **目标行为**：**仅** `?single_panel=1`（首屏）与 **`localStorage`** 键 **`ink-brain.chatbi.unified.singlePanel`**（`"1"` / `"0"`）；**后端无感**，**不**增加 Python 侧 query/header 依赖。**当前 `ai-ink-brain` 实现真值**见 **§6.1**（与目标有差异时以 §6.1 为准，直至后续 PR 对齐）。 |
| **版本协商** | Unified Chat 前端 **必须** 对 stream 请求携带 **`X-ChatBI-Sse-Contract: 2`**（见 §9）；BFF **原样透传**该头。 |
| **性能** | 高频 **`agent.llm.delta`** 下 **React 渲染** 须节流（`requestAnimationFrame` / batch）。 |

### 6.1 前端实现登记：`single_panel` / `localStorage` 与「固定双栏」（2026-05-08）

| 维度 | 内容 |
|------|------|
| **产品目标（§3.2 / §6 上表）** | 默认 **左右双栏**；**可选单栏**：`?single_panel=1` 与 **`localStorage`** `ink-brain.chatbi.unified.singlePanel`（`"1"` / `"0"`）控制折叠为 §3.1 单栏式排障。 |
| **`ai-ink-brain` 当前真值** | `UnifiedChatPageClient` 主区 **固定** `grid-cols-2`（左 **`ChainTimeline`**、右 **执行链路** 摘要区）；右栏 **不**再嵌套第二份 Timeline；**未**读取 `single_panel` query、**未**读写上述 **`localStorage`** 键；**无**勾选/持久化 UI 切换单双栏。实现入口：`buildExecutionTraceSections` + 右栏区块（与 **§3.2** 一致）。 |
| **后端** | 不受影响；§9.2 / §9.3 仍成立（布局开关**本就不**经 Python）。 |
| **后续对齐** | 若产品仍要 **query + LS** 与 SPEC 原文一致，在 **`ai-ink-brain`** 单独 PR 接线并回填本任务单验收；届时可删或收窄本节「差异」表述。 |

---

## 7. 验收标准（vNext — 可测化）

### 7.1 CI / 单测（阻断；不测真实 wall-clock 1s）

- [ ] 使用 **mock emitter**（或队列替身）注入事件序列，断言：**在首个 `chain` 且 `type: meta` 之后**，于 **同一同步探测点** 已存在 **至少一条** 后续 **`chain`**，且其 `type` ∈ **「首条有意义白名单」**（与 **§7.3** 一致）。  
- [ ] **可选加强**：断言 **`meta` → 第一条非 keepalive 的 `chain` data JSON** 之间 **插入的异步 tick 数 ≤ N**（由测试固定 N，如 `await asyncio.sleep(0)` 次数），**不**断言真实时间 ≤1s。

### 7.2 集成 / 手测（非阻断 / staging checklist）

- [ ] 脚本或清单写明：**连接 → 发流式请求 → 观察 DevTools / 脚本日志** 中 **`meta` 后尽快出现** `router.decision` 或 `agent.step.start` 或 `agent.llm.start`（产品感知的「≤1s」仅在此层描述，**不作为** CI 硬断言）。

### 7.3 「有意义」首条 `chain.type` 白名单

以下 **任一** 出现在 `meta` 之后的首条 **非 keepalive、非纯注释** 的 `chain` 上，即算满足 **§7.1**：`router.decision`、`agent.step.start`、`agent.intent`、`agent.llm.start`、`tool.call.start`。  

**不算「有意义 data 帧」**：仅 **SSE 注释行**（如 `: keepalive`）、**空行**、或 **无法解析的 data**（计 **parse_error** 但 **不**计入白名单命中）。

### 7.4 与 keepalive 的边界

- **注释行**（`:` 开头）**不**算作 **§7.1** 中的「一帧 data 事件」。  
- **`event: chain` + 合法 JSON `data`** 才算一帧。

### 7.5 其它产品验收（阻断）

- [ ] **Intent LLM**（真实 LLM 可选，见任务单 **mock vs LLM**）：左栏 Timeline 可见完整 `chain`；右栏 **执行链路** 在对应 **`step-*`** 下可见 **intent** 段 `agent.llm.*`（start / 正文 / end）或等价占位。  
- [ ] **RAG / Text2SQL / Direct**：**CI 以 mock/stub 流为准**；至少一条路径在 mock 下验证 delta 序列；**真实 LLM** 走 **release / staging checklist**（与任务单统一一句）。  
- [ ] **契约**：合并实现 PR 时 `_contract_manifest.json` 与 **前端类型** 同步；`tech_graph_contract_check` **通过**。  
- [ ] **布局**：**默认**左右双栏；**单栏降级**（query/LS，见 §6）不改变 `assistant.message` 与 `done` 语义。**当前前端**若尚未接线单栏，见 **§6.1**，本项中「单栏降级」可对 **首版** 标为 **N/A** 或拆子项验收。

---

## 8. 风险与依赖

| 风险 | 缓解 |
|------|------|
| 重构 `ChatBIAgent` 影响 P1 单测 | 保留 **同步 `run` + 批量 emit** 为 **降级路径**（env 或 flag） |
| 事件顺序与前端排序 | `ts` **单调**；文档规定 **以服务端到达顺序为准** |
| 多 LLM 厂商流式差异 | `simulated_stream` 降级 + 单测 mock |

### 8.1 run_id / step_id 与生命周期

- **`run_id`**：与首包 **`meta`** 中已有字段 **一致**，一次 Unified stream 请求 **一个** `run_id`。  
- **`step_id`**：由后端生成，建议 **`{run_id}_s{step_number}_{phase_slug}`** 或 UUID；须在 **`agent.llm.*`** 与同一 ReAct 步的 **`agent.think`** 上 **可关联**（便于右栏标题）。  
- **`conversation_id` / `message_id`（DB）与 `step_id`**：本节 **仅约束 SSE 侧** 标识；若 ingest / 表结构（如 `rag_conversation_logs`）须与 `step_id` **强绑定或同值**，属 **实现 PR 填空**，对照 **`PROJECT_CONFIG`** 与 SQL 真值 **另补一行** 即可 — **非契约阻断**（与澄清简报 **§8.8**、任务单 **实现备忘** 一致）。  
- **SSE 重连**：本版 **不** 保证跨连接续传 delta；重连视为 **新 `run_id`**（若产品后续要 resume，另开 SPEC）。

### 8.2 并发与顺序

- **多工具并行**（若存在）：**不**要求全局 `ts` 单调；客户端 **只按 SSE 到达顺序** append（与既有「策略 B」一致）。  
- **前端实现**须与 **§8.2** 一致，**禁止**按 `type` 重排覆盖到达序（除白名单测试外）。

### 8.3 流式中途失败

- **须**发出 **`agent.llm.end`**，`payload.ok: false`，并可跟 **`error`** `chain`。  
- **`done`**：**仍须**到达（`ok` 与业务一致）；**`assistant.message`** 可为 **空**、**部分**（已生成片段）或 **错误提示全文** — 三者择一须在 Events §8 与实现一致并写入测试。  
- **右栏（执行链路）**：对应 **LLM 子段** 展示至失败点为止的正文；不强制清空；**不**要求右栏与 `assistant.message` 实时逐字一致（真相源仍 §8.4）。

### 8.4 双写与真相源（全文）

- **用户可见最终答案**以 **`assistant.message`**（`chain`）为 **唯一产品真相源**。  
- **右栏** 各 **`agent.llm.*` 段内** 拼接为 **过程态**；在 **成功路径** 上，**同一 phase 内** delta 拼接与最终 **`assistant.message.content`** **宜一致**（允许末尾空白归一化差异，须在测试中固定规则）；**跨 phase** 的右栏全文 **不要求** 与最终答案逐字对齐（避免 intent 提示与 direct 正文混读）。

### 8.5 背压触顶与可观测字段

- 触顶时除 **`agent.llm.truncated`**（§5.2）外，可选再发 **`agent.llm.end`** `ok: false`；**Timeline** 左栏 **建议**展示 `agent.llm.truncated` 卡片（与 `ChainEventCard` 扩展一致）。

### 8.6 观测与隐私

- **默认**不在服务端日志中落库 **delta 全文**；若调试开启，须遵守既有 **脱敏 / 长度截断** 策略（与运维约定一句即可，细节见 `PROJECT_CONFIG` 与日志实现）。

### 8.7 版本协商（与 manifest）

- 客户端 **`X-ChatBI-Sse-Contract: 2`** 与本文 **`agent.llm.*`** 契约 **绑定**；未来 **v3** 递增版本号并同步 `tech_graph_contract_check` 允许的文档锚点。  
- **manifest** 仅承载 **已合并代码** 的枚举；**禁止**隐式仅靠路由推断契约版本。

---

## 9. 降级与组合真值表

### 9.1 环境变量

| 变量 | 默认（vNext 落地后建议） | 含义 |
|------|--------------------------|------|
| `CHATBI_USE_AGENT` | 依部署 | `false` → V1 路由路径，**不适用**本增量 SPEC。 |
| `CHATBI_SSE_INCREMENTAL` | `true` | `false` → **强制**走「`await run` 完成后批量 emit」（与当前行为一致），**忽略**客户端增量协商头（仍须安全）。 |

### 9.2 客户端识别（与后端行为）

| 条件 | 后端时序 |
|------|----------|
| `CHATBI_USE_AGENT=true` 且 `CHATBI_SSE_INCREMENTAL=true` 且请求带 **`X-ChatBI-Sse-Contract: 2`** | **增量 emit**（vNext）。 |
| 同上但 **缺失**该头，或值为 **`0` / `1`** | **批量 replay**（旧前端 / 兼容）。 |
| `CHATBI_SSE_INCREMENTAL=false` | **批量 replay**（服务端降级）。 |
| `CHATBI_USE_AGENT=false` | V1 非 Agent 路径（本表不展开）。 |

### 9.3 与前端布局的关系

- **`single_panel` / localStorage**（产品目标下）**仅影响**前端排版，**不**改变 §9.2 后端分支。  
- **当前**：若前端 **未**消费 query/LS（见 **§6.1**），本节第一句对运行时**无效果**，仍以 §9.2 为 SSE 真值。  
- BFF **须透传** `X-ChatBI-Sse-Contract`。

---

## 10. 关联与任务落点建议

| 仓库 | 任务单路径 |
|------|------------|
| `ai-ink-brain-api-python` | `docs/tasks/active/task_chatbi_v2_incremental_sse_backend_v1.md` |
| `ai-ink-brain` | `content/tasks/active/task_chatbi_v2_incremental_sse_timeline_frontend_v1.md`（前置：`task_frontend_unified_chat_streaming_sse_v1.md`） |
| `PROJECT_CONFIG` | `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` — `CHATBI_SSE_INCREMENTAL` 真值（不复制 `.env`） |

---

## 11. 修订记录

| 日期 | 说明 |
|------|------|
| 2026-05-09 | **§3.2 / §6 / §6.1 / §7.5 / §8.3–8.4**：右栏由「全量 delta 一锅端」改为 **执行链路**（Query + `step-*`、**按 phase** 拼接 LLM；router / intent / think / tool 等穿插）；**移除**右栏嵌套第二份 Timeline；与 `UnifiedChatPageClient`（`buildExecutionTraceSections`）对齐 |
| 2026-05-08 | **§6.1**：登记 `ai-ink-brain` Unified Chat **固定双栏**与 **`single_panel` + `localStorage`** 产品目标的**实现差异**；§6 布局开关行改为「产品目标 + §6.1 真值」；§3.2 / §9.3 交叉引用 |
| 2026-05-08（晚） | 文首 **状态** 与 §5「终稿」及澄清简报 §9 **对齐**（不再标 `draft`）；§8.1 增补 **DB id ↔ step_id** 为 **实现 PR 填空、非阻断** |
| 2026-05-08 | 终稿化：§0 执行顺序；§5 **chain-only** LLM 契约 + 最小 JSON；§7 可测验收 + 白名单；§8.1–8.7；§9 降级矩阵；章节 **§10** 任务 / **§11** 修订；`CHATBI_SSE_INCREMENTAL` + `X-ChatBI-Sse-Contract: 2`；manifest `_note` 约束「代码同 PR」 |
| 2026-05-06 | §3/§6/§7：方案 B 固定为 **左右双栏**、**默认开启**；**不考虑移动端**；单栏为可选非默认降级 |
| 2026-05-07 | 初稿：冻结 L5–L7 背景下，定义增量 SSE + Timeline/双栏 UX 与契约方向 |
