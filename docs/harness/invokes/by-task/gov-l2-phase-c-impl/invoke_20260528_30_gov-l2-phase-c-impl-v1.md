# Invoke · 30 执行编码 · gov-l2-phase-c-impl

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 30 |
> | task | `docs/tasks/done/task_governance_l2_phase_c_impl_v1.md` |
> | task_slug | gov-l2-phase-c-impl |
> | freeze_id | GOV-L2-PHASE-C-IMPL@2026-05-28 |
> | git_branch | task/wiki-unit-ab-plan-v1 |
> | executor | claude-code |

---

## §1 交付摘要

| # | 交付物 | 状态 |
|---|--------|------|
| 1 | `tools/tech_graph_test_manifest_check.py` `--check-failure-paths` | ✅ |
| 2 | `tests/test_tech_graph_test_manifest_check.py` Phase C 用例 + 生产 manifest 集成 | ✅ 16 passed |
| 3 | `docs/_tech_graph/_test_manifest.json` ref / error_codes 对齐 | ✅ |
| 4 | `docs/_tech_graph/99_spec.md` VERIFY 增 Phase C 行 | ✅ |

---

## §2 C2 抽样对照（≥3 Epic）

| manifest `id` | `failure_path_ref` | task 锚点 | error_codes（manifest） | 对照结论 |
| --- | --- | --- | --- | --- |
| `FP-RAG-DB-DISCONNECT` | `task_05_query_rewrite_observability.md` | F1 Supabase 不可用 | `DATABASE_DISCONNECT` | pass · corpus 含 api/index + test_chatbi_principal_network |
| `FP-QUERY-REWRITE-ANCHOR-LOST` | 同上 | F3 rewrite 失败 / query_compare | `is_key_entity_lost` | pass · api/index metadata + test_query_rewrite_compare_anchor |
| `FP-SQL-GATE-DENIED` | `task_chatbi_v3_sql_ast_text2sql_gate_v1.md` | FP-A AST 拒绝 | `ChatBiSqlGateDenied` | pass · 行内码与 manifest 子集一致 |
| `FP-HEALTH-PROBE-FAIL` | `task_chatbi_v3_p2_resilience_health_ready_v1.md` | F1 依赖未就绪 | `503` | pass · test_health_probe_routes 断言 503 + components |

---

## §3 VERIFY（30 预检）

```text
$ python tools/tech_graph_test_manifest_check.py
OK: test manifest valid (12 entries, test_paths globs resolved).

$ python tools/tech_graph_test_manifest_check.py --check-failure-paths
OK: test manifest valid (12 entries, test_paths globs resolved) [failure-paths].

$ pytest tests/test_tech_graph_test_manifest_check.py -q
16 passed

$ pytest tests -m "not intent_eval and not intent_benchmark" -q --tb=short
242 passed, 1 skipped, 2 deselected
```

---

## §4 下一棒

**40 自检帽** — 粘贴 §3 全量输出至 task §VERIFY / invoke_40；回填验收勾选。
