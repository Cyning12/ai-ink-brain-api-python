# Invoke · 关账 · R1 · p0-task-validate

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | CLOSE |
| **task** | `docs/tasks/done/task_harness_p0_task_validate_v1.md` |
| **task_slug** | `p0-task-validate` |
| **freeze_id** | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **next_task** | `docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R1** · **本 round 关账**（50 已建议关账），严格遵循：
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md（cross-round 续 R2）
- docs/harness/invokes/by-task/p0-openspec-tdd/LOOP_MANIFEST.md

【元信息】
- round: R1
- task_slug: p0-task-validate
- freeze_id: HARNESS-P0-TASK-VALIDATE@2026-05-30
- git_branch: task/harness-p0-openspec-tdd
- NEXT_TASK_PATH: docs/tasks/active/task_harness_p0_audit_selfcheck_v1.md
- NEXT_TASK_SLUG: p0-audit-selfcheck

步骤 5 · R1 关账：
1. git mv task_harness_p0_task_validate_v1.md → docs/tasks/done/
2. 状态行 done（2026-05-30 验收通过 · HARNESS-P0-TASK-VALIDATE@2026-05-30）
3. 更新 docs/tasks/_views/done.md 一行（链 reinspect）
4. 落盘本 CLOSE invoke + 文末 HANDOFF_CLOSE_TRACE
5. cross_round_semi_auto: 同会话续 MANIFEST **R2**
6. commit message: feat(harness): P0 R1 task_validate 关账 · HARNESS-P0-TASK-VALIDATE@2026-05-30

硬约束：单 PR · invoke C2 全绿 · 不改 api/ 业务
```

---

## 执行路线与 Commit 回溯

**一句结论**：R1 `harness_task_validate` + pytest 已交付；22→30→40→50 invoke C2 全绿；建议进入 MANIFEST **R2**（22/40 帽补丁）。

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | commit |
|------|-------------|----------|----------|--------|
| 1 | START | 全链启动 invoke | `invoke_20260530_start_p0-task-validate-v1.md` | （见下） |
| 2 | 22 | 零阻塞审查 · 准许 30 | `reviews/.../task_harness_p0_task_validate_v1_audit_R1_20260530.md` | （见下） |
| 3 | 30 | validate CLI + tests | `tools/harness_task_validate.py` 等 | （见下） |
| 4 | 40 | 独立 VERIFY · 自检表 | task + invoke_40 | （见下） |
| 5 | 50 | 独立复检 · 建议关账 | `reinspect_p0-task-validate_20260530_v1.md` | （见下） |
| 6 | CLOSE | git mv done · `_views` | `done/task_harness_p0_task_validate_v1.md` | （本 commit） |

**下一棒**：MANIFEST **R2** · `p0-audit-selfcheck` · [`PROMPT_LOOP_22_to_CLOSE_v1.md`](./PROMPT_LOOP_22_to_CLOSE_v1.md) round=R2
