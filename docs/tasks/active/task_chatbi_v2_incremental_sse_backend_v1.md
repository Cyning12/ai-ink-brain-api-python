# 实现 ChatBI V2 执行期增量 SSE 与 LLM 子步流式（后端 v1）

**状态**：待排期（契约与验收以 **`SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` 终稿** + **`SPEC-ChatBI-V2-Events.md` §8** 为准）  
**范围**：仅 `ai-ink-brain-api-python`（`api/unified_chat.py`、`api/agent.py` 及 LLM 调用链；契约与 CI）  
**关联图谱**：`docs/_tech_graph/` 中与 unified chat 相关条目（落地后增量更新）  
**关联 SPEC / 真值**：

- `docs/spec/v2-agent/SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md` — §0 执行顺序、§5 契约、§7 验收、§9 矩阵  
- `docs/spec/v2-agent/SPEC-ChatBI-V2-Events.md` — **§8**（Legacy 与 `agent.llm.*`）  
- `docs/_tech_graph/_contract_manifest.json` — **须与 `unified_chat.py` 同一 PR** 追加 `agent.llm.*`（见 manifest `_note`）  
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` — `CHATBI_SSE_INCREMENTAL`

**配对前端任务**：`ai-ink-brain/content/tasks/active/task_chatbi_v2_incremental_sse_timeline_frontend_v1.md`

---

## 开工门槛（前置）

- **最小子集**：`task_frontend_unified_chat_streaming_sse_v1.md` 中 **BFF `/api/py/unified/chat/stream` body 透传** + 前端能 **分帧解析** `chain`/`done` 即可并行设计后端；**合并 vNext 行为**前须 E2E 可联调。  
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
| **G1 / G2 / G3** | **推荐 G2**：`agent.run(..., emit: Callable[[dict], Awaitable[None]] | Queue)`，由 `unified_chat` 消费并转 `_sse("chain", …)`。若实作改 **G1**，须同步回改本任务单 + vNext §4.1 备注。 |
| **契约** | **`agent.llm.start` / `delta` / `end` / `truncated`**，`payload` 最小键见 vNext **§5.2** 与 Events **§8**。 |

---

## 范围 / 非范围

### 范围

| 项 | 说明 |
|----|------|
| `unified_chat` | 增量 emit；`X-ChatBI-Sse-Contract` 非 `2` 或缺省 → **批量 replay**；`CHATBI_SSE_INCREMENTAL=false` → 批量。 |
| `ChatBIAgent` | 接入 **G2 emit**；Intent / RAG / Text2SQL / Direct 各 LLM 点产出 **`agent.llm.*`**。 |
| 背压 | 触顶发 **`agent.llm.truncated`**（字段 vNext §5.2 / §4.3）。 |
| 日志 | **默认**不落 delta 全文（§8.6）；调试开关与脱敏另见实现。 |

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

- [ ] 满足 vNext **§7.1**（mock）+ **§7.5**（契约 + 至少一条 mock delta 路径）。  
- [ ] **§9 矩阵** 单元或集成测试覆盖 **≥2 个** 代表格（增量 on + 头 `2`；增量 on + 无头批量）。  
- [ ] **`_contract_manifest.json`** 与 Events **§8**、实现 **同一 PR**；`python tools/tech_graph_contract_check.py` **通过**。  
- [ ] **pytest** 与既有 CI 通过。

---

## 实现备忘（子 Agent 回填 — **实现 PR 落地选型**，非 SPEC 缺口）

以下 **`______`** 须在合并实现 PR 时填实；**不阻塞**契约审阅与澄清简报收口（参见简报 **§8.8**、主 SPEC **§8.1** DB 关联说明）。

- **DB（可选）**：若 `conversation_id` / `message_id` 与 SSE `step_id` 须落库关联 — 对照 **`PROJECT_CONFIG`** 与 SQL **另补一行** 文档或 migration 说明。  
- **`_contract_manifest.json`**：`agent.llm.*` 写入 **`type_values` + `payload_min_keys_by_type`** 须与 **`api/unified_chat.py` 同一 PR**（当前可仍仅 `_note` 预告）。  
- 实际选型（若偏离 G2）：______  
- 修改文件列表：______  
- `assistant.message` 失败策略（**空** / **部分** / **错误全文**）选定：______  

---

## 给 Cursor

验收、非范围、依赖、图谱、`_contract_manifest`、`unified_chat`、`ChatBIAgent`、`SSE`、`incremental`、`agent.llm.delta`、`X-ChatBI-Sse-Contract`、`CHATBI_SSE_INCREMENTAL`、vNext §9
