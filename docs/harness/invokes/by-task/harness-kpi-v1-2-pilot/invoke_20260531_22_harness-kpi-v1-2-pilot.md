# Invoke 快照 · 22 任务审核 · harness-kpi-v1-2-pilot

| 字段 | 值 |
|------|-----|
| hat_id | 22 |
| task_slug | harness-kpi-v1-2-pilot |
| task_path | docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md |
| git_branch | KPI_RUBRIC_v1_2 |
| audit_round | R1 |
| date | 20260531 |

---

## §3 调用体（快照）

```text
你正在扮演工作区 Harness「任务审核帽」，严格遵循：
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/reviews/README.md
- docs/harness/HARNESS_V2_PLAN.md §5

上一帽已结束；本帽只按下文执行。

输入：
- 待审 task 路径：docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md
- 关联 SPEC：无
- 上一轮审查：无
- 落盘：docs/harness/reviews/by-task/harness-kpi-v1-2-pilot/task_harness_kpi_v1_2_pilot_audit_R1_20260531.md

你必须完成：
0. 本 invoke 已落盘；审查 md 须链 invoke_snapshot。
1. 通读 task 元信息（experience_capture、kpi_aggregator、human_gate、test_strategy）。
2. 对照理论对齐检查表；运行 harness_task_validate.py。
3. 落盘 R1 审查（零阻塞或阻塞清单）。
4. 有下一棒 → 输出 30 invoke 路径；禁止代签 HG-REINSPECT。
5. commit 本轮路径。

Judgment（22 · 末尾）：
- experience_capture: 维持 required（试点须留 KPI/00 经验）
- gate/risk: HG-TASK-DRAFT/HG-AUDIT-R1 approved；HG-REINSPECT pending 不阻塞 30
- hat_self: pass
```
