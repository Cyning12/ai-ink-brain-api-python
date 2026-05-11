# 实现 ChatBI V2 执行期增量 SSE 与 LLM 子步流式（后端 v1）

**状态**：**已验收归档**（2026-05-11；`pytest` / `tech_graph_contract_check`、前后端联调通过）  
**归档自**：`docs/tasks/active/task_chatbi_v2_incremental_sse_backend_v1.md`  
**范围**：仅 `ai-ink-brain-api-python`（`api/unified_chat.py`、`api/agent.py` 及 LLM 调用链；契约与 CI）  
**关联图谱**：`docs/_tech_graph/` 中与 unified chat 相关条目（落地后增量更新）  
**关联 SPEC / 真值**：

- `docs/spec/v2-agent/SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` — §0 执行顺序、§5 契约、§7 验收、§9 矩阵  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Events.md` — **§8**（Legacy 与 `agent.llm.*`）  
- `docs/_tech_graph/_contract_manifest.json` — **须与 `unified_chat.py` 同一 PR** 追加 `agent.llm.*`（见 manifest `_note`）  
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` — `CHATBI_SSE_INCREMENTAL`、`CHATBI_V2_DEBUG_LLM_PROMPTS`、`CHATBI_SSE_EMIT_QUEUE_MAX`（与增量契约**独立**：前者控「边跑边 emit」，后者控 **LLM messages** 调试事件；delta 全文日志见 vNext **§8.6**）

**配对前端任务**：`ai-ink-brain/content/tasks/done/task_frontend_unified_chat_streaming_sse_v1.md`（及 `task_chatbi_v2_incremental_sse_timeline_frontend_v1.md`）

> **真值层级**：本单是**索引 + 后端落点**；**payload 最小键、§7.1 首条有意义 `chain` 白名单、背压字段、失败路径、§9.2 矩阵**以 vNext / Events **现行终稿**为准。若开工后发现 SPEC 与代码冲突，**走 SPEC 修订 PR**，不在本任务单内「口头改契约」。

---

## 开工前：是否需要人工确认（收口表）

| 主题 | 是否必须人工（产品/总设） | 说明 |
|------|---------------------------|------|
| 契约字段与顺序、§7.1 / §7.3、§9.2 | **否**（以 SPEC 终稿为准） | 实现与测试对齐 vNext + Events §8；争议时开 SPEC PR。 |
| **G2 → G1** 或 emit 形态变更 | **建议 TL/总设 ACK** | PR **Architecture** 标 `G1`/`G2`；**须**同步改 vNext §4.1 + 本表「架构选型」；非产品会签，但算**架构偏离**，避免评审扯皮。 |
| **`assistant.message` 失败形态**（空 / 部分 / 错误全文） | **否**（SPEC 已定枚举） | vNext **§8.3** 与 Events §8 已约束；实现 PR **选定一种可测组合写入 pytest**，前端按配对任务对齐；仅当**产品要违背 SPEC**时才上会。 |
| **DB 是否绑定 `step_id` / 审计** | **视合规/产品** | SPEC **§8.1**：默认 **非契约阻断**；若上线要求「可重放/审计 SQL」，则由产品拍板 → 补 migration + `PROJECT_CONFIG` 一行。 |
| **`agent.llm.*` 覆盖哪些调用** | **一般否** | 以 Events **§8** + vNext **§5.2 `phase`** 为准；**不含**无 `chain` 的 embedding 等；**新增** LLM 调用点须在 PR 说明并列 manifest。 |
| **manifest 门禁** | **否**（以 CI 为准） | 见下文「实现备忘 — manifest」：`tech_graph_contract_check.py` 对 `type_values` / `payload_min_keys_by_type` 与后端源码做 diff；**合并会发新 `chain.type` 的 PR 必须绿**。 |
| **§9 测试「≥2 格」选哪两格** | **否** | 与 vNext **§9.2** 对齐即可：本任务验收表已锁 **「增量 on + 头 `2`」** 与 **「增量 on + 无头 → 批量」**；`CHATBI_USE_AGENT=false` 不在本子任务矩阵扩测（见非范围）。 |

