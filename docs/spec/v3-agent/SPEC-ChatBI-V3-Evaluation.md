# ChatBI V3 — 评估与回归

> **状态**：`draft`  
> **父规**：[`SPEC-ChatBI-V3-Overview.md`](SPEC-ChatBI-V3-Overview.md) **§2.1** P2-2  
> **企业参考**：`docs/spec/SPEC-ChatBI-Enterprise-Gap.md` §3.4、§4.2（测试集）

---

## 1. 目标

建立 **可重复执行** 的问答 / Text2SQL / Agent 回归集合，用于：发版前冒烟、Prompt 或路由变更时的 **差分检测**（非一次性手工点测）。

---

## 2. 资产形态（初版）

| 资产 | 说明 |
|------|------|
| **烟测集** | 体量小、覆盖主路径（RAG / Text2SQL / 单步 Agent），**可**在 CI 用 mock 跑 |
| **标注集（扩展）** | 企业 Gap 所述量级目标（如百条级）为 **长期目标**；初版可先 **JSONL + 期望标签** 仓库内维护 |

**字段建议（每条用例）**：`id`、`input`、`session_fixture`（可选）、`expect_tool` 或 `expect_sql_pattern`、`tags`。

---

## 3. 执行与门禁

| 层级 | 约束 |
|------|------|
| **PR 阻断** | 与现仓 policy 一致：默认 **mock** 级烟测；真链路上游 **不**作为 merge 硬门槛 |
| **发布前** | staging 全量或抽样跑标注集；结果归档到 `docs/diary/` 或内部表（**不**写死路径于本规） |

---

## 4. 非范围

- 线上 A/B 分流与显著性检验（**V4**）。  
- 自动标注与主动学习闭环。

---

## 5. 关联

- `docs/tasks/active/task_chatbi_v3_planning_after_resume_v1.md`（排期与首批切片）  
- [`SPEC-ChatBI-V3-Observability-Text2SQL.md`](SPEC-ChatBI-V3-Observability-Text2SQL.md)（延迟归因与用例字段协同）

---

## 6. 修订记录

| 日期 | 变更 |
|------|------|
| 2026-05-11 | 初版子规 |
