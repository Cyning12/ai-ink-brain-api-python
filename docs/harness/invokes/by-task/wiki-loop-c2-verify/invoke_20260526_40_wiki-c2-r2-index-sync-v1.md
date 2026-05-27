# Invoke · 40 自检 · R2 · wiki-c2-r2-index-sync

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md` |
| **task_slug** | `wiki-c2-r2-index-sync` |
| **freeze_id** | `WIKI-C2-R2-INDEX@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R2** · **40 自检帽**（上一帽 30 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/40-self-check.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2）

【元信息】
- round: R2
- task_slug: wiki-c2-r2-index-sync
- freeze_id: WIKI-C2-R2-INDEX@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1

步骤 3 · 40 — 独立重跑 VERIFY：

VERIFY-1:
  rg 'C2 verify|C2 Verify' docs/harness/invokes/by-task/wiki-loop-c2-verify/README.md

VERIFY-2（关账前预期 in_progress，本帽仅检 README）:
  test -f docs/tasks/done/task_governance_loop_c2_verify_r1_schedule_draft_v1.md

VERIFY-3 · R2 invoke C2（22/30 已落盘）:
  wc -c docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_20260526_{22,30}_wiki-c2-r2-index-sync-v1.md

交付：填 task ### 自检结论表 · invoke_40 · commit · 下一棒 50
```