---

## 开工门槛（前置）

- **最小子集**：前端仓 **`ai-ink-brain/content/tasks/done/task_frontend_unified_chat_streaming_sse_v1.md`** — **BFF `/api/py/unified/chat/stream` body 透传** + 前端能 **分帧解析** `chain`/`done` 即可并行设计后端；**合并 vNext 行为**前须 E2E 可联调。  
- **契约头**：前端须发 **`X-ChatBI-Sse-Contract: 2`**（见 vNext §11）；本任务实现 **读取该头** 分支增量 vs 批量 replay。

---

## 背景与目标

当前 Agent 路径在 **`await ChatBIAgent.run` 结束后再批量 `yield`**。目标：

1. **边执行边下发**：满足 vNext **§4.1**、**§7.1**。  
2. **LLM 子步**：仅 **`chain` + `agent.llm.*`**（**禁止** Unified 增量路径用顶层 `event: token` 传子步），见 **Events §8.1**。  
3. **降级**：`CHATBI_SSE_INCREMENTAL` + 请求头组合见 **§9 矩阵**（本任务实现）。

---

## 架构选型（已锁推荐）

| 项 | 锁定值 |
|----|--------|
| **G1 / G2 / G3** | **推荐 G2**：`agent.run(..., emit: Callable[[dict], Awaitable[None]] | Queue)`，由 `unified_chat` 消费并转 `_sse("chain", …)`。**G1** 指仍在 `run` 内用**同步回调**推送 dict、无独立 consumer 任务；与 G2 差别在是否引入 **Queue + 显式消费循环**。若实作改 **G1**，PR 须声明选型，并**同步**本任务单本节 + **vNext §4.1**（否则视为评审未决项）。 |
| **契约** | **`agent.llm.start` / `delta` / `end` / `truncated`**，`payload` 最小键见 vNext **§5.2** 与 Events **§8**。 |

---

## 范围 / 非范围

### 范围

| 项 | 说明 |
|----|------|
| `unified_chat` | 增量 emit；`X-ChatBI-Sse-Contract` 非 `2` 或缺省 → **批量 replay**；`CHATBI_SSE_INCREMENTAL=false` → 批量。 |
| `ChatBIAgent` | 接入 **G2 emit**；凡走 **chat/completion 类**且影响 Timeline 的 Intent / RAG / Text2SQL / Direct 等 LLM 步，须产出 **`agent.llm.*`**（**不**含仅 embedding、无 SSE `chain` 的内部调用；边界以 **Events §8** + vNext **§5.2** 为准）。 |
| 背压 | 触顶发 **`agent.llm.truncated`**（字段 vNext §5.2 / §4.3）；队列满 **`reason=backpressure`**（见 `CHATBI_SSE_EMIT_QUEUE_MAX`）。 |
| 日志 | **默认**不落 delta 全文（vNext **§8.6**）；与 **`CHATBI_V2_DEBUG_LLM_PROMPTS`** 无关，后者见 `PROJECT_CONFIG` 表。 |

### 非范围

- 前端左右双栏 / **移动端**（纯前端）。  
- 不在本 PR **仅**改 manifest、无 `unified_chat` emit（**会失败** `tech_graph_contract_check`）。

---

## 降级与组合真值表（摘要 — 全文见 vNext §9）

| `CHATBI_USE_AGENT` | `CHATBI_SSE_INCREMENTAL` | `X-ChatBI-Sse-Contract` | 后端行为 |
|--------------------|--------------------------|-------------------------|----------|
| `false` | * | * | V1 路径（非本任务） |
| `true` | `false` | * | **批量 replay** |
| `true` | `true` | **`2`** | **增量 emit** |
| `true` | `true` | 缺省 / `0` / `1` | **批量 replay**（旧客户端） |

---

## CI vs 真实 LLM（统一一句）

