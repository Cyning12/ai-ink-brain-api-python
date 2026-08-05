# Task：Governance A4 — RECENT 排期 Wiki Loop 同步（v1）

> **状态**：done（2026-05-26 验收通过 · GOV-WIKI-A4-SCHEDULE@2026-05-26）  
> **母 Loop**：[`task_harness_wiki_loop_a1_a4_v1.md`](task_harness_wiki_loop_a1_a4_v1.md) · round **A4**  
> **排期真值**：[`docs/tasks/RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) **§1**、**§6.6**

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；随后执行母 task META 关账。  
> **Harness 字段真值**：[`docs/harness/HARNESS_V2_PLAN.md`](../harness/HARNESS_V2_PLAN.md) **§5**。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 排期表维护；无代码变更。 |
| **freeze_id** | `GOV-WIKI-A4-SCHEDULE@2026-05-26` |
| **gates_before_code** | `["human_gate", "failure_paths", "A1–A3 done 建议"]` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-a1-a4-v1` |
| **task_slug** | `wiki-a4-recent-schedule` |
| **wiki_delta** | `none` |
| **wiki_delta_note** | 存量迁移 · 本 task 无 Wiki 增量（2.18 wiki_delta） |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 母 task [`HG-LOOP-BATCH`](task_harness_wiki_loop_a1_a4_v1.md) = `approved` 后方可 22 |

---

## 帽子顺序（**跳过 10** · Loop A4）

| 序 | 帽 | 启动 |
|----|-----|------|
| — | **10** | **跳过** |
| 1 | **22 R1** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../harness/invokes/by-task/wiki-loop-a1-a4/PROMPT_LOOP_22_to_CLOSE_v1.md) · [`LOOP_MANIFEST.md`](../harness/invokes/by-task/wiki-loop-a1-a4/LOOP_MANIFEST.md) **round=A4** |
| 2–5 | **30→40→50→关账** | 同上 Loop 链 |

**建议**：A4 在 **A1–A3 均 `done/`** 后执行，§1 active 数量与「近期当前棒」才准确。

---

## 背景与目标

Wiki Loop A1–A4 将新增/移动多个 `active/` task 并最终归档；`RECENT_TASK_SCHEDULE.md` **§1 现状快照**（active 数量、近期当前棒）与 **§6.6 Wiki 行** 须在 Loop 完成后反映：**Multi done**、**Wiki Loop A1–A4 done**、下一棒（如 P1-4 远期）清晰。

**完成态**：§1 与 §6.6 与磁盘 `active/`、`done/` 及母 Loop 关账状态一致；修订记录追加一行。

---

## 范围

- [x] 更新 `RECENT_TASK_SCHEDULE.md` **§1** 现状快照：`active/` 文件数、§1.1 清单（含或不含 Loop 五 task 的最终态）。  
- [x] 更新 **§1**「近期当前」：Wiki Loop **done** 后指向合理下一棒（如 P1-4 远期或 V3 队列）。  
- [x] 更新 **§6.6**：增补 **Wiki Loop A1–A4** 行（进行中 → **done**，链母 task + 四子 done task）。  
- [x] 确认 §6.6 **Multi slug**、**T1c** 行仍为 **done**（若无漂移则保留）。  
- [x] §8 修订记录追加 2026-05-26 Loop 关账摘要。  
- [x] 22/40/50 落盘；关账 `done/`。

## 非范围

- 不改 SPEC 正文、对比表（属 A3）。  
- 不改 `docs/coding_wiki/` synthesis（属 A1/A2）。  
- 不调整 V3 ChatBI 子单排期优先级（除非 task 明示）。  
- 不改 `api/`、`tests/`、CI、prompts。

---

## 依赖与引用

| 依赖项 | 路径/说明 |
|--------|-----------|
| 排期表 | `docs/tasks/RECENT_TASK_SCHEDULE.md` §1、§1.1、§6.6、§8 |
| 母 Loop | `docs/tasks/active/task_harness_wiki_loop_a1_a4_v1.md`（关账前可能仍在 active） |
| A1–A3 done | `docs/tasks/done/task_coding_wiki_*`、`task_governance_wiki_spec_*` |
| 索引 | `docs/tasks/_views/done.md`（关账时同步） |
| 母 Loop Manifest | `LOOP_MANIFEST.md` round A4 |

---

## 失败路径

| # | 触发条件 | 系统行为 | 可重试 | 用户可见 |
|---|----------|----------|--------|----------|
| F1 | §1 active 计数与 `ls docs/tasks/active/*.md` 不符 | 40 **fail** | 是 | 重数并修正 |
| F2 | §6.6 仍写「下一棒 T1c 需新建 active」 | 文档过时；22 **阻塞** | 是 | T1c 已 done |
| F3 | A1–A3 未 done 即宣称 Loop 全 done | 22 要求 §6.6 标「进行中」或延后 A4 | 是 | 见母 task 顺序 |
| F4 | 漏更新 §1.1 仍列 Loop active task | 50 **fail** | 是 | 归档后从 active 表移除 |

---

## 验收标准

- [x] `ls docs/tasks/active/task_harness_wiki_loop*.md docs/tasks/active/task_coding_wiki_*test_strategy*.md docs/tasks/active/task_governance_wiki_*` **无结果**（Loop 五 task 均已 `done/`）。  
- [x] §1 active 数量与 §1.1 表格一致。  
- [x] §6.6 含 Wiki Loop A1–A4 **done** 行（或关账前明确「进行中」+ 链 active 路径）。  
- [x] 22 R1 落盘 `reviews/by-task/wiki-loop-a1-a4/`。  
- [x] 50 复检 pass；本 task 在 `done/`。

**合并前必绿（本仓）**：`pytest tests -m "not intent_eval and not intent_benchmark"`。

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `docs/tasks/RECENT_TASK_SCHEDULE.md`（+ 可选 `_views/done.md`） |
| 图谱变更点 | 无 |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | `ls docs/tasks/active/task_harness_wiki_loop*.md`（关账前母单仍在 active）；`grep Wiki Loop docs/tasks/RECENT_TASK_SCHEDULE.md` |
| 结论 | **pass** |
| 要点 | §6.6 Wiki Loop **done**；§8 修订已追加 |

---

## 给 Cursor

`wiki-a4-recent-schedule`、`GOV-WIKI-A4-SCHEDULE@2026-05-26`、`RECENT_TASK_SCHEDULE` §1 §6.6、`PROMPT_LOOP_22_to_CLOSE`、`round=A4`
