# Invoke · 50 独立复检 · R1 · wiki-t4-r1-pilot

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R1 |
> | hat | 50 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md` |
> | task_slug | `wiki-t4-r1-pilot` |
> | freeze_id | `GOV-T4-R1-PILOT@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |

---

## §1 角色与纪律

- 本帽为 **50 独立复检**（`docs/harness/prompts/hats/50-independent-reinspect.md`）。
- 上一帽 40 已结束；本帽独立重跑 VERIFY、逐条 pass/fail。
- 不引用 40 结论为证据；以本帽重跑命令输出为准。

## §2 复检摘要

**建议合并。无阻塞项。**

### 2.1 独立 VERIFY 重跑

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `rg '^graph_nodes:' query-rewrite-observability.md` | pass | line 10, exit 0 |
| `rg 'graph_nodes' CODING_WIKI.md` | pass | 5 处, exit 0 |
| `graph_query neighbors C1/RAG/RAG_DOC/FTS` | pass | 4/4 exit 0 |
| `graph_export --check` | pass | exit 0 |

### 2.2 抽检

- graph_nodes 增量 commit：`f2f7505`（本次 R1 30 交付），非旧提交混入。
- `git show f2f7505 -- CODING_WIKI.md | grep -c graph_nodes` = 8 处增量。
- human_gate：`HG-LOOP-BATCH approved` 在母 task；无 Agent 代填记录。

### 2.3 验收表

14 项全部 pass（详见 `docs/tasks/reinspect_results/reinspect_wiki-t4-r1-pilot_20260527_v1.md`）。

## §3 关账（无下一棒）

50 建议合并且无返工。按 `HANDOFF_CLOSE_TRACE.md` 输出执行路线与 Commit 回溯。

### 3.1 执行路线表

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 30 执行编码 | graph_nodes + CODING_WIKI + 99_spec + RECENT | 4 文件修改 | api-python@f2f7505 |
| 2 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/wiki-loop-t4-l2/*` | api-python@b1afaf6 |
| 3 | 30 invoke | invoke 落盘 + 40 Prompt | `invoke_20260527_30_*` | api-python@e4a58d3 |
| 4 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | api-python@915566e |
| 5 | 50 独立复检 | 重跑 VERIFY + 复检报告 + CLOSE_TRACE | `reinspect_*_20260527_v1.md` + `invoke_20260527_50_*` | 本 commit |

### 3.2 分仓 Commit 索引

```text
### api-python（ai-ink-brain-api-python）
- （当前）docs(harness): 50 R1 独立复检 + CLOSE_TRACE（本 commit）
- 915566e docs(harness): 40 R1 自检 + task 回填 + 50 下一棒 Prompt
- e4a58d3 docs(harness): 30 R1 执行编码 invoke + 40 下一棒 Prompt
- f2f7505 docs(governance): R1 T4 Pilot 交付 — graph_nodes + CODING_WIKI + RECENT
- b1afaf6 docs(harness): 22 R1 任务审核落盘 + invoke
```

## §4 关账动作（须执行）

1. `git mv docs/tasks/active/task_governance_wiki_t4_r1_pilot_v1.md docs/tasks/done/`
2. 更新 `docs/tasks/_views/done.md` 增索引行
3. 提交关账 commit
4. 输出 Harness 状态栏

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：50 · 独立复检
├── task：task_governance_wiki_t4_r1_pilot_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：14 项全 pass + 复检报告落盘 + CLOSE_TRACE
├── 下一棒：关账（git mv → done/ + _views）
├── 推荐：—
└── 阻塞：无
```
