# JSON vs Mermaid 对比叙事 — 日记落盘区

> **目录**：`docs/diary/jsonPKmermaid/`  
> **符号表（必读）**：[`NOTATION_zh.md`](./NOTATION_zh.md) — **Sx=段 Segment** · **Px=KPI Priority** · **Rx=规则 Rule**（Rx≠单次 LLM）  
> **用途**：**轴 II 静态载荷** 与 **轴 I 历史 Prompt A/B** 的摘要指针；**行为实验** `graph.json` vs Mermaid 语料（V3 KPI）协议。  
> **Rubric 演示**（`examples_builtin` 等）已迁至 [`../../_staging/jsonPKmermaid-rubric-demo/`](../../_staging/jsonPKmermaid-rubric-demo/)。

## 阅读顺序

| 顺序 | 文件 | 说明 |
|------|------|------|
| ★ | [`NOTATION_zh.md`](./NOTATION_zh.md) | **缩写对照**（S/P/R/Phase 消歧） |
| 0 | [`EXPERIMENT_LOG.md`](./EXPERIMENT_LOG.md) | **实验日志**（防漂移；真值表） |
| 1 | [`00_legacy_compare_summary.md`](./00_legacy_compare_summary.md) | 旧对比谱系（`docs/diary/test` + 闸口 A 专文） |
| 2 | [`01_experiment_json_vs_mermaid_kpi_v1.md`](./01_experiment_json_vs_mermaid_kpi_v1.md) | 行为实验协议（`CTX_JSON` vs `CTX_MERMAID`，`draft`） |
| 3 | [`02_minimal_first_step_v1.md`](./02_minimal_first_step_v1.md) | 最小可跑第一步（历史；P0 已超越） |
| — | [`fixtures/gate_ctx_ab_v1/`](./fixtures/gate_ctx_ab_v1/) | 题集、payloads、runner |
| — | [`runs/`](./runs/) | **仅保留 canonical S0 三批 + P0-B 全量** |
| — | [`reports/conclusion_gate_ctx_ab_three_tasks_draft_zh.md`](./reports/conclusion_gate_ctx_ab_three_tasks_draft_zh.md) | **S0 三题总表（draft）** |
| — | [`reports/conclusion_s1s2_batch_20260516_152126_zh.md`](./reports/conclusion_s1s2_batch_20260516_152126_zh.md) | S1/S2 全量（draft） |
| **4** | [`reports/conclusion_gate_ctx_ab_final_zh.md`](./reports/conclusion_gate_ctx_ab_final_zh.md) | **定稿结论（P0·accepted）**；§0.1 关系图 |
| **5** | [`P1_README.md`](./P1_README.md) | **Phase·P1 双人盲审 SOP** |
| — | [`三相塌缩等价性论文_拓扑综合.md`](./三相塌缩等价性论文_拓扑综合.md) | 理论原文（LLM/CIS 层） |
| — | [`治理层三相塌缩_Ink技术图谱应用.md`](./治理层三相塌缩_Ink技术图谱应用.md) | **论文 → Ink 治理层**应用说明（不改 Transformer） |

## 与历史资产的关系

- **Prompt A/B 原始材料**：`docs/diary/test/`（勿搬迁；本目录仅摘要与指针）。  
- **闸口 A 静态 A/B 单一真值**：`docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md` §4 / §9。
