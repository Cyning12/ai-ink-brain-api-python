# Invoke · 40 自检 · R3 · p0-status-cursor

| 字段 | 值 |
|------|-----|
| **round** | R3 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_harness_p0_status_cursor_v1.md` |
| **task_slug** | `p0-status-cursor` |
| **freeze_id** | `HARNESS-P0-STATUS-CURSOR@2026-05-30` |
| **git_branch** | `task/harness-p0-openspec-tdd` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 P0 OpenSpec×TDD Loop **R3** · **40 自检帽**（上一帽 30 已结束），严格遵循：
- docs/harness/prompts/hats/40-self-check.md（含 T3 三维表）
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md

【元信息】
- round: R3
- task_slug: p0-status-cursor
- freeze_id: HARNESS-P0-STATUS-CURSOR@2026-05-30
- git_branch: task/harness-p0-openspec-tdd

步骤 3 · 40 自检 VERIFY（须独立重跑）：
VERIFY-1：pytest tests/test_harness_change_status.py -v
VERIFY-2：python tools/harness_change_status.py --task docs/tasks/active/task_harness_p0_openspec_tdd_loop_v1.md --json
VERIFY-3：test -f .cursor/commands/harness-validate.md .cursor/commands/harness-status.md
VERIFY-4：pytest tests -m "not intent_eval and not intent_benchmark" -q

交付：回填 task §自检结论 · 50 可选跳过 · commit → CLOSE
```
