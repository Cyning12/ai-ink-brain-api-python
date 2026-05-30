# Task：Harness P0 R2 — 22/40 帽补丁（TDD + Delta 勾选）

> **状态**：done（2026-05-30 验收通过 · HARNESS-P0-AUDIT-SELFCHECK@2026-05-30）  
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

- [x] `docs/harness/prompts/hats/22-task-audit.md`：增 test_strategy / Delta / Scenario 勾选项（T1+T2）。  
- [x] `docs/harness/prompts/hats/40-self-check.md`：增 Completeness/Correctness/Coherence 三维（T3）。  
- [x] 可选：`reviews/README.md` 链到 validate 命令。  
- [x] 22 R1 审查 **本 Loop 剩余子 task**（R3）零阻塞记录落盘。

## 非范围

- 改 `tools/`（R1 已 done）。  
- 改 TEMPLATE（Step 0 已完成）。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
| F1 | `fp-audit-patch-scope` | 误改 tools/ 或 api/ | 22 阻塞 / revert | 改 diff | 范围越界 |
| F2 | `fp-validate-regress` | validate 回归失败 | 40 fail | 修 R1 或补丁 | pytest/CLI 输出 |

---

## 验收标准

- [x] 22/40  diff 可人工核对勾选条目。  
- [x] `python tools/harness_task_validate.py` 仍绿（回归 R1）。  
- [x] 50 可选（`not_applicable`）。

---

### 自检结论（执行者）

| # | 验收项 | 结果 | 证据 |
| --- | --- | --- | --- |
| V1 | 22 帽 OpenSpec×TDD 勾选 §4.2 | **pass** | `22-task-audit.md` 新增 4 项表 |
| V2 | 40 帽三维自检 §4.3 | **pass** | `40-self-check.md` Completeness/Correctness/Coherence |
| V3 | reviews/README validate 链 | **pass** | §OpenSpec 机械校验命令 |
| V4 | R3 预审查零阻塞 | **pass** | `task_harness_p0_status_cursor_v1_preflight_R1_20260530.md` |
| V5 | validate 回归 | **pass** | `python tools/harness_task_validate.py docs/tasks/done/task_harness_p0_task_validate_v1.md` exit 0 |

---

## 给 Cursor

Loop R2、skip 10、R1 须 done
