# Invoke · 30 执行编码 · R3 · gov-wiki-ingest-batch-2

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_wiki_ingest_batch_2_v1.md` |
> | task_slug | `gov-wiki-ingest-batch-2` |
> | freeze_id | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **30 执行编码**；Wiki ingest · `test_strategy: not_applicable`。

## §2 交付摘要

| 交付物 | 说明 |
| --- | --- |
| 新 synthesis ×5 | `wiki-ctx-ab-representative` · `governance-wiki-agent-readorder` · `governance-wiki-ingest-batch` · `coding-wiki-t1c-test-archive` · `harness-wiki-loop-p2-followup` |
| 既有 | `harness-wiki-loop-t4-l2`（Batch-2 覆盖 slug 之一） |
| 索引 | `index.md` +5 行 · `log.md` batch-ingest-2 |
| 计数 | syntheses **20** 篇 |

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R3** 的 **40 自检帽**。上一帽（30）已结束。

【元信息】
- round: R3
- hat: 40
- task: docs/tasks/active/task_governance_wiki_ingest_batch_2_v1.md
- task_slug: gov-wiki-ingest-batch-2
- freeze_id: GOV-WIKI-INGEST-BATCH-2@2026-05-27
- git_branch: task/wiki-loop-p2-followup-v1

### 40 帽交付
1. 重跑 VERIFY（附 exit code）：
   - `ls docs/coding_wiki/syntheses/*.md | wc -l` ≥ 20
   - `rg` 5 slug 均在 `index.md`
   - 抽样 2 篇 synthesis frontmatter（`layer: L2` · `source_task` → `done/`）
   - `python tools/tech_graph_manifest_check.py`
2. 回填 task 自检表。
3. 落盘 **50** invoke + 扩写 `reinspect_gov-wiki-ingest-batch-2_20260527_v1.md`。
4. commit。

### 硬约束
- 无 api/tests diff。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · R3 ingest
├── syntheses：20
└── 下一棒：40
```
