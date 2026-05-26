# Invoke · 关账 · R2 · wiki-c2-r2-index-sync

| 字段 | 值 |
|------|-----|
| **round** | R2 |
| **hat** | CLOSE |
| **task** | `docs/tasks/done/task_governance_loop_c2_verify_r2_index_sync_v1.md` |
| **task_slug** | `wiki-c2-r2-index-sync` |
| **freeze_id** | `WIKI-C2-R2-INDEX@2026-05-26` |
| **git_branch** | `task/wiki-loop-c2-verify-v1` |
| **next_task** | `docs/tasks/active/task_harness_wiki_loop_c2_verify_v1.md`（META） |

---

## §3 可复制 Prompt 正文

```text
你正在执行 Wiki Loop C2 Verify **R2** · **本 round 关账**（50 建议关账），严格遵循 HANDOFF_CLOSE_TRACE 与 LOOP_MANIFEST META 行。

【元信息】
- round: R2
- task_slug: wiki-c2-r2-index-sync
- freeze_id: WIKI-C2-R2-INDEX@2026-05-26
- NEXT: META 母单关账（两轮子 task 均 done/ 后）

步骤 5 · R2 关账：
1. git mv R2 task → docs/tasks/done/
2. RECENT §6.6 Wiki Loop C2 Verify 行 → **done**
3. _views/done.md 增 R2 行（R1 已有）
4. 落盘 CLOSE invoke + CLOSE_TRACE
5. cross_round_semi_auto → 续 **META** 母关账
6. commit: docs(task): Wiki loop C2 Verify R2 关账 · WIKI-C2-R2-INDEX@2026-05-26
```

---

## 执行路线与 Commit 回溯

**一句结论**：R2 invoke README 验收说明已回填；RECENT §6.6 **done**；R2 全链 invoke C2 全绿（对比 B-Q3 R2 stub 债已消除）。

| 序号 | 帽子 | commit |
|------|------|--------|
| 1 | 22 | api-python@9621c92 |
| 2 | 30 | api-python@44f1c6d |
| 3 | 40 | api-python@de67ef2 |
| 4 | 50 | api-python@a6db5a8 |
| 5 | CLOSE | （本 commit） |

**下一棒**：MANIFEST **META** · `wiki-loop-c2-verify` · 仅关账（docs-only · 无 22→50）
