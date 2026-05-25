# Task：ChatBI V3 —— 规划入口（在 V2 文档归档之后执行）

状态：**pending**（V2 文档层收口见 **`docs/tasks/done/task_chatbi_v2_docs_acceptance_archive_2026-05-11.md`**（**done**）；本入口可展开 V3 排期）  
**V3 规格真值（初版）**：`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md`（**§0 L1 子规索引**）；目录 `docs/spec/v3-agent/README.md`；L1 文件含 `SPEC-ChatBI-V3-Observability-Text2SQL.md`、`SPEC-ChatBI-V3-Logging-Trace.md`、`SPEC-ChatBI-V3-Security.md`、`SPEC-ChatBI-V3-Identity-Access.md`、`SPEC-ChatBI-V3-Resilience-Ops.md`、`SPEC-ChatBI-V3-Multiturn-Debt.md`、`SPEC-ChatBI-V3-Evaluation.md`  
**权威叙述边界**：`docs/diary/简历评估意见-2026-5-9.md`（**§三 状态分层**、**§四 技术表述**、**§五 时间线**、**§七 文档结构**）  
**企业路线图**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md`  
**已存在 V3 子单**：`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`（Text2SQL 工具链延迟与可观测，**done 2026-05-11**；**B+C 留证收口** 见 `docs/spec/v3-agent/P0/阶段B-留证-curl-stream-b-smoke-2026-05-11.md`、`…/阶段B-前端输出.md` **§归档结论**）；**分级闸门（P1-3）**：`docs/tasks/done/task_chatbi_level_gate_v1.md`（**done 2026-05-13**）；**P1-1 SQL AST**：`docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`（**done 2026-05-14**）；**P1-2 Prompt 注入 PoC**：`docs/tasks/done/task_chatbi_v3_prompt_injection_guard_poc_v1.md`（**done 2026-05-20 · PR #40 · 22 CLOSE**）；**V2 多轮/值域未纳入交付的欠债**：`task_chatbi_v3_debt_from_v2_multiturn_v1.md`（澄清 §4.3、同义词语义等，**V3 再考虑**）；**意图识别欠债（Intent vNext）**：`task_chatbi_v3_intent_classification_debt_v1.md`（复合意图 / prompt 边界等，**backlog**）

---

## 0. 本单性质（与「批次实施单」区分）

| 项 | 说明 |
|----|------|
| **本单** | **统筹 / 索引**：对齐简历话术、Gap 切片、V4 边界；**不设**独立代码验收勾选。 |
| **批次真值** | `SPEC-ChatBI-V3-Overview.md` **§2.1**（P0 / P1 / P2）；实施与 PR 以各 **子任务单** + 将来拆出的 Gap 子单为准。 |
| **是否单独「完成」** | 不要求结项为 `done` 的代码交付；随 V3 演进更新本节链接即可。 |

---

## 1. 规划顺序（与简历评估一致）

1. **对齐简历话术**：V1 已完成 / V2 主线已落地 + 简历中仍标「补强」的项（§7.1 多步 E2E、§7.2 延迟纸面）**不夸大**为已交付。  
2. **从 Enterprise Gap 抽 V3 切片**：权限（RBAC+数据权限）、安全（SQL 语法树 + Prompt 注入）、高可用（限流熔断+监控）、评估体系、结构化日志+Trace ID（见 Gap 表 **P1** 行）。  
3. **技术债与可观测先行**：已单独立单并归档 **`docs/tasks/done/task_chatbi_v3_text2sql_tool_latency_obs_v1.md`**（多轮下工具阶段 SSE/耗时归因）；V2 multiturn **收口欠债**见 **`task_chatbi_v3_debt_from_v2_multiturn_v1.md`**。**P1 安全实施单（done）**：`docs/tasks/done/task_chatbi_v3_sql_ast_text2sql_gate_v1.md`（**P1-1**）、`docs/tasks/done/task_chatbi_v3_prompt_injection_guard_poc_v1.md`（**P1-2** · CLOSE `docs/harness/reviews/by-task/chatbi_v3_prompt_injection_guard_poc_v1/task_chatbi_v3_prompt_injection_guard_poc_v1_audit_CLOSE_20260520.md`）。  
4. **V4 边界**：多租户、模型路由、A/B —— **仅排期**，不与 V3 首迭代混写同一验收口径。

---

> **优先级排序与批次交付策略**见 SPEC 总规 **`docs/spec/v3-agent/SPEC-ChatBI-V3-Overview.md` §2.1**（P0/P1/P2 三批）。

**规划要点（与 §1 同义摘要）**：对齐简历话术；从 Gap 抽切片；可观测与 multiturn 欠债见对应子单；V4 仅排期。

---

## 2. 给 Cursor 的稳定关键词

`task_chatbi_v3_planning_after_resume_v1`、`SPEC-ChatBI-V3-Overview`、`docs/spec/v3-agent`、简历评估、Enterprise Gap、V3 排期
