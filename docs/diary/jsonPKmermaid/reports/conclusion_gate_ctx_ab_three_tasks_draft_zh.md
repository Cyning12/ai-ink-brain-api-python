# 三题 S0 总表 — JSON vs Mermaid 草案（非最终签收）

> **状态**：`draft`（P0-A 收口；**未定稿**）  
> **日志**：[../EXPERIMENT_LOG.md](../EXPERIMENT_LOG.md)  
> **日期**：2026-05-16

---

## 1. 实验边界（必读）

- 只评 **Agent 主上下文**：`CTX_JSON`（`graph.json`）vs `CTX_MERMAID`（`*.ai.md` 语料总串）。  
- 两 arm **均附** `_manifest.json` + `_contract_manifest.json`；**不**注入 Cursor rules。  
- **不**覆盖人读图谱、维护/export 成本。

---

## 2. 主表（canonical batch · clean 中位数 + F1）

| 题 | topic | arm | wall_s ↓ | tokens ↓ | entry F1 ↑ | impact F1 ↑ | batch |
|----|-------|-----|---------:|-----------:|-----------:|------------:|-------|
| T001 | `rag_env_embedding` | JSON | **17.4** | **12159** | **0.822** | **0.396** | [`111037`](../runs/gate_ctx_ab_v1_batch_20260516_111037/) |
| T001 | | Mermaid | 32.5 | 12609 | 0.794 | 0.325 | |
| T002 | `unified_chat_sse` | JSON | **39.0** | **12044** | 0.667 | 0.309 | [`121253`](../runs/gate_ctx_ab_v1_batch_t2_unified_sse_chain_con_20260516_121253/) |
| T002 | | Mermaid | 47.6 | 12571 | **0.939** | 0.340 | |
| T003 | `ingest_rpc` | JSON | **45.3** | **12258** | 0.909 | 0.424 | [`144300`](../runs/gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300/) |
| T003 | | Mermaid | 57.8 | 12810 | **1.000** | **0.483** | |

↓ = 越低越好；↑ = 越高越好（F1 为 `score_gold_f1.py` 启发式）。

**6/6 次 S0 `parse_ok`**（三 batch 各 3 轮 × 2 arm）。

---

## 3. 按维度粗判（非加权打分）

| 维度 | CTX_JSON | CTX_MERMAID |
|------|----------|-------------|
| **墙钟**（3/3 题中位数更低） | **3 胜** | 0 胜 |
| **total_tokens**（3/3 更低） | **3 胜** | 0 胜 |
| **entrypoints F1**（题内均值更高） | 1 胜（T001） | **2 胜**（T002、T003） |
| **impacts F1**（题内均值更高） | 1 胜（T001） | **2 胜**（T002、T003） |

**张力**：性能三维 JSON 全胜；质量 F1 **不分胜负**（入口/影响各 1:2）。  
**不能**据此签收「生产一律 JSON 主载荷」。

---

## 4. 与单题结论文的关系

| 题 | 专文 |
|----|------|
| T001 | [`conclusion_gate_ctx_ab_comprehensive_zh.md`](./conclusion_gate_ctx_ab_comprehensive_zh.md) |
| T002 | [`conclusion_t002_s0_batch_zh.md`](./conclusion_t002_s0_batch_zh.md) |
| T003 | 本表 + batch [`gold_f1.md`](../runs/gate_ctx_ab_v1_batch_T003_ingest_admin_rpc_20260516_144300/gold_f1.md) |

---

## 5. 定稿前仍须补（见实验日志 §5）

1. **S1/S2**（至少 1 题）：多轮 token 与泄漏。  
2. **决策规则**：例如 P1/P2 权重下，F1 不劣 + token 不劣 是否要求 **≥2/3 题** 同时成立。  
3. 可选：Rubric 抽样或收紧 F1（path 必填才计 TP）。

---

## 6. 草案一句话

**三题 S0 下，JSON 在墙钟与 token 上稳定略优，Mermaid 在 T002/T003 的 gold F1（尤其入口）上略优；样本小、仅冷启动、F1 为启发式——当前仅支持「继续以 graph.json 作 Agent 主载荷候选」，不支持最终选型签收。**
