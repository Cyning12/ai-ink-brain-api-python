# ChatBI V3 — 总览（初版 SPEC）

> **状态**：`draft`（初版，2026-05-11）  
> **仓库**：`ai-ink-brain-api-python`  
> **真值层级**：本文件定义 **V3 边界、优先级叙事与任务索引**；**各支柱细则**见 **§0 子规**（同级文件）；**环境变量与路径**以 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 为准；**运行时流程**以 `docs/_tech_graph/` 与代码为准；**企业级 P0/P1 能力表**与面试叙事对齐 `docs/spec/SPEC-ChatBI-Enterprise-Gap.md` **§4.2**，本总规不复制长表以免漂移。

---

## 0. 规格层级（子规索引）

| 层级 | 文件 | 职责摘要 |
|------|------|----------|
| **L0 总览** | `SPEC-ChatBI-V3-Overview.md`（本文） | 边界、支柱、任务归拢、**§2.1** 分批优先级 |
| **L1 可观测 · Text2SQL** | [`SPEC-ChatBI-V3-Observability-Text2SQL.md`](SPEC-ChatBI-V3-Observability-Text2SQL.md) | 子阶段模型、计时/SSE、timeout、与 V2 Events 边界 |
| **L1 日志 · Trace** | [`SPEC-ChatBI-V3-Logging-Trace.md`](SPEC-ChatBI-V3-Logging-Trace.md) | `request_id` / `run_id` 贯通、JSON 日志字段初版 |
| **L1 安全** | [`SPEC-ChatBI-V3-Security.md`](SPEC-ChatBI-V3-Security.md) | SQL AST/只读策略、Prompt 注入输入输出侧 |
| **L1 身份与访问** | [`SPEC-ChatBI-V3-Identity-Access.md`](SPEC-ChatBI-V3-Identity-Access.md) | RBAC、数据域、与 Tool 链接合点 |
| **L1 韧性 · 运维** | [`SPEC-ChatBI-V3-Resilience-Ops.md`](SPEC-ChatBI-V3-Resilience-Ops.md) | 限流、熔断、/health /ready |
| **L1 多轮技术债** | [`SPEC-ChatBI-V3-Multiturn-Debt.md`](SPEC-ChatBI-V3-Multiturn-Debt.md) | §4.3 澄清、同义词、DISTINCT/YAML 工程债 |
| **L1 评估** | [`SPEC-ChatBI-V3-Evaluation.md`](SPEC-ChatBI-V3-Evaluation.md) | 烟测集、标注集、CI 门禁分层 |

**维护约定**：子规内 **§修订记录** 随该域首包合并更新；总规 **§6** 仅在层级结构或批次策略变更时修订。

---

## 1. 定位：相对 V2 的增量

| 维度 | V2（`docs/spec/v2-agent/`） | V3（本文） |
|------|-----------------------------|------------|
| 目标 | Agent + Tool + 多轮 + 事件契约 **能力闭环** | **生产可运维**：可观测、安全、权限、韧性、可评估 |
| 叙述 | 总规 §7、Runner L0–L7 已收口（见 `docs/tasks/done/task_chatbi_v2_docs_acceptance_archive_2026-05-11.md`） | 在 **不推翻** V2 语义的前提下 **增量**交付：新 env、中间件、日志、可选 SSE 契约扩展 |
| 规格结构 | 多子规（Intent / Tool / Events / Multiturn …） | **L0 总规 + L1 子规**（见 **§0**）；实现细节仍以 **任务单** 与 `PROJECT_CONFIG` 为执行真值 |

---

## 2. 范围支柱（初版 — 与 Gap §4.2 对齐）

以下按 **首批可落地** 与 **已立任务** 排序；未单列独立 task 的条目标为 **待拆任务**。

