# Task：ChatBI V3 — 低置信方案预览、用户确认与编排方案 B（后 P1-4）

> **状态**：`backlog`（**整单**：与 `SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md` 对齐的完整 implementation 仍待后续 PR；**首包「方案 B」**：见 **§5.0**，**已验收** **2026-05-13**）  
> **schedule_ref**：RECENT §1.1 #4  
> **登记日期**：2026-05-12  
> **需求真值（L1）**：`docs/spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`  
> **执行 Agent 交代（可复制 Prompt）**：[`task_chatbi_v3_low_confidence_plan_preview_confirm_v1_AGENT_PROMPT.md`](task_chatbi_v3_low_confidence_plan_preview_confirm_v1_AGENT_PROMPT.md)（首包仅 **`api/agent.py`** 方案 B + pytest）  
> **统筹入口**：`docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md`  
> **多轮母单**：`docs/tasks/active/task_chatbi_v3_debt_from_v2_multiturn_v1.md`  
> **前置（done）**：`docs/tasks/done/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`（P1-4 澄清短路）  
> **代码入口（预期）**：`api/agent.py`（澄清与 `step1_tool` / `router.decision` 顺序）、`api/intent_agent.py`、`api/unified_chat.py`；前端 **`ai-ink-brain`**：澄清总任务见 **`Projects/ai-ink-brain/content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`**；方案 B 首包 **前端烟测步骤** 见本文 **§5.0.1**

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required` |
| **semi_auto** | `false` |
| **audit_profile** | `full` |
| **git_branch** | `task/chatbi-v3-low-confidence-plan` |
| **reinspect** | 母单剩余项关账前 **必须** 50 |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | pending | 22-R1,30 | backlog → active 前 |

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-lowconf-unconfirmed-exec` | 低置信未确认即执行 | 澄清 / 预览 SSE，不升格 | 是 | 需用户确认 |
| F2 | `fp-lowconf-token-invalid` | 确认令牌无效 | `403` + 结构化错误 | 否 | 确认失效 |
| F3 | `fp-lowconf-preview-fail` | 预览生成失败 | `error` chain 事件 | 是 | 方案生成失败 |

---

## 验收标准

> 分项明细见 **§5**；本节供 Harness validate 与关账核对。

- [ ] **§5.0** 方案 B 首包已验收（2026-05-13）；**§5.1** 母单大项仍 backlog，后续 PR 逐项关闭  
- [ ] 合并前 **`pytest tests -m "not intent_eval and not intent_benchmark"`** 全绿；触达契约时 **`python tools/tech_graph_contract_check.py`** 通过  
- [ ] 母单剩余 implementation 关账前 **50** 复检落盘（`reinspect_results/`）

---

## 1. 背景与目标

在 **意图置信度低于 `INTENT_MIN_CONFIDENCE`** 时，产品需要：

1. **方案 B**：调整编排 / SSE，使「低置信 + fallback」**不再**在观测上表现为 **`final_mode: rag` 且无执行」等易误解形态（见需求规 **§1**）。  
2. **text2sql / rag**：在打断或澄清前，输出 **可审阅的执行方案草案**（SQL 草案或 RAG 检索方案级信息），便于用户判断是否改问或改进。  
3. **用户显式确认**「按识别方案执行」后，通过 **服务端认可的 bypass**（令牌 / `effective_confidence` 等，见需求规 **§4**）**通过原有意图门槛**，完成 **一轮** 全链路；**禁止**仅靠客户端篡改 `confidence` 数字。

---

## 2. 范围

- 后端：澄清门控与 **`step1_tool` / `intent.fallback` 应用顺序**；**计划预览** 生成路径（Text2SQL 草案、RAG 方案草案）；**确认后放行** 与日志。  
- 契约：新 / 扩 **`chain.type`**、manifest、`tech_graph_contract_check`。  
- 前端：确认按钮 / 续跑协议（可依赖 Ink 已有 `run_id` / session；**须**与后端同 PR 或明确分 PR 依赖顺序）。

