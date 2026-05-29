# 10 帽 Batch · ChatBI P2 Loop 起草（已完成 · 2026-05-29）

> **状态**：Batch 10 已完成；子 task **禁止** 再开 10。  
> **产出**：母单 + R1/R2 子 task + LOOP_MANIFEST + PROMPT_START

| 帽 | 产出 |
| --- | --- |
| 10 | 本文件 + 三 task + `docs/harness/invokes/by-task/chatbi-v3-p2-loop/` |
| 22+ | 人批 `HG-LOOP-BATCH` 后粘贴 `PROMPT_START_chatbi_v3_p2_loop_full_chain_v1.md` §3 |

**下一动作**：将母 task `HG-LOOP-BATCH` 改为 **approved**（建议单独 commit）→ 开 `task/chatbi-v3-p2-loop-v1` → 粘贴 PROMPT_START。

---

## §3 归档（Batch 真值摘要）

**背景**：P2-1b/W1 已合 **#86/#87**，但 active/RECENT 未关账；P2-1c 待实现。整合为 **单 Loop · 单 PR**，取代双轨并行。

**落盘文件**：

| 类型 | 路径 |
|------|------|
| 母 | `docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md` |
| R1 | `docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md` |
| R2 | `docs/tasks/active/task_chatbi_v3_p2_resilience_circuit_breaker_v1.md`（已存在 · 补 Loop 字段） |

**freeze_id**：`CHATBI-P2-LOOP@2026-05-29` · R1 `CHATBI-P2-R1-CLOSEOUT@2026-05-29`

**禁止**：本 Prompt 内执行 22/30；勿再开 `task/chatbi-v3-p2-1b-rate-limit` 独立 PR。
