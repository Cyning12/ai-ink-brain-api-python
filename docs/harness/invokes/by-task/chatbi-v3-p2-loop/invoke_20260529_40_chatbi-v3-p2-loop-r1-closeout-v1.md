# Invoke · 40 自检 · R1 · chatbi-v3-p2-loop-r1-closeout

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 40 |
| **task** | `docs/tasks/done/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md` |
| **task_slug** | `chatbi-v3-p2-loop-r1-closeout` |
| **freeze_id** | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 ChatBI P2 Loop **R1** · **40 自检帽**，严格遵循 40-self-check.md、HANDOFF_AUTO_COMMIT.md。

【元信息】
- round: R1
- task: docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md
- task_slug: chatbi-v3-p2-loop-r1-closeout
- freeze_id: CHATBI-P2-R1-CLOSEOUT@2026-05-29
- git_branch: task/chatbi-v3-p2-loop-v1

【40 自检清单】
1. 独立重跑 pytest + coding_wiki_graph_nodes_lint.py
2. 核对 active/ 无 #0b/#W1；验收标准全勾选
3. git mv 本 R1 task → done/（文首 done 与 mv 同一提交）
4. 更新 _views/done.md；落盘 invoke；commit
5. 50 可选：reinspect meta 摘要
6. cross_round_semi_auto → 续 R2（22→30→40→50 required）

硬约束：无 api/ diff · F2/F3 failure_paths 不得触发
```
