# Invoke · CLOSE · gov-l2-manifest-ci

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | CLOSE |
> | task | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` |
> | task_slug | gov-l2-manifest-ci |
> | freeze_id | GOV-L2-MANIFEST-CI@2026-05-27 |
> | git_branch | task/gov-l2-manifest-ci-v1 |
> | note | 单 task · 无 round |

---

## §1 执行路线与 Commit 回溯

| 帽 | commit | 摘要 |
|----|--------|------|
| 22 | `13d58d7` | 任务审核 R1 · review + invoke 落盘 |
| 30 | `6fbc862` | manifest ≥12 + test_manifest_check + workflow + pytest + spec |
| 40 | `0084299` | 自检 VERIFY 7/7 全绿 |
| 50 | `40f6b28` | 独立复检 7/7 pass · 建议合并 |
| 关账 | （本 commit）| git mv → done/ + _views + CLOSE invoke |

---

## §2 关账检查清单（H1–H5）

| # | 项 | 结果 |
|---|----|------|
| H1 | `git mv` active/ → done/ | ✅ |
| H2 | `_views/done.md` 索引新增 | ✅ |
| H3 | CLOSE invoke 落盘 | ✅ |
| H4 | RECENT §8 修订 | ✅（30 commit 中已完成） |
| H5 | hygiene：无意外文件残留 | ✅（未改 api/ 业务逻辑 / 未手改 graph.json） |

---

## §3 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：CLOSE
├── task：task_governance_l2_manifest_ci_v1.md · audit_profile：post_close
├── 分支：task/gov-l2-manifest-ci-v1
├── human_gate：HG-TASK-DRAFT approved · HG-AUDIT-R1 approved · HG-CI-WORKFLOW approved
├── 本棒交付：关账（git mv + _views + CLOSE invoke + H1–H5）
├── 下一棒：无（单 task 闭环）
├── 推荐：创建 PR 合并入 main
└── 阻塞：无
```

---

## §4 给下一棒 / PR  reviewer

- 合并前请确认 CI `manifest_check` job 含「Tech Graph test manifest check」step 且 pass。
- 合并后可选：将 `task/gov-l2-manifest-ci-v1` 分支删除。
