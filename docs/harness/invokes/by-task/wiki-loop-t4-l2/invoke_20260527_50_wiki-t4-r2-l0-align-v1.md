# Invoke · 50 独立复检 · R2 · wiki-t4-r2-l0-align

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R2 |
> | hat | 50 |
> | task | `docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md` |
> | task_slug | `wiki-t4-r2-l0-align` |
> | freeze_id | `GOV-T4-R2-L0-ALIGN@2026-05-27` |
> | git_branch | `task/gov-spec-t4-l2-v1` |

---

## §1 角色与纪律

- 本帽为 **50 独立复检**（`docs/harness/prompts/hats/50-independent-reinspect.md`）。
- 上一帽 40 已结束；本帽独立重跑 VERIFY、逐条 pass/fail。

## §2 复检摘要

**建议合并。无阻塞项。**

### 2.1 独立 VERIFY 重跑

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `rg 'Wiki ↔ 图谱桥接' 99_spec.md` | pass | line 42, exit 0 |
| `manifest_check` | pass | exit 0 |
| `drift_check` | **fail** | exit 1（已知历史债务） |
| `contract_check` | pass | exit 0 |
| `graph_export --check` | pass | exit 0 |
| `graph_query neighbors C1/RAG/RAG_DOC/FTS` | pass | 4/4 exit 0 |

### 2.2 drift 债务确认

独立比对 drift_check 输出与历史 task：
- `/api/py/live`, `/api/py/ready` → `task_chatbi_v3_p2_resilience_health_ready_v1.md` (P2-1a, 2026-05-25)
- `chatbi_access_tokens` → `task_chatbi_v3_planning_after_rbac_v1.md` (P1-3, 2026-05-13)
- `SUPABASE_HTTP_RETRIES` 等 → P2-1a
- `TEXT2SQL_DISTINCT_*` → P0 Text2SQL

全部 **非 R2 引入**。

### 2.3 验收表

8 项通过 7 项；drift_check 为已知债务标注。详见 `docs/tasks/reinspect_results/reinspect_wiki-t4-r2-l0-align_20260527_v1.md`。

## §3 关账（无下一棒）

50 建议合并且无返工。按 `HANDOFF_CLOSE_TRACE.md` 输出执行路线与 Commit 回溯。

### 3.1 执行路线表

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/wiki-loop-t4-l2/*` | api-python@2f6431e |
| 2 | 30 执行编码 | VERIFY 全量重跑 + drift 记录 | `invoke_20260527_30_*` | api-python@e34aa6b |
| 3 | 40 自检 | VERIFY 5/6 pass + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | api-python@769b65e |
| 4 | 50 独立复检 | 重跑 VERIFY + 复检报告 + CLOSE_TRACE | `reinspect_*_20260527_v1.md` + `invoke_20260527_50_*` | 本 commit |
| 5 | **关账** | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | 下一 commit |

### 3.2 分仓 Commit 索引

```text
### api-python（ai-ink-brain-api-python）
- （当前）docs(harness): 50 R2 独立复检 + CLOSE_TRACE（本 commit）
- 769b65e docs(harness): 40 R2 自检 + task 回填 + 50 下一棒 Prompt
- e34aa6b docs(harness): 30 R2 执行编码 invoke + 40 下一棒 Prompt
- 2f6431e docs(harness): 22 R2 任务审核落盘 + invoke
- （R1 链）e833d07 docs(task): R1 关账 — wiki-t4-r1-pilot → done/ + _views 更新
```

## §4 关账动作（须执行）

1. `git mv docs/tasks/active/task_governance_wiki_t4_r2_l0_align_v1.md docs/tasks/done/`
2. 更新 `docs/tasks/_views/done.md` 增索引行
3. 提交关账 commit
4. 输出 Harness 状态栏

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：50 · 独立复检
├── task：task_governance_wiki_t4_r2_l0_align_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：8 项复检 + 报告落盘 + CLOSE_TRACE
├── 下一棒：关账（git mv → done/ + _views）
├── 推荐：—
└── 阻塞：无
```
