# Invoke 快照 · 00 总调度 · chatbi-v3-lowconf-rag-preview

| 字段 | 值 |
|------|-----|
| hat_id | 00 |
| task_slug | chatbi-v3-lowconf-rag-preview |
| task_path | docs/tasks/active/task_chatbi_v3_lowconf_rag_preview_v1.md |
| git_branch | task/chatbi-v3-lowconf-rag-preview |
| freeze_id | CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31 |
| test_strategy | required |
| kpi_rubric | KPI_RUBRIC_v1_2 |
| kpi_aggregator | 00 |
| planned_hats | 22,30,40,50,CLOSE |
| paired_fe | ai-ink-brain · task_chatbi_v3_lowconf_rag_preview_frontend_v1 · 72f8f0c |
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
- task：docs/tasks/active/task_chatbi_v3_lowconf_rag_preview_v1.md
- slug：chatbi-v3-lowconf-rag-preview
- 计划帽序列：22,30,40,50,CLOSE
- git_branch：task/chatbi-v3-lowconf-rag-preview
- kpi_rubric：KPI_RUBRIC_v1_2
- kpi_aggregator：00
- freeze_id：CHATBI-LOWCONF-RAG-PREVIEW@2026-05-31

前置（已完成 · 勿重复造轮子）：
- Ink FE：`ai-ink-brain` commit 72f8f0c · FE-1～FE-4 · Harness 22/30/40/50 已落盘（slug：chatbi-v3-lowconf-rag-preview-frontend）
- 契约 C1（22 拍板须双端一致）：
  - 公共：plan_id, tool, warnings, plan_execution_token, expires_in_sec
  - text2sql_query + sql_draft
  - rag_search + rewrite_query（planned_top_k, preview_headlines 可选）
- 本仓 main 仍无 RAG 低置信预览链（§0 re-baseline）；30 须实现 G1–G7 + 更新 _contract_manifest.json

你必须完成：
1. 通读 task §0–§6、human_gate；维护阶段状态表。
2. 确认 HG-TASK-DRAFT / HG-AUDIT-R1 已 approved 后再派 30（禁止代签）。
3. semi_auto 同会话：22→30→40（各帽 invoke + Judgment + commit；30 先红后绿 pytest + contract check）。
4. 30 范围：api/agent.py、chatbi_plan_token.py（purpose 扩展或通用 clarify_plan_once）、unified_chat 透传、契约、tests；对齐 Ink C1 键；非 api 大重构。
5. 50：提示用户新会话 Fresh Context；收回报后继续 CLOSE。
6. 关账：### KPI（00）、G8/G9/G10、G5 母单 5-3、diary 样本（含 FE-5 联调）、CLOSE_TRACE；全栈 FE-5 须 pass 或人签 defer。

禁止：代签 human_gate；无 ### KPI（00）关账；在 main 上链式提交；假定后端已合并 main。

Judgment（00 · 末尾）：
- experience_capture: 维持 recommended | 全栈关账后升 required
- gate/risk: 双仓 PR 契约须 merge 前一致；HG-REINSPECT 双端
- hat_self: pass | pass-with-notes
```
