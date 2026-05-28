# Invoke · 40 自检 · gov-wiki-unit-ab-closeout

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 40 |
> | task_slug | gov-wiki-unit-ab-closeout |
> | freeze_id | GOV-WIKI-UNIT-AB-CLOSEOUT@2026-05-28 |
> | git_branch | task/gov-wiki-unit-ab-closeout-v1 |

---

## §1 VERIFY 输出要点

### §1 残留措辞 `rg`

```text
（无命中）
```

扫描路径：`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md` · `SPEC-Governance-Wiki-Harness-Roadmap-v1.md` · `RECENT_TASK_SCHEDULE.md`（§8 历史行允许过去态叙述）

### §2 Phase C CI（只读）

```text
.github/workflows/tech-graph.yml:31:  python tools/tech_graph_test_manifest_check.py --check-failure-paths
```

### §3 pytest（合并前必绿）

```text
242 passed, 1 skipped, 2 deselected
```

### §4 L2 manifest

```text
OK: test manifest valid (12 entries, test_paths globs resolved).
OK: test manifest valid (12 entries, test_paths globs resolved) [failure-paths].
```

### §5 human_gate

```text
harness_human_gate_check: OK
```

---

## §2 task §自检结论

| 项 | 结果 |
|----|------|
| VERIFY §1 `rg` | **pass** |
| VERIFY §2–§4 | **pass** |
| 结论 | **pass** |

---

## §3 下一棒

**50 独立复检** — diff 白名单；`reinspect_gov-wiki-unit-ab-closeout_20260528_v1.md`。
