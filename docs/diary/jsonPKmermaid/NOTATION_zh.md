# gate_ctx_ab 符号表（Notation）

> **维护**：本目录凡出现单字母或 `Sx` / `Px` / `Rx` 缩写，**以本表为准**；正文首次出现宜写「缩写（全称·中文）」，或文首链到本文件。  
> **易混警示**：**R 在定稿文 §4 = Rule（规则）**，**不是**单次 LLM API 调用，也**不是** S0 批跑的重复轮次 Repeat。

---

## 1. 实验段 · Segment `S0` `S1` `S2`

| 符号 | 全称 | 中文 | 是什么 | 不是什么 |
|------|------|------|--------|----------|
| **S0** | Segment 0 | 段 0 · 冷启动 | 协议第一段：1 题 + 全量主载荷，通常 1 次 LLM/轮（批跑可并行多轮） | 不是 arm；不是 KPI |
| **S1** | Segment 1 | 段 1 · 同题追问 | 同题固定追问 ×3（见 `user_scripts.json`） | 不是「第 1 次 API」的通用编号 |
| **S2** | Segment 2 | 段 2 · 换题 | 同线程换另外 2 题 ×2 轮，测泄漏 | 同上 |

**一次 LLM 调用** = 一条 `*.jsonl` 记录（文件名含 `_S0`、`_S1_01`、`_S2_02` 等）。

**一次会话** = 1 题 × 1 arm ×（S0 + S1×3 + S2×2）= 最多 **6 次** LLM 调用。

---

## 2. KPI 维度 · Priority `P1`～`P4`

| 符号 | 全称 | 中文 | 度量（P0 自动化程度） |
|------|------|------|------------------------|
| **P1** | Priority 1 · Handoff | 易交接 | 结构/步骤/门禁；**P1 阶段**靠双人 Rubric，P0 未跑 |
| **P2** | Priority 2 · Reliability | 可靠性 | entry/impact F1、S2 泄漏；`score_gold_f1.py` |
| **P3** | Priority 3 · Cost | 省钱 | `prompt_tokens + completion_tokens` |
| **P4** | Priority 4 · Latency | 省时 | `wall_s` / `wall_total` |

合成权重（V3）：**P1 40% > P2 35% > P3 15% > P4 10%**（见 `01_experiment_json_vs_mermaid_kpi_v1.md` §5）。

> **勿与「实验阶段 P0/P1」混淆**：下表的 **P0、P1** 表示 **Phase（阶段）**，与 KPI 的 **P1 易交接** 不同列。

---

## 3. 实验阶段 · Phase `P0` `P0-A` `P0-B` `P1`

| 符号 | 全称 | 含义 |
|------|------|------|
| **P0** | Phase 0 | 行为实验跑数 + 自动化指标（无双人 Rubric） |
| **P0-A** | Phase 0-A | ≥3 题 S0 批跑 + gold F1 |
| **P0-B** | Phase 0-B | S1/S2 全协议（`run_s1_s2.py`） |
| **P0.9** | Phase 0.9 | 定稿文 + 决策规则（文档收口） |
| **P1** | Phase 1 | 可选：双人 Rubric 抽样、F1 收紧 |

---

## 4. 签收规则 · Rule `R1`～`R6`（定稿文 §4）

| 符号 | 全称 | 中文 | 含义 |
|------|------|------|------|
| **R1～R6** | **Rule** 1–6 | 规则 1–6 | 是否签收「Agent 默认 `CTX_JSON`」的**书面门槛**；每条用**多题汇总 KPI** 判定 |

**签收判定**：Rule-1 ∧ … ∧ Rule-6（全部满足才签收）。

---

## 5. 其他易混 `R`

| 上下文 | 符号 | 全称 | 说明 |
|--------|------|------|------|
| S0 批跑 | **R**（数字） | **Repeat** 重复轮次 | 如每题跑 **R=3** 次并行取中位数；见 `01_experiment` §5.4 |
| 双人盲审 | **R1 / R2** | **Reviewer** 1/2 | 评审员编号；见 `01_experiment` §5.6 |
| 仲裁 | **R3** | **Reviewer** 3（仲裁） | 第三人，**不是** Rule-3 |

---

## 6. 对照与其它

| 符号 | 含义 |
|------|------|
| **arm** | 对照分支：`CTX_JSON` vs `CTX_MERMAID` |
| **α / β** | `context_strategy`：每轮全量 vs S0 全量 + S1/S2 摘要 |
| **T001～T003** | `tasks.json` 中的 `task_id` 简写 |

---

## 7. 段·S0 主表列名（定稿文 §2.0）

| 列 | 含义 | KPI |
|----|------|-----|
| 题 / topic | `task_id` 简写 / `topic_id` | — |
| arm | `CTX_JSON` vs `CTX_MERMAID` | — |
| wall_s ↓ | 墙钟秒数中位数（剔除离群后） | P4 |
| tokens ↓ | prompt+completion tokens 中位数 | P3 |
| entry F1 ↑ | gold `entrypoints` 启发式 F1 | P2 |
| impact F1 ↑ | gold `impacts` 启发式 F1 | P2 |
| run | canonical batch 目录 | — |

详表见 [`reports/conclusion_gate_ctx_ab_final_zh.md`](./reports/conclusion_gate_ctx_ab_final_zh.md) **§2.0**。

---

## 8. 推荐阅读顺序中的符号入口

| 文档 | 符号集中出现 |
|------|----------------|
| [`reports/conclusion_gate_ctx_ab_final_zh.md`](./reports/conclusion_gate_ctx_ab_final_zh.md) | §0 术语 + §0.1 关系图 + §4 Rule-1～6 |
| [`01_experiment_json_vs_mermaid_kpi_v1.md`](./01_experiment_json_vs_mermaid_kpi_v1.md) | S0–S2、P1–P4、Reviewer R、Repeat R |
| [`EXPERIMENT_LOG.md`](./EXPERIMENT_LOG.md) | Phase P0-A/B、段 S0/S1/S2 |