---

## 3. 非范围

- **不**在本单内完成 **Intent vNext 多候选 + 裁判**（`task_chatbi_v3_intent_classification_debt_v1.md` §2.1）。  
- **不**替代 **SQL AST 闸门 / RBAC** 实质性规则；预览与执行均须遵守 **Security**、**Identity-Access** 子规。

---

## 4. 依赖

- `SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`（需求拍板）  
- `SPEC-ChatBI-V3-Multiturn-Debt.md`、`SPEC-ChatBI-V3-Identity-Access.md`、`SPEC-ChatBI-V3-Security.md`  
- `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`（env 真值表，新增开关时同步）

---

## 5. 验收标准（分列：首包已验收 vs 母单仍 backlog）

### 5.0 首包：方案 B（`…_AGENT_PROMPT.md`）— **已验收 · 2026-05-13**

便于关单与 PR 描述；与 **`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`** 全文能力无关的子集。

| # | 验收项 | 口径 | 结果 |
|---|--------|------|------|
| **B-1** | G2 SSE：澄清短路前 `router.decision` | `CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` 且满足 P1-4 澄清条件、`emit` 非空时，`final_mode` 与 `candidate_mode` 均为 `intent.mode`（如 `text2sql`），**不得**为 `rag` 且无 `rag_search` | **通过**（`api/agent.py`：`final_mode = intent.mode if _clarify_eligible else step1_mode`） |
| **B-2** | JSON `/unified/chat`：同上观测 | `clarify_short_circuit` 时 `router.decision` **不再**把 `final_mode` 写成 fallback 的 `rag` | **通过**（`api/unified_chat.py` 已去掉对 `final_mode → tool_mode_map[fallback]` 的覆盖） |
| **B-3** | SSE 批量 replay | 与 JSON 一致，无「假 rag」 | **通过**（replay 分支已对齐） |
| **B-4** | 执行首步未改 | 非澄清路径下 `step1_tool` / 循环仍可按原 fallback 执行 | **通过**（仅改观测用 `final_mode`，未改 `step1_tool` 赋值逻辑） |
| **B-5** | 契约 | 未增删 `router.decision` 的 payload **键名** | **通过**（仅改 `final_mode` **取值**） |
| **B-6** | 自动化 | `pytest tests/test_unified_chat_backend_v2_agent.py -q` | **通过**（11 passed） |
| **B-7** | 契约门禁 | `python tools/tech_graph_contract_check.py` | **通过**（OK） |
| **B-8** | 用例与本地 env | 澄清用例断言 `final_mode == text2sql`；日记用例对 `INTENT_MIN_CONFIDENCE` **显式 0.6** | **通过**（见 `tests/test_unified_chat_backend_v2_agent.py`） |

**证据链（可复制到 PR）**

```bash
cd ai-ink-brain-api-python
pytest tests/test_unified_chat_backend_v2_agent.py -q
python tools/tech_graph_contract_check.py
```

**涉及文件**：`api/agent.py`、`api/unified_chat.py`、`tests/test_unified_chat_backend_v2_agent.py`；回填见 **§6**。

#### 5.0.1 前端验收（Ink / `ai-ink-brain` · 方案 B 首包）

> **说明**：首包 **未增删** `router.decision` 的 payload **键名**；前端仍只消费 manifest 已列字段（`prefer` / `candidate_mode` / `final_mode` / `rule_hits` / `evidence` / `fallback`）。属 **P1-4 前端任务** [`Projects/ai-ink-brain/content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`](../../../../ai-ink-brain/content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md) **闸门 B（无契约变更）** 下的 **回归烟测**；**可与后端首包分 PR**，不阻塞后端关单，但建议在合并后 **补一条通过记录**（日期 + 环境）。

