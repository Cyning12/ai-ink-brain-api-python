# Task：ChatBI V3 — 低置信 RAG 预览 + 确认放行（§5-3 · 全栈）

> **状态**：`in_progress`（2026-05-31 · 00→40 本仓 G1–G7 已落地 · **50 Fresh Context 待续** · FE-5 联调待 E2E）  
> **schedule_ref**：RECENT §1.1 #4 子项 · 母单 §5.1 **5-3**  
> **登记日期**：2026-05-31  
> **父 task**：[`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`](task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md)（§5.2 已验收 · **5-3 本单**）  
> **需求真值（L1）**：[`docs/spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`](../spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md) **§2 RAG 预览**、**§4 确认令牌**  
> **前置（done）**：[`task_chatbi_v3_lowconf_sql_preview_v1.md`](../done/task_chatbi_v3_lowconf_sql_preview_v1.md)（§5-2 · 同机制 Text2SQL）· [`task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`](../done/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md)  
> **E2E 对照样本（5-2）**：[`docs/diary/samples/chatbi-v3-lowconf-sql-preview/`](../diary/samples/chatbi-v3-lowconf-sql-preview/)  
> **配对前端（done · 代码）**：`ai-ink-brain` · [`task_chatbi_v3_lowconf_rag_preview_frontend_v1.md`](../../../ai-ink-brain/content/tasks/active/task_chatbi_v3_lowconf_rag_preview_frontend_v1.md) · 实现 `72f8f0c` · Harness 22/30/40/50 已落盘（**FE-5** 待本仓 G1–G2 联调）

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **task_slug** | `chatbi-v3-lowconf-rag-preview` |
| **test_strategy** | `required` |
| **freeze_id** | `CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31`（草案 · 开跑前可钉 commit） |
| **semi_auto** | `true` |
| **audit_profile** | `full`（涉契约扩展 + 跨仓） |
| **experience_capture** | `recommended`（全栈关账后建议升 `required`） |
| **kpi_rubric** | `KPI_RUBRIC_v1_2` |
| **kpi_aggregator** | `00`（建议 · 与 5-2 同编排） |
| **git_branch** | `task/chatbi-v3-lowconf-rag-preview` |

### 阶段状态（00 维护 · 2026-05-31）

| 帽 | 状态 | 备注 |
|----|------|------|
| 00 | done | `invoke_20260531_00_*` |
| 22 | done | R1 零阻塞 · `task_*_audit_R1_20260531.md` |
| 30 | done | G1–G7 · `clarify_plan_once` + RAG preview |
| 40 | done | pytest 277 绿 · contract OK |
| 50 | pending | **须新会话 Fresh Context** |
| CLOSE | pending | 待 50 + FE-5 / HG-REINSPECT |

### 跨仓与 Harness 节奏

| 序 | 动作 | 状态 |
|----|------|------|
| 0 | 契约 **C1**（见下） | **拍板**（Ink `72f8f0c` + review R1） |
| 1 | Ink Harness + FE 代码 | **done**（`chatbi-v3-lowconf-rag-preview-frontend`） |
| 2 | 本仓 Harness 22→50 | **进行中** |
| 3 | 联调 FE-5 + diary 样本 | 待 **G1–G2** 后发 |

**C1 契约增量（22 前须与 Ink 一致）**：

- 公共键：`plan_id`, `tool`, `warnings`, `plan_execution_token`, `expires_in_sec`
- `text2sql_query` 额外：`sql_draft`
- `rag_search` 额外：**`rewrite_query`**（`planned_top_k`、`preview_headlines` 可选）

| 序 | 动作 | 落点 |
|----|------|------|
| 0 | 冻结 **契约** | 本仓 `_contract_manifest.json` ↔ Ink 已落盘镜像 |
| 1 | **Ink** task + Harness | `content/tasks/active/task_chatbi_v3_lowconf_rag_preview_frontend_v1.md` · `content/harness/invokes/by-task/chatbi-v3-lowconf-rag-preview-frontend/` |
| 2 | **本仓** Harness | `docs/harness/invokes/by-task/chatbi-v3-lowconf-rag-preview/` |
| 3 | E2E 样本 | `docs/diary/samples/chatbi-v3-lowconf-rag-preview/`（关账） |

