# 旧对比方案总结（落盘）

> **日期**：2026-05-15  
> **范围**：本文件只总结「已发生过的对比类型」与结论层级，**不**替代原始真值文档。  
> **原始材料指针**：`docs/diary/test/`、`docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md`、`docs/tasks/done/task_engineering_tech_graph_gate_a_perf_compare_v1.md`

---

## 1. 两条独立「对比轴」（避免混读）

| 对比轴 | 代号含义 | 测的是什么 | 主真值 / 索引文档 |
|--------|-----------|------------|-------------------|
| **轴 I：Prompt 路径 A/B** | A ≈ 无图谱正文（全量/实现向读代码）；B ≈ `_tech_graph` 索引导航 + 抽样核验 | **LLM 新人冷启动接手**：token、自报时间、可审计性、V3 KPI 加权；**单次长文**为主 | `docs/diary/test/compare_three_versions_summary.md`（总表）；`compare_core_A_vs_B_v2.md`、`compare_core_A_vs_B_v3_patch.md` |
| **轴 II：闸口 A 静态载荷 A/B** | A ≈ 消费 `docs/_tech_graph/graph.json`；B ≈ 与同拓扑等价的 **Mermaid 语料总串**（工具拼接） | **不进模型**的体量与工程子集：**字节、启发式 token、导出/`--check`/pytest/CI** | `docs/tech_graph/gate_a_scheme1_perf_compare_backend_detail.md` §4 `#sec4-master-table`、§9 `#sec9-perf-backend` |

**关键结论**：轴 I 的 A/B **不是**「JSON 文件 vs Mermaid 文件」；轴 II **才是**「静态 `graph.json` vs Mermaid 语料」的载荷对比，但 **不包含**「多轮对话里 LLM 找入口/影响面」的行为实验。

---

## 2. 轴 I：Prompt A/B 演进摘要（V1 → Hybrid）

来源：`docs/diary/test/compare_three_versions_summary.md`（以下数字与定性以该文为准）。

### 2.1 V1（基线）

- **问题**：时间自报失真、token 换算系数不一致 → **不可直接比较**。
- **价值**：建立「全量深读」vs「索引导航」两条极端路径的产出形态差异。

### 2.2 V2（统一口径）

- **统一**：输入「每行 12 tokens」、输出「4 字符 ≈ 1 token」；时间按结果文件自报拆分（仍为人/会话级粗测）。
- **量化**：B ~**68.5k** total tokens，A ~**75k** → B 约 **省 8.7%**；时间 A ~**28min**，B ~**36min** → **省 token ≠ 省时间**（B 含读图谱刚性成本）。

### 2.3 V3 + Patch（KPI 加权 + 门禁收敛）

- **KPI 权重**：**P1 易交接 40% > P2 可靠性 35% > P3 省钱 15% > P4 省时 10%**（与 `compare_core_A_vs_B_v3_patch.md` 一致）。
- **Patch 要点**：A 侧禁用图谱正文但放行 **manifest/contract JSON** 与 CI 叙事，与 B 在「门禁必做」上收敛；差异更多落在 **信息形态**（实现讲义 vs 索引 + 防漂移）。
- **Patch 量化（自报）**：P3 **B 胜**（A ~**92.9k**，B ~**67.4k**）；P4 **A 胜**（A ~**33min**，B ~**60min**，读图谱 ~**25min** 为显式增量）；P2 **B 略胜**；P1 **依场景分裂**。
- **落地策略**：**Hybrid V1** — `docs/diary/test/prompt_AB_hybrid_v1.md` + `result_AB_hybrid_v1.md`，对抗式二选一退场。

### 2.4 轴 I 未覆盖（显式缺口）

- **多轮对话**、**轮与轮刻意低交集**、**首 token / 墙钟与 API 计费字段严格对齐** 等：旧 diary 实验 **未系统化**；若要做，见本目录 [`01_experiment_json_vs_mermaid_kpi_v1.md`](./01_experiment_json_vs_mermaid_kpi_v1.md)。

---

## 3. 轴 II：闸口 A 静态 A/B（2026-05-15 已签收）

- **任务单（done）**：`docs/tasks/done/task_engineering_tech_graph_gate_a_perf_compare_v1.md`（`freeze_id`、`test_strategy`、failure_paths 等以 task 为准）。
- **主表数字（示例，单一真值在专文）**：载荷 A `wc -c` **20224**；B `B.bytes_utf8` **20953**；启发式 `heuristic_tokens` A **5056** / B **5026**，ratio **0.9941**；§3.2 浏览器向 **N/A**（无用户页大图谱 Mermaid 产品确认前不得作主结论依据）。
- **与轴 I 关系**：轴 II 回答「**塞进上下文之前** 两种形态各有多重、工程侧多快」；**不回答**「模型读完后能否找对入口/影响面」。

---

## 4. 本目录后续文档

| 文件 | 内容 |
|------|------|
| [`01_experiment_json_vs_mermaid_kpi_v1.md`](./01_experiment_json_vs_mermaid_kpi_v1.md) | 在 **轴 II 的两种主载荷** 下，用 **V3 KPI** 做 **LLM 行为向** 新实验（冷启动 / 多轮 / 少交集）的协议草案 |
| [`02_minimal_first_step_v1.md`](./02_minimal_first_step_v1.md) | 最小可跑：**1 题 × A/B × 仅 S0** |
| [`../../_staging/jsonPKmermaid-rubric-demo/`](../../_staging/jsonPKmermaid-rubric-demo/) | Rubric `examples_builtin` 演示（**非** JSON/Mermaid 对比） |

---

## 给 Cursor 的稳定关键词

`jsonPKmermaid`、轴 I、轴 II、`compare_three_versions_summary`、`gate_a_scheme1_perf_compare_backend_detail`、V3 KPI、Hybrid V1、`freeze_id`
