# Invoke · 40 自检 · gov-l2-manifest-ci

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_l2_manifest_ci_v1.md` |
> | task_slug | gov-l2-manifest-ci |
> | freeze_id | GOV-L2-MANIFEST-CI@2026-05-27 |
> | git_branch | task/gov-l2-manifest-ci-v1 |
> | note | 单 task · 无 round |

---

## §1 自检 VERIFY

| # | 命令 | 结果 |
|---|------|------|
> | 1 | `python tools/tech_graph_test_manifest_check.py` | **pass** (12 entries) |
> | 2 | `pytest tests/test_tech_graph_test_manifest_check.py -q` | **pass** (12 passed) |
> | 3 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | **pass** (233 passed, 1 skipped) |
> | 4 | `python tools/tech_graph_manifest_check.py` | **pass** |
> | 5 | `python tools/tech_graph_contract_check.py` | **pass** |
> | 6 | `python tools/tech_graph_graph_export.py --check` | **pass** |
> | 7 | `python -c "import json; assert len(m['entries'])>=12"` | **pass** (entries=12) |

**结论：7/7 VERIFY 全绿。**

---

## §2 自检要点

- `test_manifest_check.py` JSON schema、必填字段、glob 匹配均正常。
- `--strict` 模式下仅 2 个已有 Phase A 条目的 error_code 不在 api/ 中（QUERY_REWRITE_ANCHOR_LOST / HEALTH_PROBE_FAIL），符合 SPEC 预期（Phase A 草案不阻塞）。
- 新增 6 条在 strict 模式下 error_codes 均有 api/ 匹配。
- pytest 新增 12 cases，未影响现有 233 passed。
- workflow step 已落盘，CI 将在 PR 上自动跑。

---

## §3 下一棒

**50 独立复检**

需重跑 §1 VERIFY 全部命令，并输出 `docs/tasks/reinspect_results/reinspect_gov-l2-manifest-ci_YYYYMMDD_v1.md`。

