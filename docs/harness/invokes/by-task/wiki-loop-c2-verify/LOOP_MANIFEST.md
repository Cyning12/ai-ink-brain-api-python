# Loop Manifest · C2 Verify（R1–R2 + META）

> **git_branch**（各 round 相同）：`task/wiki-loop-c2-verify-v1`  
> **母 task**：`docs/tasks/active/task_harness_wiki_loop_c2_verify_v1.md`（两轮完成后 META 关账）  
> **全链启动**：[`PROMPT_START_loop_c2_verify_full_chain_v1.md`](./PROMPT_START_loop_c2_verify_full_chain_v1.md)（【授权】cross-round **仅**在此）  
> **前置**：Loop A1–A4 **done** · Loop B-Q3 Recheck **done** · meta-reinspect **C2 FAIL** · 第三批 PROMPT_LOOP C2 自检已落盘

| round | task_path（active → done） | task_slug | freeze_id | 上一轮回填 | 关账后须回填 |
|-------|---------------------------|-----------|-----------|------------|--------------|
| **R1** | `docs/tasks/active/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` | `wiki-c2-r1-schedule-draft` | `WIKI-C2-R1-SCHEDULE@2026-05-26` | — | — |
| **R2** | `docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md` | `wiki-c2-r2-index-sync` | `WIKI-C2-R2-INDEX@2026-05-26` | R1 须在 `done/` | — |
| **META** | `docs/tasks/active/task_harness_wiki_loop_c2_verify_v1.md` | `wiki-loop-c2-verify` | `WIKI-LOOP-C2-VERIFY@2026-05-26` | 两轮均 `done/` | — |

**Loop 成功判据**：各 round 22/30/40/50 invoke **§3 ≥15 行**（或文件 ≥800B）· 元信息表含 `task_slug` · **非 stub**（见 SKILL §invoke 质量门禁 C2）。
