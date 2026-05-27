# Loop Manifest · P2 后续（R1–R3 + META）

> **git_branch**（各 round 相同）：`task/wiki-loop-p2-followup-v1`  
> **母 task**：`docs/tasks/active/task_harness_wiki_loop_p2_followup_v1.md`  
> **全链启动**：[`PROMPT_START_loop_p2_followup_full_chain_v1.md`](./PROMPT_START_loop_p2_followup_full_chain_v1.md)  
> **前置**：AB-REP **done** · P1-4 工作区 task 已起草 · **禁止** 与前端 parity 混 PR

| round | task_path（active → done） | task_slug | freeze_id | 上一轮回填 |
|-------|---------------------------|-----------|-----------|------------|
| **R1** | `docs/tasks/active/task_governance_t4_spec_active_v1.md` | `gov-t4-spec-active` | `GOV-T4-SPEC-ACTIVE@2026-05-27` | — |
| **R2** | `docs/tasks/active/task_governance_l2_phase_c_design_v1.md` | `gov-l2-phase-c-design` | `GOV-L2-PHASE-C-DESIGN@2026-05-27` | R1 须在 `done/` |
| **R3** | `docs/tasks/active/task_governance_wiki_ingest_batch_2_v1.md` | `gov-wiki-ingest-batch-2` | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` | R2 须在 `done/` |
| **META** | `docs/tasks/active/task_harness_wiki_loop_p2_followup_v1.md` | `wiki-loop-p2-followup` | `WIKI-LOOP-P2-FOLLOWUP@2026-05-27` | 三轮均 `done/` |

**顺序（硬）**：**R1 → R2 → R3 → META**  
**Loop 成功判据**：各 round invoke **C2 全绿** · META 后 **`REPORT_completion_*`**
