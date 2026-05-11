# V3 待办：多轮低置信指代澄清（V2 Multiturn §4 第 3 点 / 惯称 §4.3）

## 元信息

- **状态**：`todo`（**P1-4** 首包 **implementation**；不阻塞母单其它 §2 条目另拆 PR）
- **与总规批次对应**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` **§2.1 P1-4**
- **母单（欠债清单）**：`docs/tasks/active/task_chatbi_v3_debt_from_v2_multiturn_v1.md`（**§1**、**§0.1**）
- **L1 子规**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Multiturn-Debt.md`（**§0.1** P0 衔接、**§2**、**§4** RBAC 交叉、**§5** 验收方向）
- **V2 语义锚点**：`docs/spec/v2-agent/SPEC-ChatBI-V2-Multiturn-Semantics.md` — **§4「结构化上下文」第 3 点「澄清策略」**（组织内惯称 **§4.3**：指代表意模糊或置信不足时 **SSE 追问** 优于盲执行；与总规 **§2.4** fallback / 追问精神一致）
- **RBAC 交叉**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Identity-Access.md` — 澄清话术若 **展示表名 / 候选表**，须先对齐 **按角色脱敏** 规则（见 Multiturn-Debt **§4**）；无规约前可用 **非敏感 fixture** 或 **占位文案** 收敛技术路径
- **P0 已就绪（排障留证）**：`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`；staging 建议 **`CHATBI_JSON_LOG=1`** + Timeline **`run_id`**（与 `meta.payload.run_id` / `done` 同源）做 E2E grep 对齐 — 见 Multiturn-Debt **§0.1**
- **配对前端任务（Ink-Brain）**：`Projects/ai-ink-brain/content/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_frontend_v1.md` — SSE/Timeline 澄清 UI；**新 `chain.type` 须前后端同 PR + manifest**；前端 **开工闸门** 见该文件 **§开工闸门与前后端节奏**
- **Ink BFF（默认）**：初版 **`app/api/py/unified/chat/stream/route.ts` 无新增 query/header**；若本 PR 确需新增（如 Contract 升级），在 **§实现备忘** 显式列 **`需新增：Header/Query 名 + 示例`** 并 **@ 前端任务**；否则写 **`BFF：无需变更（Ink）`**
- **事件契约**：任何新增 **`chain.type`** 或对外 SSE 形状变更，须与 **`docs/spec/v2-agent/SPEC-ChatBI-V2-Events.md`**、**`docs/_tech_graph/_contract_manifest.json`** **同 PR** 更新，并执行 **`python tools/tech_graph_contract_check.py`**

## 背景与目标

V2 已交付 grounding、`value_hints`、历史注入等，**未**实现「低置信时主动澄清一轮」。本单在 V3 落地 **澄清路径**：在表/列指代模糊或 Intent（及/或 Text2SQL 前置信号）置信不足时，**优先追问**而非硬猜 SQL；并与现有 Agent / Intent / SSE 管道可观测性对齐。

## 范围 / 非范围

- **范围**：澄清 **触发条件**（阈值与信号来源的初版可文档化 + 最小实现）、**编排位置**（Intent 前/后或专用 gate — 实现 PR 拍板）、**用户可见话术与 SSE 事件形状草案**（实现时固化为契约）、**与 `run_id` 同源日志** 的可追溯性、**至少 1 条**可重复 E2E / pytest 用例（mock 或 staging）。
- **非范围**：母单 **§2** 同义词 / `commission_structure` 字面量、DISTINCT 节能、YAML 漂移 CI、**§1** 末「集成抽检扩展」（归 **P2-2/P2-3**）；**RBAC 全量产品化**（可与 **P1-3** 设计并行，本单仅 **不越权展示** 敏感元数据）。

## 最小技术设计（首包拍板前草案）

1. **触发**：在任务单或 PR 描述中明确 **输入信号**（例：Intent 结构化字段置信度、指代消解缺失标记、规则兜底列表）；**阈值** 可 env 化或常量首版，须与验收用例一致。
2. **编排**：澄清轮应 **短路** 后续 `text2sql_execute`（或等价），避免在待确认语义上执行写风险 SQL；与 `api/agent.py` 现有 turn / tool 边界对齐（实现备忘回填具体函数）。
3. **SSE**：新事件须符合 V2 Events 扩展流程；若引入新 **`chain.type`**，遵守 manifest + `tech_graph_contract_check`。前端消费变更若在 Ink 仓，另开任务或交叉引用（本单验收可以后端 + curl/SSE fixture 为主）。
4. **RBAC**：默认 **不**在澄清气泡中裸露用户无权限的物理表名；若产品要求展示候选表，须引用 Identity-Access 已定稿的脱敏矩阵（未定稿则验收用例仅用公开表名 fixture）。

## 依赖与引用

| 文档 | 用途 |
|------|------|
| `SPEC-ChatBI-V3-Overview.md` §2.1、§3 | 批次与任务索引 |
| `SPEC-ChatBI-V3-Multiturn-Debt.md` | L1 功能债与 P0 衔接 |
| `SPEC-ChatBI-V2-Multiturn-Semantics.md` §4 第 3 点 | 产品语义来源 |
| `SPEC-ChatBI-V3-Identity-Access.md` | 表名展示与脱敏 |
| `SPEC-ChatBI-V2-Events.md` + `_contract_manifest.json` | 契约变更真值 |

## 验收标准是否要「每一项都跑一遍」

| 场景 | 要求 |
|------|------|
| **宣称本单 done / 关单合并 PR** | **§验收标准** 五项须 **全部** `- [x]`，并在 PR 或 **§实现备忘** 留 **证据链**（pytest 摘要、`contract_check` 输出、`CHATBI_JSON_LOG` grep 或留档路径、RBAC 文字拍板、图谱文件列表）。 |
| **日常迭代提交** | **不必**每 commit 做满五项；按下方 **§执行流程** 的 **门禁子集** 即可。若当次改动触及 **契约 / manifest / Agent 主路径 / 澄清话术含表名**，则 **必须** 补跑对应阶段（见表内「对应验收项」）。 |

---

## 执行流程（建议顺序 · 与验收项对齐）

> **用途**：把「先做什么、对应哪条验收」写成可执行顺序；与 P0 RUNBOOK 类似，**过程**可随 PR 微调，**关单**仍以 **§验收标准** 为准。

### 阶段 0 — 读与范围

| 步骤 | 内容 | 对应验收 | 最小产出 |
|------|------|----------|----------|
| 0.1 | 读本单 **§范围/非范围**、**§最小技术设计** | 全项前提 | PR 描述中写清「不越界」摘要 |
| 0.2 | 对照 **`SPEC-ChatBI-V3-Multiturn-Debt.md`**、V2 **`SPEC-ChatBI-V2-Multiturn-Semantics.md` §4 第 3 点** | **语义** | 触发条件与规格一致 |

### 阶段 1 — 契约门禁

| 步骤 | 内容 | 对应验收 | 最小产出 |
|------|------|----------|----------|
| 1.1 | 若 **新增/变更** 对外 SSE、`chain.type`、payload 必填键 | **契约** | **`SPEC-ChatBI-V2-Events.md`** + **`docs/_tech_graph/_contract_manifest.json`** 同 PR |
| 1.2 | 有契约变更时 | **契约** | `python tools/tech_graph_contract_check.py` 输出 **OK**（贴 PR） |
| 1.3 | 若 **未**改对外契约 | **契约** | 在 **§实现备忘** 写 **`契约：未改（跳过 manifest）`**，**不**要求跑 1.2 |

### 阶段 2 — 自动化（语义）

| 步骤 | 内容 | 对应验收 | 最小产出 |
|------|------|----------|----------|
| 2.1 | pytest：澄清分支触发、且不盲跑 Text2SQL（mock 或可控 fixture） | **语义** | `pytest <路径> -q` 绿 + PR 内一行摘要 |

### 阶段 3 — 可观测（日志与 `run_id`）

| 步骤 | 内容 | 对应验收 | 最小产出 |
|------|------|----------|----------|
| 3.1 | **`CHATBI_JSON_LOG=true`**，走通至少 **1** 次澄清路径 | **可观测** | stderr 或 `tee` 日志中，可按 **`meta`/`done` 同源 `run_id`** grep 到澄清相关行（或引用 P0 同类留档写法：`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md` **§3.4**） |
| 3.2 | （可选）与 Ink Timeline 对读 | **可观测** | 有前端仓时交叉引用其任务单；**仅后端**时 3.1 即可 |

### 阶段 4 — RBAC 交叉

| 步骤 | 内容 | 对应验收 | 最小产出 |
|------|------|----------|----------|
| 4.1 | 澄清话术 **默认**不露无权限物理表名；或脱敏 / 表白名单 | **RBAC** | 实现或 ADR 一句 + 用例仅用安全 fixture |
| 4.2 | 产品要求展示表名 | **RBAC** | 引用 **`SPEC-ChatBI-V3-Identity-Access.md`** 已定段落；未定则本单声明 **展示待 P1-3** |

### 阶段 5 — 图谱

| 步骤 | 内容 | 对应验收 | 最小产出 |
|------|------|----------|----------|
| 5.1 | 若改 Agent 主路径、澄清门控或 SSE 边 | **图谱** | **`_tech_graph/`** 双轨与代码一致 |
| 5.2 | 若仅改阈值 env、无流程边变化 | **图谱** | **§实现备忘** 写 **`图谱：N/A`** |

### 关单前浓缩核对（复制到 PR 描述）

- [ ] **契约**：1.2 **或** 1.3 已满足  
- [ ] **语义**：2.1 pytest 已绿  
- [ ] **可观测**：3.1 已留证（grep 或 md 路径）  
- [ ] **RBAC**：4.1 **或** 4.2 已文字拍板  
- [ ] **图谱**：5.1 **或** 5.2  

---

## 验收标准（实现 PR 勾选）

- [ ] **语义**：至少 **1** 条用例（pytest 或 RUNBOOK 级手工步骤）演示：在 **触发条件满足** 时走 **澄清** 分支，**不**在无确认时执行主路径 Text2SQL（或与「用户确认后继续」的明确状态机一致并在任务单描述）。
- [ ] **可观测**：在开启 **`CHATBI_JSON_LOG`** 的 staging 或测试中，澄清相关日志可与 **同一次请求的 `run_id`**（SSE `meta` / `done`）对齐检索。
- [ ] **契约**：若新增或变更对外 SSE / `chain` 形状，**`SPEC-ChatBI-V2-Events.md`**、**`_contract_manifest.json`** 已更新，且 **`python tools/tech_graph_contract_check.py`** 通过（无契约变更则本项改为：在任务单「实现备忘」注明 **未改契约** 并跳过 manifest）。
- [ ] **RBAC 交叉**：澄清话术若含表名/列名，已实现 **脱敏或白名单** 之一（引用 Identity-Access 段落或任务单 ADR）；否则验收用例 **仅使用** 无敏感争议的 fixture 表名并在任务单声明 **产品展示待 P1-3**。
- [ ] **图谱**：若改动 Agent 主路径或 SSE 边，**`_tech_graph/`** 双轨增量与代码一致（以本仓协议为准）。

## 实现备忘（由实现 Agent 回填）

- 涉及文件：`api/agent.py`、…（待填）
- 新增 env（若有）：同步 **`docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md`**、**`.env.example`**
- 与 P1-3 RBAC 文档的评审结论链接：…
- **开工闸门（前端）**：二选一贴 PR — **(A)** manifest+Events 同 PR 绿；**(B)** 无契约变更 + **payload 键白名单** 两行。**勿**让前端在无 A/B 时开工（见 Ink 前端任务 §开工闸门）。
- **SSE 脱敏样例路径**（供前端 mock / 单测）：…（可放在 `docs/spec/v3-agent/P0/` 或 PR 附件）
- **Ink BFF**：`BFF：无需变更（Ink）` 或 `需新增：…`（见元信息）

## 给 Cursor

**验收**、**非范围**、**依赖**、**图谱**、`_tech_graph`、`§4.3`、**澄清**、**低置信**、**SSE**、`chain.type`、`_contract_manifest.json`、`CHATBI_JSON_LOG`、`run_id`、`SPEC-ChatBI-V3-Multiturn-Debt`、`SPEC-ChatBI-V2-Multiturn-Semantics`

## 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 首版：P1-4 implementation 子任务自母单 §0.1 拆出 |
| 2026-05-11 | 元信息：Ink 配对路径 `Projects/…`、BFF 默认无变更、实现备忘补开工闸门 / SSE 样例 / BFF 回填 |
| 2026-05-11 | **§验收标准是否要全跑** + **§执行流程**（阶段 0–5、关单浓缩核对）；与五项验收逐项对齐 |
