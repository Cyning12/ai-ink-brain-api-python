# Task：Harness P0 — OpenSpec 写法 × TDD 纪律 Loop 母单

> **状态**：done（2026-05-30 验收通过 · HARNESS-P0-OPENSPEC-TDD-LOOP@2026-05-30）  
> **schedule_ref**：RECENT §0.6  
> **关联 SKILL**：[`docs/tasks/skills/SKILL-harness-loop-batch.md`](../skills/SKILL-harness-loop-batch.md)  
> **执行安排真值**：[`docs/spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md`](../spec/governance/SPEC-Governance-Harness-OpenSpec-TDD-P0-v1.md)  
> **10 帽 Batch**：本 commit 已落盘母单 + R1–R3 子单；invoke 见 [`docs/harness/invokes/by-task/p0-openspec-tdd/`](../harness/invokes/by-task/p0-openspec-tdd/)

> 落盘规则：三轮子 task 均 `done/` 后本单 META 关账。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | Loop 编排；子 R1 触达 `tools/`+`tests/`；母单不直接交付实现。 |
| **freeze_id** | `HARNESS-P0-OPENSPEC-TDD-LOOP@2026-05-30` |
| **gates_before_code** | `["human_gate", "子 task 顺序 R1→R2→R3"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/harness-p0-openspec-tdd` |
| **task_slug** | `p0-openspec-tdd` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | approved | 22-R1, 30, 40, 50 | 人批 Batch 后启动 R1 全链 |

---

## 子 task 顺序（硬 · R1→R2→R3→META）

| 序 | round | task 路径 | task_slug | freeze_id |
|----|-------|-----------|-----------|-----------|
| 1 | **R1** | [`task_harness_p0_task_validate_v1.md`](task_harness_p0_task_validate_v1.md) | `p0-task-validate` | `HARNESS-P0-TASK-VALIDATE@2026-05-30` |
| 2 | **R2** | [`task_harness_p0_audit_selfcheck_v1.md`](task_harness_p0_audit_selfcheck_v1.md) | `p0-audit-selfcheck` | `HARNESS-P0-AUDIT-SELFCHECK@2026-05-30` |
| 3 | **R3** | [`task_harness_p0_status_cursor_v1.md`](task_harness_p0_status_cursor_v1.md) | `p0-status-cursor` | `HARNESS-P0-STATUS-CURSOR@2026-05-30` |
| 4 | **META** | 本文件 | `p0-openspec-tdd` | `HARNESS-P0-OPENSPEC-TDD-LOOP@2026-05-30` |

**Manifest**：[`docs/harness/invokes/by-task/p0-openspec-tdd/LOOP_MANIFEST.md`](../harness/invokes/by-task/p0-openspec-tdd/LOOP_MANIFEST.md)

---

## 背景与目标

OpenSpec 对比与 TDD 架构评估结论：**O1–O3 模板已完成**；Sprint A/B 合并为 Loop **R1–R3**（validate+22/40 → status+cursor）。单 PR 合入 `main`。

**母单完成态**：R1 `harness_task_validate.py` + pytest；R2 22/40 帽补丁；R3 `change_status --json` + Cursor 薄命令；META + `REPORT_completion_*`。

---

## 范围

- [x] 人批 `HG-LOOP-BATCH` → `approved` 后启动 R1。  
- [x] R1→R2→R3 各走 22→30→40→50→关账（或 R2/R3 按 task 省略 50）。  
- [x] 单 PR · 分支 `task/harness-p0-openspec-tdd`。  
- [x] Step 0（O1–O3 模板）已在本分支首 commit。

## 非范围

- 通用 `ink-harness` PyPI 库（见 diary v2 可行性）。  
- 存量 active task 全量回填 Delta（Sprint C · 可选 follow-up）。  
- 改 `api/` 业务逻辑。

---

## 失败路径

| # | Scenario ID | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|-------------|----------|----------|--------|----------|
| F1 | `fp-loop-gate-pending` | `HG-LOOP-BATCH` = pending | 22 拒开工 | 人批后 | 阻塞说明 |
| F2 | `fp-loop-order-r2` | R2 开工时 R1 未 done | 22 阻塞 | R1 关账后 | 审查阻塞 |
| F3 | `fp-loop-order-r3` | R3 开工时 R2 未 done | 22 阻塞 | R2 关账后 | 审查阻塞 |

---

## 验收标准

- [x] R1–R3 均在 `docs/tasks/done/`。  
- [x] `python tools/harness_task_validate.py --all-active` 可运行（R1）。  
- [x] 22/40 帽含 test_strategy / 三维自检条目（R2）。  
- [x] `harness_change_status.py --json` + `.cursor/commands/harness-*.md`（R3）。  
- [x] PR pytest Required 全绿。

---

## 给 Cursor

`Harness-loop-batch`、`p0-openspec-tdd`、`HG-LOOP-BATCH`、`semi_auto`、`RECENT §0.6`
