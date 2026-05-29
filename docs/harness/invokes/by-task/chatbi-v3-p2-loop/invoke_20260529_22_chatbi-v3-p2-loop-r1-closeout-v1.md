# Invoke · 22 任务审核 · R1 · chatbi-v3-p2-loop-r1-closeout

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 22 |
| **task** | `docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md` |
| **task_slug** | `chatbi-v3-p2-loop-r1-closeout` |
| **freeze_id** | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 ChatBI P2 韧性 Loop **R1** 帽链：**22 → 30 → 40**（50 可选），严格遵循：
- docs/harness/prompts/hats/22-task-audit.md、30-execute-code.md、40-self-check.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md
- semi_auto: true

【元信息】
- round: R1
- task: docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md
- task_slug: chatbi-v3-p2-loop-r1-closeout
- freeze_id: CHATBI-P2-R1-CLOSEOUT@2026-05-29
- git_branch: task/chatbi-v3-p2-loop-v1
- 母 task: docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
- invoke 目录: docs/harness/invokes/by-task/chatbi-v3-p2-loop/
- cross_round_semi_auto: true

【授权】semi_auto 跨 round：R1 关账后按 MANIFEST 续 R2→META。每帽 invoke + commit。

开帽前：
python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_v3_p2_resilience_loop_v1.md
python tools/harness_human_gate_check.py --task docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md

步骤 1 · 22 任务审核：
1. 确认母 task `HG-LOOP-BATCH` = **approved**（继承母闸；禁止 Agent 代填 pending）。
2. 审 task §范围 / §非范围 / §failure_paths / §验收标准 / Harness 元信息表。
3. 核对 PR #86（P2-1b）· PR #87（W1）已合 main；50 复检 `reinspect_chatbi_v3_p2_1b_rate_limit_20260529_v1.md` 已落盘。
4. 落盘 review：docs/harness/reviews/by-task/chatbi-v3-p2-loop-r1-closeout/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1_audit_R1_20260529.md
5. 无阻塞 → 准许 **30** 执行帽开工。
6. commit review + 本 invoke。

【R1 交付硬清单】
1. git mv #0b + W1 → done/（同日文首 done）
2. _views/done.md
3. RECENT §1.1 #0b/#W1 done；删 §1.2 双轨
4. 更新 done/task_chatbi_v3_p2_resilience_v1.md 子单表

硬约束：单 PR · R1 不改 api/ · 继承母闸 HG-LOOP-BATCH
```
