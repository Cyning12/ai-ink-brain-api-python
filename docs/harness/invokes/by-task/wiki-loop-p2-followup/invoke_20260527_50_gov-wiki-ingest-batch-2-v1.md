# Invoke · 50 独立复检 · R3 · gov-wiki-ingest-batch-2

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 50 |
> | task | `docs/tasks/done/task_governance_wiki_ingest_batch_2_v1.md` |
> | task_slug | `gov-wiki-ingest-batch-2` |
> | freeze_id | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |
> | reinspect | `docs/tasks/reinspect_results/reinspect_gov-wiki-ingest-batch-2_20260527_v1.md` |

---

## §1 角色与纪律

- 本帽为 **50 独立复检**；落盘 `reinspect_*`（见路径上表）。

## §2 复检结论

**建议合并。** 见 reinspect 逐项表（≥8 项）。

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R3 关账**。

【元信息】
- round: R3 · hat: CLOSE
- task_slug: gov-wiki-ingest-batch-2
- freeze_id: GOV-WIKI-INGEST-BATCH-2@2026-05-27

### 关账
1. `git mv` → done/（若尚未）· `_views/done.md`
2. `invoke_20260527_CLOSE_gov-wiki-ingest-batch-2-v1.md` + CLOSE_TRACE
3. commit

### META（三轮子 task 均 done/ 后）
1. 母单 `task_harness_wiki_loop_p2_followup_v1.md` → done/
2. `REPORT_completion_wiki_loop_p2_followup_v1.md` · RECENT §6.6 P2 Loop **done**
3. 更新 `harness-wiki-loop-p2-followup` synthesis `source_task` → done/
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：50 · R3
└── 下一棒：R3 CLOSE → META
```
