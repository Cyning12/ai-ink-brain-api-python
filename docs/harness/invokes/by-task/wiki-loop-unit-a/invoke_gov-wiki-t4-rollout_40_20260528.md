# Invoke · gov-wiki-t4-rollout · 40 · R2

| 项 | 值 |
| --- | --- |
| **round** | R2 |
| **hat** | 40 |
| **task** | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` |
| **task_slug** | `gov-wiki-t4-rollout` |
| **freeze_id** | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 30（14 篇 synthesis 已 commit @ a500b96） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 30 已结束；本帽为 40 自检帽，只按下文执行。

执行 Wiki Loop 单元 A · R2 · 40 自检。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only。
task: docs/tasks/active/task_governance_wiki_t4_rollout_v1.md
task_slug: gov-wiki-t4-rollout
freeze_id: GOV-WIKI-T4-ROLLOUT@2026-05-28

**自检步骤**
1. 逐条对照 task 验收标准
2. 运行 VERIFY 命令
3. 粘贴输出要点
4. 回填 task 内 `### 自检结论（执行者）`
5. 落盘 40 invoke + commit
6. 无阻塞则自动戴 50 帽

**VERIFY 清单**
- `for f in docs/coding_wiki/syntheses/*.md; do grep -q graph_nodes $f || echo MISS; done` → 0 miss
- `python tools/tech_graph_graph_query.py neighbors <id>` → exit 0（≥3 次）
- `test -f docs/tasks/done/task_governance_wiki_docs_hygiene_v1.md` → R1 已 done
- `git diff HEAD~1 --name-only | grep -E "^(api/|tests/|tools/)"` → 无输出
- `wc -c invoke_*` → ≥800 B
```

---

## 自检结果

### 验收标准逐项核对

| # | 验收项 | 状态 | 证据 |
| --- | --- | --- | --- |
| 1 | 14 slug 全部有 frontmatter 决策 | **pass** | 20/20 synthesis 含 graph_nodes；0 miss |
| 2 | ≥3 次 graph_query 留证 | **pass** | RAG/CR1/E2E_DOC 均 exit 0 |
| 3 | R1 已在 done/ | **pass** | `task_governance_wiki_docs_hygiene_v1.md` exists |
| 4 | invoke C2 全绿 | **pass** | 22=2221 B / 30=4080 B；§3 ≥15 行 |
| 5 | 无 api/tests/tools 改动 | **pass** | diff HEAD~1 无越界路径 |

### VERIFY 输出摘要

```
PASS: all 20 syntheses have graph_nodes
RAG: 0 | CR1: 0 | E2E_DOC: 0
PASS: R1 in done/
PASS: no api/tests/tools changes
invoke sizes: 2221 B / 4080 B (≥800 B)
```

### 结论

**全部验收项通过 · 零阻塞 · 可进入 50 复检**
