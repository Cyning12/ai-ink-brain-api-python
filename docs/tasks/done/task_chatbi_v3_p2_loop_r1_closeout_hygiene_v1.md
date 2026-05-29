# Task：ChatBI P2 Loop R1 — 已合 PR 关账与排期 hygiene

> **状态**：done（2026-05-29）  
> **schedule_ref**：RECENT §1.1 ~~#L1-R1~~ **done**  
> **epic**：ChatBI V3 · P2 韧性 Loop  
> **Loop 母单**：[`task_chatbi_v3_p2_resilience_loop_v1.md`](task_chatbi_v3_p2_resilience_loop_v1.md)  
> **round**：**R1** · 见 [`LOOP_MANIFEST.md`](../../harness/invokes/by-task/chatbi-v3-p2-loop/LOOP_MANIFEST.md)

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs/索引；实现已在 **PR #86**、**#87** 合 `main`。 |
| **freeze_id** | `CHATBI-P2-R1-CLOSEOUT@2026-05-29` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/chatbi-v3-p2-loop-v1`（与母单相同） |
| **task_slug** | `chatbi-v3-p2-loop-r1-closeout` |
| **human_gate** | **继承母单** `HG-LOOP-BATCH`（见母 task 表） |

**帽子顺序**：跳过 10 · 链 `PROMPT_LOOP_22_to_CLOSE` · round=**R1**

---

## 背景与目标

P2-1b（限流）与 W1（Wiki 验收稿扩充）已分别合入 **#86** / **#87**，但 task 仍滞留 `active/`、RECENT 仍标双轨并行。本 round **一次性关账**，为 R2 熔断清场。

---

## 范围

- [x] **`git mv`** 至 `done/`（文首 `done（2026-05-29）` 与 mv **同一提交**）：
  - `task_chatbi_v3_p2_resilience_rate_limit_v1.md`（链 [`reinspect_chatbi_v3_p2_1b_rate_limit_20260529_v1.md`](../reinspect_results/reinspect_chatbi_v3_p2_1b_rate_limit_20260529_v1.md)）
  - `task_governance_wiki_milestone_acceptance_expand_v1.md`
- [x] 更新 [`docs/tasks/_views/done.md`](../_views/done.md) 两条索引
- [x] 更新 [`docs/tasks/done/task_chatbi_v3_p2_resilience_v1.md`](done/task_chatbi_v3_p2_resilience_v1.md) **§子单状态**（P2-1b/W1 **done**）
- [x] [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) §1.1：#0b/#W1 → done；删除 §1.2 双轨 worktree
- [ ] 可选 50：[`reinspect_chatbi_v3_p2_loop_r1_closeout_20260529_v1.md`](../reinspect_results/reinspect_chatbi_v3_p2_loop_r1_closeout_20260529_v1.md)（docs 摘要）

## 非范围

- 不改 `api/`（限流代码已在 #86）
- 不实现 P2-1c（**R2**）
- 不写公众仓正文

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | 母闸 `HG-LOOP-BATCH` pending | 硬停 |
| F2 | 仅改状态不归档 | 40 fail |
| F3 | RECENT 仍写双轨 in_progress | 50 fail |

---

## 验收标准

- [x] 两 task 仅在 `done/`，`active/` 无 #0b/#W1
- [x] `_views/done.md` 与 `done/` 计数一致
- [x] RECENT §1.1 反映 **done** + 当前棒指向 Loop **R2**
- [x] `python tools/coding_wiki_graph_nodes_lint.py` OK（若 touch Wiki 路径）

---

## 给执行帽的必读列表

1. 本 task · 母单 Loop  
2. 待归档两 task 全文 + 50 复检（P2-1b）  
3. [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md)  
4. [`docs/diary/2026-05-29-wiki-milestone-acceptance.md`](../../diary/2026-05-29-wiki-milestone-acceptance.md)

---

### 自检结论（执行者）

| 项 | 结果 |
|----|------|
| 执行日期 | 2026-05-29 |
| 40 帽 | 独立复检 |
| 命令 1 | `pytest tests -m "not intent_eval and not intent_benchmark" -q` |
| 结论 1 | `253 passed, 1 skipped, 2 deselected` · exit 0 |
| 命令 2 | `python tools/coding_wiki_graph_nodes_lint.py` |
| 结论 2 | OK |
| 归档核对 | `active/` 无 #0b/#W1；`done/` 含 rate_limit + wiki_milestone + 本 R1 task |
| RECENT | §1.2 已删；§1.1 当前棒 **0c / R2** |
| 结论 | **pass** · R1 关账完成 · 可进入 R2 |
