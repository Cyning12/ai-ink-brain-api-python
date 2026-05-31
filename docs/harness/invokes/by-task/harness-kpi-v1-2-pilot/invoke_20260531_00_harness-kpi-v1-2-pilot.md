# Invoke 快照 · 00 总调度 · harness-kpi-v1-2-pilot

| 字段 | 值 |
|------|-----|
| hat_id | 00 |
| task_slug | harness-kpi-v1-2-pilot |
| task_path | docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md |
| git_branch | KPI_RUBRIC_v1_2 |
| kpi_rubric | KPI_RUBRIC_v1_2 |
| kpi_aggregator | 00 |
| planned_hats | 22,30,40,50,CLOSE |
| date | 20260531 |

---

## §3 调用体（快照）

```text
你正在扮演 Harness「总调度帽（00）」，严格遵循：
- docs/harness/prompts/hats/00-orchestrator.md
- docs/harness/guides/KPI_RUBRIC_v1_2.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/tasks/skills/SKILL-harness-task.md

输入：
- task：docs/tasks/active/task_harness_kpi_v1_2_pilot_v1.md
- slug：harness-kpi-v1-2-pilot
- 计划帽序列：22,30,40,50,CLOSE
- git_branch：KPI_RUBRIC_v1_2
- kpi_rubric：KPI_RUBRIC_v1_2
- kpi_aggregator：00

你必须完成：
1. 将 task 状态改为 in_progress；通读 task 元信息与 human_gate。
2. 维护阶段状态表：每帽 {pending|running|done|blocked}。
3. 开帽落盘：本消息全文 → docs/harness/invokes/by-task/harness-kpi-v1-2-pilot/invoke_YYYYMMDD_00_harness-kpi-v1-2-pilot.md，commit。
4. semi_auto 同会话派 22→30→40（各帽 invoke + Judgment；00 逐帽记 HatInstance）。
5. 50 提示用户新会话执行；收回报后继续。
6. 关账：写 task「### KPI（00）」+ experience 摘要 + CLOSE_TRACE；HG-REINSPECT 仍 pending 则停、不 merge。

禁止：代签 HG-REINSPECT；无 ### KPI（00）关账；在 main 上链式提交。

Judgment（00 · 末尾）：
- experience_capture: …
- gate/risk: HG-REINSPECT pending → merge 前须人签
- hat_self: pass | pass-with-notes | blocked
```
