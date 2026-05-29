# Invoke · 50 复检 · R1 · chatbi-v3-p2-loop-r1-closeout

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 50 |
| **task** | `docs/tasks/done/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md` |
| **task_slug** | `chatbi-v3-p2-loop-r1-closeout` |
| **freeze_id** | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 ChatBI P2 Loop **R1** · **50 复检帽**（可选 meta 摘要），严格遵循 50 帽规范、HANDOFF_AUTO_COMMIT.md。

【元信息】
- round: R1
- task: docs/tasks/done/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md
- task_slug: chatbi-v3-p2-loop-r1-closeout
- freeze_id: CHATBI-P2-R1-CLOSEOUT@2026-05-29
- git_branch: task/chatbi-v3-p2-loop-v1

【50 交付】
1. 落盘 docs/tasks/reinspect_results/reinspect_chatbi_v3_p2_loop_r1_closeout_20260529_v1.md
2. 独立重跑 pytest + lint；核对 RECENT / done/ / active 无 #0b/#W1
3. commit 后 cross_round → **R2** 22 帽（circuit breaker · required · 50 必做）

硬约束：R1 不改 api/ · R2 启动前 #0b/#W1 须在 done/（已满足）
```
