# 启动 Prompt · 单 task · 22 → 关账（v1 · 无 10）

> **模板** · 全链入口：[`PROMPT_START_full_chain_v1.md`](./PROMPT_START_full_chain_v1.md)  
> **SKILL**：[`SKILL-harness-task.md`](../../../tasks/skills/SKILL-harness-task.md)

---

## 1. 元信息（固定）

| 字段 | 值 |
|------|-----|
| **task** | `docs/tasks/done/task_governance_l2_manifest_ci_v1.md`（**done** · PR #70） |
| **task_slug** | `gov-l2-manifest-ci` |
| **freeze_id** | `GOV-L2-MANIFEST-CI@2026-05-27` |
| **git_branch** | `task/gov-l2-manifest-ci-v1` |
| **invoke 目录** | `docs/harness/invokes/by-task/gov-l2-manifest-ci/` |
| **review 目录** | `docs/harness/reviews/by-task/gov-l2-manifest-ci/` |

---

## 2. 22 开工前

- [ ] 分支 = `task/gov-l2-manifest-ci-v1`
- [ ] `HG-TASK-DRAFT` · `HG-AUDIT-R1` · `HG-CI-WORKFLOW` = **approved**
- [ ] 读 L2 SPEC §4.3 Phase B
- [ ] 读现有 `docs/_tech_graph/_test_manifest.json`（6 entries）

---

## 3. 可复制 Prompt 正文（帽链逐步）

```text
你正在执行单 task **gov-l2-manifest-ci** 帽链：**22 → 30 → 40 → 50 → 关账**（无 10）。

真值：
- docs/tasks/active/task_governance_l2_manifest_ci_v1.md
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md §4.3
- docs/tasks/skills/SKILL-harness-task.md
- docs/tasks/skills/SKILL-docs-governance.md
- docs/harness/prompts/hats/22 … 50
- docs/harness/prompts/handoff/HANDOFF_*

semi_auto: true · test_strategy: recommended · 每帽 invoke + commit

---

### 步骤 1 · 22

review + invoke_22 · commit

### 步骤 2 · 30

- manifest ≥12 entries
- tools/tech_graph_test_manifest_check.py
- tests/test_tech_graph_test_manifest_check.py
- tech-graph.yml step
- 99_spec 更新
invoke_30 · commit

### 步骤 3 · 40

跑 task §VERIFY 全部命令；回填 §自检结论
invoke_40 · commit

### 步骤 4 · 50

独立 reinspect；对照 git diff 与 pytest 输出
invoke_50 · commit

### 步骤 5 · 关账

done 头部 + git mv + _views + hygiene + CLOSE invoke + HANDOFF_CLOSE_TRACE

---

合并前必绿（50 须附证据）：
python tools/tech_graph_test_manifest_check.py
pytest tests/test_tech_graph_test_manifest_check.py -q
pytest tests -m "not intent_eval and not intent_benchmark" -q
python tools/tech_graph_manifest_check.py
python tools/tech_graph_contract_check.py
python tools/tech_graph_graph_export.py --check
```

---

## 4. 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-27 | v1：L2 Phase B 单 task 逐步模板 |
