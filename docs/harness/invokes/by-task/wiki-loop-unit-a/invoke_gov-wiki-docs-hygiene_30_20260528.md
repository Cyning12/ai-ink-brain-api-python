# Invoke · gov-wiki-docs-hygiene · 30 · R1

| 项 | 值 |
| --- | --- |
| **round** | R1 |
| **hat** | 30 |
| **task** | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` |
| **task_slug** | `gov-wiki-docs-hygiene` |
| **freeze_id** | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **semi_auto** | true |
| **previous_hat** | 22（review 已落盘 @ bf15688） |

---

## §3 可复制 Prompt

```text
【角色切换】上一帽 22 已结束；本帽为 30 执行帽，只按下文执行。

执行 Wiki Loop 单元 A · R1 · 30 文档同步。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only · 禁止 api/tests/tools。
task: docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md
task_slug: gov-wiki-docs-hygiene
freeze_id: GOV-WIKI-DOCS-HYGIENE@2026-05-28

**范围（逐项执行，禁止扩大）**

1. `docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`：
   - #36 T4：planned / ❌ P2 → **active+扩面 / ✅**（T4 扩面 3 synthesis graph_nodes 已 done · `task_governance_wiki_t4_expand_v2`）
   - #37 前端 Harness parity：远期 / ⏸ → **done / ✅**（前端 parity 2026-05-27 done · Ink PR #44）
   - §7 P2 Loop 行：母单路径 `active/task_harness_wiki_loop_p2_followup_v1.md` → `done/task_harness_wiki_loop_p2_followup_v1.md`；状态 done
   - §7 前端 parity 行：状态更新为 done（如未写）
   - §7 T4 expand 行：确认状态 done（如未写）
   - 版本号：v1.0 → v1.4
   - 修订记录追加：2026-05-28 | v1.4：#36 T4 active+扩面 · #37 P1-4 done · §7 P2/前端同步

2. `docs/spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`：
   - Loop 母单链接：`../../tasks/active/task_harness_wiki_loop_p2_followup_v1.md` → `../../tasks/done/task_harness_wiki_loop_p2_followup_v1.md`
   - 若 SPEC 仍为 active 且内容已全完成，状态可更新（optional）

3. `docs/tasks/RECENT_TASK_SCHEDULE.md` §6.6：
   - 在表格末尾（或更新现有 draft 行）追加/更新：
     - Wiki Loop Unit A：in_progress · 分支 task/wiki-unit-ab-plan-v1 · PR-A · cc
     - L2 Phase C impl：pending · 单元 B · PR-B · required
   - 如已有 draft 行，将 draft 替换为正式内容
   - 更新 §6.6 标题日期至 2026-05-28（若未写）

4.（可选）`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` §5.2：
   - 如未链出 SPEC-Governance-Wiki-Unit-AB-Plan-v1.md，追加 pointer

**执行纪律**
- 每文件改后自核链接有效性（相对路径）
- 不改 synthesis 正文、不改 api/tests/tools
- 40 自检：逐条对照 task 验收标准
- invoke C2：30/40/50 每帽 §3 ≥15 行
- 每帽 commit 后再戴下一帽（HANDOFF_AUTO_COMMIT）
```
