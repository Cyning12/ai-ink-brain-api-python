# 单元 B · L2 Phase C 实现全链（cc · PR-B）

> **前置**：**PR-A**（单元 A）已合 `main`；`git checkout task/wiki-unit-ab-plan-v1 && git pull origin main`  
> **分支**：`task/wiki-unit-ab-plan-v1`（**不换分支**）

| 项 | 值 |
|----|-----|
| **task** | `docs/tasks/active/task_governance_l2_phase_c_impl_v1.md` |
| **SPEC** | `docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md` §4.4 |
| **test_strategy** | `required` → **须 50** |

---

## 可复制 Prompt（cc）

```text
执行 task_governance_l2_phase_c_impl_v1（单元 B · PR-B）。
分支 task/wiki-unit-ab-plan-v1；test_strategy required；须 22→30→40→50→关账。

必读 @：
- docs/tasks/skills/SKILL-harness-task.md
- docs/spec/governance/SPEC-Governance-L2-Anchor-Test-Manifest-v1.md §4.4
- docs/spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md §3
- docs/harness/prompts/hats/22-task-audit.md … 50-independent-reinspect.md
- HANDOFF_SEMI_AUTO.md、HANDOFF_AUTO_COMMIT.md

禁止：改 docs/coding_wiki/ 批量 ingest；与 PR-A 混单 PR。
VERIFY：tech_graph_test_manifest_check（含双向模式）+ pytest（AGENTS.md 合并前命令）。

关账后建议 skill_cross_platform_v1 case：gov-l2-phase-c-impl_claude-code_<date>。
```
