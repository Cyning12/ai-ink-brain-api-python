# Invoke · 30 执行编码 · gov-l2-manifest-ci

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 30 |
> | task | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` |
> | task_slug | gov-l2-manifest-ci |
> | freeze_id | GOV-L2-MANIFEST-CI@2026-05-27 |
> | git_branch | task/gov-l2-manifest-ci-v1 |
> | note | 单 task · 无 round |

---

## §1 交付摘要

| # | 交付物 | 路径 | 状态 |
|---|--------|------|------|
| 1 | `_test_manifest.json` 扩面 | `docs/_tech_graph/_test_manifest.json` | ✅ 12 entries |
| 2 | `tech_graph_test_manifest_check.py` | `tools/tech_graph_test_manifest_check.py` | ✅ JSON schema + glob + 可选 --strict |
| 3 | pytest | `tests/test_tech_graph_test_manifest_check.py` | ✅ 12 cases 全绿 |
| 4 | workflow step | `.github/workflows/tech-graph.yml` | ✅ manifest_check job 增 step |
| 5 | `99_spec.md` | `docs/_tech_graph/99_spec.md` | ✅ 补脚本行 + VERIFY 命令块 |
| 6 | `RECENT_TASK_SCHEDULE.md` | `docs/tasks/RECENT_TASK_SCHEDULE.md` | ✅ §6.6 done + §8 修订行 |

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

## §3 执行路线

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/gov-l2-manifest-ci/*` | `13d58d7` |
| 2 | **30 执行编码** | manifest 12 entries + 脚本 + pytest + workflow + spec + RECENT | 8 文件 | **本 commit `6fbc862`** |
| 3 | 40 自检 | VERIFY 7/7 + task §自检结论回填 | task + `invoke_20260527_40_*` | 下一 commit |
| 4 | 50 独立复检 | 重跑 VERIFY + reinspect 落盘 | `reinspect_gov-l2-manifest-ci_20260527_v1.md` | 后续 commit |
| 5 | 关账 | git mv → done/ + _views + CLOSE invoke | `done/task_*` + `_views/done.md` | 最终 commit |

### 3.1 新增 manifest 条目（6 条）

| id | 域 |
|----|-----|
| FP-PROMPT-GUARD-BLOCKED | Prompt guard |
| FP-ADMIN-INGEST-INVALID-TYPE | Admin ingest |
| FP-CHAIN-CHAT-MISSING-FIELD | Chain chat |
| FP-CLIENT-CLOSED-REQUEST | Unified chat |
| FP-TOKEN-INVALID | ChatBI access |
| FP-SUPABASE-RETRY-EXHAUSTED | Supabase retry |

### 3.2 task §实现备忘

已在 30 commit 回填涉及文件列表与 CI 变更说明。

---

## §4 下一棒

**40 自检帽** — 重跑 task §VERIFY 全部命令；回填 task §自检结论。
