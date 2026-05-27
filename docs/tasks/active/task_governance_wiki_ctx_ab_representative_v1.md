# Task：治理 — Wiki-CTX-AB 代表性扩面（6 slug · P2）

> **状态**：draft  
> **前置**：P2 [`conclusion_p2_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p2_zh.md) · Multi [`task_wiki_ctx_ab_multi_slug_v1.md`](../done/task_wiki_ctx_ab_multi_slug_v1.md) · 读序+ingest **done**  
> **SPEC**：[`SPEC-Governance-Wiki-CTX-AB-Representative-v1.md`](../spec/governance/SPEC-Governance-Wiki-CTX-AB-Representative-v1.md)  
> **SKILL**：[`SKILL-harness-task.md`](../skills/SKILL-harness-task.md) · [`SKILL-docs-governance.md`](../skills/SKILL-docs-governance.md)

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；更新 `_views/done.md` · RECENT §6.6/§8 · 对比表 #46。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 对照实验填表+结论文；不改 api/CI。 |
| **freeze_id** | `WIKI-CTX-AB-REP@2026-05-27` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-ctx-ab-representative-v1` |
| **task_slug** | `wiki-ctx-ab-representative` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-TASK-DRAFT | approved | 22, 30 | SPEC + 6 slug + 阈值 |
| HG-AUDIT-R1 | approved | 30 | 22 R1 后人签 |
| HG-AB-REP-SLUGS | approved | 30 | **锁定** SPEC §2.1 六 slug |
| HG-AB-REP-RUN | approved | 30 | 允许 30 帽跑题/物化（长会话） |

---

## 长任务执行（单 task 全链）

| 规则 | 内容 |
| --- | --- |
| **模式** | `SKILL-harness-task` · 30 帽工作量大 · **同会话** 22→关账 |
| **【授权】** | 人闸已批 · 无新 pending 不停 |
| **【停】** | F1–F4 · 改 slug 名单 · W 臂作弊读 done 全文 |
| **入口** | [`PROMPT_START_full_chain_v1.md`](../../harness/invokes/by-task/wiki-ctx-ab-representative/PROMPT_START_full_chain_v1.md) |
| **ST1–ST6** | 关账前勾选 |

---

## 帽子顺序

| 序 | 帽 | 启动 |
|----|-----|------|
| 0 | **10** | **跳过** |
| 1–5 | **22→关账** | `PROMPT_START` · `PROMPT_TASK_22_to_CLOSE_v1.md` §3 |

---

## 背景与目标

读序+15 篇 synthesis 已就绪。本 task 在 **6 个代表性 slug** 上复跑 **H-lean vs W**，为 **前端 P1-4 Harness parity 大包** 提供定量证据（SPEC §5）。

**完成态**：

- 12 个 payload 物化 · `scorecard.md` 填满 · `conclusion_representative_zh.md` 聚合签收  
- 若 **accepted**：结论文 **建议** 立项前端 parity（链 Roadmap P1-4 · 不本 task 执行）

---

## 范围

- [ ] 6 slug × H-lean/W 物化（`docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads/`）
- [ ] 按 [`questions.md`](../harness/experiments/wiki_ctx_ab_representative_v1/questions.md) 跑题填表
- [ ] [`scorecard.md`](../harness/experiments/wiki_ctx_ab_representative_v1/scorecard.md) 聚合 T7/T8
- [ ] [`conclusion_representative_zh.md`](../harness/experiments/wiki_ctx_ab_representative_v1/conclusion_representative_zh.md)
- [ ] 更新 `WIKI_REQUIREMENTS_COMPARISON_v1_zh.md` #46 行（附条件外推）
- [ ] 22/30/40/50 + reinspect + 关账

## 非范围

- 前端 `ai-ink-brain` 改文件  
- 新 ingest · 新 slug  
- P1（H-full）臂  
- `api/` · `tests/` · workflow  

---

## 锁定 slug（SPEC §2.1）

| # | slug |
|---|------|
| 1 | `harness-p1-docs-consolidation` |
| 2 | `tech-graph-gate-d-v2-tasks` |
| 3 | `chatbi-v3-p2-health-ready` |
| 4 | `governance-l2-manifest-ci` |
| 5 | `wiki-ctx-ab-v1` |
| 6 | `harness-wiki-loop-t4-l2` |

---

## 失败路径

| # | 触发 | 行为 |
|---|------|------|
| F1 | 改 6 slug | 停 |
| F2 | W 读 done/invoke 全文 | slug invalid |
| F3 | <5/6 达标写 accepted | 50 fail |
| F4 | 无 payload 字符统计 | 40 fail |

---

## 验收标准

- [ ] payload 文件 **12** 个（6×2）
- [ ] SPEC §3 T7/T8 聚合 **pass**
- [ ] `conclusion_representative_zh.md` 含 **局限** + **前端建议** 节
- [ ] 50 reinspect + 关账 hygiene

**VERIFY（40）**：

```bash
ls docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads/H-lean_*.md | wc -l   # 6
ls docs/harness/experiments/wiki_ctx_ab_representative_v1/payloads/W_*.md | wc -l        # 6
test -f docs/harness/experiments/wiki_ctx_ab_representative_v1/conclusion_representative_zh.md
python tools/tech_graph_manifest_check.py
```

---

## 实现备忘（由子 Agent 回填）

| 项 | 内容 |
|----|------|
| 物化方式 | （待填：脚本/手工 · 参照 wiki_ctx_ab_v1 TEMPLATE） |
| 聚合降幅 | （待填） |

---

## 自检结论（执行者 · 40 帽回填）

| 项 | 结果 |
|----|------|
| 命令 | （待填） |
| 结论 | pass / fail |

---

## 给 Cursor

`wiki-ctx-ab-representative`、6 slug、scorecard、前端证据、H-lean、W
