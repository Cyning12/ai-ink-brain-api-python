# Task：Harness 理论对齐 · P0 收口

> **状态**：done（2026-05-29 验收通过 · PR #90）  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Harness-Theory-Align-P0-v1.md`](../spec/governance/SPEC-Governance-Harness-Theory-Align-P0-v1.md)  
> **对照稿**：`ai_coding_governance/lib/COMPARISON_Harness-Ralph理论_vs_Ink落地_v1_zh.md`  
> **排期**：[`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) **§0.5**

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 文档、AGENTS、22 清单与 task 回填；无 `api/` 行为变更 |
| **freeze_id** | `GOV-HARNESS-THEORY-ALIGN-P0@2026-05-29` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/harness-theory-align-p0` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22-R1,30 | SPEC/task 人扫（2026-05-29 人批） |
| HG-AUDIT-CLOSE | approved | done | PR #90 合并 + 50 复检关账（2026-05-29） |

---

## 背景与目标

落实培训讲义与 Ink 落地差距之 **P0**：22 清单、AGENTS 地图化、active task Harness 字段与 CI 验收条、高敏 50 规则写入审查模板。

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | 22 发现 task 缺 Harness 字段 | 阻塞清单；禁止 30 开工 | — | — |

---

## 范围

- [x] `22-task-audit.md` + `reviews/README`：§3.1～3.3 检查表
- [x] `AGENTS.md` ≤120 行（89 行 · `wc -l` 2026-05-29）
- [x] `docs/tasks/active/` 业务 task 回填（§1.1 #1～#6）
- [x] `docs/tasks/README.md`：`test_strategy` 默认表
- [x] 样例 22 审查：`reviews/by-task/harness-theory-align-p0/task_harness_theory_align_p0_v1_audit_R1_20260529.md`
- [x] `RECENT_TASK_SCHEDULE.md` §0.5 P0 → done（PR #90 合并后）

## 非范围

- Ralph / Hermes 编排器；P1 领域 Linter（另 task）

---

## 验收标准

- [x] SPEC [`SPEC-Governance-Harness-Theory-Align-P0-v1.md`](../spec/governance/SPEC-Governance-Harness-Theory-Align-P0-v1.md) **§6** 全部勾选
- [x] PR 上 `pytest` workflow 全绿（PR #90 · 本地 260 passed）

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `pytest tests -m "not intent_eval and not intent_benchmark"` |
| 结论 | pass |
| 要点 | 260 passed；PR #90 CI pytest SUCCESS |

---

## 关账引用

- **22 CLOSE**：`docs/harness/reviews/by-task/harness-theory-align-p0/task_harness_theory_align_p0_v1_audit_CLOSE_20260529.md`
- **50**：`docs/tasks/reinspect_results/reinspect_harness_theory_align_p0_20260529_v1.md`
- **PR**：[#90](https://github.com/Cyning12/ai-ink-brain-api-python/pull/90) · `f1c73f8`

---

## 给 Cursor

`harness-theory-align-p0`、`GOV-HARNESS-THEORY-ALIGN-P0`、`RECENT_TASK_SCHEDULE` §0.5、`COMPARISON_Harness-Ralph`
