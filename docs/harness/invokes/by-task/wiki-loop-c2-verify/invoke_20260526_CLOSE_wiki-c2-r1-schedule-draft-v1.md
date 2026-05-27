# Invoke · 关账 · R1 · wiki-c2-r1-schedule-draft

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | CLOSE |
| **task** | `docs/tasks/done/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |
| **task_slug** | `wiki-c2-r1-schedule-draft` |
| **freeze_id** | `WIKI-C2-R1-SCHEDULE@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |
| **next_task** | `docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R1** · **本 round 关账**（50 已建议关账），严格遵循：
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md（cross-round 续 R2）
- docs/harness/invokes/by-task/wiki-loop-c2-verify/LOOP_MANIFEST.md

【元信息】
- round: R1
- task_slug: wiki-c2-r1-schedule-draft
- freeze_id: WIKI-C2-R1-SCHEDULE@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1
- NEXT_TASK_PATH: docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md

步骤 5 · R1 关账：
1. git mv task_governance_loop_c2_verify_r1_schedule_draft_v1.md → docs/tasks/done/
2. 状态行 done（2026-05-26 验收通过 · WIKI-C2-R1-SCHEDULE@2026-05-26）· 勾选 §验收
3. 更新 docs/tasks/_views/done.md 一行（链 reinspect）
4. **不**改 RECENT §6.6 为 done（属 R2 职责）
5. 落盘本 CLOSE invoke + 文末 HANDOFF_CLOSE_TRACE
6. cross_round_semi_auto: 同会话续 MANIFEST **R2**
7. commit message: docs(task): Wiki loop C2 Verify R1 关账 · WIKI-C2-R1-SCHEDULE@2026-05-26

硬约束：单 PR · C2 invoke 全绿为本 Loop 主验收
```

---

## 执行路线与 Commit 回溯

**一句结论**：R1 RECENT §6.6 draft/in_progress 行已落盘；22→30→40→50 invoke C2 全绿；建议进入 MANIFEST **R2**。

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | commit |
|------|-------------|----------|----------|--------|
| 1 | 22 | 零阻塞审查 · 准许 30 | `reviews/.../task_governance_loop_c2_verify_r1_schedule_draft_v1_audit_R1_20260526.md` | api-python@389b30c |
| 2 | 30 | RECENT §6.6 + §8 + SKILL 修订记录 | `RECENT_TASK_SCHEDULE.md` 等 | api-python@c4d328a |
| 3 | 40 | 独立 VERIFY · 自检表 | task active + invoke_40 | api-python@763783e |
| 4 | 50 | 独立复检 · 建议关账 | `reinspect_wiki-c2-r1-schedule-draft_20260526_v1.md` | api-python@005c710 |
| 5 | CLOSE | git mv done · `_views` | `done/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` | （本 commit） |

### api-python（ai-ink-brain-api-python）

- （本 commit）docs(task): Wiki loop C2 Verify R1 关账 · WIKI-C2-R1-SCHEDULE@2026-05-26
- 005c710 docs(task): R1·50 独立复检
- 763783e docs(task): R1·40 自检
- c4d328a docs(task): R1·30 RECENT §6.6
- 389b30c docs(harness): R1·22 任务审核

**下一棒**：MANIFEST **R2** · `wiki-c2-r2-index-sync` · [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) round=R2
