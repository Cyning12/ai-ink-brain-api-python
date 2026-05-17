# S1/S2 全量批跑结论（P0-B · draft）

> **批跑**：[`gate_ctx_ab_v1_s1s2_20260516_152126`](../runs/gate_ctx_ab_v1_s1s2_20260516_152126/)  
> **策略**：β（S0 全量图谱；S1/S2 摘要 + manifest/contract）  
> **耗时**：约 4.5h（36/36 轮 `ok`，`exit_code=0`）  
> **日志**：[../EXPERIMENT_LOG.md](../EXPERIMENT_LOG.md)

---

## 1. 与 S0-only 批跑的关系

| 维度 | S0 批跑（canonical） | 本批 S1/S2 |
|------|---------------------|------------|
| 目的 | 冷启动单轮对比 | 同线程多轮 **累计 token**、换题泄漏 |
| 载荷 | 每轮全量 α | S0 全量 + S1/S2 β 摘要 |
| 不宜直接比墙钟 | 单轮中位数 | 累计 token 中位数 |

S0-only 结论仍见 [`conclusion_gate_ctx_ab_three_tasks_draft_zh.md`](./conclusion_gate_ctx_ab_three_tasks_draft_zh.md)。

---

## 2. 累计 token（会话末，6 会话）

| 题 | CTX_JSON | CTX_MERMAID | 更低 |
|----|----------|-------------|------|
| T001 | **141,365** | 148,257 | JSON |
| T002 | 159,335 | **154,664** | Mermaid |
| T003 | **154,026** | 155,509 | JSON |
| **arm 中位数** | **154,026** | **154,664** | JSON 略低（≈0.4%） |

S0 单轮 token 中位数：JSON **~12,208**；Mermaid **~12,740**（与 S0 批跑同量级）。

---

## 3. S2 串题泄漏（启发式 `leakage_count_heuristic`）

| 题 × arm | S2 两轮泄漏合计 |
|----------|----------------|
| T001 JSON / Mermaid | 4+2 / 3+2 |
| T002 JSON / Mermaid | 2+2 / 2+2 |
| T003 JSON / Mermaid | 2+5 / 4+4 |
| **arm 均值（每会话 S2 合计）** | JSON **~2.8** · Mermaid **~2.8** |

两 arm 泄漏相当；JSON 在 T003 主题题会话末 S2-2 略高（5）。

---

## 4. 墙钟离群（勿单独定论）

| 会话 | 轮次 | wall_s | 说明 |
|------|------|-------:|------|
| T001 JSON | S2-1 | **645** | 网关/API 离群 |
| T003 Mermaid | S0 | **394** | 冷启动离群 |
| T003 JSON | S2-1 | **380** | 离群 |
| T001 JSON | S1-1 | 258 | 偏高 |
| T002 Mermaid | S2-2 | 326 | 偏高 |

累计 token 仍由 API 计量；离群墙钟不计入「谁更快」主结论。

---

## 5. 本批 S0 段 gold F1（单轮，非 canonical 3×parallel）

与 S0 批跑同脚本；本批每会话仅 1 条 S0 记录。详见 [`gold_f1_s1s2_s0_segments.md`](./gold_f1_s1s2_s0_segments.md)。

| 题 | arm | entrypoints F1 | impacts F1 |
|----|-----|---------------:|-----------:|
| T001 | JSON / Mermaid | 0.800 / **0.857** | 0.333 / **0.364** |
| T002 | JSON / Mermaid | 0.500 / **1.000** | 0.154 / **0.333** |
| T003 | JSON / Mermaid | 0.909 / 0.909 | 0.267 / **0.714** |

与 canonical S0 批跑趋势一致：T002/T003 **Mermaid 入口或 impacts 更高**；不宜因 S1/S2 累计 token 略偏 JSON 而忽略 F1。

---

## 6. 规整后的问题清单（定稿前）

1. **性能 vs 质量仍分裂**：S0 批跑 JSON 墙钟/token 多题更优；S1/S2 累计 token JSON 中位数略优；F1 上 Mermaid 在 T002/T003 仍占优。  
2. **β 摘要是否够**：S1 起 `prompt_tokens` 线性涨（~16k→~39k），历史仍在膨胀；未测更短摘要模板。  
3. **泄漏启发式偏粗**：path 子串匹配，可能高估/低估。  
4. **定稿门槛**：建议 **不签收** 单一主载荷；若 Agent 默认 JSON，需接受 T002/T003 入口 F1 风险或加 Rubric 抽样（P1）。  
5. **下一步（P1）**：双人 Rubric 抽样；决策规则书面化（几胜才倾向 JSON）。

---

## 7. 一句话

**P0-B 全量跑通：36/36 合法 JSON；策略 β 下 JSON 累计 token 中位数略低于 Mermaid，S2 泄漏两 arm 相当；与 S0-only 结论一样，尚不足以签收「一律 JSON」，但 Agent 多轮场景下 JSON 未明显更费 token。**

---

## 附录

- 汇总表：[`../runs/.../152126/aggregate.md`](../runs/gate_ctx_ab_v1_s1s2_20260516_152126/aggregate.md)  
- smoke 对照：[`../runs/gate_ctx_ab_v1_s1s2_20260516_150452/`](../runs/gate_ctx_ab_v1_s1s2_20260516_150452/)
