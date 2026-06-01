# ChatBI V3 — 低置信方案预览与用户确认（后 P1-4 需求）

> **状态**：`draft`（**需求真值**；实现前须拆 **implementation** 任务单并走契约 / manifest）  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2** 多轮支柱、**§2.1**「P2 延伸」  
> **前置已交付**：[`task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`](../../tasks/done/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md)（P1-4 低置信 **澄清短路**）、`api/agent.py` 编排  
> **实施任务单**：[`task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md`](../../tasks/active/task_chatbi_v3_low_confidence_plan_preview_confirm_v1.md)  
> **环境变量真值（实现后回填）**：`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` **§C**（当前为 **规划中占位说明**，无新增可读 `env`）  
> **交叉**：[`SPEC-ChatBI-V3-Multiturn-Debt.md`](SPEC-ChatBI-V3-Multiturn-Debt.md)、[`SPEC-ChatBI-V3-Identity-Access.md`](SPEC-ChatBI-V3-Identity-Access.md)（预览中的敏感表名）、[`SPEC-ChatBI-V3-Security.md`](SPEC-ChatBI-V3-Security.md)（预览 SQL 仍须 AST/只读语义）

---

## 1. 背景与待解决问题

**P1-4 现状**：`CHATBI_V3_LOW_CONFIDENCE_CLARIFY` 开启且 `intent.confidence < INTENT_MIN_CONFIDENCE` 时，对 **`text2sql_query`** 可走 **`agent.clarify`** 短路，**不执行** Text2SQL / RAG 全链路。用户可见话术偏「请补充」，**缺少**对「若继续执行，系统**打算**怎么做」的可审阅材料。

**编排与观测**：低置信时 **`intent.fallback`** 会把首步工具切到 `rag_search`，但澄清短路在工具循环前 **`return`**，导致 Timeline 上出现 **`router.decision.final_mode: rag`** 却 **无任何工具执行**，易误解为「已转 RAG」。（讨论稿中的 **方案 B**：**先**判定澄清 / 方案阶段，**再**决定是否应用 `fallback` 到首步工具，或 **方案阶段单独 emit**，避免「假 rag」。）

**目标**：在 **text2sql** 或 **rag** 路径因 **意图置信度不足** 而可能中断时，仍向用户暴露 **可审阅的执行方案草案**（用于判断是否改问法、改 `prefer`、或 **显式确认后放行**），并在用户确认后 **以产品认可的方式** 通过原有意图门槛（见 **§4**），完成全链路。

---

## 2. 范围摘要

| 维度 | 要求 |
|------|------|
| **触发域** | **`text2sql_query`** 与 **`rag_search`** 在 **`prefer=auto`** 下因 **意图置信度** 低于 `INTENT_MIN_CONFIDENCE`（或与 P1-4 / fallback 规则叠加）而**可能不执行完整链路**的场景（具体触发组合由任务单与 env 开关收敛，**默认**建议保持与现网兼容的 **opt-in**）。 |
| **方案 B（编排）** | **澄清 / 方案预览** 判定 **早于** 将 `step1_tool` 替换为 `intent.fallback` 的对外观测；或 **`router.decision`** 在「仅方案、未执行」阶段显式标注 **`held`** / **`plan_only`** 类语义，避免 **`final_mode: rag`** 与「未执行 RAG」矛盾（字段名以 **manifest 同 PR** 为准）。 |
| **Text2SQL 预览** | 输出 **拟执行** 的 **SQL 草案**（及可读说明：涉及表、只读/变更意图、是否命中 schema_prefetch）。草案 **不得**跳过 **SQL AST / 表策略** 等 **只读预览闸**（可执行「生成 SQL」子路径若已有，则 **预览 ≠ 执行**；若尚无独立生成步，须在任务单中拆 **「仅生成不执行」** API 或复用现有 phase）。 |
| **RAG 预览** | 输出 **拟执行** 的检索侧草案：例如 **rewrite 后的检索 query**、**计划召回条数 / 过滤域**，或 **轻量预检索** 的 **标题级** 摘要（**非**完整正文泄露；与 **Logging** 脱敏策略一致）。 |
| **用户确认** | 前端（或 API）提供 **显式** 动作：**按识别方案执行** / **取消** / **编辑后重试**（编辑路径可走新用户句，不强制本单内做完）。 |
| **置信度与门槛** | 用户 **确认按方案执行** 后，**不得**伪造模型原始 `confidence`；应采用 **`user_plan_confirmed`**（命名示意）等 **服务端事实** + **单次或同 `run_id` 续跑** 的门控：**有效意图门槛** 视为满足（例如 **`effective_confidence = max(reported, INTENT_MIN_CONFIDENCE)`** 仅在该确认流生效），或 **`plan_execution_token`**（短时、绑定 `run_id` + `principal`）校验通过后放行 **一轮** 工具执行。须 **JSON 日志 / 审计字段** 记录确认事件。 |

