# Task：Harness 理论对齐 · P1 收口

> **状态**：done（2026-05-29 验收通过 · PR #92）  
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
| **linter_target** | **候选 C** — 结构化错误响应 `ok` / `error_code` / `message` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-AUDIT-R1 | approved | 30 | P1 含 Linter/CI |
| HG-AUDIT-CLOSE | approved | done | PR #92 合并 + 50 复检关账（2026-05-29） |

---

## 背景与目标

P0 完成后落实 **Fresh Context**、半自动推广、**首条** 领域结构 CI（见 SPEC §3 候选 C）。

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | Linter 缺必填键 | CI / pytest **失败**；禁止合并 | — | CI 红 |
| F2 | 22/50 附带 30 invoke 长文 | 违反 Fresh Context；须裁剪输入 | — | — |

---

## 范围

- [x] P1-1：22/50/40 与 invoke 模板 Fresh Context 条款
- [x] P1-2：`docs/tasks/README.md` 半自动决策表
- [x] P1-3：首条 Linter + CI 绿（`harness_structured_error_shape_check`）
- [x] P1-4：README `test_strategy` 季度抽检说明
- [x] `RECENT_TASK_SCHEDULE.md` §0.5 P1 → done（PR #92 合并后）

## 非范围

- `verify-fast` 升为 Required；Mini Ralph 产品化

---

## 验收标准

- [x] SPEC **§6** 全部勾选
- [x] PR 上 `pytest` workflow 全绿（PR #92）

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `python tools/harness_structured_error_shape_check.py` · `pytest tests/test_harness_structured_error_shape_check.py` |
| 结论 | pass |
| 要点 | 结构化错误 registry 覆盖 rate_limit + circuit_breaker；全量 pytest 261 passed |

---

## 关账引用

- **22 CLOSE**：`docs/harness/reviews/by-task/harness-theory-align-p1/task_harness_theory_align_p1_v1_audit_CLOSE_20260529.md`
- **50**：`docs/tasks/reinspect_results/reinspect_harness_theory_align_p1_20260529_v1.md`
- **PR**：[#92](https://github.com/Cyning12/ai-ink-brain-api-python/pull/92) · `5c33dec`

---

## 给 Cursor

`harness-theory-align-p1`、`GOV-HARNESS-THEORY-ALIGN-P1`、`RECENT_TASK_SCHEDULE` §0.5、Fresh Context、`harness_structured_error_shape_check`
