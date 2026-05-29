# Task Schedule Read Smoke — 结论文（accepted）

| 项 | 内容 |
| --- | --- |
| **freeze_id** | `TASK-SCHEDULE-READ-SMOKE@2026-05-29` |
| **关联交付** | `GOV-TASK-SCHEDULE-WIKI@2026-05-29` · [`task-schedule-ink-backend`](../../../coding_wiki/concepts/task-schedule-ink-backend.md) |
| **date** | 2026-05-29 |
| **Agent 平台** | Claude Code |
| **model** | Kimi-code |
| **证据** | [`scorecard.md`](./scorecard.md) · [`questions.md`](./questions.md) |

---

## 1. 实验结论（签收）

| 测试项 | 结果 | 说明 |
| --- | --- | --- |
| Q1 当前实现棒 | **pass** | `task_chatbi_v3_p2_resilience_rate_limit_v1`（P2-1b 限流） |
| Q2 P2 先后 | **pass** | 限流 → 熔断；母单 + RECENT 依赖 |
| Q3 L1 vs L2 | **pass** | RECENT/task 为排期真值；Wiki 为 L2 叙事 |
| Q4 陷阱（Wiki 当前棒） | **pass** | T4 ops / hub **done**；业务线优先 |

**裁决**：**接受** — 在 **无 Prompt 路径引导** 下，三方 Agent 可正确读取排期真值与 L1/L2 边界。

---

## 2. 对排期 hub 设计的影响

| 项 | 结论 |
| --- | --- |
| concept hub 是否必经 | **否** — 本 run 经 RECENT + AGENTS 即够 |
| hub 价值 | 聚合 active 表 · Epic 分区 · 反孤岛字段说明；新 Agent 仍建议 index → concept |
| RECENT 维护 | §1/§6.6 快照可被 Q4 正确消费 |

---

## 3. 局限

- 单 Agent · 单模型（Kimi-code）· 四题独立会话（由人执行，未自动化物化载荷）。  
- Open Folder 仅本后端子仓；未测工作区跨仓 RECENT。  
- 未测「仅 Wiki 读序、不读 RECENT」臂（非本 smoke 范围）。

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-29 | v1 accepted · Claude Code · Kimi-code · 4/4 pass |