**Open Folder**：后端实现与 Harness 落盘 → **本仓**；前端实现 → **`ai-ink-brain/`**（见工作区 `Projects/AGENTS.md` §2）。

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | 含 §6 前端范围人扫 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后；须核对契约与 Ink task 对齐 |
| HG-REINSPECT | pending | done | 50 后、合并前；**双仓** diff 须 50 书面覆盖 |

---

## 0. 现网基线（re-baseline · 2026-05-31 · `main`）

> **勿**假定 RAG 已与 Text2SQL 对称。5-2 仅覆盖 **`intent.tool == text2sql_query"`** 澄清预览链。

| 项 | 现网（摘要） | 5-3 缺口 |
|----|--------------|----------|
| 澄清短路 | `api/agent.py` · `_clarify_eligible` **仅 text2sql_query** | 须扩展 **rag_search** 低置信路径 |
| `agent.plan.preview` | 已存在 type；payload 以 **`sql_draft`** 为主 | 须增加 **RAG 方案级** 字段（见 SPEC §2） |
| `plan_execution_token` | `chatbi_plan_token.py` · purpose=`clarify_text2sql_once` | 须扩展校验/签发覆盖 **RAG 放行**（或统一 purpose 名） |
| 契约 | `payload_min_keys`: `plan_id`,`tool`,`sql_draft`,… | **MODIFIED** 增量键（与 Ink 同 PR） |
| Ink UI | `UnifiedChatPageClient` · 卡片「预览 **SQL**」· 仅展示 `sql_draft` | **须**按 `tool`/RAG 字段分支展示与文案 |
| 5-2 样本 | SQL 两轮 E2E 已归档 | RAG 须 **新建** 对照样本目录 |

---

## 1. 背景与目标

SPEC 要求：低置信 **`rag_search`** 场景下，用户在执行全链路 RAG 前可见 **检索方案级预览**（rewrite query、计划条数/过滤域或标题级摘要等），并通过与 5-2 一致的 **`plan_execution_token`** 显式确认后再执行。

**完成态（全栈）**：

- 后端：低置信 RAG 澄清 → **`agent.plan.preview`**（`tool: rag_search` + RAG 承诺键）→ **`agent.clarify`**；合法 token 续跑 → 跳过澄清并执行 **RAG 全链路**（含 `rag.sources` 等）。
- 契约：`tech_graph_contract_check` 通过；**无**未承诺键被前端强依赖。
- 前端：Timeline + 确认卡片可审阅 RAG 方案；**「按预览执行」** 携带 token + 同 `query`/`session_id`。
- 母单 §5.1 **5-3** → **已验收**；Harness + diary 标准样本落盘。

---

## 2. 范围

### 2.1 后端（本仓 `ai-ink-brain-api-python`）

- [x] **G1 RAG 澄清预览**：低置信 + `rag_search` 候选时发出 **`agent.plan.preview`**（非仅 text2sql）
- [x] **G2 RAG 预览载荷**：payload 含 `rewrite_query`、`planned_top_k`、`preview_headlines`（可选）+ 公共键
- [x] **G3 token 放行 RAG**：合法 token 续跑跳过 clarify → **rag_search** + `rag.sources`；`verify` 分工具（pytest）
- [x] **G4 预览失败**：`test_v3_rag_plan_preview_fail_json_no_token`
- [x] **G5 JSON + SSE parity**：`test_v3_rag_plan_preview_sse_parity`（无 defer）
- [x] **G6 契约**：`_contract_manifest.json` · `tech_graph_contract_check` OK
- [x] **G7 pytest**：`test_v3_rag_plan_*` + 全量 `pytest tests` 绿

### 2.2 前端（Ink `ai-ink-brain` · 本 task **验收项**，非本仓 commit）

> 详细范围写在 **§6 前端 task**；本仓关账 **阻塞**于 FE 烟测通过或书面 defer（须人签）。

- [ ] **FE-1 消费 `agent.plan.preview`**：`tool === rag_search`（或 manifest 约定值）时解析 RAG 字段，**不**仅渲染 `sql_draft`
- [ ] **FE-2 确认卡片 UX**：文案/标题由「预览 SQL」泛化为按 **tool 分支**（RAG 方案摘要 + TTL）；保留「按预览执行」「取消(丢弃令牌)」
- [ ] **FE-3 续跑 body**：`POST …/unified/chat/stream` 携带 **`plan_execution_token`**；**禁止**用户改问句仍沿用旧 token（与 5-2 一致）
- [ ] **FE-4 Timeline**：`ChainEventCard` / 执行链对 RAG preview 可读（非空白/非仅 SQL 区块）
- [ ] **FE-5 烟测留证**：两轮 Timeline 导出 + 截图 → 建议 `ai-ink-brain` 或本仓 diary **互链**（见 §6）

