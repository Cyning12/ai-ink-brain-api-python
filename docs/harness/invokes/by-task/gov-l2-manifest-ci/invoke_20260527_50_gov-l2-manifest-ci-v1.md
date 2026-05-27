# Invoke · 50 独立复检 · gov-l2-manifest-ci

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 50 |
> | task | `docs/tasks/active/task_governance_l2_manifest_ci_v1.md` |
> | task_slug | gov-l2-manifest-ci |
> | freeze_id | GOV-L2-MANIFEST-CI@2026-05-27 |
> | git_branch | task/gov-l2-manifest-ci-v1 |
> | note | 单 task · 无 round |

---

## §1 复检结论

**结论：建议合并 · 无阻塞项。**

### 1.1 VERIFY 重跑

| # | 命令 | 结果 |
|---|------|------|
| 1 | `python tools/tech_graph_test_manifest_check.py` | pass |
| 2 | `pytest tests/test_tech_graph_test_manifest_check.py -q` | pass (12 passed) |
| 3 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | pass (233 passed, 1 skipped) |
| 4 | `python tools/tech_graph_manifest_check.py` | pass |
| 5 | `python tools/tech_graph_contract_check.py` | pass |
| 6 | `python tools/tech_graph_graph_export.py --check` | pass |
| 7 | `python -c "assert len(entries)>=12"` | pass (entries=12) |

### 1.2 范围纪律

| 检查项 | 结果 |
|--------|------|
| 未改 api/ 业务逻辑 | pass |
| 未改 tests/ 业务用例 | pass |
| 未改 prompts/ | pass |
| 未手改 graph.json | pass |
| workflow diff 人确认 | pass (HG-CI-WORKFLOW approved) |

---

## §2 复检落盘

`docs/tasks/reinspect_results/reinspect_gov-l2-manifest-ci_20260527_v1.md`

---

## §3 下一棒

**关账**：git mv → done/ + `_views/done.md` 更新 + CLOSE invoke + hygiene H1–H5。

