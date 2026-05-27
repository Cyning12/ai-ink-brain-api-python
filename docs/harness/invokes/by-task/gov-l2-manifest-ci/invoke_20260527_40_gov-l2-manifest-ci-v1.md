# Invoke · 40 自检 · gov-l2-manifest-ci

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 40 |
> | task | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` |
> | task_slug | gov-l2-manifest-ci |
> | freeze_id | GOV-L2-MANIFEST-CI@2026-05-27 |
> | git_branch | task/gov-l2-manifest-ci-v1 |
> | note | 单 task · 无 round |

---

## §1 自检 VERIFY

| # | 命令 | 结果 |
|---|------|------|
| 1 | `python tools/tech_graph_test_manifest_check.py` | **pass** (12 entries) |
| 2 | `pytest tests/test_tech_graph_test_manifest_check.py -q` | **pass** (12 passed) |
| 3 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` | **pass** (233 passed, 1 skipped) |
| 4 | `python tools/tech_graph_manifest_check.py` | **pass** |
| 5 | `python tools/tech_graph_contract_check.py` | **pass** |
| 6 | `python tools/tech_graph_graph_export.py --check` | **pass** |
| 7 | `python -c "import json; assert len(m['entries'])>=12"` | **pass** (entries=12) |

**结论：7/7 VERIFY 全绿。**

---

## §2 自检要点

- `test_manifest_check.py` JSON schema、必填字段、glob 匹配均正常。
- `--strict` 模式下仅 2 个已有 Phase A 条目的 error_code 不在 api/ 中（QUERY_REWRITE_ANCHOR_LOST / HEALTH_PROBE_FAIL），符合 SPEC 预期（Phase A 草案不阻塞）。
- 新增 6 条在 strict 模式下 error_codes 均有 api/ 匹配。
- pytest 新增 12 cases，未影响现有 233 passed。
- workflow step 已落盘，CI 将在 PR 上自动跑。

---

## §3 自检结论与下一棒

| 项 | 结果 |
|----|------|
| 命令 | task §VERIFY 7 条（见 §1） |
| 结论 | **pass** |
| 要点 | 7/7 全绿；task §自检结论已回填；非范围纪律未越界 |

### 3.1 对应 commit

| 帽 | commit | 摘要 |
|----|--------|------|
| 40 | `0084299` | 自检 VERIFY 7/7 全绿 + task §自检结论 |

### 3.2 下一棒 · 50 独立复检

- 独立重跑 §1 全部 VERIFY 命令（不得仅引用 40 输出）。
- 落盘 `docs/tasks/reinspect_results/reinspect_gov-l2-manifest-ci_20260527_v1.md`。
- 对照 git diff：确认未改 api/ 业务、未手改 graph.json、workflow step 存在。

---

## §4 下一棒 Prompt（50）

```text
你正在执行 gov-l2-manifest-ci **50 独立复检**。

【必读】
- docs/tasks/done/task_governance_l2_manifest_ci_v1.md
- docs/harness/prompts/hats/50-independent-reinspect.md

【元信息】
- task_slug: gov-l2-manifest-ci
- freeze_id: GOV-L2-MANIFEST-CI@2026-05-27
- git_branch: task/gov-l2-manifest-ci-v1

【交付】
1. 重跑 task §VERIFY 7 条命令并附证据
2. reinspect 落盘 docs/tasks/reinspect_results/reinspect_gov-l2-manifest-ci_20260527_v1.md
3. invoke_50 · commit
```
