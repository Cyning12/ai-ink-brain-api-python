# Invoke · 全链启动 · R1 · p0-task-validate

| 字段 | 值 |
|------|-----|
| **round** | R1 |
| **hat** | START |
| **task** | `docs/tasks/active/task_harness_p0_task_validate_v1.md` |
| **task_slug** | `p0-task-validate` |
| **freeze_id** | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **cross_round_semi_auto** | `true` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Harness Loop Batch 全链（p0-openspec-tdd），严格遵循：
- docs/tasks/skills/SKILL-harness-loop-batch.md
- docs/harness/invokes/by-task/p0-openspec-tdd/LOOP_MANIFEST.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md

【授权】cross-round semi_auto：HG-LOOP-BATCH 已 approved；同会话可 R1→R2→R3 链式戴帽；每换帽先落盘 invoke §3 并 commit。

当前 round：R1
task：docs/tasks/active/task_harness_p0_task_validate_v1.md
git_branch / cwd：task/harness-p0-openspec-tdd · 本仓根
verify：pytest tests -m "not intent_eval and not intent_benchmark"

须完成：
1. 开帽落盘 invoke（本 Prompt 全文）
2. 22 R1 → docs/harness/reviews/by-task/p0-task-validate/
3. 30 实现 tools/harness_task_validate.py + tests
4. 40 自检回填 task §自检结论
5. 50 落盘 docs/tasks/reinspect_results/（R1 required）
6. 关账：git mv task → done/ · 更新 _views/done.md
7. 无阻塞则继续 R2（读 MANIFEST；勿再开 10 帽）

禁止：改 api/ 业务；在 main 上提交。
```