| 支柱 | 初版目标 | 说明 | **L1 子规** |
|------|----------|------|----------------|
| **可观测（Text2SQL）** | 子阶段耗时或子阶段事件、聚合快路径复用、LLM `timeout`、上下文预算复核 | 任务（**done**）：`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`；事件扩展须与 `SPEC-ChatBI-V2-Events.md` 及 `_contract_manifest.json` 变更流程一致 | [`SPEC-ChatBI-V3-Observability-Text2SQL.md`](SPEC-ChatBI-V3-Observability-Text2SQL.md) |
| **多轮技术债** | 低置信澄清 §4.3、同义词 / 枚举边界、可选漂移 CI、图谱与现网对齐 | 母单：`task_chatbi_v3_debt_from_v2_multiturn_v1.md`；**P1-4 implementation**：`docs/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md`；规格交叉：`SPEC-ChatBI-V2-Multiturn-Semantics.md` | [`SPEC-ChatBI-V3-Multiturn-Debt.md`](SPEC-ChatBI-V3-Multiturn-Debt.md) |
| **安全** | SQL：语法树 / 只读策略；Prompt：输入过滤 + 输出侧校验 | Gap **§4.2** P0；待拆独立任务与验收 | [`SPEC-ChatBI-V3-Security.md`](SPEC-ChatBI-V3-Security.md) |
| **权限** | RBAC + 数据域隔离；与现 Token 迁移策略 | Gap P0；待拆 | [`SPEC-ChatBI-V3-Identity-Access.md`](SPEC-ChatBI-V3-Identity-Access.md) |
| **高可用与运维** | 限流熔断、`/health` / `/ready`、监控挂钩 | Gap P1；待拆 | [`SPEC-ChatBI-V3-Resilience-Ops.md`](SPEC-ChatBI-V3-Resilience-Ops.md) |
| **结构化日志与 Trace** | JSON 日志、`request_id` / `run_id` 贯通 | Gap P1；与 P0 可观测协同 | [`SPEC-ChatBI-V3-Logging-Trace.md`](SPEC-ChatBI-V3-Logging-Trace.md) |
| **评估** | 烟测集 / 标注回归 | Gap P1；待拆 | [`SPEC-ChatBI-V3-Evaluation.md`](SPEC-ChatBI-V3-Evaluation.md) |

**明确不在 V3 首包（划入 V4 / Enterprise §4.3）**：多租户、模型路由、A/B 平台、审计合规全套 —— 仅保留在 Gap 路线图，**不与**当前 `task_chatbi_v3_*` 混写同一验收口径。

---

## 2.1 优先级排序（三批交付）

> 排序原则：**可落地性 > 面试价值 > 工程基础 > 依赖关系**。  
> 每批验收后再启动下一批；同一批内可并行。  
> 详细规划入口见 `docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md`。

### P0 — 首包（立即开工）

> **首包形态（2026-05-11）**：Text2SQL 可观测 **SSE 子阶段 + `text2sql_phases_ms` 结构化并存**（避免仅 end 瞬间拆分后再改契约）。**Commit 节奏**：可先 **P0-1+3** 中间验收，再 **P0-2**，**最终 P0 验收** 须四项齐（见 **`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`** **§拍板 #2**、**§验收标准**；本单 **2026-05-11 已归档**）。

| 排序 | 任务 | 任务单 / 来源 | 理由 |
|------|------|---------------|------|
| **P0-1** | **可观测：Text2SQL 子阶段耗时** | `docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`（**done**） | 已有独立任务单，代码路径清晰；解决「百秒级黑盒」痛点；面试可演示「从 print 到结构化耗时」 |
| **P0-2** | **结构化日志 + Trace ID** | Gap §3.3.3 / §4.2 P1 | 与 P0-1 天然协同（耗时数据需要结构化载体）；为所有后续 V3 能力提供可观测地基 |
| **P0-3** | **LLM 调用超时与降级** | obs 任务单 §4 | 同 P0-1 代码路径；解决「无限挂起」生产级问题；改动小、价值高 |

**P0 验收标志**：多轮 Text2SQL 具备 **SSE 子阶段事件** + **`text2sql_phases_ms` 结构化分段** + JSON 日志 + `request_id`/`run_id` 贯通 + LLM 分阶段 timeout 不挂死（细则见任务单 **§拍板**）。

### P1 — 第二批（P0 验收后）

| 排序 | 任务 | 任务单 / 来源 | 理由 |
|------|------|---------------|------|
| **P1-1** | **安全：SQL 语法树分析** | Gap §3.2.1 P0 | 简历 §四明确标注「V3 升级」；依赖 P0-2 日志验证防护效果 |
| **P1-2** | **安全：Prompt 注入检测 PoC** | Gap §3.2.2 P0 | 与 SQL 安全可并行；输入过滤逻辑独立 |
| **P1-3** | **权限：RBAC 设计文档 + API 门面** | Gap §3.1 P0 | 涉及数据模型变更，需设计先行；可与安全并行设计 |
| **P1-4** | **多轮技术债：低置信澄清 §4.3** | 母单 `task_chatbi_v3_debt_from_v2_multiturn_v1.md` **§1**；implementation：`docs/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md` | 产品体验提升；需与 RBAC 设计协调 SSE 事件形状 |

**P1 验收标志**：SQL 注入从关键字升级到语法树 + Prompt 注入有输入过滤 + RBAC 设计文档评审通过 + 澄清策略有 SSE 事件定义。

### P2 — 第三批（P1 验收后）

