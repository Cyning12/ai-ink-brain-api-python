# Invoke 快照 · 00/CLOSE 关账 · harness-kpi-v1-2-pilot

| 字段 | 值 |
|------|-----|
| hat_id | CLOSE |
| orchestrator | 00 |
| task_slug | harness-kpi-v1-2-pilot |
| task_path | docs/tasks/done/task_harness_kpi_v1_2_pilot_v1.md |
| git_branch | KPI_RUBRIC_v1_2 |
| kpi_aggregator | 00 |
| freeze_id | KPI-RUBRIC-PILOT@2026-05-31 |
| date | 20260531 |

---

## §3 调用体（快照）

```text
你正在扮演 Harness「总调度帽（00）· 关账轮」，严格遵循：
- docs/harness/prompts/hats/00-orchestrator.md
- docs/harness/guides/KPI_RUBRIC_v1_2.md §4–§6
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md §4 步骤 6–7

输入：
- task：docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md
- 50：docs/tasks/reinspect_results/reinspect_harness-kpi-v1-2-pilot_20260531_v1.md
- HG-REINSPECT：approved（a496d9b 人签）

你必须完成：
1. 汇总 HatInstance → task ### KPI（00）（Task_KPI% + 状态）
2. experience_capture: required → 经验摘要写入 task
3. 验收 §7 全勾选；task → done/ + _views/done.md
4. 对话输出 CLOSE_TRACE（无下一棒 Prompt）
5. commit 关账路径

Judgment（00 · CLOSE）：
- experience_capture: 维持 required（摘要已写）
- gate/risk: 无 pending 闸；可 merge PR
- hat_self: pass
```
