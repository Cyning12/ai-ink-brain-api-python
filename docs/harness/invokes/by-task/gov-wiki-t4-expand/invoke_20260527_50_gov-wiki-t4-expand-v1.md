# Invoke · 50 独立复检 · gov-wiki-t4-expand

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 50 |
> | task | `docs/tasks/active/task_governance_wiki_t4_expand_v2.md` |
> | task_slug | gov-wiki-t4-expand |
> | freeze_id | GOV-T4-EXPAND@2026-05-27 |
> | git_branch | task/gov-t4-l2-followup-v1 |

---

## §1 角色与纪律

- 本帽为 **50 独立复检**（`docs/harness/prompts/hats/50-independent-reinspect.md`）。
- 上一帽 40 已结束；本帽独立重跑 VERIFY、逐条 pass/fail。

## §2 复检摘要

**建议合并。无阻塞项。**

### 2.1 独立 VERIFY 重跑

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `rg -l '^graph_nodes:' docs/coding_wiki/syntheses/ \| wc -l` | pass | 3 files |
| `graph_query neighbors T2S` | pass | exit 0 |
| `graph_query neighbors SSE` | pass | exit 0 |
| `graph_query neighbors U2` | pass | exit 0 |
| `graph_query neighbors CR1` | pass | exit 0 |
| `graph_query neighbors E2E_DOC` | pass | exit 0 |
| `manifest_check` | pass | exit 0 |
| `graph_export --check` | pass | exit 0 |

### 2.2 验收表

10 项全部 pass（详见 `docs/tasks/reinspect_results/reinspect_gov-wiki-t4-expand_20260527_v1.md`）。

## §3 关账（无下一棒）

50 建议合并且无返工。按 `HANDOFF_CLOSE_TRACE.md` 输出执行路线与 Commit 回溯。

### 3.1 执行路线表

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 30 执行编码 | graph_nodes 扩面 2 slug + CODING_WIKI + RECENT | 4 文件 | api-python@baf86bc |
| 2 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | api-python@4c4e73a |
| 3 | 50 独立复检 | 重跑 VERIFY + 复检报告 + CLOSE_TRACE | `reinspect_*_20260527_v1.md` + `invoke_20260527_50_*` | 本 commit |
| 4 | **关账** | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | 下一 commit |

### 3.2 分仓 Commit 索引

```text
### api-python（ai-ink-brain-api-python）
- （当前）docs(harness): 50 独立复检 + CLOSE_TRACE（本 commit）
- 4c4e73a docs(harness): 40 自检 + task 回填 + 50 下一棒 Prompt
- baf86bc docs(governance): 30 graph_nodes 扩面 2 slug + CODING_WIKI + RECENT
```

## §4 关账动作（须执行）

1. `git mv docs/tasks/active/task_governance_wiki_t4_expand_v2.md docs/tasks/done/`
2. 更新 `docs/tasks/_views/done.md` 增索引行
3. 提交关账 commit
4. 输出 Harness 状态栏

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：50 · 独立复检
├── task：task_governance_wiki_t4_expand_v2.md · audit_profile：post_close
├── 分支：task/gov-t4-l2-followup-v1
├── human_gate：HG-TASK-DRAFT approved · HG-AUDIT-R1 approved
├── 本棒交付：10 项全 pass + 复检报告落盘 + CLOSE_TRACE
├── 下一棒：关账（git mv → done/ + _views）
├── 推荐：—
└── 阻塞：无
```
