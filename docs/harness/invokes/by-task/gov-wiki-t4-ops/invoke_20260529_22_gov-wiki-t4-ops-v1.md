# Invoke · 22 任务审核 · gov-wiki-t4-ops

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_wiki_t4_ops_v1.md` |
> | task_slug | gov-wiki-t4-ops |
> | freeze_id | GOV-WIKI-T4-OPS@2026-05-29 |
> | git_branch | task/gov-wiki-t4-ops-v1 |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 单 task · `test_strategy: recommended` · `audit_profile: post_close`。

## §2 审核结论

**无阻塞 · 可进入 30 执行编码。**

| # | 项 | 结果 |
|---|----|------|
| 1 | `HG-TASK-DRAFT` = approved | pass |
| 2 | `HG-AUDIT-R1` = approved | pass |
| 3 | `HG-REINSPECT` = approved | pass（50 前人签） |
| 4 | task 元信息完整 | pass |
| 5 | lint + pytest 范围清晰 | pass |
| 6 | diff 白名单明确 | pass |
| 7 | Bridge SPEC §4.3 可读 | pass |

## §3 审核落盘

审查文档：`docs/harness/reviews/by-task/gov-wiki-t4-ops/task_governance_wiki_t4_ops_audit_R1_20260529.md`

---

## §4 执行路线

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 |
|------|-------------|----------|----------|
| 1 | **22 任务审核** | review + invoke | 本目录 + `reviews/by-task/gov-wiki-t4-ops/*` |
| 2 | 30 执行编码 | lint + pytest + docs | `tools/` · `tests/` · synthesis ×3 · SPEC |
| 3 | 40 自检 | VERIFY 全绿 + task 回填 | `invoke_*_40_*` |
| 4 | 50 独立复检 | diff 白名单 + reinspect | `reinspect_gov-wiki-t4-ops_20260529_v1.md` |
| 5 | 关账 | git mv · _views · CLOSE | `done/task_*` |

---

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_wiki_t4_ops_v1.md · audit_profile：post_close
├── 分支：task/gov-wiki-t4-ops-v1
├── human_gate：HG-TASK-DRAFT approved · HG-AUDIT-R1 approved · HG-REINSPECT approved
├── 本棒交付：review + invoke 落盘
├── 下一棒：30 执行编码
└── 阻塞：无
```
