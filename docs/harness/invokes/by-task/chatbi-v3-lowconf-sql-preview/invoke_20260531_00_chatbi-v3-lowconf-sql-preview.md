# Invoke 快照 · 00 总调度 · chatbi-v3-lowconf-sql-preview

| 字段 | 值 |
|------|-----|
| hat_id | 00 |
| task_slug | chatbi-v3-lowconf-sql-preview |
| task_path | docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md |
| git_branch | task/chatbi-v3-lowconf-sql-preview |
| freeze_id | CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31 |
| test_strategy | required |
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
- task：docs/tasks/active/task_chatbi_v3_lowconf_sql_preview_v1.md
- slug：chatbi-v3-lowconf-sql-preview
- 计划帽序列：22,30,40,50,CLOSE
- git_branch：task/chatbi-v3-lowconf-sql-preview
- kpi_rubric：KPI_RUBRIC_v1_2
- kpi_aggregator：00
- freeze_id：CHATBI-LOWCONF-SQL-PREVIEW@2026-05-31

你必须完成：
1. 将 task 状态改为 in_progress；通读 task §0 re-baseline、human_gate、test_strategy: required。
2. 维护阶段状态表：每帽 {pending|running|done|blocked}。
3. 开帽落盘：本消息全文 → docs/harness/invokes/by-task/chatbi-v3-lowconf-sql-preview/invoke_20260531_00_chatbi-v3-lowconf-sql-preview.md，commit。
4. semi_auto 同会话派 22→30→40（各帽 invoke + Judgment；00 逐帽记 HatInstance）。
   - 30 范围：§2 G1–G4（无效 token deny、SSE parity、预览失败、只读闸）；非 api/ 大重构。
   - 须 pytest 先红后绿 + tech_graph_contract_check。
5. 50 提示用户新会话 Fresh Context；收回报后继续。
6. 关账：写 task ### KPI（00）+ experience 摘要 + CLOSE_TRACE；G5 同步母单 §5.1 5-2。

禁止：代签 human_gate；无 ### KPI（00）关账；在 main 上链式提交；把母单「5-2 未做」当 greenfield。

Judgment（00 · 末尾）：
- experience_capture: 维持 recommended | 关账后是否升 required
- gate/risk: HG-* 已预批 approved；50 仍须独立复检
- hat_self: pass | pass-with-notes | blocked
```