| 排序 | 任务 | 任务单 / 来源 | 理由 |
|------|------|---------------|------|
| **P2-1** | **高可用：限流熔断 + `/health` 契约** | Gap §3.3.1–3.3.2 P1 | FastAPI 生态成熟；依赖 P0-2 日志验证限流效果 |
| **P2-2** | **评估：固定烟测集 / 回归** | Gap §3.4 P1 | 前面能力稳定后才能有效评估 |
| **P2-3** | **多轮技术债：同义词边界 / DISTINCT 节能** | `task_chatbi_v3_debt_from_v2_multiturn_v1.md` §2 | 优化项；非阻塞 |

**P2 验收标志**：限流熔断有配置 + `/health` 返回契约化 JSON + 烟测集可跑回归 + 同义词边界有文档。

---

## 3. V3 任务归拢（权威列表）

> 路径相对本仓库根 `ai-ink-brain-api-python/`。**已归档**任务见 `docs/tasks/done/`（下表 **active** 与 **done** 分列）。

| 任务文件 | 元状态（以任务单头部为准） | 职责摘要 |
|----------|---------------------------|----------|
| `docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md` | `planning` | V2 收口后的 **规划入口**、迭代顺序、从 Gap 抽切片 |
| `docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md` | `done` | Text2SQL **长窗口**体感治理：子阶段可观测、确定性总结、timeout、预算、**P0-2 JSON 日志**；**执行计划 / 验收流程** [`task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md`](../../tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1_RUNBOOK.md) |
| `docs/tasks/active/task_chatbi_v3_debt_from_v2_multiturn_v1.md` | `backlog` | V2 已交付之外的 **多轮 / 值域** 欠债（澄清、同义词、DISTINCT 节能可选、图谱） |
| `docs/tasks/active/task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md` | `todo` | **P1-4**：低置信指代 **澄清**（V2 Multiturn **§4 第 3 点** / 惯称 §4.3）；SSE / 编排 / RBAC 表名展示交叉 |

**不在上表但可能并行**：V2 **增量 SSE vNext**（`docs/spec/v2-agent/SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md`）属 **交互契约升级**，排期可与 V3 支柱 **并行**；若实现触碰 `chain.type` 扩展，仍须满足 `tools/tech_graph_contract_check.py` 与「manifest 同 PR」规则。

---

## 4. 依赖与阅读顺序（实现侧）

1. `docs/spec/v3-agent/README.md`（本目录索引）  
2. **本文** §0、§2、§2.1、§3  
3. **按所改域读 L1 子规**（§0 表）  
4. `docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §4.2 / §4.3  
5. 对应 V2 子规（仅当改动该域时）：`SPEC-ChatBI-V2-Events.md`、`SPEC-ChatBI-V2-Multiturn-Semantics.md`、`SPEC-ChatBI-V2-Tool-Design.md`  
6. `docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md` — 开工顺序

---

## 5. 验收原则（初版）

- **每个**合并到主线的 V3 能力须有：**任务单 `- [ ]` 验收** +（如涉及对外契约）**manifest / Events 补丁** + **必要时 `_tech_graph` 增量**。  
- **不**在总规写死具体毫秒 SLA；数值进任务单或测试 fixture。  
- 简历 / 对外表述：**勿**将「规划中」写为「已实现」（见 `docs/diary/简历评估意见-2026-5-9.md` §四）。

---

## 6. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版：目录 `v3-agent/`、总规、README、任务归拢三单、与 Gap / V2 关系 |
| 2026-05-11 | 增补 §2.1 优先级排序（P0/P1/P2 三批交付）|
| 2026-05-11 | **§0 规格层级**：拆 L1 子规 7 份（Observability / Logging / Security / Identity / Resilience / Multiturn-Debt / Evaluation）；§2 增「子规」列；§4 阅读顺序更新 |
| 2026-05-11 | **§2.1 P0**：首包 Text2SQL **SSE + `text2sql_phases_ms` 并存**；指向任务单 **§拍板** |
| 2026-05-11 | **§2.1 P0** 旁注：允许 **先 1+3 再 2** 的阶段 commit，**最终验收** 仍须四项齐 |
| 2026-05-11 | **§2** 多轮支柱、**§2.1 P1-4**、**§3**：登记 **§4.3 澄清** implementation 子任务 `task_chatbi_v3_multiturn_clarify_semantics_4_3_v1.md` |

---

## 7. 给 Cursor 的稳定关键词

`SPEC-ChatBI-V3-Overview`、`SPEC-ChatBI-V3-Observability-Text2SQL`、`SPEC-ChatBI-V3-Logging-Trace`、`SPEC-ChatBI-V3-Security`、`SPEC-ChatBI-V3-Identity-Access`、`SPEC-ChatBI-V3-Resilience-Ops`、`SPEC-ChatBI-V3-Multiturn-Debt`、`SPEC-ChatBI-V3-Evaluation`、`v3-agent`、`task_chatbi_v3_*`、`Enterprise Gap` §4.2
