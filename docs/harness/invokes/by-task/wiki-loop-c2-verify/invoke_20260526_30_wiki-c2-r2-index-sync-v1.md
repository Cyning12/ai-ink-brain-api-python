# Invoke · 30 执行 · R2 · wiki-c2-r2-index-sync

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md` |
| **task_slug** | `wiki-c2-r2-index-sync` |
| **freeze_id** | `WIKI-C2-R2-INDEX@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R2** · **30 执行帽**（上一帽 22 已结束；本帽只按下文执行），严格遵循：
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/tasks/skills/SKILL-harness-loop-batch.md §invoke 质量门禁（C2 · R2 各帽禁止 stub）

【元信息】
- round: R2
- task_slug: wiki-c2-r2-index-sync
- freeze_id: WIKI-C2-R2-INDEX@2026-05-26
- git_branch: task/wiki-loop-c2-verify-v1

【commit 硬纪律】commit 含 WIKI-C2-R2-INDEX@2026-05-26 → 再戴 40。

步骤 2 · 30 交付（RECENT done 属 **关账**，本帽只做 README + 备忘）：
1. 更新 docs/harness/invokes/by-task/wiki-loop-c2-verify/README.md **验收说明** 段：
   - 主目标 = invoke C2 全绿
   - 链 B-Q3 meta-reinspect C2 FAIL 基线
   - 禁止 Agent 代 SKILL accepted
2. 回填 task §实现备忘（README 路径 + 摘要）
3. 落盘 invoke_20260526_30_wiki-c2-r2-index-sync-v1.md（§3 ≥15 行 · **非**「交付摘要」stub）
4. **不**在本帽改 RECENT done（关账步骤 5）

硬约束：不改 api/tests/prompts/CI
```
