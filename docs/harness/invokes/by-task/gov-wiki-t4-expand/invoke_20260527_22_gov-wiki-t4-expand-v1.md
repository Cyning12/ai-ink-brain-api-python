# Invoke · 22 任务审核 · gov-wiki-t4-expand

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 22 |
> | task | `docs/tasks/active/task_governance_wiki_t4_expand_v2.md` |
> | task_slug | gov-wiki-t4-expand |
> | freeze_id | GOV-T4-EXPAND@2026-05-27 |
> | git_branch | task/gov-t4-l2-followup-v1 |
> | note | **追溯补全** · 对应 commit dc67ec6 前序审核 |

---

## §1 角色与纪律

- 本帽为 **22 任务审核**（`docs/harness/prompts/hats/22-task-audit.md`）。
- 单 task（非 Loop）· 无 round。

## §2 审核结论

**无阻塞 · 可进入 30 执行编码。**

### 2.1 已核对项

| # | 项 | 结果 |
|---|----|------|
| 1 | `HG-TASK-DRAFT` = approved | pass |
| 2 | `HG-AUDIT-R1` = approved | pass（本 review 追溯补全） |
| 3 | task 头部元信息完整 | pass |
| 4 | 范围（2 篇必做 slug）清晰 | pass |
| 5 | 验收标准可执行 | pass |
| 6 | 非范围明确 | pass |
| 7 | Bridge SPEC 可读 | pass |
| 8 | Pilot 样例已存在 | pass |

### 2.2 阻塞项

无。

## §3 审核落盘

审查文档：`docs/harness/reviews/by-task/gov-wiki-t4-expand/task_governance_wiki_t4_expand_audit_R1_20260527.md`

---

## §4 执行路线

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | **22 任务审核** | review + invoke 落盘 | `reviews/by-task/gov-wiki-t4-expand/*` | dc67ec6（前序） |
| 2 | 30 执行编码 | graph_nodes 扩面 2 slug + CODING_WIKI + RECENT | 4 文件 | 下一 commit |
| 3 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | 后续 commit |
| 4 | 50 独立复检 | 重跑 VERIFY + 复检报告 | `reinspect_*_YYYYMMDD_v1.md` | 后续 commit |
| 5 | 关账 | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | 最终 commit |

---

## §5 下一棒 Prompt

```text
你正在执行 gov-wiki-t4-expand **30 执行编码**。

【必读】
- docs/tasks/active/task_governance_wiki_t4_expand_v2.md
- docs/spec/governance/SPEC-Governance-Wiki-TechGraph-Bridge-v1.md
- docs/coding_wiki/syntheses/query-rewrite-observability.md（Pilot 样例）

【元信息】
- task_slug: gov-wiki-t4-expand
- freeze_id: GOV-T4-EXPAND@2026-05-27
- git_branch: task/gov-t4-l2-followup-v1

【交付】
1. chatbi-v3-text2sql-tool-latency-obs.md：graph_nodes（2–4 个）+ T4 pointer
2. tech-graph-gate-d-v2-tasks.md：graph_nodes（2–4 个）+ T4 pointer
3. CODING_WIKI.md：修订记录增 T4 扩面覆盖说明
4. RECENT_TASK_SCHEDULE.md：§6.6 T4 行 + §8 修订一行
5. 每个 node id：python tools/tech_graph_graph_query.py neighbors <id> → exit 0

【commit】
git add → commit（HANDOFF_AUTO_COMMIT）
```

---

## §6 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_wiki_t4_expand_v2.md · audit_profile：post_close
├── 分支：task/gov-t4-l2-followup-v1
├── human_gate：HG-TASK-DRAFT approved · HG-AUDIT-R1 approved
├── 本棒交付：review 落盘 + invoke 落盘 + 30 Prompt
├── 下一棒：30 执行编码
├── 推荐：—
└── 阻塞：无
```
