---
title: "CI 排障 · drift_check"
slug: vol-02-06-drift
series: chatbi-graph-harness-showcase
vol: "02"
chapter: "06"
status: stub
---

# 06 · CI 事故：drift_check

## 大纲（待编写）

- [ ] PR #107 首跑：`manifest_check` 内 `tech_graph_drift_check` fail
- [ ] stderr：端点未出现在 `docs/_tech_graph/*.md`
- [ ] 修复：`99_spec.md` drift 索引登记两路径 · `02_version` 时间线
- [ ] 教训：manifest_check OK ≠ drift_check OK（vol-03 展开）
- [ ] fix commit `147d0d1`

## 对比

| 命令 | 检查什么 |
| --- | --- |
| `tech_graph_manifest_check.py` | `_manifest.json` vs 代码 |
| `tech_graph_drift_check.py` | 端点字面量 vs `*.md` 全文 |
