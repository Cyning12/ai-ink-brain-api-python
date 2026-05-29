# Invoke · 30 执行编码 · gov-wiki-t4-ops

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_wiki_t4_ops_v1.md` |
> | task_slug | gov-wiki-t4-ops |
> | freeze_id | GOV-WIKI-T4-OPS@2026-05-29 |
> | git_branch | task/gov-wiki-t4-ops-v1 |

---

## §1 交付摘要

| # | 交付物 | 路径 | 状态 |
|---|--------|------|------|
| 1 | graph_nodes lint | `tools/coding_wiki_graph_nodes_lint.py` | ✅ |
| 2 | pytest | `tests/test_coding_wiki_graph_nodes_lint.py` | ✅ 7 passed |
| 3 | 汇总页 frontmatter | `governance-wiki-t4-expand` · `governance-wiki-t4-r1-pilot` · `harness-wiki-loop-t4-l2` | ✅ `graph_nodes: []` |
| 4 | CODING_WIKI | §3 25/25 覆盖 · §4.3 lint VERIFY | ✅ |
| 5 | Bridge SPEC | §5.1 勾选 · §7 V4 lint | ✅ |
| 6 | 99_spec | Wiki 桥接 + lint 行 | ✅ |
| 7 | RECENT | §6.6 · §8（关账时 done 行） | ✅ |

---

## §2 VERIFY 结果（30 帽内预检）

```bash
python tools/coding_wiki_graph_nodes_lint.py              # OK
pytest tests/test_coding_wiki_graph_nodes_lint.py -q      # 7 passed
python -c "… assert 25 syntheses graph_nodes …"           # OK: 25 syntheses
rg -n "Wiki|T4|graph_nodes|TechGraph-Bridge" 99_spec.md   # 命中 Wiki 桥接小节
pytest tests -m "not intent_eval and not intent_benchmark" -q  # 249 passed, 1 skipped
python tools/tech_graph_graph_export.py --check             # OK
python tools/tech_graph_manifest_check.py                   # OK
```

---

## §3 lint 行为（task 回填）

| 项 | 取值 |
|----|------|
| missing key | **fail**（syntheses 强制存在 `graph_nodes` 键） |
| `graph_nodes: []` | **pass** |
| concepts 扫描 | **否**（本 task 默认仅 `syntheses/`） |
| relation 枚举 | Bridge SPEC §3.1 九项 |
| id 存在性 | `graph_query neighbors`（内存 store，等价 CLI exit 0） |

---

## §4 涉及文件

- `tools/coding_wiki_graph_nodes_lint.py`（新增）
- `tests/test_coding_wiki_graph_nodes_lint.py`（新增）
- `docs/coding_wiki/syntheses/governance-wiki-t4-expand.md`
- `docs/coding_wiki/syntheses/governance-wiki-t4-r1-pilot.md`
- `docs/coding_wiki/syntheses/harness-wiki-loop-t4-l2.md`
- `docs/coding_wiki/CODING_WIKI.md`
- `docs/_tech_graph/99_spec.md`
- `docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md`
- `docs/tasks/RECENT_TASK_SCHEDULE.md`
- Harness invoke/review（本目录 + `reviews/by-task/gov-wiki-t4-ops/`）

---

## §5 下一棒

**40 自检帽** — 重跑 task §VERIFY 全部命令；回填 task §自检结论。
