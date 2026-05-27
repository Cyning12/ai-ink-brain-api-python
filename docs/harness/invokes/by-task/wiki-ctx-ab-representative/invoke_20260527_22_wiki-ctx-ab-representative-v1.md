# Invoke · 22 任务审核 · wiki-ctx-ab-representative

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_wiki_ctx_ab_representative_v1.md` |
> | task_slug | wiki-ctx-ab-representative |
> | freeze_id | WIKI-CTX-AB-REP@2026-05-27 |
> | git_branch | task/wiki-ctx-ab-representative-v1 |
> | note | 单 task · 长链 22→关账 |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 单 task（非 Loop）· 人闸 HG-TASK-DRAFT / HG-AUDIT-R1 / HG-AB-REP-SLUGS / HG-AB-REP-RUN 均已 **approved**。

## §2 审核结论

**无阻塞 · 可进入 30。**

### 2.1 已核对项（14/14）

| # | 项 | 结果 |
|---|----|------|
| 1 | 四人工闸 approved | pass |
| 2 | SPEC §2.1 六 slug 锁定 | pass |
| 3 | 六 synthesis + done task 存在 | pass |
| 4 | P2 / Multi 基线只读 | pass |
| 5 | T7/T8 聚合阈值 | pass |
| 6 | questions.md Q1–Q4 | pass |
| 7 | 非范围（api/前端/ingest） | pass |
| 8 | test_strategy not_applicable | pass |
| 9 | failure_paths F1–F4 | pass |
| 10 | W 物化脚本可执行 | pass |
| 11 | 实验目录 README/scorecard | pass |
| 12 | semi_auto 长链授权 | pass |
| 13 | 题集 Q4 spot-check | pass（见 review 备注） |
| 14 | invoke/review by-task 路径 | pass |

### 2.2 阻塞项

无。

## §3 审核落盘

审查文档：`docs/harness/reviews/by-task/wiki-ctx-ab-representative/task_governance_wiki_ctx_ab_representative_audit_R1_20260527.md`

## §4 执行路线（计划）

| 序号 | 帽 | 关键动作 |
|------|-----|----------|
| 1 | 22 | review + invoke（本 commit） |
| 2 | 30 | 物化 ×12 · scorecard · conclusion · #46 |
| 3 | 40 | VERIFY · task §自检 |
| 4 | 50 | reinspect |
| 5 | 关账 | git mv · _views · RECENT · CLOSE |

## §5 下一棒 Prompt

见 review 文末 · `PROMPT_30_startup_wiki-ctx-ab-representative-v1.md`。

## §6 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_wiki_ctx_ab_representative_v1.md
├── 分支：task/wiki-ctx-ab-representative-v1
├── human_gate：均已 approved
├── 本棒交付：R1 review + invoke_22 + PROMPT_30
├── 下一棒：30 执行编码
└── 阻塞：无
```
