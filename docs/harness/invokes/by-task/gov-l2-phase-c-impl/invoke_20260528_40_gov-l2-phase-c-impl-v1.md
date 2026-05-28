# Invoke · 40 自检 · gov-l2-phase-c-impl

> **task**: `docs/tasks/done/task_governance_l2_phase_c_impl_v1.md`

> **hat**: 40 · **freeze_id**: GOV-L2-PHASE-C-IMPL@2026-05-28

---

## §1 VERIFY 输出（粘贴）

```text
$ python tools/tech_graph_test_manifest_check.py
OK: test manifest valid (12 entries, test_paths globs resolved).

$ python tools/tech_graph_test_manifest_check.py --check-failure-paths
OK: test manifest valid (12 entries, test_paths globs resolved) [failure-paths].

$ pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short
242 passed, 1 skipped, 2 deselected, 55 warnings in 14.93s
```

---

## §2 自检结论

| 验收项 | 结果 |
|--------|------|
| C1 双向模式 exit 0 | pass |
| C2 抽样表 | pass · 30 invoke §2 |
| C3 Wiki 边界 | pass |
| pytest 绿 | pass |
| PR-B 无 coding_wiki 批量 | pass |

---

## §3 下一棒

**50 独立复检** — `reinspect_gov-l2-phase-c-impl_20260528_v1.md`
