---
title: L2 _test_manifest Phase B（CI 校验）
slug: governance-l2-manifest-ci
layer: L2
source_task: docs/tasks/done/task_governance_l2_manifest_ci_v1.md
freeze_id: GOV-L2-MANIFEST-CI@2026-05-27
closed_date: 2026-05-27
status: compiled
test_strategy: recommended
---

# L2 _test_manifest Phase B

## 摘要

Loop R3 Phase A（6 entries 草案）之后，将 `_test_manifest.json` **扩面至 ≥12** 条 ERR↔测试映射，新增 `tools/tech_graph_test_manifest_check.py`（schema + glob + 可选 `--strict`），接入 `tech-graph.yml` Required step，并更新 `99_spec.md` VERIFY。

## 决策与验收要点

- Phase B **机器校验**与 Wiki §8 **叙事存档**分工：manifest 负责 exit 0 门禁，Wiki 解释「为何这样测」。  
- 首版与 `manifest_check` **同 job** Required。  
- 非范围：不改 `api/` 业务逻辑 · 不手改 `graph.json`。

## §测试变更

| 动作 | 说明 |
|------|------|
| 新增 | `tests/test_tech_graph_test_manifest_check.py`（≥3 cases） |
| CI | `tech-graph.yml` 增 test manifest check step |
| L1 | `test_strategy: recommended` — 关账前全仓 pytest 仍须绿 |

## 指针（L1）

→ `docs/tasks/done/task_governance_l2_manifest_ci_v1.md`  
→ `docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.3  
→ `docs/_tech_graph/_test_manifest.json`
