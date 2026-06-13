# SUMMARY · post-close hygiene · governance-tasks-done-hygiene

> **状态**：`done`（2026-06-13 关账后卫生修复完成）  
> **母 task**：[`docs/tasks/done/task_governance_tasks_done_index_hygiene_v1.md`](../../../../tasks/done/task_governance_tasks_done_index_hygiene_v1.md)  
> **关联 PR**：#160  
> **freeze_id**：`GOV-TASKS-DONE-HYGIENE@2026-06-13`

---

## 1. 修复项（G1–G7）

| ID | 项 | 结果 | 备注 |
|----|-----|------|------|
| G1 | §3 与关账状态矛盾 | pass | 移除「思考未闭合 → 22 退回 10 · 30 拒开工」；补「本单于 2026-06-13 已关账，以下路径在验收时已完成验证」 |
| G2 | §5 思考轮 | pass | 控制表填 `actual_last_round: R0` / `early_stop: yes` / `residual_risks: none`；R0–R5 极简回填 |
| G3 | §2 C1/C2 | pass | 勾选 C1/C2，与 §8 自检结论一致 |
| G4 | reinspect → done 路径 | pass | `reinspect_..._v1.md` Task 链由 `../active/...` 改 `../done/...` |
| G5 | `coding_wiki/index.md` §维护 | pass | 增 Hub / `done_by_domain` 更新纪律 + `source_task` 仍指向 L1 扁平路径 |
| G6 | invoke README 路径 | pass | Task 真值链由 `../../../tasks/done/...` 修正为 `../../../../tasks/done/...`；同时发现 task 内 `../harness/`、`../spec/` 因 `git mv` 到 `done/` 后层级变化而 broken，已统一改为 `../../harness/`、`../../spec/` |
| G7 | 空域目录 mkdir | pass | 新建 `docs/tasks/done/{harness,governance,chatbi,engineering,standards,epics}/` + `.gitkeep` |

---

## 2. 链接复检

- **命令**：`python3 /tmp/check_links_full.py`
- **扫描文件**：11 个（原 7 个关账文件 + task + reinspect + invoke README + post-close Prompt）
- **结果**：`pass` / zero BROKEN
- **总链接**：384 个；跨仓链接 6 个（`cyning-harness/harness/templates/...`）；其余仓内相对链接全部有效

---

## 3. 与 cyning-harness 模板符合度

| 项 | P0 符合 | 备注 |
|----|---------|------|
| `done/README.md` Hub | 符合 | 六域分组表 + Epic 母单节 |
| `_views/done.md` ≤15 行 | 符合 | 当前 10 行 |
| `done_by_domain.md` | 符合 | 与 Hub 语义一致 |
| FRAGMENT 链入 | 符合 | task / README / CODING_WIKI 三处 |
| Coding Wiki 三文件 | 符合 | 均链 Hub 并写明 L1 vs L2 |
| 物理 `done/<domain>/` | P1 未做 | 已建空目录作为迁移占位，bulk `git mv` 留待子 task |

---

## 4. 与工作区 Harness 试点差异

本仓 P0 采用「逻辑域化（Hub + `done_by_domain`）+ 物理仍扁平」方案，避免一次性 bulk `git mv` 138 篇 task 带来的链接风险；工作区 `Projects/docs/harness/tasks/done/README.md` 若已物理域化，本仓将在 P1 子 task 中跟进。

---

## 5. SKILL 研判

### 结论

- **是否更新**：是（已更新）
- **涉及 SKILL**：`SKILL-docs-governance` · `SKILL-harness-task`

### 理由

- `SKILL-docs-governance.md` §关账 hygiene **H2** 原写「`_views/done.md` 新增一行链 `../done/task_*.md`」，与 Hub 纪律「`_views/done.md` 薄指针、Hub / `done_by_domain` 更新」直接冲突。
- `SKILL-harness-task.md` §关账 checklist **第 3 项** 原写「`_views/done.md` 一行」，同样冲突。

### 已更新

| SKILL | 变更摘要 | 人审 |
|-------|----------|------|
| `SKILL-docs-governance.md` | H2 改为 Hub + `done_by_domain` 更新；VERIFY 改为查 Hub / `done_by_domain` + 薄指针行数 ≤15；修订记录 v1.1 | 须人审 |
| `SKILL-harness-task.md` | 关账 checklist 第 3 项改为「`_views/done.md` 保持薄指针；更新 Hub + `done_by_domain`」；修订记录 v1.3 | 须人审 |

**未改动**：`harness-loop-batch` / `harness-meta-reinspect` / `pr-post-ci` 等 SKILL 与本单 Hub 纪律无直接冲突。

---

## 6. 建议下一棒

- [x] 单独 docs commit：建议将本 SUMMARY + G1–G7 修复 + SKILL 更新作为一次 docs-only commit（无需新开 task）
- [ ] P1 子 task：`done` 物理域化 batch-1（分批 `git mv` 138 篇到 `done/<domain>/`）
- [ ] 人审 SKILL：`SKILL-docs-governance` 仍标 `draft`，需人审后标 `active`

---

## 7. 修订记录

| 日期 | 摘要 |
|------|------|
| 2026-06-13 | Agent 关账后卫生修复：G1–G7 pass、链接复检 zero broken、SKILL 已更新 |

---

## 给 Cursor

`governance-tasks-done-hygiene`、`post-close`、SUMMARY、SKILL-docs-governance、Hub、薄指针、G1–G7、zero broken
