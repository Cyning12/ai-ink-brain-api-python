# Invoke · 22 任务审核 · gov-l2-manifest-ci

> **元信息**
> | 字段 | 值 |
> |------|-----|
> | hat | 22 |
> | task | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md` |
> | task_slug | gov-l2-manifest-ci |
> | freeze_id | GOV-L2-MANIFEST-CI@2026-05-27 |
> | git_branch | task/gov-l2-manifest-ci-v1 |
> | note | 单 task · 无 round |

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
| 2 | `HG-AUDIT-R1` = approved | pass（本 review 为 R1 落盘） |
| 3 | `HG-CI-WORKFLOW` = approved | pass（workflow diff 人确认） |
| 4 | task 头部元信息完整 | pass |
| 5 | 范围（扩面 + 脚本 + workflow + pytest + spec）清晰 | pass |
| 6 | 验收标准可执行 | pass |
| 7 | 非范围明确 | pass（不改 api/ / 不手改 graph.json / 不碰 prompts） |
| 8 | test_strategy = recommended | pass（50 必须 · reinspect 落盘） |
| 9 | SPEC §4.3 Phase B 可读 | pass（schema / test_paths 仅 glob / CI 分阶段） |
| 10 | 前置 Phase A 已存在 | pass（_test_manifest.json 6 entries） |
| 11 | 参照脚本已存在 | pass（tools/tech_graph_manifest_check.py） |
| 12 | CI 真值已存在 | pass（.github/workflows/tech-graph.yml） |

### 2.2 阻塞项

无。

## §3 审核落盘

审查文档：`docs/harness/reviews/by-task/gov-l2-manifest-ci/task_governance_l2_manifest_ci_audit_R1_20260527.md`

### 3.1 审查结论摘要

- **结论**：无阻塞 · 可进入 30 执行编码。
- **SPEC 对齐**：L2 §4.3 Phase B — manifest 扩面、脚本 schema/glob、`--strict` 可选、CI 同 job Required。
- **人工闸**：HG-TASK-DRAFT / HG-AUDIT-R1 / HG-CI-WORKFLOW 均已 approved。

### 3.2 关键核对项（12/12 pass）

| 域 | 核对 |
|----|------|
| 范围 | 6→≥12 entries · 新脚本 · pytest · workflow step · 99_spec |
| 非范围 | 不改 api/ 业务 · 不手改 graph.json · 不碰 prompts |
| 前置 | Phase A 6 entries 已存在 · `tech_graph_manifest_check.py` 可参照 |
| 验收 | task §VERIFY 7 条命令可执行 · test_strategy=recommended → 50 必须 |

### 3.3 对应 commit

| 帽 | commit | 摘要 |
|----|--------|------|
| 22 | `13d58d7` | review + invoke_22 落盘 |

---

## §4 执行路线

| 序号 | 阶段 / 帽子 | 关键动作 | 落盘工件 | 对应 commit |
|------|-------------|----------|----------|-------------|
| 1 | **22 任务审核** | review + invoke 落盘 | `reviews/by-task/gov-l2-manifest-ci/*` | 本 commit |
| 2 | 30 执行编码 | manifest 扩面 + 脚本 + workflow + pytest + spec + RECENT | 多文件 | 下一 commit |
| 3 | 40 自检 | VERIFY 全绿 + task 回填 + 50 Prompt | task 自检结论 + `invoke_20260527_40_*` | 后续 commit |
| 4 | 50 独立复检 | 重跑 VERIFY + 复检报告 | `reinspect_*_YYYYMMDD_v1.md` | 后续 commit |
| 5 | 关账 | git mv → done/ + _views 更新 + CLOSE invoke | `done/task_*` + `_views/done.md` | 最终 commit |

---

## §5 下一棒 Prompt

```text
你正在执行 gov-l2-manifest-ci **30 执行编码**。

【必读】
- docs/tasks/done/task_governance_l2_manifest_ci_v1.md
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md §4.3 Phase B
- docs/_tech_graph/_test_manifest.json（现有 6 entries）
- tools/tech_graph_manifest_check.py（参照脚本）
- .github/workflows/tech-graph.yml（CI 真值）

【元信息】
- task_slug: gov-l2-manifest-ci
- freeze_id: GOV-L2-MANIFEST-CI@2026-05-27
- git_branch: task/gov-l2-manifest-ci-v1

【交付】
1. _test_manifest.json：增量至 ≥12 entries（id 稳定 · Epic 前缀 · test_paths 仅 tests/ 下 glob）
2. tools/tech_graph_test_manifest_check.py：
   - JSON schema / 必填字段校验
   - 每条 test_paths：fnmatch 在仓库根至少匹配一个 tests/**/*.py
   - 可选 --strict：error_codes 在 api/ 有字符串出现
3. tests/test_tech_graph_test_manifest_check.py：≥3 cases（合法、坏 glob、缺字段）
4. .github/workflows/tech-graph.yml：manifest_check job 增 step 跑新脚本
5. docs/_tech_graph/99_spec.md：测试 manifest 小节补脚本与 VERIFY
6. RECENT_TASK_SCHEDULE.md：§6.6 L2 Phase B 行 + §8 修订

【commit】
git add → commit（HANDOFF_AUTO_COMMIT）
```

---

## §6 状态栏

```text
📋 Harness 状态栏（版本 B）
├── 当前帽：22 · 任务审核
├── task：task_governance_l2_manifest_ci_v1.md · audit_profile：post_close
├── 分支：task/gov-l2-manifest-ci-v1
├── human_gate：HG-TASK-DRAFT approved · HG-AUDIT-R1 approved · HG-CI-WORKFLOW approved
├── 本棒交付：review 落盘 + invoke 落盘 + 30 Prompt
├── 下一棒：30 执行编码
├── 推荐：—
└── 阻塞：无
```
