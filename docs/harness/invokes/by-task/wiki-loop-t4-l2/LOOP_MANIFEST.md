# Loop Manifest · T4 + L2（R1–R3 + META）

> **git_branch**（各 round 相同）：`task/gov-spec-t4-l2-v1`  
> **母 task**：`docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md`（三轮完成后 META 关账）  
> **全链启动**：[`PROMPT_START_loop_t4_l2_full_chain_v1.md`](./PROMPT_START_loop_t4_l2_full_chain_v1.md)（【授权】cross-round **仅**在此）  
> **前置**：治理 SPEC 草案已 commit（`b3a4c06`+）· C2 Verify Loop **done** · **禁止** 与烟雾 Loop 混主题

| round | task_path（active → done） | task_slug | freeze_id | 上一轮回填 | 关账后须回填 |
|-------|---------------------------|-----------|-----------|------------|--------------|
| **R1** | `docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md` | `wiki-t4-r1-pilot` | `GOV-T4-R1-PILOT@2026-05-27` | — | — |
| **R2** | `docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md` | `wiki-t4-r2-l0-align` | `GOV-T4-R2-L0-ALIGN@2026-05-27` | R1 须在 `done/` | — |
| **R3** | `docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md` | `gov-l2-r3-test-manifest` | `GOV-L2-R3-TEST-MANIFEST@2026-05-27` | R2 须在 `done/` | — |
| **META** | `docs/tasks/active/task_harness_wiki_loop_t4_l2_v1.md` | `wiki-loop-t4-l2` | `WIKI-LOOP-T4-L2@2026-05-27` | 三轮均 `done/` | — |

**顺序（硬）**：**T4 R1 → T4 R2 → L2 R3 → META**  
**Pilot synthesis（R1）**：`docs/coding_wiki/syntheses/query-rewrite-observability.md`  
**Loop 成功判据**：各 round 22/30/40/50 invoke **C2 全绿** · T4/L2 VERIFY 通过 · META 后 **`REPORT_completion_*`**（§1～§5 落盘）