### 2.3 文档与 Harness（本仓）

- [ ] **G8 母单同步**：§5.1 **5-3** → **已验收**
- [ ] **G9 SPEC §6**：低置信 **RAG** 预览项勾选
- [ ] **G10 Harness**：`invokes/by-task/chatbi-v3-lowconf-rag-preview/` · review R1 · `reinspect_results/reinspect_chatbi-v3-lowconf-rag-preview_*` · **`### KPI（00）`**

## 3. 非范围

- **5-4** 全量审计字段 / `gate_bypass_reason` 产品化（另 task）
- **5-1** `held` / `plan_only` 新 manifest 键（另 PR；可与 5-3 协调但不阻塞）
- Intent vNext 多候选裁判
- 新增独立 `chain.type`（优先 **扩展** `agent.plan.preview` payload）
- GraphRAG 试点
- 「确认后必须执行预览 SQL 草案」语义（5-2 已说明 token 仅跳过澄清；RAG 同理，**不**保证预览与执行逐字一致，须在 22 留痕）

---

## 4. 行为变更（Delta）

### ADDED

- **Requirement**：低置信 RAG 澄清须下发可审阅的检索方案预览。  
  - **Scenario**：`lowconf-rag-plan-preview` — GIVEN `CHATBI_V3_LOW_CONFIDENCE_CLARIFY=1` 且 `CHATBI_V3_PLAN_PREVIEW_CONFIRM=1` 且 intent 为低置信 `rag_search` WHEN Unified Chat THEN 含 `agent.plan.preview`（`tool=rag_search`）且含 `plan_execution_token` 先于 `agent.clarify`。

- **Requirement**：用户确认后 RAG 全链路可执行。  
  - **Scenario**：`lowconf-rag-token-bypass` — GIVEN 合法 `plan_execution_token` 与同 `query` WHEN 续跑 THEN 无 `agent.clarify` 且出现 RAG 执行观测（如 `rag.sources` 或 tool 成功路径）。

- **Requirement**：前端可区分 RAG 与 Text2SQL 预览展示。  
  - **Scenario**：`fe-rag-preview-card` — GIVEN SSE 含 RAG `agent.plan.preview` WHEN 用户查看确认区 THEN 可见 RAG 方案字段（非仅「无 sql_draft」占位）。

### MODIFIED

- **Requirement**：`agent.plan.preview` 契约最小键集（Previously: 以 `sql_draft` 为中心）  
  - **Scenario**：`contract-rag-preview-keys` — GIVEN 后端发 RAG preview WHEN `tech_graph_contract_check` THEN 通过且 Ink 仅消费 manifest 承诺键。

- **Requirement**：母单 §5.1 **5-3** 状态（Previously: 未做）  
  - **Scenario**：`parent-task-5-3-closed` — GIVEN 全栈验收 WHEN 读母单 THEN **5-3** 已验收并链本 task + PR。

### REMOVED

无

---

## 5. 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| SPEC | [`SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md`](../spec/v3-agent/SPEC-ChatBI-V3-LowConfidence-Plan-Confirm.md) |
| 母单 | [`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`](task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md) |
| 5-2 子 task（done） | [`task_chatbi_v3_lowconf_sql_preview_v1.md`](../done/task_chatbi_v3_lowconf_sql_preview_v1.md) |
| 5-2 E2E 样本 | [`docs/diary/samples/chatbi-v3-lowconf-sql-preview/`](../diary/samples/chatbi-v3-lowconf-sql-preview/) |
| PROJECT_CONFIG | [`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`](../meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md) §C |
| 契约 | `docs/_tech_graph/_contract_manifest.json` |
| 代码入口 | `api/agent.py`、`api/chatbi_plan_token.py`、`api/unified_chat.py` |
| KPI / Harness | [`KPI_RUBRIC_v1_2.md`](../harness/guides/KPI_RUBRIC_v1_2.md) · [`SKILL-harness-task.md`](../tasks/skills/SKILL-harness-task.md) |
| 工作区调度 | [`Projects/AGENTS.md`](../../../../Projects/AGENTS.md) §2 |

