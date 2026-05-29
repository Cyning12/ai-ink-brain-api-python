# Task：治理 — Wiki 里程碑验收文档扩充

> **状态**：in_progress  
> **schedule_ref**：RECENT §1.1 #W1 · **与 P2-1b 并行**  
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
| HG-REINSPECT | pending | done | 验收人签字后可关账 |

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

- [ ] 扩充 `2026-05-29-wiki-milestone-acceptance.md`（§1 签字区、§3 留证日期、§8.2 清单进度）  
- [ ] 链 AB 实验结论 pointer（`wiki_ctx_ab_*` · task-schedule smoke）  
- [ ] `log.md` 一行 · RECENT §8 修订  
- [ ] 公众稿 **对内** 素材标注（不写公众仓正文）

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

## 给 Cursor

`gov-wiki-milestone-acceptance-expand`、diary 验收、公众稿扩充清单、与 P2-1b 并行
