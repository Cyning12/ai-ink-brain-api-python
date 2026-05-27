# Invoke · 30 执行编码 · gov-l2-manifest-ci

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_l2_manifest_ci_v1.md` |
> | task_slug | gov-l2-manifest-ci |
> | freeze_id | GOV-L2-MANIFEST-CI@2026-05-27 |
> | git_branch | task/gov-l2-manifest-ci-v1 |
> | note | 单 task · 无 round |

---

## §1 交付摘要

| # | 交付物 | 路径 | 状态 |
> |---|--------|------|------|
> | 1 | `_test_manifest.json` 扩面 | `docs/_tech_graph/_test_manifest.json` | ✅ 12 entries |
> | 2 | `tech_graph_test_manifest_check.py` | `tools/tech_graph_test_manifest_check.py` | ✅ JSON schema + glob + 可选 --strict |
> | 3 | pytest | `tests/test_tech_graph_test_manifest_check.py` | ✅ 12 cases 全绿 |
> | 4 | workflow step | `.github/workflows/tech-graph.yml` | ✅ manifest_check job 增 step |
> | 5 | `99_spec.md` | `docs/_tech_graph/99_spec.md` | ✅ 补脚本行 + VERIFY 命令块 |
> | 6 | `RECENT_TASK_SCHEDULE.md` | `docs/tasks/RECENT_TASK_SCHEDULE.md` | ✅ §6.6 done + §8 修订行 |

---

## §2 VERIFY 结果（30 帽内预检）

```bash
python tools/tech_graph_test_manifest_check.py              # OK (12 entries)
pytest tests/test_tech_graph_test_manifest_check.py -q      # 12 passed
pytest tests -m "not intent_eval and not intent_benchmark" -q  # 233 passed, 1 skipped
python tools/tech_graph_manifest_check.py                   # OK
python tools/tech_graph_contract_check.py                   # OK
python tools/tech_graph_graph_export.py --check             # OK
python -c "import json; ... assert len(m['entries'])>=12"   # entries=12 OK
```

---

## §3 自检结论（40 帽回填区）

| 项 | 结果 |
|----|------|
| 命令 | （40 帽回填） |
| 结论 | （40 帽回填） |
| 要点 | （40 帽回填） |

---

## §4 下一棒

**40 自检帽**

