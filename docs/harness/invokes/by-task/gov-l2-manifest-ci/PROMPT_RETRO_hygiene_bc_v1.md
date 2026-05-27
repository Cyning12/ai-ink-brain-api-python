# Hygiene Prompt · gov-l2-manifest-ci（Part A · PR #70 后补债）

> **与 `PROMPT_START_full_chain_v1.md` 的区别**
>
> | 文件 | 何时用 |
> |------|--------|
> | **PROMPT_START** | **首次**全链执行 22→关账（业务交付 · 历史） |
> | **本文件（PROMPT_RETRO）** | PR #70 merge 后 **补 Harness 文档债**（Part A） |

| 项 | 值 |
|----|-----|
| **task_slug** | `gov-l2-manifest-ci` |
| **freeze_id** | `GOV-L2-MANIFEST-CI@2026-05-27` |
| **业务 PR** | #70 · 已 merge `main` |
| **hygiene 分支** | `task/gov-l2-manifest-ci-hygiene-v1` |
| **SKILL** | [`SKILL-harness-task.md`](../../../tasks/skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../../../tasks/skills/SKILL-docs-governance.md) |

---

## Part A · Hygiene 修复

> 根因与 T4 expand 同类（见 [`gov-wiki-t4-expand/REPORT_retro_gap_analysis_20260527_v1.md`](../gov-wiki-t4-expand/REPORT_retro_gap_analysis_20260527_v1.md)）；ST1–ST6 已在 PROMPT_START v1.1 写入，本 task 首次执行时仍未完全执行 ST5 正文项。

### A1 · task done 正文（ST5 / N2）

- [x] `docs/tasks/done/task_governance_l2_manifest_ci_v1.md`：头部 `done（2026-05-27 · GOV-L2-MANIFEST-CI@2026-05-27）`
- [x] 范围 / 验收 `- [x]`

### A2 · invoke §3 ≥15 行（ST1 / N1）

- [x] `invoke_20260527_22_*` · §3 扩写（审查摘要 + commit 表）
- [x] `invoke_20260527_30_*` · §3 执行路线 + 修复 §1 表格 Markdown
- [x] `invoke_20260527_40_*` · §3 自检结论 + 50 Prompt
- [x] `invoke_20260527_50_*` · §3 关账指引 + ST5 追溯说明

### A3 · 交叉引用 H5

- [x] invoke 元信息 `task` → `docs/tasks/done/...`
- [x] `README.md` → done 路径 + PR #70 说明
- [x] review R1 task 路径 → done

### A4 · RECENT §8

- [x] §8 增 hygiene 修订行（与 §6.6 L2 Phase B done 一致）

**VERIFY（A）**：

```bash
rg 'done（' docs/tasks/done/task_governance_l2_manifest_ci_v1.md
rg '\- \[x\]' docs/tasks/done/task_governance_l2_manifest_ci_v1.md | wc -l   # 须 ≥10
rg 'docs/tasks/active/task_governance_l2_manifest_ci' docs/harness/invokes/by-task/gov-l2-manifest-ci/invoke_*.md docs/harness/reviews/by-task/gov-l2-manifest-ci/ || echo "H5 pass"
```

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：PR #70 后 Part A hygiene 补债 Prompt |
