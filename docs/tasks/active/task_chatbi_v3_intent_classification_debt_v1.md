# Task：ChatBI V3 —— 意图识别欠债（预留 **Intent vNext** 版本升级）

> **状态**：`backlog`（**不阻塞**当前 Text2SQL / RAG 主线；后续单独开 **Intent 升级** 批次时以此单为母索引）  
> **schedule_ref**：RECENT §1.1 #6  
> **登记日期**：2026-05-13  
> **统筹入口**：`docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md`  
> **V3 总规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` **§3**（任务归拢表）；**P3+ 远期 Intent（多候选 + 裁判）** 见总规 **§2.1**  
> **实现真值（当前）**：`api/intent_agent.py`（`decide_intent_v2` / `_llm_decide_v2`）、`api/intent_router.py`（V1 规则路由）、`api/agent.py`（`prefer` 覆盖与步进编排）

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Intent vNext 母单 backlog；implementation 另开 |
| **semi_auto** | `false` |
| **audit_profile** | `human_only` |
| **git_branch** | — |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | — | backlog 母单 |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | Intent 升级后路由漂移 | 见 implementation 子 task | — | — |

---

## 1. 背景：为何单独记一笔「欠债」

当前 **单轮、单工具标签**（`rag_search` | `text2sql_query` | `direct_answer`）+ **Prompt 内显式边界表**（例如「表有哪些字段」→ `rag_search`）在多数场景可用，但在 **复合意图**、**「文档式表结构」与「真实库 DDL / DML」语义重叠** 时，易出现 **整句被前半句主导** 的路由结果，与用户对「查库 / 改库」的预期不一致。

典型讨论用例（**不**要求本单内改 prompt）：

- 用户：**先**「获取某表结构」**再**「插入测试数据」——前半在边界提示中与 **「heros 表有哪些字段」→ rag** 同型，易导致 **intent → rag**，而后半 **INSERT** 未被 **text2sql** 路径优先覆盖。

此类问题涉及 **产品语义、Prompt 版本、是否多标签 / 分步计划、与 Router 的先后关系**，适合在 **Intent 专门版本升级** 中统一设计，故本单仅 **登记欠债与升级方向**，避免与 multiturn 母单（值域 / §4.3）混为一谈。

---

## 2. 欠债条目（实施时拆子任务 / PR）

| # | 主题 | 说明 | 升级时可选方向（**非承诺**，仅备选型） |
|---|------|------|----------------------------------------|
| A | **复合意图与单标签** | 一句多目标时，单一 `tool` 难以覆盖；易被 **Prompt 表格首匹配** 带走。 | 多标签、置信分工具、或 **Planner** 输出有序子步；与 `agent.think` 对齐可观测性。 |
| B | **「表结构 / 字段」语义** | 文档中的 DDL 说明 vs **连接真实库** 的 schema / introspection vs **text2sql_execute** 内预取，三条路径产品上要划清。 | 修订 `intent_agent` 边界表与 few-shot；或与 **schema_prefetch** 能力在文案上对齐「何时必须 text2sql」。 |
| C | **与 `prefer` / Router 的关系** | `prefer` 强制可绕过 LLM intent；Router 证据与 intent 结论可能不一致时的 **仲裁** 规则未总规化。 | 总规或 L1 子规中写清 **优先级链**；必要时增加 **冲突时的 SSE / 日志** 字段。 |
| D | **启发式降级** | `intent_agent._heuristic_decide` 在 LLM 不可用时默认偏 `rag_search`，与「写库」类口语的交集待盘点。 | 关键字 / 结构化信号（如 `structured_signals`）补强；与 level gate 协同。 |
| E | **评测与回归集** | Intent 升级易引入 **路由漂移**；需固定 **黄金问句集**（含复合句、表名、中英混写）。 | 对齐 `SPEC-ChatBI-V3-Evaluation.md`；pytest + 可选离线 JSON 断言。 |
| F | **多候选意图 + 裁判融合（远期）** | 当前为 **单条** JSON（一 `tool` + 自报 `confidence`）；边界疑难时缺乏 **显式对比**。 | 见 **§2.1**（**低优先级**，Intent vNext 再立项；非当前验收项）。 |

---

## 2.1 远期候选（低优先级 · 非承诺）

> **优先级**：**P3+ / 远期**，不阻塞 Text2SQL / RAG / 权限 / P1-4 等主线；实现前须另开 implementation 任务单并走契约（若新增 SSE / `agent.intent` 载荷字段）。

**方向摘要**

1. **主意图 LLM** 输出 **Top-K 候选**（K 暂定为 **5**），每条至少含：`tool`、`reasoning`（短）、可选保留模型自报 `confidence` 作先验。
2. **裁判阶段**对 K 条再打分，取 **分数最高** 的一条作为最终 `IntentDecision`（再与 `INTENT_MIN_CONFIDENCE`、`fallback`、P1-4 澄清等现有门控衔接）。
3. **裁判实现选型（讨论结论，可迭代）**
   - **Rerank（交叉编码器 / 专用重排）**：将每条候选压成 `(query, tool+reasoning 摘要)` 对，输出可比较的分数；通常 **延迟与成本优于大 LLM**，适合作为主路径精排。
   - **LLM 裁判**：强在复杂边界与长历史；成本与解析稳定性需工程化（JSON schema、超时、降级）。
   - **混合建议**：默认 **Rerank 全量 K 条打分取 argmax**；若 **top1 与 top2 分差过小** 或 **胜者为 `text2sql_query`（高风险）** 时，再 **二次调用小 LLM** 做确认或三档裁决，以控制调用量。
4. **可观测与契约**：是否暴露 `agent.intent.candidates` / `agent.intent.judge`、日志字段与前端体积，须单独规格；解析失败或裁判超时须有 **退化策略**（例如回退为当前单条行为并打标 `used: "degraded"`）。
5. **评测**：离线黄金集对比「单条 vs K+裁判」的 tool 准确率、误触 SQL 率、P95 延迟与单次成本。

---

## 3. 非范围（本 backlog 单不包干）

- 不在本单内 **重写** 当前 `intent` prompt 或 **改** `router.decision` 阈值（除非另开 implementation 子任务并走 manifest / 前端对齐流程）。  
- 不替代 **`task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`**（§4.3 **指代澄清**）；二者可 **交叉引用**，但职责分离：**澄清** vs **意图分类 / 复合路由**。

---

## 4. 验收（母单级）

- [ ] 另开 **Intent vNext** implementation 任务单时，须 **回链本文件 §2** 并勾选子项。  
- [ ] 若对外契约变更（新 `chain.type` / intent 载荷），须 **`_contract_manifest.json` + `tech_graph_contract_check` + 前端 SSE 消费** 同 PR 规则。
- [ ] PR 上 `pytest` workflow 全绿（纯文档：`pytest tests -m "not intent_eval and not intent_benchmark"` 本地等价）

---

## 5. 给 Cursor 的稳定关键词

`intent`、`decide_intent_v2`、`_llm_decide_v2`、复合意图、`rag_search` vs `text2sql_query`、表结构、Prompt 边界、**Intent vNext**、多候选、K=5、裁判、Rerank、`task_chatbi_v3_intent_classification_debt_v1`
