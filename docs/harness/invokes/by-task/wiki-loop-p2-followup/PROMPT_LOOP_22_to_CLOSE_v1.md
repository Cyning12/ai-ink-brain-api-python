# Loop 22→关账 · P2 后续（各 round 替换表）

> **用途**：R1/R2/R3 各轮 **22 → 30 → 40 → 50 → 关账**；**禁止** 再开 10。  
> **母单**：`docs/tasks/active/task_harness_wiki_loop_p2_followup_v1.md`

---

## §3 可复制 Prompt（替换 `{round}` / `{task}` / `{task_slug}` / `{freeze_id}`）

```text
你正在 ai-ink-brain-api-python 执行 Wiki Loop P2 后续 **{round}**：**22 → 30 → 40 → 50 → 关账**（跳过 10）。

【元信息】
- round: {round}
- task: docs/tasks/active/{task}
- task_slug: {task_slug}
- freeze_id: {freeze_id}
- git_branch: task/wiki-loop-p2-followup-v1
- 母 task: docs/tasks/active/task_harness_wiki_loop_p2_followup_v1.md
- invoke 目录: docs/harness/invokes/by-task/wiki-loop-p2-followup/
- SPEC: docs/spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md
- semi_auto: true
- cross_round_semi_auto: true（仅 R1 启动 Prompt 含【授权】时生效）

【步骤】
0. 确认 HG-LOOP-BATCH approved；上一 round（若有）已在 done/
1. 22：R1 审计 task + SPEC；落盘 invoke_YYYYMMDD_22_*.md §3 ≥15 行
2. 30：执行本 round 交付；R3 前确认 HG-INGEST-BATCH-2-SCOPE
3. 40：自检 C2 清单
4. 50：独立复检 → docs/tasks/reinspect_results/
5. 关账：git mv task → done/ · 更新 _views/done.md · RECENT §6.6
6. 若 {round} ≠ META：按 LOOP_MANIFEST 续下一 round（同会话）
7. 若 META：REPORT_completion_wiki_loop_p2_followup_v1.md + CLOSE_TRACE

硬约束：单 PR · docs-only · 不改 api/tests/prompts/CI
```

---

## round 替换表

| round | task | task_slug | freeze_id |
| --- | --- | --- | --- |
| R1 | `task_governance_t4_spec_active_v1.md` | `gov-t4-spec-active` | `GOV-T4-SPEC-ACTIVE@2026-05-27` |
| R2 | `task_governance_l2_phase_c_design_v1.md` | `gov-l2-phase-c-design` | `GOV-L2-PHASE-C-DESIGN@2026-05-27` |
| R3 | `task_governance_wiki_ingest_batch_2_v1.md` | `gov-wiki-ingest-batch-2` | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` |
