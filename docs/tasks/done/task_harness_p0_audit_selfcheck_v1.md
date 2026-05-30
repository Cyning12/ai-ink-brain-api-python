# Task：Harness P0 R2 — 22/40 帽补丁（TDD + Delta 勾选）

> **状态**：pending  
> **schedule_ref**：RECENT §0.6 · Loop R2  
> **母单**：[`task_harness_p0_openspec_tdd_loop_v1.md`](task_harness_p0_openspec_tdd_loop_v1.md)  
> **前置**：R1 在 `done/`

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 仅改 Harness 帽 md；无 api/ 行为变更。 |
| **freeze_id** | `HARNESS-P0-AUDIT-SELFCHECK@2026-05-30` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **task_slug** | `p0-audit-selfcheck` |

---

## 行为变更（Delta）

无

---

## 范围

- [ ] `docs/harness/prompts/hats/22-task-audit.md`：增 test_strategy / Delta / Scenario 勾选项（T1+T2）。  
- [ ] `docs/harness/prompts/hats/40-self-check.md`：增 Completeness/Correctness/Coherence 三维（T3）。  
- [ ] 可选：`reviews/README.md` 链到 validate 命令。  
- [ ] 22 R1 审查 **本 Loop 剩余子 task**（R3）零阻塞记录落盘。

## 非范围

- 改 `tools/`（R1 已 done）。  
- 改 TEMPLATE（Step 0 已完成）。

---

## 验收标准

- [ ] 22/40  diff 可人工核对勾选条目。  
- [ ] `python tools/harness_task_validate.py` 仍绿（回归 R1）。  
- [ ] 50 可选（`not_applicable`）。

---

## 给 Cursor

Loop R2、skip 10、R1 须 done
