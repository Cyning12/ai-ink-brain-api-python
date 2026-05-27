# Invoke · 30 执行编码 · gov-wiki-t4-expand

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 30 |
> | task | `docs/tasks/active/task_governance_wiki_t4_expand_v2.md` |
> | task_slug | gov-wiki-t4-expand |
> | freeze_id | GOV-T4-EXPAND@2026-05-27 |
> | git_branch | task/gov-t4-l2-followup-v1 |
> | note | **追溯补全** · 对应 commit baf86bc |

---

## §1 执行摘要

T4 `graph_nodes` 扩面 2 篇 synthesis + CODING_WIKI 覆盖说明 + RECENT 同步。

## §2 交付详情

### 2.1 chatbi-v3-text2sql-tool-latency-obs.md

- frontmatter 新增 `graph_nodes`（3 项）：
  - `id: T2S` · `relation: documents` · Text2SQL 子流程
  - `id: SSE` · `relation: triggers` · SSE 流式子阶段
  - `id: U2` · `relation: documents` · Unified SSE 契约
- 正文新增 T4 pointer 行（Bridge SPEC §4.1 读序）
- 验证：`graph_query neighbors T2S/SSE/U2` → exit 0

### 2.2 tech-graph-gate-d-v2-tasks.md

- frontmatter 新增 `graph_nodes`（2 项）：
  - `id: CR1` · `relation: documents` · Code Query / graph_query v2 消费
  - `id: E2E_DOC` · `relation: documents` · E2E 边界 / 闸口 D 验证基线
- 正文新增 T4 pointer 行
- 验证：`graph_query neighbors CR1/E2E_DOC` → exit 0

### 2.3 CODING_WIKI.md

- §修订记录 增一行：T4 扩面 3 slug 含 `graph_nodes`

### 2.4 RECENT_TASK_SCHEDULE.md

- §6.6 T4 行更新：Pilot done → 3 slug 扩面
- §8 增修订行（2026-05-27）

---

## §3 执行路线

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/gov-wiki-t4-expand/*` | dc67ec6（前序） |
| 2 | **30 执行编码** | graph_nodes 扩面 2 slug + CODING_WIKI + RECENT | 4 文件 | 本 commit（baf86bc） |
| 3 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | 下一 commit |
| 4 | 50 独立复检 | 重跑 VERIFY + 复检报告 | `reinspect_*_YYYYMMDD_v1.md` | 后续 commit |
| 5 | 关账 | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | 最终 commit |

---

## §4 40 下一棒 Prompt

```text
你正在执行 gov-wiki-t4-expand **40 自检**。

【必读】
- docs/tasks/active/task_governance_wiki_t4_expand_v2.md
- docs/harness/prompts/hats/40-self-check.md

【元信息】
- task_slug: gov-wiki-t4-expand
- freeze_id: GOV-T4-EXPAND@2026-05-27
- git_branch: task/gov-t4-l2-followup-v1

【自检】
1. VERIFY：rg -l '^graph_nodes:' docs/coding_wiki/syntheses/（须 ≥3）
2. 逐 id 跑 graph_query neighbors（T2S/SSE/U2/CR1/E2E_DOC）→ exit 0
3. manifest_check + graph_export --check → 绿
4. 确认未改 api/tests/prompts/CI

【回填】
- task §实现备忘：涉及文件列表
- task §自检结论：命令/结果/要点

【commit】
git add → commit → invoke_20260527_40_* 落盘
```

---

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：30 · 执行编码
├── task：task_governance_wiki_t4_expand_v2.md · audit_profile：post_close
├── 分支：task/gov-t4-l2-followup-v1
├── human_gate：HG-TASK-DRAFT approved · HG-AUDIT-R1 approved
├── 本棒交付：2 slug graph_nodes + CODING_WIKI + RECENT + 40 Prompt
├── 下一棒：40 自检
├── 推荐：—
└── 阻塞：无
```