| # | 验收项 | 口径 | 结果 |
|---|--------|------|------|
| **FE-1** | Timeline / `router.decision` | Unified Chat（Agent + SSE）展开 **Timeline / 调试区**；后端 **`CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1`**、`prefer=auto`，问句触发 **低置信 text2sql + 澄清短路**。同 **`run_id`** 下 **`router.decision`**：`final_mode` 与 **`candidate_mode`** 均为 **`text2sql`**（与 `agent.intent` 一致），**不得**出现 **`final_mode=rag`** 且无后续 **`rag.sources`** / RAG 工具帧 | **烟测通过 · 2026-05-31**（样本 [`docs/diary/samples/chatbi-v3-lowconf-sql-preview/`](../diary/samples/chatbi-v3-lowconf-sql-preview/)） |
| **FE-2** | 策略 B 容错 | 未知 `chain.type` / 未承诺键：不白屏、不抛未捕获异常（本首包 **无新 type**） | **通过**（沿用既有前端实现） |
| **FE-3** | 代码锚点（排障） | `components/unified-chat/UnifiedChatPageClient.tsx`（`e.type === "router.decision"` → `final_mode` / `finalMode`）、`components/chain-chat/ChainEventCard.tsx`（`router.decision` 卡片 `candidate_mode` / `final_mode`） | 若 FE-1 异常：核对 **`PY_API_URL`** 是否指向已含方案 B 的后端、**硬刷新** 避免旧 SSE |

**操作步骤（可复制）**

1. **`ai-ink-brain`**：`.env.local` 中 `PY_API_URL`（或等价 BFF 配置）指向已合并方案 B 的后端；按需开启 Agent 路径（如 `CHATBI_USE_AGENT` 等，以该仓 `PROJECT_CONFIG` / 联调文档为准）。  
2. **后端**：`CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1`；用 **`INTENT_MIN_CONFIDENCE`** 高于当前问句意图置信度等方式触发澄清（与 `docs/spec/v3-agent/text2sql/P1-4-第二次对话测试.md` 同类场景即可）。  
3. 浏览器打开 **Unified Chat** → 发送触发问句 → 在 Timeline 中找到 **`router.decision`** 与 **`agent.clarify`**。  
4. **断言**：`candidate_mode` 与 `final_mode` **均为 `text2sql`**；存在 **`agent.clarify`**；**无**「仅 final=rag 且无 RAG 执行」的孤立展示。

---

### 5.1 母单大项（与 §5.0 全量验收 / SPEC 全文对齐）— **仍 backlog**

> **合并前必绿**（后续 implementation PR）：`pytest tests -m "not intent_eval and not intent_benchmark"`

| # | 原 §5 项 | 状态 |
|---|----------|------|
| **5-1** | 方案 B **完整表述**：无矛盾或 `held` / `plan_only` 等显式字段 + 前后端可读 | **部分**：首包已消除「`final_mode: rag` 且无 RAG」；**未做** `held` 等新键（与 manifest **另 PR**）。**子项 §5-1a（首包）**：澄清短路下 `router.decision.final_mode` 与意图候选一致 — **已满足（2026-05-13）**。 |
| **5-2** | Text2SQL 低置信：SQL 草案预览 + 只读闸 + 确认后一次跑通（含 deny） | **已验收**（2026-05-31 · 子 task [`task_chatbi_v3_lowconf_sql_preview_v1.md`](../done/task_chatbi_v3_lowconf_sql_preview_v1.md) · 分支 `task/chatbi-v3-lowconf-sql-preview` · reinspect [`reinspect_chatbi-v3-lowconf-sql-preview_20260531_v1.md`](../tasks/reinspect_results/reinspect_chatbi-v3-lowconf-sql-preview_20260531_v1.md)） |
| **5-3** | RAG 低置信：检索方案级预览 + 确认后全链路 | **进行中**（子 task [`task_chatbi_v3_lowconf_rag_preview_v1.md`](task_chatbi_v3_lowconf_rag_preview_v1.md) · 全栈 · 先 Ink Harness 再联调） |
| **5-4** | 门控：`user_confirmed` / token、`plan_id`、`gate_bypass_reason` 日志 | **未做** |
| **5-5** | pytest + contract（**全特性**） | **部分**：当前仅覆盖方案 B + 既有 Agent 用例 |
| **5-6** | `_tech_graph` 双轨增量（若流程结构变化） | **未要求**（首包未改流程图节点语义；可选后续在 `11_flow_*` 补一句） |

