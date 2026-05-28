# Invoke · gov-wiki-t4-rollout · 30 · R2

| 项 | 值 |
| --- | --- |
| **round** | R2 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_governance_wiki_t4_rollout_v1.md` |
| **task_slug** | `gov-wiki-t4-rollout` |
| **freeze_id** | `GOV-WIKI-T4-ROLLOUT@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 22（review 已落盘 @ e14a08b） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 22 已结束；本帽为 30 执行帽，只按下文执行。

执行 Wiki Loop 单元 A · R2 · 30 T4 graph_nodes 铺量。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only · 禁止 api/tests/tools。
task: docs/tasks/active/task_governance_wiki_t4_rollout_v1.md
task_slug: gov-wiki-t4-rollout
freeze_id: GOV-WIKI-T4-ROLLOUT@2026-05-28

**范围（14 篇 synthesis 补 graph_nodes frontmatter）**

铺量清单（当前无 graph_nodes → 补 frontmatter）：
1. chatbi-v3-p2-health-ready → [] 纯叙事
2. coding-wiki-pilot → [{id: RAG_DOC, relation: documents}]
3. coding-wiki-t1c-test-archive → [] 纯叙事
4. docs-tasks-reorg-move → [] 纯叙事
5. governance-l2-manifest-ci → [{id: E2E_DOC, relation: documents}]
6. governance-l2-r3-test-manifest → [{id: E2E_DOC, relation: documents}]
7. governance-wiki-agent-readorder → [] 纯叙事
8. governance-wiki-ingest-batch → [{id: CR1, relation: documents}]
9. harness-p1-docs-consolidation → [] 纯叙事
10. harness-wiki-loop-c2-verify → [{id: E2E_DOC, relation: documents}]
11. harness-wiki-loop-p2-followup → [] 纯叙事
12. wiki-ctx-ab-multi-slug → [{id: CR1, relation: evidence}]
13. wiki-ctx-ab-representative → [{id: RAG, relation: evidence}]
14. wiki-ctx-ab-v1 → [{id: RAG, relation: evidence}]

**验证纪律**
- graph_nodes[].id 须 `python tools/tech_graph_graph_query.py neighbors <id>` exit 0
- relation 用 SPEC §3.1 枚举
- 不改 synthesis 正文
- 每帽 commit 后再戴下一帽
```

---

## 执行记录

### graph_query 验证（3 次以上留证）

```bash
# 验证 1: RAG
$ python tools/tech_graph_graph_query.py neighbors RAG >/dev/null; echo $?
0

# 验证 2: CR1
$ python tools/tech_graph_graph_query.py neighbors CR1 >/dev/null; echo $?
0

# 验证 3: E2E_DOC
$ python tools/tech_graph_graph_query.py neighbors E2E_DOC >/dev/null; echo $?
0

# 验证 4: RAG_DOC
$ python tools/tech_graph_graph_query.py neighbors RAG_DOC >/dev/null; echo $?
0
```

### 铺量结果统计

| 类型 | 数量 | slug 示例 |
| --- | --- | --- |
| 有种子 id | 6 | coding-wiki-pilot, governance-l2-manifest-ci, governance-l2-r3-test-manifest, governance-wiki-ingest-batch, harness-wiki-loop-c2-verify, wiki-ctx-ab-multi-slug, wiki-ctx-ab-representative, wiki-ctx-ab-v1 |
| `[]` 纯叙事 | 8 | chatbi-v3-p2-health-ready, coding-wiki-t1c-test-archive, docs-tasks-reorg-move, governance-wiki-agent-readorder, harness-p1-docs-consolidation, harness-wiki-loop-p2-followup |
| 原有（跳过） | 6 | query-rewrite-observability, chatbi-v3-text2sql-tool-latency-obs, tech-graph-gate-d-v2-tasks, governance-wiki-t4-expand, governance-wiki-t4-r1-pilot, harness-wiki-loop-t4-l2 |
| **总计** | **20** | 全部含 `graph_nodes` frontmatter |

---

## 已修改文件

- `docs/coding_wiki/syntheses/chatbi-v3-p2-health-ready.md`
- `docs/coding_wiki/syntheses/coding-wiki-pilot.md`
- `docs/coding_wiki/syntheses/coding-wiki-t1c-test-archive.md`
- `docs/coding_wiki/syntheses/docs-tasks-reorg-move.md`
- `docs/coding_wiki/syntheses/governance-l2-manifest-ci.md`
- `docs/coding_wiki/syntheses/governance-l2-r3-test-manifest.md`
- `docs/coding_wiki/syntheses/governance-wiki-agent-readorder.md`
- `docs/coding_wiki/syntheses/governance-wiki-ingest-batch.md`
- `docs/coding_wiki/syntheses/harness-p1-docs-consolidation.md`
- `docs/coding_wiki/syntheses/harness-wiki-loop-c2-verify.md`
- `docs/coding_wiki/syntheses/harness-wiki-loop-p2-followup.md`
- `docs/coding_wiki/syntheses/wiki-ctx-ab-multi-slug.md`
- `docs/coding_wiki/syntheses/wiki-ctx-ab-representative.md`
- `docs/coding_wiki/syntheses/wiki-ctx-ab-v1.md`
