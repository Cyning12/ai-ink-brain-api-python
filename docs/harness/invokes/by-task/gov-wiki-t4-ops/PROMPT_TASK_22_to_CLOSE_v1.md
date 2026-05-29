# P1 · T4 运营化 · 22→关账

> **task**：`docs/tasks/active/task_governance_wiki_t4_ops_v1.md`  
> **分支**：`task/gov-wiki-t4-ops-v1`（从最新 `origin/main` 拉出）

---

## 执行前

```bash
git checkout main && git pull origin main
git checkout -b task/gov-wiki-t4-ops-v1

python tools/harness_human_gate_check.py \
  --task docs/tasks/active/task_governance_wiki_t4_ops_v1.md
```

---

## §3 可复制 Prompt（22→关账）

```text
【步骤 0 · Gate】打开 task_governance_wiki_t4_ops_v1.md，扫描 human_gate。
HG-TASK-DRAFT / HG-AUDIT-R1 未 approved → 硬停。
HG-REINSPECT 在 50 前须 approved。

执行 P1 · gov-wiki-t4-ops · test_strategy: recommended · 22→30→40→50→关账。
分支 task/gov-wiki-t4-ops-v1。

必读 @：
- docs/tasks/active/task_governance_wiki_t4_ops_v1.md
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md §4.3 · §5.1
- docs/coding_wiki/CODING_WIKI.md §4
- docs/tasks/skills/SKILL-harness-task.md
- tools/tech_graph_graph_query.py（lint 复用）
- 本文件 PROMPT_TASK_22_to_CLOSE_v1.md

【30 要点】
1. tools/coding_wiki_graph_nodes_lint.py + pytest
2. 99_spec.md Wiki 桥接 pointer（≤30 行）
3. 3 篇 T4 汇总 synthesis：graph_nodes: []
4. CODING_WIKI 25/25 覆盖表 · Bridge SPEC §5.1 勾选
5. RECENT §6.6 · 每帽 invoke/review/reinspect · HANDOFF_AUTO_COMMIT

【40】粘贴 task §VERIFY 全部命令输出要点。

【50】独立复检 diff 白名单；reinspect_gov-wiki-t4-ops_<date>_v1.md。

关账：git mv done/ · _views · CLOSE_TRACE。
```

---

## C2 / invoke 落盘

| 帽 | 路径模式 |
|----|----------|
| 22 | `docs/harness/reviews/by-task/gov-wiki-t4-ops/review_*_22_*` |
| 30 | `docs/harness/invokes/by-task/gov-wiki-t4-ops/invoke_*_30_*` |
| 40 | `docs/harness/invokes/by-task/gov-wiki-t4-ops/invoke_*_40_*` |
| 50 | `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-ops_*` |

§3 正文 **≥15 行**；元信息含 `task_slug` · `freeze_id` · `git_branch`。
