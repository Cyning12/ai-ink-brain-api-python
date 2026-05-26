# Invoke · 40 帽 · Wiki Loop A1 · ingest test_strategy（v1）

| 字段 | 值 |
|------|-----|
| **hat_id** | 40 · 自检 |
| **task_slug** | `wiki-a1-ingest-test-strategy` |
| **task_path** | `docs/tasks/active/task_coding_wiki_ingest_test_strategy_v1.md` |
| **freeze_id** | `CODING-WIKI-A1-TEST-STRATEGY@2026-05-26` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **round** | A1 |
| **semi_auto** | true |
| **date** | 2026-05-26 |
| **invoke_snapshot** | 本文件 |

---

## §3 调用体快照

```text
Wiki Loop A1 · 40 自检帽 · 重跑 VERIFY + 回填 §自检结论
```

---

## VERIFY 执行记录

| 命令 | 结果 |
|------|------|
| `rg -n test_strategy docs/coding_wiki/syntheses/query-rewrite-observability.md` | 3 行命中，含 `recommended` |
| `git diff` 范围 | 仅 `docs/coding_wiki/*`、task、harness 落盘；无 `api/`/`tests/`/`prompts/` |
| `pytest tests -m "not intent_eval and not intent_benchmark" -q` | **221 passed**, 1 skipped |

---

## 下一棒

- **帽**：50 · 独立复检
- **invoke**：`invoke_20260526_50_wiki-a1-ingest-test-strategy-v1.md`