---

## 6. 前端涉及点（Ink · 已完成 · 本仓验收引用）

> **真值 task**：`ai-ink-brain/content/tasks/active/task_chatbi_v3_lowconf_rag_preview_frontend_v1.md`  
> **实现 commit**：`72f8f0c`（`main`）· **FE-1～FE-4 pass** · **FE-5** 阻塞于本仓 RAG preview 未就绪  
> **50 复检**：`content/tasks/reinspect_results/reinspect_chatbi-v3-lowconf-rag-preview-frontend_20260531_v1.md`

### 6.1 须改模块（参考 5-2 已 done 前端 task）

| 模块 | 路径（Ink） | 变更要点 |
|------|-------------|----------|
| 主会话 | `components/unified-chat/UnifiedChatPageClient.tsx` | 解析 preview：`tool`/`rag_*` 字段；`pendingPlanConfirm` 状态；按 tool 切换卡片文案；续跑 `plan_execution_token` |
| 事件卡片 | `components/chain-chat/ChainEventCard.tsx` | `agent.plan.preview` 分支：RAG 展示块（非仅 `sql_draft` 围栏） |
| 类型 | `components/chain-chat/types.ts` | 扩展 `AgentPlanPreviewPayload`（或 discriminated union by `tool`） |
| 契约消费 | `docs/_tech_graph/_contract_manifest.json`（Ink 侧镜像/指针） | 与后端 **同 PR 或紧耦合 PR** 对齐承诺键 |
| 图谱（可选） | `docs/_tech_graph/11_flow_api*.md` | RAG 低置信预览 + token 续跑一句 |

### 6.2 前端验收（关账阻塞项）

| # | 项 | 口径 |
|---|-----|------|
| F1 | 低置信 RAG 问句 | 触发 `agent.plan.preview` + `agent.clarify`；`router.decision` 不出现 5-0 前「假 rag」回归 |
| F2 | 确认卡片 | 可见 RAG 方案摘要（非空）；TTL 倒计时；**按预览执行** / **取消** 可用 |
| F3 | 第二轮 | Network body 含 `plan_execution_token`；`query` 与首轮一致；出现 RAG 执行帧（如 `rag.sources`） |
| F4 | 改问句丢弃 token | 输入框改问句发送后不使用旧 token（与 5-2 一致） |
| F5 | 留证 | Timeline JSON ×2 + 截图；路径写入前端 task §实现备忘并 **链** 本仓 diary 样本 |

### 6.3 与 5-2 前端差异（避免复制粘贴误判）

| 维度 | 5-2（已做） | 5-3（本单） |
|------|------------|------------|
| 卡片标题 | 「低置信 · 预览 **SQL** 已就绪」 | **RAG 方案** / 按 `tool` 分支 |
| 主展示字段 | `sql_draft` | **rewrite query**、计划条数、标题级 hits 等（以实现拍板为准） |
| 执行第二轮 | Text2SQL 全链路 | **RAG** 全链路 |
| 后端澄清条件 | `text2sql_query` | **`rag_search`** |

### 6.4 Harness（Ink · 待流程更新）

- 在 **Ink 侧** 明确：`content/tasks/` task 的 invoke/review 落点（若与后端 `docs/harness/` 对称或工作区索引）。
- 本后端 task 关账时，22/50 审查 md 须含 **「前端 task 路径 + FE-1～F5 勾选」** 或 **defer 理由（人签）**。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-lowconf-rag-unconfirmed` | 低置信 RAG 未确认即执行全量 | 仍 preview / clarify | 是 | 需预览或确认 |
| F2 | `fp-lowconf-rag-token-invalid` | token 无效/过期/问句不匹配 | 拒放；仍 clarify 或无 RAG 执行 | 否 | 确认失效 |
| F3 | `fp-lowconf-rag-preview-fail` | RAG 预览生成失败 | 无 token；clarify 含失败说明 | 是 | 无法预览方案 |
| F4 | `fp-lowconf-rag-preview-off` | `CHATBI_V3_PLAN_PREVIEW_CONFIRM=0` | 仅 clarify，无 preview | 是 | 无方案预览 |
| F5 | `fp-lowconf-contract-drift` | RAG preview 键与 manifest 不一致 | contract check **fail** | 是 | CI 红 |
| F6 | `fp-fe-unknown-preview-keys` | 前端读取未承诺键崩溃 | 策略 B：不白屏（FE-2 回归） | 是 | 降级文案 |

---

## 验收标准

> **全栈** · 合并前必绿

- [ ] §2 **G1–G10** 满足；§6 **FE-1～F5** 满足或 22 书面 defer（**人签**）
- [ ] 契约 PR：**后端 + Ink** 键一致（可双 PR，但合并顺序须在 task 写明）
- [ ] `pytest tests -m "not intent_eval and not intent_benchmark"` 全绿
- [ ] `python tools/tech_graph_contract_check.py` 通过
- [ ] Harness：00/22/30/40/50 invoke · review · reinspect · **`### KPI（00）`**
- [ ] diary 样本：`docs/diary/samples/chatbi-v3-lowconf-rag-preview/`（关账轮建）
- [ ] **HG-*** → `approved` 后再 merge

