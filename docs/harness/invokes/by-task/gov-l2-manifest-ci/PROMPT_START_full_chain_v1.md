# 新 Agent 入口 · 单 task 全链（22→关账 · 仅粘贴一次）

> **用途**：**gov-l2-manifest-ci** 完整帽链 · **建议** Task A（T4 扩面）关账后再开。  
> **性质**：**单 task**（`SKILL-harness-task`）· **非** Loop Batch。  
> **分支（硬）**：`task/gov-l2-manifest-ci-v1` · Open **`ai-ink-brain-api-python/`**

| 项 | 值 |
|----|-----|
| **task** | `docs/tasks/active/task_governance_l2_manifest_ci_v1.md` |
| **task_slug** | `gov-l2-manifest-ci` |
| **freeze_id** | `GOV-L2-MANIFEST-CI@2026-05-27` |
| **SPEC** | `docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.3 Phase B |
| **帽链真值** | [`PROMPT_TASK_22_to_CLOSE_v1.md`](./PROMPT_TASK_22_to_CLOSE_v1.md) §3 |
| **SKILL** | [`SKILL-harness-task.md`](../../../tasks/skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../../../tasks/skills/SKILL-docs-governance.md) |

---

## 1. 执行前自检

```bash
git fetch origin main
git checkout -b task/gov-l2-manifest-ci-v1 origin/main   # 若 A 已 merge，从 main 拉
git branch --show-current   # 须 task/gov-l2-manifest-ci-v1

grep 'HG-TASK-DRAFT.*approved' docs/tasks/active/task_governance_l2_manifest_ci_v1.md
grep 'HG-AUDIT-R1.*approved' docs/tasks/active/task_governance_l2_manifest_ci_v1.md
grep 'HG-CI-WORKFLOW.*approved' docs/tasks/active/task_governance_l2_manifest_ci_v1.md

test -f docs/_tech_graph/_test_manifest.json
test -f docs/harness/invokes/by-task/gov-l2-manifest-ci/PROMPT_TASK_22_to_CLOSE_v1.md
```

---

## 2. semi_auto（单 task）

```text
22→30→40→50→关账 同会话连续；每帽 invoke §3 ≥15 行 + commit。
本 task 含 tools/tests/workflow：test_strategy recommended · 50 须重跑 pytest。
```

---

## 3. 可复制 Prompt（全文复制到 Claude Code / 新对话）

```text
你正在 ai-ink-brain-api-python 执行 **单 task** gov-l2-manifest-ci 帽链：**22 → 30 → 40 → 50 → 关账**（**跳过 10**）。

【必读 · 显式打开路径】
- docs/tasks/active/task_governance_l2_manifest_ci_v1.md
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md（§4.3 Phase B）
- docs/tasks/skills/SKILL-harness-task.md
- docs/tasks/skills/SKILL-docs-governance.md
- docs/harness/prompts/hats/22-task-audit.md … 50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md、HANDOFF_CLOSE_TRACE.md
- docs/harness/invokes/by-task/gov-l2-manifest-ci/PROMPT_TASK_22_to_CLOSE_v1.md §3
- 参照：tools/tech_graph_manifest_check.py

【元信息】
- task_slug: gov-l2-manifest-ci
- task: docs/tasks/active/task_governance_l2_manifest_ci_v1.md
- freeze_id: GOV-L2-MANIFEST-CI@2026-05-27
- git_branch: task/gov-l2-manifest-ci-v1
- semi_auto: true
- test_strategy: recommended
- invoke 目录: docs/harness/invokes/by-task/gov-l2-manifest-ci/
- human_gate: HG-TASK-DRAFT · HG-AUDIT-R1 · HG-CI-WORKFLOW 均已 approved

【semi_auto】同会话 22→关账；每帽 invoke + commit。

【invoke 质量 · 硬】§3 ≥15 行 · 元信息含 task_slug · 非 stub

【30 帽交付】
- docs/_tech_graph/_test_manifest.json 扩至 ≥12 entries
- 新增 tools/tech_graph_test_manifest_check.py（fnmatch test_paths · JSON 校验 · 可选 --strict error_codes）
- 新增 tests/test_tech_graph_test_manifest_check.py（≥3 cases）
- .github/workflows/tech-graph.yml manifest_check job 增 step
- docs/_tech_graph/99_spec.md 补脚本与 VERIFY
- RECENT §6.6 L2 Phase B + §8

【50 + 关账】
- 重跑：python tools/tech_graph_test_manifest_check.py
- pytest tests/test_tech_graph_test_manifest_check.py -q
- pytest tests -m "not intent_eval and not intent_benchmark" -q
- manifest_check · contract_check · graph_export --check
- reinspect_gov-l2-manifest-ci_YYYYMMDD_v1.md
- git mv → done/ + _views + hygiene H1–H5 + CLOSE_TRACE

硬约束：不改 api/ 业务逻辑 · 不改 Harness prompts 正文 · workflow 变更已 HG-CI-WORKFLOW approved

现在开始：分支 task/gov-l2-manifest-ci-v1，执行 **22 帽**。
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：L2 Phase B 单 task 全链 · Claude Code |
