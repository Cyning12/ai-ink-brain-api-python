# 新 Agent 入口 · 单 task 全链（22→关账 · 仅粘贴一次）

> **用途**：**gov-l2-manifest-ci**（L2 `_test_manifest` Phase B）完整帽链 · **前置** T4 扩面已 merge（PR #69 · `GOV-T4-EXPAND@2026-05-27`）。  
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
git checkout -b task/gov-l2-manifest-ci-v1 origin/main   # 从已含 T4 关账的 main 拉出
git branch --show-current   # 须 task/gov-l2-manifest-ci-v1

grep 'HG-TASK-DRAFT.*approved' docs/tasks/active/task_governance_l2_manifest_ci_v1.md
grep 'HG-AUDIT-R1.*approved' docs/tasks/active/task_governance_l2_manifest_ci_v1.md
grep 'HG-CI-WORKFLOW.*approved' docs/tasks/active/task_governance_l2_manifest_ci_v1.md

test -f docs/_tech_graph/_test_manifest.json
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m['entries'])==6"
test -f docs/harness/invokes/by-task/gov-l2-manifest-ci/PROMPT_TASK_22_to_CLOSE_v1.md
test -f tools/tech_graph_manifest_check.py
! test -f tools/tech_graph_test_manifest_check.py   # 预期尚未存在 · 30 帽新建
```

---

## 2. semi_auto（单 task · 含 tools/tests/workflow）

```text
22→30→40→50→关账 同会话连续；每帽 invoke §3 ≥15 行 + commit。
test_strategy: recommended · 50 须独立 reinspect + 附 pytest / 脚本 exit 0 证据。

【禁止跳帽 · 硬】
- 未落盘当前帽 invoke + commit → 禁止进入下一帽（即使业务已写完）
- 关账前须逐项勾选 SKILL-harness-task §ST1–ST6（见下）

【关账前自检 ST1–ST6】（关账 commit 前在 invoke 或对话中勾选）
- [ ] ST1 22 review + invoke_22
- [ ] ST2 invoke_30（含 tools/tests/workflow/99_spec/manifest 扩面 commit）
- [ ] ST3 invoke_40 + task §自检结论已回填
- [ ] ST4 reinspect + invoke_50
- [ ] ST5 done 头部 + git mv + _views + CLOSE invoke
- [ ] ST6 RECENT §6.6 L2 Phase B 行 → done + §8 修订 · hygiene H1–H5
```

---

## 3. 可复制 Prompt（全文复制到 Claude Code / 新 Cursor 对话）

```text
你正在 ai-ink-brain-api-python 执行 **单 task** gov-l2-manifest-ci 帽链：**22 → 30 → 40 → 50 → 关账**（**跳过 10**）。

【必读 · 显式打开路径 · 非 Cursor 无 .mdc 自动加载】
- docs/tasks/active/task_governance_l2_manifest_ci_v1.md
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md（§4.1.1 · §4.3 Phase B）
- docs/tasks/skills/SKILL-harness-task.md
- docs/tasks/skills/SKILL-docs-governance.md
- docs/harness/prompts/hats/22-task-audit.md
- docs/harness/prompts/hats/30-execute-code.md
- docs/harness/prompts/hats/40-self-check.md
- docs/harness/prompts/hats/50-independent-reinspect.md
- docs/harness/prompts/handoff/HANDOFF_SEMI_AUTO.md
- docs/harness/prompts/handoff/HANDOFF_AUTO_COMMIT.md
- docs/harness/prompts/handoff/HANDOFF_CLOSE_TRACE.md
- docs/harness/invokes/by-task/gov-l2-manifest-ci/PROMPT_TASK_22_to_CLOSE_v1.md §3
- 参照脚本：tools/tech_graph_manifest_check.py（结构/CLI 风格）
- 现有 manifest：docs/_tech_graph/_test_manifest.json（6 entries · Phase A）
- CI 真值：.github/workflows/tech-graph.yml（manifest_check job）