---

### 5.2 关单建议用语（评审 / 自己备注）

- **若只合并「方案 B 首包」**：可写 — *「本 PR 仅完成 `task_chatbi_v3_low_confidence_plan_preview_confirm_v1_AGENT_PROMPT.md` 方案 B；`task_chatbi_v3_low_confidence_plan_preview_confirm_v1` **§5.1 整单仍为 backlog**；**§5-1** 子目标「假 rag」已通过 **§5-1a** 满足。」*  
- **勾选策略**：**§5.0** 整表视为首包关闭；**§5.1** 保持未勾全直至 5-2～5-4 等后续 PR 落地。  
- **前端**：**§5.0.1** 烟测可与后端 **分 PR**；建议在 Ink 或本任务 **§6** 补 **FE-1 通过日期**。

---

## 6. 实现备忘（回填）

- **验收分列**：首包 **§5.0**（B-1～B-8）已关闭；母单 **§5.1**（5-1～5-6）续拆 PR。  
- **2026-05-12（文档真值）**：已在 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` **§C** 增加 **P2 延伸占位说明**；已在 `.env.example` 增加 **规划中** 注释块（尚无代码可读 `env`）。  
- **2026-05-13（文档）**：**§5.0.1** 增补 **Ink 前端验收**（FE-1～FE-3 + 操作步骤）；**`Projects/ai-ink-brain/content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`**「手动测试」增加 **§4** 与方案 B 联调条目。  
- **2026-05-13（方案 B 首包 · 执行交代 `…_AGENT_PROMPT.md`）**：澄清短路前 **`router.decision.final_mode`** 与 **`candidate_mode`** 对齐为 **`intent.mode`（text2sql）**，不再沿用 fallback 的 **`step1_mode`（rag）**；避免「假 RAG、无工具调用」。实现：`api/agent.py`（提前 `_clarify_eligible` + G2 emit）、`api/unified_chat.py`（移除 JSON/SSE replay 下对 `clarify_short_circuit` 的 `final_mode→fallback` 覆盖）；`tests/test_unified_chat_backend_v2_agent.py`：`final_mode` 断言改为 **`text2sql`**；**`test_v2_natural_diary_query_rag_empty_fallback_to_direct`** 内固定 **`INTENT_MIN_CONFIDENCE=0.6`**，避免开发者 `.env` 提高阈值导致与启发式 rag 置信度不一致。PR：本地未开 PR 时填「无」。  
- 涉及文件列表：`api/agent.py`、`api/unified_chat.py`、`tests/test_unified_chat_backend_v2_agent.py`、本任务 §6  
- 新增 env：无（沿用既有 `CHATBI_V3_LOW_CONFIDENCE_CLARIFY` 等）  
- Ink 任务单：`Projects/ai-ink-brain/content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md`（**§5.0.1** 前端烟测步骤；本首包 **无 Ink 代码变更**）

---

## 7. 给 Cursor 的稳定关键词

`低置信`、`方案预览`、`用户确认`、`plan_execution_token`、`effective_confidence`、`方案B`、`§5-1a`、`§5.0.1`、`FE-1`、`router.decision`、`agent.clarify`、`INTENT_MIN_CONFIDENCE`、`task_chatbi_v3_low_confidence_plan_preview_confirm_v1`、`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm`、`UnifiedChatPageClient`