---

## 3. 非范围与安全约束

- **不**以「把模型 JSON 里的 `confidence` 数字改掉」作为唯一手段对外展示（避免与事实不一致）；展示层可区分 **`model_confidence`** vs **`gate_effective`**。  
- **不**在未经 **AST / 策略** 的情况下把 **写操作** SQL 当「安全预览」全文展示给低权限用户（须 **Identity-Access** 脱敏规则）。  
- **不**替代 **Intent vNext** 多候选 + 裁判（见 `task_chatbi_v3_intent_classification_debt_v1.md` §2.1）；二者可 **先后** 立项。

---

## 4. 置信度升格（产品语义 · 须实现拍板）

以下 **择一或组合**（implementation 任务单中拍板并写 pytest）：

1. **确认令牌（推荐）**：首条响应下发 `plan_id` + **`plan_execution_token`**（短 TTL、绑定主体与方案哈希）；用户点击「执行」后，后续请求携带 token，**仅该次** 跳过「低于 `INTENT_MIN_CONFIDENCE` 则 clarify」分支，**仍**走完整 SQL gate / RBAC。  
2. **会话内标志位**：服务端 `session` 存储 `pending_plan_confirmed`（风险：多标签页并发须版本号）。  
3. **`effective_confidence`**：确认后本连接内一次 **`max(reported, threshold)`** 仅用于 **门控比较**，日志中 **并列**写入 `model_confidence` 与 `user_confirmed_bypass`。

**禁止**：无确认、仅凭客户端传任意 `confidence` 字段绕过门槛。

---

## 5. 契约与可观测（草案）

- 新增或扩展 **`chain.type`**（示例名，以契约 PR 为准）：如 **`agent.plan.preview`**（payload：`tool`、`sql_draft` / `rag_plan`、`warnings`、`plan_id`）、**`agent.plan.confirm`**（用户动作回传由 **BFF/API** 定义）。  
- **`tech_graph_contract_check.py`** + **`_contract_manifest.json`** + **Ink SSE 消费** 同 PR 更新。  
- **`CHATBI_JSON_LOG`**：字段建议含 `plan_id`、`intent_tool`、`model_confidence`、`gate_bypass_reason=user_confirmed_plan`。

---

## 6. 验收方向（母规级）

- [x] 低置信 **Text2SQL**：Timeline 可见 **SQL 草案预览**（或等价结构化字段），用户 **确认后** 可完成 **一次** 与预览一致的执行（或明确「预览已过期」错误）。（2026-05-31 · [`task_chatbi_v3_lowconf_sql_preview_v1.md`](../../tasks/done/task_chatbi_v3_lowconf_sql_preview_v1.md) · `agent.plan.preview` + `plan_execution_token` + pytest G1–G4）  
- [x] 低置信 **RAG**：可见 **检索方案** 级预览；确认后完成 RAG 全链路。（2026-05-31 · [`task_chatbi_v3_lowconf_rag_preview_v1.md`](../../tasks/done/task_chatbi_v3_lowconf_rag_preview_v1.md) · `clarify_plan_once` + `rewrite_query` + pytest G1–G7）  
- [x] **方案 B（首包 · 2026-05-13）**：澄清短路路径上不再出现「**`final_mode: rag`** 且无 **`rag_search`**」的误导组合（实现见任务单 **§5.0**；**`held` / `plan_only` 显式字段**仍待 **§5.1**）。  
- [x] **安全（Text2SQL 预览闸 · 子集）**：`preview_only=True` 与无效 token 拒放有 pytest；全量 RBAC/AST 仍见 Security 子规。（2026-05-31 · 同上子 task）

---

## 7. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-12 | 初版：方案 B + text2sql/rag 预览 + 用户确认 + 置信度升格语义 |
| 2026-05-12 | 元信息：增加 **PROJECT_CONFIG §C** 占位与 **`.env.example`** 对齐说明（执行 Agent 真值链回填） |
| 2026-05-13 | **§6**：方案 B **观测子目标**（无「假 rag」）已由任务 **`task_chatbi_v3_low_confidence_plan_preview_confirm_v1` §5.0** 首包满足；**held** / SQL 预览 / token 等仍 backlog（任务单 **§5.1**） |
| 2026-05-31 | **§6**：低置信 Text2SQL 预览 + token 放行（**5-2**）由子 task `task_chatbi_v3_lowconf_sql_preview_v1` 关账；RAG 预览（5-3）仍 backlog |
| 2026-05-31 | **§6**：低置信 RAG 预览 + token 放行（**5-3**）由子 task `task_chatbi_v3_lowconf_rag_preview_v1` 关账 |
