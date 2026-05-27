# 任务审核 — T4 Wiki 图谱桥接 Pilot（R1）

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | task | `docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md` |
> | task_slug | `wiki-t4-r1-pilot` |
> | freeze_id | `GOV-T4-R1-PILOT@2026-05-27` |
> | round | R1 |
> | audit_profile | post_close |
> | invoke_snapshot | `docs/harness/invokes/by-task/wiki-loop-t4-l2/invoke_20260527_22_wiki-t4-r1-pilot-v1.md` |

---

## 审查结论摘要

**零阻塞。建议执行帽开工。**

- 母闸 `HG-LOOP-BATCH` 状态 `approved`（母 task `task_harness_wiki_loop_t4_l2_v1.md`）。
- 任务范围明确：Pilot 固定为 `query-rewrite-observability`，仅 docs（`syntheses/`、`CODING_WIKI.md`、`RECENT_TASK_SCHEDULE.md`）。
- 验收标准可执行：4 条 VERIFY 命令均已本地预跑通过。
- failure_paths 覆盖母闸 pending、graph_nodes id 不存在、relation 非法、RECENT 误标 done。

---

## 已核对项

| # | 检查项 | 结果 | 证据 |
|---|--------|------|------|
| 1 | `HG-LOOP-BATCH` = approved | pass | 母 task §human_gate |
| 2 | task 含验收标准 + VERIFY 命令 | pass | task §验收标准 |
| 3 | task 含 failure_paths | pass | task §失败路径 |
| 4 | graph_nodes id 存在于 graph_v2 | pass | `graph_query neighbors C1/RAG/RAG_DOC/FTS` exit 0 |
| 5 | graph_nodes relation 在 Bridge SPEC §3.1 | pass | `documents`/`triggers`/`branches` 均入表 |
| 6 | 不改 api/tests/prompts/CI | pass | task §非范围 |
| 7 | CODING_WIKI.md diff 已含 T4 字段/lint | pass | 当前分支 diff：`+graph_nodes` 字段、`+lint` 行、链 Bridge SPEC |
| 8 | 99_spec.md 已增 Wiki 桥接 pointer | pass | 当前分支 diff：`+T4 · 叙事指针` 小节 |

---

## 阻塞 / 非阻塞

**无阻塞。**

唯一待完成项：`RECENT_TASK_SCHEDULE.md` §6.6 增 Wiki Loop T4+L2 **in_progress** 行（属 30 帽范围）。

---

## 签收 / 关闭

本 task **R1 可进入执行帽**。30 帽负责：
1. `git add` + `git commit` 当前分支已有 3 文件修改（`99_spec.md`、`CODING_WIKI.md`、`query-rewrite-observability.md`）。
2. 补充 `RECENT_TASK_SCHEDULE.md` §6.6 in_progress 行。
3. 40 自检后回填 task `### 自检结论`。

---

## 下一棒可复制 Prompt

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
