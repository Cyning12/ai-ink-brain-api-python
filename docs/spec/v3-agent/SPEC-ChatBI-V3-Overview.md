# ChatBI V3 — 总览（初版 SPEC）

> **状态**：`draft`（初版，2026-05-11）  
> **仓库**：`ai-ink-brain-api-python`  
> **真值层级**：本文件定义 **V3 边界、优先级叙事与任务索引**；**环境变量与路径**以 `docs/meta/PROJECT_CONFIG_AI_INK_BRAIN_API_PYTHON.md` 为准；**运行时流程**以 `docs/_tech_graph/` 与代码为准；**企业级 P0/P1 能力表**与面试叙事对齐 `docs/spec/SPEC-ChatBI-Enterprise-Gap.md` **§4.2**，本总规不复制长表以免漂移。

---

## 1. 定位：相对 V2 的增量

| 维度 | V2（`docs/spec/v2-agent/`） | V3（本文） |
|------|-----------------------------|------------|
| 目标 | Agent + Tool + 多轮 + 事件契约 **能力闭环** | **生产可运维**：可观测、安全、权限、韧性、可评估 |
| 叙述 | 总规 §7、Runner L0–L7 已收口（见 `docs/tasks/done/task_chatbi_v2_docs_acceptance_archive_2026-05-11.md`） | 在 **不推翻** V2 语义的前提下 **增量**交付：新 env、中间件、日志、可选 SSE 契约扩展 |
| 规格结构 | 多子规（Intent / Tool / Events / Multiturn …） | **先总规 + 任务单**；子规随首包落地再拆文件（如 `SPEC-ChatBI-V3-Security.md`） |

---

## 2. 范围支柱（初版 — 与 Gap §4.2 对齐）

以下按 **首批可落地** 与 **已立任务** 排序；未单列独立 task 的条目标为 **待拆任务**（规划见 `task_chatbi_v3_planning_after_resume_v1.md` §2）。

| 支柱 | 初版目标 | 说明 |
|------|----------|------|
| **可观测（Text2SQL）** | 子阶段耗时或子阶段事件、聚合快路径复用、LLM `timeout`、上下文预算复核 | 任务：`task_chatbi_v3_text2sql_tool_latency_obs_v1.md`；事件扩展须与 `SPEC-ChatBI-V2-Events.md` 及 `_contract_manifest.json` 变更流程一致 |
| **多轮技术债** | 低置信澄清 §4.3、同义词 / 枚举边界、可选漂移 CI、图谱与现网对齐 | 任务：`task_chatbi_v3_debt_from_v2_multiturn_v1.md`；规格交叉：`SPEC-ChatBI-V2-Multiturn-Semantics.md` |
| **安全** | SQL 注入：关键字之上增加 **语法树 / 只读策略** 等加强路径；Prompt 注入：输入过滤 + 输出侧校验 | Enterprise Gap **§4.2** P0；**待拆**独立 V3 安全子任务与验收 |
| **权限** | RBAC + 数据域隔离；与现 Token 方案迁移策略 | Gap P0；**待拆** |
| **高可用与运维** | 限流熔断占位、`/health` / `/ready` 契约、监控挂钩 | Gap P1；**待拆** |
| **结构化日志与 Trace** | JSON 日志、`request_id` / `run_id` 贯通（与 V2 SSE `meta` 已有字段对齐） | Gap P1；可与可观测子任务协同 |
| **评估** | 固定烟测集 / 标注样本回归 | Gap P1；**待拆** |

**明确不在 V3 首包（划入 V4 / Enterprise §4.3）**：多租户、模型路由、A/B 平台、审计合规全套 —— 仅保留在 Gap 路线图，**不与**当前 `task_chatbi_v3_*` 混写同一验收口径。

---

## 3. `docs/tasks/active` — V3 任务归拢（权威列表）

> 路径相对本仓库根 `ai-ink-brain-api-python/`。

| 任务文件 | 元状态（以任务单头部为准） | 职责摘要 |
|----------|---------------------------|----------|
| `docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md` | `planning` | V2 收口后的 **规划入口**、迭代顺序、从 Gap 抽切片 |
| `docs/tasks/active/task_chatbi_v3_text2sql_tool_latency_obs_v1.md` | `backlog` | Text2SQL **长窗口**体感治理：子阶段可观测、确定性总结、timeout、预算 |
| `docs/tasks/active/task_chatbi_v3_debt_from_v2_multiturn_v1.md` | `backlog` | V2 已交付之外的 **多轮 / 值域** 欠债（澄清、同义词、DISTINCT 节能可选、图谱） |

**不在上表但可能并行**：V2 **增量 SSE vNext**（`docs/spec/v2-agent/SPEC-ChatBI-V2-Incremental-SSE-Timeline-vNext.md`）属 **交互契约升级**，排期可与 V3 支柱 **并行**；若实现触碰 `chain.type` 扩展，仍须满足 `tools/tech_graph_contract_check.py` 与「manifest 同 PR」规则。

---

## 4. 依赖与阅读顺序（实现侧）

1. `docs/spec/v3-agent/README.md`（本目录索引）  
2. **本文** §2–§3  
3. `docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §4.2 / §4.3  
4. 对应 V2 子规（仅当改动该域时）：`SPEC-ChatBI-V2-Events.md`、`SPEC-ChatBI-V2-Multiturn-Semantics.md`、`SPEC-ChatBI-V2-Tool-Design.md`  
5. `docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md` — 开工顺序

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

---

## 7. 给 Cursor 的稳定关键词

`SPEC-ChatBI-V3-Overview`、`v3-agent`、`task_chatbi_v3_planning_after_resume`、`task_chatbi_v3_text2sql_tool_latency_obs`、`task_chatbi_v3_debt_from_v2_multiturn`、`Enterprise Gap` §4.2、可观测、RBAC、语法树、Trace ID
