---
title: "证据索引"
slug: vol-01-06-evidence
series: chatbi-graph-harness-showcase
vol: "01"
chapter: "06"
status: compiled
---

# 06 · 证据索引（Vol-01）

> L1 真值指针；本页 **不复制** reinspect/task 全文。

---

## 1. PR 与 merge

| 项 | 值 |
| --- | --- |
| **PR** | [#106](https://github.com/Cyning12/ai-ink-brain-api-python/pull/106) |
| **标题** | fix(chatbi): 基线合并闸 — v3 clarify 测试环境 + contract label |
| **merge commit** | `26e1c45` |
| **分支** | `task/chatbi-baseline-merge-gate-v1`（已删） |

---

## 2. Task 与 Harness 落盘

| 类型 | 路径 |
| --- | --- |
| task | `docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md` |
| 22 R1 | `docs/harness/reviews/task_chatbi_baseline_merge_gate_v1_audit_R1_20260604.md` |
| 50 | `docs/tasks/reinspect_results/reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md` |
| invokes | `docs/harness/invokes/by-task/chatbi_baseline_merge_gate_v1/` |

---

## 3. 实现 commit 链（时间序）

| commit | 说明 |
| --- | --- |
| `a0830bb` | 10 帽 task + invoke |
| `c51369e` | 22 R1 审查落盘 |
| `bbd6ded` | human_gate 人签 |
| `eed212e` | **业务 fix**（conftest · agent · manifest） |
| `d289fe9` | 40 自检回填 |
| `c04e481` | 50 复检落盘 |
| `26e1c45` | **merge to main** (#106) |

---

## 4. 业务 diff 文件（`origin/main...eed212e`）

```
tests/conftest.py
api/agent.py
docs/_tech_graph/_contract_manifest.json
docs/_tech_graph/02_version.md
```

Harness 文档（同 PR 分支内，非 runtime）：

```
docs/tasks/active/task_chatbi_baseline_merge_gate_v1.md
docs/harness/reviews/...
docs/harness/invokes/by-task/chatbi_baseline_merge_gate_v1/...
docs/tasks/reinspect_results/reinspect_chatbi_baseline_merge_gate_v1_20260604_v1.md
```

---

## 5. 50 独立复跑摘要（2026-06-04）

| 命令 | exit | 要点 |
| --- | ---: | --- |
| 10× v3 测 | 0 | 10 passed |
| 全集 pytest | 0 | 277 passed · 1 skipped |
| contract_check | 0 | OK |
| manifest_check | 0 | OK |
| harness_task_validate | 0 | OK |
| human_gate_check | 0 | OK |

**50 总评**：pass-with-notes · 条件性建议 merge（须 PR CI 绿）。

---

## 6. 关联 SPEC / 图谱

| 文档 | 用途 |
| --- | --- |
| `docs/harness/guides/RUNBOOK_graph_contract_ci_red_v1.md` | label 路径 A |
| `docs/_tech_graph/_contract_manifest.json` | contract 真值 |
| P0 50（选 B 依据） | `reinspect_chatbi_graph_p0_foundation_v1_20260603_v1.md` |

---

## 7. 系列内交叉引用

| 卷 | 关系 |
| --- | --- |
| vol-02 | 依赖本 PR merge 后 rebase |
| vol-03 | Harness / CI 横切 |
| `_meta/EVIDENCE_LINKS.md` | 全系列 L1 一览 |
