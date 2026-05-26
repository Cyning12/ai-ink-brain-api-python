# 任务审核 · R1 · Wiki Loop C2 Verify · invoke README / 索引同步

| 字段 | 值 |
|------|-----|
| **task_path** | `docs/tasks/active/task_governance_loop_c2_verify_r2_index_sync_v1.md` |
| **task_slug** | `wiki-c2-r2-index-sync` |
| **freeze_id** | `WIKI-C2-R2-INDEX@2026-05-26` |
| **audit_round** | R1 |
| **invoke_snapshot** | `docs/harness/invokes/by-task/wiki-loop-c2-verify/invoke_20260526_22_wiki-c2-r2-index-sync-v1.md` |
| **PREV_DONE** | `docs/tasks/done/task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |

---

## 审查结论摘要

**零阻塞 · 准许 30 执行帽开工。**

---

## 已核对项

| # | 项 | 结果 |
|---|-----|------|
| 1 | R1 在 `docs/tasks/done/` | pass · `task_governance_loop_c2_verify_r1_schedule_draft_v1.md` |
| 2 | RECENT §6.6 含 Loop C2 Verify **in_progress** 行 | pass |
| 3 | 母闸继承 · `HG-LOOP-BATCH` approved | pass |
| 4 | §范围：README 验收说明 + 关账 RECENT done + `_views` | 可观测 |
| 5 | §非范围：不改 prompts/api · 不代 SKILL accepted | 明确 |
| 6 | failure_paths F1–F3 | 完整 |
| 7 | **R2 invoke C2 禁止 stub**（对比 B-Q3 R2 债） | 已写入 task F2 |

---

## 阻塞 / 非阻塞

**无阻塞项。**

---

## 是否建议执行帽开工

**是** — 准许 **30** 更新 invoke README 验收说明段落。

---

## 签收 / 关闭

本审查为 **R2 首轮**；task **未**关账。

---

## 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop C2 Verify **R2** · **30 执行帽**，遵循 30-execute-code.md 与 task §范围。

【元信息】task_slug=wiki-c2-r2-index-sync · freeze_id=WIKI-C2-R2-INDEX@2026-05-26

交付：补全 wiki-loop-c2-verify/README.md 验收说明（链 B-Q3 meta-reinspect C2 FAIL 基线）· 回填 §实现备忘 · invoke_30 §3 ≥15 行 · commit
```
