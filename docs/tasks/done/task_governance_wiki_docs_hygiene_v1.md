# Task：治理 — Wiki 文档 hygiene（单元 A · R1）

> **状态**：done（2026-05-28）  
> **round**：**R1** · 母单 [`task_harness_wiki_loop_unit_a_v1.md`](task_harness_wiki_loop_unit_a_v1.md)  
> **SPEC**：[`SPEC-Governance-Wiki-Unit-AB-Plan-v1.md`](../spec/governance/SPEC-Governance-Wiki-Unit-AB-Plan-v1.md) §2 R1

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs 指针与对比表同步；不改 pytest。 |
| **freeze_id** | `GOV-WIKI-DOCS-HYGIENE@2026-05-28` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-unit-ab-plan-v1` |
| **task_slug** | `gov-wiki-docs-hygiene` |
| **wiki_delta** | `docs/coding_wiki` |
| **wiki_delta_note** | 存量迁移 · 本 task 触及 docs/coding_wiki（2.18 wiki_delta） |

### 人工闸

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-LOOP-BATCH | pending | 22, 30 | **继承母单** |

---

## 背景与目标

P2 Loop / P1-4 / AB-REP 已关账，但 [`WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`](../../coding_wiki/WIKI_REQUIREMENTS_COMPARISON_v1_zh.md) 与 [`SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`](../spec/governance/SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md) 仍有 **planned/远期/active 路径** 漂移。

**完成态**：对比表 #36 T4、#37 P1-4、§7 表与 **2026-05-27 done** 一致；P2 SPEC 母单链指向 `done/`；RECENT §6.6 增 **单元 A/B** 草案行（in_progress → META 改 done）。

---

## 范围

- [ ] `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md`：#36→✅ T4 active+扩面；#37→✅ P1-4 done；§7 P2 T4/前端行更新  
- [ ] `SPEC-Governance-Wiki-Promotion-Phase-P2-v1.md`：`task_harness_wiki_loop_p2_followup_v1` → `docs/tasks/done/…`  
- [ ] `docs/tasks/RECENT_TASK_SCHEDULE.md` §6.6：增 `Wiki Loop Unit A` / `L2 Phase C impl` 行（状态 in_progress）  
- [ ] （可选）`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md` §5.2 链出本 Unit AB SPEC  
- [ ] 22→30→40→50 · invoke · 关账 → `done/`

## 非范围

- 改 synthesis 正文（属 R2/R3）  
- 改 `api/tests/tools`

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 |
|---|----------|----------|--------|
| F1 | 对比表与 SPEC 结论矛盾 | 22 **阻塞**；列冲突表请人裁决 | 是 |
| F2 | 拟改 Batch-3 slug 名单 | 仅 R3 + 母单 `HG-INGEST-BATCH-3-SCOPE` | — |

---

## 验收标准

- [x] 上表范围勾选完成
- [x] invoke C2 全绿
- [ ] `git mv` → `docs/tasks/done/`

---

### 自检结论（执行者）

| # | 检查项 | 结果 |
| --- | --- | --- |
| 1 | 对比表 #36 T4 active+扩面 | ✅ pass · v1.4 |
| 2 | 对比表 #37 P1-4 done | ✅ pass |
| 3 | 对比表 §7 P2 T4/前端同步 | ✅ pass |
| 4 | P2 SPEC 母单链 `done/` | ✅ pass · 文件存在 |
| 5 | RECENT §6.6 Unit A in_progress | ✅ pass |
| 6 | Roadmap §5.2 A/B 双 PR 行 | ✅ pass |
| 7 | invoke C2（22=2800 B / 30=2747 B） | ✅ pass · §3 ≥15 行 |
| 8 | 无 api/tests/tools 改动 | ✅ pass |

**结论：全部验收项通过 · 零阻塞 · 2026-05-28**

---

## 给 Cursor / Claude Code

`gov-wiki-docs-hygiene`、`GOV-WIKI-DOCS-HYGIENE`、Loop R1