【元信息】
- task_slug: gov-l2-manifest-ci
- task: docs/tasks/active/task_governance_l2_manifest_ci_v1.md
- freeze_id: GOV-L2-MANIFEST-CI@2026-05-27
- git_branch: task/gov-l2-manifest-ci-v1
- semi_auto: true
- test_strategy: recommended
- audit_profile: post_close
- invoke 目录: docs/harness/invokes/by-task/gov-l2-manifest-ci/
- review 目录: docs/harness/reviews/by-task/gov-l2-manifest-ci/
- human_gate: HG-TASK-DRAFT · HG-AUDIT-R1 · HG-CI-WORKFLOW 均已 approved

【semi_auto】同会话连续 22→关账；每帽 invoke + commit 后再换帽。

【invoke 质量 · 硬】
- 各 invoke §3 ≥15 行；元信息表含 task_slug、freeze_id、git_branch
- 禁止仅写「交付摘要 + commit」式 stub

【commit 硬纪律】每帽结束 before 下一帽：git add → commit → 回复「已提交：<short-hash>」

【22 帽】
- R1 audit 落盘 docs/harness/reviews/by-task/gov-l2-manifest-ci/
- 审 manifest 扩面方案（6→≥12）、脚本行为、workflow step、非范围边界
- invoke_YYYYMMDD_22_gov-l2-manifest-ci-v1.md · commit

【30 帽交付摘要】
1. docs/_tech_graph/_test_manifest.json：在现有 6 条上增量至 **≥12 entries**（id 稳定 · Epic 前缀 · test_paths 仅 `tests/` 下 fnmatch glob）
2. 新增 tools/tech_graph_test_manifest_check.py：
   - JSON schema / 必填字段校验
   - 每条 test_paths：fnmatch 在仓库根至少匹配一个 tests/**/*.py
   - 可选 --strict：error_codes 须在 api/ 有字符串出现
3. 新增 tests/test_tech_graph_test_manifest_check.py（≥3 cases：合法 manifest、坏 glob、缺字段）
4. .github/workflows/tech-graph.yml：manifest_check job 增 step 跑新脚本（Required · 已 HG-CI-WORKFLOW approved）
5. docs/_tech_graph/99_spec.md：测试 manifest 小节补脚本与 VERIFY
6. task §实现备忘回填涉及文件列表
- invoke_30 · commit

【40 帽】
- 跑 task §VERIFY 全部命令；回填 task §自检结论
- invoke_40 · commit

【50 + 关账】
- 独立 reinspect：docs/tasks/reinspect_results/reinspect_gov-l2-manifest-ci_YYYYMMDD_v1.md
- 对照 git diff、pytest 输出、workflow step 是否存在
- invoke_50 · commit
- 验收项 `- [x]` · 头部 done（日期 · freeze_id）
- git mv → docs/tasks/done/task_governance_l2_manifest_ci_v1.md（与 done 头部同 commit）
- docs/tasks/_views/done.md 一行
- RECENT §6.6 L2 Phase B 行标 done + §8 修订
- docs-governance hygiene H1–H5
- invoke_CLOSE + HANDOFF_CLOSE_TRACE

【合并前 VERIFY · 40/50 须附证据】
python tools/tech_graph_test_manifest_check.py
pytest tests/test_tech_graph_test_manifest_check.py -q
pytest tests -m "not intent_eval and not intent_benchmark" -q
python tools/tech_graph_manifest_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
python -c "import json; m=json.load(open('docs/_tech_graph/_test_manifest.json')); assert len(m['entries'])>=12"

【硬约束 · 非范围】
- 不改 api/ 业务逻辑（脚本只读扫描 error_codes 字符串）
- 不改既有 tests/ 业务用例（仅允许新增 manifest check 测试文件）
- 不改 Harness prompts 正文
- 不手改 graph.json · Phase C failure_paths 双向校验不在本 task
- workflow 变更已 HG-CI-WORKFLOW approved

现在开始：确认分支 task/gov-l2-manifest-ci-v1（从 origin/main 拉出），执行 **22 帽**（review + invoke_YYYYMMDD_22_*）。
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：L2 Phase B 单 task 全链 · Claude Code |
| 2026-05-27 | v1.1：T4 已 merge · ST1–ST6 · 禁止跳帽 · 22/30/40/50 逐步交付 · VERIFY 全表 |
