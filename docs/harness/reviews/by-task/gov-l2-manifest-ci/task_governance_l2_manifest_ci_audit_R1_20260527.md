# Review · gov-l2-manifest-ci · R1 · 2026-05-27

> **task_slug**: gov-l2-manifest-ci
> **freeze_id**: GOV-L2-MANIFEST-CI@2026-05-27
> **task**: `docs/tasks/active/task_governance_l2_manifest_ci_v1.md`
> **SPEC**: `docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.3 Phase B
> **invoke_snapshot**: `docs/harness/invokes/by-task/gov-l2-manifest-ci/invoke_20260527_22_gov-l2-manifest-ci-v1.md`

---

## 审查结论摘要

**结论：可进入执行帽 · 无阻塞。**

本 task 为 L2 `_test_manifest` **Phase B**：在 Loop T4+L2 R3 Phase A（6 entries 草案）基础上扩面至 ≥12 条，实现 `tools/tech_graph_test_manifest_check.py`（JSON schema / glob 匹配 / 可选 --strict），接入 `tech-graph.yml` CI，更新 `99_spec.md`。

### 已核对项

| # | 项 | 结果 | 备注 |
|---|----|------|------|
| 1 | `HG-TASK-DRAFT` | approved | 人批；manifest 扩面条目 + CI 方案已扫 |
| 2 | `HG-AUDIT-R1` | approved | 本 review 为 R1 落盘 |
| 3 | `HG-CI-WORKFLOW` | approved | workflow diff 人确认 |
| 4 | 分支 | `task/gov-l2-manifest-ci-v1` | 从 main 拉出 |
| 5 | task 头部元信息 | 完整 | freeze_id / semi_auto / audit_profile 齐备 |
| 6 | 范围（扩面 + 脚本 + workflow + pytest + spec） | 清晰 | 6 项交付清单 |
| 7 | 验收标准 | 可执行 | 脚本 exit 0 · pytest 绿 · ≥12 entries · CI pass |
| 8 | 非范围 | 明确 | 不改 api/ 业务逻辑 / 不手改 graph.json / 不碰 prompts 正文 |
| 9 | test_strategy | recommended | 50 必须 · reinspect 必须落盘 |
| 10 | SPEC §4.3 Phase B | 可读 | schema / test_paths 仅 glob / CI 演进分阶段 |
| 11 | 前置 Phase A | 已存在 | `_test_manifest.json` 6 entries（Loop R3） |
| 12 | 参照脚本 | 已存在 | `tools/tech_graph_manifest_check.py` 结构可参照 |

### 阻塞项

无。

---

## 需任务帽回填清单（若无阻塞则无）

无阻塞项，无需回填。

---

## 签收 / 关闭

本 task **可进入 30 执行编码帽**。单 task 无 round；22→30→40→50→关账 同会话连续执行。

---

## 下一棒可复制 Prompt

```text
你正在执行 gov-l2-manifest-ci **30 执行编码**。

【必读】
- docs/tasks/active/task_governance_l2_manifest_ci_v1.md
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

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | R1：无阻塞 · 可开工 · HG-CI-WORKFLOW approved |
