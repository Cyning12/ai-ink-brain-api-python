# Loop Manifest · ChatBI P2 韧性（R1–R2 + META）

> **git_branch**（各 round 相同）：`task/chatbi-v3-p2-loop-v1`  
> **母 task**：`docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md`  
> **全链启动**：[`PROMPT_START_chatbi_v3_p2_loop_full_chain_v1.md`](./PROMPT_START_chatbi_v3_p2_loop_full_chain_v1.md)  
> **前置**：PR **#86**（P2-1b）· PR **#87**（W1）已合 `main` · **禁止** 再开旧双轨分支

| round | task_path（active → done） | task_slug | freeze_id | 上一轮回填 |
|-------|---------------------------|-----------|-----------|------------|
| **R1** | `docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md` | `chatbi-v3-p2-loop-r1-closeout` | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` | — |
| **R2** | `docs/tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md` | `chatbi-v3-p2-loop-r2-circuit-breaker` | `SPEC-ChatBI-V3-Resilience-Ops@2026-05-11` | R1 须在 `done/` · #0b/#W1 已归档 |
| **META** | `docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md` | `chatbi-v3-p2-loop` | `CHATBI-P2-LOOP@2026-05-29` | R1+R2 均 `done/` |

**顺序（硬）**：**R1 → R2 → META**  
**Loop 成功判据**：R2 **50 必落盘** · META 后 **`REPORT_completion_chatbi_v3_p2_loop_v1.md`**
