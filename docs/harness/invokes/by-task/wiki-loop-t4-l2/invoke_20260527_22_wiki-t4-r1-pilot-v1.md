# Invoke · 22 任务审核 · R1 · wiki-t4-r1-pilot

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md` |
> | task_slug | `wiki-t4-r1-pilot` |
> | freeze_id | `GOV-T4-R1-PILOT@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |
> | cross_round_semi_auto | true |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 母 Loop：`task_harness_wiki_loop_t4_l2_v1.md` · `HG-LOOP-BATCH` = approved。
- 下一棒：30 执行编码。
- 按 `HANDOFF_AUTO_COMMIT.md` commit 后再切换。

## §2 审查结论

**零阻塞。可进入 30。**

- graph_nodes 4 id（C1/RAG/RAG_DOC/FTS）经 `graph_query neighbors` 全部 exit 0。
- relation（documents/triggers/branches）均在 Bridge SPEC §3.1 表内。
- 当前分支 diff 已覆盖：99_spec T4 指针、CODING_WIKI 字段/lint、Pilot synthesis graph_nodes。
- 待 30 补：`RECENT_TASK_SCHEDULE.md` §6.6 in_progress 行。

## §3 下一棒可复制 Prompt

```text
你正在执行 Wiki Loop T4+L2 **R1** 的 **30 执行编码帽**。上一帽（22 任务审核）已结束；本帽只按下文执行。

【元信息】
- round: R1
- hat: 30
- task: docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md
- task_slug: wiki-t4-r1-pilot
- freeze_id: GOV-T4-R1-PILOT@2026-05-27
- git_branch: task/gov-spec-t4-l2-v1
- pilot_synthesis: docs/coding_wiki/syntheses/query-rewrite-observability.md

### 当前分支状态
已有 3 文件修改（未提交）：
- docs/_tech_graph/99_spec.md  — 新增 Wiki↔图谱桥接（T4·叙事指针）小节
- docs/coding_wiki/CODING_WIKI.md  — T4 字段（graph_nodes）+ lint + 链 Bridge SPEC
- docs/coding_wiki/syntheses/query-rewrite-observability.md  — frontmatter graph_nodes（C1/RAG/RAG_DOC/FTS）+ 正文 T4 pointer

### 30 帽交付
1. 确认上述 3 文件修改满足 task 验收标准；若有缺漏，补正。
2. 更新 `docs/tasks/RECENT_TASK_SCHEDULE.md` §6.6：增 Wiki Loop T4+L2 **in_progress** 行（freeze_id：`WIKI-LOOP-T4-L2@2026-05-27`）。
3. `git add` 本轮路径 → `git commit`（按 HANDOFF_AUTO_COMMIT）。
4. 输出 40 自检 invoke。

### 硬约束
- 不改 api/、tests/、docs/harness/prompts/、CI workflow。
- commit message 含 freeze_id。
- 仅 docs；test_strategy = not_applicable。

### VERIFY（40 须重跑）
```bash
rg -n '^graph_nodes:' docs/coding_wiki/syntheses/query-rewrite-observability.md
rg -n 'graph_nodes' docs/coding_wiki/CODING_WIKI.md
for id in C1 RAG RAG_DOC FTS; do python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null; done
python tools/tech_graph_graph_export.py --check
```
```

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_wiki_t4_r1_pilot_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved（blocks 22,30,40,50）
├── 本棒交付：review 落盘 docs/harness/reviews/by-task/wiki-loop-t4-l2/ + invoke 落盘
├── 下一棒：A=30 执行编码 · B=—
├── 推荐：A（唯一路径）
└── 阻塞：无
```
