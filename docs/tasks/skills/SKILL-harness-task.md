# SKILL：Harness 任务执行模式（子仓指针）

> **状态**：`active`（2026-05-31）  
> **用途**：被 task / invoke 引用时，说明 **22→关账** 等模式；**执行真值** 不在本文件堆全文。

---

## 读序（Agent）

1. 本 task 正文与 `human_gate` / `semi_auto` / `experience_capture` / `test_strategy`  
2. **子仓** `docs/harness/README.md` §1（Open **本仓** 执行）  
3. **工作区协议**（跨仓 / 00 / KPI）：`Projects/docs/harness/HARNESS_V2_PLAN.md` §5.7–§5.8、[`SDD_HAT_FLOW.md`](../../../../docs/harness/SDD_HAT_FLOW.md) §0  
4. KPI 打分：[`Projects/docs/harness/guides/KPI_RUBRIC_v1_2.md`](../../../../docs/harness/guides/KPI_RUBRIC_v1_2.md)  
5. 总调度：[`Projects/docs/harness/prompts/00-orchestrator.md`](../../../../docs/harness/prompts/00-orchestrator.md)

---

## 模式摘要

| 模式 | 链 |
|------|-----|
| **22→关账** | 22 → 30 → 40 → 50 → CLOSE（可跳过 10） |
| **semi_auto** | 见子仓 `docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md` |
| **经验** | **无 60 帽**；`experience_capture` 三档 + 各帽 Judgment |

---

## 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-05-31 | v1：补全被 task 引用的指针 stub（KPI v1.2 / 00） |