- **CI / pytest 阻断**：以 **mock emitter / stub 流** 断言 **`meta` → 首条有意义 `chain`** 顺序及 **`agent.llm.delta`** 序列（见 vNext **§7.1**、**§7.5**）。  
- **真实 LLM**：**release / staging 手测 checklist**（非 PR 阻断，除非仓库另有 policy）。

---

## 验收标准（可勾选）

- [x] 满足 vNext **§7.1**（mock）+ **§7.5**（契约 + 至少一条 mock delta 路径）。  
- [x] **§9 矩阵** 单元或集成测试覆盖 **≥2 个** 代表格，且**须包含** vNext **§9.2** 两格：**`CHATBI_SSE_INCREMENTAL=true` + 头 `2` → 增量**；**同 env + 无/`0`/`1` 头 → 批量**。若将来 SPEC 为矩阵加维，以 vNext 修订为准扩测；本子任务**不**强制 `CHATBI_USE_AGENT=false` 格。  
- [x] **`_contract_manifest.json`** 与 Events **§8**、实现 **同一 PR**；`python tools/tech_graph_contract_check.py` **通过**。  
- [x] **pytest** 与既有 CI 通过。

---

## 实现备忘（子 Agent 回填 — **实现 PR 落地选型**，非 SPEC 缺口）

以下 **`______`** 须在合并实现 PR 时填实；**不阻塞**契约审阅与澄清简报收口（参见简报 **§8.8**、主 SPEC **§8.1** DB 关联说明）。

- **DB（可选）**：若 `conversation_id` / `message_id` 与 SSE `step_id` 须落库关联 — 对照 **`PROJECT_CONFIG`** 与 SQL **另补一行** 文档或 migration 说明；**是否必选**见上文「开工前」表（合规/产品）。  
- **`_contract_manifest.json`（门禁口径）**：`tools/tech_graph_contract_check.py` 会校验 manifest 结构，并将 **`unified_chat.py` + `agent.py`** 中出现的 `chain.type` / payload 键与 **`type_values`、`payload_min_keys_by_type`** 对齐。**规则**：凡 PR **已**在上述源码中 emit **新的** `chain.type`（含 `agent.llm.*`），**同一 PR** 必须更新 manifest 至 **CI 通过** — **禁止**依赖长期「仅 `_note`、无枚举」糊弄门禁。独立「仅文档 / `_note` 预告」PR 仅在不引入新 `chain` 类型、且不导致 checker 失败的前提下允许。  
- 实际选型（若偏离 G2）：**G2**（`ChatBIAgent.run(..., emit=)` → `asyncio.Queue`，`unified_chat` 消费队列边 `yield`；背压见 `CHATBI_SSE_EMIT_QUEUE_MAX`）  
- 修改文件列表：`api/unified_chat.py`、`tests/test_unified_chat_sse_incremental_vnext.py`、`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（`CHATBI_SSE_EMIT_QUEUE_MAX`）  
- `assistant.message` 失败路径用例（**空** / **部分** / **错误全文** 中本轮选定的 **fixture 组合**）：**空（无 `assistant.message` 帧）** — `tests/test_unified_chat_sse_incremental_vnext.py::test_sse_incremental_agent_run_raises_error_without_assistant_message`（`run` 抛错 → `error` chain + `done.ok=false`）；背压：`::test_sse_incremental_queue_backpressure_emits_truncated`  

---

## 归档记录（验收收口）

| 项 | 说明 |
|----|------|
| 归档日 | 2026-05-11 |
| 前端联调 | Unified Chat 非一次性 SSE、Text2SQL 等路径人测通过（见前端 `content/tasks/done/task_frontend_unified_chat_streaming_sse_v1.md`） |

---

## 给 Cursor

验收、非范围、依赖、图谱、`_contract_manifest`、`unified_chat`、`ChatBIAgent`、`SSE`、`incremental`、`agent.llm.delta`、`X-ChatBI-Sse-Contract`、`CHATBI_SSE_INCREMENTAL`、vNext §9
