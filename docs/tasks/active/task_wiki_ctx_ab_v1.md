# Task：Wiki-CTX-AB v1（Harness 上下文消费对照 · P1→P2）

> **状态**：`active`（P1 **done** · P2 待 coding_wiki pilot）  
> **关联 SPEC**：[`docs/spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md`](../spec/governance/SPEC-Governance-Wiki-Harness-Roadmap-v1.md)  
> **实验目录**：[`docs/harness/experiments/wiki_ctx_ab_v1/`](../harness/experiments/wiki_ctx_ab_v1/README.md)  
> **并行**：[`task_coding_wiki_pilot_v1.md`](./task_coding_wiki_pilot_v1.md)（T1b，供 P2 的 W 臂）

---

## Harness 元信息

| 字段 | 值 |
|------|-----|
| **test_strategy** | `not_applicable` |
| **test_strategy_note** | 实验填表 + 结论文；无代码/CI 变更。 |
| **freeze_id** | `WIKI-CTX-AB@2026-05-25` |
| **gates_before_code** | `["human_gate"]` |
| **semi_auto** | `false` |
| **audit_profile** | `post_close` |

| human_gate_id | status | blocks_hats | 说明 |
|---------------|--------|-------------|------|
| HG-AB-SLUG | approved | — | gold slug = `harness-p1-docs-consolidation` |
| HG-AB-P1-DONE | approved | P2 执行 | P1 已验收 — [`conclusion_p1_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p1_zh.md) |

---

## 背景与目标

用可复现 **H-full / H-lean / W** 对照，为 **Harness 全仓推广** 与 **Coding Wiki 默认读序** 提供证据（见 SPEC §3）。

**P1 完成态**：物化两 payload + `scorecard` §P1 + `conclusion_p1_zh.md`。  
**P2 完成态**（依赖 pilot 同 slug ingest）：`TEMPLATE-W` + `scorecard` §P2 + `conclusion_p2_zh.md`。

---

## 范围

- [x] 按 [`questions.md`](../harness/experiments/wiki_ctx_ab_v1/questions.md) 跑 P1（4 题 × 2 臂）。
- [x] `payloads/H-full_harness-p1-docs-consolidation.md`、`H-lean_*.md` 已物化。
- [x] [`scorecard.md`](../harness/experiments/wiki_ctx_ab_v1/scorecard.md) · [`conclusion_p1_zh.md`](../harness/experiments/wiki_ctx_ab_v1/conclusion_p1_zh.md)。
- [ ] （P2）同 slug 的 Wiki 页就绪后，补 W 臂与 `conclusion_p2_zh.md`。

## 非范围

- 不改 `docs/harness/prompts/`、CI、api/。
- 不替代 `task_coding_wiki_pilot_v1` 交付 `coding_wiki/` 骨架。

---

## 验收标准

- [ ] P1 `scorecard` 含每题 × 两臂的 `payload_char_count`、正确性 pass/fail。
- [ ] `conclusion_p1_zh.md` 明确：是否推荐 T3 Harness 推广。
- [ ] （P2）`conclusion_p2_zh.md` 明确：是否默认先读 `coding_wiki/`。

---

## 修订记录

| 日期 | 摘要 |
| --- | --- |
| 2026-05-25 | 初稿 `draft` |
