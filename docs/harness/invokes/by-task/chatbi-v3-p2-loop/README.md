# Invoke · ChatBI V3 P2 韧性 Loop（`chatbi-v3-p2-loop`）

> **母 task**：`docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md`  
> **分支**：`task/chatbi-v3-p2-loop-v1` · **单 PR**  
> **SKILL**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../../../tasks/skills/SKILL-harness-loop-batch.md)

## 流程索引

| 步骤 | 文件 | 说明 |
|------|------|------|
| 1 | [`PROMPT_BATCH_10_chatbi_v3_p2_loop_v1.md`](./PROMPT_BATCH_10_chatbi_v3_p2_loop_v1.md) | 一次性起草（**已完成**则跳过） |
| 2 | 人批 `HG-LOOP-BATCH` → `approved` | 建议单独 commit |
| 3 | [`PROMPT_START_chatbi_v3_p2_loop_full_chain_v1.md`](./PROMPT_START_chatbi_v3_p2_loop_full_chain_v1.md) | R1 全链启动（含【授权】） |
| 4 | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) | 断点续跑 / 单 round 模板 |
| 5 | [`LOOP_MANIFEST.md`](./LOOP_MANIFEST.md) | round → task 真值 |

**META 产出**：`REPORT_completion_chatbi_v3_p2_loop_v1.md`（关账后落本目录）

## Round 摘要

| round | 交付 |
|-------|------|
| **R1** | 归档 P2-1b + W1 · RECENT hygiene |
| **R2** | P2-1c 熔断 · `api/` + pytest + **50** |
| **META** | RECENT §0/§5 · Wiki 排期 hub · 母单 `done/` |
