# Invoke · 50 独立复检 · R3 · gov-l2-r3-test-manifest

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | round | R3 |
> | hat | 50 |
> | task | `docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md` |
> | task_slug | gov-l2-r3-test-manifest |
> | freeze_id | GOV-L2-R3-TEST-MANIFEST@2026-05-27 |
> | git_branch | task/gov-spec-t4-l2-v1 |

---

## §1 角色与纪律

- 本帽为 **50 独立复检**（`docs/harness/prompts/hats/50-independent-reinspect.md`）。
- 上一帽 40 已结束；本帽独立重跑 VERIFY、逐条 pass/fail。

## §2 复检摘要

**建议合并。无阻塞项。**

### 2.1 独立 VERIFY 重跑

| 命令 | 结果 | 输出摘要 |
|------|------|----------|
| `test -f docs/_tech_graph/_test_manifest.json` | pass | exit 0 |
| `python -c "assert len(entries)>=5"` | pass | 6 entries |
| `manifest_check` | pass | exit 0 |
| `graph_export --check` | pass | exit 0 |

### 2.2 验收表

10 项全部 pass（详见 `docs/tasks/reinspect_results/reinspect_gov-l2-r3-test-manifest_20260527_v1.md`）。

## §3 关账（无下一棒）

50 建议合并且无返工。按 `HANDOFF_CLOSE_TRACE.md` 输出执行路线与 Commit 回溯。

### 3.1 执行路线表

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | 22 任务审核 | review + invoke 落盘 | `reviews/by-task/wiki-loop-t4-l2/*` | api-python@52ac63d |
| 2 | 30 执行编码 | _test_manifest.json + 4 文件修改 | 5 文件 | api-python@b3c7770 |
| 3 | 30 invoke | invoke 落盘 + 40 Prompt | `invoke_20260527_30_*` | api-python@23e01c6 |
| 4 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | api-python@80397da |
| 5 | 50 独立复检 | 重跑 VERIFY + 复检报告 + CLOSE_TRACE | `reinspec_*_20260527_v1.md` + `invoke_20260527_50_*` | 本 commit |
| 6 | **关账** | git mv → done/ + _views 更新 | `done/task_*` + `_views/done.md` | 下一 commit |

### 3.2 分仓 Commit 索引

```text
### api-python（ai-ink-brain-api-python）
- （当前）docs(harness): 50 R3 独立复检 + CLOSE_TRACE（本 commit）
- 80397da docs(harness): 40 R3 自检 + task 回填 + 50 下一棒 Prompt
- 23e01c6 docs(harness): 30 R3 执行编码 invoke + 40 下一棒 Prompt
- b3c7770 docs(governance): R3 L2 manifest 交付 — _test_manifest.json + 99_spec + CODING_WIKI + RECENT
- 52ac63d docs(harness): 22 R3 任务审核落盘 + invoke
```

## §4 关账动作（须执行）

1. `git mv docs/tasks/active/task_governance_l2_r3_test_manifest_v1.md docs/tasks/done/`
2. 更新 `docs/tasks/_views/done.md` 增索引行
3. 提交关账 commit
4. 输出 Harness 状态栏

## §5 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：50 · 独立复检
├── task：task_governance_l2_r3_test_manifest_v1.md · audit_profile：post_close
├── 分支：task/gov-spec-t4-l2-v1
├── human_gate：HG-LOOP-BATCH approved
├── 本棒交付：10 项全 pass + 复检报告落盘 + CLOSE_TRACE
├── 下一棒：关账（git mv → done/ + _views）
├── 推荐：—
└── 阻塞：无
```