**建议验证命令（后端）**：

```bash
cd ai-ink-brain-api-python
pytest tests/test_unified_chat_backend_v2_agent.py -k "lowconf and rag" -q
pytest tests/test_chatbi_plan_token.py -q
python tools/tech_graph_contract_check.py
pytest tests -m "not intent_eval and not intent_benchmark"
python tools/harness_task_validate.py docs/tasks/active/task_chatbi_v3_lowconf_rag_preview_v1.md
```

---

## 7. 计划帽链

```text
（可选）Ink Harness 流程对齐 → 00 → 22 → 30 → 40 → 50（Fresh Context）→ 00/CLOSE
并行：ai-ink-brain 前端 task（FE）· 与后端 30 互锁联调
```

| 帽 | 本仓落盘 |
|----|----------|
| 00 | `invokes/by-task/chatbi-v3-lowconf-rag-preview/invoke_*_00_*` |
| 22 | `reviews/by-task/chatbi-v3-lowconf-rag-preview/` |
| 30–50 | `invokes/...` · `reinspect_results/reinspect_chatbi-v3-lowconf-rag-preview_*` |

---

## 8. 开跑前确认（草案）

| # | 项 | 建议 |
|---|-----|------|
| C1 | 契约增量键名 | 22 前拍板：`rag_plan` 对象 vs 扁平键（`rewrite_query` 等） |
| C2 | token purpose | 扩展 `clarify_text2sql_once` 为通用 `clarify_plan_once` 或分 purpose |
| C3 | PR 策略 | **双 PR**（api-python + ink）或 monorepo 工作区一次提交 — **人择** |
| C4 | Harness | **先** Ink 侧 invoke/落盘约定，再后端 00 开帽 |
| C5 | 预览 vs 执行一致性 | 文档声明：token 仅跳过澄清，**不**保证预览草案与执行检索逐字一致 |

---

## 9. ### KPI（00）

> **由 00 / CLOSE 填写**；格式见 [`KPI_RUBRIC_v1_2.md`](../harness/guides/KPI_RUBRIC_v1_2.md)。

（占位 · 关账后删除）

---

## 10. ### 自检结论（执行者）

| 项 | 结果 |
|----|------|
| 日期 | 2026-05-31 · 40 帽 |
| `pytest tests -m "not intent_eval and not intent_benchmark"` | **277 passed**, 1 skipped |
| `pytest … -k "v3_rag_plan or v3_plan"` | **9 passed**（含 5-2 回归） |
| `python tools/tech_graph_contract_check.py` | **OK** |
| `python tools/harness_task_validate.py` | 待 50 前复跑 |
| 实现摘要 | `clarify_plan_once` token；`rag_search` 低置信预览 + bypass；`tools.rag_search_execute(preview_only)` |
| 阻塞 | **50** 须 Fresh Context；**FE-5** E2E 样本待联调；**HG-REINSPECT** pending |

---


## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-31 | v0.1 草案：§5-3 全栈 · 前端 §6 · Harness 跨仓节奏 · 依赖 5-2 |

---

## 给 Cursor

`chatbi-v3-lowconf-rag-preview`、`5-3`、`rag_search`、`agent.plan.preview`、`plan_execution_token`、Ink、`UnifiedChatPageClient`、`cross-repo`、`KPI_RUBRIC_v1_2`、`failure_paths`、`required`
