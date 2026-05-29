# Task：治理 — Wiki 里程碑验收文档扩充

> **状态**：done（2026-05-29 · PR #87 · Loop R1 归档）  
> **Loop 承接**：R1 关账 [`task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md`](../done/task_chatbi_v3_p2_loop_r1_closeout_hygiene_v1.md) · 已合 **PR #87**  
> **schedule_ref**：RECENT §1.1 #W1 · **done**  
> **epic**：治理 · Wiki / 验收留证  
> **blocked_by**：无（#83 · #85 已合 `main`）  
> **blocks**：无（不阻塞 V3 业务线）  
> **排期**：见 [`RECENT_TASK_SCHEDULE.md`](../RECENT_TASK_SCHEDULE.md) · Wiki hub [`task-schedule-ink-backend`](../../coding_wiki/concepts/task-schedule-ink-backend.md)  
> **基线文稿**：[`docs/diary/2026-05-29-wiki-milestone-acceptance.md`](../../diary/2026-05-29-wiki-milestone-acceptance.md)

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 纯 docs / diary 验收扩充；无 `api/` 变更。 |
| **freeze_id** | `GOV-WIKI-MILESTONE-ACCEPT@2026-05-29` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/gov-wiki-milestone-acceptance-expand-v1` |
| **worktree_root** | `../ai-ink-brain-api-python-wt-wiki-accept`（与 P2-1b 并行） |
| **task_slug** | `gov-wiki-milestone-acceptance-expand` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 30 | 与业务线并行扩充验收稿 |
| HG-REINSPECT | approved | done | 里程碑验收已批准（2026-05-29 · 人授 Agent 代填） |

---

## 背景与目标

Wiki 治理线机器门禁与 AB 证据已收口（#83 · diary 草案）；本 task **扩充对内验收文稿**，便于验收人签字与后续公众稿蒸馏（§8），**不**替代 L0/L1 真值。

**完成态**：

1. diary 验收稿 §1 结论表可签字（VERIFY 留证完整、边界清晰）  
2. §6 smoke / §7 边界 / §8.2 扩充清单逐项推进（能 frozen 的勾选并注明依据）  
3. RECENT §6.6 或修订记录同步「验收扩充 done」  
4. 关账 `git mv` · `_views/done.md`（可选 50）

---

## 范围

- [x] 扩充 `2026-05-29-wiki-milestone-acceptance.md`（§1 签字区、§3 留证日期、§8.2 清单进度）— 30 已执行  
- [x] 链 AB 实验结论 pointer（`wiki_ctx_ab_*` · task-schedule smoke）— diary 已链  
- [ ] `log.md` 一行 · RECENT §8 修订 — 非本 10→30 链范围  
- [x] 公众稿 **对内** 素材标注（不写公众仓正文）— §8.2 6/8 已勾选

## 非范围

- Batch-4 ingest · P3 lint CI（另单）  
- 改 `api/` · 图谱机器轨  
- 公众仓 `ai-coding-closed-loop-articles` 定稿发布

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | diary 结论覆盖 L0 图谱 | 22/人审阻塞 · 改 pointer |
| F2 | 无 VERIFY 留证即标「批准」 | 验收 fail · 补 §3 |

---

## 验收标准

- [ ] diary §1 四项均有 pass/边界说明且可签字  
- [ ] §8.2 至少 **5/8** 项已勾选或显式 defer 理由  
- [ ] `python tools/coding_wiki_graph_nodes_lint.py` 仍 OK（若 touch Wiki）  
- [ ] 关账 `git mv` · `_views/done.md`

---

## 自检结论（执行者）

| 项 | 结果 |
|----|------|
| 执行日期 | 2026-05-29 |
| 执行帽 | 30 · R1 |
| 修改文件 | `docs/diary/2026-05-29-wiki-milestone-acceptance.md` |
| 验证命令 | `python tools/coding_wiki_graph_nodes_lint.py` |
| 验证结果 | **OK** |

### 修改摘要

- §1：追加「可签字确认」小结（VERIFY 留证完整、AB 证据链可链、工程交付已关账）
- §3.2：追加「留证完整」结语（本机 main · 2026-05-29 · 六命令全绿）
- §6：追加「可签字确认」小结（smoke 4/4 pass · freeze_id 已标注）
- §7：追加「可签字确认」小结（边界表已列明、业务线同步按 §4.1 ingest）
- §8.2：6/8 项勾选（附依据备注）、2/8 defer（附理由）
- §9：追加「10→30 扩充」一行修订记录

### 验收标准核对

- [x] diary §1 四项均有 pass/边界说明且可签字 — §1 已追加可签字确认小结
- [x] §8.2 至少 5/8 项已勾选或显式 defer 理由 — **6/8 已勾选、2/8 defer**
- [x] `coding_wiki_graph_nodes_lint.py` 仍 OK — 验证通过
- [ ] 关账 `git mv` + `_views/done.md` — 不在本 10→30 链范围（可选 50 或人手动）

### 40 复检确认（独立重跑）

| 项 | 结果 |
|----|------|
| 复检日期 | 2026-05-29 |
| 复检帽 | 40 · R1 |
| 验证命令 | `python tools/coding_wiki_graph_nodes_lint.py` |
| 退出码 | 0 |
| 输出摘要 | `coding_wiki_graph_nodes_lint: OK` |
| diff 核对 | 仅 `docs/diary/2026-05-29-wiki-milestone-acceptance.md` 变更；无 api/、图谱、CODING_WIKI、RECENT 误触 |
| 验收标准 | §1 可签字 ✓ · §8.2 6/8 ✓ · lint OK ✓ · 范围锁遵守 ✓ |
| 结论 | **通过** · 可进入 50 或关账

---

## 给 Cursor

`gov-wiki-milestone-acceptance-expand`、diary 验收、公众稿扩充清单、与 P2-1b 并行
