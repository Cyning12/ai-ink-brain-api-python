# Invoke · 30 执行 · R1 · chatbi-v3-p2-loop-r1-closeout

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md` |
| **task_slug** | `chatbi-v3-p2-loop-r1-closeout` |
| **freeze_id** | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 ChatBI P2 Loop **R1** · **30 执行帽**（22 已零阻塞），严格遵循 30-execute-code.md、HANDOFF_AUTO_COMMIT.md、SKILL-harness-loop-batch。

【元信息】
- round: R1
- task: docs/tasks/active/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md
- task_slug: chatbi-v3-p2-loop-r1-closeout
- freeze_id: CHATBI-P2-R1-CLOSEOUT@2026-05-29
- git_branch: task/chatbi-v3-p2-loop-v1
- 22 review: docs/harness/reviews/by-task/chatbi-v3-p2-loop-r1-closeout/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1_audit_R1_20260529.md

【交付清单】
1. git mv → done/（文首 done（2026-05-29）与 mv 同一提交）：
   - task_chatbi_v3_p2_resilience_rate_limit_v1.md（#0b · PR #86）
   - task_governance_wiki_milestone_acceptance_expand_v1.md（W1 · PR #87）
2. 更新 docs/tasks/_views/done.md 两条索引
3. RECENT §1.1：#0b/#W1/L1-R1 → done；0c 标 R2 当前棒；删 §1.2
4. 更新 docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md §子单状态
5. 回填 task §自检结论；pytest 绿；commit
6. semi_auto → 40 自检帽

验证：pytest tests -m "not intent_eval and not intent_benchmark"
禁止：改 api/ · 独立 PR
```
