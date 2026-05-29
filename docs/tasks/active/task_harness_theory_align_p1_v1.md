# Task：Harness 理论对齐 · P1 收口

> **状态**：`pending`（P0 已关账 · PR #90 · 2026-05-29）  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Harness-Theory-Align-P1-v1.md`](../spec/governance/SPEC-Governance-Harness-Theory-Align-P1-v1.md)  
> **排期**：[`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) **§0.5**

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `required`（首条领域 Linter + 测） |
| **freeze_id** | `GOV-HARNESS-THEORY-ALIGN-P1@2026-05-29` |
| **semi_auto** | `false` |
| **audit_profile** | `full` |
| **git_branch** | `task/harness-theory-align-p1` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-AUDIT-R1 | pending | 30 | P1 含 Linter/CI |
| HG-AUDIT-CLOSE | pending | done | P1 关账 |

---

## 背景与目标

P0 完成后落实 **Fresh Context**、半自动推广、**首条** 领域结构 CI（见 SPEC §3 候选）。

---

## 范围

- [ ] P1-1：22/50/40 与 invoke 模板 Fresh Context 条款
- [ ] P1-2：`docs/tasks/README.md` 半自动决策表
- [ ] P1-3：首条 Linter + CI 绿
- [ ] `RECENT_TASK_SCHEDULE.md` §0.5 P1 → done

## 非范围

- `verify-fast` 升为 Required；Mini Ralph 产品化

---

## 验收标准

- [ ] SPEC **§6** 全部勾选
- [ ] PR 上 `pytest` workflow 全绿

---

## 给 Cursor

`harness-theory-align-p1`、blocked until P0 done、`RECENT_TASK_SCHEDULE` §0.5
