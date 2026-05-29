# Invoke · 40 自检 · gov-wiki-t4-ops

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_wiki_t4_ops_v1.md` |
> | task_slug | gov-wiki-t4-ops |
> | freeze_id | GOV-WIKI-T4-OPS@2026-05-29 |
> | git_branch | task/gov-wiki-t4-ops-v1 |

---

## §1 VERIFY 命令输出要点

### §1 lint 全树

```text
$ python tools/coding_wiki_graph_nodes_lint.py
coding_wiki_graph_nodes_lint: OK
exit 0
```

### §2 lint 单测

```text
$ pytest tests/test_coding_wiki_graph_nodes_lint.py -q --tb=short
7 passed in 0.02s
exit 0
```

### §3 25/25 synthesis 含 graph_nodes 键

```text
$ python - <<'PY' …
OK: 25 syntheses
exit 0
```

### §4 99_spec Wiki pointer

```text
$ rg -n "Wiki|T4|graph_nodes|TechGraph-Bridge" docs/_tech_graph/99_spec.md
42:### Wiki ↔ 图谱桥接（T4 · 叙事指针）
46:… TechGraph-Bridge …
50:| **Lint** | python tools/coding_wiki_graph_nodes_lint.py …
exit 0
```

### §5 合并前必绿

```text
$ pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short
249 passed, 1 skipped, 2 deselected
exit 0
```

### §6 图谱

```text
$ python tools/tech_graph_graph_export.py --check
OK

$ python tools/tech_graph_manifest_check.py
OK: manifest matches code/SQL truth …
exit 0
```

### §7 关账前人闸

```text
$ python tools/harness_human_gate_check.py --task docs/tasks/active/task_governance_wiki_t4_ops_v1.md
harness_human_gate_check: OK
exit 0
```

---

## §2 task §自检结论

| 项 | 结果 |
|----|------|
| VERIFY §1–§4 | **pass** |
| VERIFY §5–§6 | **pass** |
| 结论 | **pass** |

---

## §3 下一棒

**50 独立复检** — diff 白名单核对；落盘 `reinspect_gov-wiki-t4-ops_20260529_v1.md`。

---

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── task：task_governance_wiki_t4_ops_v1.md
├── 分支：task/gov-wiki-t4-ops-v1
├── VERIFY：7/7 pass
├── 下一棒：50 独立复检
└── 阻塞：无
```
