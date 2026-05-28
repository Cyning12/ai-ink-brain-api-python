# Invoke · gov-wiki-ingest-batch-3 · 40 · R3

| 项 | 值 |
| --- | --- |
| **round** | R3 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md` |
| **task_slug** | `gov-wiki-ingest-batch-3` |
| **freeze_id** | `GOV-WIKI-INGEST-BATCH-3@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 30（5 slug 已 commit @ 965d834） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 30 已结束；本帽为 40 自检帽，只按下文执行。

执行 Wiki Loop 单元 A · R3 · 40 自检。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only。
task: docs/tasks/active/task_governance_wiki_ingest_batch_3_v1.md
task_slug: gov-wiki-ingest-batch-3
freeze_id: GOV-WIKI-INGEST-BATCH-3@2026-05-28

**自检步骤**
1. 逐条对照 task 验收标准
2. 运行 VERIFY 命令
3. 粘贴输出要点
4. 回填 task 内 `### 自检结论（执行者）`
5. 落盘 40 invoke + commit
6. 无阻塞则自动戴 50 帽
```

---

## 自检结果

### 验收标准逐项核对

| # | 验收项 | 状态 | 证据 |
| --- | --- | --- | --- |
| 1 | HG-INGEST-BATCH-3-SCOPE approved | **pass** | 母单已 approved |
| 2 | syntheses ≥25 | **pass** | count=25 |
| 3 | 新 5 篇有 graph_nodes | **pass** | 全部含 frontmatter |
| 4 | R2 在 done/ | **pass** | 文件存在 |
| 5 | 无 api/tests/tools 改动 | **pass** | diff 无越界 |
| 6 | index/log 更新 | **pass** | 均已更新 |

### VERIFY 输出摘要

```
syntheses count: 25 → PASS
新 5 篇 graph_nodes: 全部 PASS
R2 in done/: PASS
无 api/tests/tools: PASS
index.md/log.md: PASS
```

### 结论

**全部验收项通过 · 零阻塞 · 可进入 50 复检**
