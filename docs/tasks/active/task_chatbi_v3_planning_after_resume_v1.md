# Task：ChatBI V3 —— 规划入口（在 V2 文档归档之后执行）

状态：**planning**（V2 文档层收口见 **`docs/tasks/done/task_chatbi_v2_docs_acceptance_archive_2026-05-11.md`**（**done**）；本入口可展开 V3 排期）  
**权威叙述边界**：`docs/diary/简历评估意见-2026-5-9.md`（**§三 状态分层**、**§四 技术表述**、**§五 时间线**、**§七 文档结构**）  
**企业路线图**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md`  
**已存在 V3 子单**：`task_chatbi_v3_text2sql_tool_latency_obs_v1.md`（Text2SQL 工具链延迟与可观测）

---

## 1. 规划顺序（与简历评估一致）

1. **对齐简历话术**：V1 已完成 / V2 主线已落地 + 简历中仍标「补强」的项（§7.1 多步 E2E、§7.2 延迟纸面）**不夸大**为已交付。  
2. **从 Enterprise Gap 抽 V3 切片**：权限（RBAC+数据权限）、安全（SQL 语法树 + Prompt 注入）、高可用（限流熔断+监控）、评估体系、结构化日志+Trace ID（见 Gap 表 **P1** 行）。  
3. **技术债与可观测先行**：已单独立单 **`task_chatbi_v3_text2sql_tool_latency_obs_v1.md`**（多轮下工具阶段 SSE/耗时归因）。  
4. **V4 边界**：多租户、模型路由、A/B —— **仅排期**，不与 V3 首迭代混写同一验收口径。

---

## 2. 首批可拆子任务（骨架；实施时各自建 task）

| 方向 | 建议首包 | 备注 |
|------|----------|------|
| 可观测 | Text2SQL 子阶段耗时 / 契约扩展评估 | 见 `task_chatbi_v3_text2sql_tool_latency_obs_v1.md` |
| 安全 | SQL 只读校验加强路径、Prompt 注入检测 PoC | 简历 §四：勿写「已实现语法树」除非代码落地 |
| 权限 | Admin 与数据域隔离设计文档 + API 门面 | 与 `PROJECT_CONFIG` 对齐 |
| 高可用 | 限流 + 熔断占位 + `/health` 契约 | Gap P1 |

---

## 3. 给 Cursor 的稳定关键词

`task_chatbi_v3_planning_after_resume_v1`、简历评估、Enterprise Gap、V3 排期
