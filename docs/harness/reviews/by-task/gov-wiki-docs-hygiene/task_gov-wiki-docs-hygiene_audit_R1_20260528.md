# 22 任务审核 — gov-wiki-docs-hygiene · R1

| 项 | 值 |
| --- | --- |
| **task** | `docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md` |
| **task_slug** | `gov-wiki-docs-hygiene` |
| **freeze_id** | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **round** | R1 |
| **audit_profile** | post_close |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **human_gate** | HG-LOOP-BATCH approved（母单 `task_harness_wiki_loop_unit_a_v1.md`） |
| **review_date** | 2026-05-28 |

---

## 审查结论摘要

**零阻塞 · 可进入 30 执行帽**

本 task 为 docs-only hygiene，范围明确（对比表同步 + P2 SPEC 路径更新 + RECENT 增行），不涉及 `api/tests/tools`。`test_strategy: not_applicable` 合理。

---

## 已核对项

| # | 检查项 | 结论 | 说明 |
| --- | --- | --- | --- |
| 1 | human_gate | pass | 母单 `HG-LOOP-BATCH` = approved；`harness_human_gate_check.py --task` exit 0 |
| 2 | 范围 vs 非范围 | pass | 仅改 `docs/coding_wiki/`、`docs/spec/governance/`、`docs/tasks/RECENT_TASK_SCHEDULE.md`；禁止项未触及 |
| 3 | 关联文件存在性 | pass | `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`、`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`、`RECENT_TASK_SCHEDULE.md`、`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md` 均存在 |
| 4 | 前置 done 状态 | pass | `task_harness_wiki_loop_p2_followup_v1.md` 已 `done/`；T4 扩面（`task_governance_wiki_t4_expand_v2`）、P1-4 前端 parity 已 done |
| 5 | failure_paths | pass | F1（对比表矛盾）当前无证据；F2（Batch-3 改名单）不属 R1 |
| 6 | freeze_id 一致性 | pass | 子 task `GOV-WIKI-DOCS-HYGIENE@2026-05-28` 与母单 `WIKI-LOOP-UNIT-A@2026-05-28` 区分正确 |

---

## 阻塞 / 非阻塞

**非阻塞**。无 pending human_gate，无范围越界，无文件缺失。

---

## 签收 / 关闭

**结论：可执行**

R1 为 hygiene 同步任务，改动类型为「状态/路径指针更新」，风险 Low。建议 30 执行时逐项对照 §7 表与 done/ 目录，避免状态漂移。

---

## 下一棒可复制 Prompt

```text
执行 Wiki Loop 单元 A · R1 · 30→40→50→关账。
分支 task/wiki-unit-ab-plan-v1 · PR-A docs-only · 禁止 api/tests/tools。

task: docs/tasks/active/task_governance_wiki_docs_hygiene_v1.md
task_slug: gov-wiki-docs-hygiene
freeze_id: GOV-WIKI-DOCS-HYGIENE@2026-05-28
semi_auto: true

**范围（逐项执行）**
1. `docs/coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`：
   - #36 T4：planned/❌ → active+扩面/✅（T4 扩面 3 synthesis graph_nodes 已 done）
   - #37 P1-4：远期/⏸ → done/✅（前端 parity 2026-05-27 done）
   - §7 P2 Loop 行：更新母单路径 `active/` → `done/`；状态 done
   - §7 前端 parity 行：更新状态 done
   - §7 T4 行：如有需要同步扩面信息
   - 版本号 v1.0 → v1.4（按修订记录日期）
   - 修订记录追加 2026-05-28 条目

2. `docs/spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`：
   - Loop 母单链接 `../../tasks/active/task_harness_wiki_loop_p2_followup_v1.md` → `../../tasks/done/task_harness_wiki_loop_p2_followup_v1.md`
   - 若 SPEC 状态仍为 active 且内容已全完成，可更新状态

3. `docs/tasks/RECENT_TASK_SCHEDULE.md` §6.6：
   - 在表格末尾追加两行（或更新现有 draft 行）：
     - Wiki Loop Unit A：in_progress · 分支 task/wiki-unit-ab-plan-v1 · PR-A
     - L2 Phase C impl：pending · 单元 B · PR-B · required
   - 更新日期至 2026-05-28

4.（可选）`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` §5.2：
   - 如未链出 Unit AB SPEC，追加 pointer

**执行纪律**
- 每文件改后自核链接有效性
- 不扩大范围（不改 synthesis 正文、不改 api/tests/tools）
- 40 自检：逐条对照 task 验收标准
- invoke C2：每帽 §3 ≥15 行，元信息完整
- 每帽 commit 后再戴下一帽（HANDOFF_AUTO_COMMIT）
```
