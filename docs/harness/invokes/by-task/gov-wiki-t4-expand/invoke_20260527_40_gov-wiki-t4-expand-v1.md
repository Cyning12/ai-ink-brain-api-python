# Invoke · 40 自检 · gov-wiki-t4-expand

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 40 |
> | task | `docs/tasks/active/task_governance_wiki_t4_expand_v2.md` |
> | task_slug | gov-wiki-t4-expand |
> | freeze_id | GOV-T4-EXPAND@2026-05-27 |
> | git_branch | task/gov-t4-l2-followup-v1 |

---

## §1 自检结论

**pass · 建议合并**

### 1.1 VERIFY 重跑

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `rg -l '^graph_nodes:' docs/coding_wiki/syntheses/` | pass | 3 files（≥3） |
| `graph_query neighbors T2S` | pass | exit 0 |
| `graph_query neighbors SSE` | pass | exit 0 |
| `graph_query neighbors U2` | pass | exit 0 |
| `graph_query neighbors CR1` | pass | exit 0 |
| `graph_query neighbors E2E_DOC` | pass | exit 0 |
| `manifest_check` | pass | exit 0 |
| `graph_export --check` | pass | exit 0 |

### 1.2 范围核对

| 检查项 | 结果 | 备注 |
|--------|------|------|
| 扩面 2 slug 各 ≥2 个 graph_nodes | pass | chatbi-v3-text2sql: 3 个；tech-graph-gate-d: 2 个 |
| 未改 api/ | pass | docs-only |
| 未改 tests/ | pass | docs-only |
| 未改 prompts/ | pass | docs-only |
| 未改 CI workflow | pass | docs-only |
| 未手改 graph.json | pass | 仅 frontmatter |

### 1.3 交付清单

- [x] `chatbi-v3-text2sql-tool-latency-obs.md`：`graph_nodes`（T2S/SSE/U2）+ T4 pointer
- [x] `tech-graph-gate-d-v2-tasks.md`：`graph_nodes`（CR1/E2E_DOC）+ T4 pointer
- [x] `CODING_WIKI.md`：修订记录增 T4 扩面 3 slug 行
- [x] `RECENT_TASK_SCHEDULE.md`：§6.6 T4 行 + §8 修订行
- [x] task 文件：实现备忘 + 自检结论回填

---

## §2 执行路线

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 30 执行编码 | graph_nodes 扩面 2 slug + CODING_WIKI + RECENT | 4 文件 | api-python@baf86bc |
| 2 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + 本 invoke | 本 commit |
| 3 | 50 独立复检 | 重跑 VERIFY + 复检报告 | `reinspect_*_YYYYMMDD_v1.md` | 下一 commit |
| 4 | 关账 | git mv → done/ + _views + CLOSE_TRACE | `done/task_*` + `_views/done.md` | 最终 commit |

---

## §3 50 下一棒 Prompt

```text
你正在执行 gov-wiki-t4-expand **50 独立复检**。

【必读】
- docs/tasks/active/task_governance_wiki_t4_expand_v2.md
- docs/harness/prompts/hats/50-independent-reinspect.md

【元信息】
- task_slug: gov-wiki-t4-expand
- freeze_id: GOV-T4-EXPAND@2026-05-27
- git_branch: task/gov-t4-l2-followup-v1

【复检重点】
1. 独立重跑 VERIFY：
   rg -l '^graph_nodes:' docs/coding_wiki/syntheses/   # 须 ≥3
   for id in T2S SSE U2 CR1 E2E_DOC; do
     python tools/tech_graph_graph_query.py neighbors "$id" >/dev/null
   done   # 须全 exit 0
   python tools/tech_graph_manifest_check.py
   python tools/tech_graph_graph_export.py --check

2. 抽样检查新增 graph_nodes 的 relation 合法性：
   documents / triggers / branches / yields / gates / merges / signoff / archives / evidence
   （须全在 SPEC §3.1 表内）

3. 确认未改 api/tests/prompts/CI

【交付】
- reinspect: docs/tasks/reinspect_results/reinspect_gov-wiki-t4-expand_YYYYMMDD_v1.md
- 10 项 pass/fail 表
- 建议：merge / rework

【关账（若建议合并）】
- git mv docs/tasks/active/task_governance_wiki_t4_expand_v2.md docs/tasks/done/
- 更新 docs/tasks/_views/done.md 增索引行
- 输出 HANDOFF_CLOSE_TRACE
- git commit
```

---

## §4 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：40 · 自检
├── task：task_governance_wiki_t4_expand_v2.md · audit_profile：post_close
├── 分支：task/gov-t4-l2-followup-v1
├── human_gate：HG-TASK-DRAFT approved · HG-AUDIT-R1 approved
├── 本棒交付：VERIFY 全绿 + task 回填 + 50 Prompt
├── 下一棒：50 独立复检
├── 推荐：—
└── 阻塞：无
```
