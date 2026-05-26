# Invoke · 50 独立复检 · R2 · wiki-c2-r2-index-sync

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 50 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md` |
| **task_slug** | `wiki-c2-r2-index-sync` |
| **freeze_id** | `WIKI-C2-R2-INDEX@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R2** · **50 独立复检帽**（上一帽 40 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2 · **R2 禁止 stub**）

【元信息】
- round: R2
- task_slug: wiki-c2-r2-index-sync
- freeze_id: WIKI-C2-R2-INDEX@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1

步骤 4 · 50 — 独立重跑 40 VERIFY + R2 全链 invoke C2 抽检：

VERIFY-1:
  rg 'C2 verify|C2 Verify' docs/harness/invokes/by-task/wiki-loop-c2-verify/README.md

VERIFY-2:
  wc -c docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_20260526_{22,30,40,50}_wiki-c2-r2-index-sync-v1.md
  → 各 ≥800B · §3 非 stub（对比 B-Q3 R2 322B stub）

落盘: docs/tasks/reinspect_results/reinspect_wiki-c2-r2-index-sync_20260526_v1.md
结论: 建议关账 / 须回 30
commit reinspect + invoke_50
```
