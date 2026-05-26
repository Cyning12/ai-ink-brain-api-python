# Task：Wiki-CTX-AB Multi — B-Q3 Recheck 载荷与 scorecard（R1）

> **状态**：draft  
> **母 Loop**：[`task_harness_wiki_loop_bq3_recheck_v1.md`](task_harness_wiki_loop_bq3_recheck_v1.md) · round **R1**  
> **关联实验**：[`docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/`](../../harness/experiments/wiki_ctx_ab_multi_slug_v1/)  
> **题面**：[`questions.md`](../../harness/experiments/wiki_ctx_ab_multi_slug_v1/questions.md) · slug B **B-Q3**

> 落盘规则：验收通过后 `git mv` → `docs/tasks/done/`；关账须回填 R2 [`PLACEHOLDER:R1_OUTCOME`](task_wiki_ctx_ab_multi_conclusion_bq3_sync_v1.md)。

---

## Harness 元信息（执行 Agent 必读）

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 实验文档与 W 载荷物化；不跑 pytest、不改 api。 |
| **freeze_id** | `WIKI-BQ3-R1-PAYLOAD@2026-05-26` |
| **semi_auto** | `true` |
| **audit_profile** | `post_close` |
| **git_branch** | `task/wiki-loop-bq3-recheck-v1` |
| **task_slug** | `wiki-bq3-r1-payload-scorecard` |

### 人工闸 `human_gate`

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| （继承母闸） | — | 22, 30, 40, 50 | 母 task [`HG-LOOP-BATCH`](task_harness_wiki_loop_bq3_recheck_v1.md) = `approved` 后方可 22 |

---

## 帽子顺序（**跳过 10** · Loop R1）

| 序 | 帽 | 启动 |
|----|-----|------|
| — | **10** | **跳过** |
| 1–5 | **22→50→关账** | [`PROMPT_LOOP_22_to_CLOSE_v1.md`](../../harness/invokes/by-task/wiki-loop-bq3-recheck/PROMPT_LOOP_22_to_CLOSE_v1.md) · MANIFEST **round=R1** |

---

## 背景与目标

A1 已在 [`query-rewrite-observability.md`](../../coding_wiki/syntheses/query-rewrite-observability.md) 补 `test_strategy: recommended`，但 Multi W 载荷 [`W_query-rewrite-observability.md`](../../harness/experiments/wiki_ctx_ab_multi_slug_v1/payloads/W_query-rewrite-observability.md) 仍为 A1 前快照（scorecard B-Q3 W **fail**）。

**完成态**：更新 W 载荷；在载荷隔离下重答 B-Q3（建议 slug B W 四题快检）；在 [`scorecard.md`](../../harness/experiments/wiki_ctx_ab_multi_slug_v1/scorecard.md) 增 **§Recheck** addendum（**不改** §Multi 主表）。

---

## 范围

- [x] 重新物化/更新 `payloads/W_query-rewrite-observability.md`（含 index + 目标 synthesis；frontmatter 须可见 `test_strategy`）。  
- [x] 独立会话或 50 帽模拟：依据 **仅 W 载荷** 答 B-Q3；记录 pass/fail 与要点对齐 [`questions.md`](../../harness/experiments/wiki_ctx_ab_multi_slug_v1/questions.md) gold。  
- [x] `scorecard.md` 末尾 **§Recheck（Wiki Loop B-Q3 · 2026-05-26）**：新 payload 字符量、B-Q1–Q4 W 臂 pass/fail、B-Q3 原文摘要。  
- [x] VERIFY：`rg -n test_strategy docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/payloads/W_query-rewrite-observability.md`  
- [ ] 关账回填 R2 `PLACEHOLDER:R1_OUTCOME`；`git mv` 至 `done/`。

## 非范围

- 不改 H-lean 载荷；不改 scorecard §Multi 冻结行。  
- 不在本 task 改 conclusion / 对比表 / SPEC（属 R2/R3）。  
- 不改 `api/`、`tests/`。

---

## 依赖与引用

| 依赖项 | 路径 |
|--------|------|
| synthesis 真值 | `docs/coding_wiki/syntheses/query-rewrite-observability.md` |
| 原 scorecard | `docs/harness/experiments/wiki_ctx_ab_multi_slug_v1/scorecard.md` |
| 物化参考 | 同目录 `payloads/` 现有 W 文件结构 · Multi task done 备忘 |
| B-Q3 gold | `questions.md` · `recommended` + 改 api 需 pytest 理由 |

---

## 失败路径

| # | 触发条件 | 系统行为 |
|---|----------|----------|
| F1 | 母闸 pending | 22 拒开工 |
| F2 | W 载荷仍无 test_strategy | 30/40 阻塞 · 查 synthesis / 物化脚本 |
| F3 | B-Q3 仍 fail | 允许关账但 R2 须如实写「仍部分」 |
| F4 | 误改 §Multi 主表 | 50 fail · revert 主表行 |

---

## 验收标准

- [ ] W payload 更新且 VERIFY 通过。  
- [ ] scorecard §Recheck 存在且与答题一致。  
- [ ] R2 占位已回填。  
- [ ] 22/40/50 落盘。

---

## 实现备忘（执行者回填）

| 项 | 内容 |
|----|------|
| 涉及文件 | `payloads/W_query-rewrite-observability.md` · `scorecard.md` §Recheck |
| B-Q3 结论 | **pass** · `recommended` + api/pytest 理由（§测试变更） |
| W 4/4 | **是** · slug B W 臂 B-Q1–Q4 全 pass（§Recheck） |

### 自检结论（执行者）

| 检查项 | 结果 | 备注 |
|--------|------|------|
| rg test_strategy W payload | | |
| scorecard §Recheck | | |

---

## 给 Cursor

`W_query-rewrite-observability`、§Recheck、B-Q3、载荷隔离、Loop R1
