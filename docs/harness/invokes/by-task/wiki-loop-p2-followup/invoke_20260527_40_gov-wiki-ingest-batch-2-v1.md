# Invoke · 40 自检 · R3 · gov-wiki-ingest-batch-2

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_wiki_ingest_batch_2_v1.md` |
> | task_slug | `gov-wiki-ingest-batch-2` |
> | freeze_id | `GOV-WIKI-INGEST-BATCH-2@2026-05-27` |
> | git_branch | `task/wiki-loop-p2-followup-v1` |

---

## §1 角色与纪律

- 本帽为 **40 自检**；独立重跑 VERIFY。

## §2 自检结果

### 2.1 命令输出

**V1 · syntheses 计数**：
```bash
$ ls docs/coding_wiki/syntheses/*.md | wc -l
20
EXIT:0
```

**V2 · index 含 Batch-2 slug**：
```bash
$ rg -n 'wiki-ctx-ab-representative|governance-wiki-agent-readorder|governance-wiki-ingest-batch|harness-wiki-loop-p2-followup|coding-wiki-t1c-test-archive' docs/coding_wiki/index.md
# 5 hits
EXIT:0
```

**V3 · manifest_check**：
```bash
$ python tools/tech_graph_manifest_check.py
EXIT:0
```

**V4 · log.md batch-ingest-2**：
```bash
$ rg -n 'batch-ingest-2' docs/coding_wiki/log.md
EXIT:0
```

### 2.2 验收

| 项 | 结果 |
| --- | --- |
| ≥20 syntheses | **pass** |
| 5 slug 覆盖 | **pass** |
| HG scope approved | **pass**（母单） |
| docs-only | **pass** |

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop P2 后续 **R3** 的 **50 独立复检帽**。

【元信息】
- round: R3 · hat: 50
- task_slug: gov-wiki-ingest-batch-2
- freeze_id: GOV-WIKI-INGEST-BATCH-2@2026-05-27

### 50 交付
1. 重跑上表 VERIFY → `reinspect_gov-wiki-ingest-batch-2_20260527_v1.md`。
2. 关账：git mv task → done/ · _views · `invoke_*_CLOSE_*`。
3. commit 后 **META 关账**（母单 · REPORT_completion）。
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · R3
└── VERIFY：4/4 pass
```
